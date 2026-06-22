#!/usr/bin/env python3
"""
Xniper Social Studio — colorkit: one brand hex → a full, balanced color system.

A pro never designs from a single flat color. From ONE brand hex this derives a
tonal ramp, a premium dark + light palette in the skill's exact palette schema
(bg/surface/text/muted/accent/accent2/gradient), color harmonies, 60-30-10
guidance, and WCAG contrast checks — so the output is balanced, not a guess.

Pure standard library (colorsys). No dependencies.

Examples
--------
  python colorkit.py "#e94560"
  python colorkit.py 1a73e8 --light
  python colorkit.py "#00F0FF" --json        # palette object ready for content.json
"""
import argparse
import colorsys
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------- conversions
def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"bad hex: {h!r}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c))):02X}" for c in rgb)


def rgb_to_hls(rgb):
    r, g, b = (c / 255 for c in rgb)
    return colorsys.rgb_to_hls(r, g, b)  # h, l, s in 0..1


def hls_to_hex(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h % 1.0, max(0, min(1, l)), max(0, min(1, s)))
    return rgb_to_hex((r * 255, g * 255, b * 255))


# --------------------------------------------------------------- WCAG contrast
def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (_lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(hex_to_rgb(a)), luminance(hex_to_rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def rate(ratio):
    if ratio >= 7:    return "AAA"
    if ratio >= 4.5:  return "AA"
    if ratio >= 3:    return "AA-large"
    return "FAIL"


# ----------------------------------------------------------------- derivations
def ramp(hex_in):
    """50 (lightest) → 900 (darkest), holding hue, easing lightness + saturation."""
    h, l, s = rgb_to_hls(hex_to_rgb(hex_in))
    steps = [("50", 0.96), ("100", 0.90), ("200", 0.80), ("300", 0.68),
             ("400", 0.57), ("500", 0.50), ("600", 0.42), ("700", 0.33),
             ("800", 0.24), ("900", 0.15)]
    out = {}
    for name, L in steps:
        # ease saturation down at the extremes so tints/shades don't go neon/muddy
        sat = s * (0.6 + 0.4 * (1 - abs(L - 0.5) * 2))
        out[name] = hls_to_hex(h, L, sat)
    return out


def harmonies(hex_in):
    h, l, s = rgb_to_hls(hex_to_rgb(hex_in))
    def at(deg, dl=0.0, ds=0.0):
        return hls_to_hex(h + deg / 360.0, l + dl, max(0, min(1, s + ds)))
    return {
        "complement":       at(180),
        "analogous":        [at(-30), at(30)],
        "triad":            [at(120), at(240)],
        "split_complement": [at(150), at(210)],
        "accent2 (suggested)": at(150, dl=0.04),  # split-comp, slightly lifted
    }


def palette(hex_in, light=False):
    """Build a balanced palette in the skill's schema from one brand hex."""
    h, l, s = rgb_to_hls(hex_to_rgb(hex_in))
    accent = hex_in if hex_in.startswith("#") else "#" + hex_in.lstrip("#")
    accent = accent.upper()
    accent2 = hls_to_hex(h + 150 / 360.0, min(0.62, l + 0.04), max(0, min(1, s)))
    if not light:
        bg      = hls_to_hex(h, 0.07, min(s, 0.35))   # near-black, hue-tinted
        surface = hls_to_hex(h, 0.12, min(s, 0.30))
        text    = hls_to_hex(h, 0.97, min(s, 0.12))   # near-white, faintly tinted
        muted   = hls_to_hex(h, 0.66, min(s, 0.18))
    else:
        bg      = hls_to_hex(h, 0.975, min(s, 0.10))
        surface = hls_to_hex(h, 0.93, min(s, 0.12))
        text    = hls_to_hex(h, 0.12, min(s, 0.25))
        muted   = hls_to_hex(h, 0.42, min(s, 0.20))
    ar, ag, ab = hex_to_rgb(accent)
    a2r, a2g, a2b = hex_to_rgb(accent2)
    gradient = (
        f"radial-gradient(120% 90% at 15% 10%, rgba({ar},{ag},{ab},0.22), transparent 55%), "
        f"radial-gradient(120% 90% at 90% 95%, rgba({a2r},{a2g},{a2b},0.20), transparent 55%), "
        f"{bg}"
    )
    return {
        "id": "brand-derived",
        "name": "Brand Derived",
        "tags": ["light" if light else "dark", "brand", "derived"],
        "bg": bg, "surface": surface, "text": text, "muted": muted,
        "accent": accent, "accent2": accent2, "gradient": gradient,
    }


# ---------------------------------------------------------------------- report
def report(hex_in, light):
    pal = palette(hex_in, light)
    print(f"\nBRAND COLOR  {hex_in.upper()}   ({'light' if light else 'dark'} system)\n" + "─" * 52)

    print("\nTONAL RAMP")
    for k, v in ramp(hex_in).items():
        print(f"  {k:>3}  {v}")

    print("\nPALETTE (skill schema — drop into content.json)")
    for k in ("bg", "surface", "text", "muted", "accent", "accent2"):
        print(f"  {k:<8} {pal[k]}")

    print("\nCONTRAST (WCAG)")
    for label, fg, bg in (("text on bg", pal["text"], pal["bg"]),
                          ("muted on bg", pal["muted"], pal["bg"]),
                          ("text on surface", pal["text"], pal["surface"]),
                          ("accent on bg", pal["accent"], pal["bg"])):
        r = contrast(fg, bg)
        print(f"  {label:<16} {r:>5}:1  {rate(r)}")
    print("  (body text needs AA 4.5:1; large display 3:1.)")

    print("\nHARMONIES")
    for k, v in harmonies(hex_in).items():
        print(f"  {k:<22} {v}")

    print("\n60-30-10 BALANCE")
    print(f"  60% dominant  → {pal['bg']} (+ surface for panels)")
    print(f"  30% secondary → {pal['surface']} / {pal['muted']} (structure, body)")
    print(f"  10% accent    → {pal['accent']} (focal only — never >~15% of canvas)")
    print("  Tint shadows toward bg hue, never pure #000. De-band gradients with")
    print("  `assets.py texture grain` overlaid at low opacity.\n")


def main():
    ap = argparse.ArgumentParser(description="One brand hex → full color system")
    ap.add_argument("hex", help="brand color, e.g. #e94560 or e94560")
    ap.add_argument("--light", action="store_true", help="build a light-mode palette")
    ap.add_argument("--json", action="store_true", help="print only the palette object")
    args = ap.parse_args()
    try:
        hex_to_rgb(args.hex)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(palette(args.hex, args.light), indent=2))
    else:
        report(args.hex, args.light)
    return 0


if __name__ == "__main__":
    sys.exit(main())
