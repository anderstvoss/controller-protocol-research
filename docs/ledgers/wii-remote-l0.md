# Wii Remote L0 source and consumer ledger

No physical experiment or device-side promotion. Seven pinned,hashed source files
(kernel core/modules/header/IDs, SDL Wii, Dolphin emulation and HIDAPI) support the
source_only consumer claims. Kernel/SDL/emulator behavior is never on its own
proof of a physical protocol,reference image or revision. No upstream excerpts.

## Revision boundary

| Revision | Record | Disposition |
| --- | --- | --- |
| Original RVL-CNT-01 | wii-original-remote-consumer-revision | Kernel Gen1 name policy only |
| Early integrated Plus/non-TR | wii-early-plus-revision-gap | Unknown discriminator/calibration; not collapsed into original or TR |
| RVL-CNT-01-TR | wii-tr-consumer-revision | Kernel Gen2/builtin-MP policy only |

## Protocol inventory

| Area | Records | Limit |
| --- | --- | --- |
| Bluetooth bus match | wii-kernel-bluetooth-match | Bus metadata only; no actual radio |
| Report IDs/modes | wii-kernel-report-modes; wii-sdl-extension-modes | Consumer dispatch, not observed firmware packets |
| Status/ACK flow | wii-kernel-status-ack-flow | Cadence/error behavior still requires a reference |
| Extension ID/init/encryption | wii-kernel-extension-init; wii-extension-encryption-gap | Consumer disable-encryption path is not all encrypted behavior |
| MotionPlus/pass-through | wii-kernel-motionplus-pass-through | External/integrated and downstream extensions remain distinct |
| IR modes | wii-kernel-ir-mode-policy | No image quality or physical point validation |
| LEDs/rumble/battery | wii-kernel-outputs-battery | LED/power-supply endpoints distinct from evdev axes |
| Memory | wii-dolphin-memory-routing; wii-memory-size-hypothesis | EEPROM/I2C separation;0x1700 is a hypothesis, not a frozen map |
| HIDAPI usability | wii-dolphin-hidapi-probe | Active status write; no host/radio acceptance |

## Pinned Linux consumer shape

All ranges below come from hid-wiimote-modules.c at the wii-linux-modules source
revision. Nodes remain separate; this table is the source-derived reference for
a future uinput oracle, not a fixture captured from hardware. Balance Board,
Wii U Pro and musical accessories are excluded from this base/extension table.

| Logical node | Advertised shape | Source lines |
| --- | --- | --- |
| Base keys | KEY_LEFT,KEY_RIGHT,KEY_UP,KEY_DOWN,KEY_NEXT,KEY_PREVIOUS,BTN_1,BTN_2,BTN_A,BTN_B,BTN_MODE |47-99|
| Base rumble | FF_RUMBLE on base input node, memless consumer path |112-164|
| Accelerometer | ABS_RX/RY/RZ -500..500,fuzz2,flat4 |498-506|
| IR | ABS_HAT0X/Y through ABS_HAT3X/Y; X0..1023,Y0..767,fuzz2,flat4 |750-768|
| Nunchuk | BTN_C,BTN_Z; HAT0X/Y -120..120; RX/RY/RZ -500..500,fuzz2,flat4 |809-818,945-966|
| Classic | Own key map; HAT1X/Y,HAT2X/Y,HAT3X/Y -30..30,fuzz1,flat1 |1239-1264|
| MotionPlus | ABS_RX/RY/RZ -16000..16000,fuzz4,flat8 |2814-2825|

These consumer units are not raw sensor units,canonical physical calibration or
a promised universal evdev mapping for every revision. The Wii package must
implement a golden shape from the pinned consumer source and validate actual
hid-wiimote binding on an eligible host. Source-only claims plus explicit unknown
device claims express the evidence boundary without a new claim-schema marker.
