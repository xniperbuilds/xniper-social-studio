---
name: xniper-social-studio
description: >-
  Design premium, scroll-stopping social media graphics from a text brief — and
  export them to exact-size, pixel-perfect PNGs. Use whenever the user wants to
  create, design, make, or generate a social post, carousel, story, reel cover,
  thumbnail, quote card, announcement, promo, ad creative, or any branded image
  for Instagram, Facebook, LinkedIn, X/Twitter, TikTok, YouTube, Pinterest, or
  Threads. Triggers on: "design a post", "make a carousel", "story for", "IG
  post", "thumbnail", "quote card", "promo graphic", "social media image", "post
  for my brand", "reel cover", "pin", "OG image", "post banao", "carousel banao".
  Produces real HTML/CSS rendered to PNG (not advice) with a
  bold, modern, magazine-grade look — never flat, generic, or templated.
license: MIT
metadata:
  author: XniperBuilds
  version: "1.1.0"
---

# Xniper Social Studio — Premium Social Graphics, Brief → PNG

You design social media graphics that look like a senior art director made them,
then render them to **exact-size PNGs** ready to post. You do not stop at advice
or a description — you ship the finished image file.

The bar is simple: **if it could pass for a Behance / Awwwards-grade brand post,
ship it. If it looks like a default AI template, throw it out and redo it.**

**Variety is the product.** Two posts must never look like the same template with
the words swapped. Before building, sample a distinct *aesthetic direction* from
the library (`data/directions.json` via `scripts/ideate.py`) — 24 directions ×
24 palettes × 19 font pairings × layouts × motifs = tens of thousands of looks.
**Never reuse the same direction two posts in a row.**

---

## What this skill is for

USE IT when the task is to create a *static social graphic*:

- Feed posts (square / portrait), carousels (multi-slide), stories & reel covers
- Quote cards, tips/listicles, announcements, launches, promos, sales
- Stat / data cards, testimonials, before→after, "swipe" hooks
- YouTube thumbnails, Pinterest pins, LinkedIn/X link cards

SKIP IT for: video/motion, full websites or app UIs (use `frontend-design` /
`ui-ux-pro-max`), logo/brand-identity systems (use `design`), printing with
bleed/CMYK, or actually posting/scheduling to a platform.

---

## The pipeline (always follow this)

```
1. READ the brief   →  platform · format · topic · brand · vibe · #slides
2. PICK A DIRECTION →  scripts/ideate.py  (sample distinct aesthetics; never repeat the last)
3. PULL the system  →  scripts/search.py  (palette + font pairing + template + hook)
4. BUILD HTML       →  fill a template AND push it to the direction (motifs), or hand-build
5. RENDER PNG       →  scripts/render.py  (exact px, 2x, awaits fonts)
6. QA + iterate     →  open the PNG, check the Pre-Flight list, fix, re-render
```

Tools live beside this file. Resolve paths from the skill directory (the folder
containing this SKILL.md). All three scripts find their own `../data` and
`../templates`, so they work from any CWD.

```bash
SKILL="<path to this skill dir>"
python "$SKILL/scripts/search.py"  "<brief keywords>" --recommend
python "$SKILL/scripts/new_post.py" --template <id> --brand <preset|custom> --content content.json --out out/post.html
python "$SKILL/scripts/render.py"  out/post.html --size 1080x1350 --out out/post.png
```

`render.py` auto-installs the Chromium binary if Playwright is present but the
browser is missing. If Playwright itself is missing, tell the user to run
`pip install playwright` once.

---

## Step 1 — Read the brief

Extract, and only ask if genuinely missing:

- **Platform + format** → maps to exact pixels (see `reference/platforms.md`).
  Default if unspecified: Instagram portrait **1080×1350**.
- **Topic / message** → the single idea this graphic must land.
- **Brand** → a preset in `data/brand-presets.json`, or custom (colors, font,
  logo, handle). If none given, infer a fitting palette from the topic — do not
  default to purple-on-white.
- **Vibe words** → "bold", "minimal", "luxury", "playful", "techy", "editorial".
- **Carousel?** → how many slides; plan a cover + body + CTA arc.

## Step 2 — Pick a direction, then state the Design Read

Sample distinct aesthetic directions and commit to ONE (different from your last):

```bash
python "$SKILL/scripts/ideate.py" "<brief>" -n 6     # 6 distinct directions, fresh each run
python "$SKILL/scripts/ideate.py" "<brief>" --direction riso-print   # lock a look, vary the rest
```

Then one line, out loud, before any HTML:

> *"Reading this as a `<format>` for `<audience>` in the **`<direction>`** direction — `<palette>` palette, `<display font>` / `<body font>`, `<layout>`, with `<motifs>`."*

`data/directions.json` = 24 movements; `reference/directions.md` = how to build each + the **Motif Cookbook** (grain, highlighter, sketch-underline, connector-dots, glass, etc.). Commit fully and execute with precision.

## Step 3 — Pull the design system

```bash
python "$SKILL/scripts/search.py" "fitness coach bold motivational instagram" --recommend
```

Returns a ready system: palette (bg/surface/text/accent/gradient), font pairing,
a recommended template id, and a matching hook. Deep-dive any dimension:

```bash
python "$SKILL/scripts/search.py" "luxury dark gold"   --domain palettes -n 5
python "$SKILL/scripts/search.py" "editorial elegant"  --domain fonts
python "$SKILL/scripts/search.py" "quote announcement" --domain templates
python "$SKILL/scripts/search.py" "tips listicle"      --domain hooks
```

## Step 4 — Build the HTML

Fastest path — fill a template (matches what `search.py --recommend` prints):

```bash
python "$SKILL/scripts/new_post.py" --template quote-bold \
  --palette midnight-neon --font grotesk-mono \
  --content content.json --size 1080x1350 --out out/slide-1.html
```

Style precedence (high→low): **content.json `palette`/`font` > `--palette`/`--font` flags > `--brand` preset > built-in default.** For a saved brand, swap the two flags for one: `--brand xniperbuilds`.

`content.json` carries the copy + chosen tokens:

```json
{
  "eyebrow": "NEW DROP",
  "headline": "Beat 50 levels.\nOne tap.",
  "subhead": "Free to play — no download.",
  "cta": "Play now",
  "handle": "@xniperbuilds",
  "palette": "midnight-neon",
  "font": "grotesk-mono"
}
```

For a non-standard idea, hand-build from `templates/` — keep the canvas at exact
pixels, inline all CSS, load fonts from Google Fonts CDN, and obey
`reference/design-rules.md`. Read `reference/recipes.md` for per-archetype
blueprints (cover, tip-stack, stat, testimonial, before/after, CTA end-card).

## Step 5 — Render to PNG

```bash
python "$SKILL/scripts/render.py" out/slide-1.html --size 1080x1350 --out out/slide-1.png
# whole folder at once:
python "$SKILL/scripts/render.py" out/ --batch --out out/exports/
```

Renders at `deviceScaleFactor: 2` (crisp), hides scrollbars, and waits for fonts
+ images before capture. Filenames may encode size (`name-1080x1350.png`) and
the batch mode reads it automatically.

## Step 6 — QA, then iterate

Open the exported PNG and run the **Pre-Flight Checklist** below. Fix the HTML,
re-render, re-check. Never hand over an unrendered HTML file as the deliverable —
the PNG is the deliverable.

---

## The Premium Standard (non-negotiable)

This is what separates this skill from generic output. Full detail in
`reference/design-rules.md`; the load-bearing rules:

1. **Different every time, committed every time.** Sample a fresh direction
   (`ideate.py`) — never repeat the last. Then commit fully: refined-minimal or
   loud-maximal both win, timid middle-ground loses.
2. **Distinctive type only.** Never Arial / Inter / Roboto / system as the
   display face. Pair a characterful display font with a clean body font
   (`data/fonts.json`). Headlines: tight tracking, heavy weight, big.
3. **Kill the AI tells.** No purple-glow-on-white gradient. No three identical
   cards. No emoji used as icons. No centered-everything. No flat cheap look.
4. **One locked accent.** Neutral base + a single high-impact accent, used
   consistently. Tint shadows to the background hue — never pure black.
5. **Depth & atmosphere.** Layer gradient meshes, grain/noise, soft glows,
   overlapping shapes, large background type. A solid flat fill is a fallback,
   not a design.
6. **Brutal hierarchy.** One focal point. The headline is unmissable. Eye flow
   is obvious in a half-second thumbnail glance.
7. **Real contrast, real legibility.** Text passes WCAG AA (4.5:1). Test it
   readable at 30% size — that's the feed.
8. **Safe zones.** Keep critical content in the central ~80%. Stories and Reels
   have *different* UI overlays on 1080×1920 — check `reference/platforms.md`
   before placing text/CTA.
9. **Copy self-audit.** Re-read every visible string. Cut anything cute-but-
   broken. Headline ≤ ~8 words. One idea per graphic.

> Rejected forever (brand owner's hard rule): plain / flat / "90s" / black-and-
> white / cheap-looking. Every output is premium, modern, vibrant, with depth.

---

## Platform sizes (defaults)

| Platform | Format | Size (px) | Aspect |
|---|---|---|---|
| Instagram | Portrait post / carousel | **1080×1350** | 4:5 |
| Instagram | Square post | 1080×1080 | 1:1 |
| Instagram / TikTok | Story / Reel cover | 1080×1920 | 9:16 |
| Facebook / OG link | Feed / share image | 1200×630 | 1.91:1 |

**Full table** (X, LinkedIn, Pinterest, YouTube, Threads, profile headers) **+ per-platform safe zones → `reference/platforms.md`.** Stories and Reels safe zones differ — check before placing text on 1080×1920.

## Typography scale (at 1080px width — multiply for larger canvases)

| Role | Min size | Weight |
|---|---|---|
| Display headline | 72–140px | 800–900 |
| Headline | 48–72px | 700–800 |
| Subhead | 30–40px | 600 |
| Body | 24–28px | 400–500 |
| Eyebrow / label | 18–22px | 600, uppercase, tracked |
| CTA | 28–34px | 700 |

---

## Carousels

Plan the arc, don't just repeat a template:

- **Slide 1 = pure hook** (a question, bold claim, or callout — see
  `data/hooks.json`). No feature dump on the cover.
- **Middle slides** = one point each, consistent system, varied composition
  (don't stamp the identical layout 6×).
- **Last slide = CTA / follow / save.**
- Lock palette + fonts + margins across all slides; vary only the layout.
- One direction per set; rotate to a NEW direction next post (on a posting cadence, do a full direction overhaul every few posts so the feed never goes samey).

Generate each slide as its own HTML, render the folder with `--batch`.

---

## Resources in this skill

| Path | What |
|---|---|
| `reference/platforms.md` | Every size + safe zones, per platform/format |
| `reference/design-rules.md` | The full premium / anti-slop ruleset |
| `reference/directions.md` | 24 aesthetic directions + Motif Cookbook (how to build each) |
| `reference/recipes.md` | Layout blueprints per post archetype |
| `reference/copywriting.md` | Hook, headline & CTA formulas |
| `data/directions.json` | 24 aesthetic directions — the variety engine |
| `data/palettes.json` | 24 curated premium palettes (mood/industry tagged) |
| `data/fonts.json` | 19 Google-Font display+body pairings |
| `data/motifs.json` | Decorative motif index (snippets in directions.md) |
| `data/templates.json` | Template registry (id → file, format, use) |
| `data/hooks.json` | Viral hook library by category |
| `data/brand-presets.json` | Ready brand tokens + a custom slot |
| `scripts/ideate.py` | Sample distinct aesthetic directions (the variety engine) |
| `scripts/search.py` | Recommend / search the design system |
| `scripts/new_post.py` | Fill a template with content + brand → HTML |
| `scripts/render.py` | HTML → exact-size PNG (Playwright) |

---

## Pre-Flight Checklist (run on every exported PNG)

- [ ] Renders at the exact target pixels, nothing cut off
- [ ] One clear focal point; headline readable at thumbnail (30%) size
- [ ] Display font is distinctive (not Arial/Inter/Roboto/system)
- [ ] The web display font actually rendered — not a system fallback
- [ ] Single locked accent; no stray off-palette color
- [ ] Has depth — gradient/grain/glow/shape/large type, not a flat fill
- [ ] No AI tells (purple-on-white glow, 3 identical cards, emoji-as-icon)
- [ ] Text contrast ≥ 4.5:1 everywhere; CTA legible
- [ ] Critical content inside safe zones (story UI clear)
- [ ] Copy audited: ≤ ~8-word headline, no broken/cute-wrong strings
- [ ] Carousel: consistent system, varied layouts, hook→points→CTA arc
- [ ] Brand handle/logo placed and on-brand
