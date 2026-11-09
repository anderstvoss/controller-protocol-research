# Switch 2 Pro — host evidence and what remains to capture

[← Switch 2 Pro](index.md)

> Reviewed corpus: 2026-11-09. Unless stated otherwise this chapter describes inspected *consumer source code*, not a physical retail capture.

## Decoder versus physical behavior

The specific Switch 2 Pro claim relates to the **paddle field decoded by a newer SDL source revision**. Do not infer that an SDL 3.2.0 control probe or a kernel evdev implementation recognizes those paddle bits. The physical buttons, firmware mapping, raw packets and exact host-selected backend have not been independently measured: [`switch2-independent-raw`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-independent-raw.json), [`switch2-sdl-decoder`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-sdl-decoder.json), [`switch2-linux-exposure-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-linux-exposure-unknown.json).

The public current Linux [`hid-nintendo.c` source](https://github.com/torvalds/linux/blob/master/drivers/hid/hid-nintendo.c) mentions Switch 2 model support; because `master` moves, compare its **pinned actual commit** to the repository's earlier source pins before writing new claims. This link is *supplemental outside-corpus reference*, not a qualified physical result.

## Needed investigation

1. Obtain exact physical model/revision and USB/Bluetooth descriptors (privacy-scrubbed).
2. Compare physical raw inputs, every extra button, sticks, triggers, motion and disconnect/reset behavior against pinned SDL and kernel consumers.
3. Characterize Bluetooth identity, security/pairing and report framing **separately** from USB.
4. Record output command/ACK/rumble/LED semantics, not just input visibility.
5. Run fixed-version SDL HIDAPI, SDL evdev, kernel and Steam as separate consumers; require backend attribution.
6. Before making controller-specific implementation promises, create corpus claims with pinned sources, controlled experiments and fixtures.

The explicit no-physical-evidence status remains [`switch2-physical-corroboration-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-physical-corroboration-unknown.json). A perceived lack of paddle evdev events may be a driver/backend issue, not an absence of native buttons.
