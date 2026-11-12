# GameCube USB adapter — L0 follow-up ledger (source only)

**Research label:** GameCube USB research, prep for #296. **Tracking:** `anderstvoss/virtualgamepad#296`. **Hardware:** no WUP-028 and no original GameCube controller. No host tests or physical captures.

The following supplements (does not replace or edit) the 13 `gc-adapter-*` records merged in #93. Their identities, 0x13/0x21/0x11 messages, 0x04/0x10/0x20 status bits and SDL/Dolphin libusb-only paths remain the baseline.

| New claim | Source lineage | Exact source line intervals | Confidence and limit |
| --- | --- | --- | --- |
| `gc-adapter-toadking-four-uinput-pads` | ToadKing | 126–220, 329–346 | Source supported bridge, not device truth |
| `gc-adapter-toadking-evdev-range` | ToadKing | 40–65, 149–173, 378–392 | Raw 0–255 or narrower limits, Y inverted |
| `gc-adapter-toadking-rumble-power` | ToadKing | 329–346, 497–526 | 0x04 power and 0/1 outputs |
| `gc-adapter-hinara-kernel-evdev` | Hinara | 109–128, 175–246, 340–410 | URB bInterval from descriptor, not observed constant |
| `gc-adapter-eden-direct-libusb` | Eden/yuzu lineage | 230–328, 351–381 | Direct libusb, not evdev |
| `gc-adapter-cemu-direct-libusb` | Cemu | 163–253, 257–305, 309–344 | Direct libusb, not evdev |
| `gc-adapter-dolphin-android-usbmanager` | Dolphin | 48–62, 87–115, 122–164 | Android permission prompt, not Linux libusb |
| `gc-adapter-toadking-external-sdl-map` | ToadKing | SDL_GameController.txt 1–17 | Explicit external config; built-in mapping **No evidence** |
| `gc-adapter-remaining-status-unknown` | None | — | Unknown status bits and firmware-specific meaning |
| `gc-adapter-descriptor-details-unconfirmed` | None | — | Unknown actual descriptors, interval and strings |

## Lineage policy

- ToadKing and its downstream forks count as one lineage for independence. Hinara is a different kernel implementation but may have reused public constants. Cemu, Eden and Dolphin may share historical code. Source counts alone do not justify promotion without a provenance comparison.
- `gc-adapter-port-power-bit` currently cites SDL alone. The ToadKing daemon independently **reads** 0x04; do **not** edit the original claim or assert a physical power-cable signal was measured.
- No source inspected defines new status-bit meanings; do not claim USB descriptor facts from constants in clients. Hinara uses the endpoint's *read* `bInterval`, so it does not establish its value.
- New consumer/source evidence must remain `source_only`, `experiments: []` and `evidence_role: consumer` where appropriate. Actual adapter descriptors, soundness of value 2 brake and peripheral response remain unknown.

## Previous records referenced without changes

`gc-adapter-usb-identity`, `gc-adapter-init-command`, `gc-adapter-input-report-layout`, `gc-adapter-port-type-bits`, `gc-adapter-port-power-bit`, `gc-adapter-button-bits`, `gc-adapter-rumble-output`, `gc-adapter-rumble-brake-value`, `gc-adapter-set-protocol-kick`, `gc-adapter-consumer-neutral-calibration`, `gc-adapter-consumers-require-usb-device`, `gc-adapter-linux-no-specific-driver`, `gc-adapter-descriptors-unknown`.

**Cloud agent (GameCube USB research)**

## Controller gaps round 2 — published descriptors and status consumers (2026-11-11)

Source-only; **no hardware, host or controller run**. This section appends evidence and does not revise existing `gc-adapter-*` records. Brief: [gamecube-usb-adapter-gaps-2.md](../gamecube-usb-adapter-gaps-2.md).

| Claim | Role / source status | Pinned evidence | Remaining boundary |
| --- | --- | --- | --- |
| `gc-cgap-published-usb-interface` | Device / source-supported | Linuxhw EP0 8 and EP0 64 archived `lsusb` entries | Authenticity and all device versions not validated |
| `gc-cgap-published-interrupt-endpoints` | Device / source-supported | Two dumps, IN 0x81 37 bytes, OUT 0x02 5 bytes, bInterval 8 | Host poll delivery and timing unmeasured |
| `gc-cgap-control-endpoint-packet-size-variance` | Device / source-supported discrepancy | Public dumps report bMaxPacketSize0 8 versus 64 | Do not force a universal value |
| `gc-cgap-emulated-hid-descriptor-model` | Consumer / source-supported | HIDMaestro pinned USB/IP persona | 214-byte advertised descriptor length is published; exact physical descriptor contents not verified |
| `gc-cgap-hid-report-length-tension` | Consumer / inferred | HIDMaestro HID report ID 0x21 field declaration | Descriptor versus transfer-length interpretation, not tested |
| `gc-cgap-wavebird-status-consumer-divergence` | Consumer / source-supported | Nintendont, RetroArch, HIDMaestro | 0x22 / 0x20 remain consumer policy until hardware checks |

The two archived device logs share the linuxhw collection lineage, and downstream compatibility implementations can reuse community constants. Independent physical corroboration is **not claimed**. The established `gc-adapter-descriptors-unknown`, `gc-adapter-descriptor-details-unconfirmed` and `gc-adapter-remaining-status-unknown` records are preserved rather than superseded; their exact-device and runtime ceilings remain open. Physical checks listed in the brief are **not run**.
