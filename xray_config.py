"""xray_config.py"""
import json
import logging
from pathlib import Path
from datetime import datetime

from config    import XRAY_MAIN_CFG, XRAY_PORT_BASE, XRAY_PORT_MAX
from state     import LINKS, LINKS_LOCK
from protocols import get_protocol

logger = logging.getLogger("RVG.xray_config")

_PORT_MAP: dict[str, int] = {}
_NEXT_PORT = XRAY_PORT_BASE


def assign_port(uuid: str) -> int:
    global _NEXT_PORT
    if uuid in _PORT_MAP:
        return _PORT_MAP[uuid]
    port = _NEXT_PORT
    _PORT_MAP[uuid] = port
    _NEXT_PORT += 1
    if _NEXT_PORT > XRAY_PORT_MAX:
        _NEXT_PORT = XRAY_PORT_BASE
    return port


def _is_allowed(link: dict) -> bool:
    if not link.get("active", True):
        return False
    exp = link.get("expires_at")
    if exp:
        try:
            if datetime.now() > datetime.fromisoformat(exp):
                return False
        except:
            pass
    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) >= lb:
        return False
    return True


async def build_xray_config(snapshot: dict | None = None) -> dict:
    if snapshot is None:
        async with LINKS_LOCK:
            snapshot = dict(LINKS)

    inbounds = []

    for uuid, link in snapshot.items():
        if not _is_allowed(link):
            continue
        protocol_name = link.get("protocol", "vless")
        stream = link.get("stream", "ws")
        tls = link.get("tls", True)
        port = link.get("xray_port") or assign_port(uuid)

        try:
            import os
            cert_ok = os.path.exists("/data/certs/cert.pem") and os.path.exists("/data/certs/key.pem")
            proto = get_protocol(protocol_name)
            inbound = proto.get_xray_inbound(
                port=port,
                uuid=uuid,
                password=link.get("secret", uuid),
                stream=stream,
                tls=tls and cert_ok,
                sni=link.get("sni", ""),
                **link.get("stream_params", {})
            )
            inbound["tag"] = f"in-{uuid[:8]}"
            inbounds.append(inbound)
        except Exception as e:
            logger.warning(f"Skip {uuid[:8]}: {e}")

    if not inbounds:
        inbounds = [{
            "tag": "placeholder",
            "listen": "127.0.0.1",
            "port": XRAY_PORT_BASE,
            "protocol": "dokodemo-door",
            "settings": {"address": "127.0.0.1", "port": 1, "network": "tcp"},
            "sniffing": {"enabled": True, "destOverride": ["http", "tls"]}
        }]

    return {
        "log": {"loglevel": "warning"},
        "inbounds": inbounds,
        "outbounds": [
            {"protocol": "freedom", "tag": "direct"},
            {"protocol": "blackhole", "tag": "block"}
        ],
        "routing": {
            "rules": [
                {"type": "field", "outboundTag": "block", "ip": ["geoip:private", "127.0.0.0/8"]},
                {"type": "field", "outboundTag": "direct", "network": "tcp,udp"}
            ]
        }
    }


async def write_xray_config() -> str:
    config = await build_xray_config()
    path = Path(XRAY_MAIN_CFG)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    logger.info(f"Xray config written: {len(config['inbounds'])} inbounds")
    return str(path)


# این تابع حتما باید باشه
def get_port_map() -> dict:
    return dict(_PORT_MAP)
