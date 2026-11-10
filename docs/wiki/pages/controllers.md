# Controller library

The registry distinguishes controllers, families, compatibility emulators and host-interface concepts. A family claim does not automatically apply to every model or revision.

## Valve

- [Steam Controller (2026)](controllers/steam-controller-2026/index.md) — direct HID, native inputs, lizard mode, feature/output traffic, consumer arbitration.
- [Steam Controller Puck](controllers/steam-controller-2026-puck/index.md) — receiver identity, USB interface layout, wireless slots, OpenPuck comparison.
- [OpenPuck compatibility firmware](controllers/openpuck-firmware/index.md) — emulated USB receiver and other device modes; **not** a physical reference.

## Nintendo

- [Wii Remote / MotionPlus / extensions](controllers/wii-remote/index.md)
- [Switch Pro Controller](controllers/switch-pro/index.md)
- [Switch 1 Joy-Con family](controllers/switch-joycon-family/index.md)
- [Joy-Con (L)](controllers/switch-joycon-left/index.md)
- [Joy-Con (R)](controllers/switch-joycon-right/index.md)
- [Switch 2 Pro Controller](controllers/switch2-pro/index.md)
- [Switch 2 GameCube USB Controller](controllers/switch2-gamecube/index.md)
- [GameCube four-port USB adapter (WUP-028)](controllers/gamecube-usb-adapter/index.md)

## Sony

- [DualSense](controllers/dualsense/index.md)
- [DualSense Edge](controllers/dualsense-edge/index.md)
- [DualSense family](controllers/sony-dualsense-family/index.md)
- [DualShock 4](controllers/dualshock4/index.md)

## Microsoft and third-party

- [Xbox 360 standard-HID realization](controllers/xbox360/index.md) — explicitly separate from native XUSB.
- [Xbox Series Controller](controllers/xbox-series/index.md)
- [8BitDo Pro 2](controllers/8bitdo-pro-2/index.md)

## Cross-platform

- [Linux joystick identity / SDL / evdev](controllers/linux-joystick-identity/index.md) — a host-interface registry entry, not a physical controller.

The [controller registry](https://github.com/anderstvoss/controller-protocol-research/tree/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller) supplies names, parent relationships and tracking issues; these pages are not substitutes for that registry.
