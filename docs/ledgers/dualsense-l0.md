# DualSense L0 protocol and consumer evidence ledger (Package D)

## Scope and provenance

This is a **source-backed L0 ledger**, not a physical device certification or proof that a virtual HID topology is interchangeable with a genuine controller. All source-read claims are `source_only` regardless of `device`/ `consumer` role. Explicit missing physical USB/BT measurements use the relevant transport. All 25 new `ds-l0-*` claims set `evidence_role`.

The baseline is research `main` `c92438d36242fb73c6524a88890f1446aabf42ea` after B #58. Package C #60 is independent and is not imported. All evidence is pinned to existing published source records; no copied vendor firmware, new raw private captures or unpinned experimental branch citations.

| Existing source ID | Pinned revision / file | Evidence role |
| --- | --- | --- |
| `audio-linux-hid-playstation` | Linux `4056b3c9d3c92ea45955641dbafeb9b960e146ef`, `drivers/hid/hid-playstation.c` | Linux HID/evdev consumer contract |
| `audio-sdl-ps5`, `sdl-ps5-baseline` | SDL `535d80badefc83c5c527ec5748f2a20d6a9310fe`, `src/joystick/hidapi/SDL_hidapi_ps5.c` | SDL HIDAPI consumer |
| `dualsense-uhid-gyro-hhd-device-source`, `dualsense-uhid-gyro-hhd-uhid-source`, `hhd-dualsense` | HHD `adbd50ff30614df886a6c76bd8855a64fde5d0b8` virtual DualSense | Independently developed emulated device / compatible protocol model |
| `openpuck-ps-layout` | OpenPuck `29f4d1e8b85c0a7c19e0c8b977a1a56a2c42ea6d`, PlayStation helper mappings | Compatibility helper only; no retail DualSense report capture |
| `vg-alpha1-exp0015` | virtualgamepad `c60c16409e91e39ddba56a78475bdabe3780d1d0` | Maintainer-reported physical DualSense 054c:0ce6, limited read-only USB observations |
| `vg-alpha1-dummy-hcd-poc` | archived virtualgamepad `a5310c605fe033e3165a9b9ae65f5874de1f6ced`, POC lines 46–58 | Maintainer-reported virtual USB gadget vs UHID Steam gyro result |
| `audio-vg-exp0023` | pinned virtualgamepad EXP-0023 | Maintainer physical USB audio topology/subjective routing, already in corpus |

The `audio-vg-exp0023` record is reused, never duplicated. `ds-vg-exp0015-physical-usb-hid` in merged B remains `source_supported` **device** evidence, with explicit “maintainer-reported physical observation, not corpus physical validation”. No new controlled physical experiment is fabricated.

## Protocol/realization inventory

| Dimension | Pinned consumer / emulated-device evidence | New L0 IDs | Missing measurement |
| --- | --- | --- | --- |
| USB/BT report framing | Linux USB input 0x01, 64 bytes; Bluetooth enhanced input 0x31, 78 bytes with CRC, USB output 0x02, BT output 0x31. SDL uses its own BT output prefix and CRC | `ds-l0-kernel-usb-bt-input-shape`, `ds-l0-kernel-output-usb-bt`, `ds-l0-sdl-output-transport` | Retail BT setup and end-to-end output timing |
| USB common input | Sticks/triggers, hat/buttons, gyro/accel, timestamp, two packed touch points, battery/status; Linux evdev mapping, SDL enhanced/default modes | `ds-l0-kernel-input-evdev`, `ds-l0-sdl-input-and-sensor-modes` | Exact reference values and host association |
| Feature reports | GET 0x05 calibration (41 bytes), 0x09 pairing (20), 0x20 firmware (64); SDL uses 0x03 capabilities for third-party paths | `ds-l0-kernel-feature05-calibration`, `ds-l0-kernel-feature09-20-identity`, `ds-l0-sdl-device-feature-probes` | Firmware/revision-scope variations; unknown feature exchange and errors |
| Calibration and timestamps | Linux and SDL parse gyro and accel calibration from 0x05, with distinct failure semantics. SDL announces 250 Hz USB and 1000 Hz BT as consumer metadata; HHD emits synthetic event-driven timestamps | `ds-l0-sdl-calibration-fallback`, `ds-l0-sdl-sensor-availability`, `ds-l0-hhd-touch-motion`, `ds-l0-hhd-steam-gyro-policy` | Measured gyro calibration, timing jitter and physical rate |
| Touch and extra controls | Two packed touch contacts and separate Linux touch/IMU endpoints; SDL touch/gyro enhancement remains backend-dependent | `ds-l0-sdl-touch-battery`, `ds-l0-kernel-input-evdev` | Physical geometry, pressure and multi-backend association |
| Output | Common effects block provides rumble, LED/player indicators, microphone mute/power-save, audio routing and other fields. SDL/HHD and Linux present different realizations | `ds-l0-sdl-output-transport`, `ds-l0-kernel-audio-vs-hid` | Physical adaptive triggers, motor/LED/audio actuation, report ACK/failure semantics |
| Device compatibility implementation | HHD creates virtual Sony-identity USB/BT UHID and supplies synthetic GET responses and encoded motion/touch reports; this is *emulated-device* evidence only | `ds-l0-hhd-uhid-identity`, `ds-l0-hhd-feature-replies`, `ds-l0-hhd-touch-motion` | Authentic retail descriptor, calibration, BT pairing and physical parity |

## Historical virtual-host acceptance and Steam gyro disagreement

Merged B's `ds-vg-exp0006-uhid-startup`, `ds-vg-exp0007-bus-driver-observation`, `ds-vg-exp0008-sdl-standard-motion`, `ds-vg-exp0008-sdl-feedback`, `ds-vg-exp0017-individual-uhid`, `ds-vg-dummy-hcd-steam-gyro` and physical `ds-vg-exp0015-physical-usb-hid` remain separate claim records. They are not reclassified or upgraded here.

The archived [DualSense `dummy_hcd` POC](https://github.com/anderstvoss/virtualgamepad/blob/a5310c605fe033e3165a9b9ae65f5874de1f6ced/docs/POC_DUMMY_HCD_DUALSENSE.md#confirmed-finding-2026-08-15) lines **46–58** reports:

1. Steam Controller Test observed a changing gyro from virtual **USB-gadget/dummy_hcd** presentation.
2. The prior virtual **UHID** DualSense gyro was missing in Steam despite a reportedly shared report format, features, axis mapping and nominal cadence.
3. The same-host USB-gadget POC is **not a physical controller comparison**; no current Steam/SDL build or complete independent differential capture is provided.

`ds-l0-dummy-hcd-steam-gyro-contrast` is a `source_supported` **consumer** historical observation citing the archived source and merged B experiment. The distinct `ds-l0-uhid-gyro-association-hypothesis` is **inferred**, not observed: Steam/SDL might treat sensor association differently when the device originates from `BUS_VIRTUAL`/UHID rather than a USB HID interface. This is a *testable explanation*, not a proven root cause or a reason to edit source report bytes. `ds-l0-steam-input-mode-unmeasured` explicitly preserves missing Steam build, backend and mapping provenance.

## Physical evidence still missing

- A genuine DualSense 054c:0ce6 was read-only inspected in EXP-0015: 273-byte HID descriptor, 0x05/0x09/0x20 feature lengths, 64 increasing timestamps and limited USB audio descriptor fields. The source does **not** provide the actual raw descriptor/calibration/pairing bytes for public cross-reference. Damaged triggers and stick drift make affected mechanical observations unsuitable for quantitative fidelity.
- Bluetooth pairing, HID descriptors/security/CRC and native transport behavior have no controlled public reference.
- Haptics, adaptive triggers, LED, microphone and integrated audio routing require separate semantic measurements. EXP-0023's physical USB UAC1 observations and subjective grip/headphone routing are useful historical *source* evidence, not physical-validation promotion.
- HHD is a compatibility emulator. Linux and SDL are consumers; agreement between them is not an independent real-device bit-level capture.

## Proposed future lab tests (none run in this PR)

| Gate | Apparatus / test | Acceptance evidence and safety boundary |
| --- | --- | --- |
| D-P1 | Owner-approved read-only reference USB DualSense; exact device ancestry, detached identity proof | Private raw descriptors, public sanitized hashes and field map, firmware/hardware/feature sizes and revisions |
| D-P2 | USB feature 0x03/05/09/20 request/reply matrix, safe error paths | Validate feature availability and field semantics by revision; never publish pairing contents or identifiers |
| D-P3 | Reference versus virtual SDL 3.2.0 standard/HIDAPI controls | One-control-at-a-time neutral/min/max and touch report, exact node/backend/mapping names; no phantom physical label claim |
| D-P4 | IMU and timestamp orientation experiment | Measured axes, reference motion and static gravity, sensor clock, jitter, calibrated physical quantities |
| D-P5 | Steam gyro **differential**: UHID `BUS_VIRTUAL` vs `dummy_hcd` USB vs physical reference | Fixed Steam/SDL/kernel build, GUID/serial, hidraw/evdev/sensor node association and driver ownership; determine which boundary loses sensor, not just whether UI moves |
| D-P6 | Output report 0x02/0x31 and reverse-request semantics | Bounded safe rumble/LED, explicit ACK/error/lifecycle cleanup; physically verify motor/LED only with owner-approved reference |
| D-P7 | Bluetooth transport independent of USB | SDP/HIDP, pairing/reconnect/security, input CRC and output headers; redact private device and link identifiers |
| D-P8 | Touch, adaptive triggers and audio integration | Isolate touch desktop hazards, repair/replace damaged reference for trigger experiments; reuse EXP-0023 USB UAC1 as a scope-limited source, not output fidelity |
| D-P9 | Per-revision/long-run host acceptance | Three+ repeated reference/virtual sessions, startup/shutdown, detach/reopen, concurrency and exact cleanup; do not infer hardware parity from one SDL success |

## Integration direction

Curated typed controller state, normalization/codec and identity belong in `gr-controllers`. OS providers realize devices and perform I/O but must not own Sony semantics. Model USB/UHID, USB gadget and Bluetooth as different realization scopes. Do not conflate SDL nominal sensor rates with wire-cadence measurements, or use source acceptance to promote a support matrix. A controlled physical benchmark is required before any `physically_observed` claim.

**Cloud agent (realized-controller research parity)**
