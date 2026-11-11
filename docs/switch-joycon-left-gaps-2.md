# Switch 1 Joy-Con (L) — controller gaps 2, source-only

For virtualgamepad [#297](https://github.com/anderstvoss/virtualgamepad/issues/297). **No host, physical Joy-Con, USB receiver, Bluetooth pairing, or virtual controller test was run.** This brief narrows left-half behavior without revising the shared `joycon-*` / `swpro-*` record set. Each source below is an existing immutable-pin, SHA-256-verified corpus source record.

## Ranked implementation decisions

| Priority | Source finding / impact on virtualgamepad | Playable / faithful | Evidence ceiling | New claim and existing foundation |
| --- | --- | --- | --- | --- |
| P0 | Keep each Joy-Con (L) a `BUS_BLUETOOTH` `057e:2006` HID unit with device-info type `0x01`. Do not manufacture a wire-level `057e:2008` pair. | Faithful identity requirement; also enables compatible consumer detection | Source-only; descriptor and retail name not captured | `joycon-cgap-left-identity`; `joycon-hid-nintendo-bus-binding`, `joycon-a-device-info-type`, `joycon-sdl-hidapi-pair-combination` |
| P0 | Emit left-side D-pad, rail, L/ZL and shared Minus/stick-click/Capture bits at their left-specific positions in full report `0x30`. | Playable controls and faithful packet shape | Source-supported parser expectations, not retail capture | `joycon-cgap-left-wire-fields`; `joycon-a-full-report-per-side` |
| P0 | Validate Linux `hid-nintendo` left-key mapping, including SL/SR outside Charging Grip. D-pad is four buttons rather than Pro-style hat axes. | Playable Linux evdev | Source-only consumer | `joycon-cgap-left-kernel-buttons`; `joycon-a-home-led-and-rail-buttons` |
| P0 | Pack left stick into three bytes, use independent left calibration and confirm Linux `ABS_X`/`ABS_Y` with inverted vertical sign. Never infer unused right-stick bytes. | Playable and source-faithful scaling | Source-only consumer/device; inactive side unknown | `joycon-cgap-left-kernel-stick`; `joycon-a-calibration-per-side` |
| P1 | Preserve left IMU raw-channel convention: `hid-nintendo` calibrates then leaves the left axes' signs unchanged, while it negates right Y/Z. | Faithful consumer parity | Source-only consumer; not physical orientation | `joycon-cgap-left-kernel-imu`; `joycon-a-right-imu-signs` |
| P1 | Test SDL3's standalone sideways mini-pad versus vertical/parented map separately. SDL rotates presentation; the HID report layout does **not** change. | Playable SDL mapping, faithful raw identity | Source-only SDL3; no runtime acceptance | `joycon-cgap-left-sdl3-modes`; `joycon-sdl-hidapi-pair-combination` |

## Source-backed left-half details

### Identity and raw left control fields

Linux's pinned `hid-nintendo` device table matches `057e:2006` on Bluetooth, and its left controller-type is `0x01` from device-info subcommand `0x02` (kernel lines 315–324, 708–716, 2495–2551, 2883–2900). SDL3 provides the normalized display name `Nintendo Switch Joy-Con (L)` and left gamepad type; this does not establish the retail on-air HID string (SDL lines 1369–1373, 1416–1428). The physical two-half pair remains two devices; SDL's `057e:2008` is a consumer-created aggregate.

For standard input report `0x30`, kernel's 24-bit button field begins at absolute byte 3. In the **shared byte 4**, bit 0 means Minus (field bit 8), bit 3 left-stick click (bit 11), and bit 5 Capture (bit 13). In **left byte 5**, bits 0–7 mean Down, Up, Right, Left, SR, SL, L and ZL, respectively (field bits 16–23). Kernel constants and mappings are at lines 341–394. The input left-stick field is bytes 6–8; the right-stick field is bytes 9–11 in the family layout (`joycon-a-full-report-per-side`). This is source-described protocol layout, not measured retail bytes; nothing establishes the inactive right-stick encoding.

### Linux input and stick normalization

For left type, `hid-nintendo` configures main `ABS_X` and `ABS_Y`, `BTN_TL` (L), `BTN_TL2` (ZL), `BTN_SELECT` (Minus), `BTN_THUMBL`, D-pad `BTN_DPAD_*`, and `BTN_Z` (Capture). Outside the Charging Grip it additionally maps SL to `BTN_TR` and SR to `BTN_TR2`; within the grip it excludes those additional keys (kernel lines 370–394, 1756–1765, 2189–2211). This is a host mapping, not an assertion of rail-state packet bytes.

Kernel extracts two 12-bit left-stick axes from the packed three-byte field, applies its left-side calibration, sends X to `ABS_X`, and negates normalized Y into `ABS_Y` (lines 1100–1145, 1676–1692). The existing `joycon-a-calibration-per-side` describes the left factory region `0x603d` and the left user calibration region; those locations are not new claims.

### IMU and SDL interpretation

For each full input IMU packet, the kernel parses three samples and scales raw gyro/accel channels using its calibration. It applies an additional Y/Z sign inversion **only for right-capable Joy-Con types**, not for Joy-Con (L); the left output is sent as accelerometer `ABS_X/Y/Z`, gyroscope `ABS_RX/RY/RZ` on a separate IMU event node (kernel lines 1397–1415, 1525–1611, 2115–2175). This is kernel consumer behavior, not physical proof of the left board's sensor orientation.

At pinned SDL3, unparented Joy-Con (L) defaults to sideways mini-gamepad mode unless the vertical Joy-Con hint is enabled. Mini-mode maps the left D-pad to face buttons and rotates the stick presentation (left X from negated raw calibrated Y, left Y from negated raw calibrated X); the parented/vertical path instead presents a D-pad hat and conventional left X/Y mapping. SDL also has a mini-mode-specific sensor-axis rotation for left and exposes left-specific gyro/accel channels when parented (SDL lines 2260–2303, 2306–2349, 2384–2414, 2448–2460, 2590–2604). No switch in the physical report format is implied by SDL orientation.

### Reused pinned evidence

- `joycon-linux-hid-nintendo`: [Linux `hid-nintendo.c`, pinned 4056b3c](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-nintendo.c), kernel GPL-2.0-only (SPDX in file); see line locators above. Restated, no excerpts.
- `joycon-linux-hid-ids`: [Linux HID IDs, same pin](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-ids.h), Linux GPL-2.0-only.
- `joycon-sdl-switch`: [SDL3 Switch HIDAPI, pinned 535d80b](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_switch.c), Zlib licence.
- `joycon-sdl-hidapijoystick`: [SDL3 combination logic, same pin](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapijoystick.c), Zlib licence.
- `swpro-dekunukem-bluetooth-hid-notes`: [community input report notes, pinned b354f21](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/b354f21ae81f7b0d1d060b2b61e66ad0d9bc1756/bluetooth_hid_notes.md); use existing research-lead provenance. Not an independently measured left-half capture in this lane.

These are existing source records with already pinned file hashes. This lane adds no duplicate source records and makes no changes to existing claims.

## Proposed acceptance probes — not run

1. Instantiate only left-side Bluetooth-bus UHID `057e:2006` and device-info type `0x01`. Record bind/probe, ACKs, left main node, separate motion node and player LEDs; no combined `057e:2008` raw device.
2. At a deterministic packet/driver parser seam, toggle one field bit at a time: Minus, Capture, click, four D-pad directions, L/ZL, SL/SR. Confirm evdev mapping, including Charging Grip conditional exclusion only in its separately scoped topology.
3. Inject calibrated left-stick extrema/center, verify `ABS_X/Y` scaling and negative Y, and confirm that arbitrary opposite-stick bytes are not used for left output. Do **not** claim their retail defaults.
4. Inject three asymmetric IMU vector samples and verify left no-additional-sign-inversion versus the already documented right sign rule; verify independent sensor timestamps and axes.
5. Test SDL3 HIDAPI with standalone mini, vertical hint, parented pair, direct HIDAPI versus evdev, and removal. Verify the mini-mode input/sensor rotation is application interpretation. Capture only sanitized non-identifying results.
6. Physical descriptor/name, retail inactive-stick values, cadence, and actuator response stay on the existing owner hardware research path, not inferred here.

**Evidence ceiling:** All six new claims are source-supported at pinned revisions. No physical/host run or vendor firmware analysis. No source for the exact retail Bluetooth descriptor or runtime behavior was added.
