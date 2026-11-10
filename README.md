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
- `tests/`: 13 automated tests.

## Run it

```
python -m helpdesk.cli dns example.com
python -m helpdesk.cli ip 192.168.1.20 255.255.255.0 192.168.2.1
python -m helpdesk.cli port example.com 443
python -m pytest
```

## What worked

The checks print a plain sentence that can be pasted straight into a ticket ("gateway 192.168.2.1 is outside the subnet
192.168.1.0/24"), so whoever picks the ticket up next does not have to repeat the work. A ticket also cannot be closed without
a resolution note, which is the habit I would want on a real desk.

The VPN runbook has the step I would not have thought of at first: check the user's clock before anything else. A laptop that
is a few minutes off breaks certificate checks, and the VPN client then reports a login failure that sends everyone to the
password. The example note in the runbook comes from that case (clock 12 minutes ahead).

## What did not work, or only half worked

- **The first version of the priority rules missed how people actually write.** They looked for "cannot log in", so "I can't log
  in" and "cant login" both fell through to P4, the lowest priority, with a 24 hour target. I now fold the apostrophe and
  spelling variants together and the same three sentences come out as P2. It is still a list of phrases, so the next odd
  spelling will get through too.
- **"Everyone" was not treated as an outage.** "Everyone in finance has no internet" was P2. I added "everyone" and "whole team"
  to the P1 words. "Email is down for the whole sales team" still comes out as P2 because the group is named in the middle of the
  sentence, and I left it there rather than keep adding phrases.
- **"Security update needs installing on my laptop" is filed as P1** and flagged for escalation, because it contains "security".
  A real desk would hate that. A proper fix needs more than keywords, and I have not done it.
- **The network checks only see what the machine sees.** A DNS check that passes from my laptop says nothing about the user's
  network, so the runbooks say what to ask the user to run, not just what to run here.

## Notes

- Standard library only, Python 3.11 or newer.
- It does not replace a monitoring tool. It records what a person finds and does.
