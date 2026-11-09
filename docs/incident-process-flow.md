# Incident process flow

How a request moves from the first call to a closed ticket. This is the process the toolkit follows, written as a
flow so that anyone can read it at a glance.

```mermaid
flowchart TD
    A[Request arrives: phone, email or chat] --> B[Log ticket: requester, channel, description]
    B --> C{Triage by wording}
    C -->|outage, security, all users| P1[P1: respond within 1 hour]
    C -->|VPN, login, no internet| P2[P2: respond within 4 hours]
    C -->|slow, printer, install| P3[P3: respond within 8 hours]
    C -->|anything else| P4[P4: respond within 24 hours]
    P1 --> E[Escalate to second line immediately]
    P2 --> D[Follow the runbook]
    P3 --> D
    P4 --> D
    D --> F{Resolved?}
    F -->|no| G[Escalate with findings and steps tried]
    F -->|yes| H[Write resolution note]
    G --> H
    E --> H
    H --> I[Close ticket]
```

## Where this comes from

`helpdesk/tickets.py` implements the triage rules and the rule that a ticket cannot be closed without a resolution
note. The same stages (log, prioritise, work, escalate, resolve, close) are the core of IT service management tools
such as ServiceNow, which I would like to learn through real projects.
