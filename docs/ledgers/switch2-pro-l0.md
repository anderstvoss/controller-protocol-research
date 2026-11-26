# Switch 2 Pro — L0 source-only Linux / SDL consumer ledger

**Scope:** `switch2-pro`, after Alpha 2, virtualgamepad #171. No host or controller hardware access. Detailed decision table and full pinned links: [starter brief](../switch2-pro-starter.md).

## L0 source facts versus unresolved proof

| Layer | Source-backed state | Claim IDs | Boundary |
| --- | --- | --- | --- |
| Identity and driver selection | Linux v7.4-rc2 has USB product 0x2069; HID + vendor-class bulk USB driver | `switch2-pa2-pro-identity`, `switch2-pa2-usb-split-interfaces` | Registry/driver match, not an observed descriptor |
| Linux evdev | Four signed stick axes, two D-pad hats, independently mapped grip right, grip left and C, capture, conditional FF and LEDs | `switch2-pa2-linux-evdev-gr-gl-c` | No actual evdev event trace |
| Linux reports | Pro 0x09, unified 0x05, separate C/grip bits, calibrated stick decoding | `switch2-pa2-linux-report09` | No physical input report comparison |
| Linux configuration | Bulk command/reply and staged firmware/calibration/features/report selection | `switch2-pa2-linux-init` | No retail ACK or error proof |
| Native rumble | Pro two-slot output command 0x02, distinct from GC 0x03 | `switch2-pa2-linux-rumble` | No actuator response measurements |
| SDL USB and mapping | Direct libusb and interface 1 bulk, Pro Share/C/paddles and joystick sensor slots | `switch2-pa2-sdl-usb-libusb`, `switch2-pa2-sdl-pro-mapping` | Mixed pinned SDL commits, no actual build session |
| SDL startup/output | Bulk initialization and Pro 0x02 HID rumble | `switch2-pa2-sdl-init-rumble` | No host/runtime acceptance |
| Bluetooth | Pinned Linux and SDL paths do not implement Switch 2 Pro Bluetooth | `switch2-pa2-bluetooth-consumer` | No statement about retail wireless hardware capabilities |
| Realization | `linux.uinput` reduced playable first; composite USB provider extension needed for native | `switch2-pa2-uinput-first`, `switch2-pa2-switch1-distinct` | Inferred recommendation; no provider tested |
| Critical unknowns | Full retail descriptors, firmware, HID-only fallback, host event parity and outputs | `switch2-pa2-retail-device-unknown`, `switch2-pa2-hid-only-unknown`, `switch2-pa2-actual-host-observation-unknown` | Unknown until qualified hardware/host testing |

## Evidence lineage

- Linux tag `v7.4-rc2`: `switch2-pa2-linux-hid-v74rc2`, `switch2-pa2-linux-usb-v74rc2`, `switch2-pa2-linux-ids-v74rc2`, `switch2-pa2-linux-kconfig-v74rc2`. Single kernel lineage; per-file SHA-256 and licence locators in source records.
- SDL: existing `sdl-switch2` (Switch 2 native decoder) and `switch2-gc-sdl-libusb` (global direct-libusb selection), pinned at distinct commits. Do not assert one specific SDL release without a coherent build proof.
- Original Switch Pro comparison: existing `audio-sdl-switch-pro`. `switch2-gc-*` claims are sibling research, not Switch 2 Pro physical evidence.
- Existing `switch2-linux-exposure-unknown` and `switch2-physical-corroboration-unknown` **remain open** for measured physical and consumer evidence despite pinned source declarations.

## Decision and future gates

`linux.uinput` offers a reduced **playable** evdev target without native bulk setup. A **faithful** host-facing Switch 2 Pro requires an extended USB composite realization with HID input/output and working vendor-class bulk control. Experimental `dummy_hcd` or USB/IP are future candidates; neither is source-validated for this controller. UHID alone cannot provide USB bulk. Bluetooth-bus UHID metadata does not implement physical pairing.

**Proposed, not run:** source-to-host Linux evdev mapping; SDL libusb permissions/detachment and native raw versus standardized mapping; USB open/close, report and FF reply tests; direct comparison to a non-identifying physical reference; backend composite USB acceptance; HID-only negative test. No firmware reverse engineering in this public corpus.
