# Changelog

All notable changes to Xniper Social Studio.

## [1.9.0] — 2026-06-14
### Added — template batch 5 (47 → 57): the remaining direction-baked aesthetics
- `riso-print` (halftone + 2-ink overprint), `claymorphism` (puffy clay cards), `depth-3d` (extruded layered type), `isometric` (iso grid + 2.5D cubes), `paper-craft` (layered cut-paper), `organic-natural` (soft blob + serif), `art-deco` (gold frame + sunburst), `collage-cutout` (torn paper + tape + ransom type), `sketch-notebook` (dot-paper + marker + hand-drawn circle/arrow), `grain-gradient` (duotone gradient + heavy grain). All rendered/verified — every one a distinct visual world.

## [1.8.0] — 2026-06-14
### Added — template batch 4 (37 → 47): direction-BAKED templates (each a whole aesthetic)
- `neon-cyber-card` (glow + scanlines + HUD), `glass-aurora-card` (frosted glass over mesh), `memphis-pop` (confetti + squiggle + sticker), `vaporwave-cover` (perspective grid + sun glow), `swiss-grid` (hairline grid + big index), `bauhaus-block` (primary shapes + thick borders), `y2k-chrome` (chrome metallic type + sparkles), `magazine-editorial` (drop cap + columns + pull quote), `mono-terminal` (editor window + caret), `dark-luxe-card` (gold + centered serif statement).
- Unlike earlier batches (structure-variety), these bake a full visual DIRECTION as the template's default look — so the library now ships many genuinely distinct aesthetics. All rendered/verified.

## [1.7.0] — 2026-06-14
### Fixed — the big one: ASK FIRST + no template-look
- **SKILL.md now mandates asking the user first** (AskUserQuestion: brand · vibe/theme · platform/format · message · reference) before generating — added as one of "Two laws that override everything", rewritten Step 1, and a Pre-Flight gate. Fixes the complaint that it generated without asking.
- **Hard anti-template law:** never default-fill a template; every output must commit to a sampled direction + chosen palette/font + ≥2 motifs + content-adapted layout. Fixes the "AI vibe / looks like a template" output.
### Added — template batch 3 (27 → 37), each a distinct structure
- `quote-serif`, `stat-trio`, `diagram-flow`, `listicle-cards`, `hook-split`, `definition-card`, `stat-brutal`, `announcement-ticket`, `mistake-warning`, `value-prop-hero` — alternate looks/structures for high-use purposes (serif quote, three-stat row, horizontal flow, card stack, split cover, dictionary entry, neo-brutal stat, perforated ticket, warning callout, benefit hero). All rendered/verified.
- **+24 font pairings (61 total):** Climate Crisis, Rubik Mono One, Darker Grotesque, Gasoek One, Abril Fatface, Yeseva One, League Gothic, Chakra Petch, Orbitron, Righteous, Pacifico, Red Hat, Pixelify Sans, VT323, Special Elite, Lora, Epilogue, Host Grotesk, Schibsted Grotesk, Albert Sans, Khand, Archivo, Gloria Hallelujah, Reddit Sans.

## [1.6.0] — 2026-06-14
### Added — template batch 2 (17 → 27 templates), each a distinct structure
- `leaderboard` (ranked podium bars), `before-after` (50/50 split + VS), `product-showcase` (spotlight-staged hero + spec chips), `lead-magnet` (checklist + taped PDF card), `promo-offer` (neo-brutal big-number block + starburst), `cheatsheet` (dense 2-col keycaps + ghost glyph), `index-contents` (TOC with dotted leaders + spiral edge), `recipe-card` (ingredients + numbered method), `faq-qa` (Q/A badge cards), `tool-roundup` (logo + name + one-liner rows).
- Every template has its OWN layout skeleton (not a recoloured copy); all rendered/verified.

## [1.5.0] — 2026-06-14
### Added — template batch 1 (10 → 17 templates)
- 7 new purpose-templates: `listicle-numbered`, `step-flow`, `checklist-rows`, `testimonial-glass`, `profile-intro`, `timeline-roadmap`, `myth-bust` — each token-filled chrome + editable sample body, using the studied content atoms (numbered rows, connector flow, check rows, glass quote, avatar intro, node spine, myth-vs-truth). All rendered/verified.

## [1.4.0] — 2026-06-14
### Added — learnings from studying all ~180 reference carousels (25 creators)
- **+5 aesthetic directions (37 total):** halftone-photo, authentic-lifestyle (real photos + UI-card overlays), editorial-accent (serif + one accent clause + brush underline + screenshots), kraft-bold (kraft paper + taped lead-magnet cards), tweet-clean (X-header chrome + mono code-pills + flow diagrams + progress bar).
- **+3 purpose categories (27 total):** index-contents, cheatsheet (keycaps/shortcuts), lead-magnet (comment-for-PDF).
- **+20 motifs** with cookbook CSS for the high-value ones: callout-pin (annotate screenshots), keycap, code-pill, prompt-paste-box, ui-card-overlay, tweet-header, progress-bar, device-mockup frame, taped-card, halftone, number-badge, meta-pill/meta-line, brush-underline, dashed-caption, spiral-binding, dotted-leader, app-icon-sticker, wordmark-bleed, ghost-number, icon-card-flow, photo-collage.

## [1.3.0] — 2026-06-14
### Added — purpose taxonomy + reference-grounded systems (master-plan phase 1)
- **`data/categories.json` — 24 purpose categories** (hook-cover, listicle, feature-grid, step-by-step, comparison-vs, stat-number, benchmark-leaderboard, before-after, diagram-explainer, quote-statement, checklist, testimonial, announcement, promo-offer, value-prop, product-showcase, profile-intro, myth-bust, definition, timeline, recipe-card, faq-qa, tool-roundup, cta-outro). A template = **category × direction × role**.
- **`reference/carousel-systems.md`** — distilled from studying real top-creator IG carousels: persistent chrome, the cover→content→recap→cta role arc, the icon+keyword content atom, palette discipline, proof-via-real-artifacts, depth devices, semantic icons, engagement mechanics, and the purpose×aesthetic matrix.
- `ideate.py`: `--list-categories` and `--category <id>` (ideas that fit a purpose).
- **+18 font pairings (37 total):** Boldonse, Gloock, Bodoni Moda, Alfa Slab One, Bungee, Monoton, Caprasimo, Marcellus, Cormorant Garamond, Newsreader, Geist, Funnel Display, Fredoka, Baloo 2, Shantell Sans, Tektur, Krona One, Caveat.
- **2 new templates (10 total):** `comparison-vs` (dual glass panels + VS + payoff bar) and `feature-grid` (2×3 icon cards).
> Phase 1 of the master plan (100+ templates / 20+ categories / 100+ fonts). Next phases mass-produce templates per category and continue fonts toward 100.

## [1.2.0] — 2026-06-14
### Added
- **+8 aesthetic directions (32 total):** 3D-depth, isometric, claymorphism, grain-gradient, liquid-chrome, paper-craft, data-viz, sketch-notebook.
- **`ideate.py --carousel N`** — plans a whole carousel: locks ONE direction + palette + font, assigns each slide a role (hook cover → points → CTA end-card), varies the layout, and prints per-slide content skeletons + build/batch-render commands.
- **2 new templates (8 total):** `carousel-cover` (pure hook + counter + swipe cue) and `cta-endcard` (one big follow/save CTA).
- +6 motifs (extrude-3d, iso-tile, clay, noise-gradient, papercut-shadow, duotone) with copy-paste CSS in the Motif Cookbook.

## [1.1.0] — 2026-06-14
### Added — the Variety Engine (every post a different look, never the same AI vibe)
- `data/directions.json` — **24 distinct aesthetic directions** (editorial-vintage, bold-grotesk-grid, blueprint-diagram, sticker-doodle, poster-bold, swiss, neo-brutalism, glass-aurora, dark-luxe, neon-cyber, riso-print, memphis, y2k-chrome, vaporwave, magazine, kinetic-type, gradient-mesh, organic, art-deco, collage, mono-terminal, minimal-photo, bauhaus, corporate-clean).
- `scripts/ideate.py` — combinatorial idea generator: sample N distinct directions for a brief (direction × palette × font × layout × motifs = tens of thousands of looks), fresh each run or `--seed` for reproducibility.
- `reference/directions.md` — per-direction build notes + a **Motif Cookbook** of copy-paste CSS/SVG (grain, highlighter, sketch-underline, doodle-arrow, connector-dots, glass, halftone, scanlines, blob, chrome text, drop-cap, and more).
- `data/motifs.json` — decorative motif index.
- 2 new templates: `editorial-vintage` (cream paper + serif + sketch/doodle) and `blueprint-diagram` (grid paper + highlighter + connector dots). Now 6 templates.
- +10 palettes (24 total) and +7 font pairings (19 total) to widen the combinatorial space.
- `new_post.py` now also keeps inline `<mark>` (highlighter motif).
### Changed
- `SKILL.md` reframed around variety: pick a direction first, never repeat the last, rotate across a posting cadence; updated pipeline, resources, and Premium Standard.

## [1.0.1] — 2026-06-14
### Fixed
- `render.py`: deterministic Chromium auto-install (no longer relies on matching Playwright's error wording); `document.fonts.ready` is now properly **awaited** so exports never capture a system-fallback font; batch mode continues past a single bad file and exits non-zero on any failure; bad `--size` now warns instead of being silently ignored.
- `new_post.py`: copy is now HTML-escaped (fixes bare `&`, stray `<`, and injection) while still allowing `<em>`/`<strong>`/`<br>`; inline-JSON vs file detection reordered and JSON parse errors fail gracefully; fixed a module/variable name clash.
- `search.py`: tag-weighted, de-duplicated scoring; guards empty data; flags weak (no-match) recommendations instead of silently returning the first item; hook lookups fall back safely.
- Default palette changed from `electric-violet` to `ocean-deep` (avoids defaulting to the purple family the skill itself flags).
### Changed
- `SKILL.md`: consistent `$SKILL/scripts/...` invocation everywhere; clarified style precedence; trimmed the duplicated platform table; added font-rendered QA check; more trigger phrases (incl. Roman-Urdu).
- `reference/platforms.md`: split Stories vs Reels safe zones (they differ), added per-platform file-size caps, a profiles/headers table, a verified-on date, and corrected the carousel-bottom guidance.

## [1.0.0] — 2026-06-14
### Added
- Initial release: brief → premium social graphic → exact-size PNG via HTML/CSS + Playwright (deviceScaleFactor 2).
- 4 templates (quote-bold, announcement, tip-card, stat-card), 15 palettes, 12 font pairings, hook library, brand presets.
- Scripts: `search.py` (recommend), `new_post.py` (fill), `render.py` (PNG export).
- Reference docs (platforms, design rules, recipes, copywriting) + plugin/marketplace packaging.

> **Version source of truth:** `plugins/xniper-social-studio/.claude-plugin/plugin.json`. Bump it together with the mirrors in `.claude-plugin/marketplace.json` and `SKILL.md` (`metadata.version`) on each release.
