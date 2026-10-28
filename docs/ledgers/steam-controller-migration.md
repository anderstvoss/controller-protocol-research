# Steam Controller/Puck migration ledger

This is plan11c, not P0/P1 acceptance. Kernel facts are source_only consumer
evidence, OpenPuck facts concern that compatibility firmware, and historical
handoff statements remain conflicted. No upstream excerpts/captures copied.

| Area | Records | Boundary |
| --- | --- | --- |
| Kernel IDs/buses | sc2-migration-kernel-identities |1302 wired,1303 BLE,1304 Puck,1305 internal; not physical enumeration |
| Kernel interfaces | sc2-migration-kernel-interface-shape; sc2-migration-kernel-selection | Unified wired vs receiver slots/pogo; P1 still required |
| Kernel reports | sc2-migration-kernel-reports |0x80..85 consumer-defined;86..89 not established by kernel |
| Kernel desktop policy | sc2-migration-kernel-lizard-policy | Parameter/policy, not measured watchdog behavior |
| OpenPuck identity | sc2-migration-openpuck-identities; puck-current | Current pinned implementation1304/1305 |
| OpenPuck HID slots | sc2-migration-openpuck-slots | Four HID objects, not real Puck total interfaces |
| Compatibility report list | sc2-migration-openpuck-report-declarations | Descriptor declarations, not physical support proof |
| Historical conflict | puck-historical-compat; puck-historical-physical | Old1142 origin and capture unrecovered; current1304 does not erase history |
| Timing gap | sc2-cadence | Report description only; no measured physical cadence |

Source openpuck is reused and its exact bytes/hash reverified; new kernel source
records pin0fcb05b72344f40806cbe810de8872f1698bf053 as brief11 requests. P0 research
PR8 independently carries the first-release and SDL pins; this branch starts
from clean main so it does not spread PR8's problematic commit ancestry. Merge
main and retain both evidence sets after P0 lands. PR9 owns sc2-gap/sc2-src files;
none are edited here. Kernel and SDL claims are now marked `evidence_role: consumer`. Their
source-only scopes remain intact, but consumer evidence no longer elevates
the device category. OpenPuck layouts retain device-role source evidence of
a compatibility implementation, not evidence of the physical controller. Per-transport Puck assertions follow owner comment
6189359458 on virtualgamepad#176, preserving both USB and source-only evidence.
