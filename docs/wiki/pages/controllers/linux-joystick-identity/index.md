# Linux joystick identity and SDL backend attribution

> **Reviewed corpus:** 2026-11-09. A source parser, compatibility shim or virtual-host acceptance does not establish native physical hardware fidelity.

**Registry:** [Linux joystick identity](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/linux-joystick-identity.json), a **host-interface research topic**, not a controller device.

## Why VID/PID and a displayed name are insufficient

Different Linux input paths can generate similarly identified app devices. A consumer may open `hidraw` and use a native SDL HIDAPI decoder, or consume `evdev` nodes that were already normalized by the kernel, `uinput` or an input compositor. The same name does **not** prove identical report semantics, sensor availability or ability to receive feature/output requests. See [`sdl-linux-backend-signatures`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sdl-linux-backend-signatures.json).

## Pinned SDL 3.2.0 backend-signature inference

The pinned structured SDL GUID includes a driver signature at byte **14**: HIDAPI uses `h` and the SDL Linux joystick path uses zero/signature data, with a native device path. Combining that with *the exact* `hidraw` or event device path and VID/PID supports a **conservative inference** of selected backend. It is not a universal detector: ambiguous names, incomplete GUIDs, user overrides, different SDL revisions and nonstandard devices remain unknown. [`sdl-linux-backend-signatures`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sdl-linux-backend-signatures.json).

## Recommended application-visible evidence

Capture:
- exact SDL version, backend driver, hints, GUID, vendor/product, bus and active source path;
- kernel-bound driver, HID interface/collection ancestry and evdev/hidraw sibling nodes;
- all digital/analog fields in neutral/isolated windows, sensor instance count and calibration;
- feature and output requests, permissions, simultaneous readers, close/removal and lifecycle.

For backend controls see external [SDL3 HIDAPI hint](https://wiki.libsdl.org/SDL3/SDL_HINT_JOYSTICK_HIDAPI) and [gamepad type override](https://wiki.libsdl.org/SDL3/SDL_HINT_GAMECONTROLLERTYPE). These are documentation references, **not evidence that a particular historical run set a hint**.

## Compare across controllers

The same distinction appears in [Xbox 360](../xbox360/consumers-and-compatibility.md), [DualSense](../dualsense/consumers-and-validation.md), [Steam Controller](../steam-controller-2026/modes-and-consumers.md), [Wii Remote](../wii-remote/consumers.md) and [GameCube adapter](../gamecube-usb-adapter/consumers-and-virtualization.md).
