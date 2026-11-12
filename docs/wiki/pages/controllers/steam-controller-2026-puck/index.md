# Steam Controller Puck (2026 wireless receiver)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

**Registry:** [physical Puck](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/steam-controller-2026-puck.json), parent [Steam Controller 2026](../steam-controller-2026/index.md). The distinct [OpenPuck](../openpuck-firmware/index.md) record represents **compatibility firmware**, not the original Valve USB device.

## Reader path

- [USB composite interfaces, slots and identity](interfaces-and-slots.md)
- [Per-slot kernel and SDL receiver lifecycle](receiver-lifecycle.md) — 2026-11-11 source-only host study.
- [Simulated-Puck implementation considerations](implementation.md)
- [Physical capture and validation](validation.md)
- [Controller native protocol](../steam-controller-2026/protocol.md) — shared report family, with receiver-specific uncertainty.

## Established versus anticipated

Retained 2026-07-31 operator notes associate the official receiver with **`28de:1304`** and a reviewed **372-byte HID descriptor length**. That is currently **source-supported** evidence from the retained note, **not** an available full physical Puck configuration/endpoint capture: [`sc2-july-puck-identity-descriptor`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-july-puck-identity-descriptor.json), [`sc2-gap-puck-usb-descriptors`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-usb-descriptors.json).

The notes record Puck-path `0x42` 54-byte input report counts across idle, lizard and reconnect windows. These are aggregate retained counts and cannot independently establish each field or a physical reporting frequency: [`sc2-july-puck-input-42`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-july-puck-input-42.json).

Pinned Linux and SDL describe a **seven-interface receiver design** with controller slots 2–5, non-HID interfaces 0–1 and pogo interface 6. This is host **source** interpretation, not an independently recovered retail descriptor: [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json).

## Scope boundaries

- One Puck and one Steam Controller 2026 are available for D9 follow-up; a Steam Machine internal receiver `1305` is *out of scope*.
- The four controller slots represent receiver interfaces, **not** four guaranteed simultaneously tested retail controllers.
- A direct wired controller `1302`, BLE model `1303`, external Puck `1304` and internal receiver `1305` must remain distinct modes/identities.
- Historical `1142` OpenPuck compatibility assertions were not silently dropped; see [`puck-historical-compat`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/puck-historical-compat.json) and [`puck-historical-physical`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/puck-historical-physical.json).

**Deep research:** [full Puck research gaps](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-controller-2026-research-gaps.md); [migration ledger](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/steam-controller-migration.md).

## November 11 source-only lifecycle update

Pinned Linux/SDL consumer code clarifies how four receiver-slot HID interfaces are **attached and removed independently**: Linux status `0x79`; SDL status IDs `0x46`/`0x79`, **not** `0x7b`; native evdev/sensor/battery lifetimes depend on slot connectivity and raw-HID ownership. Per-slot reconnect epochs are inferred, and retail pairing/bond persistence still lacks physical evidence. See [receiver lifecycle](receiver-lifecycle.md), [`rcv-puck-sdl-presence`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-sdl-presence.json), [`rcv-puck-physical-slot-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/rcv-puck-physical-slot-unknown.json).
