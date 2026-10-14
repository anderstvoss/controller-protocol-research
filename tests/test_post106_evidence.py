"""Regression: source decoders and vendor macros cannot become physical truth."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExposureEvidence(unittest.TestCase):
    def record(self, category, name):
        return json.loads((ROOT / 'records' / category / (name + '.json')).read_text())

    def test_source_claims_remain_independent_implementation_evidence(self):
        for name, source in [('edge-independent-raw', 'sdl-ps5-baseline'), ('switch2-independent-raw', 'sdl-switch2')]:
            record = self.record('claim', name)
            self.assertEqual(record['status'], 'source_supported')
            self.assertEqual(record['sources'], [source])
            self.assertEqual(record['experiments'], [])
            origin = self.record('source', source)
            self.assertEqual(origin['kind'], 'independent_implementation')
            self.assertRegex(origin['revision'], r'^[0-9a-f]{40}$')
            self.assertIn(origin['revision'], origin['url'])

    def test_macro_documentation_does_not_establish_raw_absence(self):
        raw = self.record('claim', 'pro2-independent-raw-unknown')
        self.assertEqual(raw['status'], 'unknown')
        self.assertEqual(self.record('claim', 'pro2-physical-macro-controls')['status'], 'source_supported')
        source = self.record('source', '8bitdo-pro2-faq')
        excerpt = (ROOT / 'evidence/source-excerpts/pro2-faq.txt').read_bytes()
        self.assertEqual(hashlib.sha256(excerpt).hexdigest(), source['sha256'])
        self.assertIn('excerpt-sha256:', source['revision'])

    def test_linux_and_physical_unknowns_are_explicit(self):
        for prefix in ['edge', 'switch2', 'pro2']:
            for suffix in ['linux-exposure-unknown', 'physical-corroboration-unknown']:
                self.assertEqual(self.record('claim', prefix + '-' + suffix)['status'], 'unknown')

    def test_mapping_and_backend_research_preserves_scope_and_baseline(self):
        for name in ['edge-sdl-default-mapping', 'sdl-linux-backend-signatures', 'dualsense-kernel-aux-parser']:
            record = self.record('claim', name)
            self.assertEqual(record['status'], 'source_supported')
            self.assertEqual(record['experiments'], [])
            self.assertEqual(record['applicability']['firmware'], 'not measured')
            for source in record['sources']:
                if source == 'kernel':
                    continue
                origin = self.record('source', source)
                self.assertEqual(origin['revision'], '535d80badefc83c5c527ec5748f2a20d6a9310fe')
                self.assertIn(origin['revision'], origin['url'])
                self.assertRegex(origin['sha256'], r'^[0-9a-f]{64}$')
                self.assertEqual(origin['lineage'], 'libsdl')
        # More SDL files do not create independent implementation lineages.
        mapping = self.record('claim', 'edge-sdl-default-mapping')
        self.assertNotEqual(mapping['status'], 'independently_corroborated')
        self.assertIn('User mappings can override', mapping['statement'])
        self.assertIn('Vendor-less', self.record('claim', 'sdl-linux-backend-signatures')['statement'])
