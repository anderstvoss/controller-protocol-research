# Xbox 360 — test matrix

[← Xbox 360 overview](index.md)

> **Reviewed corpus:** 2026-11-09. A source parser, compatibility shim or virtual-host acceptance does not establish native physical hardware fidelity.

Run two **independent** test lanes:

**Native wired reference:** obtain a genuine `045e:028e` model and safely record configuration/interface, input `00 14`, every control, LED/rumble request and actual actuation. Verify Linux `xpad` ownership, SDL native parser and restart behavior. Test at least three independent sessions; keep device identifiers private. Claims pending: [`x360-l0-device-physical-wired-usb-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-physical-wired-usb-unknown.json).

**Standard-HID/virtual host:** confirm exact descriptor usages and evdev key-code mapping, SDL backend selection, neutral and individual controls, uinput FF callbacks and optional LEDs; do not report the result as native XUSB acceptance. Reproduce the EXP-0016 explicit-usage correction and document any fixed Eden/Steam build/backend. [`x360-l0-consumer-exp0016-hid-usage-correction`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-exp0016-hid-usage-correction.json), [`x360-l0-consumer-sdl-backend-selection-unmeasured`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-sdl-backend-selection-unmeasured.json).

A third **wireless receiver** lane would need its own `045e:0719`, four-slot handling and distinct output capture; it is neither the wired model nor generic Bluetooth HID: [`x360-l0-device-physical-receiver-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-physical-receiver-unknown.json).

See [F-P1 to F-P8 gates](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/xbox360-l0.md).

## P5a virtual host observations

USB-bus UHID bound hid-generic; the exact-path evdev sweep recorded four face transitions and stick endpoints. Steam listed standard HID and showed sticks/triggers and three face transitions; East was inconclusive, and ping unavailable. The uinput comparator recorded face/stick/trigger controls and ping pulse/stop, though the repeat missed the first nonzero right-trigger step. Neither demonstrates native XUSB or retail fidelity. [`vg-p5a-stock-xbox360-linux-uhid-usb-bound-ed8065b4be2c`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-p5a-stock-xbox360-linux-uhid-usb-bound-ed8065b4be2c.json), [`vg-p5a-stock-xbox360-linux-uinput-bound-ed8065b4be2c`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-p5a-stock-xbox360-linux-uinput-bound-ed8065b4be2c.json).
