# Wii Remote — remaining tests and implementation boundary

[← Wii overview](index.md)

> **Scope:** reviewed corpus 2026-11-09; source and virtual-host evidence do not establish a retail Wii Remote physical capture.

## Minimum reproducible comparisons

1. **Native codec:** neutral and isolated remote A/B/D-pad, acceleration, IR and Nunchuk/Classic samples; exact IDs/lengths and ACK/feature errors.
2. **Memory/configuration:** EEPROM `0x0016`, extension IDs `A400FA`, MotionPlus activation `A600FE`, downstream `A400F6` and calibration `A40020/40`; never invent absent factory bytes.
3. **Kernel/SDL gyro:** hold or release kernel MotionPlus evdev FD, vary SDL version/order, log mode and actual calibrated gyro; test OS driver binding independently.
4. **Dolphin:** distinguish scanner found, HID opened, status ACK, calibration loaded, MP mode mapped, first changing gyro and downstream accessory state.
5. **Real Bluetooth:** only a proper L2CAP/radio realization can demonstrate discoverability, pairing, connection/security and reconnect.
6. **Physical revision:** original vs early integrated Plus vs TR; per-revision identity, calibration, hotplug/status edges, speaker and IR behavior.
7. **Teardown:** stop speaker/rumble, neutralize input, cancel retries and release all child nodes under competing readers.

## Important unresolved issues

- Integrating MotionPlus physically and exposing a `TR` name do not prove exact integrated register defaults ([`wii-early-plus-revision-gap`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-early-plus-revision-gap.json)).
- A plausible MemoryPlus challenge/register representation is **not** proof of a genuine encrypted protocol implementation ([`wii-extension-encryption-gap`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-extension-encryption-gap.json)).
- Source-accommodating `A400F6/A40040` logic needs separate real hardware confirmation ([`wii-gap-dolphin-attach-passthrough-four-byte-id-f6`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-gap-dolphin-attach-passthrough-four-byte-id-f6.json)).
- No user-facing gyro should be labeled calibrated without a measured sensor reference and a verified decoded consumer path.

**Original lab records:** [W5 gyro diagnosis](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-w5-gyro-diagnosis.md), [fresh Plus follow-up](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-w9i-fresh-plus.md), [status edges and choices](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-motionplus-activation-status.md).
