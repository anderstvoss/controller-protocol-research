# W9f counted stimulus and reporting boundary

The tests-only code PR #262 pins 24 data reports for 24 codec commits in each
of mode 05/Nunchuk and mode 07/Classic, strictly alternating latest gyro and
child values. It passes on the existing model. Its setup sends the report mode
after activation; this matters for the observed live sequence below.

The old private stimulus loops shared a nominal pump cadence and changed
multiple state fields before commit, but retained no actual commit counters.
The old 28/14002 native read counts do not establish old application commit
rates. The replacement uses one atomic input snapshot per scheduled 20 ms
commit for both arms, drives gyro and acceleration plus Nunchuk controls on
the same schedule, and counts successful commits and errors explicitly.

The owner alone created three generic-bound virtual devices in a
2.033653-second window and restored/read back ignore_special_drivers = 0
before raw grants and consumers. The reserved off device was never used,
because the on arm did not pass. All devices were closed idempotently and
HID/raw removal verified; no LED nodes were created. No agent sudo, persistent
policy, model, descriptor or API change was involved. #258 remains a release
gate. Runtime was merged main c60c164, not a new model implementation.

| Arm | Producer counter interval | Post-mode-05 native frames per full consumer window | UI |
| --- | --- | --- | --- |
| MP+Nunchuk on, 180 seconds | 13018 successes, 0 errors / 260.348710 seconds | 0 MP, 0 child; 0/0 per consumer second | No changing Nunchuk or gyro observed |
| MP-only, 150 seconds | 8462 successes, 0 errors / 169.221721 seconds | 7462 MP; 49.746667 per consumer second | Changing mapped gyro, auto-calibration period 0 |

Producer intervals extend beyond consumer exit. Do not divide cumulative
producer counts by consumer duration. In-arm cumulative samples also showed
about 50 Hz successful commits; the final totals are not a physical cadence,
latency or delivery guarantee. Native frame rates use the entire bounded
consumer window, including setup, not only an active burst.

Timestamped trace shows all 28 MP+Nunchuk report 0x37 frames precede mode 05.
They cannot be tagged as MP/child passthrough merely from discriminator bits.
Dolphin selected report 0x37 before mapping and did not resend it after mapping;
MP-only did resend it. The existing codec switches to AwaitingMode on the map
transition and suppresses data until another 0x12. Calibration reads still
succeed while paused. This is a concrete consumer/model reporting-policy
boundary, not proof of the faithful replacement policy or authorization to
change the codec. The boundary was reported on virtualgamepad #158 before
any fix; no reporting/status policy change is made here.

F6 was not read. Imported MP/child calibration succeeds in the on arm. Native
and combined post-mode-05 A400F0=55 counts are zero in both arms. The off
control and adoption are not warranted because on does not pass. Earlier W9e
results remain historical; new counters do not reconstruct its missing
measurements. Only reduced counts, relative rates, booleans and hashes are
published. No raw bytes, images, scripts, identities or wall clocks; no
physical, radio, game, calibrated-rate or challenge claim follows.
