"""link_manager.py — توابع کمکی CRUD لینک‌ها"""
import hashlib
import secrets
from datetime import datetime, timedelta

from protocols import get_protocol, list_protocols
from state     import LINKS, LINKS_LOCK, SUBS, SUBS_LOCK

PROTOCOLS_INFO = list_protocols()


# ── UUID / Secret ─────────────────────────────────────────────────────────────
def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def generate_secret(protocol: str) -> str:
    if protocol in ("vless", "vmess"):
        return generate_uuid()
    return secrets.token_urlsafe(24)


# ── Helpers ───────────────────────────────────────────────────────────────────
def parse_size(value: float, unit: str) -> int:
    u = unit.upper()
    if u == "GB": return int(value * 1024**3)
    if u == "MB": return int(value * 1024**2)
    if u == "KB": return int(value * 1024)
    return int(value)


def fmt_bytes(b: int) -> str:
    if b < 1024:        return f"{b} B"
    if b < 1024**2:     return f"{b/1024:.1f} KB"
    if b < 1024**3:     return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"


def is_expired(link: dict) -> bool:
    exp = link.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(exp)
    except Exception:
        return False


def is_allowed(link: dict | None) -> bool:
    if link is None:
        return False
    if not link.get("active", True):
        return False
    if is_expired(link):
        return False
    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) >= lb:
        return False
    return True


def protocol_defaults(protocol: str) -> dict:
    info = PROTOCOLS_INFO.get(protocol, {})
    return {
        "protocol":           protocol,
        "stream":             info.get("default_stream", "tcp"),
        "tls":                info.get("default_tls", True),
        "stream_params":      {},
        "reality":            False,
        "reality_pbk":        "",
        "reality_sid":        "",
        "reality_sni":        "",
        "reality_fingerprint":"chrome",
        "sni":                "",
        "fingerprint":        "chrome",
        "alpn":               "h3" if protocol == "hysteria2" else "http/1.1",
    }


def generate_link_url(link: dict, host: str) -> str:
    protocol_name = link.get("protocol", "vless")
    try:
        proto = get_protocol(protocol_name)
        # کلیدهایی که صریح پاس میشن را از stream_params حذف کن تا تکراری نشن
        _explicit = {"password", "uuid", "host", "port", "stream", "tls", "sni",
                     "fingerprint", "alpn", "remark", "reality", "reality_pbk",
                     "reality_sid", "reality_sni", "reality_fingerprint"}
        sp = {k: v for k, v in link.get("stream_params", {}).items() if k not in _explicit}
        return proto.generate_link(
            password=link.get("secret", link["uuid"]),
            uuid=link["uuid"],
            host=host,
            port=link.get("port", 443),
            stream=link.get("stream", "ws"),
            tls=link.get("tls", True),
            sni=link.get("sni", ""),
            fingerprint=link.get("fingerprint", "chrome"),
            alpn=link.get("alpn", "http/1.1"),
            remark=f"RVG-{link.get('label', '')}",
            reality=link.get("reality", False),
            reality_pbk=link.get("reality_pbk", ""),
            reality_sid=link.get("reality_sid", ""),
            reality_sni=link.get("reality_sni", ""),
            reality_fingerprint=link.get("reality_fingerprint", "chrome"),
            **sp,
        )
    except Exception as e:
        import logging
        logging.getLogger("RVG.link_manager").error(f"generate_link_url failed for {protocol_name}: {e}")
        return ""
