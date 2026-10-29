# Wii Remote Plus P1 kernel-bound host runs

These runs use published code PR virtualgamepad #263 at
87700df59fbfe7fef99f5ab35bd09aee53abf9ab. Tr remains the internal revision;
its GUI label is Wii Remote Plus. Two dedicated virtual Bluetooth-bus PID
0330 devices used the default built-in inactive ID policy, external-style
compat option off, both passthrough shims on and the same caller-imported
synthetic EEPROM/MP/Nunchuk blocks as W9. No Original acceptance is inherited.
Physical identity/calibration/status/descriptor captures remain unmeasured.

No special-driver window was used. Both bound to wiimote and reported
`devtype = gen20`, with MotionPlus nodes; the Nunchuk device also initially had
its child node. The owner ran exact-device raw/LED grants, then the agent
revalidated association, identity, driver and raw/input/LED links. No agent
sudo, persistent rule, module change or debug setting change was involved.

| Run | Observation | Disposition |
| --- | --- | --- |
| MP-only kernel and xwiimote together, 18 seconds | ABS_RX/RY/RZ and xwiimote MotionPlus each show two driven values | Bounded gyro delivery pass |
| Nunchuk kernel and xwiimote together, 18 seconds | Same changing gyro; child presence is not decoded-child acceptance | Bounded gyro delivery pass |
| MP-only SDL 3.2.10, 60 seconds, kernel MP node held | HIDAPI open, no disconnect, changing kernel gyro; no SDL gyro capability | Changing SDL gyro unestablished |
| Nunchuk SDL 3.2.10, 60 seconds, kernel MP node held | SDL gyro capable/enabled but polled angular arrays stay zero while kernel gyro changes | Changing SDL gyro unestablished |
| MP-only native Dolphin 2503 bound, 150 seconds | Exact imported MP chunks and sampled changing mapped gyro/accel/basic IR, calibration period 0 | Bounded Plus-specific mapping pass |

SDL headers and dynamic library were selected explicitly from system
3.2.10 (877399b2b), independently of the separate local 3.5.0 installation.
Sensor API sample counts are repeated polls, not fresh nonzero sensor events;
capability, enable success and reads of zero do not establish decoded delivery.
The concurrent holder is a stated precondition, not an implicit universal
SDL startup condition. No disconnect/removal was observed in either bound.
These failures are consumer observations, not a physically zero virtual gyro
or an authorization for a model fix.

In xwiimote's Nunchuk capture, requested versus opened interface masks are
retained separately; no child button/stick decode pass is inferred from gyro
or initial node presence. Normalization was left at its initial configuration.
Kernel axis ranges and xwiimote values are controlled virtual samples, not
calibrated physical angular rates. No cadence or latency claim follows.

Kernel journal/dmesg access was denied to the agent user. The owner ran a
read-only exact-device dmesg filter locally. Its detection lines confirm the
known classification but contain no full inactive-ID hex at current logging
level. That observation remains unavailable; debug logging was not enabled.
A600FA requests and the source-selected `00 00 A4 20 00 05` policy are not a
substitute for a kernel log readback. Leading zero bytes remain unknown model
bytes, and no retail identity is measured.

Consumers used exact-owned nodes, isolated profiles and the prior raw/radio
observation guard where applicable; the hook is not a complete sandbox. All
consumers and producers were closed, with HID/raw/LED removal and idempotent
cleanup verified. No Cemu, live Classic or generic-bound Plus passthrough was
run. W9f's reporting pause is separate and unchanged. #258 still gates release
special-driver policy; #52 keeps physical captures deferred. Only reduced
counts/ranges/booleans and hashes are published; raw logs, screenshots, local
scripts, identities, paths and wall clocks remain private.
