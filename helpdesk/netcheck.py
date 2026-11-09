"""Basic network checks a service desk analyst runs first.

Each check returns a result with a plain-language verdict, so the output can be pasted
into a ticket as it is. Standard library only.
"""
from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass


@dataclass
class Result:
    check: str
    ok: bool
    detail: str

    def __str__(self) -> str:
        return f"[{'OK' if self.ok else 'FAIL'}] {self.check}: {self.detail}"


def check_ip_config(address: str, netmask: str, gateway: str) -> Result:
    """Is the gateway inside the machine's own subnet? A common cause of 'Wi-Fi connected, no internet'."""
    try:
        iface = ipaddress.ip_interface(f"{address}/{netmask}")
        gw = ipaddress.ip_address(gateway)
    except ValueError as exc:
        return Result("ip config", False, f"invalid value: {exc}")
    if iface.ip.is_link_local:
        return Result("ip config", False, "169.254.x.x address: the device did not get an address from DHCP")
    if gw not in iface.network:
        return Result("ip config", False, f"gateway {gw} is outside the subnet {iface.network}")
    return Result("ip config", True, f"{iface.ip} in {iface.network}, gateway {gw} reachable on the subnet")


def check_dns(hostname: str) -> Result:
    """Does the name resolve? Separates 'DNS is broken' from 'the network is down'."""
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        return Result("dns", False, f"{hostname} did not resolve ({exc.strerror})")
    addresses = sorted({info[4][0] for info in infos})
    return Result("dns", True, f"{hostname} resolves to {', '.join(addresses)}")


def check_port(host: str, port: int, timeout: float = 3.0) -> Result:
    """Can a TCP connection be opened? Used for VPN gateways, mail servers and web services."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return Result("port", True, f"{host}:{port} accepts connections")
    except socket.timeout:
        return Result("port", False, f"{host}:{port} timed out (firewall or host down)")
    except OSError as exc:
        return Result("port", False, f"{host}:{port} refused or unreachable ({exc.strerror})")
