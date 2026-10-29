# Xbox 360 — supplementary kernel-vs-app contention note (H)

This note is the Xbox 360 **consumer-survey contention section** for G (the G survey remains a separate PR until merged; do not duplicate its entire file in H). On a real wired `045e:028e`, USB xpad binds the **vendor-specific XUSB** interface, creates evdev, xpad FF and LED class; SDL may attach via its selected 20-byte XUSB HIDAPI decoder. If `xpad` is unbound, kernel-created evdev/FF/LED disappears, while a direct USB XUSB driver may still be possible with device permissions; exact bus-claim conflict **No evidence**. On virtualgamepad's **standard-HID UHID**, xpad's USB interface was never present; generic hid-input or SDL evdev accepts ordinal HID usages, while SDL's XUSB HIDAPI path is **not** implied by PID. Claims: `x360-l0-consumer-xpad-id-usb-binding`, `x360-l0-consumer-sdl360-vs-generic-hid`, `x360-l0-consumer-xpad-ff-uinput`, `x360-l0-consumer-xpad-led-class`.

| Consumer | xpad USB driver bound | xpad unbound or standard-HID UHID |
| --- | --- | --- |
| evdev, SDL Linux-event, RetroArch | xpad input/FF/LED nodes exposed, SDL mapping database; live read **not run**. [xpad.c 118–132, 883–951, 1542–1759] | No xpad USB output FF/LED; standard-HID usage mapping via `hid-input.c` 795–835 may create ordinary evdev, but native XUSB **No evidence**. |
| SDL Xbox360 HIDAPI | Native 20-byte XUSB parser is selected only for matching type/interface; which process owns USB endpoint and FF/LED **No evidence**. [SDL_xbox360.c 62–95, 243–338] | Real USB device may be claimed by raw library; exact arbitration **No evidence**; generic HID UHID may take SDL event path instead of XUSB. |
| Steam / Wine | Private Steam USB requests **No evidence**; Wine HID and XInput layers may choose specialized or event path, untested. | Steam current-backend selection **No evidence**. |

Proposed bound/unbound lab only after a physical controller is acquired; virtual-only tests should first trace SDL backend and evdev mapping. Do not reinterpret B virtual UHID FF as physical xpad force feedback.

**Cloud agent (realized-controller research parity)**
