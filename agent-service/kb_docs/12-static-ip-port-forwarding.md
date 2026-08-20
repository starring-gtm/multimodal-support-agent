---
id: static-ip-port-forwarding
category: advanced-networking
team: network-ops
---

# Static IP and Port Forwarding (Advanced)

## Static IP addresses
Static IPs are only available on Business and Pro-tier plans. Residential plans use dynamic IP addresses that may change periodically.

To request a static IP on an eligible plan: submit a request via the account portal under Advanced > Static IP. Provisioning typically takes 1-2 business days and includes one-time setup documentation sent by email.

## Port forwarding
Port forwarding allows external devices to reach a specific device on the customer's home network (commonly needed for hosting game servers, security cameras, or remote access tools).

### Steps
1. Log in to the router's admin panel (typically at 192.168.1.1).
2. Navigate to Advanced Settings > Port Forwarding.
3. Specify the internal device's local IP address, the port number(s) needed, and the protocol (TCP/UDP).
4. Save and apply — changes typically take effect within 30 seconds without requiring a router restart.

## Common issue: port forwarding not working
This is almost always caused by one of:
- The internal device's local IP changed (assign it a static local IP via DHCP reservation to prevent this).
- A firewall on the device itself is blocking the port.
- The plan is on Carrier-Grade NAT (CGNAT), which is default on some residential plans and blocks inbound port forwarding entirely — this requires a static IP add-on to resolve.

## When to escalate
If a customer on a static IP plan still cannot get port forwarding to work after confirming local IP and firewall settings, escalate to **Network Operations** for a line-level configuration check.
