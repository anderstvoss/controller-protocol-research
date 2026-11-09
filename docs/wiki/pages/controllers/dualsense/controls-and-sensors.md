# DualSense — controls, touchpad, IMU and calibration

[← DualSense overview](index.md) · [Report contract](reports-and-features.md)

> **Evidence snapshot:** corpus `ab74f662…` (2026-11-09); source-only versus physical and device versus consumer evidence are kept distinct.

## Common gamepad input

In the source-described USB `0x01` packet the four stick bytes occupy positions **1–4**; analog triggers **5–6**; a sequence field follows, with button/hat data, IMU and touch contacts later in the report. This is a **layout description**, not a guarantee that every consumer exposes every field as a joystick axis. [`ds-l0-device-usb01-full-fields`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-usb01-full-fields.json).

Do not synthesize L2/R2 digital bits by pretending that one physical analog threshold has been established: the inspected SDL path uses a **zero-analog plus digital-bit fallback**, whereas Linux provides separate digital controls. The genuine hardware threshold is not proven by this contrast: [`ds-l0-consumer-l2r2-digital-analog-policy`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-consumer-l2r2-digital-analog-policy.json).

## Touchpad and contact state

Two 4-byte contact structures encode a 7-bit contact ID and top-bit inactive flag, with packed **12-bit X/Y** coordinates. Linux uses a **1920×1080** convention; SDL's different normalization denominator is consumer behavior, not evidence of a physically smaller touch surface. See [`ds-l0-device-touchpad-format-dimensions`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-touchpad-format-dimensions.json).

For implementation, preserve each contact's active/inactive state and ID through release. A single generic mouse motion node cannot encode this full report history or prove touch API parity.

## Motion and calibration

Source formats use signed little-endian **16-bit accelerometer and gyro channels**. Linux calibrates from `0x05` via per-axis `(raw − bias) × (sensitivity numerator / denominator)`, while compatible HHD conventions may choose synthetic scales. Host normalized units are not automatically raw sensor resolution: [`ds-l0-device-imu-scaling-formulas`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-imu-scaling-formulas.json), [`ds-l0-hhd-touch-motion`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-hhd-touch-motion.json).

A useful reference test includes: static gravity at several orientations, known axis rotations, timestamps and observed noise/bias, warm-up and one-axis-at-a-time movement. Repeat against physical and virtual paths while logging exact SDL sensor backend and kernel sensor sibling nodes. Otherwise leave axis direction, scale and timing as revision-specific or unknown.

## Battery and status

Kernel and SDL can interpret battery/charge fields in input reports, but a synthetic always-full/external-power default is not a device observation. Treat power/status and sampled sensor timing as independent state channels. See [`ds-l0-sdl-touch-battery`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-sdl-touch-battery.json).
