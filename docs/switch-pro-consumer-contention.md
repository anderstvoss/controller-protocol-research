# Switch Pro — kernel hid-nintendo versus raw-app contention (H)

**Research parity, part 2: consumers and decisions** · source-only, **no lab run**. Nintendo `057e:2009`, wired and Bluetooth are distinct bus cases. Pins: `audio-linux-hid-nintendo` Linux `4056b3c` (`drivers/hid/hid-nintendo.c`); `audio-sdl-switch-pro` SDL `535d80b` (`SDL_hidapi_switch.c`); `swpro-dekunukem-*`, `swpro-openpuck-mode` are *device-oriented documentary leads*; joycond upstream pinned `0df025a` README lines 1–24 (G source, referenced by direct commit). Kernel/app host behavior is explicitly `consumer`.

## Ownership and order

1. **Kernel bound:** hid-nintendo claims the Nintendo HID interface, USB driver probe initializes transport; USB `0x80` handshake and HID subcommands `0x01` with `0x21` ACK read state, SPI calibration and color, then `0x40` IMU enable, `0x03` report mode and `0x48` vibration enable are sequenced by the driver (`hid-nintendo.c` 2369–2633, including 2600–2633; `swpro-l0-consumer-kernel-initialization-sequence` when present). Kernel drives EV_ABS/KEY and FF/LED class endpoints.
2. **SDL HIDAPI raw:** SDL Switch family can send its own command/ACK sequence, `0x48` vibration during open, select report mode, and `0x40` IMU on application sensor activation, rather than unconditionally (`SDL_hidapi_switch.c` 1536–1567, 1790–1805; part-1 `swpro-l0-*` consumer claims). Report `0x30` carries multiple IMU samples. Kernel and SDL both changing report mode/calibration can interfere; raw hidraw opening alone does not guarantee exclusive transport command ownership. Collision is **inferred**, not a demonstrated observed reset.
3. **joycond:** `DanielOgorchock/joycond` README 1–24 states it *consumes hid-nintendo evdev*, pairs Pro via buttons, and Plus+Minus builds an additional virtual controller for Steam. joycond therefore depends on kernel bound state and may create a **second uinput** identity. Exact USB output command ordering joycond emits: **No evidence** in this README.
4. **Steam Input:** the public `steam-client-udev-60-steam-input` grants do not reveal Steam's private feature calls. Steam kernel/joycond/raw open ordering, subcommands and report mode: **No evidence**.
5. **Wine/Proton:** Wine's generic hidraw/evdev preference may choose either; a Pro-specific report handshake in current pinned winebus path: **No evidence**.

### Bound/unbound matrix — proposed, not run

| Consumer | hid-nintendo **bound** | Kernel **unbound / hid-generic** |
| --- | --- | --- |
| Kernel evdev/evtest | hid-nintendo owns `0x80` USB handshake, `0x21` subcommand ACK and SPI/IMU calibration; evdev and FF/LED from kernel. [hid-nintendo.c 2369–2633] | Generic HID may expose descriptors/basic buttons only; Switch Pro vendor subcommands, SPI normalization, IMU and output from kernel absent. **No evidence** of exact generic events. |
| SDL HIDAPI Switch Pro | Potential concurrent kernel and SDL subcommands for `0x03`, `0x40`, `0x48`; capture `0x21` sequence/ACK ownership and report mode transitions. [SDL 1536–1567,1790–1805] | SDL raw becomes likely sole explicit device-command writer if it opens and has hidraw ACL. Kernel codec unavailable. Full report `0x30` acceptance still needs actual consumer test. |
| joycond | Expects kernel hid-nintendo evdev, may pair and create Pro `uinput`; duplicate controllers/LED ownership possible. [joycond README 1–24] | Driver-dependent evdev cues missing; **No evidence** joycond recognizes generic-HID device or can pair/virtualize it. |
| Steam Input | Exact raw commands, joystick path, kernel/joycond arbitration **No evidence**. Public rules only. | **No evidence** for Steam raw Switch subcommands or fallback mapping when unbound. |
| Wine/Proton | hidraw-versus-evdev choice implementation exists; which Switch Pro path/feature writes selected **No evidence**. [Wine main.c 501+] | Generic hidraw may be chosen; report ID handling and motion path **No evidence**. |
| SDL evdev, RetroArch, Chromium, Eden | Kernel-decoded evdev and SDL mapping if granted event-node access; gyro sibling depends on driver. Eden's `SDLDriver` is downstream SDL, not own HID driver. | Generic evdev can present a joystick; motion, rumble and full identity **No evidence**, map only observed events. |
| Kernel + SDL/Steam mixed | Two stateful subcommand owners are plausible; **No evidence** of ACK starvation, negotiated report mode or final IMU state without interleaving logs. | No hid-nintendo background writes but SDL/Steam coexistence still needs trace; **No evidence** on Steam arbitration. |

## Proposed low-risk host matrix

With no physical Switch Pro on hand, first run on virtual UHID while recording `/sys/bus/hid/drivers`, read-only hidraw availability, SDL selected driver and evdev nodes. Compare bound/unbound on a development host; never assume hid-generic yields full Nintendo feature replies. Record read/ACK sequencing for `0x80`, `0x21`, `0x03`, `0x40`, `0x48`, SPI 0x60xx/0x80xx; start without rumble, then request operator authorization for bounded output. Three independent sessions per condition, timeouts, clean kernel-driver rebind, no real Bluetooth pairing claim. Compare joycond running/not running and SDL HIDAPI enabled/disabled. Label all host tests **not run**.

**Claims feeding H:** `swpro-l0-*` in [the C ledger](ledgers/switch-pro-l0.md), including the C “what this settles” table; `swpro-vg-exp0009-sdl-motion` is *virtual host* acceptance, not source proof of device real-world mode negotiation.

**Cloud agent (realized-controller research parity)**
