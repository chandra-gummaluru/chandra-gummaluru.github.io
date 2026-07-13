# Adding posts to the website

You add new posts/projects/etc. by writing a Markdown file here in `content/`,
then running one command. No HTML by hand.

## Steps

1. Copy `_TEMPLATE.md` to a new file. The file name becomes the URL slug,
   e.g. `content/new-bus-screens.md` -> `post/new-bus-screens.html`.
2. Fill in the frontmatter (the block between the two `---` lines) and write
   your content in Markdown below it.
3. From the site's top folder, run:

   ```
   python build_posts.py
   ```

   That processes every `.md` file in `content/`. To build just one:

   ```
   python build_posts.py content/new-bus-screens.md
   ```

4. Commit and push. Done — the post page is generated and a card is added to
   the page you chose, newest first.

## Frontmatter fields

| Field        | Required | Notes                                                        |
|--------------|----------|--------------------------------------------------------------|
| `title`      | yes      | Post title.                                                  |
| `page`       | yes*     | Where the card goes: `blog`, `projects`, `research`, `teaching`. Defaults to `blog`. |
| `date`       | no       | Shown on the card and post, e.g. `July 12, 2026`.            |
| `category`   | no       | The small badge label.                                       |
| `excerpt`    | no       | Card summary (1-2 sentences).                                |
| `subtitle`   | no       | One line under the title on the post page.                   |
| `cover`      | no       | Card background image (projects/research/teaching cards).    |
| `size`       | no       | `large` or `medium` (image-card pages). Default `medium`.    |
| `link_label` | no       | Button text on the card.                                     |
| `link`       | no       | Point the card at an external URL instead of generating a post page. |

## Notes

- Re-running the script is safe. It updates a post in place (matched by file
  name) instead of adding a duplicate.
- Files starting with `_` (like `_TEMPLATE.md`) are ignored.
- To remove a post, delete its `post/<slug>.html`, then delete the
  `<!-- post:<slug> -->` card block from the listing page (between the
  `AUTO-POSTS` markers).
- Markdown supported: headings, paragraphs, **bold**, *italic*, `code`,
  [links](url), bullet/numbered lists, and images `![caption](path)`.
