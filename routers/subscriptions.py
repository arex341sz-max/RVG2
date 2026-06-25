"""routers/subscriptions.py — endpoint های subscription"""
import base64
import os
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response, JSONResponse

from auth         import hash_password, require_auth
from config       import PUBLIC_DOMAIN
from link_manager import generate_link_url, is_allowed, fmt_bytes
from state        import LINKS, LINKS_LOCK, SUBS, SUBS_LOCK, connections

router = APIRouter()


def _host():
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", PUBLIC_DOMAIN)


@router.get("/sub/{uuid}")
async def sub_single(uuid: str):
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link or not is_allowed(link):
        raise HTTPException(404, "not found or inactive")
    url = generate_link_url(link, _host())
    if not url:
        raise HTTPException(500, "link generation failed")
    content = base64.b64encode(url.encode()).decode()
    return Response(
        content=content,
        media_type="text/plain",
        headers={
            "profile-title":          quote(link["label"]),
            "support-url":            "https://t.me/CodeBoxo",
            "profile-update-interval": "12",
        },
    )


@router.get("/sub-all")
async def sub_all(_=Depends(require_auth)):
    host = _host()
    async with LINKS_LOCK:
        lines = [generate_link_url(d, host) for d in LINKS.values() if is_allowed(d)]
    lines   = [l for l in lines if l]
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain")


@router.get("/sub-group/{uuid_key}")
async def sub_group(uuid_key: str, request: Request):
    async with SUBS_LOCK:
        sub = next((s for s in SUBS.values() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        raise HTTPException(404, "not found")
    if sub.get("password_hash"):
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            raise HTTPException(403, "wrong password")
    host     = _host()
    link_ids = sub.get("link_ids", [])
    async with LINKS_LOCK:
        lines = [generate_link_url(LINKS[lid], host)
                 for lid in link_ids
                 if lid in LINKS and is_allowed(LINKS[lid])]
    lines   = [l for l in lines if l]
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(
        content=content,
        media_type="text/plain",
        headers={
            "profile-title":          quote(sub["name"]),
            "support-url":            "https://t.me/CodeBoxo",
            "profile-update-interval":"12",
        },
    )


@router.get("/api/public/sub/{uuid_key}")
async def public_sub_data(uuid_key: str, request: Request):
    async with SUBS_LOCK:
        sub_entry = next(
            ((sid, s) for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None
        )
    if not sub_entry:
        raise HTTPException(404, "not found")
    sub_id, sub = sub_entry
    has_pw = sub.get("password_hash") is not None
    if has_pw:
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            return JSONResponse({"locked": True, "name": sub["name"]})

    host     = _host()
    link_ids = sub.get("link_ids", [])
    async with LINKS_LOCK:
        snap = dict(LINKS)

    links_out   = []
    active_conns = 0
    for lid in link_ids:
        link = snap.get(lid)
        if not link:
            continue
        conn_count    = sum(1 for c in connections.values() if c.get("uuid") == lid)
        active_conns += conn_count
        links_out.append({
            "uuid":       lid,
            "label":      link["label"],
            "protocol":   link.get("protocol", "vless"),
            "stream":     link.get("stream", "ws"),
            "active":     is_allowed(link),
            "used_bytes": link.get("used_bytes", 0),
            "used_fmt":   fmt_bytes(link.get("used_bytes", 0)),
            "limit_bytes":link.get("limit_bytes", 0),
            "limit_fmt":  "∞" if not link.get("limit_bytes") else fmt_bytes(link["limit_bytes"]),
            "expires_at": link.get("expires_at"),
            "link_url":   generate_link_url(link, host),
            "sub_url":    f"https://{host}/sub/{lid}",
            "connections":conn_count,
        })

    total_used = sum(l["used_bytes"] for l in links_out)
    return {
        "locked":             False,
        "name":               sub["name"],
        "desc":               sub.get("desc", ""),
        "sub_url":            f"https://{host}/sub-group/{uuid_key}",
        "active_connections": active_conns,
        "total_used_fmt":     fmt_bytes(total_used),
        "links":              links_out,
    }
