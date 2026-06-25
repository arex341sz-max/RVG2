"""protocols/vless.py — VLESS با همه مدهای استریم"""
from urllib.parse import quote
from .base import BaseProtocol


class VLESSProtocol(BaseProtocol):
    display_name = "VLESS"
    icon = "ti-shield-check"
    color = "#3B82F6"
    supports_tls = True
    default_tls = True
    supports_reality = True
    default_stream = "ws"

    stream_modes = {
        "ws": {
            "label": "WebSocket",
            "icon": "ti-webhook",
            "desc": "عبور از فایروال با هدر HTTP",
            "params": [
                {"key": "path",  "label": "مسیر", "placeholder": "/ws",         "default": "/ws"},
                {"key": "host",  "label": "Host",  "placeholder": "example.com", "default": ""},
            ],
        },
        "tcp": {
            "label": "TCP",
            "icon": "ti-arrows-transfer-down",
            "desc": "مستقیم و سریع",
            "params": [],
        },
        "grpc": {
            "label": "gRPC",
            "icon": "ti-binary-tree-2",
            "desc": "HTTP/2 multiplexing",
            "params": [
                {"key": "serviceName", "label": "Service Name", "placeholder": "grpc",  "default": "grpc"},
                {"key": "multiMode",   "label": "Multi Mode",   "type": "bool",         "default": True},
            ],
        },
        "httpupgrade": {
            "label": "HTTPUpgrade",
            "icon": "ti-arrow-up-circle",
            "desc": "ارتقای اتصال HTTP",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/upgrade", "default": "/upgrade"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
            ],
        },
        "xhttp": {
            "label": "XHTTP (SplitHTTP)",
            "icon": "ti-arrows-split-2",
            "desc": "جداسازی GET/POST — مقاوم بالا",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/xhttp", "default": "/xhttp"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
                {"key": "mode", "label": "Mode",  "type": "select",
                 "options": ["auto", "packet-up"], "default": "auto"},
            ],
        },
        "mkcp": {
            "label": "mKCP",
            "icon": "ti-bolt",
            "desc": "بر اساس UDP — مناسب افت پکت",
            "params": [
                {"key": "seed",       "label": "Seed",              "placeholder": "رندوم", "default": ""},
                {"key": "header",     "label": "Header Type",       "type": "select",
                 "options": ["none","srtp","utp","wechat-video","dtls","wireguard"], "default": "none"},
                {"key": "congestion", "label": "Congestion Control","type": "bool", "default": False},
            ],
        },
    }

    # ── Link generation ──────────────────────────────────────────────────────
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
        reality: bool = False,
        reality_pbk: str = "",
        reality_sid: str = "",
        reality_sni: str = "",
        reality_fingerprint: str = "chrome",
        **sp,
    ) -> str:
        p = {"encryption": "none"}
        if reality:
            p.update(security="reality", pbk=reality_pbk, sid=reality_sid,
                     sni=reality_sni or host, fp=reality_fingerprint or fingerprint, type=stream)
        elif tls:
            p.update(security="tls", sni=sni or host, fp=fingerprint, alpn=alpn, type=stream)
        else:
            p.update(security="none", type=stream)

        self._add_stream_params(p, stream, host, sp)
        q = "&".join(f"{k}={quote(str(v))}" for k, v in p.items())
        return f"vless://{uuid}@{host}:{port}?{q}#{quote(remark)}"

    # ── Xray inbound ────────────────────────────────────────────────────────
    def get_xray_inbound(self, port: int, **kw) -> dict:
        uuid   = kw.pop("uuid", "")
        stream = kw.pop("stream", "ws")
        tls    = kw.pop("tls", True)
        return {
            "listen": "127.0.0.1",      # فقط localhost — Railway پورت رو expose نمی‌کنه
            "port":   port,
            "protocol": "vless",
            "settings": {
                "clients":    [{"id": uuid, "flow": ""}],
                "decryption": "none",
            },
            "streamSettings": self._stream(stream, tls, **kw),
            "sniffing": {"enabled": True, "destOverride": ["http", "tls"]},
        }

    # ── Helpers ─────────────────────────────────────────────────────────────
    def _add_stream_params(self, p: dict, stream: str, host: str, sp: dict):
        mode = self.stream_modes.get(stream, {})
        for pdef in mode.get("params", []):
            key = pdef["key"]
            val = sp.get(key, pdef.get("default", ""))
            if val is not None and val != "" and val is not False:
                p[key] = "true" if isinstance(val, bool) and val else str(val)
        if stream in ("ws", "httpupgrade", "xhttp") and not sp.get("host"):
            p["host"] = host

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
            ss["grpcSettings"] = {
                "serviceName": kw.get("serviceName", "grpc"),
                "multiMode":   kw.get("multiMode", True),
            }
        elif stream == "httpupgrade":
            ss["httpUpgradeSettings"] = {
                "path": kw.get("path", "/upgrade"),
                "host": kw.get("host", ""),
            }
        elif stream == "xhttp":
            ss["xhttpSettings"] = {
                "path": kw.get("path", "/xhttp"),
                "host": kw.get("host", ""),
                "mode": kw.get("mode", "auto"),
            }
        elif stream == "mkcp":
            ss["kcpSettings"] = {
                "seed":        kw.get("seed", ""),
                "header":      {"type": kw.get("header", "none")},
                "congestion":  kw.get("congestion", False),
            }
        # Reality
        if kw.get("reality"):
            ss["security"] = "reality"
            ss["realitySettings"] = self._build_reality_settings(
                sni=kw.get("reality_sni", "") or kw.get("host", ""),
                pbk=kw.get("reality_pbk", ""),
                sid=kw.get("reality_sid", ""),
                fp=kw.get("reality_fingerprint", "chrome"),
            )
        elif tls:
            ss["security"] = "tls"
            ss["tlsSettings"] = self._build_tls_settings(
                sni=kw.get("sni", "") or kw.get("host", ""),
            )
        return ss
