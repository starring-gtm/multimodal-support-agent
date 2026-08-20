---
id: error-codes-light-patterns
category: connectivity
team: network-ops
---

# Router Light Pattern & Error Code Reference

Quick reference for interpreting router status lights and in-app error codes.

## Light patterns
| Light | Pattern | Meaning |
|---|---|---|
| Power | Off | No power reaching the router |
| Power | Solid white | Normal operation |
| Internet/WAN | Off | No connection attempt in progress |
| Internet/WAN | Blinking blue | Attempting to connect |
| Internet/WAN | Solid blue | Connected, normal operation |
| Internet/WAN | Solid red | No signal detected — line issue |
| Internet/WAN | Blinking red | Recently dropped, attempting to reconnect |
| Wi-Fi | Off | Wireless radio disabled |
| Wi-Fi | Solid green | Normal operation |

## In-app error codes
| Code | Meaning | Typical fix |
|---|---|---|
| ERR-101 | Authentication failure with network | Restart router; if persists, escalate to Network Ops |
| ERR-204 | DNS resolution failure | Restart router; try alternate DNS in advanced settings |
| ERR-310 | ONT signal loss | Check fiber cable connection; likely line fault if persists |
| ERR-450 | Account suspended (billing) | Refer to Billing — not a technical issue |
| ERR-512 | Firmware update failed | Retry update; if repeated failure, escalate to Network Ops |

## When to escalate
Any error code beginning with ERR-3xx (line-related) that persists after a router restart should be escalated to **Network Operations** directly, without further troubleshooting steps, since these indicate physical line faults.
