# Nintendo Wii Remote, MotionPlus and expansion devices

> **Scope:** reviewed corpus 2026-11-09; source and virtual-host evidence do not establish a retail Wii Remote physical capture.

**Registry:** [Wii Remote](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/wii-remote.json). The registry includes expansions unless a claim restricts scope. Model **core remote**, **extension**, **external MotionPlus** and **integrated Remote Plus revision** as separate dimensions.

## Pages

- [Bluetooth HID reports, memory and base functions](protocol-and-memory.md)
- [Nunchuk, Classic, MotionPlus and accessory hotplug](extensions-and-motionplus.md)
- [Infrared, LEDs, rumble and speaker](io-and-audio.md)
- [Linux, SDL, Dolphin, Cemu and other consumers](consumers.md)
- [Known host failures and validation plan](validation.md)

## Major revision distinction

| Family | Identifiers in pinned consumer/community sources | Do not infer |
| --- | --- | --- |
| Original RVL-CNT-01 | Bluetooth-facing Nintendo `057e:0306` | Physical presence of an integrated MotionPlus |
| Early integrated Plus, non-TR | Can use the same `RVL-CNT-01` / `0306` identifiers | Identity alone does **not** distinguish it from original; built-in calibration unknown |
| Later Remote Plus RVL-CNT-01-TR | Often `057e:0330`, `RVL-CNT-01-TR` | Its built-in gyro behavior is not just an attached external module with identical register truth |

Corpus [`wii-original-remote-consumer-revision`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-original-remote-consumer-revision.json), [`wii-early-plus-revision-gap`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-early-plus-revision-gap.json), [`wii-tr-consumer-revision`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-tr-consumer-revision.json); detailed [revision decision brief](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-remote-plus.md).

## Current evidence boundary

The core research includes source inspections of Linux `hid-wiimote`, SDL Wii HIDAPI, Dolphin, Cemu, wiiuse and xwiimote; it also includes **virtual-host** runs with specific passed and blocked consumer paths. These do not prove physical protocol equivalence or genuine Bluetooth advertising/pairing. Report such acceptance narrowly.

The most consequential design requirement is **stateful accessory handling**. A fixed controller-as-subset permutation loses hotplug, extension identities, calibration and post-MotionPlus register remapping. The compatibility path can still create an initial extension set while preserving runtime attachment state. See [`wii-kernel-extension-init`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-kernel-extension-init.json) and [`wii-kernel-motionplus-pass-through`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-kernel-motionplus-pass-through.json).

**Research:** [consolidated Wii ledger](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/wii-remote-l0.md), [integrated Plus decision](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-remote-plus.md).
