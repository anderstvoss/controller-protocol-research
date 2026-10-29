# Switch Pro — source citation map and capture handoff (K)

**Research parity, part 2: consumers and decisions** · source-only analysis of virtualgamepad `8f60dcce577ab02bd8ed8b3426349729d417393c`. **No host run, report capture or hardware operations performed.** This is not a statement that acceptance-manifest WIP cells pass. Each offset below is **0-based within the unnumbered report payload**, excluding the report-ID prefix when one exists; the device-side report-ID name is included in the field. Fields lacking a specific independent record are marked **uncited**, even when Rust code explicitly assigns them. Source-supported consumer parsing is not proof of retail fidelity. `source_only` records differ from `virtual_host_run` B records and from physical validation.

## Complete emitted/answered field groups by realization

| Target / payload byte or field | Encoded behavior | virtualgamepad code line(s) | Existing evidence record or **uncited** |
| --- | --- | --- | --- |
| linux.uhid.usb: **0x30:0** | input frame timer/counter | `crates/gr-curated-controllers/src/switch_pro.rs` 654–657 | `swpro-l0-device-report30-full` |
| linux.uhid.usb: **0x30:1** | fixed 0x80 battery/USB power | `crates/gr-curated-controllers/src/switch_pro.rs` 657 | `swpro-l0-device-battery-connection-bits` |
| linux.uhid.usb: **0x30:2–4** | face, system, shoulder and D-pad bits | `crates/gr-curated-controllers/src/switch_pro.rs` 658–677 | `swpro-l0-device-report30-full` |
| linux.uhid.usb: **0x30:5–10** | paired 12-bit sticks and Y compensation | `crates/gr-curated-controllers/src/switch_pro.rs` 639–653, 678–690 | `swpro-l0-openpuck-imu-sticks` |
| linux.uhid.usb: **0x30:11–47** | sample counter and 3× IMU signed 16-bit values | `crates/gr-curated-controllers/src/switch_pro.rs` 691–710 | `swpro-l0-device-report30-full` |
| linux.uhid.usb: **0x30:48–62** | reserved/zero | `crates/gr-curated-controllers/src/switch_pro.rs` 654–710 | **uncited** |
| linux.uhid.usb: **0x81 USB reply** | 0x80 handshake ACK, Pro type, synthetic identity | `crates/gr-curated-controllers/src/switch_pro.rs` 722–733 | `swpro-l0-device-usb-cmd-sequence` |
| linux.uhid.usb: **0x21:12–13** | ACK flags and subcommand ID | `crates/gr-curated-controllers/src/switch_pro.rs` 753–802 | `swpro-l0-device-subcmd-ack-byte` |
| linux.uhid.usb: **0x21:14–25 for 0x02** | firmware/type/synthetic MAC/colours-present byte | `crates/gr-curated-controllers/src/switch_pro.rs` 763–769 | `swpro-l0-device-info02-fields` |
| linux.uhid.usb: **0x21:14–62 for 0x10** | SPI address, 0x6020 IMU, 0x603d stick and 0x6050 colour fallbacks | `crates/gr-curated-controllers/src/switch_pro.rs` 735–750, 770–783 | `swpro-l0-device-factory-spi-map` |
| linux.uhid.usb: **0x21 0x03,0x04,0x21/default** | report mode and other synthetic ACKs | `crates/gr-curated-controllers/src/switch_pro.rs` 785–801 | `swpro-l0-consumer-imu-rumble-ack-gates` |
| linux.uhid.usb: **UHID descriptor, VID/PID and bus** | 057e:2009 USB report declarations | `crates/gr-curated-controllers/src/switch_pro.rs` 804–836; gr-controller-wire/src/lib.rs | `swpro-l0-openpuck-hid-shape` |
| linux.uinput: **uinput capabilities** | EV_KEY, ABS, FF and axes/hat; no native subcommand endpoint | `crates/gr-curated-controllers/src/switch_pro.rs` 585–637, 837–875 | `swpro-vg-exp0011-evdev-mapping` |
| linux.uhid.usb: **output handling/period** | 250Hz virtual output timing; HD rumble physical waveform unproven | `crates/gr-curated-controllers/src/switch_pro.rs` protocol.rs 54–63; worker state | `swpro-l0-device-usb-cadence-conflict` |

**Descriptor and output boundaries:** These are fields grouped by contiguous report ranges or identical semantics; preserved reserved-byte holes remain uncited. `linux.uinput` supplies evdev capabilities/events, not HID GET_REPORT, SPI or XUSB. `linux.dummy_hcd.usb-hid` is **not-supported** in the pinned manifest because f_hid cannot satisfy required GET_REPORT metadata/negative replies. `linux.usbip.usb-audio` (where declared) is a different composite topology, not available simply by changing UHID bus identity; its full audio fields are uncited absent a pinned independently verified host run. Reverse output decoding is a consumer contract, not an observed physical output.

## Proposed evidence IDs for existing acceptance-manifest cells

Source: `acceptance/virtualgamepad.switch-pro.toml` (pinned revision above, original per-cell `test_id`). **Suggestions are not manifest edits or promotions**. A document/claim can support source evidence; a virtual-host claim only supports its exact historical consumer and backend. All current status and `research_revision` values are retained. Any report field with thin secondary only, especially DS4 Bluetooth and Xbox 360 wired XUSB, remains **unknown** for physical fidelity.

| Function / test ID | Realization | Current cell | Suggested existing claim IDs (no acceptance promotion) |
| --- | --- | --- | --- |
| `buttons` / `acceptance/switch-pro/buttons` | `linux.uinput` | **wip** | `swpro-vg-exp0017-individual-uhid` |
| `buttons` / `acceptance/switch-pro/buttons` | `linux.uhid.usb` | **wip** | `swpro-vg-exp0017-individual-uhid` |
| `buttons` / `acceptance/switch-pro/buttons` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `sticks` / `acceptance/switch-pro/sticks` | `linux.uinput` | **wip** | `swpro-vg-exp0009-sdl-motion` |
| `sticks` / `acceptance/switch-pro/sticks` | `linux.uhid.usb` | **wip** | `swpro-vg-exp0009-sdl-motion` |
| `sticks` / `acceptance/switch-pro/sticks` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `triggers` / `acceptance/switch-pro/triggers` | `linux.uinput` | **wip** | `swpro-vg-exp0017-individual-uhid` |
| `triggers` / `acceptance/switch-pro/triggers` | `linux.uhid.usb` | **wip** | `swpro-vg-exp0017-individual-uhid` |
| `triggers` / `acceptance/switch-pro/triggers` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `identity` / `acceptance/switch-pro/identity` | `linux.uinput` | **wip** | `swpro-l0-device-info02-fields` |
| `identity` / `acceptance/switch-pro/identity` | `linux.uhid.usb` | **wip** | `swpro-l0-device-info02-fields` |
| `identity` / `acceptance/switch-pro/identity` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `lifecycle` / `acceptance/switch-pro/lifecycle` | `linux.uinput` | **wip** | `swpro-l0-consumer-kernel-open-order` |
| `lifecycle` / `acceptance/switch-pro/lifecycle` | `linux.uhid.usb` | **wip** | `swpro-l0-consumer-kernel-open-order` |
| `lifecycle` / `acceptance/switch-pro/lifecycle` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `motion` / `acceptance/switch-pro/motion` | `linux.uinput` | **wip** | `swpro-vg-exp0009-sdl-motion` |
| `motion` / `acceptance/switch-pro/motion` | `linux.uhid.usb` | **wip** | `swpro-vg-exp0009-sdl-motion` |
| `motion` / `acceptance/switch-pro/motion` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `battery` / `acceptance/switch-pro/battery` | `linux.uinput` | **wip** | `swpro-l0-device-battery-connection-bits` |
| `battery` / `acceptance/switch-pro/battery` | `linux.uhid.usb` | **wip** | `swpro-l0-device-battery-connection-bits` |
| `battery` / `acceptance/switch-pro/battery` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `player-indicators` / `acceptance/switch-pro/player-indicators` | `linux.uinput` | **wip** | `swpro-l0-linux-led-battery-consumer` |
| `player-indicators` / `acceptance/switch-pro/player-indicators` | `linux.uhid.usb` | **wip** | `swpro-l0-linux-led-battery-consumer` |
| `player-indicators` / `acceptance/switch-pro/player-indicators` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `hd-rumble` / `acceptance/switch-pro/hd-rumble` | `linux.uinput` | **wip** | `swpro-l0-device-rumble-word-tables` |
| `hd-rumble` / `acceptance/switch-pro/hd-rumble` | `linux.uhid.usb` | **wip** | `swpro-l0-device-rumble-word-tables` |
| `hd-rumble` / `acceptance/switch-pro/hd-rumble` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |
| `spi-calibration` / `acceptance/switch-pro/spi-calibration` | `linux.uinput` | **wip** | `swpro-l0-device-factory-spi-map` |
| `spi-calibration` / `acceptance/switch-pro/spi-calibration` | `linux.uhid.usb` | **wip** | `swpro-l0-device-factory-spi-map` |
| `spi-calibration` / `acceptance/switch-pro/spi-calibration` | `linux.dummy_hcd.usb-hid` | **not-supported** | No evidence to override refusal |

## Minimal owner-authorized capture plan (all proposed, not run)

**No physical Switch Pro on hand.** If acquired, capture sanitized USB interface/descriptor read-only, then with authorized host interaction inspect 0x80/0x81, 0x21/0x30 and SPI 0x6020/0x603d/0x6050/0x8010 with bounds and report mode/ACK sequence. Differentiate hid-nintendo bound and generic HID; HD rumble/LED only after explicit authorization. Never publish pairing MAC or private SPI.

**No evidence:** any uncited field above, actual hardware response to unissued output reports, exact consumer backend on Anders's host, per-instance private identity values, physical timing/force/IMU parity. **Cloud agent (realized-controller research parity)**
