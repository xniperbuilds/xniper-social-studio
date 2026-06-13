#!/usr/bin/env python3
"""
Xniper Social Studio — design-system search & recommender.

Examples
--------
  python search.py "fitness coach bold motivational" --recommend
  python search.py "luxury dark gold"  --domain palettes -n 5
  python search.py "editorial elegant" --domain fonts
  python search.py "tips listicle"     --domain hooks
  python search.py "announcement promo" --domain templates

Returns a ready design system (palette + font pairing + template + hook) plus the
exact new_post.py / render.py commands to build it. No external dependencies.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DATA = Path(__file__).resolve().parent.parent / "data"


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def tokens(text):
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t]


def score(item_terms, query_terms):
    """+2 for each query token that hits a tag, +1 for a name/use substring hit."""
    s = 0
    joined = " ".join(item_terms)
    for q in query_terms:
        if q in item_terms:
            s += 2
        elif q in joined:
            s += 1
    return s


def rank(items, terms_fn, query_terms):
    scored = [(score(terms_fn(it), query_terms), it) for it in items]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


# --- term extractors per domain --------------------------------------------
def palette_terms(p):
    return tokens(" ".join(p.get("tags", [])) + " " + p.get("name", "") + " " + p.get("id", ""))


def font_terms(f):
    return tokens(" ".join(f.get("tags", [])) + " " + f.get("name", "") + " " + f.get("id", ""))


def tmpl_terms(t):
    return tokens(" ".join(t.get("tags", [])) + " " + t.get("name", "") + " " + t.get("use", "") + " " + t.get("id", ""))


HOOK_KEYS = {
    "question": ["question", "ask", "curious"],
    "bold_claim": ["bold", "claim", "value", "benefit"],
    "listicle": ["tip", "tips", "list", "listicle", "steps", "howto", "guide", "ways", "mistakes"],
    "callout": ["callout", "audience", "founder", "beginner", "for"],
    "curiosity": ["curiosity", "secret", "reveal", "behind"],
    "contrarian": ["contrarian", "unpopular", "stop", "myth"],
    "transformation": ["before", "after", "transformation", "result", "growth", "journey"],
    "mistake": ["mistake", "wrong", "fail", "avoid", "error"],
    "cta": ["cta", "follow", "save", "launch", "promo", "sale", "announcement", "drop", "free"],
}


def pick_hook_category(query_terms):
    best, best_n = "question", 0
    for cat, kws in HOOK_KEYS.items():
        n = sum(1 for q in query_terms if q in kws)
        if n > best_n:
            best, best_n = cat, n
    return best


def show_list(title, ranked, fmt, n):
    print(f"\n== {title} ==")
    for s, it in ranked[:n]:
        if s <= 0 and ranked[0][0] > 0:
            break
        print(fmt(it, s))


def main():
    ap = argparse.ArgumentParser(description="Xniper Social Studio design search")
    ap.add_argument("query", help="brief keywords, e.g. 'bold gaming neon'")
    ap.add_argument("--recommend", action="store_true", help="return a full design system")
    ap.add_argument("--domain", choices=["palettes", "fonts", "templates", "hooks"])
    ap.add_argument("-n", type=int, default=6, help="max results")
    args = ap.parse_args()

    q = tokens(args.query)
    palettes = load("palettes.json")["palettes"]
    fonts = load("fonts.json")["fonts"]
    templates = load("templates.json")["templates"]
    hooks = load("hooks.json")["hooks"]

    if args.domain == "palettes":
        show_list("PALETTES", rank(palettes, palette_terms, q),
                  lambda p, s: f"  [{p['id']:<16}] {p['name']:<20} accent {p['accent']}  tags: {', '.join(p['tags'])}", args.n)
        return
    if args.domain == "fonts":
        show_list("FONT PAIRINGS", rank(fonts, font_terms, q),
                  lambda f, s: f"  [{f['id']:<18}] {f['name']:<40} tags: {', '.join(f['tags'])}", args.n)
        return
    if args.domain == "templates":
        show_list("TEMPLATES", rank(templates, tmpl_terms, q),
                  lambda t, s: f"  [{t['id']:<14}] {t['name']:<26} {t['use']}", args.n)
        return
    if args.domain == "hooks":
        cat = pick_hook_category(q)
        print(f"\n== HOOKS ({cat}) ==  [replace {{topic}} with your subject]")
        for h in hooks[cat]:
            print(f"  - {h}")
        return

    # default → recommend
    bp = rank(palettes, palette_terms, q)[0][1]
    bf = rank(fonts, font_terms, q)[0][1]
    bt = rank(templates, tmpl_terms, q)[0][1]
    cat = pick_hook_category(q)

    print("=" * 64)
    print("  XNIPER SOCIAL STUDIO — RECOMMENDED DESIGN SYSTEM")
    print("=" * 64)
    print(f"  Brief        : {args.query}")
    print(f"  Palette      : {bp['id']}  ({bp['name']})")
    print(f"     bg {bp['bg']}  text {bp['text']}  accent {bp['accent']}  accent2 {bp['accent2']}")
    print(f"  Font pairing : {bf['id']}  ({bf['name']})")
    print(f"  Template     : {bt['id']}  ({bt['name']})  -> use for: {bt['use']}")
    print(f"  Hook style   : {cat}")
    print("  Hook ideas   :")
    for h in hooks[cat][:3]:
        print(f"     - {h}")
    print("-" * 64)
    print("  content.json skeleton:")
    skeleton = {
        "eyebrow": "", "headline": "Your bold headline\nin two lines",
        "subhead": "One supporting line.", "cta": "Play now",
        "handle": "@yourbrand", "index": "01", "bigword": "10x",
        "palette": bp["id"], "font": bf["id"],
    }
    print(json.dumps(skeleton, indent=2))
    print("-" * 64)
    print("  Build it:")
    print(f"    python scripts/new_post.py --template {bt['id']} --content content.json \\")
    print(f"        --palette {bp['id']} --font {bf['id']} --size 1080x1350 --out out/post.html")
    print(f"    python scripts/render.py out/post.html --size 1080x1350 --out out/post.png")
    print("=" * 64)


if __name__ == "__main__":
    main()
