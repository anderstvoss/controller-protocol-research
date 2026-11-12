# Xbox 360 consumer gaps 2 — xpad LED node and SDL backend selection

**Source-only result; no host, controller, Steam or Eden tests.** This is a pinned-kernel/SDL consumer audit, not a retail-device protocol claim. Tracking: [virtualgamepad #157](https://github.com/anderstvoss/virtualgamepad/issues/157).

## Ranked decisions

| Rank | Gap / prior record | Playable or faithful | Evidence ceiling and decision | New claim / issue |
| --- | --- | --- | --- | --- |
| 1 | `x360-l0-consumer-uhid-ff-led-unknown` | **Faithful LED surface** | **Source-supported negative:** the kernel xpadN LED registration is USB xpad's own optional class-device integration; neither uinput nor standard-HID UHID automatically obtains it. Actual LED/FF behavior on a running build remains unmeasured. | `x360-cgap-xpad-led-usb-binding`; #157 |
| 2 | `x360-l0-consumer-sdl-backend-selection-unmeasured` | **Playable SDL routing** | **Conditional source-supported default:** SDL 3.2.0 on Linux enables HIDAPI and recognizes 045e:028e as Xbox 360, so an accessible, successfully initialized UHID HIDAPI device can be claimed before evdev and sent to the Xbox 360 XUSB decoder. Evdev is available when HIDAPI does not claim it. **Actual host/app selection remains unknown.** | `x360-cgap-sdl-linux-hidapi-preemption-conditional`, `x360-cgap-sdl-linux-evdev-when-unclaimed`; #157 |

## Evidence and source reuse

All source links are immutable commits. Kernel source is GPL-2.0-or-later; no kernel code is reproduced. The SDL driver and headers use the embedded SDL zlib-style permissive notice. SDL's controller type and list files carry the embedded permissive Valve notice.

| Source record | Pinned file and locator | Relevance |
| --- | --- | --- |
| `xbox-series-linux-xpad` (reuse) | [Linux xpad.c](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/input/joystick/xpad.c) 477–503, 1641–1785, 1945–2052, 2320–2329 | USB interface matching, optional xpadN LED setup and cleanup |
| `x360-l0-sdl-hidapi-360-320` (reuse) | [SDL Xbox 360 HIDAPI](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_xbox360.c) 56–95, 243–338 | Hint inheritance, driver eligibility and XUSB-only packet parsing |
| `x360-l0-sdl-hidapi-routing` (reuse) | [SDL HIDAPI joystick dispatcher](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapijoystick.c) 213–350, 929–932, 1237–1285 | Type derived from VID/PID; discovered/active HIDAPI device ownership |
| `sdl-joystick-baseline` and `sdl-linux-joystick-baseline` (reuse) | [SDL joystick priority](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/SDL_joystick.c) 51–75, 680–700; [SDL Linux event backend](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/linux/SDL_sysjoystick.c) 277–341 | HIDAPI is higher priority; Linux evdev checks for another driver |
| `x360-cgap-sdl-hidapi-default-320` (new) | [HIDAPI configuration](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapijoystick_c.h) 51–60 | Linux default enabled |
| `x360-cgap-sdl-hint-defaults-320` (new) | [SDL hints](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/include/SDL3/SDL_hints.h) 1387–1402, 1825–1859 | Global, Xbox and Xbox 360 override hierarchy |
| `x360-cgap-sdl-controller-type-320` and `x360-cgap-sdl-controller-list-320` (new) | [Type lookup](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/controller_type.c) 52–120; [Xbox 360 table entry](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/controller_list.h) 171 | 045e:028e is classified Xbox 360 before report-level verification |

New source records contain SHA-256 of each entire cited file, not just these line ranges. Source files are **not** committed.

## Driver binding and LED-class registration

At the pinned kernel revision, `xpad` is a **USB interface driver**. Its Xbox 360 binding matches vendor-specific USB interface class/subclass/protocol and an allowed vendor, not an evdev or HID node whose PID happens to resemble a wired controller. Its input setup registers an `xpadN` LED class device only for the Xbox 360 type family, and only when `CONFIG_JOYSTICK_XPAD_LEDS` is built. For wired USB, that setup runs from USB probe; receiver slot handling is outside this session. Registration attaches to the USB device; teardown unregisters it. This is independent of optional force-feedback support.

An evdev device created using `uinput` and a HID device created using `UHID` are not USB-interface probes for this `xpad` path. Thus **a matching identity or FF_RUMBLE capability does not produce xpad's LED class**. This is a conclusion about the xpad registration mechanism, not a universal claim that no other software could expose an LED or that any hardware LED actually lit. Existing `x360-l0-consumer-xpad-led-class` remains corroborating source evidence; existing `x360-l0-consumer-uhid-ff-led-unknown` also contains distinct Steam/FF acceptance unknowns and is not wholly superseded.

## SDL Linux backend selection: default, fallback and uncertainty

Pinned SDL 3.2.0 makes HIDAPI the highest-priority joystick driver when built. `SDL_HIDAPI_DEFAULT` is true on Linux. The Xbox 360 HIDAPI driver checks first the Xbox 360-specific, then Xbox-wide, then global HIDAPI hint. Without overrides, it is enabled.

The controller classifier maps **045e:028e** to Xbox 360 by VID/PID, independently of the actual generic-HID descriptor. The HIDAPI Xbox 360 eligibility check accepts that classification unless another exclusion applies (including disqualifying interface number, wireless-receiver exception or unsupported usage). If the virtual device is discoverable and readable in HIDAPI and initialization succeeds, the Xbox 360 HIDAPI backend can claim it **before** the Linux event driver. This is a potential **wrong-parser identity collision**: HIDAPI's Xbox 360 consumer expects native XUSB reports, while virtualgamepad's standard-HID UHID is intentionally not XUSB. The default being enabled is **not** evidence of successful input parsing.

The Linux event driver checks whether a higher-priority driver already owns the equivalent device. If the Xbox 360 HIDAPI driver is disabled with `SDL_JOYSTICK_HIDAPI_XBOX_360=0`, or HIDAPI cannot enumerate/open/initialize an equivalent instance, the evdev path may handle the kernel event node. A gamepad database mapping is not proof of the owning backend.

**What the sources cannot decide:** whether a particular UHID node becomes accessible in an installed build, its exact reported interface/usage, whether SDL initialization succeeds, app-specific overrides, dynamic library/build version, and actual Steam/Eden/SDL backend output. Consequently `x360-l0-consumer-sdl-backend-selection-unmeasured` remains valid for observed runtime selection. No claims of measured Steam/Eden compatibility are made.

## Decisions for virtualgamepad

- **LED fidelity:** do not expect `xpadN` on generic uinput or standard-HID UHID, nor treat FF_RUMBLE as an LED API. If an LED surface is required, design and verify an explicit separate output realization rather than labeling generic HID as native XUSB.
- **Playable inputs:** a copied Xbox 360 VID/PID may trigger SDL's native XUSB HIDAPI parser despite a generic-HID report descriptor. Preserve the virtual realization's correct report schema; instrument backend selection before modifying identity or setting consumer-side override policy.
- **Scope:** the wired consumer code is not a physical reference capture; wireless receiver behavior is assigned elsewhere. Existing physical validation #281 and #282 is unaffected.

## Proposed host tests — all **not run**

| Gate | Proposed procedure | Decision evidence (no sensitive identifiers) |
| --- | --- | --- |
| LED-L1 | On an authorized Linux host, compare a standard-HID UHID controller and an evdev uinput controller with 045e:028e identity; inspect each kernel driver binding and whether any `xpadN` LED-class node belongs to that virtual device; record kernel config. | Confirm xpad does not bind to either virtual creation route; distinguish separate unrelated LEDs. No controller hardware needed. |
| SDL-S1 | On a pinned SDL 3.2.0 build, create a neutral UHID standard-HID 045e:028e and record HIDAPI discovery, class/interface/usage, selected SDL joystick path and GUID, backend initialization and input decode. | Distinguish HIDAPI eligible, HIDAPI successfully claimed, event backend claimed, or neither. Never infer a selected decoder from VID/PID or mapping alone. |
| SDL-S2 | Repeat SDL-S1 with `SDL_JOYSTICK_HIDAPI_XBOX_360=0` set before SDL initializes. Compare default and override evdev mappings and error paths; capture only non-identifying capability summaries. | Verify fallback in that build, plus controls and conventional rumble separately. Keep Steam and Eden as separately instrumented future consumers. |

No host or hardware experiments were performed in this cloud session. These are conditional source results, not an acceptance-status promotion.
