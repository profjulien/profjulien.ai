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
| `index.html` | the page — CSS, the portrait and the chart are all inlined |
| `portrait-web.jpg` | the processed 1200×1000 crop, also embedded in the page |
| `wui-2026-07.json` | World Uncertainty Index, 223 monthly points, 2008-01 to 2026-07 |

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
