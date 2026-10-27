# W8 caller-image Cemu and native Dolphin baseline

These seven arms are virtual-host consumer observations. They do not establish
physical Wii Remote compatibility, calibration, audio, radio or game acceptance.
Code baseline: `0da0d020bdcd5c28d6b63dd5007783c855e7e53c`. Cemu is the installed
ARM64 AppImage at commit `29f2f1f`; native Dolphin is Debian ARM64 2503,
package `2503+dfsg-1+deb13u1`. Fixtures pin binaries and private artifact hashes.
Each completed arm is bounded to 35 seconds with a fresh application profile,
owned-device access, radio sockets denied and cleanup before the next profile.
Protocol state is warm and reused within each producer; no cold-isolation claim.

| Arm | First unpassed protocol checkpoint | Record prefix |
| --- | --- | --- |
| Cemu image, MP, no external holder | Extension identity exchange; no native calibration request at `0x20` | `wii-w8-cemu-image-motionplus-no-holder` |
| Cemu image, MP, external holder | Repeated identity exchange; no native calibration request at `0x20` | `wii-w8-cemu-image-motionplus-holder` |
| Cemu image, MP+Nunchuk, no external holder | Nunchuk calibration: 18 register reads at A40020/16 receive error 7 | `wii-w8-cemu-image-motionplus-nunchuk-no-holder` |
| Dolphin default, MP | Empty EEPROM blocks base calibration | `wii-w8-dolphin-default-motionplus` |
| Dolphin default, MP+Nunchuk | Empty EEPROM blocks base calibration | `wii-w8-dolphin-default-motionplus-nunchuk` |
| Dolphin image, MP | Speaker mute acknowledgement before MP setup | `wii-w8-dolphin-image-motionplus` |
| Dolphin image, MP+Nunchuk | Speaker mute acknowledgement before MP setup | `wii-w8-dolphin-image-motionplus-nunchuk` |

Each prefix has its own `-result` claim, `-host-run` experiment and `-host`
fixture. The seven baseline claims raise the Wii count from 138 to 145 at that stage without
changing source-only gaps or promoting physical evidence. Earlier W7 records
are historical and remain unchanged.

The synthetic caller EEPROM image covers both 10-byte accelerometer blocks and
has valid additive checksums. The 512-unit centre and 104-unit one-g delta are
lab choices from pinned Dolphin emulator fallback constants, not a codec factory
scale or retail data. The existing caller-image API imports it privately; no
project default or published image bytes are added. Cemu's base EEPROM read now
succeeds. Its MP+Nunchuk sequence identifies Nunchuk before the register-space
`0x20` request, distinguishing it from EEPROM `0x0020` and MP calibration.

Dolphin's own file logs are primary. All four usable native runs show HIDAPI
discovery and ControllerInterface device addition. The installed binary omits
the inspected debug success strings despite debug configuration, so notice and
warning messages are supplemented by private owned-I/O traces. Offscreen
attempts yielded no useful own log and are excluded. Visible Qt runs worked.
With an empty EEPROM, the own log reports base-calibration failures. With the
caller image, the base read succeeds and those failures disappear, followed by
repeated speaker mute output `0x19` and handler expiry. No native MP calibration
request occurs within those image-only bounds.

Ladder limits remain explicit: temporary usability writes are transport evidence,
not proof that their status request was accepted. ControllerInterface addition
does not demonstrate mapping UI selection. Buttons, accelerometer, visible IR
and gyro have no decoded application-state oracle here. The source task order
and own handler-expiry log place the image-only protocol stall in speaker setup
before MP activation/calibration; shared kernel traffic is not sole-actor proof.
No kernel-binding warning was observed, and hid-wiimote was not unbound. Native
enumeration succeeded, so the fallback hidapi diagnostic was unnecessary.

Dolphin can open its own evdev companion nodes; “no external holder” does not
mean absence of kernel MP use. Cemu's explicit external holder is recorded
separately. Raw bytes, logs, identities, paths and binaries remain private.
All completed consumers are gone and their owned nodes were verified removed.

The earlier stop instruction prevented the fourth Cemu baseline arm. The later
owner decisions authorize separate imported-calibration and speaker-control ACK
PRs, both for Anders to merge. Those changes merged as `0c36691` and `5a11e50`; the post-merge results follow.


## Post-merge imported-block results

The reruns use merged code `5a11e507ac973c23ca10beb36edb44fc35034376` with
the same caller EEPROM image plus synthetic MP and Nunchuk imports. The MP
block uses the pinned emulator fallback layout, a 16-bit zero of 32768, scale
offset 17408, fast/slow degree scales of 1200/270 and non-retail UID placeholders.
The Nunchuk block uses a 512-unit centre, 616-unit one-g value and caller-chosen
stick min/max/centre of 0/255/128. CRC32 and additive checksums were independently
validated. No resource bytes or images are published or installed as defaults.

| Arm | Bound and result | First unpassed checkpoint |
| --- | --- | --- |
| Dolphin imported MP | 180-second transport arm plus 150-second mapping observation; MP calibration read succeeds in two chunks | No failure observed through mapped gyro within this scope |
| Dolphin imported MP+Nunchuk | 180 seconds; mapped device visible and active mode 5 | 12,128 A400F6/4 reads receive error 7 before MP calibration |
| Cemu imported MP | 35-second coexistence arm; base EEPROM succeeds | Repeated mapped/unmapped identity initialization, including A600FA error 7; decoded state unobserved |
| Cemu imported MP+Nunchuk | 35-second coexistence arm; base EEPROM and 44 A40020/16 reads succeed | Replies match the MP block first half while mapped; no clean Nunchuk-path or decoded-gyro pass |

The two Dolphin prefixes are `wii-w8-dolphin-imported-motionplus` and
`wii-w8-dolphin-imported-motionplus-nunchuk`. Cemu uses
`wii-w8-cemu-imported-motionplus` and
`wii-w8-cemu-imported-motionplus-nunchuk`, each with its own claim, experiment
and reduced fixture. The current Wii inventory is 149 claims.

For MP-only, the owned native mapping window visibly lists the Bluetooth
ControllerInterface device. Inspected private samples show A alternating
between active and inactive; acceleration preview changes between displayed
1.37 g and 2.27 g; two basic IR points move; and the gyroscope indicator changes.
The UI profile uses explicit bindings and sets its additional gyro
auto-calibration period to zero. Source-backed basic IR vectors are driven only
while a basic-capable report mode is selected. These are application-state
observations with synthetic calibration, not proof of accurate rates, physical
calibration, all controls or complete-controller acceptance. A private emulated
mapping slot is used; no Real slot or game content is used.

For MP+Nunchuk, the mapping device and one acceleration preview were observed,
but changing buttons/motion were not established. Basic IR drive was not
enabled in that arm. Its first protocol blocker is the mapped passthrough
identity window at F6, as the own source task order and native requests show.
No new model, codec, descriptor or API behavior was implemented to bypass it.
This is not evidence of zero gyro or physical incompatibility.

The Cemu clean no-holder preflight stopped before application launch because a
foreign browser held a companion event node. The original no-holder guard was
retained. Separate coexistence arms ran with exactly the previously observed
holder at preflight; the runner opened no holder and changed no foreign process.
Native writes are attributed directly, while shared kernel outputs are not
assigned to one actor. Matching the returned MP block to caller data does not
establish Cemu interpreted it as Nunchuk calibration. The original no-holder
Nunchuk read path therefore remains unretested; decoded Cemu gyro is unobserved.

All owned consumers exited between profiles. The producer closed idempotently;
its HID, hidraw and four LED nodes were verified removed. Screenshots, raw bytes,
logs, process/device identities and host paths remain private. Source and
artifact hashes preserve provenance; no latency or firmware-cadence acceptance
is inferred.


## Clean Cemu follow-up after the browser holder closed

The earlier coexistence arms and blocked preflight remain historical evidence.
After the owner closed the browser holder, a fresh virtual device used the same
merged runtime and caller resources. Each 35-second native Cemu arm passed its
no-companion-holder preflight; the runner opened no holder. The kernel driver
remained bound, so kernel output is not attributed solely to Cemu. Profiles are
fresh, while the producer is reused between the two arms.

| Arm | Delivered result | Next unestablished checkpoint |
| --- | --- | --- |
| Clean imported MP | Base EEPROM succeeds; no native extension calibration read | Repeated identity/status/report-mode initialization; decoded motion unobserved |
| Clean imported MP+Nunchuk | All 18 A40020/16 reads succeed; 17 replies match imported Nunchuk and one matches MP first half | Repeated initialization; decoded motion unobserved |

The first native extension identity before the MP+Nunchuk calibration read is
Nunchuk. Matching the private payloads demonstrates delivery beyond the earlier
Nunchuk calibration refusal. It does not prove Cemu interpreted the values,
paired each reply with a request, or produced decoded gyro. Mapping can change
under shared kernel activity, so the mixed block matches do not establish a
wrong-bank defect or a sole-actor race cause. No new model, codec, descriptor or
API change is inferred or implemented.

The new prefixes are `wii-w8-cemu-imported-clean-motionplus` and
`wii-w8-cemu-imported-clean-motionplus-nunchuk`. They add two sets without
rewriting the previous arms: W8 now contains 13 arms and the current Wii
inventory is 151 claims. Both consumers exited before the next profile; fresh
HID, raw and four LED nodes were verified removed after idempotent close.
