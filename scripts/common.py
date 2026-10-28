"""
Shared helpers for the site maintenance scripts.

index.html is the source of truth for the <head>, <header> and <footer> of every page.
The scripts in this folder can be run from any directory, as all paths are resolved from the repository root.
"""
import os
import re
import time
from datetime import datetime
from pathlib import Path

WRITE_ATTEMPTS = 5

ROOT = Path(__file__).resolve().parent.parent
DRAFTS_DIR = ROOT / "drafts"
SITE_NAME = "Callum O'Riley"
SKIP_DIRS = {"env", "venv", "node_modules", "markdown", "assets", "scripts"}

# Text shown above the lists on the generated index pages
BLOG_INTRO = 'This is where I write about smaller projects that are in less of a polished or finished state than the projects in the "Projects" page. I also might write on some non-technical topics.'
PROJECTS_INTRO = "These are the projects that I am most proud of and put the most amount of work into."

# Projects have no dates, so their order on projects.html is set here (file names without .html).
# Projects not listed go after these, alphabetically.
PROJECT_ORDER = ["magneticFluxCamera", "breadboardComputer", "nanoSCMotorDriver", "ballRobot", "sonarMappingSystem"]


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    """Writes the file with LF line endings. Returns True if the contents changed."""
    if Path(path).exists() and read_text(path) == text:
        return False
    for attempt in range(1, WRITE_ATTEMPTS + 1):
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            return True
        except OSError:
            # On Windows, OneDrive can briefly lock a file it is syncing and the write fails with "Invalid argument"
            if attempt == WRITE_ATTEMPTS:
                raise
            time.sleep(0.5 * attempt)


def html_files():
    """Every page of the site, as paths. Skips folders that don't contain pages."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.lower().endswith(".html"):
                yield Path(dirpath) / name


def depth_of(path):
    """How many folders deep a page is (0 for pages in the repository root)."""
    return len(Path(path).resolve().relative_to(ROOT).parts) - 1


def get_section(html, tag):
    """The contents of the first <tag>...</tag> in the html, or None if there isn't one."""
    match = re.search(rf"<{tag}>(.*?)</{tag}>", html, re.DOTALL)
    return match.group(1) if match else None


def set_section(html, tag, inner):
    return re.sub(rf"<{tag}>.*?</{tag}>", lambda _: f"<{tag}>{inner}</{tag}>", html, count=1, flags=re.DOTALL)


def get_h3(html):
    """The page's main heading, with whitespace collapsed."""
    match = re.search(r"<h3>(.*?)</h3>", html, re.DOTALL)
    return " ".join(match.group(1).split()) if match else None


def set_title(html, heading):
    title = f"{SITE_NAME} | {heading}" if heading else SITE_NAME
    return re.sub(r"<title>.*?</title>", lambda _: f"<title>{title}</title>", html, count=1, flags=re.DOTALL)


def relative_header(header, depth):
    """Prefixes the header's relative links with ../ for pages that are in subfolders."""
    return re.sub(r'href="(?![a-z]+:|#|/)', 'href="' + "../" * depth, header)


def fix_asset_paths(html, path):
    """
    Points the page's links to assets/ at the right place for the folder the page is in, so pages can be moved between
    folders. Pages in drafts/ look in drafts/assets/ first (for the images of unfinished pages), then in assets/.
    """
    page_dir = Path(path).resolve().parent
    in_drafts = DRAFTS_DIR in page_dir.parents or page_dir == DRAFTS_DIR

    def fix(match):
        name = match.group(2)
        assets_dir = ROOT / "assets"
        if in_drafts and (DRAFTS_DIR / "assets" / name).exists():
            assets_dir = DRAFTS_DIR / "assets"
        elif not (assets_dir / name).exists():
            print(f"Warning: {Path(path).resolve().relative_to(ROOT)} links to a missing image: assets/{name}")
        return match.group(1) + os.path.relpath(assets_dir, page_dir).replace(os.sep, "/") + "/" + name

    return re.sub(r'((?:src|href|data)=")(?:\.\./)*assets/([^"]*)', fix, html)


def load_template():
    """The head, header and footer contents (as found in index.html)."""
    index = read_text(ROOT / "index.html")
    parts = {tag: get_section(index, tag) for tag in ("head", "header", "footer")}
    missing = [tag for tag, inner in parts.items() if inner is None]
    if missing:
        raise RuntimeError(f"index.html is missing: {', '.join('<' + tag + '>' for tag in missing)}")
    return parts


def render_page(heading, main_html, depth):
    """A complete page: the common head/header/footer around the given <main> contents."""
    template = load_template()
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>{template['head']}</head>
<body>
<header>{relative_header(template['header'], depth)}</header>
<main>
{main_html}
</main>
<footer>{template['footer']}</footer>
</body>
</html>
"""
    return set_title(page, heading)


def parse_date(text):
    """Accepts 2025-12-22 or the style used on the site: December 22nd, 2025."""
    text = text.strip()
    try:
        return datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return datetime.strptime(re.sub(r"(\d+)(st|nd|rd|th)", r"\1", text), "%B %d, %Y")


def format_date(dt):
    suffix = "th" if 11 <= dt.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(dt.day % 10, "th")
    return f"{dt.strftime('%B')} {dt.day}{suffix}, {dt.year}"
