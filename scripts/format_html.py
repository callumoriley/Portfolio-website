"""
Pretty-prints every HTML page so that the files stay consistently indented and diffs stay small.

Run with: python3 scripts/format_html.py
"""
from bs4 import BeautifulSoup

from common import ROOT, html_files, read_text, write_text


def format_html_file(path):
    formatted_html = BeautifulSoup(read_text(path), "html.parser").prettify()
    if write_text(path, formatted_html):
        print(f"Formatted: {path.relative_to(ROOT)}")


def main():
    for path in html_files():
        format_html_file(path)


if __name__ == "__main__":
    main()
