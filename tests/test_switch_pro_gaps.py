import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SwitchProHomeLightGap(unittest.TestCase):
    def test_source_only_consumer_claim(self):
        path = ROOT / "records/claim/swpro-cgap-home-led-consumer.json"
        claim = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(claim["id"], "swpro-cgap-home-led-consumer")
        self.assertEqual(claim["applicability"]["controller"], "switch-pro")
        self.assertEqual(claim["applicability"]["transport"], "source_only")
        self.assertEqual(claim["evidence_role"], "consumer")
        self.assertEqual(claim["status"], "source_supported")
        self.assertEqual(claim["sources"], ["audio-linux-hid-nintendo"])
        self.assertEqual(claim["experiments"], [])


if __name__ == "__main__":
    unittest.main()
