# Joy-Con (L) — source-derived wire fields and host presentation

[← Joy-Con Left overview](index.md) · [Joy-Con family](../switch-joycon-family/index.md) · [Pairing](../switch-joycon-family/pairing-and-consumers.md)

> **2026-11-11 source-only narrowing.** The new `joycon-cgap-left-*` records distinguish *device protocol descriptions* from *kernel/SDL consumer interpretations*. No retail Joy-Con, host session or physical sensor/rumble validation was performed. Full dispositions: [left-half gaps brief](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/docs/switch-joycon-left-gaps-2.md).

## Native left-half identity and fields

The source-described standalone Bluetooth left half uses Nintendo **`057e:2006`**, device-info subcommand `0x02` type byte **`0x01`**. The consumer-combined `057e:2008` identity is *not* the left half's native identity. [`joycon-cgap-left-identity`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/joycon-cgap-left-identity.json).

In report `0x30`, source-described common button byte 4 contains Minus (bit 0), left-stick click (bit 3) and Capture (bit 5). Left-side byte 5 bits 0–7 encode Down, Up, Right, Left, SR, SL, L and ZL. The 12-bit packed left stick occupies bytes 6–8. **Unused right-stick bytes on a real left half remain unknown**; an emulator filling zeros is not a physical capture. [`joycon-cgap-left-wire-fields`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/joycon-cgap-left-wire-fields.json).

## Linux `hid-nintendo`: separate evdev representation

| Input | Selected Linux kernel output |
| --- | --- |
| D-pad | `BTN_DPAD_*` keys, **not a hat axis** |
| Minus / Capture | `BTN_SELECT` / `BTN_Z` |
| L / ZL / stick-click | `BTN_TL` / `BTN_TL2` / `BTN_THUMBL` |
| SL / SR | `BTN_TR` / `BTN_TR2` only outside the USB Charging Grip |
| Stick | Decode 12-bit left X/Y, apply left-stick calibration, emit `ABS_X/Y` with normalized Y inverted |
| Motion | Three accelerometer/gyro frames per `0x30` input, separate sensor evdev node; **no additional Y/Z sign reversal for left** |

The left-versus-right IMU distinction matters: the pinned consumer negates Y/Z for a right-capable half, not the standalone left. These are **consumer transformations**, not raw packet guarantees. [`joycon-cgap-left-kernel-buttons`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/joycon-cgap-left-kernel-buttons.json), [`joycon-cgap-left-kernel-stick`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/joycon-cgap-left-kernel-stick.json), [`joycon-cgap-left-kernel-imu`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/joycon-cgap-left-kernel-imu.json).

## SDL3: sideways mini-mode versus vertical/paired

An unparented left Joy-Con defaults in pinned SDL3 to a **sideways mini-gamepad**: D-pad inputs become face buttons and stick/sensor axes rotate for that presentation. Paired or configured vertical mode instead maps the same physical fields to conventional left axes and a D-pad hat. This changes the **host-visible input shape**, not the Joy-Con's raw bytes or identity. [`joycon-cgap-left-sdl3-modes`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/joycon-cgap-left-sdl3-modes.json).

## What remains untested

Physical HID report map and unused-stick bytes, calibration and IMU response, rail-mode behavior, SDL backend selection, Charging Grip handoff, wireless pairing and output correctness. A faithful implementation needs separate raw-device capture and consumer acceptance; the left half should not inherit right-half transforms merely because both are members of the same family.
