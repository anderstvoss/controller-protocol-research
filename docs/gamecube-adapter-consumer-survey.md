# GameCube USB adapter: source and consumer survey

**Source-only.** No physical adapter, host run or capture is recorded. Tracking:
anderstvoss/virtualgamepad#296. Registry ID: `gamecube-usb-adapter`
(Nintendo WUP-028, the Wii U / Switch GameCube controller adapter).

Pinned sources (URL, revision and SHA-256 in `records/source/`):
SDL HIDAPI GameCube driver, SDL `usb_ids.h`, SDL `SDL_hidapi.c` libusb
selection, Dolphin `InputCommon/GCAdapter.cpp`, Linux `hid-ids.h` and
`hid-quirks.c`. All are cited and restated; no code is excerpted.

## Device protocol as both consumers read it

| Function | What the sources say | Claim | Status |
| --- | --- | --- | --- |
| Identity | USB 057e:0337 | `gc-adapter-usb-identity` | corroborated (SDL, Dolphin) |
| Initialisation | host writes 0x13 on interrupt OUT | `gc-adapter-init-command` | corroborated |
| Input report | 37 bytes: 0x21 + 4 × 9-byte port blocks | `gc-adapter-input-report-layout` | corroborated |
| Port presence and type | status 0x10 wired, 0x20 WaveBird | `gc-adapter-port-type-bits` | corroborated |
| Rumble power | status 0x04 = second USB cable | `gc-adapter-port-power-bit` | SDL only |
| Buttons | A B X Y, D-pad, Start, Z, L/R digital | `gc-adapter-button-bits` | corroborated |
| Rumble | 0x11 + one byte per port (0 stop, 1 run) | `gc-adapter-rumble-output` | corroborated |
| Rumble brake | value 2 hard stop | `gc-adapter-rumble-brake-value` | SDL only |
| Descriptors | USB/HID descriptors, polling interval, strings | `gc-adapter-descriptors-unknown` | unknown |

## Consumer findings that shape realization choice

1. **Both native consumer paths need a USB-level device**
   (`gc-adapter-consumers-require-usb-device`). SDL lists 057e:0337 as
   libusb-required and ignores it on hidraw; Dolphin uses libusb hotplug and
   detaches the kernel driver. A `linux.uhid.usb` device with the native
   identity would not be opened by either adapter path. Reaching them needs
   a USB-level realization (dummy_hcd, USB/IP), which virtualgamepad currently
   treats as experimental. A `linux.uinput` realization reaches consumers only
   as four ordinary evdev pads, without native adapter semantics.
2. **Host requests to accept**: SET_PROTOCOL (class request 11, wValue 1) at
   open (`gc-adapter-set-protocol-kick`), the 0x13 init and 0x11 rumble.
3. **Calibration is learned from the device**
   (`gc-adapter-consumer-neutral-calibration`): Dolphin takes the first sample
   after a port connects as origin; SDL widens an assumed range from samples.
4. **Linux binds no adapter-specific driver** at the pinned revision
   (`gc-adapter-linux-no-specific-driver`); evdev from the generic HID path
   depends on the unrecorded report descriptor.

## Open gaps

- USB and HID descriptors, polling interval, strings and any serial
  (needed for faithful enumeration and per-instance identity).
- Meaning of the remaining port status bits, and device response to rumble
  values other than 0 and 1.
- Behaviour of out-of-tree Linux drivers and userspace adapter daemons, and of
  Steam Input, not surveyed here.
- Switch 2 GameCube controller (057e:2073) is a separate device, tracked on the
  same issue for later; Linux has an in-tree ID for it (`NS2_GCCON`).
