# Joy-Con L/R compat-versus-faithful decision table (F)

**Joy-Con research, prep for virtualgamepad #297.** Design choices below are **proposals**, not implemented features or physical validation. A consumer-generated `057e:2008` pair is explicitly not a native Joy-Con personality. Claims are source-only: see `joycon-*` and reused `swpro-*` records, without editing them.

| Branched-on value / behavior | Consumer dependence | Compat choice (configurable, if needed) | Faithful/default choice | Claim/source IDs |
| --- | --- | --- | --- | --- |
| L/R Bluetooth HID name | SDL pairs halves by PID; Charging Grip fallback can check '(L)' and '(R)' in normalized names; Linux input node uses HID name. Retail on-air strings **No evidence** | Expose SDL-recognizable side-specific display names when a host needs them | Preserve the real on-air name if subsequently captured; never claim SDL's normalized name is physical | `joycon-sdl-hidapi-pair-combination`, `joycon-sdl-switch`, `joycon-c-kernel-version-and-identity` |
| PID | hid-nintendo Bluetooth table binds 2006/2007, SDL HIDAPI accepts these, joycond listens for physical main events, Steam rule grants hidraw for both | Keep side-specific 2006/2007. Never manufacture 2008 in a hardware codec | Exact L/R PIDs with independent devices | `joycon-hid-nintendo-bus-binding`, `joycon-e-steam-hidraw-grants`, `joycon-d-sdl2-hidapi-pair` |
| Device-info type | hid-nintendo requires `0x02` and uses type 0x01 L / 0x02 R; SDL device-info may fail and fall back to PID | Do not contradict PID; if needing spoofed unknown type, isolate as experimental and off by default | 0x01 L, 0x02 R, per device | `joycon-a-device-info-type`, `joycon-c-kernel-bt-probe-required`, `joycon-c-sdl3-bt-open-gates` |
| Uniq/MAC | Kernel copies six device-info bytes to input uniq; SDL derives serial from them, joycond can use identity for reconnect/pair | Per-instance generated stable bytes within session, deterministic for reconnect; never hard-code a public shared identity | Caller-settable six-byte value, most-significant byte first in device-info response; no sample bytes recorded | `joycon-c-kernel-version-and-identity`, `swpro-l0-consumer-linux-mac-uniq`, `swpro-l0-consumer-sdl-mac-serial-guid` |
| Version (HID and device firmware) | Kernel sets high bit on hdev version for SDL2 remapping; SDL can use version in GUID; firmware bytes from 0x02 are separate | Optional host-visible version override only where necessary for documented mapping; do not fabricate physical firmware revision | Preserve caller-specified HID/firmware values and real documented format when captured | `joycon-c-kernel-version-and-identity`, `swpro-l0-device-info02-fields` |
| Colours | SDL/kernel SPI readers and game UIs may use body/button RGB; software identity differences do not prove physical calibration | Permit caller-configured RGB and optional missing-colour indication | Preserve per-instance RGB colour arrays: three bytes each for body and buttons; grip colours only where supported | `joycon-a-calibration-per-side`, `swpro-l0-device-factory-spi-map`, `swpro-l0-device-info02-fields` |
| HID descriptor | Generic Linux HID parser, HIDAPI and hidraw discovery need a valid descriptor. **Exact retail descriptor No evidence.** | Explicitly identify provisional descriptor as compatibility scaffold, not faithful emulation | Byte-for-byte source-backed retail descriptor only after pinned evidence, tested through both kernel and SDL | `joycon-c-kernel-version-and-identity`, `joycon-hid-nintendo-bus-binding` |
| Side IMU, rail/SL-SR | Kernel transforms right IMU Y/Z signs; SL/SR excluded on grip; exact rail state unknown | Expose side-specific capabilities explicitly, avoid treating rail as generic button | Preserve per-half IMU coordinates and rail-dependent controls; avoid cross-half aliasing | `joycon-a-right-imu-signs`, `joycon-a-home-led-and-rail-buttons` |
| Pair | SDL2/SDL3 create in-process 2008, joycond creates uinput 2008; kernel never combines | Convenience creates/removes both L/R instances atomically; do not publish third 2008 device | Two independent Bluetooth-bus instances; Charging Grip receiver as a separately researched USB topology | `joycon-joycond-pair-combination`, `joycon-sdl-hidapi-pair-combination`, `joycon-d-sdl2-hidapi-pair` |

## Per-instance identity properties at creation

- **MAC/uniq:** six bytes in controller-info reply, most-significant byte first; unique per instance and stable for reconnect where lifecycle requires. No address-shaped or serial-shaped examples belong in public source control.
- **HID version:** host HID version integer distinct from **firmware version** (two bytes in device-info response). Kernel may modify its reported high bit. Format of actual retail firmware values is **No evidence** without capture.
- **Serial:** optional opaque caller-provided value; **retail SPI serial region format and Bluetooth HID serial presentation are No evidence** at current pins. Do not invent one or imply the device-info MAC is a manufacturer serial.
- **Colours:** body RGB and button RGB as three components per item, with grip RGB slots only if they truly exist for a particular shape. Use a colour-presence flag where consumer checks it.
- **Body type:** caller-selectable logical side L/R and its type byte; any additional SPI body-revision/type property remains **No evidence**.
- **Pair membership:** library coordination identity, not a wire-visible 2008 personality. Each half retains independent per-instance identity.

## Decision pending physical evidence

Use Bluetooth-bus UHID with true side IDs as the source-supported architectural target. Do **not** state that a retail descriptor or product name is known, or that a local Linux/SDL application has recognized any generated device.

**Cloud agent (Joy-Con research)**
