"""Synthetic parser cases and the pinned source-derived consumer reference."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('wii_shape', ROOT / 'tools/wii_consumer_shape.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WiiConsumerShape(unittest.TestCase):
    def test_constants_resolve_numbers_and_prior_aliases_only(self):
        self.assertEqual(MODULE.constants('#define TEST_A 0x10\n#define TEST_B TEST_A\n'
                                         '#define TEST_C UNKNOWN\n#define TEST_D dangerous()\n'),
                         {'TEST_A': 16, 'TEST_B': 16})

    def test_synthetic_source_parameters_preserve_fuzz_and_flat(self):
        text = 'input_set_abs_params(fake, ABS_RX, -12, 34, 2, 4);'
        self.assertEqual(MODULE.axes(text, 1, 1), [('ABS_RX', -12, 34, 2, 4)])

    def test_hash_mismatch_is_rejected_before_source_interpretation(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'modules.c').write_text('synthetic mismatched source')
            with self.assertRaisesRegex(ValueError, 'source hash mismatch'):
                MODULE.read(directory, 'modules.c', 'wii-linux-modules')

    def test_golden_nodes_are_synthetic_separate_and_keep_fuzz(self):
        trace = json.loads((ROOT / 'fixtures/wii-c5-evdev-golden.json').read_text())
        self.assertTrue(trace['manifest']['synthetic'])
        self.assertEqual(len(trace['manifest']['sources']), 6)
        self.assertEqual([s['control_count'] for s in trace['manifest']['sources']], [12, 3, 8, 7, 21, 3])
        self.assertTrue(all(c['absolute_range']['fuzz'] > 0 for c in trace['controls'] if c['event_type'] == 3))
