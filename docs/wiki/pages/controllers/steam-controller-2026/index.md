# Valve Steam Controller (2026)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

**Registry:** [Steam Controller 2026](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/steam-controller-2026.json). This is the **controller**, not the separate [Puck receiver](../steam-controller-2026-puck/index.md) or [OpenPuck emulator](../openpuck-firmware/index.md).

The D9 research establishes a useful physical **wired `28de:1302`** reference, especially for native input and selected output exchanges. Its value is limited to the recorded device and procedures. Neither the existence of a kernel decoder nor successful virtual enumeration settles wireless fidelity or Steam client integration.

## Chapter map

- [USB identity and report protocol](protocol.md)
- [Buttons, axes, pads and motion](controls.md)
- [Lizard, kernel, SDL and Steam ownership](modes-and-consumers.md)
- [Rumble, MIDI, PCM haptics and audio](haptics-and-audio.md)
- [Implementation and physical verification plan](validation.md)
- [Puck receiver](../steam-controller-2026-puck/index.md) — separate USB composite device.

## What is supported

The physical wired descriptor has **one USB HID interface**, not a three-interface composite: its 372-byte HID report descriptor contains three top-level application collections. The configuration/endpoint observation and report declaration are independently recorded in [`steam-s3-1302-usb-interface`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-s3-1302-usb-interface.json) and [`steam-s3-1302-report-shapes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-s3-1302-report-shapes.json) (**physically observed**, USB).

D9 isolated many of the raw `0x42` digital controls, analog sticks/triggers and touch/capacitive channels. These are **measured one-device windows**, with incidental contacts and qualitative stimulus limitations retained: [`steam-d9-native-digital-correspondence`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-native-digital-correspondence.json), [`steam-d9-native-touch-pressure`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-native-touch-pressure.json). A later SDL API-enabled run made IMU fields change; earlier motion windows did not: [`steam-d9-sdl-enabled-motion`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-sdl-enabled-motion.json).

Host-side kernel and SDL paths are still distinct. A raw client may suppress kernel-produced gamepad/sensor nodes while firmware-origin mouse/keyboard reports remain independently visible. The Steam client's own routing and activation state cannot be inferred merely by enumerating a node: [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json), [mode evidence and limitations](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-controller-modes.md).

## Explicitly not established

- A physical BLE `28de:1303` pairing and report study, equivalent in scope to the wired work.
- Universal firmware defaults and exact physical watchdog timeout across revisions.
- Full physical transfer functions and actuation fidelity for every haptic/pad/grip output.
- An assertion that virtual UHID, virtual USB and Steam Input select identical host paths.

**Primary corpus narrative:** [full gaps matrix](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-controller-2026-research-gaps.md), [S3 physical descriptor](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-s3-physical-descriptor.md), [D9 input reference](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-d9-native-input-reference-2026-11-04.md).
