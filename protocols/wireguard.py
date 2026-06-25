"""protocols/wireguard.py"""
from urllib.parse import quote
from .base import BaseProtocol


class WireGuardProtocol(BaseProtocol):
    display_name = "WireGuard"
    icon = "ti-shield"
    color = "#EC4899"
    supports_tls = False
    default_tls = False
    supports_reality = False
    default_stream = "udp"

    stream_modes = {
        "udp": {
            "label": "UDP Tunnel",
            "icon": "ti-bolt",
            "desc": "WireGuard UDP خودکار",
            "params": [
                {"key": "mtu",      "label": "MTU",               "placeholder": "1420",   "default": "1420"},
                {"key": "reserved", "label": "Reserved (کاما جدا)","placeholder": "0,0,0", "default": "0,0,0"},
            ],
        },
    }

    def generate_link(self, password: str, host: str, port: int,
                      public_key: str = "", preshared_key: str = "",
                      reserved: str = "0,0,0", mtu: str = "1420",
                      remark: str = "RVG", **kw) -> str:
        p = {"publickey": public_key, "type": "wireguard", "mtu": mtu}
        if preshared_key:
            p["presharedkey"] = preshared_key
        if reserved and reserved != "0,0,0":
            p["reserved"] = reserved
        q = "&".join(f"{k}={quote(str(v))}" for k, v in p.items())
        return f"wireguard://{password}@{host}:{port}?{q}#{quote(remark)}"

    def get_xray_inbound(self, port: int, **kw) -> dict:
        reserved_list = [0, 0, 0]
        try:
            reserved_list = [int(x.strip()) for x in kw.get("reserved", "0,0,0").split(",")]
        except Exception:
            pass
        while len(reserved_list) < 3:
            reserved_list.append(0)
        return {
            "listen":   "0.0.0.0",
            "port":     port,
            "protocol": "wireguard",
            "settings": {
                "secretKey": kw.get("password", ""),
                "peers": [{
                    "publicKey":    kw.get("public_key", ""),
                    "presharedKey": kw.get("preshared_key", ""),
                    "reserved":     reserved_list[:3],
                }],
                "mtu": int(kw.get("mtu", 1420)),
            },
        }
