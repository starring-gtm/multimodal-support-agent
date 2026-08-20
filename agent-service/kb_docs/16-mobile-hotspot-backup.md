---
id: mobile-hotspot-backup
category: equipment
team: network-ops
---

# NovaLink Backup Hotspot (Business & Pro Plans)

Business and Pro-tier plans include an optional cellular backup hotspot device that automatically activates during a fiber outage.

## How it works
The backup hotspot continuously monitors the primary fiber connection. If the primary connection drops for more than 60 seconds, the hotspot automatically activates and the router fails over to it. Failover is automatic — no customer action is required.

## Checking backup hotspot status
The hotspot has its own status light, separate from the main router:
- **Solid green:** Standing by, primary connection healthy.
- **Blinking green:** Actively providing backup connectivity (primary is down).
- **Solid amber:** No cellular signal available in this location.
- **Off:** Device not activated on the account, or powered off.

## Data limits
Backup hotspot data is capped at 50GB/month by default on most plans, intended for essential connectivity during outages rather than as a primary connection. Usage beyond this cap may result in reduced backup speeds until the next billing cycle.

## When to escalate
If the hotspot shows solid amber (no signal) at a location that previously had signal, or fails to activate during a confirmed primary outage, escalate to **Network Operations**.
