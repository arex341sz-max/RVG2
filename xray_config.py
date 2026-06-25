"""xray_config.py — نسخه بسیار ساده و پایدار"""
import json
import logging
from pathlib import Path

from config    import XRAY_MAIN_CFG, XRAY_PORT_BASE
from state     import LINKS, LINKS_LOCK
from protocols import get_protocol

logger = logging.getLogger("RVG.xray_config")

_PORT_MAP = {}
_NEXT_PORT = XRAY_PORT_BASE


def get_port_map():
    return dict(_PORT_MAP)


async def build_xray_config():
    async with LINKS_LOCK:
        snapshot = dict(LINKS)

    inbounds = []
    for uuid, link in snapshot.items():
        if not link.get("active", True):
            continue
        try:
            proto = get_protocol(link.get("protocol", "vless"))
            inbound = proto.get_xray_inbound(
                port=10000,  # پورت ثابت برای تست
                uuid=uuid,
                password=link.get("secret", uuid),
                stream=link.get("stream", "ws"),
                tls=True,
                sni="localhost"
            )
            inbound["tag"] = f"in-{uuid[:8]}"
            inbounds.append(inbound)
        except Exception as e:
            logger.warning(f"Skip {uuid}: {e}")

    if not inbounds:
        inbounds = [{
            "tag": "placeholder",
            "listen": "127.0.0.1",
            "port": 10000,
            "protocol": "dokodemo-door",
            "settings": {"address": "127.0.0.1", "port": 1},
            "sniffing": {"enabled": True}
        }]

    config = {
        "log": {"loglevel": "warning"},
        "inbounds": inbounds,
        "outbounds": [
            {"protocol": "freedom", "tag": "direct"},
            {"protocol": "blackhole", "tag": "block"}
        ],
        "routing": {
            "rules": [
                {"type": "field", "outboundTag": "block", "ip": ["geoip:private"]},
                {"type": "field", "outboundTag": "direct", "network": "tcp,udp"}
            ]
        }
    }
    return config


async def write_xray_config():
    config = await build_xray_config()
    path = Path(XRAY_MAIN_CFG)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    logger.info(f"✅ Config written with {len(config['inbounds'])} inbounds")
    return str(path)
