#!/usr/bin/env python3
"""
Xniper Social Studio — VARIETY ENGINE. Spin up N distinct design directions for a
brief, each a different aesthetic so nothing ever looks like the same AI template.

  direction x palette x font x layout x motifs  =  tens of thousands of combos.

Examples
--------
  python ideate.py "indie game launch"            # 6 distinct directions, fresh each run
  python ideate.py "productivity tips carousel" -n 8
  python ideate.py "luxury skincare" --seed 42    # reproducible
  python ideate.py "anything" --direction riso-print   # force one direction, vary the rest

Each idea prints: the aesthetic direction (+ how to build it), a palette, a font
pairing, a layout/template, motifs to use, and a ready build command. Pick one and
either fill a template (new_post.py) or hand-build per reference/directions.md.
"""
import argparse
import json
import random
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DATA = Path(__file__).resolve().parent.parent / "data"


def load(name, key):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)[key]


def tokens(text):
    return [t for t in re.split(r"[^a-z0-9]+", str(text).lower()) if t]


def tag_score(item_tags, query_terms):
    tags = set(t.lower() for t in item_tags)
    return sum(1 for q in query_terms if q in tags)


def pick(items, by_id, ids, query_terms, rng):
    """Prefer an example id that exists; else a query/tag match; else random."""
    valid = [i for i in ids if i in by_id]
    if valid:
        return by_id[rng.choice(valid)]
    if query_terms:
        ranked = sorted(items, key=lambda it: tag_score(it.get("tags", []), query_terms), reverse=True)
        top = [it for it in ranked if tag_score(it.get("tags", []), query_terms) > 0][:5]
        if top:
            return rng.choice(top)
    return rng.choice(items)


HOOK_KEYS = {
    "listicle": ["tip", "tips", "list", "steps", "howto", "guide", "ways", "mistakes", "rules", "hacks"],
    "transformation": ["before", "after", "growth", "result", "journey", "transform"],
    "mistake": ["mistake", "wrong", "fail", "avoid", "error", "flop"],
    "cta": ["launch", "promo", "sale", "drop", "free", "new", "announce"],
    "curiosity": ["secret", "reveal", "behind", "nobody"],
    "bold_claim": ["bold", "value", "benefit", "best"],
    "question": [],
}


def pick_hook_category(query_terms):
    best, best_n = "question", 0
    for cat, kws in HOOK_KEYS.items():
        n = sum(1 for q in query_terms if q in kws)
        if n > best_n:
            best, best_n = cat, n
    return best


def carousel_plan(d, palettes, fonts, templates, hooks, q, n, size, rng):
    pal_by = {p["id"]: p for p in palettes}
    font_by = {f["id"]: f for f in fonts}
    pal = pick(palettes, pal_by, d.get("example_palettes", []), q + d.get("tags", []), rng)
    fnt = pick(fonts, font_by, d.get("example_fonts", []), q + d.get("tags", []), rng)
    ids = {t["id"] for t in templates}
    cover = "carousel-cover" if "carousel-cover" in ids else "quote-bold"
    cta = "cta-endcard" if "cta-endcard" in ids else "announcement"
    body_pool = [t for t in ["tip-card", "blueprint-diagram", "stat-card", "editorial-vintage", "quote-bold"] if t in ids] or ["tip-card"]
    cat = pick_hook_category(q)
    hook = (hooks.get(cat) or hooks.get("question") or ["Here's the one thing about {topic}"])
    hook = rng.choice(hook).replace("{topic}", (" ".join(q) or "this"))
    handle = "@yourbrand"

    print("=" * 70)
    print(f"  CAROUSEL PLAN — {n} slides")
    print(f"  Direction : {d['name']} ({d['id']})   [LOCKED across the set]")
    print(f"  Palette   : {pal['id']}   Font: {fnt['id']}   (locked; vary only layout)")
    print(f"  How-to    : {d['vibe']}")
    print("=" * 70)
    slides = []
    for i in range(1, n + 1):
        if i == 1:
            role, tmpl = "COVER / HOOK", cover
            content = {"eyebrow": f"1/{n}", "headline": hook, "handle": handle, "cta": "swipe"}
        elif i == n:
            role, tmpl = "CTA / END-CARD", cta
            content = {"eyebrow": f"{n}/{n}", "headline": "Found this useful?", "subhead": "Save it + follow for more.", "cta": "Follow", "handle": handle}
        else:
            role, tmpl = "POINT", body_pool[(i - 2) % len(body_pool)]
            idx = f"{i-1:02d}"
            content = {"eyebrow": f"POINT {idx}", "index": idx, "headline": "Point goes here", "subhead": "One supporting line.", "handle": handle, "cta": f"{i}/{n}"}
        slides.append((i, role, tmpl, content))
        print(f"\n  Slide {i} — {role}   template: {tmpl}")
        print(f"     content: {json.dumps(content, ensure_ascii=False)}")
    print("\n" + "-" * 70)
    print("  Write each content above to s1.json..sN.json, then (palette+font LOCKED):")
    for i, role, tmpl, _ in slides:
        print(f"    python scripts/new_post.py --template {tmpl} --palette {pal['id']} --font {fnt['id']} --content s{i}.json --size {size} --out out/slide-{i}-{size}.html")
    print("    python scripts/render.py out/ --batch --out out/exports/")
    print("\n  Keep the direction the SAME on every slide; vary the layout. Next carousel: a different direction.")


def main():
    ap = argparse.ArgumentParser(description="Generate N distinct design directions for a brief")
    ap.add_argument("query", nargs="?", default="", help="brief / topic keywords")
    ap.add_argument("-n", type=int, default=6, help="how many distinct ideas (default 6)")
    ap.add_argument("--carousel", type=int, metavar="SLIDES", help="plan a full carousel of SLIDES slides (one locked direction)")
    ap.add_argument("--seed", type=int, help="seed for reproducible output")
    ap.add_argument("--size", default="1080x1350", help="target size WxH")
    ap.add_argument("--direction", help="force a specific direction id (vary everything else)")
    ap.add_argument("--category", help="bias ideas to a purpose category id (see --list-categories)")
    ap.add_argument("--list-categories", action="store_true", help="list the purpose categories and exit")
    args = ap.parse_args()

    rng = random.Random(args.seed)  # seed=None -> fresh every run = endless ideas
    q = tokens(args.query)

    directions = load("directions.json", "directions")
    palettes = load("palettes.json", "palettes")
    fonts = load("fonts.json", "fonts")
    try:
        templates = load("templates.json", "templates")
    except Exception:
        templates = []
    try:
        hooks = load("hooks.json", "hooks")
    except Exception:
        hooks = {}
    try:
        categories = load("categories.json", "categories")
    except Exception:
        categories = []
    cat_by = {c["id"]: c for c in categories}
    pal_by = {p["id"]: p for p in palettes}
    font_by = {f["id"]: f for f in fonts}

    if args.list_categories:
        print("PURPOSE CATEGORIES  (template = category x direction x role)\n")
        for c in categories:
            print(f"  [{c['id']:<22}] {c['name']:<26} role:{c.get('role',''):<8} {c['purpose']}")
        return

    cat = cat_by.get(args.category) if args.category else None
    if args.category and not cat:
        print(f"ERROR: no category '{args.category}'. Try --list-categories.", file=sys.stderr)
        sys.exit(1)

    # full-carousel plan: one locked direction across the whole set
    if args.carousel:
        if args.direction:
            d = next((x for x in directions if x["id"] == args.direction), None)
            if not d:
                print(f"ERROR: no direction '{args.direction}'. Options: {', '.join(x['id'] for x in directions)}", file=sys.stderr)
                sys.exit(1)
        elif q:
            d = sorted(directions, key=lambda x: tag_score(x.get("tags", []), q) + rng.random(), reverse=True)[0]
        else:
            d = rng.choice(directions)
        carousel_plan(d, palettes, fonts, templates, hooks, q, max(2, args.carousel), args.size, rng)
        return

    # choose which directions to feature
    if args.direction:
        chosen = [d for d in directions if d["id"] == args.direction]
        if not chosen:
            print(f"ERROR: no direction '{args.direction}'. Options: {', '.join(d['id'] for d in directions)}", file=sys.stderr)
            sys.exit(1)
        chosen = chosen * args.n
    else:
        pool = directions[:]
        if cat:
            suited = set(cat.get("directions", []))
            pool = [d for d in directions if d["id"] in suited] or directions[:]
        if q:
            # bias toward matches but keep variety: sort by score, then jitter
            pool.sort(key=lambda d: tag_score(d.get("tags", []), q) + rng.random(), reverse=True)
        else:
            rng.shuffle(pool)
        chosen = pool[:args.n] if args.n <= len(pool) else pool + [rng.choice(pool) for _ in range(args.n - len(pool))]

    topic = args.query.strip() or "your topic"
    print("=" * 70)
    print(f"  {len(chosen)} DISTINCT DIRECTIONS for: {topic}")
    if cat:
        print(f"  Category: {cat['name']} ({cat['id']}) — {cat['purpose']}  [role: {cat.get('role','')}]")
    print(f"  (run again for a fresh set; --seed to lock; combos in the tens of thousands)")
    print("=" * 70)

    for i, d in enumerate(chosen, 1):
        pal = pick(palettes, pal_by, d.get("example_palettes", []), q + d.get("tags", []), rng)
        fnt = pick(fonts, font_by, d.get("example_fonts", []), q + d.get("tags", []), rng)
        motifs = d.get("motifs", [])
        use_motifs = motifs if len(motifs) <= 3 else rng.sample(motifs, 3)
        # suggest a template if one shares a tag, else hand-build
        tmpl = None
        for t in templates:
            if set(t.get("tags", [])) & set(d.get("tags", [])):
                tmpl = t["id"]; break

        print(f"\n[{i}] {d['name'].upper()}  ({d['id']})")
        print(f"    vibe   : {d['vibe']}")
        print(f"    type   : {d['type']}")
        print(f"    bg     : {d['bg']}")
        print(f"    palette: {pal['id']}  (bg {pal['bg']} / text {pal['text']} / accent {pal['accent']})")
        print(f"    font   : {fnt['id']}  ({fnt['name']})")
        print(f"    motifs : {', '.join(use_motifs)}")
        print(f"    layout : {d['layout']}")
        print(f"    avoid  : {d['avoid']}")
        if tmpl:
            print(f"    build  : python scripts/new_post.py --template {tmpl} --palette {pal['id']} --font {fnt['id']} --content content.json --size {args.size} --out out/{i}.html")
        else:
            print(f"    build  : hand-build this direction per reference/directions.md, then render.py")

    print("\n" + "-" * 70)
    print("  Tip: every render should use a DIFFERENT direction than the last —")
    print("  especially across a carousel set and across consecutive posts.")


if __name__ == "__main__":
    main()
