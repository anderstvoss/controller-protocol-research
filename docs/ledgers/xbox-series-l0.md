# Xbox Series L0 evidence ledger

Source-reviewed only. Sources/claims are pinned to full commits and exact file
hashes. Every kernel/SDL claim is source_only consumer evidence; USB-GIP and
Bluetooth device-side gaps are separate unknown claims. Xbox360 standard HID is
not a Series reference. No upstream excerpts, fixture bytes or device identity
are copied.

| Area | Records | Limits |
| --- | --- | --- |
| xpad identity/Share | xbox-series-xpad-identity-share | Firmware-specific extension, not universal raw packet |
| evdev domains | xbox-series-xpad-axis-domains | 10-bit triggers, signed sticks, hat; post-driver surface |
| ordinary FF | xbox-series-xpad-trigger-rumble-limitation | Trigger motors zeroed by xpad, hardware capability not denied |
| SDL Bluetooth | xbox-series-sdl-bluetooth-rumble; xbox-series-sdl-bluetooth-report-roles | Consumer templates/decoder, not physical packets |
| SDL USB GIP | xbox-series-sdl-gip-rumble | Distinct framing from Bluetooth |
| serial correction | xbox-series-sdl-disabled-serial-request | Disabled source does not establish active requests |
| observed evdev artifact | xbox-series-published-evdev-shape |26 controls/14 frames; not firmware/GIP/Bluetooth truth |
| unknown device behavior | xbox-series-usb-device-gaps; xbox-series-bluetooth-device-gaps | No new physical experiment |

The prep described a fixture accepted by corpus PR6. Inspection shows PR6
accepted the format, with no Xbox fixture record on current main. This ledger
therefore links/hashes the public gamepadcapture artifact without fabricating a
corpus fixture ID or repeating a physical promotion. The consumer-evidence schema marker now tags the eight source-supported
host/software claims as `consumer`. Their source-only transport scopes no
longer elevate the device category, while the two unknown USB/Bluetooth gaps
remain device-side. This supersedes the earlier plan11a shortcut.
