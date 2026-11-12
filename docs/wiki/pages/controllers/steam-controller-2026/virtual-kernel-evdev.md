# Steam Controller 2026 — virtual Linux kernel/evdev experiment

[← Steam Controller overview](index.md) · [Kernel and SDL ownership](modes-and-consumers.md) · [Validation](validation.md)

> **New 2026-11-11 experiment, corpus e8cca52c51f7.** These are **virtual host-consumer observations** from virtualgamepad #304/D9 on Linux 7.3. They do **not** demonstrate a retail controller's output, firmware defaults, physical motion accuracy or Steam Input acceptance. The corresponding claim statuses are `source_supported` and their role is `consumer`; do not silently promote them.

## Native-mode gate and ownership

With a new wired `28de:1302` UHID controller, `hid-steam` initially registered gamepad and sensor evdev nodes with readable capabilities, **but no events were emitted**. In this session a **650 ms Menu press/release** changed the kernel mode and events flowed; this is compatible with the driver source's nominal 450-ms long-hold gate, not a measurement of a universal 450-ms firmware timer. Holding the layered hidraw node caused the kernel-native gamepad and sensor nodes to be removed. Device enumeration alone therefore does not prove functional event routing. [`steam-d9-virtual-kernel-mode-gate`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/steam-d9-virtual-kernel-mode-gate.json).

## Report decoding observed through the virtual host

The mode-enabled kernel path decoded **22 native digital controls** into press/release key events. This includes A/B/X/Y, Menu/View/Steam/QAM, shoulders, trigger clicks, D-pad, sticks and rear grip controls. Left/right pad presses produced independent key codes even without reported touch. Normalized sticks use `ABS_X/Y` and `ABS_RX/RY` (vertical polarity inverted); left/right analog triggers map to `ABS_HAT2Y` (code 21) and `ABS_HAT2X` (20) respectively. The source claim lists every input code and the isolated-control correspondence. [`steam-d9-virtual-kernel-evdev-decoding`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/steam-d9-virtual-kernel-evdev-decoding.json).

**Not fully reproduced at evdev:** untouched pad positions were not emitted; no independent pressure, contact, stick-touch or grip-touch event surfaced. On UHID only, a separate input sensor node translated three-axis accelerometer and gyroscope samples, with `MSC_TIMESTAMP` per sample. The reduced `uinput` realization did not provide a sensor node. A negative trigger test exposed a distinction between raw UHID passthrough and uinput clamping; the follow-up virtualgamepad implementation rejects negative trigger inputs. [`steam-d9-virtual-kernel-evdev-decoding`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/steam-d9-virtual-kernel-evdev-decoding.json).

## Capability attributes and realization tradeoffs

The experiment queried `EVIOCGABS` across the gamepad and sensor. The virtual UHID node's min/max, fuzz, flat and resolution values matched the pinned kernel IBEX claims: sticks ±32767 with resolution 6553; pads ±32767 with fuzz 256 and resolution 1638; triggers 0–32767; sensors have their own accelerometer/gyro ranges and `INPUT_PROP_ACCELEROMETER`. Reduced uinput matched gamepad ranges/flat values but reported zero fuzz/resolution and no sensor node. These are *post-driver* attributes, not raw HID report resolutions. [`steam-d9-virtual-kernel-abs-ioctl`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/steam-d9-virtual-kernel-abs-ioctl.json).

## What this closes, and what it does not

- **Supported:** a bounded virtual wired UHID mode-gated host-decoding session, with sensor-node and input capability observations; a reduced uinput comparison.
- **Not supported:** retail USB packet fidelity, physically measured sensor/trigger transfer functions, exclusive Steam client ownership behavior, or direct BLE/Puck equivalence.
- **Regression gate:** create a fresh node, record driver and evdev capabilities, perform and log the mode transition, verify isolated controls and release, then close the raw client and remove all owned nodes.

The original run is in [`steam-d9-virtual-kernel-evdev`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/experiment/steam-d9-virtual-kernel-evdev.json); see [migration ledger](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/docs/ledgers/steam-controller-migration.md) for the broader realization context.
