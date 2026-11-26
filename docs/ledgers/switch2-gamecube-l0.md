# Switch 2 GameCube controller — L0 post-Alpha 2 evidence ledger

**Scope:** source-only starter synthesis for virtualgamepad #360. **State:** no physical or virtual-host run, no product implementation, no new source or claim records. This device is separate from the WUP-028 adapter in #296. The legacy registry tracking field still names #296 and is deliberately unchanged.

## Decision summary

| Tier | Recommended mechanism | Status / acceptance boundary |
| --- | --- | --- |
| Playable-first | `linux.uinput` reproducing Linux GameCube evdev sticks, hats, analog triggers, distinct click/buttons and available FF | **Proposed, not run.** Generic consumers only until independently tested. |
| Native USB-faithful | A **new USB-level vendor-bulk personality/provider**, possibly based on USB/IP/VHCI or a new appropriate dummy_hcd function | **Research required.** Existing `linux.usbip.usb-audio` is not the required bulk protocol; current `linux.dummy_hcd.usb-hid` unavailable. |
| HID metadata-only | `linux.uhid.usb` | **Not USB-equivalent.** Cannot supply USB bulk endpoints or native libusb discovery. |
| Bluetooth | No reviewed GameCube transport evidence in this corpus | **Unknown**, no negative device claim. |

## Source-only claim map (existing record IDs, unchanged)

| Claim ID | Evidence role and status | Starter implication / limit |
| --- | --- | --- |
| `switch2-gc-direct-libusb-identity` | consumer; independently corroborated | SDL native libusb and Linux USB PID matching; not measured enumeration |
| `switch2-gc-dynamic-bulk-endpoints` | consumer; independently corroborated | Interface/endpoint discovery requires real USB-level plumbing |
| `switch2-gc-command-handshake` | consumer; independently corroborated | USB bulk request/reply startup is part of faithful behavior |
| `switch2-gc-report0a-linux` | consumer; source supported | Dedicated report 0x0a and unified report 0x05, not captured |
| `switch2-gc-linux-evdev-presentation` | consumer; source supported | Baseline for first playable uinput presentation |
| `switch2-gc-distinct-controls` | consumer; independently corroborated | Preserve C, analog triggers and distinct click controls |
| `switch2-gc-trigger-zero-calibration` | consumer; independently corroborated | Consumer calibration reads; never infer private values |
| `switch2-gc-identity-calibration-consumer` | consumer; independently corroborated | Metadata and calibration request behavior, no physical ID |
| `switch2-gc-rumble-binary` | consumer; independently corroborated | Simple rumble command 0x03, not Pro HD rumble |
| `switch2-gc-retail-physical-unknown` | device; unknown | All physical equivalence and actuation claims remain open |

## Reused pinned source records

- `sdl-switch2`: SDL `fe2bca9748afa754ebbca4c543c5b28bbce30cf4`; SHA-256 `204daf9ce1a9d2548ce233c4e296f26a174dc336c97bc2f450b44ad1c37658c3`; zlib, SDL lineage.
- `switch2-gc-sdl-libusb`: SDL `d6fbbbe14dddfa09d6168267a0fcd39dea5a398a`; SHA-256 `fb7c91544a114c4a77e9fe28755cd2da5aa8cf106026e4c2a786a441887bf2fe`; zlib, same SDL lineage.
- `switch2-gc-linux-usb`: Linux `9417132df63e5cd7230433af05198538e759f3ae`; SHA-256 `c0bed151d80471552ec7cb0a0254a4084e00ec2cf99fde5da88aa5214cde2bb4`; GPL-2.0-or-later, Linux lineage.
- `switch2-gc-linux-hid`: Linux `77c7155e2707ba5b1d56f3dc1acead48cf17f98d`; SHA-256 `24c36517d7030a3fb5d46131314e356cca931562c55bf028bb091dd4690c360d`; GPL-2.0-or-later, same Linux lineage.

The brief `docs/switch2-gamecube-starter.md` gives revision-pinned **file/line links** for each source. Source hashes are inherited from existing, unmodified corpus records; separate lines from the same repository are not counted as independent confirmations.

## Outstanding checks — none run

The existing `docs/switch2-gamecube-physical-capture-plan.md` defines bounded S0–S5 owner-operated runs. Before support promotion also require uinput/SDL generic recognition, raw USB-level libusb+kernel acceptance, reverse rumble, lifecycle/per-instance identity and permissions checks. Run controller-specific device evidence and virtual-host consumer acceptance separately. No raw identifiers, firmware, private calibration contents or host traces are included here.

**Claim IDs newly created:** none. Existing ten claims retain their original status and scope.
