"""core/ws_relay.py — WebSocket relay
دو حالت:
  1. Default link (VLESS/WS): FastAPI مستقیم VLESS relay می‌کنه
  2. بقیه لینک‌ها: FastAPI به عنوان WS proxy عمل می‌کنه — WS کلاینت → Xray WS
"""
import asyncio
import logging
import secrets
import socket
from datetime import datetime

import websockets
import websockets.exceptions
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


# ── Socket tuning ─────────────────────────────────────────────────────────────
def _tune_socket(sock: socket.socket) -> None:
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if hasattr(socket, "TCP_KEEPIDLE"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
        if hasattr(socket, "TCP_KEEPINTVL"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
        if hasattr(socket, "TCP_KEEPCNT"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 524288)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 524288)
    except Exception:
        pass


# ── VLESS header parser ───────────────────────────────────────────────────────
def _parse_vless_header(chunk: bytes) -> tuple[int, str, int, bytes]:
    if len(chunk) < 24:
        raise ValueError("chunk too small")
    pos       = 17
    addon_len = chunk[pos]; pos += 1 + addon_len
    command   = chunk[pos]; pos += 1
    port      = int.from_bytes(chunk[pos:pos+2], "big"); pos += 2
    addr_type = chunk[pos]; pos += 1
    if addr_type == 1:
        address = ".".join(map(str, chunk[pos:pos+4])); pos += 4
    elif addr_type == 2:
        dlen    = chunk[pos]; pos += 1
        address = chunk[pos:pos+dlen].decode(); pos += dlen
    elif addr_type == 3:
        ab      = chunk[pos:pos+16]; pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown addr_type={addr_type}")
    return command, address, port, chunk[pos:]


# ── Relay: WS ↔ TCP (برای default VLESS link) ────────────────────────────────
async def _ws_to_tcp(
    ws: WebSocket,
    writer: asyncio.StreamWriter,
    conn_id: str,
    uid: str,
) -> None:
    try:
        while True:
            msg   = await ws.receive()
            mtype = msg["type"]
            if mtype == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            stats["total_requests"] += 1
            connections[conn_id]["bytes"] += len(data)
            if not await _consume(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled")
                break
            writer.write(data)
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
    vless_response: bool = False,
) -> None:
    first = vless_response
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            connections[conn_id]["bytes"] += len(data)
            if not await _consume(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled")
                break
            if first:
                await ws.send_bytes(b"\x00\x00" + data)
                first = False
            else:
                await ws.send_bytes(data)
    except (WebSocketDisconnect, asyncio.CancelledError):
        pass
    except Exception as e:
        logger.debug(f"tcp→ws [{conn_id}]: {e}")


# ── Default VLESS link handler ────────────────────────────────────────────────
async def _handle_default_vless(ws: WebSocket, uuid: str, conn_id: str) -> None:
    writer = None
    try:
        first_msg = await asyncio.wait_for(ws.receive(), timeout=HANDSHAKE_TIMEOUT)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        _cmd, address, port, payload = _parse_vless_header(first_chunk)

        if not await _consume(uuid, len(first_chunk)):
            await ws.close(code=1008, reason="quota/disabled")
            return

        stats["total_requests"] += 1
        connections[conn_id]["bytes"] += len(first_chunk)
        logger.info(f"➡️  [{conn_id}] default VLESS → {address}:{port}")

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port), timeout=CONNECT_TIMEOUT
        )
        sock = writer.transport.get_extra_info("socket")
        if sock:
            _tune_socket(sock)

        if payload:
            writer.write(payload)
            await writer.drain()

        await asyncio.gather(
            _ws_to_tcp(ws, writer, conn_id, uuid),
            _tcp_to_ws(ws, reader, conn_id, uuid, vless_response=True),
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
        logger.error(f"default VLESS error [{conn_id}]: {exc}")
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass


# ── Xray WS proxy handler ─────────────────────────────────────────────────────
async def _handle_xray_ws_proxy(
    client_ws: WebSocket,
    uuid: str,
    conn_id: str,
    xray_port: int,
    ws_path: str,
) -> None:
    """
    کلاینت WS → FastAPI → Xray WS (روی 127.0.0.1:xray_port)
    FastAPI به عنوان WS bridge عمل می‌کنه.
    """
    xray_url = f"ws://127.0.0.1:{xray_port}{ws_path}"
    logger.info(f"🔀 [{conn_id}] WS bridge → {xray_url}")

    xray_ws = None
    try:
        # وصل شدن به Xray WS
        xray_ws = await asyncio.wait_for(
            websockets.connect(
                xray_url,
                ping_interval=None,
                ping_timeout=None,
                max_size=16 * 1024 * 1024,
                open_timeout=CONNECT_TIMEOUT,
            ),
            timeout=CONNECT_TIMEOUT,
        )

        async def client_to_xray():
            try:
                while True:
                    msg  = await client_ws.receive()
                    mtype = msg["type"]
                    if mtype == "websocket.disconnect":
                        break
                    data = msg.get("bytes")
                    text = msg.get("text")
                    if data:
                        connections[conn_id]["bytes"] += len(data)
                        if not await _consume(uuid, len(data)):
                            break
                        await xray_ws.send(data)
                    elif text:
                        encoded = text.encode()
                        connections[conn_id]["bytes"] += len(encoded)
                        if not await _consume(uuid, len(encoded)):
                            break
                        await xray_ws.send(text)
            except (WebSocketDisconnect, asyncio.CancelledError):
                pass
            except websockets.exceptions.ConnectionClosed:
                pass
            except Exception as e:
                logger.debug(f"client→xray [{conn_id}]: {e}")
            finally:
                try:
                    await xray_ws.close()
                except Exception:
                    pass

        async def xray_to_client():
            try:
                async for message in xray_ws:
                    if isinstance(message, bytes):
                        connections[conn_id]["bytes"] += len(message)
                        if not await _consume(uuid, len(message)):
                            break
                        await client_ws.send_bytes(message)
                    elif isinstance(message, str):
                        encoded = message.encode()
                        connections[conn_id]["bytes"] += len(encoded)
                        if not await _consume(uuid, len(encoded)):
                            break
                        await client_ws.send_text(message)
            except (WebSocketDisconnect, asyncio.CancelledError):
                pass
            except websockets.exceptions.ConnectionClosed:
                pass
            except Exception as e:
                logger.debug(f"xray→client [{conn_id}]: {e}")

        stats["total_requests"] += 1
        await asyncio.gather(
            client_to_xray(),
            xray_to_client(),
            return_exceptions=True,
        )
        asyncio.create_task(save_state())

    except asyncio.TimeoutError:
        stats["total_errors"] += 1
        logger.warning(f"⏱ [{conn_id}] Xray WS timeout → {xray_url}")
        error_logs.append({"error": f"xray ws timeout port={xray_port}", "time": datetime.now().isoformat()})
    except ConnectionRefusedError:
        stats["total_errors"] += 1
        logger.error(f"❌ [{conn_id}] Xray not on 127.0.0.1:{xray_port} — is Xray running?")
        error_logs.append({"error": f"xray refused port={xray_port}", "time": datetime.now().isoformat()})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
        logger.error(f"Xray WS proxy error [{conn_id}]: {exc}")
    finally:
        if xray_ws:
            try:
                await xray_ws.close()
            except Exception:
                pass


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
    proto  = link.get("protocol", "vless")
    stream = link.get("stream", "ws")
    logger.info(
        f"✅ WS [{conn_id}] uuid={uuid[:8]}… "
        f"proto={proto} stream={stream} total={len(connections)}"
    )

    try:
        is_default = link.get("is_default", False)
        xray_port  = link.get("xray_port")

        if is_default and proto == "vless" and stream == "ws":
            # لینک default: FastAPI مستقیم VLESS relay
            await _handle_default_vless(ws, uuid, conn_id)

        elif xray_port and stream == "ws":
            # لینک‌های دیگه با WS transport: WS bridge به Xray
            sp       = link.get("stream_params", {})
            ws_path  = sp.get("path", f"/ws/{uuid}")
            await _handle_xray_ws_proxy(ws, uuid, conn_id, xray_port, ws_path)

        elif xray_port and stream in ("xhttp", "httpupgrade", "grpc"):
            # این transport ها HTTP-based هستن، نه WS
            # کلاینت‌ها (مثل v2rayN) معمولاً WS endpoint رو صدا نمیزنن
            # اما اگه صدا زدن، بهتره خطا بدیم تا hang کنیم
            logger.warning(
                f"⚠️  [{conn_id}] WS called for {stream} transport — "
                f"client should use HTTP endpoint instead"
            )
            await ws.close(code=1003, reason=f"use HTTP for {stream} transport")

        else:
            logger.warning(
                f"⚠️  [{conn_id}] uuid={uuid[:8]}… xray_port=None — Xray not ready"
            )
            await ws.close(code=1013, reason="Xray not ready, retry in a moment")

    finally:
        connections.pop(conn_id, None)
        logger.info(f"🔌 WS closed [{conn_id}] total={len(connections)}")


# ── HTTP proxy برای XHTTP/HTTPUpgrade ────────────────────────────────────────
async def handle_http_proxy(
    uuid: str, method: str, path: str,
    headers: dict, body: bytes, xray_port: int,
) -> tuple[int, dict, bytes]:
    """HTTP request رو به Xray local port forward می‌کنه"""
    import httpx
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.request(
                method=method,
                url=f"http://127.0.0.1:{xray_port}{path}",
                headers={k: v for k, v in headers.items()
                         if k.lower() not in ("host", "content-length")},
                content=body,
            )
            return resp.status_code, dict(resp.headers), resp.content
    except Exception as e:
        logger.error(f"HTTP proxy error uuid={uuid[:8]}: {e}")
        return 502, {}, b"Bad Gateway"
