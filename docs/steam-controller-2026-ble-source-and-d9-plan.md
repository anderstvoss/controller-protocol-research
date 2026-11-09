# Steam Controller 2026 Bluetooth — pinned source research and D9 evidence plan

**Evidence class:** source inspection only. This document records Linux/SDL/BlueZ/Valve public consumer implementations and their implications for a potential `28de:1303` realization. No Bluetooth pairing, D9 physical capture, scratch UHID run or Steam UI test was performed for this record. The report descriptor, firmware, report cadence and radio behavior remain **No evidence** for the physical `1303` reference.

**Scope:** direct BLE `28de:1303`, the Bluetooth-bus UHID target `linux.uhid.bluetooth`, and comparison to the separately accepted wired `28de:1302` baseline. Puck receiver details are only source hints. Do not merge Bluetooth claims into receiver or wired acceptance.

## Reviewed pins and lineage

| Source | Pin | Evidence |
|---|---|---|
| [Linux hid-steam](https://github.com/torvalds/linux/blob/c03c1a14507dfaf8b856c2608f9ac216021fc222/drivers/hid/hid-steam.c) | v7.3, `c03c1a1` | Kernel consumer source, GPL (not reproduced) |
| [SDL Triton used on D9](https://github.com/libsdl-org/SDL/blob/e0232c5b9d972ad394d597ce858185cd15a0f1a7/src/joystick/hidapi/SDL_hidapi_steam_triton.c) | `e0232c5`; existing source `steam-closeout-sdl-triton-e0232c5` | Consumer source only |
| [SDL later Triton](https://github.com/libsdl-org/SDL/blob/531acc0a76cf910b7616b2c5f63de2c5b3a4ba0a/src/joystick/hidapi/SDL_hidapi_steam_triton.c), [structs](https://github.com/libsdl-org/SDL/blob/531acc0a76cf910b7616b2c5f63de2c5b3a4ba0a/src/joystick/hidapi/steam/controller_structs.h), [IDs](https://github.com/libsdl-org/SDL/blob/531acc0a76cf910b7616b2c5b3a4ba0a/src/joystick/controller_list.h) | `531acc0` | SDL lineage; not independent of prior SDL |
| [BlueZ profile](https://github.com/bluez/bluez/blob/aa4f5ce97c875961a7c3ca88baa30c544edb58cd/profiles/input/hog.c), [shared HoG](https://github.com/bluez/bluez/blob/aa4f5ce97c875961a7c3ca88baa30c544edb58cd/src/shared/hog.c), [UHID](https://github.com/bluez/bluez/blob/aa4f5ce97c875961a7c3ca88baa30c544edb58cd/src/shared/uhid.c) | `aa4f5ce` | One BlueZ lineage |
| [Valve steam-devices rules](https://github.com/ValveSoftware/steam-devices/blob/22ec85e5ff5ea2e15c56d71a41bcbef46356cd60/60-steam-input.rules) | `22ec85e` | Public rules only; not Steam client internals |
| [OpenPuck receiver](https://github.com/safijari/openpuck/blob/29f4d1e8b85c0a7c19e0c8b977a1a56a2c42ea6d/OpenPuck/puck_hid.cpp) | `29f4d1e` | Proprietary-radio relay hint, not HOGP evidence |
| [Official Valve connection instructions](https://help.steampowered.com/en/faqs/view/33E8-5EDF-24E6-4CFB) | Public support page (mutable) | Operator pairing procedure only, not a pinned protocol source |

All pinned source file SHA-256 values reside in `records/source/steam-ble-*.json`, except the previously recorded private SDL revision and OpenPuck. No upstream source text or firmware content is copied here. Existing wired physical claims live in research PRs #105/#106/#108/#109/#110. Source line references below are pinned to their above revisions.

## Linux `hid-steam` consumer contract

1. **Identity and matching.** `hid-steam.c:2751-2761` declares Bluetooth VID/PID `28de:1303` with `STEAM_QUIRK_IBEX | STEAM_QUIRK_BLE`. The BLE match reaches one unified HID interface (`1618-1626`); a USB interface number is not needed.
2. **Input.** `2530-2619`: `0x42` requires 54 bytes including ID; `0x45` requires 46; `0x43` battery requires 15; `0x79` connect/disconnect requires 2. The same IBEX switch handles both wired and BLE. A declaration or parser for `0x47` in SDL does not make `0x47` a Linux gamepad input format. Any physical BLE input mix is **unknown**.
3. **Shared codec prefix.** For both `0x42` and `0x45`, seq is offset 1, buttons 2-5, triggers 6/8, sticks 10/12/14/16, left pad X/Y/pressure 18/20/22, right pad 24/26/28, IMU time 30-33, accel 34-39, gyro 40-45. `0x42` additionally carries quaternion bytes 46-53. This is the host consumer interpretation; no physical BLE bit-level validation is implied. Existing `steam-c6-input-42` and `steam-c6-input-45` describe these fields.
4. **Feature transport.** IBEX controller uses feature ID 1. `435-665` uses nominal 64-byte HID features, command and length fields and a SET/GET exchange, with bounded protocol/EPIPE retries. Registration requests the unit string and attributes (`667-717, 1372-1418`), and a returned connection-interval attribute may override the initial 9000-us kernel sensor cadence. A feature GET failure may be nonfatal at probe, but missing responses can degrade identification. Unsupported requests need deterministic error replies; do not hang a host transaction.
5. **Mode/clients.** `880-975, 1372-1418, 1633-1874`: registration sets desktop mapping and lizard/settings intention and registers gamepad, sensors and battery. Opening the synthetic layered hidraw client suppresses kernel native inputs; closing permits re-registration. Raw-client close alone is not an unconditional firmware restore operation. The input Menu long-hold handler can switch native gamepad mode after about 450 ms (`2441-2458`). Distinguish firmware-side desktop reports `0x40/0x41` from kernel-native input gates.
6. **Output.** Kernel `0x80` rumble and `0x81` pulse are IBEX output paths (`751-875`). They are host writes, not evidence of audible/tactile effects on Bluetooth. Physical LED, haptics and PCM response are unverified.

## SDL Triton: exact D9 build and upstream comparison

The exact `e0232c5` Triton driver is retrievable at its pinned upstream commit; the corpus already records its SHA-256. SDL classifies `1302` and `1303` as Triton (`controller_list.h:671-674` at the D9 revision). Later `531acc0` still classifies both. SDL accepts `0x42`, `0x45` and `0x47`, battery `0x43`, and recognized wireless status inputs. `0x45` uses the no-quaternion shape; `0x47` uses a different pad/IMU timestamp representation. There is no reason to select `0x47` as the only Bluetooth stream.

SDL sends periodic feature-ID-1 lizard-disable updates at approximately three-second intervals and an IMU mode setting when sensors are enabled. Its advertised `4032`-us sensor update interval is a consumer constant, not a BLE measurement. Ordinary rumble sends output report `0x80` and resends while active approximately every 40 ms; optional short haptic effect reports `0x81` through `0x85` have explicit length checks. SDL's rumble support or return from a write is not proof that a Bluetooth actuator responded. Physical feature exchange, battery cadence, LED support, output pacing and internal PCM modes are unknown.

## BlueZ HOGP: report map, GET/SET and identity

BlueZ `profiles/input/hog.c:62-85,188-206` acquires the name and PnP version, requires link security/bonding for a real GATT HID device, and attaches the HoG client. `src/shared/hog.c:842-897` waits for a Report Map and discovered reports and constructs one `UHID_CREATE2`. `src/shared/uhid.c:391-445` sets `BUS_BLUETOOTH` (5), VID/PID/version and descriptor. This is the host-facing device visible to Linux; it is **not** a USB composite device.

`src/shared/hog.c:686-801` translates UHID feature SET/GET requests to the appropriate GATT Report characteristic write/read; for numbered SET reports it drops the numbered prefix before writing, while the numbered GET reply is rewrapped at the UHID boundary. The kernel's HID feature API does not itself establish an RF connection. A scratch UHID daemon must service the host's requests synchronously enough to avoid timeouts and use correct numbered-report conventions.

BlueZ obtains host/peer socket identifiers and exposes them as `phys` and `uniq` in `UHID_CREATE2` (`shared/hog.c:803-853`, `shared/uhid.c:391-435`). No real address, fictitious address-shaped literal or Bluetooth bond belongs in this corpus. The planned emulator should follow the existing Wii Remote identity precedent: a typed, caller-set six-octet **locally administered unicast** Bluetooth-style identity with a fresh per-instance synthetic default. Serialize that runtime identity into the Bluetooth-style host `uniq` without storing real or example address values in the repository. The feature-report unit serial remains a different identity channel. Whether Steam/SDL requires a particular `uniq` representation is a scratch-test question.

## Public Steam client evidence and its limits

The pinned Valve `60-steam-input.rules:7-14` covers Valve hidraw on Bluetooth bus 5 and Valve evdev access. These access rules alone do not show Steam Input discovering, retaining or accepting a virtual BLE controller. No public pinned Steam client protocol parser was established by this study. Steam listing, details, Begin Test, feature transactions (including `0xae`) and output/LED acceptance **require owner-operated D9 observation**. Wired success or `0xae` rejection cannot be transferred to Bluetooth.

Valve's support guide describes Bluetooth mode as blue LED and a right/left slot; the controller maintains Bluetooth pairing separately from Puck pairings. With the controller off, the owner uses Steam+B+R1 for the right Bluetooth slot or Steam+B+L1 for the left; continuing through the second chime and double-blue pulse enters pairing mode. A normal power-on using the same chord is not the same as requesting a new pairing. Do not include the advertised identity suffix in published captures. Do not accept firmware updates.

## OpenPuck applicability and excluded paths

OpenPuck `29f4d1e` forwards controller input `0x42/0x45` from the proprietary receiver radio link to USB per-slot interfaces. That supports *only* a cross-transport hypothesis that the controller can produce these encodings. The relay is not a Bluetooth GATT capture, does not establish BLE MTU or report map, and cannot justify using its Puck descriptor as a `1303` descriptor. Puck receiver `1304`, internal receiver `1305`, real HCI radio emulation and firmware analysis are not part of this lane.

## Provisional architecture decision (not yet approved implementation)

Keep the compiled family `virtualgamepad.steam-controller-2026` and existing native state (22 buttons, triggers, two sticks/pads, touch/pressure, IMU, battery and host outputs). Add explicit target `linux.uhid.bluetooth` with bus 5, VID `28de`, PID `1303`, a **measured** BLE HID descriptor and per-realization report encoder. No automatic fallback to `linux.uhid.usb`, no distinct family ID unless capture reveals incompatible native topology. No product changes in this PR.

The existing wired `SteamController2026Options` has `identity`, `steam_client_compat`, `haptic_streaming`, `lizard_mode`. Resolve the API review as follows: preserve a caller-restorable feature serial; add a separately typed Bluetooth link identity option (or extend the existing identity type) for UHID `uniq`, without conflating it with the feature serial. Reuse the Wii-style locally administered unicast validation and per-instance generation policy; a Bluetooth-style `uniq` is not evidence of a real address, link or bond. Keep `steam_client_compat` and `lizard_mode` target-scoped and keep lizard off by default, following the wired owner decision, pending BLE tests. Do not mark `haptic_streaming` supported on Bluetooth without physical output/feedback evidence. The descriptor's report inventory and version are not yet known.

## D9 capture and scratch validation order (owner only)

**Coordination gate:** the Puck session and this BLE session share one Steam Controller. Owner must explicitly release it from the other session before pairing, and stop this session before Puck testing resumes. Agents perform no controller pairing, physical sends, root/module operations, unbind/rebind or BlueZ configuration changes.

1. **Owner pairing:** record selected right/left Bluetooth slot, confirmation of BLE vs BR/EDR from owner-private discovery, and non-identifying visible connection state. Keep complete Bluetooth monitor logs privately.
2. **Descriptor/enumeration:** on paired `1303` list kernel bus, VID/PID, version, HID driver, input/hidraw child count and the HOGP descriptor. Publish the full descriptor only after manual review or else its length/hash. Redact `phys`, `uniq`, peer/host identity, local paths, wall-clock timestamps and link material.
3. **Isolated baseline:** Steam/SDL/Dolphin closed, record idle and active native evdev observation. A separate layered hidraw read can remove those native nodes under `hid-steam`; never conclude that this alone is a kernel decode failure.
4. **One control at a time:** neutral, every digital input, both triggers, all sticks, pad touch/click/position/pressure, capacitive controls, independently labelled IMU movements; compare with wired #105 offsets and semantics. Record relative event cadence, dropped captures and disagreements.
5. **Kernel/SDL feature lifecycle:** passive full private monitor observation around kernel attach and normal SDL open/enable/disable/close. Retain each request and complete reply pair and error; do not manually replay them to hardware. Record setting writes, input mode changes, IMU rate negotiation and battery/status.
6. **Steam:** fresh Steam listing, details, Begin Test, per-control test, UI stability/re-open, feature `0xae`/attribute/setting exchanges and error replies, then optional passive LED/haptic observations while Steam itself sends them. Do not trigger a firmware update or unsafe commands.
7. **Cleanup:** reconnect and detach observations, controller released back to Puck lane, private logs retained and reviewed. Publish only approved whole safe payloads and source hashes in a *separate physical research PR* with controlled-physical experiment records. No fixture is asserted by this source PR.
8. **Scratch UHID, physically separate:** with no product-code or host-policy changes, use an existing experimental seam and a unique synthetic locally administered unicast Bluetooth-style identity, measured BLE descriptor, bus 5 and `1303`. Assert original `hid-steam` bind, layered hidraw/native sibling behavior, all feature-request responses, SDL open/decode and input-report timing, error/malformed path, Steam UI separately, and idempotent removal/node disappearance. Failed bind or unsupported descriptor must stop without silently falling back to wired.

**All physical capture products** are private until personally inspected. No real addresses or even address-shaped placeholders, unit serials, link keys, host paths, absolute timestamps, raw monitor dumps, raw client logs or unrelated identifying fields may appear anywhere in a public branch. Forbidden firmware/update and pairing/bond writes are never emitted to hardware by an agent.

## Acceptance ledger — evidence needed before implementation/promotion

| Cell | Current evidence | Acceptance required |
|---|---|---|
| Kernel supports `1303` | Source-supported | D9 binding and paired sysfs identity |
| BLE descriptor and report inventory | No physical evidence | Owner-reviewed descriptor and hashes |
| BLE input format and cadence | Source-only parser | Full physical per-control fixtures and relative timings |
| Battery/status/IMU | Source-only parser | Physical reports, rates and consumer readings |
| Feature / lizard lifecycle | Source-only host commands | Paired GET/SET responses plus native/raw handoff |
| SDL input and haptics | Source-only | SDL HIDAPI BLE open, decoding and optional outputs |
| Steam listing/details/Begin Test | No BLE evidence | Owner Steam UI capture and sanitized request/reply ledger |
| Scratch BLE UHID | Not run | Bind/SDL/cleanup, false-positive/failure cases and no leaks |
| True Bluetooth radio / pairing emulation | Deferred | Separate #164 transport gate; not accepted by UHID |

Track requests/constraints on [virtualgamepad #159](https://github.com/anderstvoss/virtualgamepad/issues/159) and [#164](https://github.com/anderstvoss/virtualgamepad/issues/164). The current work is research only. Implementation must wait for the owner-reviewed source and physical evidence plus Wii/Steam API review.
