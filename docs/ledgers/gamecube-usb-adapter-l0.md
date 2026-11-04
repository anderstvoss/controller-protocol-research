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
