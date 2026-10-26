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
fixture. The seven claims raise the current Wii count from 138 to 145 without
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
PRs, both for Anders to merge. Imported-block reruns and the final evidence and
adoption PRs await those merges; this report makes no claim about those reruns.
