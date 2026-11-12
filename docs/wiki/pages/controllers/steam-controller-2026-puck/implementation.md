# Puck — emulation architecture and compatibility boundaries

[← Puck overview](index.md) · [USB interface map](interfaces-and-slots.md)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

## Target: a simulated USB receiver, not just four input event nodes

The intended **`dummy_hcd` virtual Puck** should present a coherent composite USB device so consumers can enumerate its expected interfaces and issue real control/interrupt transfers. The interface/endpoint layout must be established from physical or suitable pinned source evidence; merely copying an OpenPuck HID descriptor is insufficient for full USB fidelity. [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json), [`sc2-gap-puck-usb-descriptors`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-usb-descriptors.json).

A useful decomposition is:

- **USB receiver container:** VID/PID, configuration, interface descriptors, endpoint descriptors, HID report collections; actual slot interface numbering.
- **Slot router:** independent connected state and report streams per slot, close/removal/reconnect, feature/output delivery and neutralization.
- **Native codec:** reuse measured `0x42` and source-described `0x45`/`0x47` roles from the controller protocol where applicable.
- **Firmware-compatibility adapter:** OpenPuck-style state synthesis and report handling as an *implementation reference*, not a physical oracle.
- **Validation harness:** Linux enumeration, kernel bind, SDL HIDAPI, Steam recognition and per-slot bidirectional traces as independent results.

## Reuse OpenPuck deliberately

OpenPuck's pinned external mode uses **`28de:1304`** ([`puck-current`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/puck-current.json)) and creates four HID slots ([`sc2-migration-openpuck-slots`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-migration-openpuck-slots.json)). It offers a concrete porting candidate for feature exchange and slot semantics, but expected output must be compared with real Puck captures and with Linux/SDL requirements. Avoid copying upstream code into the CC-BY-4.0 evidence data; review its own license and the destination code license separately. Source record: [`openpuck`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/source/openpuck.json).

## Consumer-specific acceptance

For each target, log which USB interface and driver it bound, raw/client ownership, feature requests, slot activity and output acknowledgments. One SD​L-detected instance is not acceptance for Steam, kernel evdev, simultaneous clients or composite teardown. The kernel and SDL source expectations are in [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json); the physical gaps are in [`sc2-gap-puck-slots`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-slots.json).

## Excluded shortcut

Four uinput gamepads can be a useful application-output demo but do **not** emulate an external Puck as a real USB receiver. Likewise generic UHID may suffice for a direct-controller experiment but is not proof of 2–5 Puck interface enumeration.

## Receiver implementation state transitions (source-only)

The [receiver lifecycle study](receiver-lifecycle.md) adds an operational contract for a virtual Puck: a slot presence gate, conditional gamepad/sensor/battery registration, **fresh device lifetime on reconnect**, interface-local HID features/output, and independent removal of its joystick/nodes. A slot epoch is a reasonable *inferred* model, not a measured Puck transport field. SDL distinguishes wireless status `0x46`/`0x79` and does not recognize the historical `0x7b` as a status at the pinned revision. Receiver-wide failure, pairing and output after absence remain untested. [`rcv-puck-sdl-presence`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-sdl-presence.json), [`rcv-puck-reconnect-epoch-inference`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-reconnect-epoch-inference.json), [`rcv-puck-physical-slot-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-physical-slot-unknown.json).
