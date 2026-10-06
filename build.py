#!/usr/bin/env python3
"""Rebuild founder-wisdom.html and the teaser band in index.html from founder-wisdom.json.

Add or edit an entry in founder-wisdom.json, then:  python3 build.py
"""
import json, html, re, pathlib, sys

HERE = pathlib.Path(__file__).parent
data = json.loads((HERE / "founder-wisdom.json").read_text(encoding="utf-8"))
E, ORDER = data["entries"], data["theme_order"]
LABEL = {t: data["theme_labels"].get(t, t) for t in ORDER}
esc = lambda t: html.escape(t or "", quote=True)

def kind(u):
    if not u: return "no link yet"
    if "youtu" in u: return "talk"
    if "ted.com" in u: return "TED talk"
    if u.endswith(".pdf"): return "paper"
    if "readwise" in u: return "tool"
    return "essay"

def theme_of(e):
    for t in ORDER:
        if t in e["themes"]: return t
    return e["themes"][0] if e["themes"] else "Tools"

def row(e, as_link=True):
    th = theme_of(e)
    meta = " &nbsp;·&nbsp; ".join(x for x in [esc(e["author"]), kind(e["url"])] if x)
    inner = (f'          <div>\n'
             f'            <p class="fw-t">{esc(e["title"])}</p>\n'
             f'            <p class="fw-by">{meta}</p>\n'
             f'            <span class="fw-tag">{esc(LABEL.get(th, th))}</span>\n'
             f'          </div>\n'
             f'          <p class="fw-take">{esc(e["tldr"])}</p>')
    if e["url"] and as_link:
        return f'        <a class="fw" data-tag="{esc(th)}" href="{esc(e["url"])}" rel="noopener">\n{inner}\n        </a>'
    return f'        <div class="fw fw--nolink" data-tag="{esc(th)}">\n{inner}\n        </div>'

ordered = sorted(E, key=lambda e: (ORDER.index(theme_of(e)) if theme_of(e) in ORDER else 99,
                                   e["title"].lower()))
counts = {}
for e in ordered: counts[theme_of(e)] = counts.get(theme_of(e), 0) + 1

# ---------- page ----------
page = (HERE / "founder-wisdom.html").read_text(encoding="utf-8")
chips = ['<button class="chip" type="button" data-filter="all" aria-pressed="true">All '
         f'<span class="chip-n">{len(ordered)}</span></button>']
for t in ORDER:
    if t in counts:
        chips.append(f'<button class="chip" type="button" data-filter="{esc(t)}" aria-pressed="false">'
                     f'{esc(LABEL.get(t,t))} <span class="chip-n">{counts[t]}</span></button>')

page = re.sub(r'(<div class="chips"[^>]*>)(.*?)(</div>)',
              lambda m: m.group(1) + "\n        " + "\n        ".join(chips) + "\n      " + m.group(3),
              page, count=1, flags=re.S)
page = re.sub(r'(<div class="fw-list" id="fw-list">)(.*?)(\n      </div>)',
              lambda m: m.group(1) + "\n" + "\n".join(row(e) for e in ordered) + m.group(3),
              page, count=1, flags=re.S)
page = re.sub(r'<p class="counter">[^<]*</p>',
              f'<p class="counter">{len(ordered)} entries &nbsp;·&nbsp; {len(counts)} themes</p>',
              page, count=1)
(HERE / "founder-wisdom.html").write_text(page, encoding="utf-8")

# ---------- teaser band on the landing page ----------
TEASER = ["How to get startup ideas", "How to do great work", "How to legally own another person",
          "You’re not a lottery ticket", "Wartime vs. peacetime CEO"]
by = {e["title"]: e for e in E}
picks = [by[t] for t in TEASER if t in by] or ordered[:5]

idx = (HERE / "index.html").read_text(encoding="utf-8")
start, end = "<!-- fw:teaser:start -->", "<!-- fw:teaser:end -->"
if start in idx:
    block = ("\n" + "\n".join(row(e) for e in picks) + "\n      ")
    idx = re.sub(re.escape(start) + r".*?" + re.escape(end),
                 start + block + end, idx, count=1, flags=re.S)
    idx = re.sub(r'(id="founder-wisdom".*?)<p class="counter">[^<]*</p>',
                 lambda m: m.group(1) + f'<p class="counter">{len(ordered)} entries &nbsp;·&nbsp; {len(counts)} themes</p>',
                 idx, count=1, flags=re.S)
    idx = re.sub(r'All \d+ entries', f'All {len(ordered)} entries', idx, count=1)
    (HERE / "index.html").write_text(idx, encoding="utf-8")
else:
    print("note: teaser markers missing in index.html — band left untouched", file=sys.stderr)

drafted = [e["title"] for e in E if e.get("tldr_by") == "claude"]
print(f"built {len(ordered)} entries across {len(counts)} themes")
if drafted: print(f"  {len(drafted)} TLDRs still flagged tldr_by=claude (unreviewed)")
for e in E:
    if not e["url"]: print(f"  no source link: {e['title']}")
