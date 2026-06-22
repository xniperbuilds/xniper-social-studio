#!/usr/bin/env python3
"""
Xniper Social Studio — real assets: brand logos + generated textures.

Kills the flat CSS-only look by pulling REAL brand logos (Simple Icons, no key)
and generating grain / noise / paper / gradient-mesh texture layers (Pillow,
fully offline). Pair these with the photo-treatment CSS in reference/assets.md.

Examples
--------
  # Brand logo as SVG (recolored), no API key needed:
  python assets.py icon instagram --color FFFFFF --out out/ig.svg
  python assets.py icon github                       --out out/gh.svg

  # Texture overlays (offline, Pillow):
  python assets.py texture grain  --size 1080x1350 --out out/grain.png
  python assets.py texture noise  --size 1080x1350 --opacity 14 --out out/noise.png
  python assets.py texture paper  --size 1080x1350 --out out/paper.png
  python assets.py texture mesh   --size 1080x1350 --colors 1a1a2e,e94560,0f3460 --out out/mesh.png

Simple Icons slugs: lowercase brand name, no spaces (e.g. "youtube", "x",
"tiktok", "linkedin"). Full list: https://simpleicons.org
"""
import argparse
import io
import math
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SIZE_RE = re.compile(r"(\d{2,5})x(\d{2,5})")


def parse_size(s, default=(1080, 1350)):
    if not s:
        return default
    m = SIZE_RE.search(s)
    return (int(m.group(1)), int(m.group(2))) if m else default


# ---------------------------------------------------------------- brand logos
def fetch_icon(slug, color, out):
    """Simple Icons CDN → SVG. No API key. color = hex without '#', or None."""
    try:
        import requests
    except ImportError:
        print("ERROR: 'requests' not installed. Run: pip install requests", file=sys.stderr)
        return 1
    slug = slug.strip().lower()
    color = (color or "").lstrip("#").strip()
    url = f"https://cdn.simpleicons.org/{slug}"
    if color:
        url += f"/{color}"
    try:
        r = requests.get(url, timeout=20)
    except Exception as e:
        print(f"ERROR: fetch failed ({e}). Check your connection.", file=sys.stderr)
        return 1
    if r.status_code != 200 or b"<svg" not in r.content[:400]:
        print(f"ERROR: no logo for slug '{slug}' (HTTP {r.status_code}). "
              f"Check the slug at https://simpleicons.org", file=sys.stderr)
        return 1
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(r.content)
    print(f"OK  {out}  (logo: {slug}{', #' + color if color else ''})")
    return 0


# ------------------------------------------------------------------- textures
def _img(w, h):
    from PIL import Image
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def tex_grain(w, h, opacity, mono=True):
    """Fine film grain as a transparent overlay (multiply/overlay it in CSS)."""
    from PIL import Image
    import random
    px = bytearray()
    a = max(0, min(255, opacity))
    for _ in range(w * h):
        v = random.randint(0, 255)
        if mono:
            px += bytes((v, v, v, a))
        else:
            px += bytes((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), a))
    return Image.frombytes("RGBA", (w, h), bytes(px))


def tex_noise(w, h, opacity):
    return tex_grain(w, h, opacity, mono=False)


def tex_paper(w, h, opacity):
    """Soft paper fiber: low-frequency mottle + light grain."""
    from PIL import Image, ImageFilter
    import random
    base = Image.new("L", (w, h), 128)
    px = base.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = max(0, min(255, 128 + random.randint(-40, 40)))
    base = base.filter(ImageFilter.GaussianBlur(2.5))
    out = Image.new("RGBA", (w, h))
    op = out.load()
    bp = base.load()
    a = max(0, min(255, opacity))
    for y in range(h):
        for x in range(w):
            v = bp[x, y]
            op[x, y] = (v, v, v, a)
    return out


def tex_mesh(w, h, colors):
    """Gradient mesh: a few soft radial blobs blended — a real background layer."""
    from PIL import Image, ImageDraw, ImageFilter
    if not colors:
        colors = ["1a1a2e", "e94560", "0f3460"]
    cols = [tuple(int(c.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) for c in colors]
    base = Image.new("RGB", (w, h), cols[0])
    # anchor blob positions deterministically around the canvas
    anchors = [(0.22, 0.25), (0.80, 0.30), (0.30, 0.82), (0.78, 0.78), (0.5, 0.5)]
    for i, c in enumerate(cols[1:] + cols[:1]):
        ax, ay = anchors[i % len(anchors)]
        cx, cy = int(w * ax), int(h * ay)
        rad = int(max(w, h) * 0.55)
        blob = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(blob)
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=255)
        blob = blob.filter(ImageFilter.GaussianBlur(rad * 0.35))
        layer = Image.new("RGB", (w, h), c)
        base = Image.composite(layer, base, blob)
    base = base.filter(ImageFilter.GaussianBlur(2))
    # light grain to de-band the gradient
    g = tex_grain(w, h, 8)
    out = base.convert("RGBA")
    out.alpha_composite(g)
    return out


def make_texture(kind, w, h, opacity, colors, out):
    builders = {
        "grain": lambda: tex_grain(w, h, opacity if opacity is not None else 16),
        "noise": lambda: tex_noise(w, h, opacity if opacity is not None else 16),
        "paper": lambda: tex_paper(w, h, opacity if opacity is not None else 22),
        "mesh":  lambda: tex_mesh(w, h, colors),
    }
    if kind not in builders:
        print(f"ERROR: unknown texture '{kind}'. Use: grain | noise | paper | mesh", file=sys.stderr)
        return 1
    try:
        img = builders[kind]()
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip install pillow", file=sys.stderr)
        return 1
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    print(f"OK  {out}  (texture: {kind} {w}x{h})")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Real assets: brand logos + textures")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("icon", help="fetch a brand logo SVG (Simple Icons, no key)")
    pi.add_argument("slug", help="brand slug, e.g. instagram, youtube, github")
    pi.add_argument("--color", help="hex fill without '#', e.g. FFFFFF")
    pi.add_argument("--out", required=True, help="output .svg")

    pt = sub.add_parser("texture", help="generate a texture overlay PNG (offline)")
    pt.add_argument("kind", help="grain | noise | paper | mesh")
    pt.add_argument("--size", help="WxH (default 1080x1350)")
    pt.add_argument("--opacity", type=int, help="0-255 alpha for grain/noise/paper")
    pt.add_argument("--colors", help="mesh colors, comma hex e.g. 1a1a2e,e94560,0f3460")
    pt.add_argument("--out", required=True, help="output .png")

    args = ap.parse_args()
    if args.cmd == "icon":
        return fetch_icon(args.slug, args.color, args.out)
    if args.cmd == "texture":
        w, h = parse_size(args.size)
        colors = [c for c in (args.colors or "").split(",") if c.strip()]
        return make_texture(args.kind, w, h, args.opacity, colors, args.out)
    return 1


if __name__ == "__main__":
    sys.exit(main())
