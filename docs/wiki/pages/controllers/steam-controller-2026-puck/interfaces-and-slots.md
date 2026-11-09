# Puck — USB composite interface model and slots

[← Puck overview](index.md) · [Implementation](implementation.md)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

## Host-observed expectations from source

| Interface | Source-described purpose | Evidence limit |
| --- | --- | --- |
| 0–1 | Receiver non-HID functions | Not yet physically captured or semantically characterized |
| 2–5 | Up to four HID controller slots | SDL Triton explicitly selects these interface numbers |
| 6 | Pogo/interface-specific function | Physical endpoint/report semantics unverified |

This seven-interface arrangement comes from **pinned kernel/SDL code**, not a complete captured Puck `lsusb` configuration. See [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json) and [`sc2-gap-puck-usb-descriptors`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-usb-descriptors.json).

**Important:** a single UHID device can expose suitable HID usages and report IDs while still reporting interface number **−1** to Linux HIDAPI because it has no USB interface parent. Therefore it cannot automatically satisfy SDL's `interface_number` 2–5 receiver filter. A `dummy_hcd` USB composite presentation is one way to test a full interface ancestry; it is an **implementation direction**, not a proven requirement of every possible consumer. See [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json).

## Wireless lifecycle versus USB slot representation

Controller slot binding and release, receiver-wide USB health, native state stream, per-slot output and reconnect are separate state machines. Source parsers know `0x79` connection events and OpenPuck synthesizes slot state, but device-side event order, pairing and multi-slot interactions remain unverified: [`sc2-gap-puck-slots`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-slots.json), [`sc2-gap-wireless-events`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-wireless-events.json), [`sc2-migration-openpuck-slots`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-migration-openpuck-slots.json).

The retained notes specifically observed `0x42` size 54 and aggregate report windows at `1304`, without proving exact per-packet cadence or source-derived `0x7b` semantics: [`sc2-july-puck-input-42`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-july-puck-input-42.json), [`sc2-cadence`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-cadence.json).

## Avoid two common modeling errors

1. **Treating four OpenPuck HID objects as the official complete seven-interface USB composite:** OpenPuck proves only its own compatibility design ([`sc2-migration-openpuck-slots`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-migration-openpuck-slots.json)).
2. **Treating a slot's native state as its entire lifecycle:** connect/disconnect, feature requests, lizard policy, ownership and outgoing motor traffic require explicit coverage ([`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json)).

The needed physical Puck descriptor inventory is a controlled, read-only capture of device/configuration/interface/endpoint/HID data, tied to device revision and scrubbed before corpus publication.
