"""
Generates HTML pages from the markdown files in markdown/.

    markdown/posts/<name>.md     ->  posts/<name>.html
    markdown/projects/<name>.md  ->  projects/<name>.html

The page's head, header and footer come from index.html. The first heading of the markdown file becomes the page title,
and the other headings are shifted so that sections end up as <h4> (like the hand-written pages).

A markdown file can start with a front matter block:

    ---
    title: Overrides the first heading
    date: 2026-01-31      (or "January 31st, 2026")
    ---

A markdown file is only published if it has a date. Without one it is a draft and is skipped. Posts show their date under
the title; projects don't show it, but still need one to be published.

Run with: python3 scripts/page_gen.py [file.md ...]   (no arguments converts everything)
"""
import argparse
import html
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from common import ROOT, format_date, parse_date, read_text, render_page, write_text

MARKDOWN_DIR = ROOT / "markdown"
SECTIONS = ("posts", "projects")
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$")


def parse_front_matter(text):
    """Splits a markdown file into a dict of its front matter (simple `key: value` lines) and the rest."""
    match = re.match(r"---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text.lstrip("﻿"), re.DOTALL)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            meta[key.strip().lower()] = value.strip().strip("\"'")
    return meta, text[match.end():]


def split_title(body):
    """Takes the leading heading off the body. Returns (title, heading level, body), with None if there is no heading."""
    lines = body.lstrip("\n").splitlines()
    if lines:
        match = HEADING.match(lines[0])
        if match:
            return match.group(2), len(match.group(1)), "\n".join(lines[1:])
    return None, None, body


def render_markdown(body, heading_shift):
    md = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])
    tokens = md.parse(body)
    for token in tokens:
        if token.type in ("heading_open", "heading_close"):
            token.tag = f"h{min(max(int(token.tag[1]) + heading_shift, 1), 6)}"
    return md.renderer.render(tokens, md.options, {})


def style_images(body_html):
    """Gives images the site's img-fluid class, and turns an image on its own line into a centered figure with a caption."""
    soup = BeautifulSoup(body_html, "html.parser")
    for img in soup.find_all("img"):
        img["class"] = img.get("class", []) + ["img-fluid"]
        parent = img.parent
        if parent.name == "p" and len(parent.contents) == 1:
            figure = soup.new_tag("div", attrs={"class": "text-center"})
            img.extract()
            figure.append(soup.new_tag("br"))
            figure.append(img)
            if img.get("alt"):
                caption = soup.new_tag("figcaption")
                caption.string = img["alt"]
                figure.append(caption)
            figure.append(soup.new_tag("br"))
            parent.replace_with(figure)
    return str(soup)


def convert(md_path, html_path, is_post):
    """Writes the page for a markdown file. Returns True if the file was converted, False if it was skipped."""
    meta, body = parse_front_matter(read_text(md_path))
    title, title_level, body = split_title(body)
    title = meta.get("title", title or md_path.stem)

    if "date" not in meta:
        print(f"Skipped (draft, no date in front matter): {md_path.relative_to(ROOT)}")
        return False
    date = format_date(parse_date(meta["date"])) if is_post else None

    content = style_images(render_markdown(body, 3 - (title_level or 3)))
    main_html = f"""<div class="container text-left">
<h3>{html.escape(title, quote=False)}</h3>
{f'<time>{date}</time>' if date else ''}
<br/><br/>
{content}
</div>"""

    html_path.parent.mkdir(exist_ok=True)
    changed = write_text(html_path, render_page(html.escape(title, quote=False), main_html, depth=1))
    print(f"{'Generated' if changed else 'Unchanged'}: {html_path.relative_to(ROOT)}")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate HTML pages from markdown files.")
    parser.add_argument("files", nargs="*", help="markdown files to convert (default: everything in markdown/posts and markdown/projects)")
    args = parser.parse_args(argv)

    if args.files:
        md_files = [Path(f).resolve() for f in args.files]
    else:
        md_files = sorted(p for section in SECTIONS for p in (MARKDOWN_DIR / section).glob("*.md"))

    count = 0
    for md_path in md_files:
        section = md_path.parent.name
        if md_path.parent.parent != MARKDOWN_DIR or section not in SECTIONS:
            print(f"Skipped (must be in markdown/posts or markdown/projects): {md_path}")
            continue
        count += convert(md_path, ROOT / section / f"{md_path.stem}.html", is_post=(section == "posts"))
    print(f"Generated {count} page(s) from markdown.")


if __name__ == "__main__":
    sys.exit(main())
