import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class ContentionsH(unittest.TestCase):
    def test_documents_and_inferred_not_promoted(self):
        for f in ["sony-consumer-contention.md","switch-pro-consumer-contention.md","xbox360-consumer-contention.md"]:
            s = (ROOT/"docs"/f).read_text()
            self.assertIn("No evidence",s)
            self.assertIn("not run",s.lower())
            self.assertIn("bound",s.lower())
            self.assertIn("unbound",s.lower())
        for f in (ROOT/"records/claim").glob("parity-h-*.json"):
            o=json.loads(f.read_text())
            self.assertEqual(o["evidence_role"],"consumer")
            self.assertEqual(o["applicability"]["transport"],"source_only")
            self.assertFalse(o["experiments"])
            self.assertIn(o["status"],("inferred","source_supported"))
if __name__ == "__main__":
    unittest.main()
