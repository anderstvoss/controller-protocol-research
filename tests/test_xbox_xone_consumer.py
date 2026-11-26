import json
import unittest
from pathlib import Path


class XoneConsumerEvidence(unittest.TestCase):
    def test_xone_claims_are_consumer_only_without_experiments(self):
        root = Path(__file__).resolve().parents[1]
        paths = sorted((root / "records/claim").glob("xbox-xone-*.json"))
        self.assertTrue(paths)
        claims = [json.loads(path.read_text()) for path in paths]
        self.assertEqual(len({claim["id"] for claim in claims}), len(claims))
        self.assertTrue(all(claim["id"] == path.stem for path, claim in zip(paths, claims)))
        self.assertTrue(all(claim["evidence_role"] == "consumer" for claim in claims))
        self.assertTrue(all(claim["applicability"]["controller"] == "xbox-series" for claim in claims))
        self.assertTrue(all(claim["experiments"] == [] for claim in claims))
        self.assertTrue(all(claim["status"] in {"source_supported", "inferred", "unknown"} for claim in claims))
        receiver_bind = next((claim for claim in claims if claim["id"] == "xbox-xone-receiver-bind"), None)
        self.assertIsNotNone(receiver_bind)
        self.assertEqual(receiver_bind["status"], "source_supported")
        self.assertIn("receiver", receiver_bind["statement"].lower())
        self.assertEqual(receiver_bind["applicability"]["transport"], "source_only")


if __name__ == "__main__":
    unittest.main()
