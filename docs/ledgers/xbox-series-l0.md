# Xbox Series L0 evidence ledger

Source-reviewed only. Sources/claims are pinned to full commits and exact file
hashes. Every kernel/SDL claim is source_only consumer evidence; USB-GIP and
Bluetooth device-side gaps are separate unknown claims. Xbox360 standard HID is
not a Series reference. No upstream excerpts, fixture bytes or device identity
are copied.

| Area | Records | Limits |
| --- | --- | --- |
| xpad identity/Share | xbox-series-xpad-identity-share | Firmware-specific extension, not universal raw packet |
| full xpad evdev shape | xbox-series-xpad-evdev-shape; xbox-series-xpad-evdev-golden | Synthetic capability expectation corroborated by the linked public observation |
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

The follow-up golden fixture describes one stock xpad gamepad with force
feedback enabled. It records the observed post-driver input ID version
as an evdev sample. It contains no captured frames or identifying
device strings. Linux's memoryless force-feedback layer adds gain and
periodic capabilities to xpad's ordinary two-motor rumble. The kernel
converts periodic effects to main-motor magnitudes. Independent impulse
motors, wired GIP and Bluetooth device behavior remain outside this fixture.

For the evdev mapping, the face buttons use the Linux Xbox-layout face
codes. The bumpers use TL and TR, the two stick clicks use THUMBL and
THUMBR, and View, Menu, Guide and Share use SELECT, START, MODE and
RECORD respectively. Stick pairs are X/Y and RX/RY. Triggers are Z/RZ.
Hat 0 uses positive X for right and positive Y for down. The stick Y
values are the post-driver axes, where xpad reverses the incoming
vertical direction. See the pinned xpad source at lines 1051–1059 and
1095–1158 for the mappings. This table describes evdev controls only.

## Bluetooth-bus UHID consumer gap (source-only)

[Bluetooth consumer gap brief](../xbox-series-bluetooth-consumer.md) records 13 `xbox-cgap-*` consumer claims and pins Linux `hid-microsoft` / `hid-generic` and xpadneo sources. It reuses `xbox-series-sdl-xboxone` and existing BlueZ HOGP/UHID sources rather than creating competing versions of PR #116 or PR #123.

- **Kernel binding:** `xbox-cgap-linux-binding`, `xbox-cgap-hogp-uhid`; standard Bluetooth model 1914 matches kernel `hid-microsoft`, but no tested virtual bind.
- **Descriptors/firmware:** `xbox-cgap-descriptor-example`, `xbox-cgap-descriptor-variants`; 283-byte Series example; older 1708 and Elite 1797 references are *comparators*, not alternate Series truth.
- **xpadneo:** `xbox-cgap-xpadneo-binding-identity`, `xbox-cgap-xpadneo-descriptor-remap`, `xbox-cgap-xpadneo-buttons-battery`, `xbox-cgap-xpadneo-impulse-derived`, `xbox-cgap-xpadneo-hogp-output` describe optional driver selection, rewritten identity, conditional mappings, derived trigger rumble and acknowledged BLE output.
- **SDL:** `xbox-cgap-sdl-descriptor-gate`, `xbox-cgap-sdl-firmware-buttons`, `xbox-cgap-sdl-guide-battery-policy` expand the parser-versus-fallback and firmware distinctions without duplicating existing Bluetooth report claims.
- **Decision boundary:** `xbox-cgap-virtual-uhid-feasibility` is `inferred`, not a host acceptance. Original `xbox-series-bluetooth-device-gaps` remains unknown. Physical and virtual tests are **not run**.

### xpadneo-specific follow-up (consumer-only)

The [xpadneo deep dive](../xbox-series-xpadneo-consumer.md) corrects `xbox-cgap-xpadneo-buttons-battery`: the xpadneo `BTN_SHARE` name is a macro for **keyboard KEY_F12**, not an evdev gamepad Share button. The driver also emits separate auxiliary evdev devices, a default Guide modifier, an extra `ABS_PROFILE` axis and a conditional connection-rumble sequence. Its packaged rules restrict hidraw access, affecting SDL HIDAPI acceptance. `xbox-cgap-xpadneo-*` source-only consumer claims record these behaviors with empty experiments. Physical Bluetooth Series behavior remains **unknown**.

## xone GIP consumer (source-only, draft research)

The separate [xone consumer brief](../xbox-series-xone-consumer.md) records
`dlundqvist/xone` at `f2aa9fe01103d7600553b505b298ff0bd47ff280`.
Its `xbox-xone-*` source records hash each referenced upstream file. Its
`xbox-xone-*` claim records are **consumer** evidence only and add no
experiments or physical validation. They do not replace the existing xpad,
SDL, USB-device-gap or Bluetooth-device-gap records.

- **Startup / identity:** `xbox-xone-wired-bind`,
  `xbox-xone-startup-identify`, `xbox-xone-ack-sequence`,
  `xbox-xone-host-rejection` describe USB binding, GIP metadata and host
  parser limits. Physical descriptors, timing and keep-alive remain unknown.
- **Input / evdev:** `xbox-xone-input-share-guide` and
  `xbox-xone-evdev-compare` compare xone's Guide/Share handling and
  post-driver surface against the existing 26-capability xpad baseline.
- **Impulse triggers:** `xbox-xone-rumble-main-only` shows four GIP motor
  fields but only main-motor Linux FF mapping. Pinned SDL has a distinct
  conditional trigger-rumble GIP path, not proof of physical actuation.
- **Other surfaces:** `xbox-xone-led-battery-power` and
  `xbox-xone-gip-headset` describe LED, battery, power and conditional GIP
  headset-to-ALSA playback/capture. xpad's GIP-audio exclusion remains valid.
- **Receiver:** `xbox-xone-receiver-bind` and
  `xbox-xone-receiver-clients` describe the Xbox Wireless Adapter and
  per-associated-client GIP adapters (transport `receiver`, not Bluetooth).
  A separately supplied firmware prerequisite is recorded without analysis.
- **Gaps:** `xbox-xone-physical-unknown` retains physical-device unknowns.
  The proposed tests in the brief are explicitly **not run**.
