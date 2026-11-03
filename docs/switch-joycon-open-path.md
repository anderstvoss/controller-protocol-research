# Joy-Con Bluetooth-bus open path and Charging Grip (C)

**Joy-Con research, prep for virtualgamepad #297** · source-only research from pinned `joycon-linux-hid-nintendo`, `joycon-sdl-switch` and existing Switch Pro source records. All host tests are proposed and **not run**.

## C1. Linux hid-nintendo Bluetooth probe — exact source order

At Linux `4056b3c9d3c92ea45955641dbafeb9b960e146ef`, the HID table matches 057e:2006/2007 **only** with BUS_BLUETOOTH. After HID descriptor parsing, `hid_hw_start(...HID_CONNECT_HIDRAW)`, `hid_hw_open`, and beginning I/O, initialization follows this sequence:

| Order | Operation | Required to finish probe? | Failure behavior |
| --- | --- | --- | --- |
| 1 | USB handshake | **Not sent** on a Bluetooth-bus half | Entire USB branch bypassed |
| 2 | Subcommand `0x02` get device info, reply `0x21` | **Yes** | Failure aborts initialization; type byte and six-byte address are parsed from reply |
| 3 | SPI `0x10`: user-calibration markers and factory/user stick data | **No** | Bad or failed stick reads use hard-coded defaults |
| 4 | SPI `0x10`: user and factory IMU calibration | **No** | IMU offsets/scales use defaults |
| 5 | Subcommand `0x40` enable IMU | **Yes** for retail Joy-Con | Failure aborts; exception is licensed Pro device, not L/R |
| 6 | Subcommand `0x03` select full report mode `0x30` | **Yes** | Failure aborts |
| 7 | Subcommand `0x48` enable vibration | **Yes** for retail Joy-Con | Failure aborts; licensed Pro exception does not apply |
| 8 | After init: LED creation, battery supply and input node creation | **Yes** for complete kernel probe | Failure prevents completion and triggers cleanup |

Synchronous subcommands are delivered in output `0x01`, with a wrapped counter and two rumble words, and replies are selected by echoed ID in `0x21`. Kernel response matching compares reply report ID and subcommand ID; the probed code path does not independently test the ACK high bit when selecting a match. **Important:** an ACK-only-looking `0x21` with matching ID is enough to wake the waiter, but fabricated SPI data can still fail validation and trigger fallbacks; do not infer full implementation sufficiency.

Write pacing: two attempts across timeouts, 60 ms BT minimum, three consecutive 8–17 ms input deltas in strict mode; repeated timeouts in the rate gate eventually relax to the older 25 ms limiter. These are *kernel policies*, not guaranteed controller timing.

Source locators: `joycon-linux-hid-nintendo` 840–1040, 1080–1320, 2495–2635, 2680–2910; shared framing `swpro-l0-device-subcmd-ack-byte`.

## C2. SDL3 HIDAPI Bluetooth init/open — separate from the kernel contract

At SDL `535d80badefc83c5c527ec5748f2a20d6a9310fe`:

1. Driver eligibility accepts Nintendo 2006 (L), 2007 (R) and 200e grip by PID. It makes a separate special-case device-info probe for some Pro-PID clones.
2. `InitDevice` initializes neutral rumble and **attempts** `0x02` device-info over BT, but does not make failure fatal. It assigns L/R type from product ID if the type read fails, and rewrites the displayed HIDAPI name/VID/PID/type. It also constructs an SDL serial from device-info address bytes; **do not encode a real address in the corpus**.
3. `OpenJoystick` probes the currently received input report mode; BT bypasses USB setup. It requires a successful *factory stick SPI-read* after trying optional user calibration; factory read failure returns open failure.
4. IMU calibration is **optional**: failure uses defaults in the SDL routine, but the joystick marks sensors supported only after successful calibration. The vibration-enable return is ignored by this caller. Enhanced-report hint initialization chooses full `0x30` for Joy-Con in automatic mode to avoid the simple-mode stick-as-D-pad limitation. The code does not use all kernel-fatal subcommands with the same conditions.
5. For synchronous subcommands SDL accepts only `0x21` with matching subcommand and ACK bit, and retries to its configured attempt limit (normally five). For Bluetooth output, it uses a distinct padded output size from USB.

This source pin shows **meaningful differences** between hid-nintendo and SDL3. A device that passes one open path may fail the other. SDL2 exact version and divergence are **No evidence** in this pass; an SDL2 tag/commit must be pinned before specifying differences.

Source locators: `joycon-sdl-switch` 355–510, 605–700, 775–855, 930–1100, 1130–1210, 1300–1565.

## C3. Identity, descriptor, version and uniq gates

| Item | hid-nintendo (pinned) | SDL3 HIDAPI (pinned) |
| --- | --- | --- |
| VID/PID & bus | Explicit bus-qualified Joy-Con HID table | Nintendo VID and L/R/grip PID are eligibility gates; names are set/normalized after type inference |
| Device type | **Required** in `0x02` reply to select capabilities | Obtained from optional info probe or product fallback |
| Device name | Node name reflects HID name, no Joy-Con name predicate in its device table | Name used for specific third-party exclusions and for classifying combined grip/pair; L/R displayed name is normalized |
| Version | Sets high bit of `hdev->version` for SDL2 mapping distinction; not a device admission check here | Device identity/GUID can include version, but L/R PID eligibility does not gate on a specific version |
| MAC/uniq | Six bytes from device info become input-node uniq; absence of valid `0x02` reply prevents probe | Synthesizes HIDAPI serial from reply bytes; PID fallback can still permit initialization |
| Report descriptor | Invokes generic HID parse; **no retail Joy-Con descriptor byte source pinned** | HIDAPI enumeration requires a usable underlying HID interface, but no exact Joy-Con descriptor comparison established by this source |

**No evidence:** actual retail Bluetooth HID report descriptor, on-air product name and the precise descriptor bytes needed for all Linux HID/SDL enumeration branches. Avoid claiming a reproduced descriptor or a guaranteed UHID bind.

## C4. Charging Grip USB path (distinct receiver topology)

The USB Charging Grip PID is `057e:200e`, not USB-bus `2006` or `2007`. The kernel's grip initialization requires an acknowledged `0x80` USB handshake subcommand `0x02`; it optionally sets `0x03` high baud rate, requires a second `0x02` handshake, then sends unacknowledged `0x04` no-timeout. Failure of the *first* grip handshake aborts, unlike the conditional Pro/BLE branch. USB replies use report `0x81`. Side is determined from device-info type `0x01`/ `0x02`; SDL can fall back to interface-number discrimination (interface 1 left, otherwise right). Kernel hides SL/SR when grip attached and treats grip IMU as available. **Exact real USB interface descriptor and interface-to-side invariants are not independently captured.**

Source: `joycon-hid-nintendo-bus-binding`, `joycon-linux-hid-nintendo`, `joycon-sdl-switch`.

## Proposed host tests (not run)

- **BT kernel:** present separately created BUS_BLUETOOTH 2006 and 2007 UHID instances with an explicitly sourced descriptor; trace every `0x01` request and `0x21` matched ACK, including retries, and separate fatal vs defaulted paths.
- **BT SDL3 and SDL2:** pin library build/driver selection and open both direct HIDAPI and evdev backends; compare device-info failure, factory/user SPI failure, sensor visibility and 0x3F-to-0x30 transitions.
- **Grip USB:** only after a receiver-like topology is implemented, check USB bus identity 200e, interface-to-side mapping, two handshakes, optional baud and no-timeout, SL/SR exclusion and IMU nodes.
- **Identity:** capture from *authorized physical hardware*, privately, a sanitized HID descriptor shape and name/uniq expectations. No physical capture was performed here.

**Cloud agent (Joy-Con research)**
