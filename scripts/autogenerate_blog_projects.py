"""
Generates blog.html and projects.html: the lists of links to every page in posts/ and projects/.

Blog posts are sorted newest first, using the <time> on each post. Posts without a <time> are left out.
Projects are sorted using PROJECT_ORDER in common.py.
Unfinished pages go in drafts/ and are never listed.
The head, header and footer come from index.html.

Run with: python3 scripts/autogenerate_blog_projects.py
"""
import re

from common import (PROJECT_ORDER, ROOT, BLOG_INTRO, PROJECTS_INTRO, format_date, get_h3, parse_date,
                    read_text, render_page, write_text)


def get_entries(section):
    """The (title, date, href) of every listable page in posts/ or projects/. The date is None if the page has none."""
    entries = []
    for path in sorted((ROOT / section).glob("*.html")):
        href = f"{section}/{path.name}"
        html_str = read_text(path)
        title = get_h3(html_str)
        if not title:
            print(f"Skipped (no <h3> title): {href}")
            continue

        date = None
        match = re.search(r"<time>(.*?)</time>", html_str, re.DOTALL)
        if match:
            date = parse_date(" ".join(match.group(1).split()))
        entries.append((title, date, href))
    return entries


def get_entry_str(title, date, href):
    date_str = f'\n      <div class="date">\n       {format_date(date)}\n      </div>' if date else ""
    return f'<a class="list-group-item list-group-item-action" href="{href}">\n      {title}{date_str}\n     </a>'


def get_index_page(heading, intro, entries):
    links = "\n".join(get_entry_str(*entry) for entry in entries)
    main_html = f"""<div class="container text-left">
<h3>{heading}</h3>
<p>{intro}</p>
<br/>
<div class="list-group">
{links}
</div>
</div>"""
    return render_page(heading, main_html, depth=0)


def main():
    posts = []
    for title, date, href in get_entries("posts"):
        if date is None:
            print(f"Skipped (no <time>): {href}")
        else:
            posts.append((title, date, href))
    posts.sort(key=lambda entry: entry[1], reverse=True)

    def project_key(entry):
        name = entry[2].split("/")[-1].removesuffix(".html")
        return (PROJECT_ORDER.index(name) if name in PROJECT_ORDER else len(PROJECT_ORDER), entry[0].lower())

    projects = sorted(get_entries("projects"), key=project_key)

    for filename, heading, intro, entries in (("blog.html", "Blog posts", BLOG_INTRO, posts),
                                              ("projects.html", "Projects", PROJECTS_INTRO, projects)):
        changed = write_text(ROOT / filename, get_index_page(heading, intro, entries))
        print(f"{'Generated' if changed else 'Unchanged'}: {filename} ({len(entries)} entries)")


if __name__ == "__main__":
    main()
