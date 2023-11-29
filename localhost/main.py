import io
import logging
import os.path
import socket
import subprocess
import time
from collections.abc import Generator
from typing import Union, Dict, List

import pandas as pd
import requests

from localhost.models import settings, Device

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.INFO)


def get_network_id() -> str:
    """Get network id from the current IP address."""
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        socket_.connect(("8.8.8.8", 80))
        ip_address = socket_.getsockname()[0]
        network_id = '.'.join(ip_address.split('.')[0:3])
        socket_.close()
    except OSError as error:
        LOGGER.warning(error)
        network_id = "192.168.1"
    return network_id


def generate_dataframe() -> pd.DataFrame:
    """Generate a dataframe using the devices information from router web page.

    Returns:
        pd.DataFrame:
        Devices list as a data frame.
    """
    # pd.set_option('display.max_rows', None)
    try:
        response = requests.get(url=f"http://{get_network_id()}.254/cgi-bin/devices.ha")
    except requests.RequestException as error:
        LOGGER.error(error)
        raise ConnectionError(error.args)
    else:
        if response.ok:
            html_source = response.text
            html_tables = pd.read_html(io.StringIO(html_source))
            return html_tables[0]
        else:
            LOGGER.error("[%s] - %s" % (response.status_code, response.text))


def get_attached_devices() -> Generator[Device]:
    """Get all devices connected to the router.

    Yields:
        Generator[Device]:
        Yields each device information as a Device object.
    """
    device_info = {}
    dataframe = generate_dataframe()
    if dataframe is None:
        return
    for value in dataframe.values:
        if str(value[0]) == "nan":
            yield Device(device_info)
            device_info = {}
        elif value[0] == "IPv4 Address / Name":
            key = value[0].split('/')
            val = value[1].split('/')
            device_info[settings.format_key(key[0].strip())] = val[0].strip()
            device_info[settings.format_key(key[1].strip())] = val[1].strip()
        else:
            device_info[settings.format_key(value[0])] = value[1]


def parse_host_file() -> Dict[Union[int, str], Union[List[str], str]]:
    """Parse the host file and convert the host entries into key-value pairs.

    Returns:
        Dict[Union[int, str], List[str]]:
        Returns a dictionary of parsed hosts file information.
    """
    host_entries = {}
    with open(settings.etc_hosts, 'r') as file:
        for idx, line in enumerate(file):
            # Yield comments and empty lines with an integer as key
            if not line.strip():
                host_entries[idx] = None
                continue
            if line.startswith('#'):
                host_entries[idx] = line.rstrip()
                continue
            # Split the line into columns (fields)
            fields = line.split()
            # Extract IP address and hostnames
            ip_address = fields[0]
            hostnames = fields[1:]
            hostnames = ' '.join(hostnames).split(',')  # rejoin as string and split by comma (,)
            hostnames = list(map(str.strip, hostnames))  # strip individual hostnames and make a list
            if host_entries.get(ip_address):
                host_entries[f"{ip_address}_DUPLICATE{idx}"] = hostnames
            else:
                host_entries[ip_address] = hostnames
    return host_entries


def update_host_file(host_entries: Dict) -> None:
    """Update the hosts entry file, with all the devices currently connected to the router.

    Args:
        host_entries: Data that has to be dumped into the hosts file.
    """
    with open(settings.etc_hosts, 'w') as file:
        for key, value in host_entries.items():
            if value is None:
                file.write("\n")
                continue
            if isinstance(key, int):
                file.write(f"{value}\n")
                continue
            key = key.split('_')[0]
            if isinstance(value, list):
                file.write(f"{key}\t{', '.join(value)}\n")
                continue
            file.write(f"{key}\t{value}\n")


def flush_dns_cache() -> None:
    """Flushes the DNS cache."""
    for cmd in settings.flush_dns:
        result = subprocess.run(cmd, shell=True)
        if result.returncode:
            LOGGER.error("Failed to clear DNS cache")
            break
    else:
        LOGGER.info("ALL SET!!")


def dump() -> None:
    """Dumps all devices' hostname and IP addresses into the hosts file."""
    try:
        f = open(settings.etc_hosts, 'w')
        f.close()
    except PermissionError:
        raise PermissionError(
            "script needs to run with sudo or as an administrator"
        )
    host_entries = parse_host_file()
    eos = False
    for device in get_attached_devices():
        eos = True
        if device.ipv4_address:
            host_entries[device.ipv4_address] = f"{device.name}"
        else:
            LOGGER.error(device.__dict__)
    if eos:
        host_entries[int(time.time())] = "\n# End of section"
    update_host_file(host_entries)
    flush_dns_cache()


if __name__ == '__main__':
    dump()
