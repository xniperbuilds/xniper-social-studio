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


def main():
    ap = argparse.ArgumentParser(description="Generate N distinct design directions for a brief")
    ap.add_argument("query", nargs="?", default="", help="brief / topic keywords")
    ap.add_argument("-n", type=int, default=6, help="how many distinct ideas (default 6)")
    ap.add_argument("--seed", type=int, help="seed for reproducible output")
    ap.add_argument("--size", default="1080x1350", help="target size WxH")
    ap.add_argument("--direction", help="force a specific direction id (vary everything else)")
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
    pal_by = {p["id"]: p for p in palettes}
    font_by = {f["id"]: f for f in fonts}

    # choose which directions to feature
    if args.direction:
        chosen = [d for d in directions if d["id"] == args.direction]
        if not chosen:
            print(f"ERROR: no direction '{args.direction}'. Options: {', '.join(d['id'] for d in directions)}", file=sys.stderr)
            sys.exit(1)
        chosen = chosen * args.n
    else:
        pool = directions[:]
        if q:
            # bias toward matches but keep variety: sort by score, then jitter
            pool.sort(key=lambda d: tag_score(d.get("tags", []), q) + rng.random(), reverse=True)
        else:
            rng.shuffle(pool)
        chosen = pool[:args.n] if args.n <= len(pool) else pool + [rng.choice(directions) for _ in range(args.n - len(pool))]

    topic = args.query.strip() or "your topic"
    print("=" * 70)
    print(f"  {len(chosen)} DISTINCT DIRECTIONS for: {topic}")
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
