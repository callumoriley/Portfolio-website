"""
Runs all of the site scripts in order. The pre-commit hook (.githooks/pre-commit) runs this before every commit.

    1. page_gen                    markdown/  ->  posts/ and projects/ pages
    2. autogenerate_blog_projects  blog.html and projects.html (lists of links)
    3. common_header_footer        same head/header/footer everywhere
    4. title_script                page titles
    5. format_html                 tidy up the HTML

Run with: python3 scripts/build_site.py
"""
import autogenerate_blog_projects
import common_header_footer
import format_html
import page_gen
import title_script

STEPS = [
    ("Generating pages from markdown", lambda: page_gen.main([])),
    ("Generating blog and projects lists", autogenerate_blog_projects.main),
    ("Syncing head, header and footer", common_header_footer.main),
    ("Setting page titles", title_script.main),
    ("Formatting HTML", format_html.main),
]

if __name__ == "__main__":
    for name, step in STEPS:
        print(f"\n== {name}")
        step()
