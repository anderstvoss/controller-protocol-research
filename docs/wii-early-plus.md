# Early integrated Wii Remote Plus (`057e:0306`)

**Evidence boundary:** source-only revision analysis at controller-protocol-research main `e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7`. No early integrated retail sample, virtual host run, Bluetooth pairing trial or physical capture was available. All proposed experiments are **not run**.

## Revision model and scope

The early RVL-036 Wii Remote Plus has integrated MotionPlus yet advertises the original Wii Remote Bluetooth HID identity: Nintendo RVL-CNT-01 and 057e:0306. This overlaps the original RVL-003 identity. The later TR Plus advertises Nintendo RVL-CNT-01-TR and 057e:0330. Neither vendor/product identity nor shell color proves the early integrated sensor is present on a particular connected unit. The pinned xwiimote device catalogue describes early integrated hardware as similar to an original Remote with MotionPlus internally attached; that description is **not** a byte-for-byte equivalence measurement.

Existing records establish the shared identity and TR behavior: `wii-gap-plus-physical-revision-taxonomy`, `wii-gap-early-plus-kernel-name-ambiguity`, `wii-gap-plus-integrated-mp-presence-and-identity-gap`, the `wii-gap-plustrace-*` consumer records, and the outstanding `wii-early-plus-revision-gap`. This brief limits its new findings to **conditional early 0306 consumer behavior**. No previous record is edited or promoted to physical evidence.

## Gen 1 probe, kernel devtype and xwiimote

| Component | Pinned source-derived behavior | Implication for early 0306 |
| --- | --- | --- |
| Linux hid-wiimote v6.12 classifier | Old exact name or 0306 selects gen10; TR name or 0330 selects gen20. Gen20 loads BUILTIN_MP, gen10 does not. | Early 0306 is reported as **gen10**, not gen15, even when the MP probe later succeeds. |
| Linux initial/reconciliation MP probe | Initialize A600 then read six bytes from A600FA; accepts length 6 and final byte 0x05. Later mapped modes are read at A400FA and mode writes choose 0x04 / 0x05 / 0x07. | Both built-in-style and external-style inactive suffixes can satisfy the loose probe. A responding early unit gains a MotionPlus evdev child without requiring a Gen 2 identity. |
| Linux idle discovery | On gen10, four-second polling reads inactive MP; opening the MotionPlus node activates MP_USED and enables the mapped path. Gen20's built-in policy suppresses periodic idle polling, not all reconciliation. | A Gen 1-style timing and probe pattern matters; simply copying TR discovery may conceal an early-unit timing difference. |
| xwiimote | Public header allows descriptions such as gen15 for first-generation integrated Plus, but the pinned kernel has no gen15 devtype. libxwiimote follows a bound wiimote HID parent and kernel evdev siblings rather than probing A600 itself. | A gen10 kernel devtype with a MotionPlus evdev node is a coherent early-Plus discovery outcome; gen15 is **not** a guaranteed Linux string. |

Pinned references: [Linux classifier and module list](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-core.c#L570-L605), [kernel identification/probing](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-core.c#L513-L530), [initial detection and polling](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-core.c#L811-L933), [reconciliation](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-core.c#L1100-L1224), [xwiimote device labels](https://github.com/xwiimote/xwiimote/blob/4df713d9037d814cc0c64197f69e5c78d55caaf1/lib/xwiimote.h#L93-L115), [xwiimote device handling](https://github.com/xwiimote/xwiimote/blob/4df713d9037d814cc0c64197f69e5c78d55caaf1/lib/core.c#L335-L393). Sources are GPL-2.0-only (Linux) and xwiimote permissive-licensed (xwiimote); no upstream excerpts are reproduced.

## Inactive versus active MotionPlus IDs

| Reader | Inactive probe | Active / mapped detection | Does it distinguish early integrated from original plus external? |
| --- | --- | --- | --- |
| Linux v6.12 | A600FA/6, reply length 6 and byte 5 = 0x05 | A400FA/6; mapped bytes 4–5 = 0x04 0x05, 0x05 0x05 or 0x07 0x05 | **No**, not by MP identity. Kernel devtype remains gen10 for 0306. |
| wiiuse e769bd7 | A600FA/6; interprets last four bytes A4200005 built-in or A6200005 external (also selected no-longer-active codes) | After A600 setup/mode writes 0x04 or 0x05, accepts mapped suffixes A4200405, A4200505, A4200705 | **Yes** at the inactive identity predicate; then shared motion setup and decode paths. Does not prove the real early response. |
| SDL 3.2.10 Wii HIDAPI | Reads A600FE/2 if A400FE/2 does not already identify MP; masked 0xF0FF result 0x0005 | A400FE/2 identifies mapped MP; on Linux activation writes are omitted in favor of kernel-owned mapping | **No full built-in/external ID comparison** in this predicate. No guaranteed gyro without kernel and joystick-state success. |
| Cemu 29f2f1 | A600FA/6 shares a lower-address reply handler with A400FA/6 | A6200005 external branch invokes MP activation, A4200005 built-in branch only notes inactive; its gyro export remains source-limited | **Yes**, with a consequential built-in inactive nonactivation path. Both 0306 and 0330 pass HID enumeration. |
| Dolphin 3eb30c | Native discovery accepts 0306 and 0330; setup probes inactive A600 registers when motion is desired | Tracks mapped A400 identity, chooses mode, then requires MP calibration and conditionally F6/40 child data | **No explicit early-integrated discriminator** in the reviewed native setup. Native acceptance and real calibrated gyro remain unmeasured for early 0306. |
| xwiimote 4df713 | No independent native MP-register probe | Opens kernel-created MotionPlus evdev interface, consuming kernel gyro axes | Delegates identity and mapping to kernel. |

The WiiBrew oldid 121955 source record notes possible **built-in** inactive values at different register banks, including an ordinary extension-bank 00 00 A4 20 00 05 identity at A400FA and a possible unencrypted 01 00 A6 20 00 05 at A600FA. WiiBrew oldid 120079 separately describes an external inactive A600 identity. These community documents are **not** an exact early retail six-byte capture. In particular, a consumer's four-byte constant cannot be expanded into invented leading bytes, and no single built-in response should be asserted as universal.

Pinned references: [wiiuse inactive setup](https://github.com/wiiuse/wiiuse/blob/e769bd73860a4f941bd110ebae5a790f968b71e3/src/motion_plus.c#L45-L104), [wiiuse mapped identity](https://github.com/wiiuse/wiiuse/blob/e769bd73860a4f941bd110ebae5a790f968b71e3/src/motion_plus.c#L106-L198), [wiiuse constants](https://github.com/wiiuse/wiiuse/blob/e769bd73860a4f941bd110ebae5a790f968b71e3/src/wiiuse_internal.h#L223-L239), [SDL probe](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L385-L427), [SDL Linux mode policy](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L457-L491), [Cemu identity dispatch](https://github.com/cemu-project/Cemu/blob/29f2f1fae4631e2317977debd9eacd55cc28dd7d/src/input/api/Wiimote/WiimoteControllerProvider.cpp#L324-L381), [Dolphin accepted IDs](https://github.com/dolphin-emu/dolphin/blob/3eb30c7620b4475b2e0404228ba0d2b238a132f1/Source/Core/Core/HW/WiimoteReal/WiimoteReal.cpp#L1009-L1036), [Dolphin setup](https://github.com/dolphin-emu/dolphin/blob/3eb30c7620b4475b2e0404228ba0d2b238a132f1/Source/Core/InputCommon/ControllerInterface/Wiimote/WiimoteController.cpp#L449-L657). wiiuse and Dolphin are GPL-licensed; SDL uses zlib and Cemu MPL-2.0. Links reference pinned revisions; no source excerpts are reproduced.

## What an early-Plus virtual personality would need

**Source-compatible subset:** preserve Nintendo RVL-CNT-01 and 057e:0306 while declaring a non-detachable, logically activatable MotionPlus sensor. Keep a shared Wii Remote engine, host-driven 0x15/0x20 status, writable A600 initialization/mode changes, coherent inactive A600 and active mapped A400 banks, optional external-port Nunchuk/Classic semantics, and controlled gyro/report data. Unlike a TR personality, this one must tolerate the **gen10 four-second hotplug path**, which does not set BUILTIN_MP, and it must not falsely treat devtype gen10 as absence of a gyroscope. The identity policy differs from TR, while the actual native report semantics may be shared only as a **compatibility approximation**.

**Differences from original with external MP:** both can enumerate as 0306 and expose a MotionPlus node. Physically the early Plus has a built-in gyro rather than a user-removable adapter. A 0306 identity cannot tell the app which configuration is present. wiiuse and Cemu have code paths that distinguish candidate inactive IDs; Cemu may not activate a built-in-style reply. SDL, kernel and Dolphin do not establish a reliable physical discriminator from that identity alone. Preserve explicit creation-time revision choice and avoid automatic guessing.

**Still unknown:** actual early-unit A600FA/6 and A600FE/2 bytes before and after activation; whether A400FA/6 and F6/40 readbacks match external adapters; true timing and state-edge order for MP activation, status bits and downstream attachments; real EEPROM calibration/CRC and factory gyro scale; extension encryption/challenge details; Bluetooth pairing/reconnect and native consumer results on a real early unit. Prior TR virtual-host tests do not validate this early revision. The existing `wii-early-plus-revision-gap` remains **unknown**.

**Not run:** any physical 0306 early-unit capture, an original plus external-MP comparison, native Linux/SDL/Dolphin/Cemu trials, or radio and timing tests. Research #52 remains the deferred owner lab; this brief neither runs nor replans it. No firmware, EEPROM image, device identifiers, keys or private capture data are supplied.

## Decision table

| Option | Source-supported case | Unknown / tradeoff | Decision |
| --- | --- | --- | --- |
| Realize as its own revision | Different 0306 identity and Gen 1 kernel/polling behavior; integrated physical sensor; consumer-specific inactive ID branches; use existing shared engine | Actual early reply bytes and physical calibration are unknown; source-based candidate only | **Preferred for an explicitly labeled, opt-in compatibility revision** with separate acceptance, not a fidelity promise. |
| Fold into original Remote plus external MotionPlus | Shared 0306 enumeration, many downstream mapped MP and gyro paths can reuse implementation | Loses non-detachable built-in model and may give Cemu/wiiuse the wrong inactive reply; identity alone is ambiguous | **Use code reuse only**. Do not collapse distinct claimed hardware revisions or inherit Original passes. |
| Wait for hardware | Provides a path to establish full early-unit IDs, timing, calibration and cross-consumer acceptance | Delays a potentially useful source-only compatibility prototype | **Required before physical-fidelity or validated early-Plus claims**, not required for a clearly bounded research/compat preset. |

## New claim IDs and existing evidence

- `wii-gap-earlyplus-gen10-probe-and-devtype`
- `wii-gap-earlyplus-xwiimote-gen15-label`
- `wii-gap-earlyplus-wiiuse-inactive-versus-active-id`
- `wii-gap-earlyplus-sdl-suffix-not-revision-gate`
- `wii-gap-earlyplus-cemu-builtin-inactive-branch`
- `wii-gap-earlyplus-dolphin-native-no-early-discriminator`
- `wii-gap-earlyplus-revision-preset-not-physical-parity`

New claim count for Wii Remote L0: **246** (239 on the pinned main plus seven new claims). Existing unknown records and historical ledger checkpoints remain unchanged.
