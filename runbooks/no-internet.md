# Wi-Fi connected but no internet

**Priority:** P2.

1. Is the Wi-Fi name correct, and do other devices on it work? If none do, report a possible outage.
2. Read the device's IP address, subnet mask and gateway. Run
   `python -m helpdesk.cli ip <address> <netmask> <gateway>`.
   A 169.254.x.x address means DHCP gave no address: renew the lease or reconnect.
3. Test DNS separately: `python -m helpdesk.cli dns example.com`. If an IP works but names do not, the problem is DNS.
4. Restart the Wi-Fi adapter, then the device. Only then involve the router or the network team.
5. Escalate with the findings from steps 2 and 3.
