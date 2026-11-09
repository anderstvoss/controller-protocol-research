# Nintendo Switch 2 Pro Controller

> Reviewed corpus: 2026-11-09. Unless stated otherwise this chapter describes inspected *consumer source code*, not a physical retail capture.

**Registry:** [Switch 2 Pro](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/switch2-pro.json). The Switch 2 protocol and host decoder must **not** be treated as an inherited Switch 1 Pro HID variant solely on the basis of similar labels or Nintendo vendor ID.

## The current source-supported scope

A newer pinned SDL Switch 2 code path identifies two additional **paddle** buttons in its `data[8]` bits `0x01/0x02` and maps them to distinct consumer joystick positions. That is a **source-only consumer mapping**, not a physical capture, a guarantee that original device button identifiers match the SDL labels, or proof that the older SDL 3.2.0 binary contains this driver: [`switch2-independent-raw`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-independent-raw.json), [`switch2-sdl-decoder`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-sdl-decoder.json).

The corpus explicitly retains missing physical/raw and Linux event-device exposure: [`switch2-linux-exposure-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-linux-exposure-unknown.json), [`switch2-physical-corroboration-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-physical-corroboration-unknown.json).

## Read next

- [Host decoding, identity, Bluetooth/USB and validation](source-and-validation.md).
- [Switch 2 GameCube USB controller](../switch2-gamecube/index.md) — a **different** device with analogue trigger travel, separate clicks and simpler motor output.
- [Switch 1 Pro](../switch-pro/index.md) — separate protocol, source and firmware scope.

## Public supplementary research

[ndeadly Switch 2 controller research](https://github.com/ndeadly/switch2_controller_research) publishes evolving material on controller HID, commands and Bluetooth. It has **not** been pinned/hashed into these specific corpus claims at this snapshot; treat it as a research lead until the evidence corpus ingests an immutable revision.
