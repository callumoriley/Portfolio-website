# Portfolio website

Source for [callumoriley.ca](https://callumoriley.ca), hosted on GitHub Pages from the `gh-pages` branch.
The site is plain HTML with Bootstrap. A few Python scripts in `scripts/` generate and tidy the pages.

`_config.yml` keeps this README, `markdown/`, `drafts/`, `scripts/` and `todo.md` out of the published site.

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | The home page. **Its `<head>`, `<header>` and `<footer>` are the template for every other page.** |
| `blog.html`, `projects.html` | Lists of links. **Generated**, don't edit by hand. |
| `posts/`, `projects/` | Finished pages. Either generated from `markdown/` or written by hand. |
| `drafts/posts/`, `drafts/projects/` | Unfinished hand-written pages. Never listed and not published. |
| `markdown/posts/`, `markdown/projects/` | Markdown sources that become pages in `posts/` and `projects/`. |
| `assets/` | Images. |
| `scripts/` | The scripts described below. |

## Drafts

- **Markdown**: a file in `markdown/` with no `date` is a draft (see below). Nothing is generated from it.
- **Hand-written HTML**: keep it in `drafts/posts/` or `drafts/projects/` until it's done, then move it to `posts/` or
  `projects/` and run the build. The build fixes the page's links (header and `assets/`) for its new folder, and
  `blog.html`/`projects.html` pick it up. A post also needs a `<time>` to be listed.
- **Images for a draft**: put them in `drafts/assets/` (same structure as `assets/`). The build points a draft's images at
  `drafts/assets/` if they're there, otherwise at `assets/`. When you publish the page, move its images to `assets/` too;
  the build warns about any image it can't find.

`drafts/` is excluded from the published site (`_config.yml`), but it is still in the git repository.

## Writing a post or project in markdown

The markdown converter is **only run locally**; the GitHub Action doesn't run it. After running it, commit the generated pages.

1. Create `markdown/posts/<name>.md` (or `markdown/projects/<name>.md`). It becomes `posts/<name>.html`.
2. The first line is the page title (a `#`, `##` or `###` heading). Other headings are shifted so sections become `<h4>`.
   Whatever level the title is, the headings under it keep their relative order.
3. Images: `![Caption shown under the image](../assets/folder/picture.jpg)` on a line of its own.
   Raw HTML (like an `<iframe>` for a video) works too.
4. When it's ready to publish, add a date at the very top of the file:

   ```
   ---
   date: 2026-01-31
   ---
   ## My title
   ```

   `January 31st, 2026` also works. You can add `title: ...` there as well to override the first heading.

**A markdown file with no `date` is a draft: it is never published.** Posts show the date under the title and are sorted
by it on `blog.html`. Projects don't show the date, but still need one to be published.
To unpublish, remove the date *and* delete the generated `.html` (the scripts never delete pages).

If a hand-written page already exists with the same name, publishing the markdown file **overwrites** it.

## The scripts

Install the dependencies once with `pip install -r requirements.txt`. All of the scripts can be run from any directory.

| Script | What it does |
| --- | --- |
| `page_gen.py` | Converts markdown to pages in `posts/` and `projects/`. `python scripts/page_gen.py [file.md ...]`. |
| `autogenerate_blog_projects.py` | Rebuilds `blog.html` and `projects.html` from the pages in `posts/` and `projects/`. |
| `common_header_footer.py` | Copies `index.html`'s head, header and footer into every other page (keeping each page's title). |
| `title_script.py` | Sets every page's `<title>` to `Callum O'Riley | <the page's h3 heading>`. |
| `format_html.py` | Pretty-prints all of the HTML so diffs stay small. |
| `build_site.py` | Runs all of the above in that order. |
| `common.py` | Shared code and settings, not run directly. |

Run everything locally with:

```
python scripts/build_site.py
```

The Action only runs the last four scripts (see below), so it is fine to run just `page_gen.py` and commit.

To change something on every page (a nav link, the footer, the analytics snippet), edit it in `index.html` and run the build.

### What gets listed on `blog.html` and `projects.html`

- **Posts**: every page in `posts/` with a `<time>`, newest first.
- **Projects**: every page in `projects/`, in the order of `PROJECT_ORDER` in `scripts/common.py` (others go last, alphabetically).
- Pages in `drafts/` are never listed.

Anything in `posts/` or `projects/` is reachable by its URL once it is pushed to `gh-pages`, listed or not, so don't put
unfinished pages there.

## GitHub Action

`.github/workflows/build-site.yml` runs `autogenerate_blog_projects.py`, `common_header_footer.py`, `title_script.py` and
`format_html.py` (as separate steps, in that order) on every push to `gh-pages` that touches pages or scripts, and on demand
from the Actions tab. It does **not** run `page_gen.py`. If anything changed it commits the result as `github-actions[bot]`.
On pull requests it runs the same steps but doesn't commit, so you can see if they break.

Because the action commits to `gh-pages`, run `git pull` before you start working.
