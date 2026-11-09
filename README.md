# Helpdesk Toolkit

A small first-line IT support toolkit written to practise the work of a service desk analyst: diagnosing
connection problems, logging tickets with priorities, and following written procedures (SOPs).

## What is in it

- `helpdesk/netcheck.py`: three checks I run first when someone says "no internet":
  IP configuration (gateway inside the subnet, 169.254.x.x means DHCP failed), DNS resolution, and TCP port reachability.
- `helpdesk/tickets.py`: a SQLite ticket log. Requests arrive by phone, email or chat, get a priority (P1 to P4) and a
  response target from their wording, P1 is flagged for escalation, and a ticket cannot be closed without a resolution note.
- `runbooks/`: five step-by-step procedures (VPN, no internet, printer, slow laptop, software install) written the way
  a new colleague could follow them, each saying when to escalate and what to include.
- `docs/incident-process-flow.md`: the whole process drawn as a flow diagram.
- `tests/`: 11 automated tests.

## Run it

```
python -m helpdesk.cli dns example.com
python -m helpdesk.cli ip 192.168.1.20 255.255.255.0 192.168.2.1
python -m helpdesk.cli port example.com 443
python -m pytest
```

## Notes and limits

- Standard library only, Python 3.11 or newer.
- The priority rules are keyword based and a starting point: a real desk would tune them to its own services.
- It does not replace a monitoring tool. It records what a person finds and does.
