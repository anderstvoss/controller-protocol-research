# DualShock 4 — source citation map and capture handoff (K)

**Research parity, part 2: consumers and decisions** · source-only analysis of virtualgamepad `8f60dcce577ab02bd8ed8b3426349729d417393c`. **No host run, report capture or hardware operations performed.** This is not a statement that acceptance-manifest WIP cells pass. Each offset below is **0-based within the unnumbered report payload**, excluding the report-ID prefix when one exists; the device-side report-ID name is included in the field. Fields lacking a specific independent record are marked **uncited**, even when Rust code explicitly assigns them. Source-supported consumer parsing is not proof of retail fidelity. `source_only` records differ from `virtual_host_run` B records and from physical validation.

## Complete emitted/answered field groups by realization

| Target / payload byte or field | Encoded behavior | virtualgamepad code line(s) | Existing evidence record or **uncited** |
| --- | --- | --- | --- |
| linux.uhid.usb: **0x01:0–3** | sticks/axes | `crates/gr-curated-controllers/src/dualshock4.rs` 889–894 | `ds4-l0-device-usb01-input` |
| linux.uhid.usb: **0x01:4–8** | hat, face, shoulders, digital/analog L2/R2 and system | `crates/gr-curated-controllers/src/dualshock4.rs` 895–909 | `ds4-l0-device-usb01-input` |
| linux.uhid.usb: **0x01:9–10, 12–23** | timestamp, gyro/accel | `crates/gr-curated-controllers/src/dualshock4.rs` 910–923 | `ds4-l0-device-imu-and-touch-units` |
| linux.uhid.usb: **0x01:29** | battery/status constant 0x1b | `crates/gr-curated-controllers/src/dualshock4.rs` 928 | **uncited** |
| linux.uhid.usb: **0x01:32–41** | touch update count=1, sequence, two contacts including release | `crates/gr-curated-controllers/src/dualshock4.rs` 924–948 | `ds4-l0-consumer-kernel-touch-report-buffer-count` |
| linux.uhid.usb: **0x01 other** | reserved/zero, not individually measured | `crates/gr-curated-controllers/src/dualshock4.rs` 888–933 | **uncited** |
| linux.uhid.usb: **output 0x05** | rumble/lightbar output and feedback decoder | `crates/gr-curated-controllers/src/dualshock4.rs` 1203–1210 | `audio-dualshock4-hid-output` |
| linux.uhid.usb: **feature 0x02** | 37B synthetic calibration | `crates/gr-curated-controllers/src/dualshock4.rs` gr-controller-wire/src/lib.rs 34–57 | `ds4-l0-device-feature02-calibration-unknown` |
| linux.uhid.usb: **feature 0x12** | 16B pairing and identity | `crates/gr-curated-controllers/src/dualshock4.rs` gr-controller-wire/src/lib.rs 34–57 | `ds4-l0-consumer-kernel-pairing12` |
| linux.uhid.usb: **feature 0xA3** | 49B firmware stub (byte 1=1) | `crates/gr-curated-controllers/src/dualshock4.rs` gr-controller-wire/src/lib.rs 54–57 | `ds4-l0-consumer-hidsony-a3-probe-gate` |
| linux.uhid.usb: **UHID descriptor and identity** | 054c:05c4 v0120 and numbered reports | `crates/gr-curated-controllers/src/dualshock4.rs` 976–1004 | `ds4-l0-device-revision-identity-unknown` |
| linux.uinput: **uinput keys, axes, FF** | evdev and rumble, not raw GET/BT | `crates/gr-curated-controllers/src/dualshock4.rs` 808–843, 995–1024 | `ds4-vg-exp0010-evdev-ff` |
| linux.uhid.usb: **Bluetooth 0x01/0x11 and CRC** | thin noisyloop source only; not realized by USB UHID | `crates/gr-curated-controllers/src/dualshock4.rs` no matching code/physical capture | **uncited** |
| linux.usbip.usb-audio: **USB/IP audio path** | audio actual composite and streaming acceptance | `crates/gr-curated-controllers/src/dualshock4.rs` audio realization | **uncited** |

**Descriptor and output boundaries:** These are fields grouped by contiguous report ranges or identical semantics; preserved reserved-byte holes remain uncited. `linux.uinput` supplies evdev capabilities/events, not HID GET_REPORT, SPI or XUSB. `linux.dummy_hcd.usb-hid` is **not-supported** in the pinned manifest because f_hid cannot satisfy required GET_REPORT metadata/negative replies. `linux.usbip.usb-audio` (where declared) is a different composite topology, not available simply by changing UHID bus identity; its full audio fields are uncited absent a pinned independently verified host run. Reverse output decoding is a consumer contract, not an observed physical output.

## Proposed evidence IDs for existing acceptance-manifest cells

Source: `acceptance/virtualgamepad.dualshock4.toml` (pinned revision above, original per-cell `test_id`). **Suggestions are not manifest edits or promotions**. A document/claim can support source evidence; a virtual-host claim only supports its exact historical consumer and backend. All current status and `research_revision` values are retained. Any report field with thin secondary only, especially DS4 Bluetooth and Xbox 360 wired XUSB, remains **unknown** for physical fidelity.

| Function / test ID | Realization | Current cell | Suggested existing claim IDs (no acceptance promotion) |
| --- | --- | --- | --- |
| `buttons` / `acceptance/dualshock4/buttons` | `linux.uinput` | **wip** | `ds4-vg-exp0009-sdl-standard-touch` |
| `buttons` / `acceptance/dualshock4/buttons` | `linux.uhid.usb` | **wip** | `ds4-vg-exp0009-sdl-standard-touch` |
| `buttons` / `acceptance/dualshock4/buttons` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `buttons` / `acceptance/dualshock4/buttons` | `linux.usbip.usb-audio` | **wip** | `ds4-vg-exp0009-sdl-standard-touch` |
| `sticks` / `acceptance/dualshock4/sticks` | `linux.uinput` | **wip** | `ds4-vg-exp0017-individual-uhid` |
| `sticks` / `acceptance/dualshock4/sticks` | `linux.uhid.usb` | **wip** | `ds4-vg-exp0017-individual-uhid` |
| `sticks` / `acceptance/dualshock4/sticks` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `sticks` / `acceptance/dualshock4/sticks` | `linux.usbip.usb-audio` | **wip** | `ds4-vg-exp0017-individual-uhid` |
| `triggers` / `acceptance/dualshock4/triggers` | `linux.uinput` | **wip** | `ds4-vg-exp0017-individual-uhid` |
| `triggers` / `acceptance/dualshock4/triggers` | `linux.uhid.usb` | **wip** | `ds4-vg-exp0017-individual-uhid` |
| `triggers` / `acceptance/dualshock4/triggers` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `triggers` / `acceptance/dualshock4/triggers` | `linux.usbip.usb-audio` | **wip** | `ds4-vg-exp0017-individual-uhid` |
| `identity` / `acceptance/dualshock4/identity` | `linux.uinput` | **wip** | `ds4-l0-device-revision-identity-unknown` |
| `identity` / `acceptance/dualshock4/identity` | `linux.uhid.usb` | **wip** | `ds4-l0-device-revision-identity-unknown` |
| `identity` / `acceptance/dualshock4/identity` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `identity` / `acceptance/dualshock4/identity` | `linux.usbip.usb-audio` | **wip** | `ds4-l0-device-revision-identity-unknown` |
| `lifecycle` / `acceptance/dualshock4/lifecycle` | `linux.uinput` | **wip** | `ds4-vg-exp0011-combined-node-discovery` |
| `lifecycle` / `acceptance/dualshock4/lifecycle` | `linux.uhid.usb` | **wip** | `ds4-vg-exp0011-combined-node-discovery` |
| `lifecycle` / `acceptance/dualshock4/lifecycle` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `lifecycle` / `acceptance/dualshock4/lifecycle` | `linux.usbip.usb-audio` | **wip** | `ds4-vg-exp0011-combined-node-discovery` |
| `touchpad` / `acceptance/dualshock4/touchpad` | `linux.uinput` | **wip** | `ds4-l0-consumer-kernel-touch-report-buffer-count` |
| `touchpad` / `acceptance/dualshock4/touchpad` | `linux.uhid.usb` | **wip** | `ds4-l0-consumer-kernel-touch-report-buffer-count` |
| `touchpad` / `acceptance/dualshock4/touchpad` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `touchpad` / `acceptance/dualshock4/touchpad` | `linux.usbip.usb-audio` | **wip** | `ds4-l0-consumer-kernel-touch-report-buffer-count` |
| `motion` / `acceptance/dualshock4/motion` | `linux.uinput` | **wip** | `ds4-l0-device-imu-and-touch-units` |
| `motion` / `acceptance/dualshock4/motion` | `linux.uhid.usb` | **wip** | `ds4-l0-device-imu-and-touch-units` |
| `motion` / `acceptance/dualshock4/motion` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `motion` / `acceptance/dualshock4/motion` | `linux.usbip.usb-audio` | **wip** | `ds4-l0-device-imu-and-touch-units` |
| `battery` / `acceptance/dualshock4/battery` | `linux.uinput` | **wip** | `ds4-l0-device-usb01-input` |
| `battery` / `acceptance/dualshock4/battery` | `linux.uhid.usb` | **wip** | `ds4-l0-device-usb01-input` |
| `battery` / `acceptance/dualshock4/battery` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `battery` / `acceptance/dualshock4/battery` | `linux.usbip.usb-audio` | **wip** | `ds4-l0-device-usb01-input` |
| `rumble` / `acceptance/dualshock4/rumble` | `linux.uinput` | **wip** | `ds4-l0-consumer-rumble-lightbar-output` |
| `rumble` / `acceptance/dualshock4/rumble` | `linux.uhid.usb` | **wip** | `ds4-l0-consumer-rumble-lightbar-output` |
| `rumble` / `acceptance/dualshock4/rumble` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `rumble` / `acceptance/dualshock4/rumble` | `linux.usbip.usb-audio` | **wip** | `ds4-l0-consumer-rumble-lightbar-output` |
| `lightbar` / `acceptance/dualshock4/lightbar` | `linux.uinput` | **wip** | `ds4-l0-consumer-rumble-lightbar-output` |
| `lightbar` / `acceptance/dualshock4/lightbar` | `linux.uhid.usb` | **wip** | `ds4-l0-consumer-rumble-lightbar-output` |
| `lightbar` / `acceptance/dualshock4/lightbar` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `lightbar` / `acceptance/dualshock4/lightbar` | `linux.usbip.usb-audio` | **wip** | `ds4-l0-consumer-rumble-lightbar-output` |
| `headset-audio` / `acceptance/dualshock4/headset-audio` | `linux.uinput` | **wip** | `audio-dualshock4-hid-output`; **unknown physical fidelity** |
| `headset-audio` / `acceptance/dualshock4/headset-audio` | `linux.uhid.usb` | **wip** | `audio-dualshock4-hid-output`; **unknown physical fidelity** |
| `headset-audio` / `acceptance/dualshock4/headset-audio` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal; **unknown physical fidelity** |
| `headset-audio` / `acceptance/dualshock4/headset-audio` | `linux.usbip.usb-audio` | **wip** | `audio-dualshock4-hid-output`; **unknown physical fidelity** |
| `speaker-audio` / `acceptance/dualshock4/speaker-audio` | `linux.uinput` | **wip** | `audio-dualshock4-hid-output`; **unknown physical fidelity** |
| `speaker-audio` / `acceptance/dualshock4/speaker-audio` | `linux.uhid.usb` | **wip** | `audio-dualshock4-hid-output`; **unknown physical fidelity** |
| `speaker-audio` / `acceptance/dualshock4/speaker-audio` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal; **unknown physical fidelity** |
| `speaker-audio` / `acceptance/dualshock4/speaker-audio` | `linux.usbip.usb-audio` | **wip** | `audio-dualshock4-hid-output`; **unknown physical fidelity** |
| `calibration` / `acceptance/dualshock4/calibration` | `linux.uinput` | **wip** | `ds4-l0-device-feature02-calibration-unknown`; **unknown physical fidelity** |
| `calibration` / `acceptance/dualshock4/calibration` | `linux.uhid.usb` | **wip** | `ds4-l0-device-feature02-calibration-unknown`; **unknown physical fidelity** |
| `calibration` / `acceptance/dualshock4/calibration` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal; **unknown physical fidelity** |
| `calibration` / `acceptance/dualshock4/calibration` | `linux.usbip.usb-audio` | **wip** | `ds4-l0-device-feature02-calibration-unknown`; **unknown physical fidelity** |

## Minimal owner-authorized capture plan (all proposed, not run)

**1. First read-only source import:** PS4 Developer Wiki [DS4-USB](https://www.psdevwiki.com/ps4/DS4-USB) and [DS4-BT](https://www.psdevwiki.com/ps4/DS4-BT) are **source pending: fetch blocked**. Owner/local agent should retrieve exact revision/date, SHA-256 and section locators before device-fidelity claims. **2. No physical DS4 on hand:** if acquired, sanitized USB descriptor and read-only feature 0x02,0x12,0xA3 and historically 0x81; 05c4/09cc separate. 3. Only with owner approval later, input touch history and bounded output; do not conflate BT 0x11 with USB 0x01.

**No evidence:** any uncited field above, actual hardware response to unissued output reports, exact consumer backend on Anders's host, per-instance private identity values, physical timing/force/IMU parity. **Cloud agent (realized-controller research parity)**
