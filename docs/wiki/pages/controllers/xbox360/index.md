# Xbox 360 — standard HID versus native XUSB

> **Reviewed corpus:** 2026-11-09. A source parser, compatibility shim or virtual-host acceptance does not establish native physical hardware fidelity.

**Registry:** [Xbox 360 standard-HID controller](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/xbox360.json). The corpus contains two **distinct interfaces**: (1) virtualgamepad's intentionally generic HID/evdev personality, and (2) source descriptions of genuine Microsoft **vendor-specific XUSB**.

## Pages

- [Native wired XUSB and receiver report protocols](xusb-protocol.md)
- [Linux xpad, SDL, generic HID and virtualization](consumers-and-compatibility.md)
- [Physical and host acceptance plan](validation.md)

## Non-interchangeability is the central finding

A genuine wired `045e:028e` Xbox 360 controller typically exposes a vendor-specific USB interface decoded by `xpad` or native Xbox 360 consumers. Assigning `045e:028e` to a **generic HID Game Pad** does not create the same interface or make `xpad` bind. The corpus's historical virtual HID successes therefore demonstrate **consumer compatibility on that realization**, not native XUSB protocol fidelity: [`x360-l0-device-xusb-nonhid-interface`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-xusb-nonhid-interface.json), [`x360-l0-consumer-sdl360-vs-generic-hid`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-sdl360-vs-generic-hid.json).

The native XUSB 20-byte input and host rumble/LED packets are source-backed candidates, not retail controlled capture. Wireless receiver `045e:0719` is a separate path with slot presence/packets and must not be treated as Bluetooth or wired XUSB: [`x360-l0-device-xusb-wired20`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-xusb-wired20.json), [`x360-l0-device-wireless-receiver0719-lead`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-wireless-receiver0719-lead.json).

**Research source:** [F ledger](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/xbox360-l0.md), [native/compatibility decision table](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/xbox360-decision-table.md).
