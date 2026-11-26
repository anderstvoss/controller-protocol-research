# Xbox 360 Wireless Receiver — Linux xpad and SDL consumer lifecycle

**Evidence:** source-only; no physical receiver, host experiment, pairing, firmware inspection, USB capture, output actuation or live SDL run. Addresses and identity-bearing captures are out of scope.

## Decision table — ranked virtualgamepad consequences

| Rank | Finding | For ADR-0022 and #165 | Playable / faithful | Evidence ceiling | Claim IDs |
| --- | --- | --- | --- | --- | --- |
| 1 | xpad expects vendor USB interface protocol 129 and two interrupt endpoints | A generic HID or uinput controller is not an actual xpad receiver | Faithful requires USB-level emulation | Kernel consumer plus inference | rcv-x360-binding, rcv-x360-usb-provider |
| 2 | Receiver listener exists before a pad input device | Allow an empty receiver and per-slot presence-driven creation | Faithful slot lifecycle | Kernel consumer | rcv-x360-presence, rcv-x360-evdev-epoch |
| 3 | One xpad state machine per bound interface; a second host polls four pipes | Receiver aggregate maps to separately serviced slot interfaces; actual layout must be captured | Faithful multi-slot conditional | Two consumers, no device capture | rcv-x360-four-slot-consumer, rcv-x360-teardown |
| 4 | SDL HIDAPI excludes the receiver and Linux evdev adds/removes each joystick | Do not equate a USB receiver with one SDL joystick; expect new instances on reconnect | Playable through evdev | SDL consumer only | rcv-x360-sdl-evdev |
| 5 | Wireless FF/LED output follows interface-local USB OUT, not app player index | Retain per-slot output routing and uncertain delivery discipline | Faithful output unvalidated | Kernel source, no actuation | rcv-x360-output, rcv-x360-output-epoch-gap |
| 6 | Input product ID and LED index are assigned on attachment | Do not conflate receiver identity, slot ID, LED allocation and game player | Faithful host identity | Kernel consumer | rcv-x360-identity-led |
| 7 | The kernel parser sees headset presence but creates no companions | No xpad keyboard/pointer/audio companion; other drivers may differ | Source-scoped reduced path | Kernel host only | rcv-x360-companion-battery |
| 8 | Physical descriptor and four concurrent connections not captured | Hold fidelity promotion for owner-only lab gates | Unknown physical fidelity | No measurement | rcv-x360-physical-unknown |

## Provenance and non-duplication

The earlier Xbox 360 ledger established a wireless receiver lead (x360-l0-device-wireless-receiver0719-lead) and distinguished standard HID from native XUSB (x360-l0-consumer-xpad-id-usb-binding). This review adds the **previously unrecorded receiver/slot lifetime**, SDL attach semantics and per-interface output/cleanup. It does not repeat the Puck interface study or Xbox Wireless Adapter/xone lifecycle; see existing xbox-xone-receiver-bind and xbox-xone-receiver-clients.

- Linux xpad: [pinned v7.3-rc1 resolved commit](https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c), claim source rcv-x360-linux-v73rc1-xpad, SHA-256 92d10718912544a5360eb7e3c12b12bc151b0070621f478bcf0b787dbd8bf200; licence GPL-2.0-or-later.
- USB Host Shield: [pinned XBOXRECV.cpp](https://github.com/felis/USB_Host_Shield_2.0/blob/e5bc9950ba5389b67ad99175c312154af53df71d/XBOXRECV.cpp), reused source x360-l0-usbhost-receiver; licence GPL-2.0.
- SDL Linux backend: [pinned SDL_sysjoystick.c](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/linux/SDL_sysjoystick.c), reused source sdl-linux-joystick-baseline; licence zlib.
- SDL HIDAPI Xbox 360: [pinned SDL_hidapi_xbox360.c](https://github.com/libsdl-org/SDL/blob/829a65d769d935c4852f8159e964312c0957260a/src/joystick/hidapi/SDL_hidapi_xbox360.c), reused source x360-l0-sdl-hidapi-360-3418; licence zlib.

The SDL sources are pinned at distinct upstream commits, not asserted to be one synchronized release. No GPL source code is reproduced.

## 1. USB identity, interfaces and four-slot interpretation

The xpad table maps 045e:0719 and related 045e:0291 and 045e:02a9 to XTYPE_XBOX360W; the wired 045e:028e path is XTYPE_XBOX360 (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L123-L131). Vendor-specific interface matching requires subclass 93 and wireless protocol 129 rather than wired protocol 1 (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L469-L481). Probe requires two endpoints, detects IN and OUT interrupt endpoints, and allocates **one separate xpad context for each USB interface** (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L2044-L2160). This is USB interface binding, not UHID report-descriptor matching.

Independent USB Host Shield host software polls **four input pipes** and routes outgoing status, LED and rumble to a controller-indexed pipe (https://github.com/felis/USB_Host_Shield_2.0/blob/e5bc9950ba5389b67ad99175c312154af53df71d/XBOXRECV.cpp#L283-L316, https://github.com/felis/USB_Host_Shield_2.0/blob/e5bc9950ba5389b67ad99175c312154af53df71d/XBOXRECV.cpp#L537-L568). This supports a four-slot consumer model but does **not** prove a specific retail receiver has four identical interfaces, endpoint numbers, or a stable device-side slot identity. The kernel does not centrally allocate four protocol slots inside one xpad context. Slot interface numbering and descriptor variations remain host-test gaps.

## 2. Slot presence and input-device lifetime

The wireless interface starts receiving at USB bind, without allocating a joystick input node, and sends a status inquiry to discover attached pads (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L1847-L1875, https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L2186-L2209). Its parser treats byte 0 bit 3 as a status change and byte 1 bit 7 as pad present; byte 1 bit 6 is a headset indication. Ordinary input is decoded only when a valid-pad report is recognized and a non-null RCU input pointer exists (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L987-L1024). These are **consumer parser expectations**, not a device wire capture.

The presence worker creates/registers a controller input node and LED class device when the controller arrives. On loss it clears the RCU pointer, synchronizes in-progress readers, and unregisters the input and LED nodes. Reconnection allocates a new Linux input object, not a permanently allocated empty slot device (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L961-L983, https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L1924-L2036). Consequently applications must handle evdev removal and a new joystick instance; Linux event number reuse and rapid status edge races require measurement.

## 3. Per-slot identity, battery, light assignment and companions

The Linux input identity for a connected wireless controller is assigned product ID 0x02a1 rather than reusing the USB receiver product ID (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L1933-L1959). An xpadN LED index is allocated globally when the controller input comes up, used to choose a light pattern, and freed on removal (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L1700-L1768). This index is **not a receiver protocol slot ID** and is **not** GamepadManager's player allocation. The reviewed xpad code contains no persisted per-pad identity mapping across disconnect/reconnect.

The xpad wireless parser sees a headset-presence indication but creates no headset/audio, keyboard or pointer input node from it. This path has no kernel battery power-supply registration (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L987-L1024, https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L1924-L2036). The separate USB Host Shield implementation issues battery inquiries (https://github.com/felis/USB_Host_Shield_2.0/blob/e5bc9950ba5389b67ad99175c312154af53df71d/XBOXRECV.cpp#L537-L556); this does not imply xpad exposes battery state or establish absence of device-side battery/headset features.

## 4. Output routing, slot loss and receiver failure

The wireless FF_RUMBLE formatter uses a 12-byte command distinct from the wired 8-byte output; LED commands likewise use a wireless-specific command. The per-interface xpad context owns the interrupt OUT endpoint, the queued command structures and their URB (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L1293-L1391, https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L1530-L1585, https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L1661-L1718). There is no global application player index in the output path. The ordinary FF and LED userspace endpoints are unregistered with the pad, so an absent slot has no new conventional userspace FF/LED callback.

The per-slot detach path does not visibly flush every already queued output item. Source alone cannot prove that an in-flight or pending command is cancelled, safely applied, or prevented from affecting a later attachment. **No delivery or replay behavior is verified**. ADR-0022's stronger rule remains necessary: a stateful command with uncertain delivery is not blindly replayable.

Each bound interface has separate presence work, pad state and USB input/output resources. A one-slot presence removal does not directly unregister sibling contexts. Physical receiver unplug invokes disconnect on every bound interface, stops the wireless listener and worker, unregisters input/LED, then deinitializes output resources (https://github.com/torvalds/linux/blob/cee9395acd8043be0644b25c34bfa86623f2b935/drivers/input/joystick/xpad.c#L2044-L2247). A shared USB error, concurrent disconnect ordering, resource exhaustion, suspend/resume and sibling survival under real faults remain untested.

## 5. Pinned SDL consumer interpretation

SDL's Xbox 360 HIDAPI driver explicitly **rejects wireless receiver IDs and protocol 129**, rather than interpreting their data as wired Xbox 360 reports (https://github.com/libsdl-org/SDL/blob/829a65d769d935c4852f8159e964312c0957260a/src/joystick/hidapi/SDL_hidapi_xbox360.c#L86-L105). SDL's Linux evdev driver handles input-node discovery via udev or scanning, assigns a new SDL joystick instance on each added node and dispatches removal for a vanished node (https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/linux/SDL_sysjoystick.c#L277-L341, https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/linux/SDL_sysjoystick.c#L383-L413, https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/linux/SDL_sysjoystick.c#L434-L567). Therefore the software model predicts distinct SDL joystick add/remove events for occupied receiver slots, instead of a single composite SDL joystick. Actual SDL selected driver, enumerated GUID, node names, timing and hotplug handling require live validation.

## 6. Realization feasibility and ADR-0022 alignment

ADR-0022's separation of one receiver lifetime, 0–4 typed protocol slots, slot-local loss and receiver-wide cleanup is appropriate. For this particular receiver **the actual USB-level topology is a required part of the host-visible contract**. Merely emitting four uinput gamepads can achieve reduced, playable evdev compatibility but cannot make Linux xpad bind as a receiver. UHID cannot create the required USB vendor-specific interface and interrupt OUT endpoints.

Potential faithful test vehicles are a custom USB gadget modeled through Linux dummy_hcd or an equivalent fully implemented USB device connected through USB/IP. Those are transport options, **not ready-made receiver emulators**; the custom descriptor, presence/status handling and endpoint-driven output still need implementation and test. Do not claim that virtualgamepad's existing Xbox 360 standard-HID identity is proprietary XUSB or the receiver. Keep host-visible slot identity, LED index and GamepadManager player assignment separate. No controller code change is proposed here.

## 7. Owner-only validation gates — NOT RUN

| Gate | Required experiment and recorded success criteria |
| --- | --- |
| R2-1 | Privately inspect original and third-party receiver USB descriptors; publish reviewed non-identifying interface class/protocol, count and endpoint types, and compare with xpad matching |
| R2-2 | Attach zero to four controllers; verify USB receiver survives with none, and individual evdev/LED objects appear only for active slots |
| R2-3 | Remove and reconnect one slot while siblings remain; record new SDL instance, node re-creation and LED reassignment without publishing identifiers |
| R2-4 | Independently issue bounded per-slot FF/LED and verify correct USB endpoints, effect actuation and no feedback leakage |
| R2-5 | Disconnect during queued FF/LED commands; distinguish definitely-unsent, uncertain and completed writes and prevent unsafe replay |
| R2-6 | Inspect headset-presence and battery handling through actual Linux consumers; verify no invented keyboard/pointer companion |
| R2-7 | Unplug and resume receiver with occupied slots; capture teardown ordering, sibling isolation and rollback under USB errors |
| R2-8 | Compare the same SDL/evdev consumer with a generic reduced uinput controller versus a modeled USB dummy_hcd/USB/IP receiver; record xpad binding separately from mere playable controls |

No physical receiver data is committed. If a gap requires examining vendor firmware, it **needs private analysis** and remains outside this public research.
