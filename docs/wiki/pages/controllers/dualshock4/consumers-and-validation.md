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

## USB wireless adapter lifecycle (source-only)

The dedicated Sony dongle parser uses report 0x01 status to gate calibration and input. The gamepad, sensor, touchpad, battery and lightbar surfaces are created at receiver probe and retained during ordinary wireless loss. Output uses the existing dongle handle, without a multi-slot selector; delivery while absent is unknown. [`rcv-pattern-ds4-dongle-presence`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/rcv-pattern-ds4-dongle-presence.json), [`rcv-pattern-ds4-node-persistence`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/rcv-pattern-ds4-node-persistence.json), [`rcv-pattern-ds4-output-boundary`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/rcv-pattern-ds4-output-boundary.json). No physical pairing test was performed.

## Bounded virtual USB-bus host observations

In the P5a virtual-host runs, stock playstation bound the USB-bus UHID presentation and an exact-path sweep delivered four face-button transitions and stick endpoints via hidraw. The broad diagnostic failed, the backend classifier did not cover SDL 3.4.20, and Steam did not list the presentation. The uinput comparison delivered the same bounded sweep via event nodes and was listed by Steam, with triggers and a ping pulse/stop reported. The privileged comparison stopped at its first attempted sysfs write. These are virtual observations, not radio, timing or retail fidelity. [`vg-p5a-stock-dualshock4-linux-uhid-usb-bound-ed8065b4be2c`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-p5a-stock-dualshock4-linux-uhid-usb-bound-ed8065b4be2c.json), [`vg-p5a-stock-dualshock4-linux-uinput-bound-ed8065b4be2c`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-p5a-stock-dualshock4-linux-uinput-bound-ed8065b4be2c.json).

## P5a follow-up timing

USB/IP N1/N3 runs verified creation, appearance, direct evdev opening, SDL readiness and removal in all 50/150 slots, with an empty final attach list. This is virtual lifecycle evidence, not retail timing or audio qualification. [`vg-p5a-followup-dualshock4-usbip-timing`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-p5a-followup-dualshock4-usbip-timing.json).

## Alpha 2 polish virtual host experiments

Cleanup 1 stock USB-bus UHID sessions removed their owned HID parents; generic binding failed with ENODEV for specialized-driver models. Cleanup 2 verified three of three stock binds per family, but privilege restrictions blocked the parameter-enabled generic comparison. No host setting was changed. [`vg-alpha2-polish-p5a-usb-binding`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-alpha2-polish-p5a-usb-binding.json), [`vg-alpha2-polish-cleanup2-usb-binding`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-alpha2-polish-cleanup2-usb-binding.json).

Bluetooth-bus UHID cleanup 1 bound two independent sessions, with typed rumble/LED effects isolated to the stimulated device; raw evdev exact controls were 8/8 but SDL evdev 1/8. Cleanup 2 verified all five lifecycle stages in 50/50 and 150/150 slots; sequential SDL HIDAPI exact-with-reset was 4/8 and fallback evdev 1/8. Isolated analog tests attributed all controls correctly, with triggers returning to zero but sticks settling at +128 after excursion. Strict neutral acceptance remains open (experiment status failed). No radio or retail fidelity is inferred. [`vg-alpha2-polish-p5b-dualshock4-bt`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-alpha2-polish-p5b-dualshock4-bt.json), [`vg-alpha2-polish-cleanup2-dualshock4-bluetooth`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-alpha2-polish-cleanup2-dualshock4-bluetooth.json).

The synthetic scale-change experiment matched predictions on USB; Bluetooth caller data was rejected before provider creation. No Bluetooth calibration result was obtained. [`vg-alpha2-polish-p10d-calibration`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-alpha2-polish-p10d-calibration.json).
