#!/usr/bin/env python3
"""
build_posts.py — Turn Markdown files in content/ into website pages.

WORKFLOW
--------
1. Create a Markdown file in the content/ folder, e.g. content/my-post.md
2. Put a frontmatter block at the top (see content/_TEMPLATE.md).
3. Run:  python build_posts.py
   (or, to build just one file:  python build_posts.py content/my-post.md)

The script will:
  * generate post/<slug>.html from your Markdown, and
  * add/update a card for it on the page you chose (blog / projects /
    research / teaching), newest first.

Re-running is safe: it updates existing posts in place instead of
duplicating them. The slug comes from the file name (my-post.md -> my-post).

No external libraries needed — just Python 3.
"""

import sys
import os
import re
import html
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
POST_DIR = os.path.join(ROOT, "post")

# Which listing page each `page:` value maps to, and the card style it uses.
PAGES = {
    "blog":     {"file": "blog.html",     "style": "blog",  "cta": "Read More"},
    "projects": {"file": "projects.html", "style": "card",  "cta": "View Project"},
    "research": {"file": "research.html", "style": "card",  "cta": "View Research"},
    "teaching": {"file": "teaching.html", "style": "card",  "cta": "View"},
}

START = "<!-- AUTO-POSTS:START -->"
END = "<!-- AUTO-POSTS:END -->"


# --------------------------------------------------------------------------
# Frontmatter + Markdown parsing
# --------------------------------------------------------------------------
def parse_frontmatter(text):
    """Split a `--- key: value --- body` file into (meta dict, body str)."""
    if not text.startswith("---"):
        raise ValueError("File must begin with a '---' frontmatter block.")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Frontmatter block is not closed with a second '---'.")
    meta = {}
    for line in parts[1].strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        meta[key.strip().lower()] = val.strip().strip('"').strip("'")
    return meta, parts[2].strip()


def md_inline(text):
    """Inline Markdown: escape HTML, then apply links/bold/italic/code."""
    text = html.escape(text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)",
                  r'<img src="\2" alt="\1" style="max-width:100%;border-radius:8px;">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def md_to_html(body):
    """Minimal block-level Markdown -> HTML (headings, lists, images, paras)."""
    lines = body.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1)) + 1  # h1 reserved for hero title
            level = min(level, 6)
            out.append(f"<h{level}>{md_inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # Standalone image
        if re.match(r"^!\[[^\]]*\]\([^)]+\)$", stripped):
            m2 = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", stripped)
            alt, src = m2.group(1), m2.group(2)
            fig = ['<figure style="margin:0;">',
                   f'<img src="{src}" alt="{html.escape(alt)}" '
                   'style="width:100%;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1);">']
            if alt:
                fig.append('<figcaption style="margin-top:0.75rem;font-size:0.95rem;'
                           'color:var(--color-text-light);text-align:center;'
                           f'font-style:italic;">{html.escape(alt)}</figcaption>')
            fig.append("</figure>")
            out.append("\n".join(fig))
            i += 1
            continue

        # Unordered list
        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(f"<li>{md_inline(lines[i].strip()[2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(f"<li>{md_inline(re.sub(r'^\d+\.\s+', '', lines[i].strip()))}</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue

        # Paragraph (gather consecutive non-blank lines)
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,4}\s|[-*]\s|\d+\.\s|!\[)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{md_inline(' '.join(para))}</p>")

    return "\n            ".join(out)


# --------------------------------------------------------------------------
# HTML generation
# --------------------------------------------------------------------------
def build_post_page(meta, body_html):
    title = html.escape(meta["title"])
    subtitle = html.escape(meta.get("subtitle", ""))
    category = html.escape(meta.get("category", ""))
    date = html.escape(meta.get("date", ""))
    subtitle_html = f'<p class="post-hero-subtitle">{subtitle}</p>' if subtitle else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Chandra Gummaluru</title>
    <link rel="stylesheet" href="../styles.css">
    <link rel="stylesheet" href="../post-styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="nav-container">
        <div class="nav-content">
            <a href="../index.html" class="logo">Chandra Gummaluru</a>
            <div class="nav-links">
                <a href="../index.html" class="nav-link">Home</a>
                <a href="../teaching.html" class="nav-link">Teaching</a>
                <a href="../research.html" class="nav-link">Research</a>
                <a href="../projects.html" class="nav-link">Projects</a>
                <a href="../blog.html" class="nav-link">Blog</a>
            </div>
        </div>
    </nav>

    <!-- Hero Banner -->
    <section class="post-hero">
        <div class="post-hero-content">
            <div class="post-meta">
                <span class="post-category">{category}</span>
                <span class="post-date">{date}</span>
            </div>
            <h1 class="post-hero-title">{title}</h1>
            {subtitle_html}
        </div>
        <div class="post-hero-graphic">
            <div class="graphic-circle"></div>
            <div class="graphic-square"></div>
            <div class="graphic-triangle"></div>
        </div>
    </section>

    <!-- Content -->
    <article class="post-content">
        <div class="post-container">
            <section class="content-block">
                <div class="block-content">
            {body_html}
                </div>
            </section>

            <nav class="post-navigation">
                <a href="../{meta['_page_file']}" class="nav-back">
                    <span class="nav-arrow">&larr;</span>
                    Back
                </a>
            </nav>
        </div>
    </article>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <p class="footer-text">&copy; 2025 Chandra Gummaluru</p>
            <div class="footer-links">
                <a href="mailto:chandra@cs.toronto.edu" class="footer-link">Email</a>
                <a href="https://github.com/chandra-gummaluru" class="footer-link">GitHub</a>
                <a href="#" class="footer-link">Google Scholar</a>
            </div>
        </div>
    </footer>
</body>
</html>
"""


def build_card(meta, slug):
    """Card markup for a listing page. Wrapped in slug-tagged comments."""
    style = meta["_style"]
    cta = html.escape(meta.get("link_label") or meta["_cta"])
    title = html.escape(meta["title"])
    date = html.escape(meta.get("date", ""))
    excerpt = html.escape(meta.get("excerpt", ""))
    category = html.escape(meta.get("category", "Post"))
    # Link: explicit `link:` wins, otherwise the generated post page.
    link = html.escape(meta.get("link") or f"./post/{slug}.html")
    tag = f"<!-- post:{slug} -->"

    if style == "blog":
        return f"""{tag}
                <a href="{link}" class="blog-post">
                    <div class="blog-post-meta">
                        <span class="card-badge">{category}</span>
                        <span class="blog-post-date">{date}</span>
                    </div>
                    <h3 class="blog-post-title">{title}</h3>
                    <p class="blog-post-excerpt">
                        {excerpt}
                    </p>
                </a>"""

    # card-with-image style
    size = meta.get("size", "medium")
    cover = meta.get("cover", "")
    if cover:
        img_style = f"background-image: url('{html.escape(cover)}'); background-color: #667eea;"
    else:
        img_style = "background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);"
    return f"""{tag}
                <div class="card-with-image {size}">
                    <div class="card-image" style="{img_style}"></div>
                    <div class="card-content">
                        <div class="card-badge">{category}</div>
                        <h3 class="card-title">{title}</h3>
                        <p class="card-date">{date}</p>
                        <p class="card-excerpt">
                            {excerpt}
                        </p>
                        <a href="{link}" class="card-link">{cta}</a>
                    </div>
                </div>"""


def insert_card(page_file, slug, card_html):
    """Insert (or replace) a slug-tagged card between the AUTO-POSTS markers."""
    path = os.path.join(ROOT, page_file)
    with open(path, "r", encoding="utf-8") as f:
        page = f.read()

    if START not in page or END not in page:
        raise ValueError(f"{page_file} is missing the AUTO-POSTS markers.")

    before, rest = page.split(START, 1)
    region, after = rest.split(END, 1)

    # Drop any existing block for this slug so re-runs update in place.
    tag = f"<!-- post:{slug} -->"
    if tag in region:
        pattern = re.compile(
            re.escape(tag) + r".*?(?=<!-- post:|\Z)", re.DOTALL)
        region = pattern.sub("", region)

    # Newest first: prepend.
    new_region = "\n                " + card_html.strip() + "\n" + region.rstrip() + "\n                "
    page = before + START + new_region + END + after
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------
def process(md_path):
    slug = os.path.splitext(os.path.basename(md_path))[0]
    with open(md_path, "r", encoding="utf-8") as f:
        meta, body = parse_frontmatter(f.read())

    if "title" not in meta:
        raise ValueError(f"{md_path}: frontmatter needs a 'title:'.")
    page = meta.get("page", "blog").lower()
    if page not in PAGES:
        raise ValueError(f"{md_path}: page '{page}' must be one of {list(PAGES)}.")

    cfg = PAGES[page]
    meta["_style"] = cfg["style"]
    meta["_cta"] = cfg["cta"]
    meta["_page_file"] = cfg["file"]

    # Only generate a post page when the card links to one (no external `link:`).
    if not meta.get("link"):
        body_html = md_to_html(body)
        os.makedirs(POST_DIR, exist_ok=True)
        out = os.path.join(POST_DIR, f"{slug}.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(build_post_page(meta, body_html))
        print(f"  wrote post/{slug}.html")

    insert_card(cfg["file"], slug, build_card(meta, slug))
    print(f"  added '{meta['title']}' to {cfg['file']}")


def main():
    args = sys.argv[1:]
    if args:
        paths = args
    else:
        if not os.path.isdir(CONTENT_DIR):
            print("No content/ folder found. Create one and add .md files.")
            return
        paths = [os.path.join(CONTENT_DIR, f)
                 for f in sorted(os.listdir(CONTENT_DIR))
                 if f.endswith(".md") and not f.startswith("_")]
        if not paths:
            print("No .md files in content/ (files starting with _ are ignored).")
            return

    for p in paths:
        print(f"Processing {os.path.relpath(p, ROOT)} ...")
        try:
            process(p)
        except Exception as e:
            print(f"  ERROR: {e}")
    print("Done.")


if __name__ == "__main__":
    main()
