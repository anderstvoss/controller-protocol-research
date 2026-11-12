# Xbox 360 — xpad, SDL HIDAPI and generic HID

[← Xbox 360 overview](index.md)

> **Reviewed corpus:** 2026-11-09. A source parser, compatibility shim or virtual-host acceptance does not establish native physical hardware fidelity.

## Host-driver distinctions

| Consumer | What it requires | What a generic HID replacement proves |
| --- | --- | --- |
| Linux `xpad` | Matching vendor USB device/interface, its USB decoder, FF/LED outputs | **Nothing** about xpad if it binds as `hid-generic` |
| SDL Xbox 360 HIDAPI | Eligible recognized type/interface and proper Xbox 360 report parser | A familiar VID/PID **does not prove** this driver was selected |
| SDL Linux evdev/gamepad DB | Correct Linux input events and selected mapping | Supports application compatibility, not XUSB USB protocol |
| uinput FF | Program responding to EV_FF callbacks | **Not** automatic xpad motor writes or xpad LED class nodes |

See [`x360-l0-consumer-xpad-id-usb-binding`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-xpad-id-usb-binding.json), [`x360-l0-consumer-sdl360-classification`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-sdl360-classification.json), [`x360-l0-consumer-uhid-ff-led-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-uhid-ff-led-unknown.json).

## The specific legacy face-button correction

Linux generic `hid-input` maps Game Pad Button usage `n` to `BTN_GAMEPAD + n−1`, creating a subtle X/Y mapping difference from xpad. Historical EXP-0016 corrected the standard-HID descriptor from consecutive usages to **1,2,4,5,7,8,11,12,13,14,15**, plus five constant padding bits, preserving report length while obtaining expected Linux X/Y numeric codes **307/308**. This result is *evdev/SDL host compatibility*, not a physical XUSB discovery test: [`x360-l0-consumer-exp0016-hid-usage-correction`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-exp0016-hid-usage-correction.json), [`x360-l0-consumer-hidinput-button-usage-list`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-hidinput-button-usage-list.json).

## D-pad, triggers, FF and LED

xpad can expose D-pad axes or button domains, trigger values and joystick axes with its own ranges; generic HID decoding follows its descriptor instead. An FF endpoint may be present in an evdev virtual device without any registered xpad `xpadN` LED. Track ownership and whether an output command actually reaches a motor. [`x360-l0-consumer-xpad-dpad-axes-v-buttons`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-xpad-dpad-axes-v-buttons.json), [`x360-l0-consumer-xpad-sticks-trigger-ranges`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-xpad-sticks-trigger-ranges.json), [`x360-l0-consumer-xpad-led-class`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-xpad-led-class.json).

## Recommendation

Keep current standard-HID personality **honestly labeled** as an app-compatible Xbox 360-style gamepad. Only add native XUSB as a *separate USB-interface realization* with its own decoder and verification gates. See [compatibility/fidelity choices](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/xbox360-decision-table.md).
