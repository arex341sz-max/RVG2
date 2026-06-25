"""protocols/hysteria2.py"""
from urllib.parse import quote
from .base import BaseProtocol


class Hysteria2Protocol(BaseProtocol):
    display_name = "Hysteria2"
    icon = "ti-flame"
    color = "#F59E0B"
    supports_tls = True
    default_tls = True
    supports_reality = False
    default_stream = "quic"

    stream_modes = {
        "quic": {
            "label": "QUIC (TLS)",
            "icon": "ti-bolt",
            "desc": "UDP/QUIC خودکار",
            "params": [
                {"key": "obfs",       "label": "Obfs Password",     "placeholder": "خالی=بدون obfs", "default": ""},
                {"key": "salamander", "label": "Salamander Obfs",    "type": "bool",                  "default": False},
                {"key": "up_mbps",    "label": "آپلود (Mbps)",       "placeholder": "0=∞",            "default": "0"},
                {"key": "down_mbps",  "label": "دانلود (Mbps)",      "placeholder": "0=∞",            "default": "0"},
            ],
        },
    }

    def generate_link(self, password: str, host: str, port: int,
                      sni: str = "", alpn: str = "h3", remark: str = "RVG",
                      obfs: str = "", salamander: bool = False,
                      up_mbps: str = "0", down_mbps: str = "0", **kw) -> str:
        p = {"security": "tls", "sni": sni or host, "type": "quic", "alpn": alpn}
        if salamander and obfs:
            p["obfs"] = "salamander"
            p["obfs-password"] = obfs
        if up_mbps and up_mbps != "0":
            p["upmbps"] = up_mbps
        if down_mbps and down_mbps != "0":
            p["downmbps"] = down_mbps
        q = "&".join(f"{k}={quote(str(v))}" for k, v in p.items())
        return f"hysteria2://{password}@{host}:{port}?{q}#{quote(remark)}"

    def get_xray_inbound(self, port: int, **kw) -> dict:
        inbound = {
            "listen": "0.0.0.0",   # Hysteria2 باید مستقیم expose بشه (UDP)
            "port":   port,
            "protocol": "hysteria2",
            "settings": {
                "clients": [{"password": kw.get("password", "")}],
                "ignoreClientBandwidth": True,
            },
            "streamSettings": {
                "network":  "quic",
                "security": "tls",
                "tlsSettings": {
                    "serverName":   kw.get("sni", ""),
                    "certificates": [{"certificateFile": "/data/certs/cert.pem",
                                      "keyFile":         "/data/certs/key.pem"}],
                    "alpn": ["h3"],
                },
            },
            "sniffing": {"enabled": True, "destOverride": ["http", "tls"]},
        }
        if kw.get("salamander") and kw.get("obfs"):
            inbound["settings"]["obfs"] = {"type": "salamander", "password": kw["obfs"]}
        return inbound
