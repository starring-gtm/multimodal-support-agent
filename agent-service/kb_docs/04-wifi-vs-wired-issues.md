---
id: wifi-vs-wired-issues
category: connectivity
team: network-ops
---

# Wi-Fi Not Working But Wired Connection Is Fine

If a device connected via Ethernet cable has internet access but Wi-Fi devices do not, the issue is isolated to the router's wireless radio, not your internet connection itself.

## Steps to resolve
1. Confirm the Wi-Fi network name (SSID) is visible when scanning for networks on an affected device.
2. If the network is not visible at all:
   - Restart the router.
   - Check if the router has a physical Wi-Fi on/off switch or button that may have been accidentally toggled.
3. If the network is visible but devices cannot connect or authenticate:
   - Double check the Wi-Fi password is entered correctly (case-sensitive).
   - Try "forgetting" the network on the device and reconnecting fresh.
4. If only some devices are affected (not all), the issue is likely device-specific, not router-specific — check that device's own Wi-Fi settings.

## When to escalate
If the Wi-Fi radio does not broadcast a network at all even after a restart, and wired connections work normally, escalate to **Network Operations** — this typically indicates a hardware fault in the router's wireless module and may require a replacement unit.
