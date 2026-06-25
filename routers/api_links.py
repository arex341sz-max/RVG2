"""routers/api_links.py — CRUD کامل لینک‌ها"""
import asyncio
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request

from auth         import require_auth
from config       import PUBLIC_DOMAIN
from core.persistence import save_state
from link_manager import (
    generate_uuid, generate_secret, protocol_defaults,
    parse_size, fmt_bytes, is_expired, is_allowed, generate_link_url,
    PROTOCOLS_INFO,
)
from protocols    import get_protocol
from state        import LINKS, LINKS_LOCK, SUBS, SUBS_LOCK
from xray_manager import reload_xray
import os

router = APIRouter()


def _host() -> str:
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", PUBLIC_DOMAIN)


# ── Create ────────────────────────────────────────────────────────────────────
@router.post("/api/links")
async def create_link(request: Request, _=Depends(require_auth)):
    body     = await request.json()
    protocol = str(body.get("protocol", "vless")).lower().strip()
    stream   = str(body.get("stream", "")).lower().strip()
    tls      = bool(body.get("tls", True))
    label    = (body.get("label") or "لینک جدید").strip()[:60]
    note     = (body.get("note") or "").strip()[:200]
    sub_id   = body.get("sub_id") or None
    port     = int(body.get("port", 0))
    reality  = bool(body.get("reality", False))
    stream_params = body.get("stream_params", {})

    lv = float(body.get("limit_value") or 0)
    lu = body.get("limit_unit") or "GB"
    limit_bytes = 0 if lv <= 0 else parse_size(lv, lu)

    exp_days   = int(body.get("expires_days") or 0)
    expires_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None

    # ── اعتبارسنجی ───────────────────────────────────────────────────────────
    try:
        proto = get_protocol(protocol)
    except ValueError:
        raise HTTPException(400, f"پروتکل نامعتبر: {protocol}")

    if not stream:
        stream = proto.default_stream
    if stream not in proto.stream_modes:
        raise HTTPException(400, f"استریم '{stream}' برای {protocol} پشتیبانی نمی‌شود")
    if reality and not proto.supports_reality:
        raise HTTPException(400, f"Reality برای {protocol} پشتیبانی نمی‌شود")
    if not proto.supports_tls:
        tls = False

    if port == 0:
        if protocol == "hysteria2": port = 8443
        elif protocol == "wireguard": port = 51820
        elif tls: port = 443
        else: port = 80

    uid    = generate_uuid()
    secret = generate_secret(protocol)

    entry = {
        "uuid":                uid,
        "secret":              secret,
        "protocol":            protocol,
        "stream":              stream,
        "tls":                 tls,
        "stream_params":       stream_params,
        "port":                port,
        "label":               label,
        "limit_bytes":         limit_bytes,
        "used_bytes":          0,
        "created_at":          datetime.now().isoformat(),
        "active":              True,
        "expires_at":          expires_at,
        "note":                note,
        "is_default":          False,
        "sub_id":              sub_id,
        "reality":             reality,
        "reality_pbk":         body.get("reality_pbk", ""),
        "reality_sid":         body.get("reality_sid", ""),
        "reality_sni":         body.get("reality_sni", ""),
        "reality_fingerprint": body.get("reality_fingerprint", "chrome"),
        "sni":                 body.get("sni", ""),
        "fingerprint":         body.get("fingerprint", "chrome"),
        "alpn":                body.get("alpn", "h3" if protocol == "hysteria2" else "http/1.1"),
        "xray_port":           None,   # بعد از reload تعیین می‌شه
    }

    async with LINKS_LOCK:
        LINKS[uid] = entry

    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].setdefault("link_ids", [])
                if uid not in ids:
                    ids.append(uid)

    # reload Xray (بدون restart — SIGHUP)
    asyncio.create_task(reload_xray())
    asyncio.create_task(save_state())

    host     = _host()
    link_url = generate_link_url(entry, host)
    return {"uuid": uid, **entry, "expired": False,
            "link_url": link_url, "sub_url": f"https://{host}/sub/{uid}"}


# ── List ──────────────────────────────────────────────────────────────────────
@router.get("/api/links")
async def list_links(_=Depends(require_auth)):
    host = _host()
    async with LINKS_LOCK:
        snap = dict(LINKS)
    result = []
    for uid, d in snap.items():
        result.append({
            "uuid": uid, **d,
            "expired":   is_expired(d),
            "link_url":  generate_link_url(d, host),
            "sub_url":   f"https://{host}/sub/{uid}",
            "used_fmt":  fmt_bytes(d.get("used_bytes", 0)),
            "limit_fmt": "∞" if not d.get("limit_bytes") else fmt_bytes(d["limit_bytes"]),
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"links": result}


# ── Update ────────────────────────────────────────────────────────────────────
@router.patch("/api/links/{uid}")
async def update_link(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(404, "link not found")
        link    = LINKS[uid]
        old_sub = link.get("sub_id")

        for field in ("active", "label", "note", "sni", "fingerprint", "alpn",
                      "reality", "reality_pbk", "reality_sid", "reality_sni", "reality_fingerprint"):
            if field in body:
                link[field] = body[field]

        if body.get("reset_usage"):
            link["used_bytes"] = 0

        if "limit_value" in body:
            lv = float(body.get("limit_value") or 0)
            link["limit_bytes"] = 0 if lv <= 0 else parse_size(lv, body.get("limit_unit", "GB"))

        if "expires_days" in body:
            ed = int(body["expires_days"] or 0)
            link["expires_at"] = (datetime.now() + timedelta(days=ed)).isoformat() if ed > 0 else None

        if "protocol" in body:
            try:
                get_protocol(body["protocol"])
                link["protocol"] = body["protocol"].lower()
                link["secret"]   = generate_secret(link["protocol"])
            except ValueError:
                pass

        if "stream" in body:
            proto = get_protocol(link["protocol"])
            if body["stream"] in proto.stream_modes:
                link["stream"] = body["stream"]

        if "tls" in body:
            proto = get_protocol(link["protocol"])
            if proto.supports_tls:
                link["tls"] = bool(body["tls"])

        if "stream_params" in body:
            link["stream_params"] = body["stream_params"]

        if "port" in body:
            link["port"] = int(body["port"])

        new_sub = body.get("sub_id", "UNCHANGED")
        if new_sub != "UNCHANGED":
            link["sub_id"] = new_sub or None

    if new_sub != "UNCHANGED":
        async with SUBS_LOCK:
            if old_sub and old_sub in SUBS:
                ids = SUBS[old_sub].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
            if new_sub and new_sub in SUBS:
                ids = SUBS[new_sub].setdefault("link_ids", [])
                if uid not in ids:
                    ids.append(uid)

    asyncio.create_task(reload_xray())
    asyncio.create_task(save_state())
    return {"ok": True}


# ── Delete ────────────────────────────────────────────────────────────────────
@router.delete("/api/links/{uid}")
async def delete_link(uid: str, _=Depends(require_auth)):
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(404, "link not found")
        sub_id = LINKS[uid].get("sub_id")
        del LINKS[uid]

    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)

    asyncio.create_task(reload_xray())
    asyncio.create_task(save_state())
    return {"ok": True, "deleted": uid}
