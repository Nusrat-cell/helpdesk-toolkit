import pytest

from helpdesk.tickets import TicketLog, triage


def test_triage_priorities():
    assert triage("VPN will not connect")[0] == "P2"
    assert triage("Printer on floor 2 not printing")[0] == "P3"
    assert triage("Outage: all users cannot work")[0] == "P1"
    assert triage("Please add a second monitor")[0] == "P4"


def test_p1_is_escalated_and_p3_is_not():
    log = TicketLog()
    a = log.open_ticket("Anna", "phone", "Outage, all users affected")
    b = log.open_ticket("Ben", "chat", "Laptop is slow")
    rows = {r[0]: r for r in log.open_by_priority()}
    assert rows[a][4] == 1 and rows[b][4] == 0


def test_empty_description_rejected():
    with pytest.raises(ValueError):
        TicketLog().open_ticket("Cara", "email", "   ")


def test_cannot_close_without_resolution_and_closed_tickets_leave_the_queue():
    log = TicketLog()
    t = log.open_ticket("Dan", "email", "Cannot log in to mail")
    with pytest.raises(ValueError):
        log.close(t, "")
    log.close(t, "Reset password, user confirmed access")
    assert log.open_by_priority() == []


def test_queue_is_ordered_by_priority():
    log = TicketLog()
    log.open_ticket("A", "chat", "Update my software")
    log.open_ticket("B", "phone", "VPN not working")
    assert [r[1] for r in log.open_by_priority()] == ["P2", "P3"]
