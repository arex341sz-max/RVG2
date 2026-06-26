"""main.py — RVG Gateway v10 | FastAPI + Xray subprocess"""
import asyncio
import logging
import os
import secrets
import time
from datetime import datetime

import httpx
import uvicorn
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from auth             import init_auth, is_valid_session, SESSION_COOKIE
from config           import PORT, PUBLIC_DOMAIN, XRAY_CERT_DIR, XRAY_CERT_FILE, XRAY_KEY_FILE
from core.persistence import load_state, save_state
from core.ws_relay    import handle_ws, handle_http_proxy
from link_manager     import (
    generate_uuid, protocol_defaults, generate_link_url, is_allowed, fmt_bytes, PROTOCOLS_INFO,
)
from protocols        import list_protocols, get_protocol
from routers.api_auth   import router as auth_router
from routers.api_links  import router as links_router
from routers.api_subs   import router as subs_router
from routers.api_xray   import router as xray_router
from routers.api_stats  import router as stats_router
from routers.subscriptions import router as sub_router
from state            import LINKS, LINKS_LOCK, SUBS, connections, stats
from xray_manager     import start_monitor, stop_monitor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("RVG")

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="RVG Gateway", version="10.0", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

for r in (auth_router, links_router, subs_router, xray_router, stats_router, sub_router):
    app.include_router(r)

_http: httpx.AsyncClient | None = None


def _ensure_self_signed_cert() -> bool:
    import subprocess
    if os.path.exists(XRAY_CERT_FILE) and os.path.exists(XRAY_KEY_FILE):
        logger.info(f"🔐 Cert already exists → {XRAY_CERT_DIR}/")
        return True
    os.makedirs(XRAY_CERT_DIR, exist_ok=True)
    try:
        subprocess.run(
            ["openssl", "req", "-x509", "-newkey", "rsa:2048",
             "-keyout", XRAY_KEY_FILE, "-out", XRAY_CERT_FILE,
             "-days", "3650", "-nodes", "-subj", "/CN=rvg-gateway"],
            check=True, capture_output=True, text=True,
        )
        logger.info(f"🔐 Self-signed cert generated → {XRAY_CERT_DIR}/")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ openssl failed (rc={e.returncode}): {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        logger.error("❌ openssl not found")
        return False
    except Exception as e:
        logger.error(f"❌ Cert generation error: {e}")
        return False


@app.on_event("startup")
async def startup():
    global _http
    init_auth()
    await load_state()
    await _ensure_default_link()

    cert_ok = _ensure_self_signed_cert()
    if not cert_ok:
        logger.warning("⚠️ TLS cert missing — Xray TLS inbounds will fail!")

    limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)
    _http  = httpx.AsyncClient(limits=limits, timeout=httpx.Timeout(30, connect=10),
                                follow_redirects=True)
    await start_monitor()

    logger.info(f"🚀 RVG Gateway v10 — port {PORT}")
    logger.info(f"📡 Protocols: {', '.join(PROTOCOLS_INFO)}")
    logger.info("🔀 Architecture: FastAPI(public) → Xray(127.0.0.1:10xxx)")


@app.on_event("shutdown")
async def shutdown():
    await stop_monitor()
    await save_state()
    if _http:
        await _http.aclose()


async def _ensure_default_link():
    import hashlib
    from config import SECRET_KEY
    async with LINKS_LOCK:
        if any(l.get("is_default") for l in LINKS.values()):
            return
        uid = hashlib.sha256(f"default{SECRET_KEY}".encode()).hexdigest()
        uid = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
        if uid not in LINKS:
            defaults = protocol_defaults("vless")
            LINKS[uid] = {
                "uuid":          uid,
                "secret":        uid,
                **defaults,
                "stream":        "ws",
                "label":         "لینک پیش‌فرض",
                "port":          443,
                "limit_bytes":   0,
                "used_bytes":    0,
                "created_at":    datetime.now().isoformat(),
                "active":        True,
                "expires_at":    None,
                "note":          "",
                "is_default":    True,
                "sub_id":        None,
                "xray_port":     None,   # default link توسط FastAPI handle میشه، نه Xray
                "stream_params": {"path": f"/ws/{uid}"},
            }
            asyncio.create_task(save_state())


# ── WebSocket endpoints ───────────────────────────────────────────────────────

@app.websocket("/ws/{uuid}")
async def websocket_endpoint(ws: WebSocket, uuid: str):
    await handle_ws(ws, uuid)


@app.websocket("/ws")
async def websocket_plain(ws: WebSocket):
    uuid = ws.query_params.get("uuid") or ws.query_params.get("ed")
    if not uuid:
        uuid = ws.headers.get("x-uuid") or ws.headers.get("X-UUID")
    if not uuid:
        proto_header = ws.headers.get("sec-websocket-protocol", "")
        parts = [p.strip() for p in proto_header.split(",")]
        for part in parts:
            if len(part) == 36 and part.count("-") == 4:
                uuid = part
                break
    if not uuid:
        logger.warning("🚫 WS /ws rejected — no UUID provided")
        await ws.close(code=1008, reason="UUID required")
        return
    await handle_ws(ws, uuid)


# ── Dynamic WS endpoints — بر اساس path لینک‌ها ─────────────────────────────
@app.websocket("/xhttp/{uuid}")
async def ws_xhttp(ws: WebSocket, uuid: str):
    """XHTTP transport WS endpoint"""
    await handle_ws(ws, uuid)


@app.websocket("/upgrade/{uuid}")
async def ws_httpupgrade(ws: WebSocket, uuid: str):
    """HTTPUpgrade transport WS endpoint"""
    await handle_ws(ws, uuid)


@app.websocket("/siz/{uuid}")
async def ws_siz(ws: WebSocket, uuid: str):
    """SIZ10A WS endpoint"""
    await handle_ws(ws, uuid)


# ── Catch-all WS endpoint — UUID رو از path استخراج می‌کنه ──────────────────
@app.middleware("http")
async def xray_http_proxy_middleware(request: Request, call_next):
    """
    HTTP requests رو که به Xray inbound‌ها تعلق دارن (XHTTP/HTTPUpgrade)
    به Xray local port forward می‌کنه.
    """
    path = request.url.path

    # API و dashboard رو skip کن
    if (path.startswith("/api/") or path.startswith("/sub") or
            path in ("/", "/login", "/dashboard") or path.startswith("/p/")):
        return await call_next(request)

    # پیدا کردن لینک بر اساس path
    target_link = None
    target_uuid = None

    async with LINKS_LOCK:
        for uuid, link in LINKS.items():
            if link.get("is_default"):
                continue
            sp = link.get("stream_params", {})
            link_path = sp.get("path", "")
            service   = sp.get("serviceName", "")

            if link_path and path.startswith(link_path):
                target_link = link
                target_uuid = uuid
                break
            if service and path.startswith(f"/{service}"):
                target_link = link
                target_uuid = uuid
                break

    if not target_link or not target_link.get("xray_port"):
        return await call_next(request)

    from link_manager import is_allowed as _is_allowed_link
    if not _is_allowed_link(target_link):
        return Response(status_code=403)

    xray_port = target_link["xray_port"]
    body = await request.body()
    headers = dict(request.headers)

    status, resp_headers, content = await handle_http_proxy(
        uuid=target_uuid,
        method=request.method,
        path=path,
        headers=headers,
        body=body,
        xray_port=xray_port,
    )

    # hop-by-hop headers حذف کن
    _HOP = {"connection", "keep-alive", "transfer-encoding", "te",
            "trailers", "upgrade", "content-encoding", "content-length"}
    clean_headers = {k: v for k, v in resp_headers.items() if k.lower() not in _HOP}

    return Response(content=content, status_code=status, headers=clean_headers)


# ── HTTP endpoints ────────────────────────────────────────────────────────────

@app.get("/api/protocols")
async def api_protocols():
    return {"protocols": list_protocols()}

@app.get("/api/protocols/{name}/modes")
async def api_protocol_modes(name: str):
    try:
        proto = get_protocol(name)
        return {"protocol": name, "modes": proto.stream_modes}
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(404, "پروتکل پیدا نشد")


_HOP = {"connection","keep-alive","proxy-authenticate","proxy-authorization",
        "te","trailers","transfer-encoding","upgrade","content-encoding","content-length"}

@app.api_route("/proxy/{target_url:path}",
               methods=["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"])
async def http_proxy(target_url: str, request: Request):
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    try:
        body    = await request.body()
        headers = {k: v for k, v in request.headers.items()
                   if k.lower() not in _HOP and k.lower() != "host"}
        resp = await _http.request(request.method, target_url, headers=headers, content=body)
        stats["total_bytes"]    += len(resp.content)
        stats["total_requests"] += 1
        return Response(
            content=resp.content, status_code=resp.status_code,
            headers={k: v for k, v in resp.headers.items() if k.lower() not in _HOP},
        )
    except Exception as exc:
        from fastapi import HTTPException
        raise HTTPException(502, f"Proxy error: {exc}")


@app.get("/")
async def root():
    return {"service": "RVG Gateway", "version": "10.0", "status": "active",
            "protocols": list(PROTOCOLS_INFO), "channel": "https://t.me/CodeBoxo"}

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse("/dashboard")
    from pages.login import HTML as LOGIN_HTML
    return HTMLResponse(content=LOGIN_HTML)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse("/login")
    from pages.dashboard import HTML as DASH_HTML
    return HTMLResponse(content=DASH_HTML)

@app.get("/p/{uuid_key}", response_class=HTMLResponse)
async def public_page(uuid_key: str):
    from pages.public import get_html
    return HTMLResponse(content=get_html(uuid_key))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="info", workers=1)
