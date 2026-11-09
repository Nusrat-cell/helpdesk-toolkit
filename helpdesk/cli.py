"""Command line entry point: python -m helpdesk.cli dns example.com"""
from __future__ import annotations

import argparse

from .netcheck import check_dns, check_ip_config, check_port


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="helpdesk", description="First-line network checks")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dns"); d.add_argument("host")
    t = sub.add_parser("port"); t.add_argument("host"); t.add_argument("port", type=int)
    i = sub.add_parser("ip"); i.add_argument("address"); i.add_argument("netmask"); i.add_argument("gateway")
    a = p.parse_args(argv)
    result = {"dns": lambda: check_dns(a.host), "port": lambda: check_port(a.host, a.port),
              "ip": lambda: check_ip_config(a.address, a.netmask, a.gateway)}[a.cmd]()
    print(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
