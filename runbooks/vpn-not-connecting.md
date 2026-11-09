# VPN will not connect

**Priority:** P2 (respond within 4 hours). **Channel:** phone, email or chat.

1. Ask: what is the exact error message, and did it work yesterday?
2. Confirm normal internet works: open a website. If not, go to the "No internet" runbook.
3. Check the VPN gateway is reachable: `python -m helpdesk.cli port vpn.example.com 443`.
4. Check the user's date and time are correct. A wrong clock breaks certificate checks.
5. Ask the user to sign out of the VPN client fully and sign in again.
6. Try another network (phone hotspot). If it works there, the home network or router blocks the VPN.
7. Still failing: **escalate** to the network team with the error text, the steps above and the time of each attempt.

**Close note example:** "Clock was 12 minutes ahead; user corrected time sync, VPN connected, user confirmed."
