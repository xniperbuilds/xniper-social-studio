# Aesthetic Directions + Motif Cookbook

The whole point of this skill is **variety**. Two posts should never look like the
same template with the words swapped. `data/directions.json` holds 24 distinct
design *movements*; this file is the build manual for them plus a copy-paste
**Motif Cookbook** for the hand-made touches that kill the flat-AI look.

## How to get endless ideas

```bash
python "$SKILL/scripts/ideate.py" "your brief" -n 6      # 6 distinct directions, fresh each run
python "$SKILL/scripts/ideate.py" "your brief" --seed 7  # reproducible set
python "$SKILL/scripts/ideate.py" "x" --direction riso-print   # lock the look, vary the rest
```

Each idea = a direction × palette × font × layout × motifs. 24 × 24 × 19 × layouts
× motifs ≫ tens of thousands of combinations. **Rule: never reuse the same
direction two posts in a row, and vary it across every slide-set.**

## Build flow per post

1. `ideate.py` (or just pick a direction). Commit to ONE.
2. If a template shares the direction's tags, fill it (`new_post.py`) **then push it
   toward the direction** with motifs below. Otherwise hand-build the HTML.
3. Always layer at least one depth motif (grain + one more). Render with `render.py`.

---

## Direction build notes (the signature move for each)

- **editorial-vintage** — cream paper + `grain`; serif headline, one word in accent; `sketch-underline` + a `doodle-arrow`; a `pill-badge` "SLIDE 2".
- **bold-grotesk-grid** — light grainy gradient; ONE huge centered grotesk line; rounded device/screenshot cards; `pill-badge` + `swipe-affordance`.
- **blueprint-diagram** — `grid-paper` bg; bold headline with a `highlighter` word; labelled boxes joined by `connector-dots`; one `handwritten-accent` line; mono labels.
- **sticker-doodle** — faint grid; phone mockup + value cards; `highlighter`, `sticker-star`, `tape`; a small code/quote block + a "WHY" note.
- **poster-bold** — dark field + one `gradient-orb`; condensed display at extreme scale pinned to edges; `grain`.
- **swiss-international** — flat off-white/black; strict columns; `thin-rule` + index number; one red accent; zero decoration.
- **neo-brutalism** — one bright flat colour; `thick-border` + `hard-shadow` on chunky blocks; slight rotation; `sticker-star`.
- **glass-aurora** — `gradient-mesh` bg + `glass-panel` holding the message + `glow`; fine inner-border highlight.
- **dark-luxe** — near-black + faint top `glow` + `grain`; high-contrast serif statement; tracked caps eyebrow; vast space.
- **neon-cyber** — black + neon `glow` + `scanlines`; glowing text-shadow headline; HUD corner labels.
- **riso-print** — paper `grain` + `halftone` + `overprint` (two inks offset/multiply); chunky type slightly off-register.
- **memphis-pop** — pastel field + `confetti` + `squiggle` + `sticker-star`; bouncy asymmetry.
- **y2k-chrome** — `chrome-gradient` bubble type + `sparkle` + `blob`; cool metallic field.
- **vaporwave** — magenta→cyan gradient + `perspective-grid` horizon + `glow`; centered statement above the grid.
- **magazine-editorial** — columns + `drop-cap` + `pull-quote` + `thin-rule`; serif head, sans body, hero photo.
- **kinetic-type** — the type IS the art: oversized, overlapping, cropped at edges; `big-bg-number`; minimal else.
- **gradient-mesh-soft** — big soft `gradient-mesh` + barely-there `grain`; one short line of type, lots of air.
- **organic-natural** — earthy field + one big `blob` + `grain`; soft serif; calm left-aligned message.
- **art-deco** — jewel/black + `gold-line` frames + `sunburst`; symmetric, centered, elegant caps.
- **collage-cutout** — layered `torn-paper` + `tape` + `halftone` + `sticker-star`; mixed type sizes; controlled chaos.
- **mono-terminal** — editor charcoal/paper + `dot-grid` + `caret`; monospace throughout; `// comment` labels.
- **minimal-photo** — one hero photo + quiet overlay + tiny serif caption + `thin-rule`; immense calm.
- **bauhaus-block** — off-white/primary + `geo-shapes` + `thick-border`; type locked into a geometric grid.
- **corporate-clean** — light surface + one strong accent + `pill-badge`; sharp spacing earns it. Never default purple-on-white.

---

## Motif Cookbook (copy-paste)

All assume the palette CSS vars `--bg --surface --text --muted --accent --accent2` exist.

**Grain (use almost always):**
```css
.grain{position:absolute;inset:0;z-index:1;opacity:.06;mix-blend-mode:overlay;pointer-events:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
```

**Aurora mesh / glow / orb:**
```css
.mesh{background:
  radial-gradient(60% 50% at 15% 10%, var(--accent), transparent 55%),
  radial-gradient(60% 50% at 90% 90%, var(--accent2), transparent 55%), var(--bg)}
.glow{position:absolute;width:60vw;height:60vw;border-radius:50%;filter:blur(8px);opacity:.3;
  background:radial-gradient(circle,var(--accent),transparent 62%)}
.orb{position:absolute;width:70vw;height:70vw;border-radius:50%;
  background:radial-gradient(circle at 38% 35%, #fff6, var(--accent) 38%, var(--accent2) 75%, transparent 78%);filter:blur(.5px)}
```

**Grid paper / dot grid (blueprint, notebook):**
```css
.gridpaper{background:
  linear-gradient(var(--text) 1px,transparent 1px) 0 0/64px 64px,
  linear-gradient(90deg,var(--text) 1px,transparent 1px) 0 0/64px 64px, var(--bg);opacity:1}
.gridpaper::after{content:"";position:absolute;inset:0;background:var(--bg);opacity:.94} /* fade the lines */
.dotgrid{background:radial-gradient(var(--muted) 1.4px, transparent 1.4px) 0 0/34px 34px, var(--bg);opacity:.5}
```

**Highlighter (wrap a word in `<mark>` in your copy — new_post.py keeps `<mark>`):**
```css
mark{background:linear-gradient(180deg,transparent 8%, color-mix(in srgb,var(--accent) 55%,transparent) 8% 88%, transparent 88%);
  color:inherit;padding:0 .08em;transform:rotate(-1.2deg);display:inline-block}
```

**Sketch underline (SVG, hand-drawn):**
```html
<svg class="sketch" viewBox="0 0 300 18" preserveAspectRatio="none" style="width:5em;height:.5em">
  <path d="M2 12 C 80 4, 170 18, 298 7" fill="none" stroke="var(--accent)" stroke-width="4" stroke-linecap="round"/>
</svg>
```

**Doodle arrow (SVG):**
```html
<svg viewBox="0 0 120 90" style="width:8vw" fill="none" stroke="var(--accent)" stroke-width="4" stroke-linecap="round">
  <path d="M10 12 C 40 70, 80 70, 104 40"/><path d="M104 40 l-22 6 M104 40 l-6 -22"/>
</svg>
```

**Connector dots + line (diagrams / pins):**
```css
.pin{position:relative}.pin::before{content:"";position:absolute;width:14px;height:14px;border-radius:50%;background:var(--accent)}
.connector{height:3px;background:var(--accent);border-radius:3px}
.connector::after{content:"";position:absolute;width:14px;height:14px;border-radius:50%;background:var(--accent);right:-2px;top:-6px}
```

**Sparkle / starburst (SVG):**
```html
<svg viewBox="0 0 24 24" style="width:3vw" fill="var(--accent)"><path d="M12 0 C13 8,16 11,24 12 C16 13,13 16,12 24 C11 16,8 13,0 12 C8 11,11 8,12 0Z"/></svg>
```

**Hard offset shadow + thick border (neo-brutalism):**
```css
.brut{border:3px solid var(--text);box-shadow:8px 8px 0 var(--text);background:var(--surface);border-radius:14px}
```

**Glass panel (frosted):**
```css
.glass{background:color-mix(in srgb,var(--surface) 55%,transparent);backdrop-filter:blur(22px) saturate(1.3);
  border:1px solid rgba(255,255,255,.18);box-shadow:inset 0 1px 0 rgba(255,255,255,.25),0 2vw 5vw rgba(0,0,0,.25);border-radius:24px}
```

**Halftone (riso/print):**
```css
.halftone{background:radial-gradient(var(--accent) 28%, transparent 30%) 0 0/12px 12px;opacity:.5;mix-blend-mode:multiply}
```

**Scanlines (cyber):**
```css
.scan{background:repeating-linear-gradient(0deg, rgba(255,255,255,.05) 0 1px, transparent 1px 3px);mix-blend-mode:overlay}
```

**Organic blob:**
```css
.blob{border-radius:42% 58% 63% 37% / 45% 38% 62% 55%;background:radial-gradient(circle at 35% 35%,var(--accent),var(--accent2));filter:blur(.5px)}
```

**Chrome text (Y2K):**
```css
.chrome{background:linear-gradient(180deg,#fff,#cfe0ff 40%,#7f9bd6 55%,#fff 75%,#9fb4dd);-webkit-background-clip:text;background-clip:text;color:transparent}
```

**Tape strip (collage):**
```css
.tape{position:absolute;width:120px;height:34px;background:color-mix(in srgb,var(--accent) 35%,transparent);transform:rotate(-6deg);box-shadow:0 2px 6px rgba(0,0,0,.15)}
```

**Drop cap (magazine):**
```css
.dropcap::first-letter{float:left;font-family:var(--display, serif);font-size:5.5em;line-height:.8;padding:.05em .12em 0 0;color:var(--accent)}
```

**Oversized background mark (depth):**
```css
.bgmark{position:absolute;z-index:0;font-weight:900;font-size:62vw;line-height:.7;color:var(--text);opacity:.06;pointer-events:none}
```

**Handwritten accent line** — load a script font in the head, use for ONE aside only:
```html
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&display=swap" rel="stylesheet">
<p style="font-family:'Caveat',cursive;color:var(--accent);font-size:3.4vw">and the part nobody tells you →</p>
```

> Put the grain/glow/mesh layers behind content (`z-index` below the text), keep
> text contrast ≥ 4.5:1, and respect the safe zones in `platforms.md`.
