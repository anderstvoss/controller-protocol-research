# DualSense L0 protocol and consumer evidence ledger (Package D)

## Scope and provenance

This is a **source-backed L0 ledger**, not a physical device certification or proof that a virtual HID topology is interchangeable with a genuine controller. All source-read claims are `source_only` regardless of `device`/ `consumer` role. Explicit missing physical USB/BT measurements use the relevant transport. All 39 new `ds-l0-*` claims and the separate `dsedge-l0-consumer-identity-separation` claim set explicit `evidence_role`.

The original D baseline was research `main` `c92438d36242fb73c6524a88890f1446aabf42ea` after B #58. A two-parent merge commit `0fc7df0d96d73c9bd8e00b371fd30e3ed352c579` brought in `main` `b5588a19bf72f489c2cf00a15222c3c856baecce` **after merged Switch Pro C #60**, without rebasing or replacing D history. The source evidence is controller-specific; Switch Pro `swpro-*` claims are not imported as DualSense evidence. All evidence is pinned to existing and newly published source records; no copied vendor firmware, new raw private captures or unpinned experimental branch citations.

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

## Independent community research leads added in this revision

The requested PS developer wiki was **not used**: the independently pinned open alternatives are more reproducibly reviewable, and their original bytes and section locators were fetched successfully. None should be promoted to `physically_validated` on this basis. All six files are individually `kind: research_lead`, SHA-256 hashed, and cited via distinct source records:

| Source record | Revision and locator | Evidence boundary |
| --- | --- | --- |
| `ds-community-nondebug-input-notes` | nondebug/dualsense `02338358`, README 99–148 | Community USB 0x01 basic input buttons and axes |
| `ds-community-nondebug-usb-descriptor` | same commit, `report-descriptor-usb.txt` | Model-specific USB descriptor listing input 0x01/output 0x02/feature 0x05 |
| `ds-community-nondebug-explorer` | same commit, `dualsense-explorer.html`, report parser and effect controls | WebHID physical-device exploration tool, not a corpus capture |
| `ds-community-viiper-protocol` | DualSenseClient/VIIPER `a3709034`, `docs/devices/dualsense.md` 83–102, 153–184, 259–280 | Emulated compatible report/feature schema; *not retail firmware* |
| `ds-community-trigger-notes` | iamdevmarcos/dualsense-controller `455feab5`, `controller/TRIGGER-NOTICES.md` 1–9 | Mode semantics and origin pointers |
| `ds-community-trigger-encoding` | same commit, `controller/adaptive-triggers.js` 72–105 | Independent community encoder with explicit per-mode parameters, not motor-response validation |

These three lineages are independent of HHD. Community notes, HID descriptors, host code, and emulators have different evidentiary strengths. In particular, VIIPER's documentation describes a compatible *implementation*, while nondebug's WebHID explorer documents observations and encoding choices. A sample packet or identifier in an external source does not become a physical observation in this corpus.

## New device-side format detail

| Required area | Source-derived layout / formula | Claim |
| --- | --- | --- |
| USB input `0x01` | 64 bytes including report ID: stick LX/LY/RX/RY at 1–4; L2/R2 analog at 5–6, sequence at 7, buttons/hat following; gyro and accel in signed little-endian 16-bit fields, sensor timestamp, two four-byte touch contacts, battery/charge | `ds-l0-device-usb01-full-fields` |
| Touch contacts / dimensions | Each contact has 7-bit contact ID and high-bit inactive flag; X/Y packed to 12 bits. Linux's coordinate convention is 1920 × 1080; SDL's `Y/1070` normalization is a *consumer policy*, not a different physical sensor size | `ds-l0-device-touchpad-format-dimensions` |
| USB output `0x02` | 47-byte common output; valid flag0/flag1 gate motors, audio speaker/mic volumes, audio routing, mute LED, lightbar/player LEDs, while later flag bits include lightbar setup and improved compatible rumble; independent 11-byte right/left trigger blocks | `ds-l0-device-usb02-valid-flags` |
| Trigger mode and params | Each 11-byte block starts with mode: Off `05`, Feedback `21`, Weapon `25`, Vibration `26`; Weapon = two-zone LE16 mask + strength-minus-one, Feedback/Vibration = active zone mask + packed 3-bit forces, Vibration also frequency at effect byte 9 | `ds-l0-device-adaptive-trigger-mode-block`, `ds-l0-device-adaptive-trigger-mode-parameters` |
| Feature `0x05` | 41-byte calibration response: LE16 gyro biases/plus-minus/speed and accel plus-minus, from which host calibration coefficients are derived | `ds-l0-device-feature05-shape` |
| Feature `0x09` | 20-byte pairing/device MAC identity report; public corpus carries structure only, never a real MAC or pairing key | `ds-l0-device-feature09-identity-shape` |
| Feature `0x20` | 64-byte firmware/version response with hardware/firmware fields and feature-version bytes 44–45; different consumers gate their rumble policy on these fields | `ds-l0-device-feature20-firmware-shape` |
| IMU normalization | Raw signed 16-bit per axis; kernel sensor correction uses `(raw−bias) * sensitivity_numer/sensitivity_denom`, with coefficients from feature `0x05`. VIIPER's 16.384 gyro counts/deg/s and 8192 accel counts/g represent its own *synthesis scale*, not established physical resolution | `ds-l0-device-imu-scaling-formulas` |

The device-side modes are not conflated with consumer actions. Exact operating strength, firmware acceptance for every documented mode, audio-haptics waveform, sensor accuracy and trigger physics remain subject to D-P1–D-P8.

## What this settles for virtualgamepad (part 2 / decision table I)

| Question | Finding from pinned sources | Claim ID or evidence status |
| --- | --- | --- |
| Feature `0x20`, bytes 44–45 = `0x0224` | **Material.** SDL at `535d80b` reads LE16 version and switches rumble output at `>= 0x0224`; SDL `829a65d` precomputes enhanced rumble using the same cutoff, with Edge/unknown-version exceptions. Linux uses a distinct feature-version threshold `2.21` for base, Edge always v2. Synthetic `0x0224` selects the newer SDL path; it is **not** proven authentic or mandatory firmware | `ds-l0-consumer-firmware0224-branch` |
| Synthetic feature `0x05` | **Important.** Linux fails probe when feature GET fails and substitutes per-axis gyro/accel correction values only for invalid *zero sensitivity denominators*. SDL tolerates short/failed calibration by ignoring hardware correction; no source-backed requirement for an exact synthetic calibration payload besides valid parseable scale | `ds-l0-consumer-kernel-calibration-fallback`, `ds-l0-consumer-probe-feature-failure-tolerance`, `ds-l0-sdl-calibration-fallback` |
| Feature `0x03` copied from OpenPuck | SDL's 48-byte/marker `0x28` feature `0x03` gate applies to *third-party* PlayStation detection; Sony VID path assumes capabilities. **No evidence** that `054c:0ce6` needs OpenPuck's synthetic `0x03` reply, or that its exact bytes are a device-fidelity requirement | `ds-l0-consumer-feature03-capabilities` |
| L2/R2 digital threshold | SDL has a zero-analog + digital-bit fallback (forces maximum); Linux separately exposes digital buttons. **No evidence** of a fixed physical analog-to-digital trigger threshold in these sources | `ds-l0-consumer-l2r2-digital-analog-policy` |
| UHID missing Steam gyro vs `dummy_hcd` | Historical virtual-host contrast is source-supported; association between `BUS_VIRTUAL`/UHID and SDL/Steam motion node is an **inference**, not established cause | `ds-l0-dummy-hcd-steam-gyro-contrast`, `ds-l0-uhid-gyro-association-hypothesis` |
| Edge PID/registry | Separate `054c:0df2` and extra Edge controls in Linux/SDL; **do not fold into base DualSense** | `dsedge-l0-consumer-identity-separation` |

Linux hid-playstation source spans for firmware/probe/fallback: **1023–1147, 1150–1204, 1783–1835**. SDL 535d80b spans: **297–320, 418–457, 555–666, 683–700, 1188–1199**. SDL 829a65d spans: **434–447, 719–734, 1242–1251**. These exact source pins and their case-specific scopes are in each claim's `applicability.scope`.

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
