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
| `assets/<page name>/` | Images, in one folder per page named after the page (`assets/ballRobot/` for `projects/ballRobot.html`). `assets/unused/` is for images no page uses. |
| `scripts/` | The scripts described below. |

## Drafts

- **Markdown**: a file in `markdown/` with no `date` is a draft (see below). Nothing is generated from it.
- **Hand-written HTML**: keep it in `drafts/posts/` or `drafts/projects/` until it's done, then move it to `posts/` or
  `projects/` and run the build. The build fixes the page's links (header and `assets/`) for its new folder, and
  `blog.html`/`projects.html` pick it up. A post also needs a `<time>` to be listed.
- **Images for a draft**: put them in `drafts/assets/<page name>/` (same structure as `assets/`). The build points a
  draft's images at `drafts/assets/` if they're there, otherwise at `assets/`. When you publish the page, move the
  folder to `assets/<page name>/` too; the build warns about any image it can't find.

`drafts/` is excluded from the published site (`_config.yml`), but it is still in the git repository.

## Writing a post or project in markdown

The markdown converter runs as part of the build, which the pre-commit hook runs on every commit (see below), so the
generated pages end up in the same commit as the markdown.

1. Create `markdown/posts/<name>.md` (or `markdown/projects/<name>.md`). It becomes `posts/<name>.html`.
2. The first line is the page title (a `#`, `##` or `###` heading). Other headings are shifted so sections become `<h4>`.
   Whatever level the title is, the headings under it keep their relative order.
3. Images go in `assets/<page name>/`: `![Caption shown under the image](../assets/<page name>/picture.jpg)` on a line of its own.
   Videos: an `<iframe>` on a line of its own, and its `title` becomes the caption:
   `<iframe src="https://drive.google.com/file/d/…/preview" width="640" height="360" allow="autoplay" allowfullscreen title="Caption"></iframe>`.
   Both are centered automatically. Other raw HTML works too.
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
| `check_links.py` | Checks every local link (images, videos, links to other pages) in all pages and markdown files, and lists images nothing links to. Case-sensitive, because GitHub Pages is but Windows isn't. Not part of the build: run it yourself. |
| `common.py` | Shared code and settings, not run directly. |

Run everything with:

```
python scripts/build_site.py
```

You usually don't need to: the pre-commit hook does it for you (see below).

To change something on every page (a nav link, the footer, the analytics snippet), edit it in `index.html` and run the build.

### What gets listed on `blog.html` and `projects.html`

- **Posts**: every page in `posts/` with a `<time>`, newest first.
- **Projects**: every page in `projects/`, in the order of `PROJECT_ORDER` in `scripts/common.py` (others go last, alphabetically).
- Pages in `drafts/` are never listed.

Anything in `posts/` or `projects/` is reachable by its URL once it is pushed to `gh-pages`, listed or not, so don't put
unfinished pages there.

## Pre-commit hook

`.githooks/pre-commit` runs `scripts/build_site.py` every time you run `git commit`, then adds the regenerated `.html`
files to that same commit. Nothing builds or commits on GitHub, so you never have to pull commits made by a bot.

Git doesn't enable hooks from a cloned repository, so run this once in each clone:

```
git config core.hooksPath .githooks
```

- It uses `env/python.exe` (the conda environment in this folder) if it exists, otherwise `python3`/`python`.
- If you have **unstaged** changes to `.html` files it stops and asks you to stage or stash them first, because the build
  rewrites every page and would mix your changes with its own.
- If the build crashes, the commit is aborted. Run `python scripts/build_site.py` by hand to see the error.
- `git commit --no-verify` skips the hook for one commit.
- Commits made on github.com don't run the hook, so run the build yourself afterwards.

## GitHub Action

`.github/workflows/check-links.yml` runs `scripts/check_links.py` on every push to `gh-pages`, on every pull request, and on
demand from the Actions tab. It fails (red cross, and an email from GitHub) if a page or markdown file links to something
that doesn't exist or has the wrong capitalisation. It only reads the repository: it never changes or commits anything, so
there is nothing to pull afterwards. The list of unused images it prints is just for information.
