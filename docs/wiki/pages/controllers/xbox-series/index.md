# Microsoft Xbox Series controller

> **Reviewed corpus:** 2026-11-09. A source parser, compatibility shim or virtual-host acceptance does not establish native physical hardware fidelity.

**Registry:** [Xbox Series](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/xbox-series.json), distinct from [Xbox 360 standard HID](../xbox360/index.md). The USB transport uses **GIP/vendor-style** semantics in relevant consumers, while Bluetooth uses a **separate HID report family**.

## Pages

- [USB GIP, Bluetooth HID, evdev and motor output](protocol-and-consumers.md)
- [Native wired GIP, xone, receiver and headset](wired-gip-and-receiver.md) — new source-only consumer survey.
- [Bluetooth HID, xpadneo, Guide/Share, output and UHID](bluetooth-and-xpadneo.md) — original consumer-source survey.
- [Scoped physical USB/Bluetooth and scratch-UHID observations](physical-observations.md) — newer, distinct evidence levels.

## Supported consumer facts

Pinned Linux `xpad` and SDL sources identify controller variants, Share button and separate input axis domains. The kernel can expose signed sticks, trigger axes and hat/buttons to evdev, but this mapping is **not proof of the physical raw USB/Bluetooth report**. SDL's GIP and Bluetooth rumble paths differ. See [`xbox-series-xpad-identity-share`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-xpad-identity-share.json), [`xbox-series-xpad-axis-domains`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-xpad-axis-domains.json), [`xbox-series-sdl-gip-rumble`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-sdl-gip-rumble.json), [`xbox-series-sdl-bluetooth-report-roles`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-sdl-bluetooth-report-roles.json).

The corpus includes one published **evdev observation artifact** with 26 controls and 14 frames; this is an observed post-driver surface rather than native GIP or Bluetooth traffic. Source: [`xbox-series-published-evdev-shape`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-published-evdev-shape.json). Physical raw protocol and trigger-rumble coverage remain qualified as unknown: [`xbox-series-usb-device-gaps`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-usb-device-gaps.json), [`xbox-series-bluetooth-device-gaps`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-bluetooth-device-gaps.json).

**Research:** [Series L0 evidence ledger](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/xbox-series-l0.md).

## November 10 consumer-source update

New pinned research separates **stock xpad evdev**, **xone wired/receiver GIP**, **kernel Bluetooth HID**, **xpadneo** and **SDL HIDAPI** as different consumers. xpadneo normally presents Share as a separate keyboard **F12** event rather than xpad's gamepad Record button; it may produce several input nodes. xone can register headset ALSA playback/capture where stock xpad disables the corresponding GIP audio interface. These original **source inspections** alone did not prove retail packet or sound fidelity; the November 11 physical headset session adds bounded output evidence. See [Bluetooth details](bluetooth-and-xpadneo.md), [wired/receiver details](wired-gip-and-receiver.md), [`xbox-cgap-xpadneo-share-f12`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/xbox-cgap-xpadneo-share-f12.json) and [`xbox-xone-gip-headset`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/xbox-xone-gip-headset.json).

## November 11 physical and virtual reference

One wired physical `045e:0b12` unit **validated the post-driver xpad input/reconnect shape**, with an observed minor axis-fuzz difference from C9 uinput; main rumble was felt. Loading xone's headset modules and reconnecting subsequently enabled bounded physical playback/mic capture. A physical `045e:0b13` Bluetooth session captured a **283-byte HID report descriptor** exactly matching the pinned example. Separately, a scratch Bluetooth-bus UHID passed a kernel `microsoft`/SDL evdev run and a later xpadneo session exercised a physical BT gamepad. These are separate consumer/device claims, **not** universal raw GIP or four-motor fidelity. See [physical and virtual observations](physical-observations.md), [`xsphys-xpad-input`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/xsphys-xpad-input.json) and [`xsphys-bt-descriptor-match`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/xsphys-bt-descriptor-match.json).
