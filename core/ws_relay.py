"""core/ws_relay.py — WebSocket VLESS relay بهینه‌شده"""
import asyncio
import logging
import secrets
import socket
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect

from config import RELAY_BUF
from state  import LINKS, LINKS_LOCK, connections, stats, error_logs, hourly_traffic
from core.persistence import save_state

logger = logging.getLogger("RVG.relay")


# ── Link validation ───────────────────────────────────────────────────────────
def _is_allowed(link: dict | None) -> bool:
    if not link or not link.get("active", True):
        return False
    from datetime import datetime as dt
    exp = link.get("expires_at")
    if exp:
        try:
            if dt.now() > dt.fromisoformat(exp):
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
async def _parse_vless_header(chunk: bytes) -> tuple[int, str, int, bytes]:
    """برمی‌گردونه (command, address, port, remaining_payload)"""
    if len(chunk) < 24:
        raise ValueError("chunk too small")
    pos = 1 + 16                            # version(1) + uuid(16)
    addon_len = chunk[pos]; pos += 1 + addon_len
    command   = chunk[pos]; pos += 1
    port      = int.from_bytes(chunk[pos:pos+2], "big"); pos += 2
    addr_type = chunk[pos]; pos += 1
    if addr_type == 1:                      # IPv4
        address = ".".join(str(b) for b in chunk[pos:pos+4]); pos += 4
    elif addr_type == 2:                    # Domain
        dlen    = chunk[pos]; pos += 1
        address = chunk[pos:pos+dlen].decode("utf-8", errors="ignore"); pos += dlen
    elif addr_type == 3:                    # IPv6
        ab      = chunk[pos:pos+16]; pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown addr_type: {addr_type}")
    return command, address, port, chunk[pos:]


# ── Relay coroutines ──────────────────────────────────────────────────────────
async def _ws_to_tcp(ws: WebSocket, writer: asyncio.StreamWriter,
                     conn_id: str, uid: str) -> None:
    try:
        while True:
            msg  = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            if not await _consume(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled")
                break
            stats["total_requests"] += 1
            connections[conn_id]["bytes"] += len(data)
            writer.write(data)
            # drain فقط وقتی buffer پر شده — کاهش syscall
            if writer.transport.get_write_buffer_size() > RELAY_BUF:
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


async def _tcp_to_ws(ws: WebSocket, reader: asyncio.StreamReader,
                     conn_id: str, uid: str) -> None:
    first = True
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if not await _consume(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled")
                break
            connections[conn_id]["bytes"] += len(data)
            # VLESS response: اولین پاکت هدر \x00\x00 داره
            payload = (b"\x00\x00" + data) if first else data
            first   = False
            await ws.send_bytes(payload)
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
        first_msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        _cmd, address, port, payload = await _parse_vless_header(first_chunk)

        if not await _consume(uuid, len(first_chunk)):
            await ws.close(code=1008, reason="quota/disabled")
            return

        stats["total_requests"] += 1
        connections[conn_id]["bytes"] += len(first_chunk)
        logger.info(f"➡️  [{conn_id}] → {address}:{port}")

        # ── اتصال TCP به مقصد ───────────────────────────────────────────────
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port), timeout=10.0
        )
        # TCP_NODELAY برای کاهش latency
        sock = writer.transport.get_extra_info("socket")
        if sock:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        if payload:
            writer.write(payload)
            await writer.drain()

        # ── دو relay موازی ───────────────────────────────────────────────────
        done, pending = await asyncio.wait(
            {
                asyncio.create_task(_ws_to_tcp(ws, writer, conn_id, uuid)),
                asyncio.create_task(_tcp_to_ws(ws, reader, conn_id, uuid)),
            },
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass

        asyncio.create_task(save_state())

    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        stats["total_errors"] += 1
        error_logs.append({"error": "connection timeout", "time": datetime.now().isoformat()})
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
