"""protocols/vless.py — VLESS بهینه‌شده برای حداکثر سرعت"""
from urllib.parse import quote
from config import XRAY_CERT_FILE, XRAY_KEY_FILE
from .base import BaseProtocol


class VLESSProtocol(BaseProtocol):
    display_name     = "VLESS"
    icon             = "ti-shield-check"
    color            = "#3B82F6"
    supports_tls     = True
    default_tls      = True
    supports_reality = True
    default_stream   = "ws"

    stream_modes = {
        "ws": {
            "label": "WebSocket",
            "icon":  "ti-webhook",
            "desc":  "عبور از فایروال — Early Data فعال",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/ws/{uuid}", "default": "/ws"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
            ],
        },
        "xhttp": {
            "label": "XHTTP (SplitHTTP)",
            "icon":  "ti-arrows-split-2",
            "desc":  "سریع‌ترین — GET/POST جداگانه، مقاوم بالا",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/xhttp", "default": "/xhttp"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
                {"key": "mode", "label": "Mode",  "type": "select",
                 "options": ["auto", "packet-up", "stream-up"], "default": "auto"},
            ],
        },
        "grpc": {
            "label": "gRPC",
            "icon":  "ti-binary-tree-2",
            "desc":  "HTTP/2 multiplexing",
            "params": [
                {"key": "serviceName", "label": "Service Name", "placeholder": "grpc", "default": "grpc"},
                {"key": "multiMode",   "label": "Multi Mode",   "type": "bool",        "default": True},
            ],
        },
        "httpupgrade": {
            "label": "HTTPUpgrade",
            "icon":  "ti-arrow-up-circle",
            "desc":  "ارتقای HTTP — سازگاری بالا",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/upgrade", "default": "/upgrade"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
            ],
        },
        "tcp": {
            "label": "TCP",
            "icon":  "ti-arrows-transfer-down",
            "desc":  "مستقیم — کمترین overhead",
            "params": [],
        },
        "mkcp": {
            "label": "mKCP",
            "icon":  "ti-bolt",
            "desc":  "UDP — مقاوم در برابر packet loss",
            "params": [
                {"key": "seed",       "label": "Seed",         "placeholder": "رندوم", "default": ""},
                {"key": "header",     "label": "Header Type",  "type": "select",
                 "options": ["none","srtp","utp","wechat-video","dtls","wireguard"], "default": "none"},
                {"key": "congestion", "label": "Congestion",   "type": "bool", "default": False},
            ],
        },
    }

    def generate_link(self, uuid: str = "", host: str = "", port: int = 443,
                      stream: str = "ws", tls: bool = True,
                      sni: str = "", fingerprint: str = "chrome", alpn: str = "http/1.1",
                      remark: str = "RVG", reality: bool = False,
                      reality_pbk: str = "", reality_sid: str = "",
                      reality_sni: str = "", reality_fingerprint: str = "chrome",
                      **sp) -> str:
        p = {"encryption": "none"}
        if reality:
            p.update(security="reality", pbk=reality_pbk, sid=reality_sid,
                     sni=reality_sni or host, fp=reality_fingerprint or fingerprint, type=stream)
        elif tls:
            _alpn = "h3" if stream == "xhttp" else alpn
            p.update(security="tls", sni=sni or host, fp=fingerprint, alpn=_alpn, type=stream)
        else:
            p.update(security="none", type=stream)

        mode = self.stream_modes.get(stream, {})
        for pdef in mode.get("params", []):
            key = pdef["key"]
            val = sp.get(key, pdef.get("default", ""))
            if val not in (None, "", False):
                p[key] = "true" if isinstance(val, bool) and val else str(val)

        if stream == "ws":
            cur = p.get("path", "/ws")
            if cur in ("/ws", "") and uuid:
                p["path"] = f"/ws/{uuid}"
            p.setdefault("earlyDataHeaderName", "Sec-WebSocket-Protocol")
        if stream in ("ws", "xhttp", "httpupgrade") and not sp.get("host"):
            p["host"] = host

        q = "&".join(f"{k}={quote(str(v))}" for k, v in p.items())
        return f"vless://{uuid}@{host}:{port}?{q}#{quote(remark)}"

    def get_xray_inbound(self, port: int, **kw) -> dict:
        uuid   = kw.get("uuid", "")
        stream = kw.pop("stream", "ws")
        tls    = kw.pop("tls", True)
        flow   = "xtls-rprx-vision" if stream == "tcp" and kw.get("reality") else ""
        return {
            "listen":   "0.0.0.0",
            "port":     port,
            "protocol": "vless",
            "settings": {
                "clients":    [{"id": uuid, "flow": flow}],
                "decryption": "none",
            },
            "streamSettings": self._build_stream(stream, tls, uuid=uuid, **kw),
            "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"]},
        }

    def _build_stream(self, stream: str, tls: bool, **kw) -> dict:
        uuid = kw.get("uuid", "")
        ss: dict = {"network": stream}

        if stream == "tcp":
            ss["tcpSettings"] = {"header": {"type": "none"}}

        elif stream == "ws":
            raw  = kw.get("path", "/ws")
            path = f"/ws/{uuid}" if raw in ("/ws", "") and uuid else raw
            ss["wsSettings"] = {
                "path": path,
                "headers":             {"Host": kw["host"]} if kw.get("host") else {},
                "maxEarlyData":        1024,
                "earlyDataHeaderName": "Sec-WebSocket-Protocol",
            }

        elif stream == "xhttp":
            raw  = kw.get("path", "/xhttp")
            path = f"/xhttp/{uuid}" if raw in ("/xhttp", "") and uuid else raw
            ss["xhttpSettings"] = {
                "path": path,
                "host": kw.get("host", ""),
                "mode": kw.get("mode", "auto"),
                "maxUploadSize":        100 * 1024 * 1024,
                "maxConcurrentUploads": 10,
                "scMaxEachPostBytes":   1 * 1024 * 1024,
                "scMinPostsIntervalMs": 30,
                "xPaddingBytes":        "100-1000",
            }

        elif stream == "grpc":
            ss["grpcSettings"] = {
                "serviceName": kw.get("serviceName", "grpc"),
                "multiMode":   bool(kw.get("multiMode", True)),
                "idle_timeout":  60,
                "health_check_timeout": 20,
                "permit_without_stream": True,
            }

        elif stream == "httpupgrade":
            raw  = kw.get("path", "/upgrade")
            path = f"/upgrade/{uuid}" if raw in ("/upgrade", "") and uuid else raw
            ss["httpUpgradeSettings"] = {"path": path, "host": kw.get("host", "")}

        elif stream == "mkcp":
            ss["kcpSettings"] = {
                "mtu":          1350,
                "tti":          20,
                "uplinkCapacity":   100,
                "downlinkCapacity": 100,
                "congestion":   bool(kw.get("congestion", False)),
                "readBufferSize":  4,
                "writeBufferSize": 4,
                "seed":    kw.get("seed", ""),
                "header":  {"type": kw.get("header", "none")},
            }

        if kw.get("reality"):
            ss["security"] = "reality"
            ss["realitySettings"] = {
                "show":        False,
                "dest":        f"{kw.get('reality_sni','') or kw.get('host','')}:443",
                "xver":        0,
                "serverNames": [kw.get("reality_sni", "") or kw.get("host", "")],
                "privateKey":  kw.get("reality_pbk", ""),
                "shortIds":    [kw.get("reality_sid", "")],
                "fingerprint": kw.get("reality_fingerprint", "chrome"),
            }
        elif tls:
            _alpn = ["h3", "h2", "http/1.1"] if stream == "xhttp" else ["h2", "http/1.1"]
            ss["security"] = "tls"
            ss["tlsSettings"] = {
                "serverName":   kw.get("sni", "") or "",
                "minVersion":   "1.2",
                "certificates": [{"certificateFile": XRAY_CERT_FILE, "keyFile": XRAY_KEY_FILE}],
                "alpn": _alpn,
                "enableSessionResumption": True,
            }
        return ss
