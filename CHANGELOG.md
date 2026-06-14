# Changelog

All notable changes to Xniper Social Studio.

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
