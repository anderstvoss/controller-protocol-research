# Nintendo GameCube four-port USB adapter (WUP-028)

> Reviewed corpus: 2026-11-09. Unless stated otherwise this chapter describes inspected *consumer source code*, not a physical retail capture.

**Registry:** [GameCube USB adapter](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/gamecube-usb-adapter.json), a single USB device carrying **up to four** GameCube controllers. The adapter may host wired pads or WaveBird receivers per port; it is not itself a Switch 2 GameCube USB Controller.

## Pages

- [USB interrupt reports, port slots and rumble](usb-protocol.md)
- [Libusb consumers versus four uinput gamepads](consumers-and-virtualization.md)
- [Physical verification and unknowns](validation.md)

## Protocol at a glance

The retained independent SDL and Dolphin parsers describe USB `057e:0337` (adapter), one-byte initialization `0x13` host output, **37-byte input `0x21`** (one ID byte plus four 9-byte slot blocks), and **five-byte output `0x11`** (rumble control for each port). Port status bits distinguish wired `0x10` and WaveBird `0x20` presence: [`gc-adapter-usb-identity`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-usb-identity.json), [`gc-adapter-input-report-layout`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-input-report-layout.json), [`gc-adapter-init-command`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-init-command.json), [`gc-adapter-port-type-bits`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-port-type-bits.json), [`gc-adapter-rumble-output`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-rumble-output.json).

This is unusually strong **source corroboration** for an interface contract, but it is not a captured genuine USB descriptor or physically validated adapter. Full endpoint, polling, string and clone differences remain unknown: [`gc-adapter-descriptors-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-descriptors-unknown.json), [`gc-adapter-descriptor-details-unconfirmed`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-descriptor-details-unconfirmed.json).

Source comparison: [SDL/Dolphin survey](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/gamecube-adapter-consumer-survey.md); [independent consumer follow-up](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/gamecube-usb-adapter-l0.md).
