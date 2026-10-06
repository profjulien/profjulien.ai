# profjulien.ai

Landing page for Prof Julien Salanave — ESSEC Business School, Singapore.

One self-contained file. No build step, no dependencies, no external assets
beyond Google Fonts: drop `index.html` on any static host.

## Design

The web surface of the `profjulien-design` presentation system (palette, type
pair and devices live in `~/.claude/skills/profjulien-design`). Limestone ground,
pine structure, plum as the single accent. Radii are 0. No gradients, no shadows.
The page reads as a sequence of full-width bands, one idea each, with two
inverted bands breaking the rhythm — the statement and the footer, which always
carry the opposite ground to the page in either theme.

## Files

| File | What |
| --- | --- |
| `index.html` | the landing page — CSS, the portrait and the chart are all inlined |
| `founder-wisdom.html` | the shelf, generated — do not hand-edit |
| `founder-wisdom.json` | **the system of record for the shelf** |
| `build.py` | regenerates the shelf page and the landing-page teaser from the JSON |
| `portrait-web.jpg` | the processed 1200×1000 crop, also embedded in the page |
| `wui-2026-07.json` | World Uncertainty Index, 223 monthly points, 2008-01 to 2026-07 |

## Adding to Founder wisdom

This shelf used to live in Notion. It lives here now. To add an entry, append an
object to `entries` in `founder-wisdom.json`:

```json
{ "title": "...", "author": "...", "url": "https://...",
  "themes": ["Scaling"], "tldr": "The one line you would actually say.",
  "tldr_by": "julien" }
```

Then:

```bash
python3 build.py
```

That rewrites `founder-wisdom.html` and the five-entry teaser on the landing
page, re-sorts everything by theme, and recounts the filter chips. Commit both.
The build prints a warning for any entry missing a source link, and for any
`tldr_by: "claude"` still awaiting review.

`themes` must come from `theme_order` in the same file. An entry with no `url`
renders unlinked rather than as a dead link.

**Never paste the source's own prose into `tldr`.** The repo is public. The point
of the shelf is the one line of judgement; the link sends the reader to the
author for the rest. The full Notion archive, which *does* contain long
third-party excerpts, is kept privately outside this repo at
`~/Desktop/founder-wisdom-notion-backup/`.

## The chart

Real data, not decoration: the WUI monthly GDP-weighted series across 71
countries, from the publisher's July 2026 release. Event markers sit on their
true dates — Covid 2020-03, ChatGPT 2022-11, Trump II 2025-01. If the series is
refreshed, every marker's x position must be recomputed, because they are stored
as fractions of the series length.

Source: worlduncertaintyindex.com

## Hidden

The Writing section carries `hidden` until the first piece is published. To bring
it back, delete the attribute and restore the nav link — both flagged in a
comment above the section.
