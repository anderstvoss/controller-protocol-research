# Wii Remote — Linux, SDL, Dolphin, Cemu and others

[← Wii overview](index.md) · [MotionPlus](extensions-and-motionplus.md)

> **Scope:** reviewed corpus 2026-11-09; source and virtual-host evidence do not establish a retail Wii Remote physical capture.

## Access path determines what the program can see

| Consumer | Typical selected path in pinned source | Common trap |
| --- | --- | --- |
| Linux `hid-wiimote` | Bluetooth-marked HID, kernel child evdev nodes for base/IR/extension/MP | Merely advertising MP node does not mean gyro is active |
| SDL Wii HIDAPI | Raw hidraw consumer, with its own extension-mode cache and report handling | Linux SDL may defer MP activation to kernel; cached mode can remain zero |
| xwiimote / xwiishow | Parent HID/driver and separate kernel evdev nodes | Plain uinput node naming does not create the needed HID parent |
| Dolphin | HIDAPI raw controller (scanner and ControllerInterface) or separate real Wiimote emulation path | Detect/connect ≠ completed calibration and gyro updates |
| Cemu | Own HIDAPI/optional L2CAP consumer | Native device detection ≠ proved IMU decode path |
| RetroArch | udev/evdev gamepad, sometimes sibling sensors | Generic mapped controls are not Wii-native accessory state |
| wiiuse / CWiid | BlueZ L2CAP directly | **No connection** to UHID `BUS_BLUETOOTH` alone |

This distinction is supported by [ranked consumer survey](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-consumer-survey.md) and [`wii-gap-consumer-xwiimote-driver-evdev-interface`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-gap-consumer-xwiimote-driver-evdev-interface.json).

## SDL's zero-gyro failure mode

Wii MP can be detected by kernel while SDL delivers zero motion because the kernel enables MP **on opening the MP event device**, while SDL's Linux path may skip independent mapping and keep `m_ucMotionPlusMode=0`. Holding the MP evdev FD open *before* starting SDL is a discriminating source-guided test, not an established general remedy. [SDL mode-cache investigation](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-gyro-investigation.md), [`wii-kernel-motionplus-pass-through`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-kernel-motionplus-pass-through.json).

## Dolphin startup is a dependency chain

Dolphin's ControllerInterface serializes status, LEDs/report mode, EEPROM accel read, IR/speaker setup, extension identity, MotionPlus mode and calibration. Missing ACK or calibration can stop progress before gyro data is ever consumed. For pass-through Nunchuk/Classic, Dolphin conditionally reads downstream identity at `A400F6` and calibration at `A40040`. These are essential consumer gates, even where exact retail register behavior remains uncertain: [`wii-gap-dolphin-attach-controller-task-order-and-failure`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-gap-dolphin-attach-controller-task-order-and-failure.json), [complete step trace](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-dolphin-attachment-technical.md).

## Kernel ownership and timing

Multiple readers can cause HID feature/register state competition. A change in Dolphin's reported gyro behavior while kernel evdev nodes are open does **not** demonstrate a codec failure until outgoing writes and report-mode transitions are attributed to the correct consumer. Compare bound/unbound experiments and user permission/driver state before proposing a Bluetooth stack rewrite.

## Recognition is not acceptance

For each consumer report: device discovery, successful open, calibration complete, current report mode, known native state, changing mapped gyro, multiple controlled controls, output ACK and cleanup. The historical research contains both passing and blocked **virtual-host** runs; never collapse them into "Wii Remote works". [W-series outcomes](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/wii-remote-l0.md).
