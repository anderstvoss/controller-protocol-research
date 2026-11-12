"""Tests for manually authored wiki link validation (no prose generation)."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_wiki_links import check  # noqa: E402

SHA = "a" * 40
BASE = "https://github.com/anderstvoss/controller-protocol-research"


class WikiLinkTests(unittest.TestCase):
    def test_all_authored_markdown_links_resolve(self):
        self.assertEqual([], check(ROOT))

    def test_blob_files_and_tree_directories_both_resolve(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pages = root / "docs/wiki/pages"
            pages.mkdir(parents=True)
            (pages / "other.md").write_text("# Other\n", encoding="utf-8")
            (root / "records/claim").mkdir(parents=True)
            (root / "records/controller").mkdir(parents=True)
            (root / "records/claim/example.json").write_text("{}", encoding="utf-8")
            (pages / "index.md").write_text(
                f"[claim]({BASE}/blob/{SHA}/records/claim/example.json)\n"
                f"[registry]({BASE}/tree/{SHA}/records/controller)\n"
                "[other](other.md)\n", encoding="utf-8"
            )
            self.assertEqual([], check(root))

    def test_wrong_github_link_type_or_missing_target_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pages = root / "docs/wiki/pages"
            pages.mkdir(parents=True)
            (root / "records/claim").mkdir(parents=True)
            (root / "records/claim/example.json").write_text("{}", encoding="utf-8")
            (pages / "index.md").write_text(
                f"[directory as file]({BASE}/blob/{SHA}/records/claim)\n"
                f"[file as directory]({BASE}/tree/{SHA}/records/claim/example.json)\n"
                f"[nonexistent]({BASE}/blob/{SHA}/records/claim/absent.json)\n"
                f"[moving ref]({BASE}/blob/main/records/claim/example.json)\n",
                encoding="utf-8",
            )
            errors = check(root)
            self.assertEqual(4, len(errors))
            self.assertTrue(any("cited corpus file missing" in error for error in errors))
            self.assertTrue(any("cited corpus directory missing" in error for error in errors))
            self.assertTrue(any("must use full SHA" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
