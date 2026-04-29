import os
from bs4 import BeautifulSoup

def format_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    formatted_html = soup.prettify()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(formatted_html)

    print(f"Formatted: {filepath}")

def format_all_html(root_dir="."):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".html"):
                filepath = os.path.join(root, file)
                format_html_file(filepath)

if __name__ == "__main__":
    format_all_html()

