"""Ticket log with priority rules and escalation, stored in SQLite."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

PRIORITY_RULES = [
    # (keywords in the description, priority, hours to first response)
    (("cannot work", "all users", "outage", "ransomware", "security"), "P1", 1),
    (("vpn", "cannot log in", "email down", "no internet"), "P2", 4),
    (("slow", "printer", "software install", "update"), "P3", 8),
]
DEFAULT_PRIORITY = ("P4", 24)
ESCALATE_PRIORITIES = {"P1"}


def triage(description: str) -> tuple[str, int]:
    """Pick a priority and a response target from the wording of the request."""
    text = description.lower()
    for keywords, priority, hours in PRIORITY_RULES:
        if any(k in text for k in keywords):
            return priority, hours
    return DEFAULT_PRIORITY


class TicketLog:
    def __init__(self, path: str = ":memory:") -> None:
        self.db = sqlite3.connect(path)
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY, created TEXT NOT NULL, requester TEXT NOT NULL,
                channel TEXT NOT NULL CHECK (channel IN ('phone','email','chat')),
                description TEXT NOT NULL, priority TEXT NOT NULL, respond_within_h INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'open', escalated INTEGER NOT NULL DEFAULT 0, notes TEXT NOT NULL DEFAULT ''
            )"""
        )

    def open_ticket(self, requester: str, channel: str, description: str) -> int:
        if not description.strip():
            raise ValueError("description is required")
        priority, hours = triage(description)
        escalated = int(priority in ESCALATE_PRIORITIES)
        cur = self.db.execute(
            "INSERT INTO tickets (created, requester, channel, description, priority, respond_within_h, escalated)"
            " VALUES (?,?,?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(timespec="seconds"), requester, channel,
             description.strip(), priority, hours, escalated),
        )
        self.db.commit()
        return cur.lastrowid

    def add_note(self, ticket_id: int, note: str) -> None:
        self.db.execute("UPDATE tickets SET notes = notes || ? WHERE id = ?", (note.strip() + "\n", ticket_id))
        self.db.commit()

    def close(self, ticket_id: int, resolution: str) -> None:
        if not resolution.strip():
            raise ValueError("a resolution note is required to close a ticket")
        self.add_note(ticket_id, f"Resolution: {resolution}")
        self.db.execute("UPDATE tickets SET status='closed' WHERE id = ?", (ticket_id,))
        self.db.commit()

    def open_by_priority(self) -> list[tuple]:
        return self.db.execute(
            "SELECT id, priority, requester, description, escalated FROM tickets"
            " WHERE status='open' ORDER BY priority, id"
        ).fetchall()
