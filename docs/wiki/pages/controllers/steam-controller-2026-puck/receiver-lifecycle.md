# Steam Controller Puck — per-slot host lifecycle

[← Puck overview](index.md) · [USB interfaces](interfaces-and-slots.md) · [Implementation](implementation.md) · [Physical validation](validation.md)

> **2026-11-11 consumer-source research only.** This chapter explains what pinned Linux `hid-steam` and SDL Triton code *would do* with a receiver interface; it does not report a hardware Puck session or a live virtual receiver test. See [full source decision table](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/docs/receivers-puck-consumer-lifecycle.md).

## An interface is not a player

The pinned receiver topology has non-HID interfaces 0–1, four HID controller-slot interfaces **2–5**, and reduced pogo interface 6. Linux creates a separate `steam_device` for each accepted HID interface. SDL filters receiver interfaces by number and maintains an independent joystick context for each one. Neither object should be conflated with a stable player index or with one global four-slot gamepad. [`rcv-puck-kernel-per-interface`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-kernel-per-interface.json), [`rcv-puck-sdl-joystick-lifecycle`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-sdl-joystick-lifecycle.json).

## Connection and host-device creation

| Event | Linux kernel consumer | SDL Triton consumer |
| --- | --- | --- |
| First probe | Queries wireless status; only a connected slot can register native gamepad, sensor and battery | Initially has an interface but **not** a connected joystick |
| Presence update | Decodes length-checked input report `0x79`; native input or battery reports may also schedule connection | Recognizes status IDs **`0x46` and `0x79`**; input can imply attach |
| Connected | Registers per-interface gamepad, sensor and optional battery nodes when kernel-owned | Adds joystick for that context |
| Disconnected | Unregisters native nodes and cancels selected work | Removes joystick for that context |
| Reconnected | Allocates new input objects, so do not assume prior `eventN` lifetime persists | Creates another joystick attachment for the interface |

Evidence: [`rcv-puck-kernel-presence`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-kernel-presence.json), [`rcv-puck-sdl-presence`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-sdl-presence.json), [`rcv-puck-kernel-attach`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-kernel-attach.json), [`rcv-puck-kernel-detach`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-kernel-detach.json), [`rcv-puck-sdl-joystick-lifecycle`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-sdl-joystick-lifecycle.json).

**Do not reinterpret the historical `0x7b` note as an SDL wireless-status event.** The examined SDL definitions use `0x46` and `0x79`; the retained physical Puck-path note and SDL dispatch are different evidence. [`rcv-puck-sdl-presence`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-sdl-presence.json).

## Ownership, output and failure boundaries

Kernel raw-client ownership can remove native evdev and sensor registration for the selected interface. SDL periodically requests lizard disable and IMU settings for an attached joystick; both consumers route features and haptic output using **their own HID handle**, not an application-level player number. Power/battery and serial-derived labels are scoped per kernel device, but neither proves persistent receiver bonds or player LEDs. [`rcv-puck-lizard-arbitration`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-lizard-arbitration.json), [`rcv-puck-output-routing`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-output-routing.json), [`rcv-puck-identity-battery`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-identity-battery.json).

The kernel removes native objects and drains work for a failing HID interface; SDL removes its joystick on a failed read. This does **not** establish simultaneous sibling survival or receiver-wide atomic teardown. A slot epoch (new logical lifetime on genuine disconnect/reconnect) follows as an **inference**, not a host or physical measurement. [`rcv-puck-teardown`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-teardown.json), [`rcv-puck-reconnect-epoch-inference`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-reconnect-epoch-inference.json).

## Still unknown on retail hardware

Physical USB descriptor completeness, connect-event order, multi-slot pairing and bond persistence, per-slot output after departure, receiver unplug and player indicator semantics remain unknown. Capture real Puck behavior and separately run `dummy_hcd` acceptance before claiming full receiver fidelity. [`rcv-puck-physical-slot-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-physical-slot-unknown.json); compare the existing [physical validation plan](validation.md).
