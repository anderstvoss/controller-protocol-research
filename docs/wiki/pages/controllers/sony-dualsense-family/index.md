# Sony DualSense family — commonality and non-inheritance

> **Evidence snapshot:** corpus `ab74f662…` (2026-11-09); source-only versus physical and device versus consumer evidence are kept distinct.

**Registry:** [Sony DualSense family](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/sony-dualsense-family.json). Members currently represented as distinct controllers: [DualSense](../dualsense/index.md) and [DualSense Edge](../dualsense-edge/index.md).

The family is an **evidence-scoping tool**. Similar HID report formats and host code paths do not imply identical PID, calibration payload, adaptive trigger envelope, extra-button behavior or physical features.

| Question | Reference chapter | Rule |
| --- | --- | --- |
| Standard report framing, feature probes and touch/IMU | [DualSense reports](../dualsense/reports-and-features.md) | Source-backed baseline, firmware-sensitive |
| Advanced trigger and LED output | [DualSense outputs](../dualsense/outputs-and-audio.md) | No physical Edge equivalence inferred |
| Edge identity and auxiliary buttons | [Edge](../dualsense-edge/index.md) | Separate consumer identity ([`dsedge-l0-consumer-identity-separation`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/dsedge-l0-consumer-identity-separation.json)) |
| Host-selected Sony HIDAPI or evdev | [Consumer matrix](../dualsense/consumers-and-validation.md) | Record actual backend; family name alone is inadequate |

For a future shared claim, qualify *which* revisions it covers and preserve device-versus-consumer role. If only SDL and Linux share a parser, write a **consumer** family claim rather than asserting that both retail firmwares emit identical bytes.
