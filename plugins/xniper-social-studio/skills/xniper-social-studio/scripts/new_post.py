#!/usr/bin/env python3
"""
Xniper Social Studio — fill a template with content + brand tokens → HTML.

Examples
--------
  python new_post.py --template quote-bold --brand xniperbuilds \
      --content content.json --size 1080x1350 --out out/slide-1.html

  python new_post.py --template announcement --palette midnight-neon \
      --font anton-inter --content '{"headline":"New game\nout now","cta":"Play"}' \
      --size 1080x1080 --out out/promo.html

Resolution order (high → low): content.json  >  --palette/--font CLI  >  --brand preset  >  built-in default.
HEADLINE/SUBHEAD may contain real newlines (→ <br>) and simple inline HTML like <em>word</em>.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"

# A neutral, broadly-flattering default that is NOT the banned purple-on-white
# AI tell. Override per brief/brand any time.
DEFAULT_PALETTE = "ocean-deep"
DEFAULT_FONT = "archivo-figtree"

# Inline tags allowed inside copy (everything else is escaped for safety).
ALLOWED_TAGS = ("<em>", "</em>", "<strong>", "</strong>", "<br>")


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def find(items, key, idv, kind):
    for it in items:
        if it.get(key) == idv:
            return it
    ids = ", ".join(i.get(key, "?") for i in items)
    die(f"unknown {kind} '{idv}'. available: {ids}")


def main():
    ap = argparse.ArgumentParser(description="Fill a template → HTML")
    ap.add_argument("--template", required=True, help="template id (see data/templates.json) or path to .html")
    ap.add_argument("--content", help="path to content.json OR an inline JSON string")
    ap.add_argument("--brand", help="brand preset id (data/brand-presets.json)")
    ap.add_argument("--palette", help="palette id (overrides brand)")
    ap.add_argument("--font", help="font pairing id (overrides brand)")
    ap.add_argument("--size", default="1080x1350", help="WxH, e.g. 1080x1350")
    ap.add_argument("--out", required=True, help="output .html path")
    args = ap.parse_args()

    # --- size
    m = re.fullmatch(r"(\d+)x(\d+)", args.size.lower())
    if not m:
        die(f"bad --size '{args.size}', expected WxH like 1080x1350")
    W, H = m.group(1), m.group(2)

    # --- content (test JSON-shape first so an inline blob never gets treated as a path)
    content = {}
    if args.content:
        if args.content.lstrip().startswith("{"):
            raw, src = args.content, "inline JSON"
        elif Path(args.content).exists():
            raw, src = Path(args.content).read_text(encoding="utf-8"), args.content
        else:
            die(f"--content '{args.content}' is neither a file nor JSON")
        try:
            content = json.loads(raw)
        except json.JSONDecodeError as e:
            die(f"invalid JSON in {src}: {e}")

    # --- brand preset
    brand = {}
    if args.brand:
        presets = load("brand-presets.json")["presets"]
        if args.brand not in presets:
            die(f"unknown brand '{args.brand}'. available: {', '.join(presets)}")
        brand = presets[args.brand]

    # --- resolve palette + font (content > cli > brand > default)
    palette_id = content.get("palette") or args.palette or brand.get("palette") or DEFAULT_PALETTE
    font_id = content.get("font") or args.font or brand.get("font") or DEFAULT_FONT
    palette = find(load("palettes.json")["palettes"], "id", palette_id, "palette")
    font = find(load("fonts.json")["fonts"], "id", font_id, "font")

    # --- template
    if args.template.lower().endswith(".html"):
        tmpl_path = Path(args.template)
    else:
        reg = find(load("templates.json")["templates"], "id", args.template, "template")
        tmpl_path = TEMPLATES / reg["file"]
    if not tmpl_path.exists():
        die(f"template file not found: {tmpl_path}")
    tmpl_html = tmpl_path.read_text(encoding="utf-8")

    def text(key, default=""):
        v = content.get(key, default)
        if v is None:
            v = ""
        # Escape everything (fixes bare "&", stray "<", and injection), then
        # restore the sanctioned inline tags and convert newlines to <br>.
        s = html.escape(str(v), quote=False)
        for tag in ALLOWED_TAGS:
            s = s.replace(html.escape(tag, quote=False), tag)
        return s.replace("\n", "<br>")

    handle = content.get("handle") or brand.get("handle") or "@yourbrand"

    repl = {
        "W": W, "H": H,
        "FONTS_LINK": font["link"], "DISPLAY": font["display"], "BODY": font["body"],
        "BG": palette["bg"], "SURFACE": palette["surface"], "TEXT": palette["text"],
        "MUTED": palette["muted"], "ACCENT": palette["accent"],
        "ACCENT2": palette.get("accent2", palette["accent"]), "GRADIENT": palette["gradient"],
        "EYEBROW": text("eyebrow"), "HEADLINE": text("headline", "Your headline here"),
        "SUBHEAD": text("subhead"), "CTA": text("cta"), "HANDLE": str(handle),
        "INDEX": text("index"), "BIGWORD": text("bigword"),
    }

    def sub(match):
        key = match.group(1)
        return repl.get(key, match.group(0))

    out_html = re.sub(r"\{\{([A-Z0-9_]+)\}\}", sub, tmpl_html)

    # warn on any leftover token
    leftover = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", out_html))
    if leftover:
        print(f"WARN: unfilled tokens left in template: {', '.join(sorted(leftover))}", file=sys.stderr)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(out_html, encoding="utf-8")

    print(f"OK  {out}")
    print(f"    {W}x{H} | palette={palette_id} | font={font_id} | template={args.template}")
    print(f"    render: python scripts/render.py \"{out}\" --size {W}x{H} --out \"{out.with_suffix('.png')}\"")


if __name__ == "__main__":
    main()
