import socket
import threading

from helpdesk.netcheck import check_dns, check_ip_config, check_port


def test_gateway_outside_subnet_is_reported():
    r = check_ip_config("192.168.1.20", "255.255.255.0", "192.168.2.1")
    assert not r.ok and "outside the subnet" in r.detail


def test_dhcp_failure_169_254_is_reported():
    r = check_ip_config("169.254.10.5", "255.255.0.0", "169.254.0.1")
    assert not r.ok and "DHCP" in r.detail


def test_valid_config_passes():
    assert check_ip_config("10.0.0.15", "255.255.255.0", "10.0.0.1").ok


def test_invalid_input_does_not_crash():
    assert not check_ip_config("999.1.1.1", "255.255.255.0", "10.0.0.1").ok


def test_dns_resolves_localhost_and_fails_on_invalid_name():
    assert check_dns("localhost").ok
    assert not check_dns("no-such-host.invalid").ok


def test_port_open_and_closed():
    srv = socket.socket(); srv.bind(("127.0.0.1", 0)); srv.listen(1)
    port = srv.getsockname()[1]
    threading.Thread(target=srv.accept, daemon=True).start()
    assert check_port("127.0.0.1", port).ok
    srv.close()
    assert not check_port("127.0.0.1", port, timeout=1).ok
