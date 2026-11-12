# OpenPuck — compatibility implementation, not physical Valve hardware

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

**Registry:** [OpenPuck firmware](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/openpuck-firmware.json), listed separately from the [Puck receiver](../steam-controller-2026-puck/index.md).

The pinned OpenPuck source (revision `29f4d1e8b85c0a7c19e0c8b977a1a56a2c42ea6d`) deliberately synthesizes controller/receiver behavior. The external Puck mode selects `28de:1304` ([`puck-current`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/puck-current.json)) and defines **four HID objects**, one per slot ([`sc2-migration-openpuck-slots`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-migration-openpuck-slots.json)). The same code path can select `1305` for an internal-receiver mode, but `1305` physical functionality is not in the current Puck scope ([`sc2-migration-openpuck-identities`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-migration-openpuck-identities.json)).

The modeled reports, slots, connect/status behavior and feature responses are valuable to a compatibility implementation. They **cannot establish** the genuine external receiver's entire USB configuration, exact slot lifecycle, endpoint topology or wireless behavior. This is the central contrast with [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json) and [`sc2-gap-puck-usb-descriptors`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-usb-descriptors.json).

## Topics

- [Compatibility behavior and fidelity limits](comparison.md)
- [Physical Puck chapter](../steam-controller-2026-puck/index.md)
- [Direct wired Steam Controller](../steam-controller-2026/index.md)

OpenPuck also contains non-Valve compatibility modes. Sony DS4 report/feature structures are discussed in the [DualShock 4 chapter](../dualshock4/index.md), and Switch Pro output and memory behavior in [Switch Pro](../switch-pro/index.md); neither is a genuine hardware capture. Sources: [`openpuck`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/source/openpuck.json), [`openpuck-ds4`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/source/openpuck-ds4.json), [`swpro-openpuck-mode`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/source/swpro-openpuck-mode.json).
