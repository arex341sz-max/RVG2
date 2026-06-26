"""protocols/__init__.py — registry مرکزی پروتکل‌ها"""
from .vless     import VLESSProtocol
from .trojan    import TrojanProtocol
from .vmess     import VMessProtocol
from .hysteria2 import Hysteria2Protocol
from .wireguard import WireGuardProtocol
from .siz10a    import SIZ10AProtocol

REGISTRY: dict[str, type] = {
    "siz10a":    SIZ10AProtocol,   # اول — پروتکل پیش‌فرض
    "vless":     VLESSProtocol,
    "trojan":    TrojanProtocol,
    "vmess":     VMessProtocol,
    "hysteria2": Hysteria2Protocol,
    "wireguard": WireGuardProtocol,
}


def get_protocol(name: str):
    cls = REGISTRY.get(name.lower())
    if not cls:
        raise ValueError(f"پروتکل نامعتبر: {name}")
    return cls()


def list_protocols() -> dict:
    result = {}
    for name, cls in REGISTRY.items():
        p = cls()
        result[name] = {
            "display_name":     p.display_name,
            "icon":             p.icon,
            "color":            p.color,
            "stream_modes":     p.stream_modes,
            "default_stream":   p.default_stream,
            "supports_tls":     p.supports_tls,
            "default_tls":      p.default_tls,
            "supports_reality": p.supports_reality,
        }
    return result
