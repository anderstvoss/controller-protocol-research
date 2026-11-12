# GameCube USB adapter — descriptor and status-bit gap review (round 2)

Source-only follow-up for `gamecube-usb-adapter` (Nintendo WUP-028-compatible identity, 0x057e:0x0337); tracking: [virtualgamepad #296](https://github.com/anderstvoss/virtualgamepad/issues/296). **No host or physical test was run.** The existing records remain unchanged.

## Ranked gaps and evidence ceiling

| Rank | Gap and implication | Playable / faithful | Evidence ceiling | Related records / issue |
| --- | --- | --- | --- | --- |
| 1 | Configuration, interface and interrupt endpoint layout, including bInterval. One HID interface and 37-byte IN / 5-byte OUT endpoints at nominal 8 ms are now documented by two published host dumps. | Faithful; the `linux.uinput` playable path is not blocked | **Device source-supported** only; published captures are not this project's hardware validation | `gc-cgap-published-usb-interface`, `gc-cgap-published-interrupt-endpoints`, `gc-adapter-descriptors-unknown`; #296 |
| 2 | Control EP0 and report descriptor bytes. Published EP0 sizes disagree (8 versus 64); two dumps provide only the 214-byte HID report *length*, not its bytes. A separate emulator provides a provisional byte model, including a report-length inconsistency. | Faithful | **Device source-supported** for EP0 disagreement and length; **consumer source-supported / inferred** for emulated HID bytes | `gc-cgap-control-endpoint-packet-size-variance`, `gc-cgap-emulated-hid-descriptor-model`, `gc-cgap-hid-report-length-tension`, `gc-adapter-descriptor-details-unconfirmed`; #296 |
| 3 | Remaining port status bits: WaveBird `0x22` communicating versus `0x20` not communicating or differently presented by consumers. | Faithful; playable port attach semantics affected by policy | **Consumer source-supported** only; actual transitions still unmeasured | `gc-cgap-wavebird-status-consumer-divergence`, `gc-adapter-remaining-status-unknown`, `gc-adapter-port-type-bits`; #296 |

## Device statements: published USB enumerations

Two different archived `lsusb` files in the [linuxhw/LsUSB archive](https://github.com/linuxhw/LsUSB) identify the adapter by USB vendor/product ID. These are **third-party device reports**, rather than direct host measurements here. They agree on USB 2.00, device revision 1.00; one configuration of total length 41 bytes and value 1; a single HID-class interface 0 / alternate setting 0 / subclass 0 / protocol 0; HID 1.10 and report descriptor *length* 214; configuration attributes `0xe0` and advertised maximum power 500 mA. Both name interrupt IN endpoint `0x81`, 37 bytes, and interrupt OUT endpoint `0x02`, 5 bytes, with `bInterval` 8. At full speed, the descriptor's 8 ms nominal interval corresponds to 125 polls/s, **not a measured delivery rate**. Relevant claims: `gc-cgap-published-usb-interface`, `gc-cgap-published-interrupt-endpoints`.

The archives differ in `bMaxPacketSize0`: one reports **8 bytes**, another **64 bytes**. The logs cannot establish whether the units were original Nintendo devices, clones or hardware revisions. Do not assign a universal control endpoint value or use the HIDMaestro choice as physical corroboration; retain the divergence under `gc-cgap-control-endpoint-packet-size-variance`.

These files include other USB devices and potentially identifying host information. Only pinned URL, file hash and safe adapter-specific line intervals enter the corpus; no full logs or identifying strings are reproduced.

## Consumer expectations: HID report and native access

A pinned [HIDMaestro adapter profile](https://github.com/hifihedgehog/HIDMaestro) emulates USB/IP enumeration with the layout above, selecting the 8-byte EP0 variant. It includes a 214-byte HID report descriptor and models four ports and report `0x21`. **This is software behavior, not an independent real-device descriptor capture.** The HID descriptor's declared 37 bytes of data for report ID `0x21` are in tension with a 37-byte USB transfer inclusive of the report ID (which contains 36 subsequent bytes). Preserve the byte model as a comparison target, without treating it as proof that conventional HID parsing accepts it: `gc-cgap-emulated-hid-descriptor-model`, `gc-cgap-hid-report-length-tension`.

Existing `gc-adapter-consumers-require-usb-device` remains the realization gate: SDL's native adapter and Dolphin's backend reach the USB device through libusb, not a `linux.uhid.usb` identity or four uinput pads. The new descriptors narrow what a future **USB-level** implementation should compare; they do not make that provider available, and the playable `linux.uinput` route remains a separate four-evdev-pad compatibility target. Existing Hinara `gc-adapter-hinara-kernel-evdev` derives URB interval from an endpoint descriptor and therefore did not supply a numeric interval.

## Consumer status-bit interpretations

- **Nintendont:** its pinned parser accepts wired `0x10` or a communicating WaveBird pattern `0x22`; `0x20` by itself does not pass that presence test.
- **RetroArch:** its pinned WUP-028 HID consumer recognizes `0x22` specifically as WaveBird but uses a broader non-power-only port-presence threshold, admitting `0x20` into its generic path.
- **HIDMaestro:** its simulated device assigns `0x22` to communicating wireless and `0x20` to non-communicating wireless.

These implementations are not three independent physical measurements, and their provenance can overlap. No new bit is physically established. The old `gc-adapter-port-type-bits` description of `0x20` as WaveBird type is not necessarily a sufficient **connected** predicate. Avoid implementing `0x20` as a universally usable controller without an explicit compatibility policy and a hardware validation gate. See `gc-cgap-wavebird-status-consumer-divergence`.

## Source lineage and limits

| Source ID | Role | Pinned file and lines | Limit |
| --- | --- | --- | --- |
| `gc-cgap-linuxhw-ep0-8` | Published device report | Linuxhw archive, lines 100–168; CC-BY-4.0 | Not author-verified original hardware; EP0 8 bytes |
| `gc-cgap-linuxhw-ep0-64` | Published device report | Linuxhw archive, lines 3–68; CC-BY-4.0 | Not author-verified original hardware; EP0 64 bytes |
| `gc-cgap-hidmaestro-profile` | Compatibility implementation | HIDMaestro profile, lines 13–16, 24–35, 72–95; MIT | Downstream emulation; cannot substitute for physical report descriptor |
| `gc-cgap-nintendont-padread` | Consumer implementation | Nintendont PADReadGC, lines 410–422; GPL-2.0 project | Only one client's status predicate |
| `gc-cgap-retroarch-wiiugca` | Consumer implementation | RetroArch WUP-028 connector, lines 28–33, 273–301, 321–335; GPL-3.0 | Only one client's status predicate |

Hashes, immutable revisions and full source paths are recorded in `records/source/`. Existing SDL/Dolphin, ToadKing, Hinara and Cemu/Eden claims and source records are reused by ID; no copies or changes. No vendor firmware was analyzed. No code has been copied from GPL projects.

## Proposed physical and host checks — NOT RUN

1. On an owner-approved host, enumerate an authentic WUP-028 and identified third-party Wii U-mode units separately. Collect sanitized device, configuration, interface, endpoint and HID report descriptors; verify both advertised `bInterval` and the differing EP0 packet sizes. Record actual provenance and controller version without publishing identifying strings.
2. Confirm the exact HID report bytes and report ID / payload length discrepancy using a hardware-approved descriptor read, distinguishing transfer length from HID report declaration. Do not infer behavior from the emulator alone.
3. With a wired controller and a WaveBird receiver, vary connected / communicating / powered states separately and record per-port raw status changes. Test `0x20` versus `0x22` presence and output behavior, without assuming a universal meaning for other bits.
4. If a USB-level virtual realization becomes available, test libusb discovery and interface claim through SDL and Dolphin, bidirectional `0x13` / `0x21` / `0x11` behavior and actual input latency. Do not treat nominal `bInterval` as measured production cadence. Compare separately against four uinput pads.

**No acceptance, validation or device-physics promotion** is implied by this source-only update.
