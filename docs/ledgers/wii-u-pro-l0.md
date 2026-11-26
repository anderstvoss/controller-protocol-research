# Wii U Pro L0 — pinned starter ledger

**Tracking:** `anderstvoss/virtualgamepad#361` · **controller:** `wii-u-pro` · **status:** source-only; no host or physical tests.

| Area | Claim IDs | Source basis | Gate |
| --- | --- | --- | --- |
| Bluetooth selection and identity classifier | `wiiupro-pa2-kernel-bluetooth-match`, `wiiupro-pa2-kernel-pro-classification` | Linux v6.12 hid-wiimote core/IDs | Physical SDP/VID/PID not established |
| Pro report and evdev layout | `wiiupro-pa2-kernel-pro-mode`, `wiiupro-pa2-kernel-pro-input` | Linux v6.12 core/modules | No bound UHID or input ioctl proof |
| Sticks and calibration | `wiiupro-pa2-kernel-pro-stick-calibration` | Linux v6.12 modules | Retail neutral/EEPROM unmeasured |
| LED, rumble and battery | `wiiupro-pa2-kernel-pro-output-power` | Linux v6.12 core/modules | No physical effect or timing |
| SDL detection and mapping | `wiiupro-pa2-sdl-pro-detection`, `wiiupro-pa2-sdl-pro-report`, `wiiupro-pa2-sdl-pro-mapping`, `wiiupro-pa2-sdl-pro-power` | SDL Wii HIDAPI 877399b2 | No SDL host run |
| Cemu native Wiimote filtering | `wiiupro-pa2-cemu-native-pro-exclusion` | Cemu 29f2f1fa | Generic input is a separate unknown |
| Architecture decisions | `wiiupro-pa2-separate-family-shared-code`, `wiiupro-pa2-first-uhid-bluetooth` | Pinned Linux/SDL interpretation | Inferred; subject to host acceptance |
| Device identity and calibration gaps | `wiiupro-pa2-physical-identity-gap`, `wiiupro-pa2-physical-calibration-gap` | Source boundaries | Hardware study required; never import identifying data |
| Consumer and implementation acceptance gap | `wiiupro-pa2-virtual-acceptance-gap` | Linux/SDL/Cemu sources | No accepted support cells |

## Revision and provenance

Linux sources: [core](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-core.c#L809-L855), [Pro module](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-modules.c#L1572-L1966), [IDs](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-ids.h#L985-L987). SDL: [Wii HIDAPI](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L182-L190). Cemu: [native HIDAPI](https://github.com/cemu-project/Cemu/blob/29f2f1fae4631e2317977debd9eacd55cc28dd7d/src/input/api/Wiimote/hidapi/HidapiWiimote.cpp#L28-L48). Source record IDs: `wii-gap-dolphin-attach-kernel-core-v612`, `wii-gap-dolphin-attach-kernel-modules-v612`, `wiiupro-pa2-linux-hid-ids-v612`, `wiiupro-pa2-sdl-wii-877399b2`, `wii-gap-consumer-cemu-hidapi`. Linux GPL-2.0-or-later; SDL zlib; Cemu MPL-2.0. All external URLs pin revisions. No GPL excerpts reproduced.

The Wii Remote L0 ledger excludes Wii U Pro and is not modified. Prefix `wiiupro-pa2-` avoids the `wii-` count in `tests/test_wii_ledger.py`; no count or test assertion is changed. No claim of actual Bluetooth radio pairing follows from `linux.uhid.bluetooth`.

## Proposed tests — not run

Verify Pro classifier and `0x3d` report under Bluetooth-bus UHID, native 17-key/four-axis evdev and force feedback, SDL 15-button/six-axis mapping, battery/LED behavior, two-instance isolation, cleanup and errors. Treat real wireless pairing and physical equivalence as separate prerequisites. Inspect Dolphin and Cemu generic-gamepad paths before making affirmative emulator claims.
