# GameCube USB adapter — lab plan

[← Adapter overview](index.md)

> Reviewed corpus: 2026-11-09. Unless stated otherwise this chapter describes inspected *consumer source code*, not a physical retail capture.

## Minimum physical reference

Acquire a genuine adapter and at least one wired GameCube pad; a WaveBird receiver is needed to qualify the wireless port-type behavior. The corpus's source-only input/output contract is not a substitute for a real descriptor or port transition capture: [`gc-adapter-descriptors-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-descriptors-unknown.json).

1. **Device:** inventory USB configuration, interface, endpoints, strings and polling properties. Check power cable state.
2. **Startup:** capture bounded `0x13` initialization and device response; attribute host backend and endpoint.
3. **Port:** connect/release each wired port independently, verify complete nine-byte block and 0x10 presence; then WaveBird 0x20 if available.
4. **Controls:** sticks center/extremes, C-stick, analog trigger travel and independent clicks, D-pad, A/B/X/Y/Z/Start.
5. **Output:** bounded rumble `0x11`, port-specific actuation/power, safe stop and optional brake 2.
6. **Consumers:** fixed SDL/Dolphin/Eden/Cemu libusb versus ToadKing/evdev comparison, record active backend and permissions.
7. **Cleanup:** removal of logical pads on port loss and receiver-wide USB teardown.

Keep clone `PC mode` controllers out of claims tied to genuine Wii U mode unless separately registered and tested. The source ledger names unresolved descriptor details and status bits: [`gc-adapter-remaining-status-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-remaining-status-unknown.json), [`gc-adapter-descriptor-details-unconfirmed`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-descriptor-details-unconfirmed.json).

Owner engineering choices: [compatibility versus faithful USB](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/gamecube-adapter-decision-table.md).
