"""
Checks every local link in the site's pages and in the markdown they are generated from: images, videos and links to other
pages. The check is case-sensitive, because GitHub Pages is even though Windows isn't, so a link with the wrong
capitalisation works on your computer and breaks on the site.

Links in a markdown file are checked as they will be in the generated page (markdown/posts/x.md becomes posts/x.html).
Also lists the images in assets/ and drafts/assets/ that nothing links to (just for information).

Run with: python3 scripts/check_links.py     (exits with 1 if a link is broken)
"""
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup

from common import DRAFTS_DIR, ROOT, exists_exact, html_files, read_text

EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", re.IGNORECASE)   # http:, mailto:, data:, //host, #anchor
ATTRIBUTES = ("src", "href", "data", "poster")
MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
RAW_ATTRIBUTE = re.compile(r"""\b(?:src|href|data|poster)\s*=\s*["']([^"']*)["']""", re.IGNORECASE)
IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"}


def html_links(path):
    """(line, link) for every local link in an html page."""
    soup = BeautifulSoup(read_text(path), "html.parser")
    for tag in soup.find_all(True):
        for attribute in ATTRIBUTES:
            if tag.get(attribute):
                yield tag.sourceline, tag[attribute]


def markdown_links(path):
    """(line, link) for every local link in a markdown file, whether written as markdown or as raw html."""
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        for match in MD_LINK.finditer(line):
            yield number, match.group(1)
        for match in RAW_ATTRIBUTE.finditer(line):
            yield number, match.group(1)


def real_path(full):
    """The path (from the repository root) with the capitalisation the files really have."""
    current, parts = ROOT, []
    for part in Path(full).relative_to(ROOT).parts:
        part = next((n for n in os.listdir(current) if n.lower() == part.lower()), part)
        parts.append(part)
        current = current / part
    return "/".join(parts)


def check(source, base_dir, links, problems, referenced):
    count = 0
    for line, link in links:
        link = link.strip()
        if not link or EXTERNAL.match(link):
            continue
        count += 1
        target = unquote(re.split(r"[?#]", link, maxsplit=1)[0])
        full = os.path.normpath(os.path.join(ROOT if target.startswith("/") else base_dir, target.lstrip("/")))
        if os.path.isdir(full):
            full = os.path.join(full, "index.html")
        referenced.add(os.path.normcase(full))
        if exists_exact(full):
            continue
        if os.path.exists(full):
            problems.append(f"{source}:{line}: {link}  (wrong capitalisation, the real path is {real_path(full)})")
        else:
            problems.append(f"{source}:{line}: {link}  (file not found)")
    return count


def main():
    problems, referenced, links_checked, files_checked = [], set(), 0, 0

    for path in html_files():
        links_checked += check(path.relative_to(ROOT), path.parent, html_links(path), problems, referenced)
        files_checked += 1

    for path in sorted((ROOT / "markdown").rglob("*.md")):
        page_dir = ROOT / path.parent.name          # markdown/posts/x.md -> posts/x.html
        links_checked += check(path.relative_to(ROOT), page_dir, markdown_links(path), problems, referenced)
        files_checked += 1

    print(f"Checked {links_checked} local links in {files_checked} files: {len(problems)} broken")
    for problem in problems:
        print(f"  {problem}")

    unused = [p for folder in (ROOT / "assets", DRAFTS_DIR / "assets") if folder.exists() for p in sorted(folder.rglob("*"))
              if p.is_file() and p.suffix.lower() in IMAGE_TYPES and os.path.normcase(str(p)) not in referenced]
    if unused:
        print(f"\nImages that nothing links to ({len(unused)}):")
        for p in unused:
            print(f"  {p.relative_to(ROOT).as_posix()}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
