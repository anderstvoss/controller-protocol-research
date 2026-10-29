# Xbox 360 — source citation map and capture handoff (K)

**Research parity, part 2: consumers and decisions** · source-only analysis of virtualgamepad `8f60dcce577ab02bd8ed8b3426349729d417393c`. **No host run, report capture or hardware operations performed.** This is not a statement that acceptance-manifest WIP cells pass. Each offset below is **0-based within the unnumbered report payload**, excluding the report-ID prefix when one exists; the device-side report-ID name is included in the field. Fields lacking a specific independent record are marked **uncited**, even when Rust code explicitly assigns them. Source-supported consumer parsing is not proof of retail fidelity. `source_only` records differ from `virtual_host_run` B records and from physical validation.

## Complete emitted/answered field groups by realization

| Target / payload byte or field | Encoded behavior | virtualgamepad code line(s) | Existing evidence record or **uncited** |
| --- | --- | --- | --- |
| linux.uhid.usb: **UHID unnumbered common input** | generic Game Pad 11 buttons/hat/six axes, not wired 00 14 XUSB | `crates/gr-curated-controllers/src/xbox360.rs` 1015–1030; gr-controller-wire/src/lib.rs | `x360-l0-consumer-sdl360-vs-generic-hid` |
| linux.uhid.usb: **HID button usages** | 1,2,4,5,7,8,11,12,13,14,15 then constant padding | `crates/gr-curated-controllers/src/xbox360.rs` gr-controller-wire/src/lib.rs 11–20 | `x360-l0-consumer-exp0016-hid-usage-correction` |
| linux.uhid.usb: **HID 8-bit axes** | 16-bit sticks transformed to six 8-bit HID axes | `crates/gr-curated-controllers/src/xbox360.rs` 1015–1028 | `x360-l0-consumer-hidinput-button-usage-list` |
| linux.uhid.usb: **HID identity** | synthetic VID/PID with standard HID descriptor; no XUSB interface | `crates/gr-curated-controllers/src/xbox360.rs` realization definition, gr-controller-wire | `x360-l0-consumer-xpad-id-usb-binding` |
| linux.uinput: **uinput EV_KEY face/aux** | BTN_A/B/X/Y legacy codes and guide | `crates/gr-curated-controllers/src/xbox360.rs` 641–657 | `x360-l0-consumer-xpad-face-legacy-codes` |
| linux.uinput: **uinput EV_ABS** | stick, triggers, hat and ranges | `crates/gr-curated-controllers/src/xbox360.rs` 659–707 | `x360-l0-consumer-xpad-sticks-trigger-ranges` |
| linux.uinput: **uinput FF/LED** | FF event path only, no independent xpad LED class | `crates/gr-curated-controllers/src/xbox360.rs` realization and FF capabilities | `x360-l0-consumer-uhid-ff-led-unknown` |
| not emitted: **XUSB 00 14/00 08 native wire** | not emitted by current generic UHID codec | `crates/gr-curated-controllers/src/xbox360.rs` No evidence in code | **uncited** |
| not emitted: **receiver 045e:0719 slots** | not realized by ordinary UHID | `crates/gr-curated-controllers/src/xbox360.rs` No evidence in code | **uncited** |
| linux.usbip.usb-audio: **USB/IP audio** | no reported composite audio parity | `crates/gr-curated-controllers/src/xbox360.rs` audio realization | **uncited** |

**Descriptor and output boundaries:** These are fields grouped by contiguous report ranges or identical semantics; preserved reserved-byte holes remain uncited. `linux.uinput` supplies evdev capabilities/events, not HID GET_REPORT, SPI or XUSB. `linux.dummy_hcd.usb-hid` is **not-supported** in the pinned manifest because f_hid cannot satisfy required GET_REPORT metadata/negative replies. `linux.usbip.usb-audio` (where declared) is a different composite topology, not available simply by changing UHID bus identity; its full audio fields are uncited absent a pinned independently verified host run. Reverse output decoding is a consumer contract, not an observed physical output.

## Proposed evidence IDs for existing acceptance-manifest cells

Source: `acceptance/virtualgamepad.xbox360.toml` (pinned revision above, original per-cell `test_id`). **Suggestions are not manifest edits or promotions**. A document/claim can support source evidence; a virtual-host claim only supports its exact historical consumer and backend. All current status and `research_revision` values are retained. Any report field with thin secondary only, especially DS4 Bluetooth and Xbox 360 wired XUSB, remains **unknown** for physical fidelity.

| Function / test ID | Realization | Current cell | Suggested existing claim IDs (no acceptance promotion) |
| --- | --- | --- | --- |
| `buttons` / `acceptance/xbox360/buttons` | `linux.uinput` | **wip** | `x360-vg-exp0016-uhid-individual-correction` |
| `buttons` / `acceptance/xbox360/buttons` | `linux.uhid.usb` | **wip** | `x360-vg-exp0016-uhid-individual-correction` |
| `buttons` / `acceptance/xbox360/buttons` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `buttons` / `acceptance/xbox360/buttons` | `linux.usbip.usb-audio` | **wip** | `x360-vg-exp0016-uhid-individual-correction` |
| `sticks` / `acceptance/xbox360/sticks` | `linux.uinput` | **wip** | `x360-vg-exp0011-evdev-mapping` |
| `sticks` / `acceptance/xbox360/sticks` | `linux.uhid.usb` | **wip** | `x360-vg-exp0011-evdev-mapping` |
| `sticks` / `acceptance/xbox360/sticks` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `sticks` / `acceptance/xbox360/sticks` | `linux.usbip.usb-audio` | **wip** | `x360-vg-exp0011-evdev-mapping` |
| `triggers` / `acceptance/xbox360/triggers` | `linux.uinput` | **wip** | `x360-vg-exp0017-individual-uhid` |
| `triggers` / `acceptance/xbox360/triggers` | `linux.uhid.usb` | **wip** | `x360-vg-exp0017-individual-uhid` |
| `triggers` / `acceptance/xbox360/triggers` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `triggers` / `acceptance/xbox360/triggers` | `linux.usbip.usb-audio` | **wip** | `x360-vg-exp0017-individual-uhid` |
| `identity` / `acceptance/xbox360/identity` | `linux.uinput` | **wip** | `x360-l0-consumer-xpad-id-usb-binding` |
| `identity` / `acceptance/xbox360/identity` | `linux.uhid.usb` | **wip** | `x360-l0-consumer-xpad-id-usb-binding` |
| `identity` / `acceptance/xbox360/identity` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `identity` / `acceptance/xbox360/identity` | `linux.usbip.usb-audio` | **wip** | `x360-l0-consumer-xpad-id-usb-binding` |
| `lifecycle` / `acceptance/xbox360/lifecycle` | `linux.uinput` | **wip** | `x360-vg-exp0009-standard-hid-controls` |
| `lifecycle` / `acceptance/xbox360/lifecycle` | `linux.uhid.usb` | **wip** | `x360-vg-exp0009-standard-hid-controls` |
| `lifecycle` / `acceptance/xbox360/lifecycle` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `lifecycle` / `acceptance/xbox360/lifecycle` | `linux.usbip.usb-audio` | **wip** | `x360-vg-exp0009-standard-hid-controls` |
| `rumble` / `acceptance/xbox360/rumble` | `linux.uinput` | **wip** | `x360-vg-exp0010-evdev-ff` |
| `rumble` / `acceptance/xbox360/rumble` | `linux.uhid.usb` | **wip** | `x360-vg-exp0010-evdev-ff` |
| `rumble` / `acceptance/xbox360/rumble` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `rumble` / `acceptance/xbox360/rumble` | `linux.usbip.usb-audio` | **wip** | `x360-vg-exp0010-evdev-ff` |
| `battery` / `acceptance/xbox360/battery` | `linux.uinput` | **wip** | **uncited** / No evidence; native XUSB not established |
| `battery` / `acceptance/xbox360/battery` | `linux.uhid.usb` | **wip** | **uncited** / No evidence; native XUSB not established |
| `battery` / `acceptance/xbox360/battery` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal; native XUSB not established |
| `battery` / `acceptance/xbox360/battery` | `linux.usbip.usb-audio` | **wip** | **uncited** / No evidence; native XUSB not established |
| `headset-audio` / `acceptance/xbox360/headset-audio` | `linux.uinput` | **wip** | **uncited** / No evidence; native XUSB not established |
| `headset-audio` / `acceptance/xbox360/headset-audio` | `linux.uhid.usb` | **wip** | **uncited** / No evidence; native XUSB not established |
| `headset-audio` / `acceptance/xbox360/headset-audio` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal; native XUSB not established |
| `headset-audio` / `acceptance/xbox360/headset-audio` | `linux.usbip.usb-audio` | **wip** | **uncited** / No evidence; native XUSB not established |

## Minimal owner-authorized capture plan (all proposed, not run)

**No physical Xbox 360 on hand.** If acquired, start with sanitized wired 045e:028e USB interface and passive 00 14 20-byte input; measure legacy BTN_X/BTN_Y, evdev vs SDL path, not generic HID assumptions. Only with approval test bounded wired 00 08 rumble and 01 03 LED. Separate 045e:0719 receiver if hardware acquired; no virtual UHID XUSB-fidelity claim.

**No evidence:** any uncited field above, actual hardware response to unissued output reports, exact consumer backend on Anders's host, per-instance private identity values, physical timing/force/IMU parity. **Cloud agent (realized-controller research parity)**
