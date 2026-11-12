"""Source-only Joy-Con left-half claim coverage; no host or hardware dependencies."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "records" / "claim"
EXPECTED = {
    "joycon-cgap-left-identity": "device",
    "joycon-cgap-left-wire-fields": "device",
    "joycon-cgap-left-kernel-buttons": "consumer",
    "joycon-cgap-left-kernel-stick": "consumer",
    "joycon-cgap-left-kernel-imu": "consumer",
    "joycon-cgap-left-sdl3-modes": "consumer",
}


class JoyConLeftGaps(unittest.TestCase):
    def test_records_remain_source_only_on_left_half(self):
        for claim_id, role in EXPECTED.items():
            with self.subTest(claim_id=claim_id):
                obj = json.loads((ROOT / (claim_id + ".json")).read_text())
                self.assertEqual(obj["id"], claim_id)
                self.assertEqual(obj["applicability"]["controller"], "switch-joycon-left")
                self.assertEqual(obj["applicability"]["transport"], "source_only")
                self.assertEqual(obj["status"], "source_supported")
                self.assertEqual(obj["evidence_role"], role)
                self.assertTrue(obj["sources"])
                self.assertEqual(obj["experiments"], [])


if __name__ == "__main__":
    unittest.main()
