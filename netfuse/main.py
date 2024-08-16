import subprocess
import sys
import time
from types import ModuleType

import click

from netfuse.config import settings
from netfuse.errors import Error, ValidationError
from netfuse.logger import LOGGER
from netfuse.modules import att, netgear


def center_text(text: str) -> str:
    """Centers the text with 80 as overall padding size.

    Args:
        text: Text to be centered.

    Returns:
        str:
        Text centered using asterisk.
    """
    ast_len = (80 - len(text)) // 2
    return f"{'*' * ast_len}  {text}  {'*' * ast_len}"


HEADER = center_text("Begin NetFuse")
WARNING1 = center_text(
    "Please do not make any manual changes within this section".upper()
)
WARNING2 = center_text("Any modifications made here will be overwritten".upper())
FOOTER = center_text("End NetFuse")


def update_host_file(host_entries: str, output_file: str, dry_run: bool) -> None:
    """Update the hosts entry file, with all the devices currently connected to the router.

    Args:
        host_entries: Data that has to be dumped into the hosts file.
        output_file: Host file that matches FQDN with server IPs hosting a specific domain.
        dry_run: Prints the information instead of writing to hosts file.
    """
    if dry_run:
        print(host_entries)
        return
    try:
        file = open(output_file, "w")
    except PermissionError as error:
        mod = f"netfuse {' '.join(sys.argv[1:])}"
        if settings.os == "Windows":
            cmd = f'runas /user:Administrator "{mod}"'
        else:
            cmd = f"sudo {mod}"
        raise Error(f"\n{error.strerror}\n\tUse {cmd!r}")
    file.write(host_entries)
    file.close()


def flush_dns_cache() -> None:
    """Flushes the DNS cache."""
    for cmd in settings.flush_dns:
        try:
            subprocess.run(cmd, shell=True)
        except subprocess.SubprocessError as warn:
            LOGGER.debug(warn)
    else:
        LOGGER.info(
            "Finished updating hosts file in %.2fs", time.time() - settings.start
        )


def dump(dry_run: bool, filepath: str, output: str, module: ModuleType) -> None:
    """Dumps all devices' hostname and IP addresses into the hosts file."""
    with open(filepath) as file:
        tmp_entries = file.read()
    host_entries = ""
    inside_block = False
    for idx, line in enumerate(tmp_entries.splitlines()):
        if HEADER in line:
            inside_block = True
            continue
        if FOOTER in line:
            inside_block = False
            continue
        if not inside_block:
            host_entries += f"{line}\n"
    host_entries = host_entries.strip()
    host_entries += "\n\n" + HEADER + "\n"
    host_entries += "\n" + "*" * 83 + "\n"
    host_entries += WARNING1 + "\n" + WARNING2
    host_entries += "\n" + "*" * 83 + "\n\n"
    for device in module.attached_devices():
        if device.ipv4_address:
            host_entries += f"{device.ipv4_address}\t{device.name}\n"
        else:
            LOGGER.debug(
                "%s [%s] does not have an IP address", device.name, device.mac_address
            )
    host_entries += "\n" + FOOTER + "\n\n"
    update_host_file(host_entries, output, dry_run)
    if output == settings.etc_hosts:
        flush_dns_cache()


# noinspection PyUnusedLocal
@click.command()
@click.pass_context
@click.option(
    "-m",
    "--model",
    required=False,
    help="Source model that's either 'att' or 'netgear'",
)
@click.option(
    "-h",
    "--host-id",
    required=False,
    default=settings.host_id,
    help="Host ID of the network administrator page",
)
@click.option(
    "-d",
    "--dry",
    required=False,
    is_flag=True,
    help="Dry run without updating the hosts file",
)
@click.option(
    "-p",
    "--path",
    required=False,
    default=settings.etc_hosts,
    help=f"Path for the hosts file, defaults to: {settings.etc_hosts}",
)
@click.option(
    "-o",
    "--output",
    required=False,
    default=settings.etc_hosts,
    help=f"Output filepath to write the updated entries, defaults to: {settings.etc_hosts}",
)
def run(
    *args,
    model: str,
    host_id: int = settings.host_id,
    dry: bool = False,
    path: str = settings.etc_hosts,
    output: str = settings.etc_hosts,
):
    """Entrypoint for commandline.

    Args:
        *args: Placeholder arg for click module.
        model: NetFuse module to choose. Choices are att or netgear.
        host_id: Host ID for At&t home network.
        dry: Boolean flag to enable dry run.
        path: Input filepath for host entry file.
        output: Output filepath for host entry file.
    """
    try:
        assert isinstance(host_id, int) and 1 <= host_id <= 256
        settings.host_id = host_id  # override default if assertion passes
    except AssertionError as error:
        LOGGER.critical(error)
    mapped = {"att": att, "netgear": netgear}
    if model in mapped.keys():
        dump(dry_run=dry, filepath=path, output=output, module=mapped[model])
    else:
        raise ValidationError(
            "\n\n-m/--model\n\tInput should be 'att' or 'netgear' "
            f"[type=string_type, input_value={model}, input_type={type(model)}]"
        )
