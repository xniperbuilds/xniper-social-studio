#!/usr/bin/env python3
"""
Xniper Social Studio — qa: measured checks on a rendered PNG.

The critique loop (reference/art-direction.md) is the judgment pass; this is the
MEASUREMENT pass that backs it with numbers instead of eyeballing. Run it on the
exported PNG before handoff. It flags what a model can't reliably see: off-by-a-
pixel sizing, an oversized file, content breaking the safe zone, a flat-fill
background (the #1 AI tell), and an over-dominant accent.

Pillow only. Honest about limits: it cannot read text, so true text/bg contrast
still needs `colorkit.py` on your chosen tokens + the visual pass — this catches
the *structural* problems.

Examples
--------
  python qa.py out/slide-1.png --size 1080x1350
  python qa.py out/slide-1.png --size 1080x1920 --platform story
  python qa.py out/exports/ --batch --size 1080x1350
"""
import argparse
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SIZE_RE = re.compile(r"(\d{2,5})x(\d{2,5})")

# central safe fraction + extra reserved bands (top/bottom) per platform UI
PLATFORM_SAFE = {
    "post":   {"margin": 0.06, "top": 0.0,  "bottom": 0.0},
    "story":  {"margin": 0.06, "top": 0.14, "bottom": 0.18},  # status + caption/CTA UI
    "reel":   {"margin": 0.06, "top": 0.12, "bottom": 0.22},  # right rail + caption
    "thumb":  {"margin": 0.04, "top": 0.0,  "bottom": 0.10},  # duration chip
}
# soft per-platform file-size ceilings (MB) — warn, don't fail
SIZE_CEIL_MB = {"post": 8, "story": 8, "reel": 8, "thumb": 4}


def expected_size(path, override):
    if override:
        m = SIZE_RE.search(override.lower())
        if m:
            return int(m.group(1)), int(m.group(2))
    m = SIZE_RE.search(path.name)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def analyze(path, expect, platform):
    from PIL import Image
    img = Image.open(path).convert("RGB")
    W, H = img.size
    issues, notes = [], []

    # 1. exact dimensions (account for 2x retina export)
    if expect:
        ew, eh = expect
        if (W, H) == (ew, eh):
            notes.append(f"dimensions {W}x{H} == target")
        elif (W, H) == (ew * 2, eh * 2):
            notes.append(f"dimensions {W}x{H} (2x of {ew}x{eh}) — retina, OK")
        else:
            issues.append(f"CRITICAL dimensions {W}x{H} != {ew}x{eh} (nor 2x). Re-render at exact size.")

    # 2. file size
    mb = path.stat().st_size / 1_048_576
    ceil = SIZE_CEIL_MB.get(platform, 8)
    (notes if mb <= ceil else issues).append(
        f"file size {mb:.2f} MB" + ("" if mb <= ceil else f" — over ~{ceil} MB; export lighter"))

    # downscale for fast pixel stats
    small = img.resize((180, round(180 * H / W)), Image.BILINEAR)
    sw, sh = small.size
    load = small.load()

    def lum(p):
        return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]

    L = [[lum(load[x, y]) for x in range(sw)] for y in range(sh)]
    flat_lums = [L[y][x] for y in range(sh) for x in range(sw)]
    mean = sum(flat_lums) / len(flat_lums)
    std = (sum((v - mean) ** 2 for v in flat_lums) / len(flat_lums)) ** 0.5
    rng = max(flat_lums) - min(flat_lums)

    # 3. flat-fill detector (the #1 AI tell). A true flat fill has σ≈0 AND tiny
    # range; a moody gradient has low σ but real range — don't punish it.
    if std < 5 and rng < 24:
        issues.append(f"FLAT background (luminance σ={std:.0f}, range {rng:.0f}) — add "
                      f"gradient/grain/glow/large type. A flat fill is a fallback, not a design.")
    elif std < 8 and rng < 40:
        notes.append(f"low depth (σ={std:.0f}, range {rng:.0f}) — consider more atmosphere")
    else:
        notes.append(f"depth OK (luminance σ={std:.0f}, range {rng:.0f})")

    # 4. safe-zone via LOCAL CONTRAST (edges/text), not bbox — a smooth full-bleed
    # gradient has near-zero local contrast, so it won't false-positive; real
    # foreground (text/shapes) near a border has high local contrast.
    def local_contrast(x, y):
        c = L[y][x]
        m = 0.0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < sw and 0 <= ny < sh:
                m = max(m, abs(c - L[ny][nx]))
        return m

    saf = PLATFORM_SAFE.get(platform, PLATFORM_SAFE["post"])
    mL = int(saf["margin"] * sw); mR = int(sw - saf["margin"] * sw)
    mT = int((saf["margin"] + saf["top"]) * sh); mB = int(sh - (saf["margin"] + saf["bottom"]) * sh)
    EDGE = 28  # local-contrast threshold that marks "real content" vs gradient
    band = {"left": False, "right": False, "top": False, "bottom": False}
    for y in range(1, sh - 1):
        for x in range(1, sw - 1):
            inside = (mL <= x <= mR and mT <= y <= mB)
            if inside:
                continue
            if local_contrast(x, y) > EDGE:
                if x < mL: band["left"] = True
                if x > mR: band["right"] = True
                if y < mT: band["top"] = True
                if y > mB: band["bottom"] = True
    breaches = [k for k, v in band.items() if v]
    if breaches:
        issues.append(f"content (text/graphic) sits in the {platform} safe-zone band on: "
                      f"{', '.join(breaches)} — pull it inward (see reference/platforms.md)")
    else:
        notes.append(f"no hard content in the {platform} safe-zone bands")

    # 5. accent dominance: strong-saturation coverage across the canvas
    from colorsys import rgb_to_hls
    strong = total = 0
    for y in range(sh):
        for x in range(sw):
            p = load[x, y]
            _, l, s = rgb_to_hls(p[0]/255, p[1]/255, p[2]/255)
            total += 1
            if s > 0.45 and 0.25 < l < 0.75:
                strong += 1
    cov = strong / total
    if cov > 0.35:
        issues.append(f"accent/saturated color covers ~{cov*100:.0f}% — an accent over "
                      f"~15% stops reading as an accent. Mute or shrink it.")
    else:
        notes.append(f"saturated coverage ~{cov*100:.0f}% (accent restrained)")

    return issues, notes


def run_one(path, expect, platform):
    print(f"\n■ {path.name}  [{platform}]")
    try:
        issues, notes = analyze(path, expect, platform)
    except ImportError:
        print("  ERROR: Pillow not installed. Run: pip install pillow", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return 1
    for n in notes:
        print(f"  ok   {n}")
    for i in issues:
        print(f"  ⚠    {i}")
    print("  → " + ("PASS — measured checks clean (still run the visual critique pass)."
                    if not issues else f"{len(issues)} issue(s) to fix, then re-render + re-run."))
    return 1 if issues else 0


def main():
    ap = argparse.ArgumentParser(description="Measured QA on a rendered PNG")
    ap.add_argument("input", help="a .png OR a folder (with --batch)")
    ap.add_argument("--size", help="target WxH (else parsed from filename)")
    ap.add_argument("--platform", default="post", help="post | story | reel | thumb")
    ap.add_argument("--batch", action="store_true", help="check every .png in a folder")
    args = ap.parse_args()
    plat = args.platform.lower()
    if plat not in PLATFORM_SAFE:
        print(f"WARN: unknown platform '{plat}', using 'post'.", file=sys.stderr)
        plat = "post"
    inp = Path(args.input)
    if args.batch or inp.is_dir():
        files = sorted(inp.glob("*.png"))
        if not files:
            print(f"ERROR: no .png in {inp}", file=sys.stderr); return 1
        bad = sum(run_one(f, expected_size(f, args.size), plat) for f in files)
        print(f"\n{bad} of {len(files)} file(s) have issues." if bad else
              f"\nAll {len(files)} file(s) passed measured QA.")
        return 1 if bad else 0
    if not inp.exists():
        print(f"ERROR: not found: {inp}", file=sys.stderr); return 1
    return run_one(inp, expected_size(inp, args.size), plat)


if __name__ == "__main__":
    sys.exit(main())
