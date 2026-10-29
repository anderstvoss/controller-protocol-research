# W9e generic-binding retry

This follows virtualgamepad #158 comment 6454022725 and research #55. The
initial explicit per-device bind refusal remains an unchanged historical
preflight result. The retry used merged code main
`c60c16409e91e39ddba56a78475bdabe3780d1d0`, both creation shims on, and the same
synthetic caller EEPROM, MotionPlus and Nunchuk calibration blocks as W9.

Anders alone checked that `ignore_special_drivers` was 0, confirmed no other
HID hotplug, set it to 1, and signaled a waiting non-root harness to create two
dedicated virtual devices. His script immediately restored and read back 0;
the measured window was 2.035782 seconds. Exact-device hidraw grants followed
restoration. The agent rechecked each identity, UHID/raw link and generic
driver binding. No agent sudo, persistent policy, module change or creation
option was involved. The value is privileged: restoration evidence is the
owner's readback and result record, not an agent privileged parameter read.

| Arm | Observed result | First unpassed checkpoint |
| --- | --- | --- |
| Native Dolphin 2503 MP+Nunchuk, 180 seconds | Mode 05; exact MP 0020/0030 and child 0040 calibration chunks; no post-map native or combined A400F0=55 | Changing decoded Nunchuk and gyro in the mapping view |
| Native Dolphin 2503 MP-only, 150 seconds | Exact MP chunks and a changing mapped gyro indicator with auto-calibration period 0; no post-map native or combined A400F0=55 | None through this bounded MP-only control |
| Exact-device kernel/xwiimote trade-off | Zero input companions and libxwiimote iface creation -19 (ENODEV), before and after both arms | Expected loss of kernel Wii input access confirmed |

The MP+Nunchuk path **did not request F6**. Successful later calibration reads
do not establish a live F6 shim pass. The A400FE/512 error 7 is the previously
source-pinned usability diagnostic, not a calibration failure. All three
calibration chunks match the imported synthetic blocks exactly. Only 28
report 0x37 frames with two distinct payloads were observed in this arm;
late sampled mapping views showed static Nunchuk controls and gyro. This is
not a universal zero-gyro or physical-incompatibility finding. The remaining
cause is not attributed from these observations, and no model fix follows.

The MP-only control observed 14002 report 0x37 frames. Its decoded gyro claim
comes from separate mapping-view samples showing different indicator positions,
not that raw count. No calibrated-rate, continuous-delivery or all-controls
qualification is inferred. Both consumers used isolated profiles with explicit
bindings, emulated mapping only, no Real Wii Remote slot or game content,
and the prior exact-owned raw/radio observation guard. The hook is an
observation aid, not a complete sandbox.

Both generic bindings persisted after the global parameter returned to 0.
Absence of input companions means no MotionPlus event node existed for evtest;
the exact-root xwiimote probe returned ENODEV. No unrelated event node was
opened. This is the observed cost of generic binding, not an API fallback.

Both consumers exited with exact-profile cleanup checked. Both devices were
closed idempotently; HID and hidraw nodes were removed. No LED nodes had been
created under this generic descriptor. The optional shim-off run was omitted
because the MP+Nunchuk arm did not pass. No adoption PR is warranted, and no
binding-mode option or model/codec/descriptor/API change was made. Test/dev
observations do not clear the release gate in virtualgamepad #258. Only reduced
results and hashes are published; raw bytes, screenshots and scripts remain
private. No physical, radio, rate, game or challenge claim follows.
