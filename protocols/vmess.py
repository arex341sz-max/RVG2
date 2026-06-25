"""protocols/vmess.py — VMess"""
import json
import base64
from urllib.parse import quote
from .base import BaseProtocol


class VMessProtocol(BaseProtocol):
    display_name = "VMess"
    icon = "ti-lock"
    color = "#8B5CF6"
    supports_tls = True
    default_tls = True
    supports_reality = False
    default_stream = "ws"

    stream_modes = {
        "ws":          {"label": "WebSocket",   "icon": "ti-webhook",            "desc": "عبور از فایروال",
                        "params": [
                            {"key": "path", "label": "مسیر", "placeholder": "/ws",          "default": "/ws"},
                            {"key": "host", "label": "Host",  "placeholder": "example.com",  "default": ""},
                        ]},
        "tcp":         {"label": "TCP",          "icon": "ti-arrows-transfer-down","desc": "مستقیم", "params": []},
        "grpc":        {"label": "gRPC",         "icon": "ti-binary-tree-2",       "desc": "HTTP/2",
                        "params": [
                            {"key": "serviceName", "label": "Service Name", "placeholder": "grpc", "default": "grpc"},
                        ]},
        "httpupgrade": {"label": "HTTPUpgrade",  "icon": "ti-arrow-up-circle",     "desc": "ارتقای HTTP",
                        "params": [
                            {"key": "path", "label": "مسیر", "placeholder": "/upgrade", "default": "/upgrade"},
                            {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
                        ]},
    }

    def generate_link(
        self,
        uuid: str,
        host: str,
        port: int,
        stream: str = "ws",
        tls: bool = True,
        sni: str = "",
        fingerprint: str = "chrome",
        alpn: str = "http/1.1",
        remark: str = "RVG",
        **sp,
    ) -> str:
        vmess = {
            "v": "2", "ps": remark, "add": host, "port": str(port),
            "id": uuid, "aid": "0", "scy": "auto",
            "net": stream, "type": "none",
            "host": sp.get("host", "") or host,
            "path": sp.get("path", "") or "/",
            "tls": "tls" if tls else "none",
            "sni": sni or host, "alpn": alpn, "fp": fingerprint,
        }
        if stream == "grpc":
            vmess["path"] = sp.get("serviceName", "grpc")
            vmess["type"] = "gun"
        encoded = base64.b64encode(
            json.dumps(vmess, ensure_ascii=False).encode()
        ).decode()
        return f"vmess://{encoded}"

    def get_xray_inbound(self, port: int, **kw) -> dict:
        stream = kw.get("stream", "ws")
        tls    = kw.get("tls", True)
        return {
            "listen": "127.0.0.1",
            "port":   port,
            "protocol": "vmess",
            "settings": {
                "clients": [{"id": kw.get("uuid", ""), "alterId": 0}],
            },
            "streamSettings": self._stream(stream, tls, **kw),
            "sniffing": {"enabled": True, "destOverride": ["http", "tls"]},
        }

    def _stream(self, stream: str, tls: bool, **kw) -> dict:
        ss = {"network": stream}
        if stream == "tcp":
            ss["tcpSettings"] = {"header": {"type": "none"}}
        elif stream == "ws":
            ss["wsSettings"] = {
                "path": kw.get("path", "/ws"),
                "headers": {"Host": kw.get("host", "")} if kw.get("host") else {},
            }
        elif stream == "grpc":
            ss["grpcSettings"] = {"serviceName": kw.get("serviceName", "grpc"), "multiMode": False}
        elif stream == "httpupgrade":
            ss["httpUpgradeSettings"] = {"path": kw.get("path", "/upgrade"), "host": kw.get("host", "")}
        if tls:
            ss["security"] = "tls"
            ss["tlsSettings"] = self._build_tls_settings(sni=kw.get("sni", "") or kw.get("host", ""))
        return ss
