# Switch Pro Controller — L0 device and consumer protocol research (Package C)

**Evidence boundary:** this ledger is based on pinned Linux hid-nintendo, SDL 3.2.0 Switch HIDAPI, OpenPuck emulation, and dekuNukem's independent community reverse-engineering notes. It does **not** establish a physical retail packet trace, authenticated retail USB/BT descriptor, physical HD-rumble transfer function, or measured device clock. No hardware was operated, and no `virtualgamepad` code was edited.

## Pinned Linux/SDL, device emulator and independent community sources

| Source ID | Revision | Content | Evidence owner |
| --- | --- | --- | --- |
| `audio-linux-hid-nintendo` | Linux `4056b3c9d3c92ea45955641dbafeb9b960e146ef` | `drivers/hid/hid-nintendo.c`, SHA256 `0ed5027206c64408b513cab219b05a5753cc6ed364883c7460abc8ba1074982f` | Host Linux consumer |
| `audio-sdl-switch-pro` | SDL `535d80badefc83c5c527ec5748f2a20d6a9310fe` | `src/joystick/hidapi/SDL_hidapi_switch.c`, SHA256 `a55cbd9df00707114c511fae33149900e556d362c37a7f9c255d821b12e4a030` | Host SDL consumer |
| `swpro-openpuck-mode` | OpenPuck `29f4d1e8b85c0a7c19e0c8b977a1a56a2c42ea6d` | `OpenPuck/mode_switch_pro.cpp`, SHA256 `13f5c426b06991b44c511e0fbe51cdd0f8133a1b5072233ad8f643356202c767` | Emulated compatible device, **not** retail capture |

Five new `kind: research_lead` community sources from [dekuNukem's Nintendo Switch Reverse Engineering](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/tree/b354f21ae81f7b0d1d060b2b61e66ad0d9bc1756) are pinned at `b354f21ae81f7b0d1d060b2b61e66ad0d9bc1756`. Their individual SHA-256 values and section/line locators are in the corresponding source records:

| Source ID | File | Relevant lines |
| --- | --- | --- |
| `swpro-dekunukem-usb-hid-notes` | `USB-HID-Notes.md` | 5–43 USB 0x80/0x81 commands and handshake |
| `swpro-dekunukem-bluetooth-hid-subcommands-notes` | `bluetooth_hid_subcommands_notes.md` | 53–81 device info/mode, 146–173 SPI, 306–314 IMU, 379–381 vibration |
| `swpro-dekunukem-spi-flash-notes` | `spi_flash_notes.md` | 90–129 factory/user calibration, colours and markers |
| `swpro-dekunukem-rumble-data-table` | `rumble_data_table.md` | 1–55 frequency/amplitude encoding, 55–332 tables |
| `swpro-dekunukem-bluetooth-hid-notes` | `bluetooth_hid_notes.md` | 43–64 rumble, 116–118 cadence, 132–181 input structure |

**Transport convention:** every claim based on reading source code or documentation uses `source_only`, regardless of its `evidence_role`; five unresolved *physical measurement* gaps use their intended `usb` or `bluetooth` transport instead.

The source IDs beginning `audio-` already existed and are reused because they pin the entire relevant file, not just its original audio-focused locator. No code excerpts, raw device data or private machine captures are redistributed.

## L0 protocol and realization inventory

| Function / boundary | Source-grounded description | Claim IDs | What remains unknown |
| --- | --- | --- | --- |
| USB vs Bluetooth and startup | Linux distinguishes USB command 0x80/ack 0x81 (status/handshake/baudrate/timeout) from 0x01 subcommands; SDL has its own USB and Bluetooth initialization paths | `swpro-l0-linux-usb-handshake`, `swpro-l0-sdl-usb-initialization`, `swpro-l0-physical-bluetooth-unknown` | Exact retail descriptors, BT HIDP/SDP/link behavior, firmware/startup timing |
| Report roles | Inputs 0x21 subcommand reply, 0x30 full state + IMU, 0x3F simple, 0x81 USB ack; SDL also recognizes 0x31 full/MCU. Outputs 0x01 rumble+subcommand, 0x10 rumble-only, 0x80 USB command | `swpro-l0-linux-report-id-routing`, `swpro-l0-sdl-report-modes`, `swpro-l0-openpuck-hid-shape` | Which retail modes and fallback paths are supported per transport and revision |
| Subcommands, response | Output 0x01 packet counter and eight motor bytes precede subcommand ID/data. Linux waits for matching 0x21 subcommand ID and retries one timeout. OpenPuck uses its own 0x21 ACK synthesis | `swpro-l0-linux-subcmd-retry-ack`, `swpro-l0-openpuck-output-accept` | Physical NACK/error matrix, retry safety, pacing, side effects |
| Gamepad controls | Full report common prefix includes counter, battery/connection, three button bytes, packed 12-bit left/right sticks, rumble echo. Linux maps Pro d-pad to ABS_HAT0 and sticks to ABS_X/Y, ABS_RX/RY | `swpro-l0-linux-full-input-shape`, `swpro-l0-linux-pro-button-mapping`, `swpro-l0-openpuck-imu-sticks` | Native packet bit parity and axis sign, orientation, digital trigger identity |
| IMU | Linux interprets 0x30 as three 6-axis IMU samples and exposes a separate accelerometer/gyro evdev node; OpenPuck emits synthesized sample triples after report-mode selection | `swpro-l0-linux-imu-evdev-consumer`, `swpro-l0-openpuck-imu-sticks` | Physical sample counts/clock, overflow, calibration, sign/permutation, drift and SDL backend association |
| Memory / calibration | SDL documents factory stick 0x603D..0x604E, user stick 0x8010..0x8025, factory IMU 0x6020..0x6037, user IMU 0x8026..0x8039. OpenPuck implements synthetic SPI response and user mirror | `swpro-l0-sdl-spi-calibration-reads`, `swpro-l0-openpuck-spi-identity`, `swpro-l0-physical-spi-calibration-unknown` | Retail flash bytes/size/protection and write/persistence/boot policy |
| HD rumble | Linux/SDL encode motor words in 0x01 or 0x10; SDL limits writes to 30 ms and refreshes after 50 ms. OpenPuck maps words to generic magnitudes, not native waveform | `swpro-l0-linux-rumble-framing`, `swpro-l0-sdl-rumble-rate-policy`, `swpro-l0-physical-rumble-unknown` | Physical frequency/amplitude response, two-motor independence, reset/stop, transport differences |
| Identity, LEDs and power | Device-info subcommand, battery/charging byte, player LEDs via 0x30 and host evdev/LED/power mapping. OpenPuck invents a compatible device info response | `swpro-l0-linux-led-battery-consumer`, `swpro-l0-openpuck-spi-identity`, `swpro-l0-physical-usb-identity-unknown` | Retail per-revision firmware/serial/color data, battery voltage, LED timing, actual host behavior |
| Audio | Existing `audio-switch-pro-hid-consumers-no-audio` is **consumer evidence only** for the inspected HID paths | existing claim | Other physical transport audio endpoints not exhaustively investigated |

`swpro-l0-*` claims now include **21 consumer** and **20 device** records: **32 source-supported**, **8 unknown**, and **1 conflicted** (the documented cadence mismatch). The independent community source grounds device-side *research* descriptions, while OpenPuck remains an emulator; both require physical checks. An emulated-device layout is useful evidence about a *candidate device-side state machine* but not independent retail hardware validation. No new experiment is marked `passed` in C.

## Existing merged virtualgamepad observations (B, research PR #58)

B's published records are now part of `main`, not pending. See [`swpro-vg-exp0009-sdl-motion`](../../records/claim/swpro-vg-exp0009-sdl-motion.json), [`swpro-vg-exp0009-rumble-unverified`](../../records/claim/swpro-vg-exp0009-rumble-unverified.json), [`swpro-vg-exp0010-evdev-ff`](../../records/claim/swpro-vg-exp0010-evdev-ff.json), [`swpro-vg-exp0011-evdev-mapping`](../../records/claim/swpro-vg-exp0011-evdev-mapping.json), [`swpro-vg-exp0014-individual-evdev`](../../records/claim/swpro-vg-exp0014-individual-evdev.json), [`swpro-vg-exp0016-eden-steam-neutral`](../../records/claim/swpro-vg-exp0016-eden-steam-neutral.json), and [`swpro-vg-exp0017-individual-uhid`](../../records/claim/swpro-vg-exp0017-individual-uhid.json). B provides *virtual-device consumer observations*, not a retail physical Switch Pro baseline. C's source-derived claims cite B where it informs a consumer gap, without promoting hardware fidelity.

## Independent device protocol research (scope and disagreements)

| Question | Community-supported result | Claim(s) | Boundary |
| --- | --- | --- | --- |
| USB 0x80 | 0x01 status, 0x02 handshake, 0x03 baudrate, second 0x02 handshake, 0x04 keep USB | `swpro-l0-device-usb-cmd-sequence` | Actual startup latencies and retail revision unmeasured |
| 0x01 output / 0x21 reply | 4-bit counter, left/right 4-byte motor words, subcommand + args; ACK MSB and response type, echo ID | `swpro-l0-device-subcmd-ack-byte` | NACK/retry and errors need device bench |
| 0x02 info reply | Firmware 2 bytes, type (0x03 Pro), MAC 6 bytes, SPI-colours flag at reply payload byte 11 | `swpro-l0-device-info02-fields` | Real identifiers intentionally not published |
| SPI | 0x6020 IMU factory, 0x603D/6046 factory sticks, 0x6050–0x605B colours, 0x8010/801B/8026 B2 A1 user magic | `swpro-l0-device-factory-spi-map`, `swpro-l0-device-user-spi-magic` | OpenPuck mirrors portions; real data and protected writes unknown |
| 0x30 full | Timer, battery/connection, buttons, 12-bit sticks, vibrator byte, three six-axis IMU samples | `swpro-l0-device-report30-full`, `swpro-l0-device-battery-connection-bits` | Sample calibration and physical accuracy unknown |
| USB report cadence | Community notes mention full mode 60 Hz and Pro 120 Hz, but do not settle USB; OpenPuck emulator uses 4 ms | `swpro-l0-device-nominal-pro-report-period`, `swpro-l0-device-usb-cadence-conflict`, `swpro-l0-device-physical-usb-period-unknown` | **No corroborated nominal physical USB period**; timing conflict documented |
| HD rumble | Community frequency log encoding, piecewise amplitude words/table; separate host encoders | `swpro-l0-device-rumble-word-tables` | No actual motor transfer-function proof |

## What this settles for virtualgamepad (#156)

| #156 question | Finding at pinned source revision | Claim ID | Host source line range |
| --- | --- | --- | --- |
| Per-instance MAC / serial / GUID | **Yes.** SDL derives a serial from the 0x02 MAC, but puts controller type (not MAC) into GUID byte 15; player number is independently assigned. Kernel also uses MAC-derived evdev `uniq`. | `swpro-l0-consumer-sdl-mac-serial-guid`, `swpro-l0-consumer-linux-mac-uniq` | SDL 629–652, 1357–1454, 1498–1509; Linux 2477–2515, 2130–2134, 2188–2198 |
| 0x40 IMU / 0x48 vibration and ACK sequencing | **Both.** Kernel synchronously waits for both and 0x03 mode; SDL calls 0x48 during open and sends 0x40 on sensor enable, not unconditionally at startup. Neither source establishes required full IMU stream before these ACKs. | `swpro-l0-consumer-imu-rumble-ack-gates` | Linux 1340–1377, 2600–2633; SDL 930–934, 1511–1567, 1790–1805 |
| Missing/0xFF user and factory calibration | Kernel falls back to factory if user marker absent and hardcoded defaults for implausible/missing stick calibration; SDL ignores missing user, **requires factory stick response**, and patches individual 0xFFF fields. IMU fallbacks differ. | `swpro-l0-consumer-kernel-calibration-fallback`, `swpro-l0-consumer-sdl-calibration-fallback` | Linux 1080–1215, 1273–1317; SDL 936–1090 |
| Colours advertised but 0x6050–0x605B all 0xFF | **No evidence** of colour reads or all-FF handling in inspected kernel/SDL initialization paths. Other applications and firmware behavior unknown. | `swpro-l0-consumer-colour-spi-no-evidence` | Linux 2477–2637; SDL 629–684, 936–1090, 1457–1567 |
| What each consumer does at open | Kernel: USB handshake, 0x02 info, stick/IMU SPI, 0x40, 0x03, 0x48. SDL: info probe, optional USB setup, stick user/factory SPI, IMU factory/user SPI, 0x48, hint-selected mode, USB reports; 0x40 on sensor activation. | `swpro-l0-consumer-kernel-open-order`, `swpro-l0-consumer-sdl-open-order` | Linux 2518–2637; SDL 1457–1567, 1800–1805 |
| Is Steam's neutral-offset hypothesis proven by SPI or MAC? | **No evidence.** B's report is unversioned and lacks backend/mapping provenance; source-only consumer code does not resolve causation. | `swpro-l0-consumer-steam-neutral-causation-unknown` | B `swpro-vg-exp0016-eden-steam-neutral`; SDL/Linux above |

## Lab qualification — proposed, no Switch Pro on hand (#136); none performed

All physical operations require owner-approved reference hardware, permission and a disposable/isolated host where appropriate. Avoid copying identifying pairing keys, Bluetooth addresses, serials, raw private calibration, or sensitive machine paths into the public corpus. Publish sanitized semantic outcomes and fixture lineage only after review.

| Gate | Test / method | Required recorded measurements | Pass / fallback |
| --- | --- | --- | --- |
| C-P1 | Reference retail Pro USB read-only inventory | physical make/model/firmware safely scoped; HID descriptor digest and public descriptor structure, interfaces and bus ancestry; exact driver, kernel/SDL version | Descriptor has clear owner provenance; otherwise keep device identity unknown |
| C-P2 | USB startup handshake capture | guarded process-owned path; 0x80 commands/0x81 responses; 0x01 subcommands, 0x21 ACK/NACK; dependency order and timeouts | Reproducible three independent startups; include negative/retry traces, do not assume identical across revisions |
| C-P3 | Input parity / mapping | isolated press/release one control at a time, sticks to endpoints/neutral, full 0x30 and simple-mode cases, battery/LED changes | Bit-exact roles and semantic labels across repeated sessions; avoid simultaneous-sweep permutation blindness |
| C-P4 | IMU and clock | known motion/no-motion reference positions, packet counters, sample triples, timestamps, calibration effect; Linux evdev and SDL separately | Sanity/range/axes and independent neutral baseline; no physical units before calibrated corroboration |
| C-P5 | SPI / memory | read-only first: size, factory/user calibration regions, error replies, per-device variability; separately authorize reversible write tests | Source address layout either corroborated or documented as variant-specific. No unapproved writes |
| C-P6 | HD-rumble output | two encoded motor words and stop/idle transitions at controlled safe magnitudes, per-motor response; compare USB and BT paths | Numeric source decode is not sufficient; physical actuation semantics need independent measurement |
| C-P7 | Bluetooth-specific lab | SDP/HIDP framing, pairing/reconnect, report lengths/IDs, input and output response, failure/cleanup; safely redact identities | Independent transport matrix; do not reuse USB success as BT evidence |
| C-P8 | Consumer differential | same reference and virtual experiment on fixed Linux/SDL/Steam/Eden builds; identify backend, active mapping and exact selected path | Categorize expected/observed divergences, link to merged B records, no source evidence promotion by virtual-only success |

## Integration guidance

Continue in `gr-controllers` for typed native state and codecs and OS providers for realization/I/O only; do not put Nintendo protocol semantics in a shared provider or infer physical timing from SDL's host policy. Use C claims and merged B record IDs in later citation maps, distinguishing community source descriptions, emulated-device behavior and real-host observations. Switch Pro *USB* and *Bluetooth* require distinct realization acceptance; no dual-mode physical pass is implied. Packages D–F should maintain the same device/consumer split.

**Cloud agent (realized-controller research parity)**
