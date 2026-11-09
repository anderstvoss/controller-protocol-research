"""Manual wiki links must exist; no generated-page dependency."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_wiki_links import check  # noqa: E402


class WikiLinkTests(unittest.TestCase):
    def test_all_authored_markdown_links_resolve(self):
        self.assertEqual([], check(ROOT))


if __name__ == "__main__":
    unittest.main()
