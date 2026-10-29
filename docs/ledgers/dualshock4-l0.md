# DualShock 4 — L0 device protocol and consumer realization ledger (Package E)

**Scope:** source-only research, not a retail-device capture or support promotion. Each new claim explicitly sets `evidence_role`: community descriptions of device report shapes and compatibility implementations may support `device` claims at `source_supported` only; Linux/SDL/hid-sony paths are `consumer`. All new claims use transport `source_only` (physical USB, Bluetooth and wireless-adapter coverage remains unknown). No hardware tests or virtualgamepad edits were made. B's historical `ds4-vg-*` claims remain separate, unchanged and consumer-scoped.

## Sources and blocked primary pages

| Source ID | Pinned source / provenance | Evidence limit |
| --- | --- | --- |
| `audio-linux-hid-playstation` | Linux `4056b3c9d3c92ea45955641dbafeb9b960e146ef`, `drivers/hid/hid-playstation.c` | Current kernel/evdev consumer; not an observed DS4 firmware |
| `ds4-linux-hid-sony-v61` | Linux v6.1 commit `830b3c68c1fb1e9176028d02ef86f3cf76aa2476`, `drivers/hid/hid-sony.c`; SHA256 `297b84f9fb1093511590bbaf57f89119cdbf998ca3650099b045b5fb0204b88d` | Historical pre-hid-playstation consumer |
| `audio-sdl-ps4` | SDL `535d80badefc83c5c527ec5748f2a20d6a9310fe`, `src/joystick/hidapi/SDL_hidapi_ps4.c` | SDL3 consumer/host policy |
| `openpuck-ds4` | OpenPuck `29f4d1e8b85c0a7c19e0c8b977a1a56a2c42ea6d`, `mode_hidgyro.cpp` | Independently developed emulated-compatible device behavior, not retail evidence |
| `ds4-community-playstation-protocol` | noisyloop `game-research` `290e4a26eeed8a1f659150e23d527c39f46a3af3`, `docs/03-console-protocols/02-playstation.md` lines 13–42; SHA256 `61101df2bc188bcfbb52d882d52b5076318138553b94cc428d27b01577e05bcb` | Public secondary community summary; references Linux and PS4 Developer Wiki, not independently captured physical hardware |

**Source pending: fetch blocked.** The PS4 Developer Wiki DS4 pages were read through public search but could not be fetched as exact hashed bytes in the available file-access environment. They are **not** recorded as verified pinned sources and are **not** used to upgrade device claims:
- `https://www.psdevwiki.com/ps4/DS4-USB` — USB HID report descriptor, feature declarations, report IDs
- `https://www.psdevwiki.com/ps4/DS4-BT` — Bluetooth HIDP/feature `0x02/0x05/0xA3`, CRC and transport state

The owner/local agent can pull and hash those exact pages or a stable wiki revision. The pinned noisyloop summary is a *secondary* community `research_lead`, explicitly not a substitute for authenticated retail packet proof. Do not copy the wiki's sample bytes into public records until independently sanitized and approved.

## L0 protocol inventory

| Protocol area | Supported source description | Claim IDs | Measurement still missing |
| --- | --- | --- | --- |
| USB full input | ID `0x01`, 64 bytes. Common prefix: left/right sticks, face/hat/shoulder buttons, analog triggers; later signed 16-bit gyro and acceleration, timestamp, battery, touch history | `ds4-l0-device-usb01-input`, `ds4-l0-consumer-kernel-transport-parsers` | Physical USB sample/descriptor and revision differences |
| Bluetooth simple vs full | Minimal `0x01` (10 bytes) vs full `0x11` (78 bytes), 2-byte leading transport header, trailing CRC32; enhanced mode can follow calibration feature reads | `ds4-l0-device-bt01-11-input-modes`, `ds4-l0-consumer-sdl-enhanced-switch` | Bluetooth negotiation/CRC and pairing evidence |
| Output | USB `0x05` (32 bytes); Bluetooth `0x11` (78 bytes), rumble and lightbar controls, Bluetooth header/CRC | `ds4-l0-device-usb05-output`, `ds4-l0-device-bt11-output`, `ds4-l0-consumer-rumble-lightbar-output` | Physical response, intensity/LED calibration, error handling |
| Calibration | USB feature `0x02`/37, BT feature `0x05`/41 with CRC, accelerometer and gyro biases/scales | `ds4-l0-device-feature02-calibration-unknown`, `ds4-l0-consumer-kernel-calibration-fallback`, `ds4-l0-consumer-sdl-calibration-fallback` | Exact per-revision retail calibration bytes; physical sensor ground truth |
| Pairing / MAC | Current Linux USB uses `0x12`/16; earlier hid-sony USB/dongle used `0x81`/7 and MAC from offset 1, BT uniq from HIDP | `ds4-l0-device-feature12-pairing-unknown`, `ds4-l0-device-feature81-mac-unknown`, `ds4-l0-consumer-kernel-pairing12`, `ds4-l0-consumer-hidsony-feature81` | Which actual devices/firmwares implement each feature and privacy-safe identity fixtures |
| Firmware | Feature `0xA3`/49, HW version LE16 at bytes 35–36, FW LE16 at bytes 41–42 expected in Linux drivers | `ds4-l0-device-featurea3-firmware-unknown`, `ds4-l0-consumer-kernel-a3-optional`, `ds4-l0-consumer-hidsony-a3-probe-gate` | Authenticated retail firmware payload; SDL does not read it |
| Touch history | Kernel's USB packet reserves **three 9-byte touch reports**, BT **four**; each report has timestamp plus **two 4-byte contacts**. Secondary summary calls them “3/4 touch points,” which conflates *report history count* with *simultaneous fingers* | `ds4-l0-device-touch-count-conflict`, `ds4-l0-consumer-kernel-touch-report-buffer-count` | Actual active history count per firmware and frame; reconcile primary wiki wording |
| IMU and touch units | Signed gyro/accel LE16, motion timestamps, calibration per-axis from feature, 1920×942 touch coordinate convention | `ds4-l0-device-imu-and-touch-units` | Physical scale, orientation and timestamp rate across revisions |
| Variants | Sony `054c:05c4`, `054c:09cc`, `054c:0ba0` adapter are separate product/receiver concerns; kernel dongle has disconnect/hotplug/calibration state | `ds4-l0-device-revision-identity-unknown`, `ds4-l0-device-wireless-adapter-unknown`, `ds4-l0-consumer-revision-and-dongle-routing` | Exact descriptor and firmware/revision difference matrix |

## What this settles for virtualgamepad / part 2 decision table I

| Question | Finding at pinned source revision | Claim ID / evidence state |
| --- | --- | --- |
| Does a fabricated/stub feature `0xA3` determine DS4 acceptance? | **Yes for historical hid-sony v6.1**: required version request failure aborts its DS4 probe (hid-sony.c 1893–1915, 2850–2863). **No for modern hid-playstation as a fatal gate**: it warns and proceeds on missing `0xA3` (hid-playstation.c 2121–2145, 2791–2795). **No evidence SDL HIDAPI PS4 requests `0xA3`** (SDL_hidapi_ps4.c 76–80, 207–351, 462–647). A synthetic report can support older consumers, not certify physical firmware | `ds4-l0-consumer-hidsony-a3-probe-gate`, `ds4-l0-consumer-kernel-a3-optional`, `ds4-l0-consumer-sdl-a3-no-evidence` |
| Which calibration report starts enhanced motion and what if it fails? | SDL PS4 probes `0x02` then `0x05` on BT and defaults identity bias/scale on failure; old hid-sony treated failure as fatal, modern hid-playstation warns and allows less accurate IMU (SDL 462–647; Linux 1938–2116, 2801–2805) | `ds4-l0-consumer-sdl-calibration-fallback`, `ds4-l0-consumer-hidsony-calibration-gate`, `ds4-l0-consumer-kernel-calibration-fallback` |
| Which USB MAC feature is mandatory? | **Version-dependent consumer policy**: old hid-sony `0x81`/7 (2615–2638), newer hid-playstation `0x12`/16 (2148–2175). No independent retail feature matrix; don't hardcode a universal requirement from either kernel alone | `ds4-l0-consumer-hidsony-feature81`, `ds4-l0-consumer-kernel-pairing12`, device gaps for both |
| Is Bluetooth `0x11` the same as USB `0x01`? | **No**. BT enhanced path uses shifted prefix and CRC and a different output; initial BT minimal path can lack motion/touch | `ds4-l0-consumer-kernel-transport-parsers`, `ds4-l0-device-bt01-11-input-modes` |
| Does `0ba0` wireless adapter equal native DS4 USB? | **No evidence**. Kernel uses a dedicated dongle hotplug state and delayed calibration | `ds4-l0-consumer-revision-and-dongle-routing`, `ds4-l0-device-wireless-adapter-unknown` |
| How many touch points does the report contain? | **Conflicted terminology** in community secondary summary versus kernel's report history arrays: three USB/four BT *samples* holding two contact slots each. No primary retail packet comparison | `ds4-l0-device-touch-count-conflict` ↔ `ds4-l0-consumer-kernel-touch-report-buffer-count` |

Historical B evidence remains valid and limited: `ds4-vg-exp0009-sdl-controls`, `ds4-vg-exp0011-combined-node-discovery`, `ds4-vg-exp0012-interrupted-split` etc. Historical DS4 combined node failed; interrupted split trial was **blocked**, not failed; source research here does not imply a present production regression or physical parity.

## Future lab gates (proposed only; no reference controller in this agent session)

| Gate | Test | Evidence to record |
| --- | --- | --- |
| E-P1 | Authorized genuine DS4 USB `05c4` and `09cc` read-only descriptor/feature inventory | Differentiate revision endpoints and report IDs, redacted hashes, firmware version |
| E-P2 | `0x02`, `0x12`, `0xA3`, `0x81` guarded GET_REPORT, including error paths | Identify actual feature population across revisions; never publish MAC/serial or pairing material |
| E-P3 | Fixed Linux 6.1 hid-sony vs modern hid-playstation start/stop comparison | Confirm probe gates for 0x81, 0x12, 0xA3 and calibration, without confusing host policy with device shape |
| E-P4 | USB vs BT separate input capture | Validate 0x01/0x11 report sizes, CRC and native button/IMU/touch layout with repeated reference sessions |
| E-P5 | DS4 touch packet differential | Count nine-byte touch samples and two contacts; test timestamp, no-contact and controller revision |
| E-P6 | SDL 3.2.0 PS4 HIDAPI and consumer app mapping | Enhanced mode/hint, motion, touch, range, power and failure handling; same-host physical vs virtual |
| E-P7 | Sony 0ba0 receiver dongle dedicated session | Reconnection, calibration worker, identity/ownership and safe teardown without assuming USB parity |
| E-P8 | Output LED/FF plus long-run reproducibility | Bound physical rumble/lightbar actuation and 3+ runs/host restart, no damage or invented fidelity |

**Cloud agent (realized-controller research parity)**
