# Xbox Elite Series 2 L0 — source-only starter ledger

Target: `xbox-elite-series-2` (post-Alpha 2, virtualgamepad #356). Branch `lane/post-alpha2/xbox-elite-series-2`. First candidate is **`linux.uinput` compatible with stock xpad Elite Series 2 evdev**, not GIP emulation. No physical hardware or host testing.

## Pinned revisions and reused corpus sources

| Lineage | Revision | Source records | Scope |
| --- | --- | --- | --- |
| Linux kernel | `4056b3c9d3c92ea45955641dbafeb9b960e146ef` | `xbox-series-linux-xpad`, `xbox-cgap-kernel-hid-ids`, `xbox-cgap-kernel-hid-microsoft`, `xbox-cgap-kernel-hid-generic` | Wired xpad identity, evdev, firmware-dependent paddle processing; Bluetooth HID matches |
| SDL | `d4557c1511c721485dc4960f7149730afc9a73a0` | Reuse `xbox-series-sdl-xboxone`; new `elite2-pa2-sdl-gamepad`, `elite2-pa2-sdl-linux-evdev` | HIDAPI wired/BT paddle parsing; generated/default Gamepad mapping; evdev paddle map |
| xpadneo (out of tree) | `56b538d951300bf804f6631738603c5eb14c04f0` | `xbox-cgap-xpadneo-core`, `xbox-cgap-xpadneo-events`, `xbox-cgap-xpadneo-device`, `xbox-cgap-xpadneo-header`, `xbox-cgap-xpadneo-elite-desc`, `xbox-cgap-xpadneo-rumble` | Optional Bluetooth HID consumer, conditional descriptor/auxiliary controls |

Each record carries immutable file URL, exact-file SHA-256 and lineage. GPL kernel and xpadneo source is paraphrased, not copied.

## New claims and evidence ceiling

| Claim ID | Status | Role | Transport | Limit |
| --- | --- | --- | --- | --- |
| `elite2-pa2-usb-xpad-identity` | `source_supported` | `consumer` | `usb` | xpad |
| `elite2-pa2-xpad-paddle-evdev` | `source_supported` | `consumer` | `usb` | xpad |
| `elite2-pa2-xpad-firmware-paddle-paths` | `source_supported` | `consumer` | `usb` | xpad |
| `elite2-pa2-xpad-profile-policy` | `source_supported` | `consumer` | `usb` | xpad |
| `elite2-pa2-bluetooth-hid-bind` | `source_supported` | `consumer` | `bluetooth` | hid-ids |
| `elite2-pa2-xpadneo-elite-bluetooth` | `source_supported` | `consumer` | `bluetooth` | xpadneo core |
| `elite2-pa2-sdl-hidapi-usb-paddles` | `source_supported` | `consumer` | `usb` | SDL_hidapi_xboxone |
| `elite2-pa2-sdl-hidapi-bt-paddles` | `source_supported` | `consumer` | `bluetooth` | SDL_hidapi_xboxone |
| `elite2-pa2-sdl-mappings` | `source_supported` | `consumer` | `source_only` | SDL_gamepad |
| `elite2-pa2-uinput-first` | `inferred` | `consumer` | `source_only` | Implementation proposal based on xpad and SDL mapping only; no host, hardware or consumer tests |
| `elite2-pa2-unknown-usb-device` | `unknown` | `device` | `usb` | Device-side gap: physical comparison at pinned firmware variants and USB GIP feasibility would be needed |
| `elite2-pa2-unknown-bluetooth-device` | `unknown` | `device` | `bluetooth` | Device and host-acceptance gaps for Elite models 0x0b05 and 0x0b22, including selected firmware revisions |
| `elite2-pa2-unknown-profile-outputs` | `unknown` | `device` | `not_measured` | Cross-transport and consumer-dependent limitations |

Existing `xbox-series-*`, `xbox-cgap-*` and `xbox-xone-*` claims remain authoritative for generic Series and shared consumer transport mechanisms. This ledger does not move Series claims to Elite by implication. The model 1797 source aliases are comparators; descriptors from other model families are not Elite evidence.

## Decision and test backlog

- First: `linux.uinput` with Elite-specific four grip keys, normal xpad axes, strict profile/remap limitations and caller-specified identity.
- Later: Bluetooth-bus `linux.uhid.bluetooth` only after version-specific descriptor, HID parsing, output/feature replies and SDL/xpadneo consumer acceptance are tested. UHID alone does not implement radio pairing.
- Blocked: pretending that USB uinput or USB HID implements wired Elite GIP; physical GIP protocol and receiver delivery are unmeasured.
- **Proposed tests, not run:** wired xpad and SDL across firmware/profile variants; isolated uinput event acceptance and lifecycle; optional xpadneo versus stock Bluetooth driver; UHID input/feature/output round trips; real-radio pairing as a separate exercise.

All new claims have empty experiment lists, and no device-level evidence has been promoted.
