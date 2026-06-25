"""state.py — shared in-memory state (یک نقطه مرکزی برای همه داده‌ها)"""
import asyncio
import time
from collections import deque, defaultdict

# ── Data stores ───────────────────────────────────────────────────────────────
LINKS: dict = {}   # { uuid: {...} }
SUBS:  dict = {}   # { sub_id: {...} }
AUTH:  dict = {}   # { password_hash: str }

LINKS_LOCK = asyncio.Lock()
SUBS_LOCK  = asyncio.Lock()

# ── Runtime stats ─────────────────────────────────────────────────────────────
stats: dict = {
    "total_bytes":    0,
    "total_requests": 0,
    "total_errors":   0,
    "start_time":     time.time(),
}
error_logs: deque   = deque(maxlen=100)
hourly_traffic: dict = defaultdict(int)

# ── Active WS connections ─────────────────────────────────────────────────────
connections: dict = {}   # { conn_id: {uuid, connected_at, bytes} }

# ── Sessions ──────────────────────────────────────────────────────────────────
SESSIONS:      dict = {}
SESSIONS_LOCK  = asyncio.Lock()
