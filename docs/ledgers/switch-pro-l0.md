# Switch Pro Controller — L0 device and consumer protocol research (Package C)

**Evidence boundary:** this ledger is based solely on pinned Linux hid-nintendo, SDL 3.2.0 Switch HIDAPI and OpenPuck Switch Pro compatibility implementation. It does **not** establish a physical retail packet trace, authenticated retail USB/BT descriptor, physical HD-rumble transfer function, or measured device clock. No hardware was operated, and no `virtualgamepad` code was edited.

## Reused pinned sources and one new independent source

| Source ID | Revision | Content | Evidence owner |
| --- | --- | --- | --- |
| `audio-linux-hid-nintendo` | Linux `4056b3c9d3c92ea45955641dbafeb9b960e146ef` | `drivers/hid/hid-nintendo.c`, SHA256 `0ed5027206c64408b513cab219b05a5753cc6ed364883c7460abc8ba1074982f` | Host Linux consumer |
| `audio-sdl-switch-pro` | SDL `535d80badefc83c5c527ec5748f2a20d6a9310fe` | `src/joystick/hidapi/SDL_hidapi_switch.c`, SHA256 `a55cbd9df00707114c511fae33149900e556d362c37a7f9c255d821b12e4a030` | Host SDL consumer |
| `swpro-openpuck-mode` | OpenPuck `29f4d1e8b85c0a7c19e0c8b977a1a56a2c42ea6d` | `OpenPuck/mode_switch_pro.cpp`, SHA256 `13f5c426b06991b44c511e0fbe51cdd0f8133a1b5072233ad8f643356202c767` | Emulated compatible device, **not** retail capture |

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

`swpro-l0-*` claims include **12 consumer source-supported**, **4 emulated-device source-supported**, and **5 unknown physical-device**. An emulated-device layout is useful evidence about a *candidate device-side state machine* but not independent retail hardware validation. No new experiment is marked `passed` in C.

## Historical virtualgamepad acceptance pointers (pending B)

Research PR [#58](https://github.com/anderstvoss/controller-protocol-research/pull/58), **pending merge**, proposes `swpro-vg-exp0009-sdl-motion`, `swpro-vg-exp0010-evdev-ff`, `swpro-vg-exp0011-evdev-mapping`, `swpro-vg-exp0014-individual-evdev`, `swpro-vg-exp0016-eden-steam-neutral`, `swpro-vg-exp0017-individual-uhid` and `swpro-vg-exp0009-rumble-unverified`. These are historical virtual-device consumer observations, *not* C's source-grounded retail L0 claims. **Do not put those pending IDs into C's claim `sources` or `experiments` arrays** until B merges. B's user-reported Steam/Eden neutral discrepancy is specifically not corroborated by the kernel or SDL mapping alone.

## Proposed lab qualification — future, not performed

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
| C-P8 | Consumer differential | same reference and virtual experiment on fixed Linux/SDL/Steam/Eden builds; identify backend, active mapping and exact selected path | Categorize expected/observed divergences, link to B after merge, no source evidence promotion by virtual-only success |

## Integration guidance

Continue in `gr-controllers` for typed native state and codecs and OS providers for realization/I/O only; do not put Nintendo protocol semantics in a shared provider or infer physical timing from SDL's host policy. Add exact source/claim references to later citation maps only when the pending research PR is merged and pinned. Switch Pro *USB* and *Bluetooth* require distinct realization acceptance; no dual-mode physical pass is implied. Packages D–F should maintain the same device/consumer split.

**Cloud agent (realized-controller research parity)**
