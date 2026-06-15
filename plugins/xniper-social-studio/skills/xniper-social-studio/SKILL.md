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
  version: "1.10.0"
---

# Xniper Social Studio — Premium Social Graphics, Brief → PNG

You design social media graphics that look like a senior art director made them,
then render them to **exact-size PNGs** ready to post. You do not stop at advice
or a description — you ship the finished image file.

The bar is simple: **if it could pass for a Behance / Awwwards-grade brand post,
ship it. If it looks like a default AI template, throw it out and redo it.**

### Two laws that override everything
1. **ASK BEFORE YOU DESIGN.** Never generate from assumptions. First ask the user —
   **brand, vibe/theme, platform/format, the message, and any reference they like** —
   with **AskUserQuestion**. A post made without asking is a FAIL even if it looks ok.
   (The #1 complaint is "it didn't ask me anything." See Step 1.)
2. **NEVER SHIP A TEMPLATE-LOOK.** Do NOT just fill a template with the default
   palette/font — that IS the "AI vibe" to avoid. Every output commits to a sampled
   aesthetic *direction* + a chosen palette + font + **≥2 motifs**, with the layout
   adapted to the actual content. If it could pass for a stock template, redo it.

**Variety is the product.** Two posts must never look like the same template with
the words swapped. Before building, sample a distinct *aesthetic direction* from
the library (`data/directions.json` via `scripts/ideate.py`) — 37 directions ×
27 categories × 24 palettes × 90 font pairings × layouts × motifs = millions of looks.
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
1. ASK FIRST        →  AskUserQuestion: brand · vibe/theme · platform/format · message · reference (NEVER skip)
2. PICK A DIRECTION →  scripts/ideate.py  (sample distinct aesthetics; never repeat the last; never default-fill)
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

## Step 1 — ASK FIRST (mandatory — do not skip)

Before generating ANYTHING, ask the user with **AskUserQuestion**. The #1 reason
posts look like generic AI templates is the model guessing instead of asking.
Even if part of this is in the brief, confirm the rest:

- **Platform & format** — IG post / story / carousel / thumbnail / pin… (→ exact px)
- **Brand** — their colours / font / logo / @handle; OR a preset
  (`data/brand-presets.json`); OR "none — propose one for me". Never invent a brand silently.
- **Vibe / theme** — the aesthetic. Offer concrete named options from `ideate.py`
  (e.g. bold-grotesk · editorial-vintage · dark-luxe · neo-brutalism · glass-aurora ·
  kraft-bold · neon-cyber · minimal-photo · y2k-chrome) and let them pick or say "you choose".
- **The message** — headline / key points / CTA.
- **Reference (optional)** — anything whose look they want matched.
- **Carousel?** — how many slides.

Example (adapt to the request):
- Q "What's this for?" → IG carousel · IG post · story/reel cover · thumbnail · other
- Q "Brand look?" → "Use my brand (give colours/font)" · a preset · "Pick something premium for me"
- Q "Which vibe?" → 3–4 named directions + "Surprise me"

Only skip asking if the user EXPLICITLY says "just make it / you decide everything".
Then state your Design Read (Step 2) so they can still course-correct, and proceed.

## Step 2 — Pick a direction, then state the Design Read

Sample distinct aesthetic directions and commit to ONE (different from your last):

```bash
python "$SKILL/scripts/ideate.py" "<brief>" -n 6     # 6 distinct directions, fresh each run
python "$SKILL/scripts/ideate.py" "<brief>" --direction riso-print   # lock a look, vary the rest
python "$SKILL/scripts/ideate.py" --list-categories                  # 27 purpose categories
python "$SKILL/scripts/ideate.py" "<brief>" --category comparison-vs # ideas that fit a purpose
```

Pick by **purpose** as well as look: a template = **category × direction × role (cover/content/recap/cta)**. `data/categories.json` = 27 purpose categories; `reference/carousel-systems.md` = what top creators actually do (persistent chrome, the role arc, icon+keyword atoms, proof devices, engagement mechanics).

Then one line, out loud, before any HTML:

> *"Reading this as a `<format>` for `<audience>` in the **`<direction>`** direction — `<palette>` palette, `<display font>` / `<body font>`, `<layout>`, with `<motifs>`."*

`data/directions.json` = 37 movements; `reference/directions.md` = how to build each + the **Motif Cookbook** (grain, highlighter, sketch-underline, connector-dots, glass, clay, 3D, etc.). Commit fully and execute with precision.

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

**Plan the whole set in one command** — locks ONE direction + palette + font, assigns each slide a role (hook → points → CTA), varies the layout:

```bash
python "$SKILL/scripts/ideate.py" "<brief>" --carousel 6
```

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
| `reference/directions.md` | 37 aesthetic directions + Motif Cookbook (how to build each) |
| `reference/carousel-systems.md` | What top creators do: chrome, role arc, content atoms, proof, engagement |
| `reference/recipes.md` | Layout blueprints per post archetype |
| `reference/copywriting.md` | Hook, headline & CTA formulas |
| `data/directions.json` | 37 aesthetic directions — the variety engine |
| `data/categories.json` | 27 purpose categories (template = category × direction × role) |
| `data/palettes.json` | 24 curated premium palettes (mood/industry tagged) |
| `data/fonts.json` | 90 Google-Font display+body pairings |
| `data/motifs.json` | Decorative motif index (snippets in directions.md) |
| `data/templates.json` | Template registry (id → file, format, use) |
| `data/hooks.json` | Viral hook library by category |
| `data/brand-presets.json` | Ready brand tokens + a custom slot |
| `scripts/ideate.py` | Sample directions / categories; plan carousels (`--carousel`, `--category`, `--list-categories`) |
| `scripts/search.py` | Recommend / search the design system |
| `scripts/new_post.py` | Fill a template with content + brand → HTML |
| `scripts/render.py` | HTML → exact-size PNG (Playwright) |

---

## Pre-Flight Checklist (run on every exported PNG)

- [ ] You ASKED the user first (brand · vibe · format · message) — not guessed
- [ ] Does NOT look like a filled template: committed to a sampled direction + a chosen palette/font + ≥2 motifs + a layout adapted to the content
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
