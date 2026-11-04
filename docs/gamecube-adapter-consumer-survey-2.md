# GameCube adapter — supplemental consumers and uinput survey

**GameCube USB research, prep for #296** · Source-only; all proposed host tests are **not run**. Supplements the existing [adapter survey](gamecube-adapter-consumer-survey.md) and its 13 claims, without editing them. A's new claim IDs are referenced for cross-PR review; B must be refreshed against main after A merges.

## Ranked access/discovery survey

| Consumer | Discovery and permissions | Input/output reports and mapping | Proposed host test (not run) |
| --- | --- | --- | --- |
| **SDL3 native GameCube adapter** | USB `057e:0337` via **libusb required**; needs USB device-node read/write or ACL, not hidraw (`gc-adapter-consumers-require-usb-device`) | 0x13 init, 37-byte 0x21 input, five-byte 0x11 rumble; 0x04 rumble power and 0x10/0x20 port type. Plain uinput pads go through SDL's separate evdev path | Compare libusb direct adapter detection against four uinput pads; log SDL backend, GUID, hotplug, reports and FF |
| **Dolphin native adapter** | libusb USB hotplug, can detach kernel driver and claim interface (`gc-adapter-consumers-require-usb-device`, `gc-adapter-set-protocol-kick`) | 0x13/0x21/0x11; Dolphin-calibrated first connected sample (`gc-adapter-consumer-neutral-calibration`) | Direct USB adapter vs independent SDL generic pads; inspect open/claim conflicts and controls |
| **Dolphin Android** | Android UsbManager device permission grant and UsbDeviceConnection, not a Linux hidraw path (`gc-adapter-dolphin-android-usbmanager`) | 0x13 init, per-port reads, five-byte rumble output through Android transfer API | Android USB permission denial/grant, disconnect and open/close |
| **Eden direct adapter** | Direct libusb device, detach, claim interface and dynamic endpoints; USB node ACL (`gc-adapter-eden-direct-libusb`) | 0x13/0x21/0x11; separate internal controller implementation | Confirm direct GameCube backend binds USB gadget; compare SDL Gamepad mapping to uinput separately |
| **Cemu direct adapter** | Direct libusb, hotplug and kernel detach; USB node ACL (`gc-adapter-cemu-direct-libusb`) | 37-byte input, 0x13/0x11, four internal controllers. Code reads rumble power from first port; actual per-port semantics **No evidence** | Test each physical port independently and unplug/replug; check power gate across ports |
| **RetroArch udev joypad** | libudev plus evdev event node permissions (`parity-g-retroarch-udev`); dedicated raw adapter backend in inspected material: **No evidence** | EV_KEY, EV_ABS and optional EV_FF from each virtual uinput pad; direct 0x13/0x21/0x11 backend: **No evidence** | Map four virtual pads, test trigger axes plus click, face orientation and FF callback |
| **SDL evdev/GameController mapping** | Linux input subsystem and `/dev/input/event*` ACL; unrelated to native libusb match. ToadKing ships explicit **external** SDL2 mapping (`gc-adapter-toadking-external-sdl-map`) | No native adapter reports; reads EV_KEY/EV_ABS/EV_FF. Built-in `gamecontrollerdb` match for ToadKing GUID: **No evidence** | Collect generated GUID for all ports; check baseline bundled database vs external mapping, SDL2 vs SDL3 |
| **Steam Input** | Public Valve udev rules at commit `22ec85e5ff5ea2e15c56d71a41bcbef46356cd60` line 236 grant `057e:0337` USB device node `MODE=0660` and `uaccess`. Steam client discovery route and actual implementation: **No evidence** | Raw packet writes/reads, mapping from daemon uinput and rumble: **No evidence** | Trace which device nodes Steam opens, native vs evdev source, and controls only after an owner-approved run |
| **InputPlumber / HHD** | No inspected adapter-specific profile or consumer source; native handling: **No evidence**. Generic evdev availability is conditional on actual source enumeration | Adapter 0x13/0x21/0x11 support, translation and FF: **No evidence** | Pin versions, inspect source profiles at exact revisions and log discovery/mapping without claiming support |
| **Chromium Gamepad / WebHID / WebUSB** | Chromium Gamepad Linux udev/input path from `parity-g-chromium-gamepad-linux`. WebHID static list at `parity-g-chromium-webhid-blocklist` does not establish grant or denial for 057e:0337; WebUSB blocklist-specific match: **No evidence** | WebHID permission, protected reports and WebUSB permission separate from Gamepad API; direct adapter report reads/writes **No evidence** | Record browser version and separate WebHID/WebUSB chooser decisions, Gamepad API mapping and any protected-report blocks |

## What cannot be concluded

- Steam's published **permissions rule is not proof of Steam Input adapter handling**. Do not infer a closed-source report decoder.
- InputPlumber or HHD generic controller support is not evidence of WUP-028 native support.
- Shared SDL/GameController mappings may be supplied by third-party daemon; do not claim that SDL ships one.
- Direct libusb backends need real USB-level enumeration; native-looking uinput VID/PID or a UHID identity does not satisfy them (`gc-adapter-consumers-require-usb-device`).
- No host run, native descriptor capture, port-status experiment or physical rumble observation was performed.

**Cloud agent (GameCube USB research)**
