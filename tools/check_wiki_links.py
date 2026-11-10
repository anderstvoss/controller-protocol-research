"""Read-only validation for the manually authored controller wiki.

Check relative Markdown page links and commit-pinned links into the corpus.
GitHub 'blob' links must resolve to files; 'tree' links must resolve to
directories. Never generate or alter wiki content or evidence records.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CORPUS_PREFIX = "/anderstvoss/controller-protocol-research/"
CORPUS_LINK = re.compile(r"^/(?:anderstvoss/controller-protocol-research)/(blob|tree)/([^/]+)/(.+)$")
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
                if url.netloc == "github.com" and url.path.startswith(
                    (CORPUS_PREFIX + "blob/", CORPUS_PREFIX + "tree/")
                ):
                    citation = CORPUS_LINK.fullmatch(url.path)
                    if not citation:
                        issues.append(relative + ": malformed corpus citation " + target)
                        continue
                    kind, revision, pathpart = citation.groups()
                    if not re.fullmatch(r"[0-9a-f]{40}", revision):
                        issues.append(relative + ": corpus citation must use full SHA " + target)
                    record = (root / unquote(pathpart)).resolve()
                    if not record.is_relative_to(root):
                        issues.append(relative + ": corpus citation escapes repository " + target)
                    elif kind == "blob" and not record.is_file():
                        issues.append(relative + ": cited corpus file missing " + target)
                    elif kind == "tree" and not record.is_dir():
                        issues.append(relative + ": cited corpus directory missing " + target)
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
