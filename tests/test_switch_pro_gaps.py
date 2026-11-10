import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SwitchProGaps(unittest.TestCase):
    def test_home_led_claim_is_source_only_consumer_record(self):
        claims = [json.loads((ROOT / "records/claim/swpro-cgap-home-led-consumer.json").read_text())]
        for claim in claims:
            self.assertEqual(claim["applicability"]["controller"], "switch-pro")
            self.assertEqual(claim["applicability"]["transport"], "source_only")
            self.assertEqual(claim["evidence_role"], "consumer")
            self.assertEqual(claim["status"], "source_supported")
            self.assertEqual(claim["experiments"], [])
            self.assertTrue(claim["sources"])


if __name__ == "__main__":
    unittest.main()
