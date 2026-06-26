"""xray_config.py — تولید Xray config با inbound های درست"""
import json
import logging
from datetime import datetime
from pathlib import Path

from config    import XRAY_MAIN_CFG, XRAY_PORT_BASE, XRAY_PORT_MAX
from state     import LINKS, LINKS_LOCK
from protocols import get_protocol

logger = logging.getLogger("RVG.xray_config")

_PORT_MAP: dict[str, int] = {}
_NEXT_PORT = XRAY_PORT_BASE


def get_port_map() -> dict:
    return dict(_PORT_MAP)


def _assign_port(uuid: str) -> int:
    global _NEXT_PORT
    if uuid not in _PORT_MAP:
        if _NEXT_PORT > XRAY_PORT_MAX:
            raise RuntimeError(f"Port pool exhausted (max={XRAY_PORT_MAX})")
        _PORT_MAP[uuid] = _NEXT_PORT
        _NEXT_PORT += 1
    return _PORT_MAP[uuid]


def _is_allowed(link: dict) -> bool:
    if not link.get("active", True):
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


async def build_xray_config() -> dict:
    """
    Config کامل Xray رو می‌سازه و همزمان xray_port رو در LINKS ذخیره می‌کنه.
    """
    async with LINKS_LOCK:
        snapshot = {k: dict(v) for k, v in LINKS.items()}

    inbounds = []
    port_assignments: dict[str, int] = {}

    for uuid, link in snapshot.items():
        # لینک default رو FastAPI مستقیم handle می‌کنه
        if link.get("is_default", False):
            continue

        if not _is_allowed(link):
            continue

        port = link.get("xray_port") or _assign_port(uuid)
        port_assignments[uuid] = port

        try:
            proto   = get_protocol(link.get("protocol", "vless"))
            inbound = proto.get_xray_inbound(
                port=port,
                uuid=uuid,
                password=link.get("secret", uuid),
                stream=link.get("stream", "ws"),
                tls=link.get("tls", True),
                sni=link.get("sni", "") or "",
                reality=link.get("reality", False),
                reality_pbk=link.get("reality_pbk", ""),
                reality_sid=link.get("reality_sid", ""),
                reality_sni=link.get("reality_sni", ""),
                reality_fingerprint=link.get("reality_fingerprint", "chrome"),
                **link.get("stream_params", {}),
            )
            inbound["tag"] = f"in-{uuid[:8]}"

            # ✅ KEY FIX: Xray فقط روی localhost گوش میده
            # Railway فقط یه پورت public داره — FastAPI ترافیک رو forward می‌کنه
            inbound["listen"] = "127.0.0.1"

            inbounds.append(inbound)
            logger.debug(
                f"  inbound: {link.get('protocol')}/{link.get('stream')} "
                f"uuid={uuid[:8]} → 127.0.0.1:{port}"
            )
        except Exception as e:
            logger.warning(f"Skip inbound {uuid[:8]}: {e}")

    # ✅ xray_port رو در LINKS ذخیره کن (با lock)
    if port_assignments:
        async with LINKS_LOCK:
            for uuid, port in port_assignments.items():
                if uuid in LINKS:
                    LINKS[uuid]["xray_port"] = port

    if not inbounds:
        inbounds = [{
            "tag":      "placeholder",
            "listen":   "127.0.0.1",
            "port":     10000,
            "protocol": "dokodemo-door",
            "settings": {"address": "127.0.0.1", "port": 1, "network": "tcp"},
        }]

    logger.info(f"📋 Xray config: {len(inbounds)} inbound(s)")
    for ib in inbounds:
        if ib.get("tag") != "placeholder":
            logger.info(
                f"   → {ib.get('protocol')} on 127.0.0.1:{ib.get('port')} "
                f"[{ib.get('tag')}]"
            )

    return {
        "log": {"loglevel": "warning"},
        "inbounds": inbounds,
        "outbounds": [
            {"protocol": "freedom",   "settings": {}, "tag": "direct"},
            {"protocol": "blackhole", "settings": {"response": {"type": "none"}}, "tag": "block"},
        ],
        "routing": {
            "domainStrategy": "IPIfNonMatch",
            "rules": [
                # ✅ حذف block برای 127.0.0.0/8 — Xray outbound نیاز به local داره
                {"type": "field", "outboundTag": "block", "ip": ["geoip:private"]},
                {"type": "field", "outboundTag": "direct", "network": "tcp,udp"},
            ],
        },
    }


async def write_xray_config() -> str:
    config   = await build_xray_config()
    path     = Path(XRAY_MAIN_CFG)
    path.parent.mkdir(parents=True, exist_ok=True)
    json_str = json.dumps(config, ensure_ascii=False, indent=2)
    json.loads(json_str)  # validate
    with open(path, "w", encoding="utf-8") as f:
        f.write(json_str)
    logger.info(f"✅ Xray config written → {path}")
    return str(path)
