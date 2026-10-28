"""
Makes the head, header and footer of every HTML page the same as the ones in index.html, so that a change to the
site-wide parts only has to be made once. Each page keeps its own <title> (see title_script.py), and pages in
subfolders get "../" added to the links in the header (and to their links to assets/, so a page can be moved between
folders, for example from drafts/posts/ to posts/).

Run with: python3 scripts/common_header_footer.py
"""
from common import (ROOT, depth_of, fix_asset_paths, get_section, html_files, load_template, read_text, relative_header,
                    set_section, write_text)


def main():
    template = load_template()
    index = ROOT / "index.html"

    for path in html_files():
        if path == index:
            continue

        html_str = read_text(path)
        if any(get_section(html_str, tag) is None for tag in template):
            print(f"Skipped (missing <head>, <header> or <footer>): {path.relative_to(ROOT)}")
            continue

        page_title = get_section(html_str, "head")
        title_start, title_end = page_title.find("<title>"), page_title.find("</title>")
        head = template["head"]
        if title_start != -1 and title_end != -1:
            # keep the page's own title instead of index.html's
            head = head[:head.find("<title>")] + page_title[title_start:title_end + len("</title>")] + head[head.find("</title>") + len("</title>"):]

        depth = depth_of(path)
        html_str = set_section(html_str, "head", head)
        html_str = set_section(html_str, "header", relative_header(template["header"], depth))
        html_str = set_section(html_str, "footer", template["footer"])
        html_str = fix_asset_paths(html_str, path)

        if write_text(path, html_str):
            print(f"Updated: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
