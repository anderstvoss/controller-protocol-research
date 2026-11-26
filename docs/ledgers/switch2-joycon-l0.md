# Switch 2 Joy-Con L0 — source-only starter ledger

**Scope:** post-Alpha 2, [virtualgamepad #362](https://github.com/anderstvoss/virtualgamepad/issues/362). Each half has a separate registry entry under `switch2-joycon-family`; no hardware, Bluetooth, Linux host, virtual provider or Steam session was tested. Detailed decisions and pinned code citations are in [the starter brief](../switch2-joycon-starter.md).

| Gate | Source-derived evidence | Claim IDs | State |
| --- | --- | --- | --- |
| Identity | Linux and SDL define separate left `0x057e:0x2067` and right `0x057e:0x2066` USB products | `switch2jc-pa2-left-usb-identity`, `switch2jc-pa2-right-usb-identity` | Source supported; physical identity unknown |
| Individual unit | Linux USB HID matches and SDL driver per-side dispatch are separate; SDL provides a mapping for a consumer-side pair | `switch2jc-pa2-per-half-host-units` | Separate is first realization; physical combination not measured |
| Transport | Linux vendor configuration uses USB bulk with HID input, SDL uses libusb; pinned Switch 2 Bluetooth consumers unavailable | `switch2jc-pa2-usb-bulk-startup`, `switch2jc-pa2-bluetooth-consumer-gap` | USB source path only |
| Left/right evdev | Each half one signed stick, unique buttons; right adds C; conditional ordinary rumble | `switch2jc-pa2-left-evdev`, `switch2jc-pa2-right-evdev` | Consumer source only |
| Native reports | Report 0x07 left, 0x08 right, unified 0x05; per-side 12-bit stick and button offsets | `switch2jc-pa2-report-layout` | Linux decoder expectation only |
| SDL mapping and IMU | Horizontal mini/vertical modes; sensor outputs are decoded from USB input | `switch2jc-pa2-sdl-controls-and-modes`, `switch2jc-pa2-sdl-motion` | Consumer source only |
| Mouse | Linux exposes a flag but no mouse evdev, SDL joystick driver lacks mouse event decoding | `switch2jc-pa2-mouse-consumer-gap`, `switch2jc-pa2-mouse-device-unknown` | Physical behavior unknown |
| Fidelity | Playable per-half uinput, not native Switch 2; native USB requires new/extended composite provider | `switch2jc-pa2-first-realization`, `switch2jc-pa2-native-transport-unknown` | Proposed, not implemented |

## Provenance and boundaries

- Linux kernel `hid-nintendo.c`: `77c7155e2707ba5b1d56f3dc1acead48cf17f98d`, existing `switch2-gc-linux-hid`; configuration-interface `hid-nintendo-switch2-usb.c`: `9417132df63e5cd7230433af05198538e759f3ae`, existing `switch2-gc-linux-usb`. Both one Linux lineage; the source files were pinned at different commits, not a single tested kernel binary.
- SDL `SDL_hidapi_switch2.c`: `fe2bca9748afa754ebbca4c543c5b28bbce30cf4`, existing `sdl-switch2`. SDL `SDL_hidapi.c` at `d6fbbbe14dddfa09d6168267a0fcd39dea5a398a` remains existing `switch2-gc-sdl-libusb`. Those SDL pins are code references, not one tested SDL binary.
- New exact-file SHA-256 source records: `switch2jc-pa2-linux-hid-ids`, `switch2jc-pa2-sdl-usb-ids`, `switch2jc-pa2-sdl-gamepad`. Licences: kernel SPDX GPL-2.0-or-later and SDL zlib. No source code, firmware or physical captures redistributed.
- Source-only implementation claims refer to consumer behavior at the listed pins; no device claim is promoted to physical evidence. `unknown` retains retail USB, Bluetooth and mouse-sensor gaps explicitly.
- The registry addition does not assert virtualgamepad implementation or a tested SDL/Steam launch.

## Proposed tests, not run

1. Independently connect left and right over each supported physical bus; review topology and sanitize all resulting evidence.
2. Exercise a future USB composite/bulk provider through Linux `hid-nintendo` and SDL libusb; compare report routing, permissions and teardown.
3. Validate the first per-half `linux.uinput` baseline, including right C and side controls; separately report inability to satisfy native SDL HIDAPI.
4. Measure motion, mouse, rumble and Bluetooth pairing only after a valid test protocol and source specification exist.

**L0 gate:** Research recorded; host acceptance, native device protocol, Bluetooth, mouse fidelity and controller support remain open.
