"""
Sets the <title> of every page (except index.html) to "Callum O'Riley | <the page's h3 heading>".

Run with: python3 scripts/title_script.py
"""
from common import ROOT, get_h3, html_files, read_text, set_title, write_text


def main():
    index = ROOT / "index.html"

    for path in html_files():
        if path == index:
            continue

        html_str = read_text(path)
        heading = get_h3(html_str)
        if heading is None:
            print(f"Skipped (no <h3>): {path.relative_to(ROOT)}")
            continue

        if write_text(path, set_title(html_str, heading)):
            print(f"Updated title: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
