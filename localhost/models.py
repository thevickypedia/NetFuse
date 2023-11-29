import platform
from typing import Optional, Callable, Union, Any, Tuple


class Device:
    """Convert dictionary into a device object.

    >>> Device

    """

    def __init__(self, dictionary: dict):
        """Set dictionary keys as attributes of Device object.

        Args:
            dictionary: Takes the input dictionary as an argument.
        """
        self.mac_address: Optional[str] = None
        self.ipv4_address: Optional[str] = None
        self.name: Optional[str] = None
        self.last_activity: Optional[str] = None
        self.status: Optional[str] = None
        self.allocation: Optional[str] = None
        self.connection_type: Optional[str] = None
        self.connection_speed: Optional[Union[float, Any]] = None
        self.mesh_client: Optional[str] = None
        for key in dictionary:
            setattr(self, key, dictionary[key])


class Settings:
    """Wrapper for the settings required by the module.

    >>> Settings

    """

    format_key: Callable = None
    os: str = platform.system()
    # Host file that matches FQDN with server IPs hosting a specific domain
    etc_hosts: str = "/etc/hosts"
    if os == "Windows":
        etc_hosts: str = r"C:\Windows\System32\drivers\etc\hosts"
        flush_dns: Tuple[str] = ("ipconfig /flushdnscache",)
    elif os == "Darwin":
        flush_dns: Tuple[str] = ("sudo dscacheutil -flushcache", "sudo killall -HUP mDNSResponder",)
    else:
        flush_dns: Tuple = tuple()
    # Unlike Windows and macOS, Ubuntu and Linux Mint do not cache DNS queries at the operating system level by default.


settings = Settings()
settings.format_key = lambda key: key.lower().replace(' ', '_').replace('-', '_')
