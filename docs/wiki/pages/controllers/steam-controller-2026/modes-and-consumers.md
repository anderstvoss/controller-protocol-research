# Steam Controller 2026 — lizard, kernel, SDL and Steam

[← Controller overview](index.md) · [Protocol](protocol.md)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

There is **not one three-state switch** between lizard, kernel gamepad and Steam Input. The relevant state is a product of: firmware desktop mapping, native HID packet emission, kernel `hid-steam` mapping, layered raw-client ownership, SDL backend and Steam client activation. These may change independently.

## Firmware and lizard mode

In source inspection, feature setting key **9** toggles lizard state; kernel also uses digital-mapping commands `0x81`/`0x85`, settings reset `0x8e` and watchdog setting key **71**. Current replacement-firmware policy is not a retail timing measurement. D9 wired captures directly show lizard `0x40` mouse and `0x41` keyboard reports and mappings ([`steam-d9-lizard-control-mapping`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-lizard-control-mapping.json)).

## Kernel `hid-steam`: representation is conditional

At the pinned v7.3-rc1 driver, IBEX native controls and sensor events may be suppressed when `gamepad_mode` is not selected; Menu long-hold schedules a nominal kernel-side ~450-ms toggle. The kernel's `client_hdev` raw-client opening causes asynchronous evdev/sensor unregistering in its selected path. Opening an IBEX evdev gamepad FD does *not* automatically implement the legacy Steam Controller lizard SET behavior. These are fixed-version **consumer-source** observations, not universal firmware guarantees: [`steam-c6-kernel-menu-hold-450ms`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-c6-kernel-menu-hold-450ms.json), [`steam-c6-kernel-client-raw-forward`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-c6-kernel-client-raw-forward.json), [`steam-c6-kernel-ibex-evdev-open-close`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-c6-kernel-ibex-evdev-open-close.json).

## SDL HIDAPI Triton

The pinned SDL driver can select `28de:1302` directly, disable lizard periodically and expose native gamepad, touchpads and IMU via SDL APIs. It need not perform Linux's exact serial/version probe sequence. If a raw SDL client and the kernel evdev client both appear, test whether they actually coexist or one path was torn down. See [`steam-c6-disagreement-open-sdl`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-c6-disagreement-open-sdl.json) versus [`steam-c6-disagreement-open-kernel`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-c6-disagreement-open-kernel.json).

## Steam Input

An application-visible Steam virtual controller is **not necessarily** the physical `1302` node, and a Steam process being present is not itself proof of managed input activation. The D9 Steam Ping, SDL and lizard transition trials have separate validity limits: [`steam-d9-steam-ping-script`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-steam-ping-script.json) and [`steam-d9-lizard-sdl-transition`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-lizard-sdl-transition.json). Do not assert proprietary internal Steam policy from kernel source inspection alone.

## Mode and ownership experiment

For each session record: Steam process state, gamepad fd ownership, SDL backend/driver and hints, kernel bound driver, native packet stream, desktop `0x40/0x41`, registered evdev/hidraw nodes, settings writes, re-registration latency and final cleanup. Separate the **stock wired** path from Puck loss/reconnect restoration experiments. The long source-backed discussion is in [mode analysis](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-controller-modes.md) and [follow-up contrasts](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-controller-modes-followup.md).
