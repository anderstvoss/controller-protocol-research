import json
import unittest
from pathlib import Path


class WiiLedger(unittest.TestCase):
    def test_consumer_records_and_revision_gaps_remain_separate(self):
        root = Path(__file__).resolve().parents[1]
        claims = [json.loads(p.read_text()) for p in (root / 'records/claim').glob('wii-*.json')]
        self.assertEqual(len(claims), 115)
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
