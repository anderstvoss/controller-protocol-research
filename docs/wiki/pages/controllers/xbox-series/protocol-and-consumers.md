# Xbox Series — USB, Bluetooth and host contracts

[← Xbox Series](index.md)

> **Reviewed corpus:** 2026-11-09. A source parser, compatibility shim or virtual-host acceptance does not establish native physical hardware fidelity.

## Transport separation

| Aspect | USB / GIP-consumer path | Bluetooth HID-consumer path |
| --- | --- | --- |
| Framing | Vendor/GIP-specific host commands and packets | HID report IDs/roles interpreted by separate SDL decoder |
| Input | Linux xpad maps buttons, Share, sticks, triggers and D-pad to evdev | SDL translates controller HID input reports into common gamepad semantics |
| Output | SDL GIP rumble path has own message envelope | SDL Bluetooth rumble path uses Bluetooth-specific output |
| Evidence | [`xbox-series-sdl-gip-rumble`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-sdl-gip-rumble.json), [`xbox-series-xpad-identity-share`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-xpad-identity-share.json) | [`xbox-series-sdl-bluetooth-report-roles`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-sdl-bluetooth-report-roles.json), [`xbox-series-sdl-bluetooth-rumble`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-sdl-bluetooth-rumble.json) |

The physical packet/feature matrix across firmware and variants is **not** established by these sources: [`xbox-series-usb-device-gaps`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-usb-device-gaps.json), [`xbox-series-bluetooth-device-gaps`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-bluetooth-device-gaps.json).

## Triggers and force feedback

The Linux `xpad` source maps 10-bit-class trigger values to its evdev domain and uses ordinary FF output; the cited driver writes **zero for trigger-specific motors** in its own FF format. This **does not prove** that physical trigger motors do not exist or cannot be addressed by other protocols/software. [`xbox-series-xpad-axis-domains`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-xpad-axis-domains.json), [`xbox-series-xpad-trigger-rumble-limitation`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-xpad-trigger-rumble-limitation.json).

## Audio and feature requests

The inspected xpad path does not expose a complete GIP headset/audio stack. It is a consumer limitation, not a hardware speaker/headset impossibility claim. Similarly, an SDL serial request left disabled in source is not evidence that active host software requests it. [`audio-xbox-series-xpad-disables-gip-audio`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/audio-xbox-series-xpad-disables-gip-audio.json), [`xbox-series-sdl-disabled-serial-request`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-sdl-disabled-serial-request.json).

## Required validation

Compare a real USB controller and real Bluetooth session (same hardware/firmware where possible), exact bus/interfaces, SDL backend, battery, Share and triggers, native output frames and actuator response, reconnect and long-run neutral cleanup. A virtual event clone can be called transparent at the **application-event level** only after separate native-transport tests.
