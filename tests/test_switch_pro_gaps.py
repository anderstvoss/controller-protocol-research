import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SwitchProGaps(unittest.TestCase):
    def test_gap_claims_are_source_only_consumer_records(self):
        claims = [json.loads(p.read_text()) for p in
                  (ROOT / "records/claim").glob("swpro-cgap-*.json")]
        self.assertEqual([c["id"] for c in claims], ["swpro-cgap-home-led-consumer"])
        for claim in claims:
            self.assertEqual(claim["applicability"]["controller"], "switch-pro")
            self.assertEqual(claim["applicability"]["transport"], "source_only")
            self.assertEqual(claim["evidence_role"], "consumer")
            self.assertEqual(claim["status"], "source_supported")
            self.assertEqual(claim["experiments"], [])
            self.assertTrue(claim["sources"])


if __name__ == "__main__":
    unittest.main()
