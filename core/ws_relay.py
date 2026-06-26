"""core/ws_relay.py — WebSocket relay بهینه‌شده برای حداکثر throughput و کمترین latency"""
import asyncio
import logging
import secrets
import socket
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect

from config import RELAY_BUF, CONNECT_TIMEOUT, HANDSHAKE_TIMEOUT, DRAIN_THRESHOLD
from state  import LINKS, LINKS_LOCK, connections, stats, error_logs, hourly_traffic
from core.persistence import save_state

logger = logging.getLogger("RVG.relay")

# ── Link validation ───────────────────────────────────────────────────────────
def _is_allowed(link: dict | None) -> bool:
    if not link or not link.get("active", True):
        return False
    exp = link.get("expires_at")
    if exp:
        try:
            if datetime.now() > datetime.fromisoformat(exp):
                return False
        except Exception:
            pass
    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) >= lb:
        return False
    return True


async def _consume(uid: str, n: int) -> bool:
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if not link or not _is_allowed(link):
            return False
        link["used_bytes"]   = link.get("used_bytes", 0) + n
        stats["total_bytes"] += n
        hourly_traffic[datetime.now().strftime("%H:00")] += n
    return True


# ── VLESS header parser ───────────────────────────────────────────────────────
def _parse_vless_header(chunk: bytes) -> tuple[int, str, int, bytes]:
    """سریع‌ترین پارسر ممکن — بدون await، خالص sync"""
    if len(chunk) < 24:
        raise ValueError("chunk too small")
    pos       = 17                          # version(1) + uuid(16)
    addon_len = chunk[pos]; pos += 1 + addon_len
    command   = chunk[pos]; pos += 1
    port      = int.from_bytes(chunk[pos:pos+2], "big"); pos += 2
    addr_type = chunk[pos]; pos += 1
    if addr_type == 1:                      # IPv4
        address = ".".join(map(str, chunk[pos:pos+4])); pos += 4
    elif addr_type == 2:                    # Domain
        dlen    = chunk[pos]; pos += 1
        address = chunk[pos:pos+dlen].decode(); pos += dlen
    elif addr_type == 3:                    # IPv6
        ab      = chunk[pos:pos+16]; pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown addr_type={addr_type}")
    return command, address, port, chunk[pos:]


def _tune_socket(sock: socket.socket) -> None:
    """تنظیم socket برای کمترین latency و بیشترین throughput"""
    try:
        # TCP_NODELAY: غیرفعال کردن Nagle — ارسال فوری هر پاکت
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # SO_KEEPALIVE: تشخیص سریع قطع اتصال
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # TCP_KEEPIDLE: بعد از 10 ثانیه بی‌فعالیت keepalive بفرست
        if hasattr(socket, "TCP_KEEPIDLE"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
        # TCP_KEEPINTVL: هر 3 ثانیه یکبار
        if hasattr(socket, "TCP_KEEPINTVL"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
        # TCP_KEEPCNT: بعد از 3 بار عدم پاسخ قطع کن
        if hasattr(socket, "TCP_KEEPCNT"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
        # بافرهای socket — 512KB برای throughput بالا
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 524288)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 524288)
    except Exception:
        pass  # بعضی env‌ها همه optionها رو support نمیکنن


# ── Relay coroutines — zero-copy pipeline ────────────────────────────────────
async def _ws_to_tcp(
    ws: WebSocket,
    writer: asyncio.StreamWriter,
    conn_id: str,
    uid: str,
) -> None:
    """
    WS → TCP با حداقل overhead:
    - بدون copy غیرضروری
    - drain فقط وقتی buffer پر شده
    - batch write برای throughput بیشتر
    """
    try:
        while True:
            msg  = await ws.receive()
            mtype = msg["type"]
            if mtype == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue

            # accounting بدون lock در hot path
            stats["total_requests"] += 1
            connections[conn_id]["bytes"] += len(data)

            # async consume — quota check
            if not await _consume(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled")
                break

            writer.write(data)
            # drain فقط وقتی buffer از threshold رد شده — کاهش syscall
            if writer.transport.get_write_buffer_size() > DRAIN_THRESHOLD:
                await writer.drain()

    except (WebSocketDisconnect, asyncio.CancelledError):
        pass
    except Exception as e:
        logger.debug(f"ws→tcp [{conn_id}]: {e}")
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass


async def _tcp_to_ws(
    ws: WebSocket,
    reader: asyncio.StreamReader,
    conn_id: str,
    uid: str,
) -> None:
    """
    TCP → WS با حداقل overhead:
    - readany برای دریافت هر چقدر داده که آماده‌ست (کمترین latency)
    - VLESS response header فقط یکبار اول اضافه میشه
    """
    first = True
    try:
        while True:
            # read هر چقدر که الان آماده‌ست — نه منتظر buffer پر شدن
            data = await reader.read(RELAY_BUF)
            if not data:
                break

            connections[conn_id]["bytes"] += len(data)

            if not await _consume(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled")
                break

            if first:
                # VLESS response header: version(1) + addon_length(1)
                await ws.send_bytes(b"\x00\x00" + data)
                first = False
            else:
                await ws.send_bytes(data)

    except (WebSocketDisconnect, asyncio.CancelledError):
        pass
    except Exception as e:
        logger.debug(f"tcp→ws [{conn_id}]: {e}")


# ── Main handler ──────────────────────────────────────────────────────────────
async def handle_ws(ws: WebSocket, uuid: str) -> None:
    await ws.accept()

    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not _is_allowed(link):
        logger.warning(f"🚫 WS rejected uuid={uuid[:8]}…")
        await ws.close(code=1008, reason="not authorized")
        return

    conn_id = secrets.token_urlsafe(6)
    connections[conn_id] = {
        "uuid":         uuid,
        "connected_at": datetime.now().isoformat(),
        "bytes":        0,
    }
    logger.info(f"✅ WS [{conn_id}] uuid={uuid[:8]}… total={len(connections)}")
    writer = None

    try:
        # ── اولین پاکت (VLESS header) ────────────────────────────────────────
        first_msg = await asyncio.wait_for(ws.receive(), timeout=HANDSHAKE_TIMEOUT)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        # sync parse — بدون await
        _cmd, address, port, payload = _parse_vless_header(first_chunk)

        if not await _consume(uuid, len(first_chunk)):
            await ws.close(code=1008, reason="quota/disabled")
            return

        stats["total_requests"] += 1
        connections[conn_id]["bytes"] += len(first_chunk)
        logger.info(f"➡️  [{conn_id}] → {address}:{port}")

        # ── اتصال TCP به مقصد ───────────────────────────────────────────────
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port), timeout=CONNECT_TIMEOUT
        )

        # tune socket برای حداکثر performance
        sock = writer.transport.get_extra_info("socket")
        if sock:
            _tune_socket(sock)

        # ارسال payload اولیه بدون تأخیر
        if payload:
            writer.write(payload)
            await writer.drain()

        # ── دو relay موازی — asyncio.gather برای overhead کمتر ─────────────
        await asyncio.gather(
            _ws_to_tcp(ws, writer, conn_id, uuid),
            _tcp_to_ws(ws, reader, conn_id, uuid),
            return_exceptions=True,
        )

        asyncio.create_task(save_state())

    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        stats["total_errors"] += 1
        error_logs.append({"error": "timeout", "time": datetime.now().isoformat()})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
        logger.error(f"WS error [{conn_id}]: {exc}")
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        connections.pop(conn_id, None)
        logger.info(f"🔌 WS closed [{conn_id}] total={len(connections)}")
