import platform
import time
from os import environ
from typing import Callable, Tuple


class Error(Exception):
    """Package's base exception."""


class ValidationError(ValueError):
    """Custom validation error."""


class MissingRequirement(ImportError):
    """Custom requirement error."""


class Settings:
    """Wrapper for the settings required by the module.

    >>> Settings

    """

    format_key: Callable = None
    os: str = platform.system()
    # Host file that matches FQDN with server IPs hosting a specific domain
    etc_hosts: str = "/etc/hosts"
    host_id: int = 254
    if os == "Windows":
        etc_hosts: str = r"C:\Windows\System32\drivers\etc\hosts"
        flush_dns: Tuple[str] = ("ipconfig /flushdnscache",)
    elif os == "Darwin":
        flush_dns: Tuple[str] = ("sudo dscacheutil -flushcache", "sudo killall -HUP mDNSResponder",)
    else:
        flush_dns: Tuple = tuple()
    # Unlike Windows and macOS, Ubuntu and Linux Mint do not cache DNS queries at the operating system level by default.
    start = time.time()
    router_pass = environ.get('router_pass') or environ.get('ROUTER_PASS')


settings = Settings()
settings.format_key = lambda key: key.lower().replace(' ', '_').replace('-', '_')
