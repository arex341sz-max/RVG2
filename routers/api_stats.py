"""routers/api_stats.py"""
import time
from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends

from auth         import require_auth
from link_manager import is_allowed, is_expired, fmt_bytes
from state        import LINKS, LINKS_LOCK, SUBS, connections, stats, error_logs, hourly_traffic
from xray_manager import get_status as xray_status_info

router = APIRouter()


def _uptime():
    s = int(time.time() - stats["start_time"])
    return f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d}"


@router.get("/stats")
async def get_stats(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)

    proto_counts: dict = defaultdict(int)
    for d in snap.values():
        if is_allowed(d):
            proto_counts[d.get("protocol", "vless")] += 1

    return {
        "active_connections": len(connections),
        "total_traffic_mb":   round(stats["total_bytes"] / (1024**2), 2),
        "total_requests":     stats["total_requests"],
        "total_errors":       stats["total_errors"],
        "uptime":             _uptime(),
        "timestamp":          datetime.now().isoformat(),
        "hourly":             dict(hourly_traffic),
        "recent_errors":      list(error_logs)[-10:],
        "links_count":        len(snap),
        "active_links":       sum(1 for l in snap.values() if is_allowed(l)),
        "expired_links":      sum(1 for l in snap.values() if is_expired(l)),
        "subs_count":         len(SUBS),
        "protocol_counts":    dict(proto_counts),
        "xray":               xray_status_info(),
    }


@router.get("/health")
async def health():
    return {
        "status":      "ok",
        "connections": len(connections),
        "uptime":      _uptime(),
        "xray":        xray_status_info()["running"],
    }
