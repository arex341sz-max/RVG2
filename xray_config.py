"""xray_config.py — تولید config صحیح برای Xray"""
import json
import logging
from datetime import datetime
from pathlib import Path

from config    import XRAY_MAIN_CFG, XRAY_PORT_BASE
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
    async with LINKS_LOCK:
        snapshot = dict(LINKS)

    inbounds = []
    for uuid, link in snapshot.items():
        if not _is_allowed(link):
            continue
        port = link.get("xray_port") or _assign_port(uuid)
        link["xray_port"] = port

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
            inbounds.append(inbound)
        except Exception as e:
            logger.warning(f"Skip inbound {uuid[:8]}: {e}")

    if not inbounds:
        inbounds = [{
            "tag":      "placeholder",
            "listen":   "127.0.0.1",
            "port":     10000,
            "protocol": "dokodemo-door",
            "settings": {"address": "127.0.0.1", "port": 1, "network": "tcp"},
        }]

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
                {"type": "field", "outboundTag": "block",
                 "ip": ["geoip:private", "127.0.0.0/8"]},
                {"type": "field", "outboundTag": "direct", "network": "tcp,udp"},
            ],
        },
    }


async def write_xray_config() -> str:
    config = await build_xray_config()
    path   = Path(XRAY_MAIN_CFG)
    path.parent.mkdir(parents=True, exist_ok=True)

    json_str = json.dumps(config, ensure_ascii=False, indent=2)
    json.loads(json_str)  # validate قبل از نوشتن

    with open(path, "w", encoding="utf-8") as f:
        f.write(json_str)

    logger.info(f"✅ Config written with {len(config['inbounds'])} inbounds")
    return str(path)
