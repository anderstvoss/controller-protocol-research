import json
import unittest
from pathlib import Path


class WiiLedger(unittest.TestCase):
    def test_consumer_records_and_revision_gaps_remain_separate(self):
        root = Path(__file__).resolve().parents[1]
        claims = [json.loads(p.read_text()) for p in (root / 'records/claim').glob('wii-*.json')]
        self.assertEqual(len(claims), 232)
        self.assertTrue(all(c['applicability']['transport'] == 'source_only'
                            for c in claims if c['status'] == 'source_supported'))
        w4_consumers = {'wii-w4-sdl-3-2-10-no-reattach',
                        'wii-w4-sdl-3-2-10-motionplus-disconnect-path',
                        'wii-w4-sdl-newer-no-reattach'}
        for claim in claims:
            expected = ['wii-w2-sdl-after-host-run', 'wii-w3-sdl-diagnosis-host-run'] if claim['id'] in w4_consumers else []
            if claim['id'] == 'wii-w5-sdl-linux-reset-gyro-limitation':
                expected = [f'wii-w5-{case}-{arm}-host-run'
                            for arm in ['control', 'holder']
                            for case in ['motionplus', 'motionplus-nunchuk']]
            elif claim['id'] == 'wii-w5-kernel-motionplus-gyro-delivery':
                expected = [f'wii-w5-{case}-kernel-host-run'
                            for case in ['motionplus', 'motionplus-nunchuk']]
            elif claim['id'] == 'wii-w7-cemu-appimage-result':
                expected = ['wii-w7-cemu-appimage-host-run']
            elif (claim['id'].startswith('wii-w8-') or
                  (claim['id'].startswith('wii-w9-') and claim['id'].endswith('-result'))):
                expected = [claim['id'].removesuffix('-result') + '-host-run']
            elif claim['id'].startswith(('wii-w9f-', 'wii-w9g-', 'wii-w9h-', 'wii-w9i-')):
                expected = [claim['id'].removesuffix('-result') + '-host-run']
            elif (claim['id'].startswith('wii-w9e-generic-')
                  and claim['id'].endswith('-result')):
                expected = [claim['id'].removesuffix('-result') + '-host-run']
            elif claim['id'] in {'wii-w9e-per-device-bind-blocked-result',
                                 'wii-w9e-consumer-arms-unmeasured-result'}:
                expected = ['wii-w9e-per-device-bind-host-run']
            elif claim['id'].startswith('wii-p1-'):
                expected = [claim['id'].removesuffix('-result') + '-host-run']
            elif claim['id'].startswith('wii-w7-'):
                expected = ['wii-w7-' + claim['id'].split('-')[2] + '-host-run']
            self.assertEqual(claim['experiments'], expected, claim['id'])
        by_id = {c['id']: c for c in claims}
        revisions = [by_id[id]['applicability']['revision'] for id in
                     ['wii-original-remote-consumer-revision', 'wii-tr-consumer-revision',
                      'wii-early-plus-revision-gap']]
        self.assertEqual(len(set(revisions)), 3)
        self.assertEqual(by_id['wii-early-plus-revision-gap']['status'], 'unknown')
        self.assertEqual(by_id['wii-memory-size-hypothesis']['status'], 'unknown')
        self.assertEqual(by_id['wii-gap-extension-calibration-checksum-unknown']['status'], 'unknown')
        self.assertEqual(by_id['wii-gap-classic-pro-full-id-physical-unknown']['status'], 'unknown')

    def test_gyro_consumer_claims_are_source_only(self):
        root = Path(__file__).resolve().parents[1]
        claim_dir = root / 'records/claim'
        wii_ids = [
            'wii-gap-sdl-gyro-registration-active-mode-separation',
            'wii-gap-sdl-linux-motionplus-activation-mode-noop',
            'wii-gap-sdl-motionplus-gyro-packet-preconditions',
            'wii-gap-sdl-periodic-motionplus-check-no-mode-recovery',
            'wii-gap-sdl-initial-extension-reset-can-disrupt-mapping',
            'wii-gap-kernel-motionplus-evdev-open-activates-used-flag',
            'wii-gap-kernel-motionplus-map-modes-and-release',
            'wii-gap-kernel-motionplus-shared-hidraw-coexistence',
        ]
        dualsense_ids = [
            'dualsense-uhid-gyro-hhd-presentation',
            'dualsense-uhid-gyro-hhd-feature-replies',
            'dualsense-uhid-gyro-hhd-imu-timestamp',
            'dualsense-uhid-gyro-sdl-ps5-enable-and-calibration',
            'dualsense-uhid-gyro-hhd-steam-scope',
        ]
        self.assertEqual(len(wii_ids), 8)
        self.assertEqual(len(dualsense_ids), 5)
        for claim_id in wii_ids + dualsense_ids:
            claim = json.loads((claim_dir / (claim_id + '.json')).read_text())
            self.assertEqual(claim['status'], 'source_supported', claim_id)
            self.assertEqual(claim['applicability']['transport'], 'source_only', claim_id)
            self.assertEqual(claim['applicability']['controller'],
                             'wii-remote' if claim_id.startswith('wii-gap-') else 'dualsense', claim_id)
            self.assertIn('evidence_role: consumer', claim['applicability']['scope'], claim_id)
            self.assertFalse(claim['experiments'], claim_id)

    def test_dolphin_consumer_claims_are_source_only(self):
        root = Path(__file__).resolve().parents[1]
        claim_dir = root / 'records/claim'
        ids = [
            'wii-gap-dolphin-hidapi-kernel-binding-competition',
            'wii-gap-dolphin-real-remote-path-separation',
            'wii-gap-dolphin-controllerinterface-motionplus-calibration-gate',
            'wii-gap-dolphin-emulated-motionplus-modes-passthrough',
        ]
        for claim_id in ids:
            claim = json.loads((claim_dir / (claim_id + '.json')).read_text())
            self.assertEqual(claim['status'], 'source_supported', claim_id)
            self.assertEqual(claim['applicability']['controller'], 'wii-remote', claim_id)
            self.assertEqual(claim['applicability']['transport'], 'source_only', claim_id)
            self.assertIn('evidence_role: consumer', claim['applicability']['scope'], claim_id)
            self.assertEqual(claim['experiments'], [], claim_id)

    def test_additional_wii_software_consumers(self):
        root = Path(__file__).resolve().parents[1]
        ids = [
            'wii-gap-consumer-xwiimote-driver-evdev-interface',
            'wii-gap-consumer-xwiishow-gyro-normalization',
            'wii-gap-consumer-cemu-hidapi-nintendo-enumeration',
            'wii-gap-consumer-cemu-motionplus-self-activation',
            'wii-gap-consumer-cemu-gyro-decode-path-limits',
            'wii-gap-consumer-retroarch-udev-sensor-sibling-limitation',
            'wii-gap-consumer-wiiuse-bluez-l2cap-linux',
            'wii-gap-consumer-cwiid-bluez-l2cap-linux',
            'wii-gap-consumer-antimicrox-sdl-general-input',
            'wii-gap-consumer-xwiimote-ng-kernel-fork',
            'wii-gap-consumer-wiimotelib-windows-hid',
            'wii-gap-consumer-wiinupro-windows-bluetooth',
            'wii-gap-consumer-dolphin-hidapi-usability-probe',
        ]
        self.assertEqual(len(ids), 13)
        for claim_id in ids:
            claim = json.loads((root / 'records/claim' / (claim_id + '.json')).read_text())
            self.assertEqual(claim['status'], 'source_supported', claim_id)
            self.assertEqual(claim['applicability']['transport'], 'source_only', claim_id)
            self.assertEqual(claim['applicability']['controller'], 'wii-remote', claim_id)
            self.assertIn('evidence_role: consumer', claim['applicability']['scope'], claim_id)
            self.assertEqual(claim['experiments'], [], claim_id)
            self.assertTrue(claim['sources'], claim_id)

    def test_dolphin_attachment_source_only(self):
        root = Path(__file__).resolve().parents[1]
        ids = [
            'wii-gap-dolphin-attach-scanner-vs-controllerinterface',
            'wii-gap-dolphin-attach-controller-task-order-and-failure',
            'wii-gap-dolphin-attach-motionplus-mode-rechecks',
            'wii-gap-dolphin-attach-passthrough-four-byte-id-f6',
            'wii-gap-dolphin-attach-active-passthrough-calibration-copy-40',
            'wii-gap-dolphin-attach-current-model-passthrough-read-denials',
            'wii-gap-dolphin-attach-kernel-shared-register-competition',
            'wii-gap-dolphin-attach-report-calibration-and-later-gates',
            'wii-gap-dolphin-attach-driver-binding-alternatives',
        ]
        self.assertEqual(len(ids), 9)
        for claim_id in ids:
            claim = json.loads((root / 'records/claim' / (claim_id + '.json')).read_text())
            self.assertEqual(claim['status'], 'source_supported', claim_id)
            self.assertEqual(claim['applicability']['controller'], 'wii-remote', claim_id)
            self.assertEqual(claim['applicability']['transport'], 'source_only', claim_id)
            self.assertIn('evidence_role: consumer', claim['applicability']['scope'], claim_id)
            self.assertEqual(claim['experiments'], [], claim_id)
            self.assertTrue(claim['sources'], claim_id)

    def test_motionplus_cross_consumer_findings_source_only(self):
        root = Path(__file__).resolve().parents[1]
        ids = [
            'wii-gap-cross-cemu-fa20-no-f6-40',
            'wii-gap-cross-cemu-motionplus-visitor-unreachable',
            'wii-gap-cross-cemu-exported-gyro-zero-sample',
            'wii-gap-cross-wiiuse-mp-sample-zeroing',
            'wii-gap-cross-cwiid-legacy-single-mp',
            'wii-gap-cross-linux-kernel-sdl-layer-contrast',
        ]
        self.assertEqual(len(ids), 6)
        for claim_id in ids:
            claim = json.loads((root / 'records/claim' / (claim_id + '.json')).read_text())
            self.assertEqual(claim['status'], 'source_supported', claim_id)
            self.assertEqual(claim['applicability']['controller'], 'wii-remote', claim_id)
            self.assertEqual(claim['applicability']['transport'], 'source_only', claim_id)
            self.assertIn('evidence_role: consumer', claim['applicability']['scope'], claim_id)
            self.assertEqual(claim['experiments'], [], claim_id)
            self.assertTrue(claim['sources'], claim_id)

    def test_motionplus_challenge_findings_are_source_only(self):
        root = Path(__file__).resolve().parents[1]
        ids = [
            'wii-gap-challenge-f7-first-stage-community',
            'wii-gap-challenge-f1-second-stage-dolphin',
            'wii-gap-challenge-50-region-width-and-banks',
            'wii-gap-challenge-rabin-public-implementation',
            'wii-gap-challenge-dolphin-ciface-versus-guest',
            'wii-gap-challenge-nonreaders-independent-consumers',
            'wii-gap-challenge-static02-limits',
        ]
        self.assertEqual(len(ids), 7)
        for claim_id in ids:
            claim = json.loads((root / 'records/claim' / (claim_id + '.json')).read_text())
            self.assertEqual(claim['status'], 'source_supported', claim_id)
            self.assertEqual(claim['applicability']['controller'], 'wii-remote', claim_id)
            self.assertEqual(claim['applicability']['transport'], 'source_only', claim_id)
            self.assertIn('evidence_role:', claim['applicability']['scope'], claim_id)
            self.assertEqual(claim['experiments'], [], claim_id)
            self.assertEqual(claim['conflicts_with'], [], claim_id)
            self.assertTrue(claim['sources'], claim_id)


    def test_remote_plus_source_only_scope(self):
        root = Path(__file__).resolve().parents[1]
        ids = [
            'wii-gap-plus-physical-revision-taxonomy',
            'wii-gap-plus-bluetooth-identities',
            'wii-gap-plus-kernel-gen2-builtin-policy',
            'wii-gap-plus-app-enumeration-versus-mp',
            'wii-gap-plus-integrated-mp-presence-and-identity-gap',
            'wii-gap-plus-passthrough-downstream-not-internal',
            'wii-gap-plus-calibration-register-challenge-unknown',
            'wii-gap-plus-base-features-and-tr-transport',
            'wii-gap-plus-compat-options-and-fidelity-gate',
        ]
        self.assertEqual(len(ids), 9)
        for claim_id in ids:
            claim = json.loads((root / 'records/claim' / (claim_id + '.json')).read_text())
            self.assertEqual(claim['status'], 'source_supported', claim_id)
            self.assertEqual(claim['applicability']['controller'], 'wii-remote', claim_id)
            self.assertEqual(claim['applicability']['transport'], 'source_only', claim_id)
            self.assertIn('evidence_role:', claim['applicability']['scope'], claim_id)
            self.assertEqual(claim['experiments'], [], claim_id)
            self.assertEqual(claim['conflicts_with'], [], claim_id)
            self.assertTrue(claim['sources'], claim_id)


    def test_remote_plus_traces_source_only(self):
        root = Path(__file__).resolve().parents[1]
        ids = [
            'wii-gap-plustrace-kernel-gen2-ladder',
            'wii-gap-plustrace-kernel-mp-id-predicate-and-fallback',
            'wii-gap-plustrace-xwiimote-sibling-only',
            'wii-gap-plustrace-sdl-fe-probe-classic-limit',
            'wii-gap-plustrace-dolphin-ciface-f6-40-sequence',
            'wii-gap-plustrace-dolphin-real-guest-routing',
            'wii-gap-plustrace-cemu-builtin-identity-nonactivation',
            'wii-gap-plustrace-wiiuse-builtin-id-and-classic-gap',
            'wii-gap-plustrace-reply-provenance-and-unknowns',
            'wii-gap-plustrace-acceptance-and-revision-contract',
        ]
        self.assertEqual(len(ids), 10)
        for claim_id in ids:
            claim = json.loads((root / 'records/claim' / (claim_id + '.json')).read_text())
            self.assertEqual(claim['status'], 'source_supported', claim_id)
            self.assertEqual(claim['applicability']['controller'], 'wii-remote', claim_id)
            self.assertEqual(claim['applicability']['transport'], 'source_only', claim_id)
            self.assertIn('evidence_role:', claim['applicability']['scope'], claim_id)
            self.assertEqual(claim['experiments'], [], claim_id)
            self.assertEqual(claim['conflicts_with'], [], claim_id)
            self.assertTrue(claim['sources'], claim_id)
