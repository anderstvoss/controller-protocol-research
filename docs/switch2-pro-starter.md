# Switch 2 Pro Controller — post-Alpha 2 starter research

**Tracking:** [virtualgamepad #171](https://github.com/anderstvoss/virtualgamepad/issues/171) · **registry:** `switch2-pro` · **boundary:** source-only, no host or controller hardware tests.

## Decision table

| Question | Finding at pinned revisions | Decision / evidence limit |
| --- | --- | --- |
| USB identity | Nintendo **0x057e:0x2069** at Linux **v7.4-rc2** ([IDs](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-ids.h#L1120-L1133)). | Kernel match is source evidence, **not** a captured retail USB descriptor. Original Switch Pro is a different identity and protocol. |
| Linux driver and evdev | `hid-nintendo` USB HID **and** `hid-nintendo-switch2-usb` vendor-class bulk configuration ([HID](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo.c#L4336-L4348), [USB](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo-switch2-usb.c#L471-L489)); Pro declares four signed stick axes, D-pad hats, `BTN_GRIPR`, `BTN_GRIPL`, `BTN_C` and `KEY_RECORD` ([evdev](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo.c#L3246-L3265), [axes](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo.c#L3639-L3668)). | Concrete **source-declared evdev shape**, not recorded events. `FF_RUMBLE` is build-conditional; LEDs declared. |
| Linux native reports | Pro report **0x09** or unified **0x05**, with separate GR/GL/C, buttons and packed stick fields ([handler](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo.c#L3933-L4036)). | Not Switch 1 report **0x30**. Physical packet parity unknown. |
| SDL driver and mapping | Pinned [Switch 2 HIDAPI driver](https://github.com/libsdl-org/SDL/blob/fe2bca9748afa754ebbca4c543c5b28bbce30cf4/src/joystick/hidapi/SDL_hidapi_switch2.c#L944-L1029) decodes Share, C, GR and GL into separate joystick slots plus sticks/triggers; [SDL libusb list](https://github.com/libsdl-org/SDL/blob/d6fbbbe14dddfa09d6168267a0fcd39dea5a398a/src/hidapi/SDL_hidapi.c#L774-L800) includes Switch 2 Pro. | Requires direct USB bulk interface access for setup; SDL native joystick fields are **not** proof of standardized Gamepad mapping in other builds. |
| SDL / Linux open | SDL claims interface 1 bulk IN/OUT dynamically ([USB open](https://github.com/libsdl-org/SDL/blob/fe2bca9748afa754ebbca4c543c5b28bbce30cf4/src/joystick/hidapi/SDL_hidapi_switch2.c#L329-L390)); Linux discovers bulk endpoints and attaches the configuration interface to HID ([USB bind](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo-switch2-usb.c#L340-L445)). | HID handles input and rumble; **vendor-class bulk** handles config/commands. UHID provides neither a composite USB device nor bulk endpoints. |
| Differences from Switch Pro (Switch 1) | A separate USB product ID, report format, setup/feature commands, grip/C controls and rumble framing ([new HID](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo.c#L2893-L3052), [older SDL](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_switch.c)). | Do not reuse the Switch 1 HID personality based on physical resemblance. |
| First realization | **`linux.uinput`, playable evdev parity first**, using exact kernel control codes/axes and honest output limits. | Source-grounded implementation choice, **not** a tested Switch 2 HIDAPI/SDL path or full native identity. |
| Faithful native USB | Candidate: extended experimental **`linux.dummy_hcd.usb-hid`** or **USB/IP** offering *both* a USB HID interface and vendor-specific bulk configuration endpoints, command/reply state and HID output. | Existing virtualgamepad dummy_hcd is unavailable and its USB/IP mechanism is WIP. Neither is demonstrated for this Pro. No UHID-only native solution is evidenced. |
| Bluetooth / HID-only path | Linux [Kconfig](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/Kconfig#L857-L894) scopes Switch 2 support to USB and the Pro match is USB only; pinned SDL [rejects Bluetooth init](https://github.com/libsdl-org/SDL/blob/fe2bca9748afa754ebbca4c543c5b28bbce30cf4/src/joystick/hidapi/SDL_hidapi_switch2.c#L323-L327). | Actual retail Bluetooth operation, custom BlueZ bridge, HID-only subset and console pairing are **unknown**. |
| Open unknowns | Firmware/mode, full descriptors, startup ACKs, independent actuator/IMU and power semantics, physical GR/GL/C and SDL/raw/evdev agreement. | Remain device/host unknown until qualified controlled experiments. |

## USB protocol and realization boundary

At Linux `v7.4-rc2`, the kernel driver handles input and HD-rumble-like output on the HID transport. A **separate configuration interface** is matched as vendor class with bulk IN/OUT endpoints, connected to the controller instance by USB topology; an eight-byte request header frames the bulk commands. Kernel startup obtains firmware information, calibration, enables features and selects Pro report `0x09` ([startup](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo.c#L4090-L4172), [bulk command](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo-switch2-usb.c#L155-L205)). SDL independently uses libusb for analogous staged setup, then reads 64-byte input reports through HIDAPI ([startup](https://github.com/libsdl-org/SDL/blob/fe2bca9748afa754ebbca4c543c5b28bbce30cf4/src/joystick/hidapi/SDL_hidapi_switch2.c#L392-L506), [read loop](https://github.com/libsdl-org/SDL/blob/fe2bca9748afa754ebbca4c543c5b28bbce30cf4/src/joystick/hidapi/SDL_hidapi_switch2.c#L1246-L1282)). The two implementation lineages support the same *architecture*, not independent proof of physical compliance.

For Linux evdev consumers, an explicit `linux.uinput` presentation can plausibly support base controls plus separate grip/C keys without pretending to pass Switch 2 protocol initialization. It may lack native SDL Switch 2 recognition, sensor access and faithful actuator reports. A `linux.uhid.usb` or `linux.uhid.bluetooth` session cannot create the bulk configuration interface. In particular, the pinned Linux Pro probe requires a real USB HID device and pairs it with the USB configuration driver. A full native virtual USB device should instead be prototyped through an extended composite USB gadget path (`dummy_hcd`) or USB/IP with HID + vendor bulk; **these are candidates, not present validated providers**.

The SDL decoder uses a Pro-specific joystick button count and slots for Share/C/grips, not the original Switch Pro set ([button setup](https://github.com/libsdl-org/SDL/blob/fe2bca9748afa754ebbca4c543c5b28bbce30cf4/src/joystick/hidapi/SDL_hidapi_switch2.c#L44-L50), [open](https://github.com/libsdl-org/SDL/blob/fe2bca9748afa754ebbca4c543c5b28bbce30cf4/src/joystick/hidapi/SDL_hidapi_switch2.c#L579-L612), [decoder](https://github.com/libsdl-org/SDL/blob/fe2bca9748afa754ebbca4c543c5b28bbce30cf4/src/joystick/hidapi/SDL_hidapi_switch2.c#L944-L1029)). Linux Pro maps the selected retail-looking bits to `KEY_RECORD`, `BTN_C`, `BTN_GRIPR` and `BTN_GRIPL`. Whether SDL Share and Linux Capture represent identical physical behavior requires validation; do not silently alias them. Pro rumble uses two encoded actuator positions with output command `0x02` in SDL, while Linux sends a two-slot rumble output report using its conventional evdev force-feedback interface ([SDL](https://github.com/libsdl-org/SDL/blob/fe2bca9748afa754ebbca4c543c5b28bbce30cf4/src/joystick/hidapi/SDL_hidapi_switch2.c#L1040-L1110), [Linux](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo.c#L3410-L3515)). No independent physical output fidelity is established.

## Source ledger

| Source record | Revision | Lineage and role |
| --- | --- | --- |
| [`switch2-pa2-linux-hid-v74rc2`](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo.c) | `v7.4-rc2` | Linux HID/evdev; Linux, GPL-2.0 family |
| [`switch2-pa2-linux-usb-v74rc2`](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-nintendo-switch2-usb.c) | `v7.4-rc2` | Linux USB bulk; Linux, GPL-2.0 family |
| [`switch2-pa2-linux-ids-v74rc2`](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/hid-ids.h) | `v7.4-rc2` | Linux identity; Linux, GPL-2.0 family |
| [`switch2-pa2-linux-kconfig-v74rc2`](https://github.com/torvalds/linux/blob/v7.4-rc2/drivers/hid/Kconfig) | `v7.4-rc2` | Linux Kconfig; Linux, GPL-2.0 family |
| [`sdl-switch2`](https://github.com/libsdl-org/SDL/blob/fe2bca9748afa754ebbca4c543c5b28bbce30cf4/src/joystick/hidapi/SDL_hidapi_switch2.c) | `fe2bca9748afa754ebbca4c543c5b28bbce30cf4` | SDL Switch 2; SDL, zlib |
| [`switch2-gc-sdl-libusb`](https://github.com/libsdl-org/SDL/blob/d6fbbbe14dddfa09d6168267a0fcd39dea5a398a/src/hidapi/SDL_hidapi.c) | `d6fbbbe14dddfa09d6168267a0fcd39dea5a398a` | SDL libusb gate; SDL, zlib |
| [`audio-sdl-switch-pro`](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_switch.c) | `535d80badefc83c5c527ec5748f2a20d6a9310fe` | SDL original Switch Pro; SDL, zlib |

Linux entries are **one upstream lineage** at the exact tagged snapshot. Reused `sdl-switch2` and `switch2-gc-sdl-libusb` records refer to two **different pinned SDL commits**, so the combined SDL interpretation must not be presented as one measured build. Each new Linux source record hashes the full pinned file; no source code or private capture is copied.

### Claims introduced

- `switch2-pa2-usb-split-interfaces` — **source_supported**, consumer; Pinned Linux USB/HID enumeration and configuration
- `switch2-pa2-pro-identity` — **source_supported**, consumer; Kernel USB matching and source identity
- `switch2-pa2-linux-evdev-gr-gl-c` — **source_supported**, consumer; Linux declared evdev capability shape
- `switch2-pa2-linux-report09` — **source_supported**, consumer; Linux Pro and unified input decoder
- `switch2-pa2-linux-init` — **source_supported**, consumer; Linux startup and firmware/calibration negotiation
- `switch2-pa2-linux-rumble` — **source_supported**, consumer; Linux Pro rumble output consumer
- `switch2-pa2-sdl-usb-libusb` — **source_supported**, consumer; SDL USB discovery and configuration transport
- `switch2-pa2-sdl-pro-mapping` — **source_supported**, consumer; SDL Pro input and controls
- `switch2-pa2-sdl-init-rumble` — **source_supported**, consumer; SDL staged USB setup and Pro output
- `switch2-pa2-bluetooth-consumer` — **source_supported**, consumer; Inspected Linux and SDL Bluetooth support boundary
- `switch2-pa2-switch1-distinct` — **inferred**, consumer; Non-substitutability with original Switch Pro
- `switch2-pa2-uinput-first` — **inferred**, consumer; Recommended initial virtualgamepad realization
- `switch2-pa2-retail-device-unknown` — **unknown**, device; Retail USB descriptor, firmware and transport applicability
- `switch2-pa2-hid-only-unknown` — **unknown**, consumer; HID-only fallback and virtual host binding
- `switch2-pa2-actual-host-observation-unknown` — **unknown**, consumer; Measured Linux evdev/SDL outputs

**Existing corpus:** `switch2-independent-raw` and `switch2-sdl-decoder` already establish source-level GR/GL, `switch2-gc-*` describes sibling USB bulk conventions; this PR adds Pro-specific Linux/SDL evidence. `switch2-linux-exposure-unknown` is **partially resolved at the consumer source-code level**, but its unmeasured *host event observation* remains true and is not superseded. `switch2-physical-corroboration-unknown` also remains open. There are no new source-supported **device** claims; the existing controller-registry evidence-category test stays correct.

## Playable versus faithful

**Playable candidate:** `linux.uinput`, with four calibrated stick axes, hat, digital triggers, dedicated GR/GL/C where the consuming app accepts their event codes, and conventional FF where supported. Caller-specified identity must be supported at creation but may not cause a native Switch 2 driver to bind. Treat IMU, native HD rumble, USB command handling and physical Bluetooth pairing as unavailable in this reduced target until implemented and qualified.

**Faithful target (not presently realized):** virtual composite USB with correct interface descriptors, bulk IN/OUT request replies, Pro HID reports, per-actuator output, calibration/state transitions and lifecycle. Do not label a USB-bus UHID as faithful or assume a HID-only fallback. The exact physical firmware/packet truth remains unknown; hardware capture would be needed. Do not analyze vendor firmware in the public corpus; any gap requiring that work **needs private analysis**.

## Proposed tests, not run

1. Select a retail model and firmware; collect non-identifying USB interface/class/endpoint topology and probe kernel module binding, preserving raw private identifiers outside the public corpus.
2. Compare real Linux evdev capability advertisements and transitions, including concurrent GR/GL/C, Report `0x09`, stick values, hat, LEDs and conventional force feedback.
3. Compare pinned SDL raw joystick buttons/axes/sensors and standardized Gamepad mapping, with libusb grants versus kernel driver contention; distinguish SDL 3.2.0 from newer source.
4. Probe read-only startup requests and response/error timing, reconnect, report selection and output/IMU behavior without publishing private data.
5. Prototype `linux.uinput` for playable baseline; separately gate a USB composite `dummy_hcd` or USB/IP experiment on bulk endpoints, accurate replies, unsupported operations and teardown. Never call either faithful based only on a static descriptor.
6. Check whether HID-only presentation ever gets a usable consumer without bulk setup; test Bluetooth in a separate owner-controlled campaign without inferring physical pairing from bus metadata.

**All tests above are proposed only; no local host, virtual-host or physical controller testing was performed.**
