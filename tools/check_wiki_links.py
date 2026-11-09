"""Read-only validation for manually authored controller wiki citations and links.

This checker intentionally does NOT generate, reformat or update any wiki pages.
It checks link existence only; evidence interpretation requires human review.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "/anderstvoss/controller-protocol-research/blob/"
LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")


def check(root=ROOT):
    root = Path(root).resolve()
    pages = root / "docs" / "wiki" / "pages"
    issues = []
    if not pages.is_dir():
        return ["missing authored wiki directory"]
    paths = sorted(pages.rglob("*.md"))
    if not paths:
        return ["wiki has no authored pages"]
    for markdown in paths:
        content = markdown.read_text(encoding="utf-8")
        relative = markdown.relative_to(root).as_posix()
        for match in LINK.finditer(content):
            target = match.group(1)
            if target.startswith("#") or target.startswith("mailto:"):
                continue
            url = urlsplit(target)
            if url.scheme in ("http", "https"):
                if url.netloc == "github.com" and url.path.startswith(PREFIX):
                    suffix = url.path[len(PREFIX):].split("/", 1)
                    if len(suffix) != 2:
                        issues.append(relative + ": malformed corpus citation " + target)
                        continue
                    revision, pathpart = suffix
                    if not re.fullmatch(r"[0-9a-f]{40}", revision):
                        issues.append(relative + ": corpus citation must use full SHA " + target)
                    record = (root / unquote(pathpart)).resolve()
                    if not record.is_relative_to(root) or not record.is_file():
                        issues.append(relative + ": cited corpus path missing " + target)
                continue
            if url.scheme:
                continue
            local = (markdown.parent / unquote(url.path)).resolve()
            if not local.is_relative_to(pages) or not local.is_file():
                issues.append(relative + ": wiki page link missing " + target)
    return issues


def main():
    issues = check(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT)
    for issue in issues:
        print(issue, file=sys.stderr)
    if issues:
        raise SystemExit(1)
    print("Wiki links: OK")


if __name__ == "__main__":
    main()
