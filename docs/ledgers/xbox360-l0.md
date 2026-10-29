# Xbox 360 L0 — native XUSB device versus standard-HID consumers (Package F)

## Evidence and architecture boundary

This is a **source-backed L0 ledger**, not a physical retail Xbox 360 certification. All source-read claims have `applicability.transport: source_only` regardless of `evidence_role` (device/consumer). The two expressly unmeasured USB/receiver gaps retain `usb` as physical measurement transport. All 22 new `x360-l0-*` claims specify their role. No physical hardware experiments have been run.

**virtualgamepad's Xbox 360 UHID personality is standard HID by design.** This is an implementation choice, **not evidence** that a retail wired 045e:028e exposes generic HID, runs Linux's USB `xpad` driver, or enters SDL's XInput/XUSB decoder. Linux `xpad` targets a vendor-specific USB interface; `hid-input` processes generic HID Game Pad usages; SDL chooses its HIDAPI Xbox 360 decoder using type/interface eligibility and can also handle an evdev/gamepad-db mapping. These must remain separate realization/consumer scopes (#148). No code-level claim about virtualgamepad is promoted to a corpus observation.

Base: research `main` `914a4a0f7c8db4ddaa23acd72d73ab70f0ae96ba` **after merged D #70 and E #77**. The B `x360-vg-*` records are real, unchanged and historical **consumer** evidence. No branch `wip/btvirt` or unrelated family labels are reused.

## Pinned source evidence and limits

| Source ID | File/revision/locator | What it proves / limit |
| --- | --- | --- |
| `xbox-series-linux-xpad` (reuse) | Linux `4056b3c9d3c92ea45955641dbafeb9b960e146ef`, `drivers/input/joystick/xpad.c` 118–132, 420–503, 883–951, 1542–1759, 1907–2034 | xpad's *host* USB binding, evdev, FF and LED behavior; not a physical-controller capture |
| `x360-l0-linux-hid-input` | Same Linux revision, `drivers/hid/hid-input.c` 795–835; pinned and SHA256 hashed | Generic Game Pad Button usage ordinal `BTN_GAMEPAD + usage - 1` |
| `x360-l0-sdl-hidapi-360-320`, `x360-l0-sdl-hidapi-360-3418` | SDL `535d80b`, `829a65d`, `SDL_hidapi_xbox360.c` 62–95/86–129 routing, 243–338/295–396 decode, output 97–107/199–209 | The **selected** SDL Xbox360 HIDAPI consumer, not generic HID behavior |
| `x360-l0-sdl-hidapi-routing`, `x360-l0-sdl-gamepad-db` | SDL `535d80b`, `SDL_hidapijoystick.c` 262, 312–346, 470–477; `SDL_gamepad_db.h` 798 (Linux), 838 (other platform) | Driver selection and platform/VID/PID/GUID mapping; mapping DB ≠ proof of HIDAPI driver |
| `x360-l0-community-protor2` | mattiasbrandt/protoR2 `4c0d06274810ea1f5c1ad5d7f56e91b715947953` `docs/spec-sheets/xbox-controller-input.md`, sections 3, 5.1 (179–202), 5.2 (203–231), 9 (528–540); pinned/hashed | Independent **secondary** community report review of wired 20-byte XUSB and wireless receiver; sourced to USB Host Shield implementation, *not a primary capture* |
| `x360-l0-usbhost-wired` / `x360-l0-usbhost-receiver` | felis/USB_Host_Shield_2.0 `e5bc9950ba5389b67ad99175c312154af53df71d` `XBOXUSB.cpp` 244–365 / `XBOXRECV.cpp` 509–578; pinned/hashed | Independently developed real USB-host parser and wired rumble/LED writers, separate wireless report protocols; **consumer implementation evidence**, corroborating expected device wire format |
| `x360-l0-wireless-x360w` | zeromiyi/x360w `a8ac63058f29e071bbf2a7c051845db5b8f67ca1` README receiver report/LED/rumble cheat sheet; pinned/hashed | Separate independently implemented receiver with author-reported tested hardware, not a corpus lab run |
| `x360-l0-free60-archived-gamepad` | Free60Project/wiki `ab1fe1994706b74e8d68ab292b817a45f6fd0710`, `docs/Hardware/Accessories/GamePad.md` 1–69; pinned/hashed | The **actual fetchable archive** contains controller speculation and wireless cable pinouts, **not** the detailed wired input/output tables frequently attributed to historical free60. The absence is documented, never silently filled in. No file is marked fetch-blocked. |

Every newly pinned source record stores its immutable commit URL, SHA-256 and locator. The independent XUSB wire support consists of a community **secondary** summary plus a separate host implementation, not authenticated retail reference packets. The Microsoft XUSB interface is vendor-specific; it is **not generic HID**.

## Device-side L0 source candidates

| Area | Source-backed candidate | Claims and boundary |
| --- | --- | --- |
| Wired XUSB input | `00 14`, 20 bytes; D-pad/button bits in 2–3, LT/RT unsigned 8-bit 4–5, LX/LY/RX/RY signed little-endian 16-bit in 6–13, reserved 14–19 | `x360-l0-device-xusb-wired20`, `x360-l0-device-xusb-wired-buttons`. Supported by pinned *secondary* protoR2, corroborated by host USB Host Shield and SDL/xpad. No genuine-device trace; this is **source evidence only**. |
| Wired output | 8-byte `00 08 00 <strong> <weak> 00 00 00` rumble; 3-byte `01 03 <LED-mode>` | `x360-l0-device-xusb-output-ff-led`. Source evidence from independent USB Host Shield writer (`XBOXUSB.cpp` 323–359) corroborated by `xpad.c` 1569–1579, 1682–1689 and SDL 97–107, 199–209. Output request shape ≠ motor/LED performance. |
| Vendor interface | Wired `045e:028e` uses XUSB/vendor-specific USB interface, not automatically parsed generic HID; VID/PID alone is insufficient without interface realization | `x360-l0-device-xusb-nonhid-interface`. Community description plus USB xpad host binding; retail descriptor capture not available. |
| Wireless receiver | `045e:0719` USB dongle, per-controller slots and presence/status, report prefix, distinct rumble/LED, proprietary 2.4 GHz rather than Bluetooth | `x360-l0-device-wireless-receiver0719-lead`. Independent protoR2 and wireless x360w plus USB Host Shield receiver, **future lead**, not equivalent to wired XUSB. |
| Physical gaps | Genuine wired descriptor/bus and genuine 0719 pairing/capture/FF/LED, actuation timing and range remain unmeasured | `x360-l0-device-physical-wired-usb-unknown`, `x360-l0-device-physical-receiver-unknown` (usb measurement scopes). |

## Consumer-side L0 decisions

**Linux xpad evdev (source `xbox-series-linux-xpad`):** `045e:028e` maps to `XTYPE_XBOX360` and `045e:0719` to `XTYPE_XBOX360W` (`xpad.c` 118–132). Default wired:
- Keys `BTN_A`, `BTN_B`, **`BTN_X` (numeric 307)**, **`BTN_Y` (numeric 308)**, `BTN_START`, `BTN_SELECT`, `BTN_THUMBL/R`, `BTN_TL/TR`, `BTN_MODE` (`xpad.c` 420–450, 921–929). In Linux naming, `BTN_NORTH` aliases `BTN_X`; don't swap spatial X/Y merely based on printed labels.
- Sticks `ABS_X/Y/RX/RY` with **-32768..32767**, fuzz 16/flat 128, with Y inverted on decode; triggers `ABS_Z/RZ` **0..255** unless mapped as key events, and D-pad `ABS_HAT0X/Y` **-1..1** by default, optional `BTN_DPAD_*` (wireless keeps historical axes-plus-buttons) (`xpad.c` 883–951, 1907–2025).
- If `CONFIG_JOYSTICK_XPAD_FF` is enabled, xpad advertises **EV_FF/FF_RUMBLE** and writes its USB motor packet; it independently registers LED class `xpadN` and sends slot pattern packets (`xpad.c` 1542–1759). Those USB and class-device interfaces **do not materialize automatically on uinput**; virtual FF requires handler and separate LED strategy.
- IDs: `x360-l0-consumer-xpad-id-usb-binding`, `x360-l0-consumer-xpad-face-legacy-codes`, `x360-l0-consumer-xpad-sticks-trigger-ranges`, `x360-l0-consumer-xpad-dpad-axes-v-buttons`, `x360-l0-consumer-xpad-ff-uinput`, `x360-l0-consumer-xpad-led-class`.

**SDL Xbox360 and generic HID:**
- SDL 3.2.0 `SDL_hidapi_xbox360.c` 62–95 selects its driver by gamepad type and interface eligibility, excluding wireless receiver/chatpad; newer SDL `829a65d` preserves this plus Steam-virtual quirks. Matching 045e:028e in `SDL_gamepad_db.h` 798 gives a platform-specific GUID/evdev **mapping**, not proof of using the 20-byte decoder.
- Its selected XUSB decoder checks packet byte 0 == `00`, decodes D-pad hat, A/B/X/Y and guide from bytes 2–3, analog triggers 4–5, signed LE16 sticks 6–13; SDL rumble emits 8-byte `00 08`, LED emits `01 03`. The generic HID / evdev path instead sees the source descriptor's declared HID Button usages and kernel's generated event codes.
- Linux `hid-input.c` lines 795–835 maps HID Button usage `n` under a Game Pad application to `BTN_GAMEPAD + n - 1` for the first 16, not xpad's legacy packed report. SDL's actual selected path for a virtual device requires live instrumentation.
- IDs: `x360-l0-consumer-sdl360-classification`, `x360-l0-consumer-sdl360-wire-parser`, `x360-l0-consumer-sdl360-rumble-led`, `x360-l0-consumer-sdl360-vs-generic-hid`, `x360-l0-consumer-sdl-db-guid-entry`, `x360-l0-consumer-hidinput-button-usage-list`.

## What this settles for virtualgamepad (#148, feeds part 2 I)

| Question | Answer | Claim ID / No evidence |
| --- | --- | --- |
| Neutral standard-HID UHID identity vs SDL's XInput decoder | **Different host pathways.** xpad needs USB vendor interface and SDL Xbox360 HIDAPI needs eligible type/interface. A recognized Xbox-like name/VID and SDL evdev control mapping do **not** demonstrate native XUSB. The exact SDL backend/driver used by Steam/Eden is **No evidence** until measured | `x360-l0-consumer-xpad-id-usb-binding`, `x360-l0-consumer-sdl360-vs-generic-hid`, `x360-l0-consumer-sdl-backend-selection-unmeasured`, B `x360-vg-exp0009-standard-hid-controls` |
| Legacy xpad `BTN_X`/`BTN_Y` on uinput | xpad maps X/Y to Linux numeric key codes **307/308**. The standard-HID descriptor must encode appropriate Game Pad usages to achieve those event codes; merely matching a PID is insufficient. Distinguish key-code aliases from physical face labels | `x360-l0-consumer-xpad-face-legacy-codes`, `x360-l0-consumer-hidinput-button-usage-list`, B `x360-vg-exp0016-uhid-individual-correction` |
| Explicit HID usage list EXP-0016 | **`1,2,4,5,7,8,11,12,13,14,15`**, then **five constant padding bits**. This corrected the legacy X/Y alias: consecutive usages had emitted X as `BTN_C` (306) and Y as `BTN_X` (307). The corrected three-session SDL evdev run covers standard UHID, not native xpad/XUSB | `x360-l0-consumer-exp0016-hid-usage-correction`, `x360-l0-consumer-hidinput-button-usage-list`, B `x360-vg-exp0016-uhid-individual-correction` |
| FF and LED on uinput | EV_FF `FF_RUMBLE` on `xpad` needs build-time flag and USB output path. Historical B virtual evdev FF `x360-vg-exp0010-evdev-ff` is **consumer** evidence, **not** actual XUSB motor effects. **No evidence** that any uinput FF endpoint automatically generates xpad's separately registered `xpadN` LED. Test callbacks and lifecycle in lab | `x360-l0-consumer-xpad-ff-uinput`, `x360-l0-consumer-xpad-led-class`, `x360-l0-consumer-uhid-ff-led-unknown` |

## Proposed lab gates — no Xbox 360 controller on hand

| Gate | Requested experiment | Evidence to capture / acceptance rule |
| --- | --- | --- |
| F-P1 | Owner-controlled retail 045e:028e read-only USB descriptor and interrupt capture | Independent USB interface 0xFF and 20-byte `00 14` baseline, sanitized IDs/hash; no public serials |
| F-P2 | 20-byte one-control-at-a-time and neutral/repeated packet differential | D-pad, 16-bit axes, trigger endpoints, tail, timestamp and firmware variation; >=3 sessions |
| F-P3 | Safe LED and FF host reports | Device-side captures of 01 03 / 00 08 with controlled rumble durations, verify physical actuation and cleanup |
| F-P4 | Linux xpad vs standard-HID virtual UHID | Confirm driver ownership, evdev key-code aliases 307/308, axes/fuzz/flat, D-pad axis-v-button, FF node + LED-class node |
| F-P5 | SDL pinned 535d80b and 829a65d backend selection | Capture selected HIDAPI/evdev driver name, GUID, VID/PID, interface class/protocol, report bytes, SDL gamepad mapping; standard UHID vs native XUSB |
| F-P6 | EX​P-0016 explicit HID usage reproducibility | Run old consecutive usages and exact corrected 11 usages; 3+ neutral/press/release sessions in SDL, evtest and Steam/Eden as separate consumers |
| F-P7 | Uinput FF callback and LED isolation | Send bounded FF_RUMBLE through uinput; trace callback and reset/reopen, test whether LED endpoint exists (expect independent realization) |
| F-P8 | Separate Xbox 360 wireless receiver 045e:0719 | Four-slot presence, USB interfaces, pairing/reconnect, wireless transport latency and distinct output commands; no assumptions from wired or Bluetooth |

All gates are **proposed**, not `virtual_host_run` experiments in this PR. No controller is on hand (#148). The original Free60 archive is accessible but lacks its historically quoted wired protocol tables, so **no Free60 page is marked `source pending: fetch blocked`** for F; the alternative pinned protocol references are used with their limits. Existing unresolved **PS4 Developer Wiki DS4-USB and DS4-BT** source-pending pages belong to E and remain on the part-1 closeout list.

**Cloud agent (realized-controller research parity)**
