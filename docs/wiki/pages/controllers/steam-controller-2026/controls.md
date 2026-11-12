# Steam Controller 2026 — native controls and sensor data

[← Controller overview](index.md) · [Report protocol](protocol.md)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

## Digital mapping of input `0x42`

Owner-labelled **direct-wired** 54-byte packets in D9 corroborated these button bit positions (bit index within the 32-bit buttons field, not absolute USB packet bit index):

| Inputs | Bits |
| --- | --- |
| A, B, X, Y | 0, 1, 2, 3 |
| Quick Access Menu, right stick click, Menu | 4, 5, 6 |
| R4, R5, right shoulder | 7, 8, 9 |
| D-pad down, right, left, up | 10, 11, 12, 13 |
| View, left stick click, Steam | 14, 15, 16 |
| L4, L5, left shoulder | 17, 18, 19 |
| Right trigger click, left trigger click | 23, 27 |

Source: [`steam-d9-native-digital-correspondence`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-native-digital-correspondence.json). View was positively observed twice after a reported missed action; most other labelled digital controls had three press/release cycles. This is not a clean negative-test matrix.

## Analog and capacitive surfaces

D9's retained packets show sticks reaching approximately **−32767 to +32767**, trigger analog values **0 to 32767**, and full-trigger click flags. The sampled capacitive channels correlate stick touch (right bit 20, left bit 24), pad touch (right bit 21, left bit 25) and grip touch (right bit 28, left bit 29). Pad coordinates have signed domains near ±32766. Qualitatively labelled touch/light/firm windows support a **nonlinear pressure response**, but do not establish a universal physical force-to-count curve. Some grip samples also touched a pad accidentally. See [`steam-d9-native-touch-pressure`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-native-touch-pressure.json) and [full D9 conditions](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-d9-native-input-reference-2026-11-04.md).

## Lizard reports are a different output of the same controller

When firmware lizard mode supplies desktop controls, the physical wired experiments recorded `0x40` mouse (6 wire bytes) and `0x41` keyboard (9 wire bytes). The default mapping included right pad relative pointer and button actions, left-pad wheel/horizontal scrolling, and keyboard-emitted mappings; this is not a substitute for native `0x42`. See [`steam-d9-lizard-control-mapping`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-lizard-control-mapping.json). Disabling native exposure in the host is a separate layer from suppressing all physical desktop output.

## Motion and sensor availability

The SDL-enabled motion session produced changing raw IMU/quaternion fields; the Steam-active batch did not produce useful changing IMU reference values. The latter result **must not** be interpreted as proof that the sensor is absent. SDL sensor enable commands and host ownership matter. No controlled physical axis-direction calibration or sensor clock accuracy is asserted: [`steam-d9-sdl-enabled-motion`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-sdl-enabled-motion.json) and [`sc2-gap-imu-calibration`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-imu-calibration.json).

## Implementation implication

Represent raw native controls, contact/touch, sensor and lizard desktop projections as **distinct state and transport concerns**. Keep a lossless raw report path where consumers need it, and test the app-visible SDL controls separately. Record every mapping as transport/firmware-conditional rather than silently treating these D9 values as BLE or Puck proof.
