# DualShock 4 — touch history, host decoding and acceptance

[← DS4 overview](index.md)

> **Evidence snapshot:** corpus `ab74f662…` (2026-11-09); source-only versus physical and device versus consumer evidence are kept distinct.

## Touch history is not multi-touch finger count

In the source-described packets, USB reserves **three nine-byte history samples** and Bluetooth reserves **four**. Each sample has timestamp plus **two four-byte contact slots**. Calling these "three/four touch points" confuses history depth with simultaneous contacts. The corpus preserves this **conflict in terminology** rather than inventing hardware evidence: [`ds4-l0-device-touch-count-conflict`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-touch-count-conflict.json) versus [`ds4-l0-consumer-kernel-touch-report-buffer-count`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-consumer-kernel-touch-report-buffer-count.json).

The source-described touch coordinate convention is 1920×942 and motion uses signed little-endian channels plus calibration. The physical sensor accuracy/revision map remains unmeasured: [`ds4-l0-device-imu-and-touch-units`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-imu-and-touch-units.json).

## Kernel, SDL and historical differences

Modern Linux `hid-playstation`, historical `hid-sony` and SDL PS4 HIDAPI have different probe and calibration-fallback rules. A simulated device that works on one may fail another. The dedicated wireless adapter `0ba0` has its own hotplug/connection/calibration handling and is **not** an alias for direct wired USB: [`ds4-l0-consumer-revision-and-dongle-routing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-consumer-revision-and-dongle-routing.json), [`ds4-l0-device-wireless-adapter-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-wireless-adapter-unknown.json).

In virtual-controller experiments, a combined touchscreen/gamepad node was classified unexpectedly by some host paths; split topology and SDL backend selection require separate verification. This is **host evidence** only. [historical virtualhost evidence](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/virtualgamepad-alpha1-backfill.md).

## Suggested bench plan

Run two physical DS4 revisions if available, USB and BT separately; record descriptor/firmware feature inventory, simple→enhanced transition, neutral and isolated buttons/axes, two simultaneous touch contacts with history and releases, bounded rumble/lightbar, reconnect and repeated open/close. Compare kernel-bound and unbound/generic-driver SDL paths on fixed versions. Preserve feature error behavior and **no identifiers** in public fixtures.

See [E-P1 through E-P8 gates](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/dualshock4-l0.md) and [ownership and contention](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/sony-consumer-contention.md).
