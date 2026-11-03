# Switch 1 Joy-Con: how hosts see singles and pairs

**Source-only survey, no host runs.** Tracking issue: anderstvoss/virtualgamepad#297.
Owner decision (2026-11-03): model Joy-Con (L) and (R) first and choose the pair
shape from evidence. This note collects that evidence from the pinned public
consumers. It makes no device-protocol claims; those need their own ledger.

Registry IDs added with this note: `switch-joycon-family`, `switch-joycon-left`,
`switch-joycon-right`. Switch 2 Joy-Con stay a separate family.

## What the hardware presents

| Connection | Host-visible devices | Source |
| --- | --- | --- |
| Bluetooth, single half | One HID device per half: 057e:2006 (L) or 057e:2007 (R) | `joycon-linux-hid-ids`, `joycon-sdl-usb-ids` |
| Bluetooth, "pair" | Still two independent HID devices; nothing on the wire joins them | `joycon-hid-nintendo-identity-and-nodes` |
| USB Charging Grip | One USB device 057e:200e with one HID interface per inserted half; the half is told apart by the device-info type byte (and in SDL by interface number as a fallback) | `joycon-hid-nintendo-bus-binding`, `joycon-sdl-switch` |
| Joy-Con alone on USB | Not a host-visible case in any surveyed consumer | `joycon-hid-nintendo-bus-binding` |

## Where the pair is built

| Consumer | Pair behaviour | Combined identity | Claim |
| --- | --- | --- | --- |
| hid-nintendo (kernel) | Never combines. Each half gets a main node, an `(IMU)` node, player LEDs; home LED only on R. MAC from device info is the evdev uniq. | None | `joycon-hid-nintendo-identity-and-nodes` |
| joycond (userspace) | Combines after a user gesture (one shoulder on each half). Grip halves pair automatically. Hides the physical main nodes with udev rules. | uinput, "Nintendo Switch Combined Joy-Cons", 057e:2008, BUS_VIRTUAL | `joycon-joycond-pair-combination` |
| SDL3 HIDAPI | Combines automatically (hint default on), no gesture. Right IMU is the primary sensor, plus per-half sensors. | In-process virtual device "Switch Joy-Con (L/R)", PID 0x2008 | `joycon-sdl-hidapi-pair-combination` |

057e:2008 appears only as a consumer-made identity (joycond, mirrored by SDL).
It is not in the kernel's Nintendo product table.

## Implications for virtualgamepad (proposal, not a decision)

1. **Halves are the native unit.** A pair should be two Joy-Con halves, each
   with its own per-instance identity (MAC, colours, type byte), created and
   removed together if the caller asks for a pair. Consumers then combine them
   exactly as they would real hardware.
2. **Never create a 057e:2008 device.** That identity belongs to joycond and
   SDL. Presenting it from the library would duplicate their combined device
   and fake hardware that does not exist.
3. **Bluetooth-bus UHID is the faithful single-half path for hid-nintendo**,
   mirroring the Wii Remote case. A USB-bus UHID 2006/2007 device does not
   match the driver table. Real Bluetooth radio stays with #164.
4. **The Charging Grip is the only USB shape**, and it is a receiver-like
   device (one USB device, two slots), which is the ADR-0022 / #165 case. It
   is a candidate, not a requirement; hid-nintendo needs the USB handshake for
   it, and SL/SR disappear in the grip.
5. **Pairing tests need both consumers.** joycond needs a gesture and runs as a
   daemon with udev rules (a host-permission item for #258); SDL pairs on its
   own. A virtual pair should be accepted only when both paths are observed.

## Open questions (not answered here)

- Device-side protocol for the halves (subcommands, SPI layout, IMU, HD rumble,
  NFC/IR MCU on R): needs a device ledger built from device-protocol sources.
- Whether hid-nintendo binds a Bluetooth-bus UHID Joy-Con on the D9/Arch host,
  and the exact node names it produces.
- SDL2 and the SDL Linux evdev backend behaviour for halves and pairs.
- Steam Input and other closed consumers: not surveyed.
- Whether the Charging Grip shape is worth realizing at all.
