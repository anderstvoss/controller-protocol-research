# Logitech DJ / Unifying receiver

[Registry entry](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/controller/logitech-dj-receiver.json). This is a receiver lifecycle comparison, not a gamepad profile.

## Source-only Linux consumer behavior

- Multiple receiver HID interfaces share one driver state. Paired children may be keyboards or pointers; child indices 1–7 are a software range, not measured concurrent capacity. [`rcv-pattern-dj-receiver-children`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/rcv-pattern-dj-receiver-children.json).
- Pair notification `0x41` creates a child; unpair `0x40` destroys it. Link loss `0x42` neutralizes input while retaining the child. Pairing again after unpair creates a new object. [`rcv-pattern-dj-linkloss-unpair`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/rcv-pattern-dj-linkloss-unpair.json).
- Child HID++ requests route through the shared receiver with the child index. Removing a child removes its request endpoint; delivery of already pending output is unverified. [`rcv-pattern-dj-routed-output`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/rcv-pattern-dj-routed-output.json).
- Loss of a required receiver USB interface destroys all paired children, even if other interfaces remain bound. Distinguish this shared failure from ordinary child link loss. [`rcv-pattern-dj-interface-failure`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/rcv-pattern-dj-interface-failure.json).

No physical receiver, pairing, concurrent capacity, or virtual USB binding was tested. See the [receiver comparison](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/docs/receivers-lifecycle-decision-table.md).
