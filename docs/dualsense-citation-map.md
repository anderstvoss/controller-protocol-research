# DualSense — source citation map and capture handoff (K)

**Research parity, part 2: consumers and decisions** · source-only analysis of virtualgamepad `8f60dcce577ab02bd8ed8b3426349729d417393c`. **No host run, report capture or hardware operations performed.** This is not a statement that acceptance-manifest WIP cells pass. Each offset below is **0-based within the unnumbered report payload**, excluding the report-ID prefix when one exists; the device-side report-ID name is included in the field. Fields lacking a specific independent record are marked **uncited**, even when Rust code explicitly assigns them. Source-supported consumer parsing is not proof of retail fidelity. `source_only` records differ from `virtual_host_run` B records and from physical validation.

## Complete emitted/answered field groups by realization

| Target / payload byte or field | Encoded behavior | virtualgamepad code line(s) | Existing evidence record or **uncited** |
| --- | --- | --- | --- |
| linux.uhid.usb: **0x01:0–5** | sticks and analog triggers | `crates/gr-curated-controllers/src/dualsense.rs` 929–946 | `ds-l0-device-usb01-full-fields` |
| linux.uhid.usb: **0x01:6–9** | sequence, hat/face, shoulder, digital triggers/system | `crates/gr-curated-controllers/src/dualsense.rs` 947–963 | `ds-l0-consumer-l2r2-digital-analog-policy` |
| linux.uhid.usb: **0x01:15–26** | gyro X/Z/-Y and accelerometer, LE16 | `crates/gr-curated-controllers/src/dualsense.rs` 964–981 | `ds-l0-device-imu-scaling-formulas` |
| linux.uhid.usb: **0x01:27–30** | LE32 timestamp | `crates/gr-curated-controllers/src/dualsense.rs` 982 | `ds-l0-device-usb01-full-fields` |
| linux.uhid.usb: **0x01:32–39** | 2 contacts, ID/active, packed 12-bit XY | `crates/gr-curated-controllers/src/dualsense.rs` 983, 1017–1032 | `ds-l0-device-touchpad-format-dimensions` |
| linux.uhid.usb: **0x01:52** | battery/charge and external power default | `crates/gr-curated-controllers/src/dualsense.rs` 984–1004 | `ds-l0-device-usb01-full-fields` |
| linux.uhid.usb: **0x01 other bytes** | reserved/zero and device-side unmeasured status fields | `crates/gr-curated-controllers/src/dualsense.rs` 928–990 | **uncited** |
| linux.uhid.usb: **output 0x02** | valid flags, rumble, trigger effect, mic LED, lightbar/player/audio routing | `crates/gr-curated-controllers/src/dualsense.rs` 1105–1190 | `ds-l0-device-usb02-valid-flags` |
| linux.uhid.usb: **feature 0x05** | 41B synthetic gyro/accel calibration | `crates/gr-curated-controllers/src/dualsense.rs` gr-controller-wire/src/dualsense.rs 31–49 | `ds-l0-device-feature05-shape` |
| linux.uhid.usb: **feature 0x09** | 20B pairing/MAC identity | `crates/gr-curated-controllers/src/dualsense.rs` gr-controller-wire/src/dualsense.rs 27–60 | `ds-l0-device-feature09-identity-shape` |
| linux.uhid.usb: **feature 0x20** | 64B firmware, bytes 44–45 synthetic 0x0224 | `crates/gr-curated-controllers/src/dualsense.rs` gr-controller-wire/src/dualsense.rs 51–60 | `ds-l0-consumer-firmware0224-branch` |
| linux.uhid.usb: **feature 0x03** | reported capability shape exact Sony requirement | `crates/gr-curated-controllers/src/dualsense.rs` gr-controller-wire/src/dualsense.rs 1–20 | `ds-l0-consumer-feature03-capabilities` |
| linux.uhid.usb: **UHID descriptor and identity** | 054c:0ce6 numbered reports, BUS_USB | `crates/gr-curated-controllers/src/dualsense.rs` 1380–1450; gr-controller-wire/src/dualsense.rs | `ds-l0-device-usb01-full-fields` |
| linux.uinput: **uinput keys/axes/touch/FF** | Linux event codes and touch approximations, not raw features | `crates/gr-curated-controllers/src/dualsense.rs` 845–912 | `ds-vg-exp0011-evdev-mapping` |
| linux.usbip.usb-audio: **USB/IP audio path** | audio composite descriptor, altsets, mixer/speaker/mic fidelity | `crates/gr-curated-controllers/src/dualsense.rs` audio realization | **uncited** |

**Descriptor and output boundaries:** These are fields grouped by contiguous report ranges or identical semantics; preserved reserved-byte holes remain uncited. `linux.uinput` supplies evdev capabilities/events, not HID GET_REPORT, SPI or XUSB. `linux.dummy_hcd.usb-hid` is **not-supported** in the pinned manifest because f_hid cannot satisfy required GET_REPORT metadata/negative replies. `linux.usbip.usb-audio` (where declared) is a different composite topology, not available simply by changing UHID bus identity; its full audio fields are uncited absent a pinned independently verified host run. Reverse output decoding is a consumer contract, not an observed physical output.

## Proposed evidence IDs for existing acceptance-manifest cells

Source: `acceptance/virtualgamepad.dualsense.toml` (pinned revision above, original per-cell `test_id`). **Suggestions are not manifest edits or promotions**. A document/claim can support source evidence; a virtual-host claim only supports its exact historical consumer and backend. All current status and `research_revision` values are retained. Any report field with thin secondary only, especially DS4 Bluetooth and Xbox 360 wired XUSB, remains **unknown** for physical fidelity.

| Function / test ID | Realization | Current cell | Suggested existing claim IDs (no acceptance promotion) |
| --- | --- | --- | --- |
| `buttons` / `acceptance/dualsense/buttons` | `linux.uinput` | **wip** | `ds-vg-exp0017-individual-uhid` |
| `buttons` / `acceptance/dualsense/buttons` | `linux.uhid.usb` | **wip** | `ds-vg-exp0017-individual-uhid` |
| `buttons` / `acceptance/dualsense/buttons` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `buttons` / `acceptance/dualsense/buttons` | `linux.usbip.usb-audio` | **wip** | `ds-vg-exp0017-individual-uhid` |
| `sticks` / `acceptance/dualsense/sticks` | `linux.uinput` | **wip** | `ds-vg-exp0008-sdl-standard-motion` |
| `sticks` / `acceptance/dualsense/sticks` | `linux.uhid.usb` | **wip** | `ds-vg-exp0008-sdl-standard-motion` |
| `sticks` / `acceptance/dualsense/sticks` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `sticks` / `acceptance/dualsense/sticks` | `linux.usbip.usb-audio` | **wip** | `ds-vg-exp0008-sdl-standard-motion` |
| `triggers` / `acceptance/dualsense/triggers` | `linux.uinput` | **wip** | `ds-l0-consumer-l2r2-digital-analog-policy` |
| `triggers` / `acceptance/dualsense/triggers` | `linux.uhid.usb` | **wip** | `ds-l0-consumer-l2r2-digital-analog-policy` |
| `triggers` / `acceptance/dualsense/triggers` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `triggers` / `acceptance/dualsense/triggers` | `linux.usbip.usb-audio` | **wip** | `ds-l0-consumer-l2r2-digital-analog-policy` |
| `identity` / `acceptance/dualsense/identity` | `linux.uinput` | **wip** | `ds-l0-device-feature09-identity-shape` |
| `identity` / `acceptance/dualsense/identity` | `linux.uhid.usb` | **wip** | `ds-l0-device-feature09-identity-shape` |
| `identity` / `acceptance/dualsense/identity` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `identity` / `acceptance/dualsense/identity` | `linux.usbip.usb-audio` | **wip** | `ds-l0-device-feature09-identity-shape` |
| `lifecycle` / `acceptance/dualsense/lifecycle` | `linux.uinput` | **wip** | `ds-vg-exp0006-uhid-startup` |
| `lifecycle` / `acceptance/dualsense/lifecycle` | `linux.uhid.usb` | **wip** | `ds-vg-exp0006-uhid-startup` |
| `lifecycle` / `acceptance/dualsense/lifecycle` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `lifecycle` / `acceptance/dualsense/lifecycle` | `linux.usbip.usb-audio` | **wip** | `ds-vg-exp0006-uhid-startup` |
| `touchpad` / `acceptance/dualsense/touchpad` | `linux.uinput` | **wip** | `ds-l0-device-touchpad-format-dimensions` |
| `touchpad` / `acceptance/dualsense/touchpad` | `linux.uhid.usb` | **wip** | `ds-l0-device-touchpad-format-dimensions` |
| `touchpad` / `acceptance/dualsense/touchpad` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `touchpad` / `acceptance/dualsense/touchpad` | `linux.usbip.usb-audio` | **wip** | `ds-l0-device-touchpad-format-dimensions` |
| `motion` / `acceptance/dualsense/motion` | `linux.uinput` | **wip** | `ds-vg-exp0008-sdl-standard-motion` |
| `motion` / `acceptance/dualsense/motion` | `linux.uhid.usb` | **wip** | `ds-vg-exp0008-sdl-standard-motion` |
| `motion` / `acceptance/dualsense/motion` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `motion` / `acceptance/dualsense/motion` | `linux.usbip.usb-audio` | **wip** | `ds-vg-exp0008-sdl-standard-motion` |
| `battery` / `acceptance/dualsense/battery` | `linux.uinput` | **wip** | `ds-l0-device-usb01-full-fields` |
| `battery` / `acceptance/dualsense/battery` | `linux.uhid.usb` | **wip** | `ds-l0-device-usb01-full-fields` |
| `battery` / `acceptance/dualsense/battery` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `battery` / `acceptance/dualsense/battery` | `linux.usbip.usb-audio` | **wip** | `ds-l0-device-usb01-full-fields` |
| `rumble` / `acceptance/dualsense/rumble` | `linux.uinput` | **wip** | `ds-l0-device-usb02-valid-flags` |
| `rumble` / `acceptance/dualsense/rumble` | `linux.uhid.usb` | **wip** | `ds-l0-device-usb02-valid-flags` |
| `rumble` / `acceptance/dualsense/rumble` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `rumble` / `acceptance/dualsense/rumble` | `linux.usbip.usb-audio` | **wip** | `ds-l0-device-usb02-valid-flags` |
| `lightbar` / `acceptance/dualsense/lightbar` | `linux.uinput` | **wip** | `ds-l0-led-inventory`, `ds-l0-led-common-offsets`, `ds-l0-led-valid-flags`, `ds-l0-led-lightbar-setup`; `ds-l0-device-usb02-valid-flags` |
| `lightbar` / `acceptance/dualsense/lightbar` | `linux.uhid.usb` | **wip** | `ds-l0-led-inventory`, `ds-l0-led-common-offsets`, `ds-l0-led-valid-flags`, `ds-l0-led-lightbar-setup`; `ds-l0-device-usb02-valid-flags` |
| `lightbar` / `acceptance/dualsense/lightbar` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `lightbar` / `acceptance/dualsense/lightbar` | `linux.usbip.usb-audio` | **wip** | `ds-l0-led-inventory`, `ds-l0-led-common-offsets`, `ds-l0-led-valid-flags`, `ds-l0-led-lightbar-setup`; `ds-l0-device-usb02-valid-flags` |
| `player-indicators` / `acceptance/dualsense/player-indicators` | `linux.uinput` | **wip** | `ds-l0-led-inventory`, `ds-l0-led-player-led-bits`, `ds-l0-led-valid-flags`; `ds-l0-device-usb02-valid-flags` |
| `player-indicators` / `acceptance/dualsense/player-indicators` | `linux.uhid.usb` | **wip** | `ds-l0-led-inventory`, `ds-l0-led-player-led-bits`, `ds-l0-led-valid-flags`; `ds-l0-device-usb02-valid-flags` |
| `player-indicators` / `acceptance/dualsense/player-indicators` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `player-indicators` / `acceptance/dualsense/player-indicators` | `linux.usbip.usb-audio` | **wip** | `ds-l0-led-inventory`, `ds-l0-led-player-led-bits`, `ds-l0-led-valid-flags`; `ds-l0-device-usb02-valid-flags` |
| `microphone-led` / `acceptance/dualsense/microphone-led` | `linux.uinput` | **wip** | `ds-l0-led-inventory`, `ds-l0-led-mute-led-off-on`, `ds-l0-led-valid-flags`; `ds-l0-device-usb02-valid-flags` |
| `microphone-led` / `acceptance/dualsense/microphone-led` | `linux.uhid.usb` | **wip** | `ds-l0-led-inventory`, `ds-l0-led-mute-led-off-on`, `ds-l0-led-valid-flags`; `ds-l0-device-usb02-valid-flags` |
| `microphone-led` / `acceptance/dualsense/microphone-led` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `microphone-led` / `acceptance/dualsense/microphone-led` | `linux.usbip.usb-audio` | **wip** | `ds-l0-led-inventory`, `ds-l0-led-mute-led-off-on`, `ds-l0-led-valid-flags`; `ds-l0-device-usb02-valid-flags` |
| `adaptive-triggers` / `acceptance/dualsense/adaptive-triggers` | `linux.uinput` | **wip** | `ds-l0-device-adaptive-trigger-mode-block` |
| `adaptive-triggers` / `acceptance/dualsense/adaptive-triggers` | `linux.uhid.usb` | **wip** | `ds-l0-device-adaptive-trigger-mode-block` |
| `adaptive-triggers` / `acceptance/dualsense/adaptive-triggers` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `adaptive-triggers` / `acceptance/dualsense/adaptive-triggers` | `linux.usbip.usb-audio` | **wip** | `ds-l0-device-adaptive-trigger-mode-block` |
| `headset-audio` / `acceptance/dualsense/headset-audio` | `linux.uinput` | **wip** | `audio-dualsense-hid-routing` |
| `headset-audio` / `acceptance/dualsense/headset-audio` | `linux.uhid.usb` | **wip** | `audio-dualsense-hid-routing` |
| `headset-audio` / `acceptance/dualsense/headset-audio` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `headset-audio` / `acceptance/dualsense/headset-audio` | `linux.usbip.usb-audio` | **wip** | `audio-dualsense-hid-routing` |
| `speaker-audio` / `acceptance/dualsense/speaker-audio` | `linux.uinput` | **wip** | `audio-dualsense-hid-routing` |
| `speaker-audio` / `acceptance/dualsense/speaker-audio` | `linux.uhid.usb` | **wip** | `audio-dualsense-hid-routing` |
| `speaker-audio` / `acceptance/dualsense/speaker-audio` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `speaker-audio` / `acceptance/dualsense/speaker-audio` | `linux.usbip.usb-audio` | **wip** | `audio-dualsense-hid-routing` |
| `calibration` / `acceptance/dualsense/calibration` | `linux.uinput` | **wip** | `ds-l0-device-feature05-shape` |
| `calibration` / `acceptance/dualsense/calibration` | `linux.uhid.usb` | **wip** | `ds-l0-device-feature05-shape` |
| `calibration` / `acceptance/dualsense/calibration` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `calibration` / `acceptance/dualsense/calibration` | `linux.usbip.usb-audio` | **wip** | `ds-l0-device-feature05-shape` |

## Minimal owner-authorized capture plan (all proposed, not run)

**1. Owner-authorized read-only first:** Anders has one physical DualSense 054c:0ce6 with stick drift and broken triggers. Obtain sanitized USB interface/HID descriptor and only feature GET 0x03, 0x05, 0x09, 0x20 at bounded lengths; redact identity/calibration values. **No output reports without his approval.** 2. Map short, absent or failing features to the Linux/SDL probe/fallback claims; do not use broken triggers for physical range calibration. 3. Only with separate approval later, bounded low-intensity outputs and kernel/SDL contention trials.

**No evidence:** any uncited field above, actual hardware response to unissued output reports, exact consumer backend on Anders's host, per-instance private identity values, physical timing/force/IMU parity. **Cloud agent (realized-controller research parity)**
