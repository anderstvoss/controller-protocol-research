# Switch 2 GameCube Controller — source-only USB consumer survey

**GameCube USB research, prep for #296** · `057e:2073` · registry ID `switch2-gamecube` · **no hardware or host tests performed**. Physically available for a later owner-operated bounded capture, not part of this submission.

## Shared family versus GameCube-specific differences

`switch2-pro` and `switch2-gamecube` are sibling registry controllers (`parent: null`), not parent/child. They share the host-command family, but Switch 2 GameCube has its own 0x0a report, analog triggers and separate travel/click controls, and **simple rather than HD rumble**. Reuse `switch2-sdl-decoder` and `switch2-independent-raw` for general Switch 2 SDL report-decoder context only: Pro paddle bits do not prove GameCube fields. `switch2-linux-exposure-unknown` remains a separate Pro physical-host unknown, not a claim about GC.

| Question | SDL (existing `sdl-switch2` plus new libusb pin) | Linux (new source pins) | Limit |
| --- | --- | --- | --- |
| USB discovery | Requires libusb, direct Nintendo ID 057e:2073; `SDL_hidapi_switch2.c` 310–318 and `SDL_hidapi.c` 774–800 | Vendor-specific USB matching `hid-nintendo-switch2-usb.c` 471–489; hid-nintendo GC device match 4470–4479 | Consumer source; no device descriptor capture |
| USB endpoints | Looks for **bulk** IN/OUT under interface **1**, discovers endpoint numbers at runtime; SDL 329–390 | Finds bulk IN/OUT dynamically in bound interface; two IN and four OUT URB slots, buffer length 64; 17–20 and 340–422 | Endpoint numbers and bInterval **No evidence** |
| Init and protocol | Raw libusb staged writes, feature selection, report-format and flash/calibration reads; SDL 392–500 | Header-framed command/reply path and staged firmware/flash/feature/rumbler/report selection; Linux USB 155–205, HID 4100–4185 | Physical ACK and revision-specific side effects **No evidence** |
| GC input | C at `data[6]` bit 0x40, analog L/R at bytes 61 and 62 in SDL internal unified packet; full-travel clicks separate; SDL 684–760 | GC report 0x0a: button bytes, two sticks and separate trigger bytes; unified report 0x05 supported; HID 3969–3983, 4009–4023 | Consumer decoders are not captures |
| Evdev/SDL axes | Joystick axes in SDL conventions and GameCube-specific native button enumeration; SDL 66–74, 584–590, 684–760 | Four signed stick axes, two triggers 0..4095, hats and FF; HID 3629–3669 | Physical calibration unknown; different consumers rescale |
| Rumble | GameCube branch emits 0x03 and simple on/off/duty-cycle values; SDL 1040–1073 | GC branch simple 0x03, other controllers HD rumble; HID 3419–3490 | Device response and intensity **not measured** |
| Identity and controller type | Specific PID branch and trigger calibration flash reads; SDL 310–318, 474–481 | Firmware info selects GC controller type, factory/user calibration, serial-related input metadata; HID 3760–3810, 4256–4265, 4372–4385 | No actual identifying values in this corpus |
| LEDs | GameCube-specific LED behavior in SDL: **No evidence** | Player LED programming in hid-nintendo 3531–3557, 3680–3727 | Whether a physical indicator follows it: **No evidence** |
| Permissions | Direct libusb requires USB device-node access, not just hidraw. Valve public USB uaccess rule line 248 includes 057e:2073 | Kernel driver binds USB/HID interfaces and presents evdev; optional hidraw access subject to host ACL | Detach, concurrent access and runtime grants: **not run** |

## Source and lineage references

- SDL driver `sdl-switch2`, pinned `fe2bca9748afa754ebbca4c543c5b28bbce30cf4` with SHA-256 in corpus; new `switch2-gc-sdl-libusb` for explicit libusb selection.
- Linux `switch2-gc-linux-usb` and `switch2-gc-linux-hid` are the **same Linux lineage**; never count as two independent confirmations. SDL versus Linux provides separate consumer implementation lineages.
- Pre-existing `steam-client-udev-60-steam-input` line 248 establishes a permission rule **only**; does not prove Steam Input's 0x2073 handling.
- All proposed host validation (SDL/libusb discovery, kernel binding, state, rumble, LEDs and source-identity collisions) is **not run**.

**Cloud agent (GameCube USB research)**
