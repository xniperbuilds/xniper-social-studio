#!/usr/bin/env python3
"""
Xniper Social Studio — brandkit: save a brand once, reuse it across every post.

Series consistency is what separates a real brand feed from one-off AI posts.
This persists a brand (palette + fonts + handle + logo) to a LOCAL config file so
the same look carries across posts and sessions — the user gives it once, not
every time. Pairs with the ASK-FIRST law: ask once, save, then stop re-asking.

From a single brand hex it derives a full balanced palette via colorkit, so the
user can save a brand with just one color.

Storage: ~/.config/xniper-social-studio/brandkit.json  (local; gitignored)

Examples
--------
  python brandkit.py save mybrand --hex "#e94560" --font editorial-serif \
        --handle "@xniperbuilds" --logo instagram
  python brandkit.py list
  python brandkit.py get mybrand                 # human-readable
  python brandkit.py get mybrand --json          # merge into content.json
  python brandkit.py rm mybrand
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STORE = Path.home() / ".config" / "xniper-social-studio" / "brandkit.json"


def _load_colorkit():
    """Import colorkit.py from the same scripts dir to derive a palette from a hex."""
    p = Path(__file__).with_name("colorkit.py")
    spec = importlib.util.spec_from_file_location("colorkit", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_store():
    if STORE.exists():
        try:
            return json.loads(STORE.read_text(encoding="utf-8"))
        except Exception:
            print(f"WARN: {STORE} unreadable; starting fresh.", file=sys.stderr)
    return {}


def write_store(d):
    STORE.parent.mkdir(parents=True, exist_ok=True)
    STORE.write_text(json.dumps(d, indent=2), encoding="utf-8")


def cmd_save(args):
    store = load_store()
    brand = store.get(args.name, {})

    if args.hex:
        try:
            ck = _load_colorkit()
            pal = ck.palette(args.hex, light=args.light)
        except Exception as e:
            print(f"ERROR: could not derive palette from {args.hex!r}: {e}", file=sys.stderr)
            return 1
        brand["palette"] = {k: pal[k] for k in ("bg", "surface", "text", "muted",
                                                "accent", "accent2", "gradient")}
    # explicit token overrides (any subset)
    for key in ("bg", "surface", "text", "muted", "accent", "accent2", "gradient"):
        v = getattr(args, key, None)
        if v:
            brand.setdefault("palette", {})[key] = v if v.startswith(("#", "radial", "linear")) else "#" + v
    if args.font:   brand["font"] = args.font
    if args.handle: brand["handle"] = args.handle
    if args.logo:   brand["logo"] = args.logo

    if "palette" not in brand and not any([args.font, args.handle, args.logo]):
        print("ERROR: nothing to save. Pass --hex (or explicit colors) and/or "
              "--font/--handle/--logo.", file=sys.stderr)
        return 1

    store[args.name] = brand
    write_store(store)
    print(f"OK  saved brand '{args.name}' → {STORE}")
    _print_brand(args.name, brand)
    return 0


def cmd_list(args):
    store = load_store()
    if not store:
        print("(no saved brands yet — save one with: brandkit.py save <name> --hex <#hex>)")
        return 0
    print(f"Saved brands ({STORE}):")
    for name, b in store.items():
        acc = b.get("palette", {}).get("accent", "—")
        print(f"  {name:<16} accent {acc}  font {b.get('font','—')}  {b.get('handle','')}")
    return 0


def cmd_get(args):
    store = load_store()
    if args.name not in store:
        print(f"ERROR: no brand '{args.name}'. See: brandkit.py list", file=sys.stderr)
        return 1
    b = store[args.name]
    if args.json:
        # flatten into a content.json-friendly object
        out = dict(b.get("palette", {}))
        if b.get("font"):   out["font"] = b["font"]
        if b.get("handle"): out["handle"] = b["handle"]
        if b.get("logo"):   out["logo"] = b["logo"]
        print(json.dumps(out, indent=2))
    else:
        _print_brand(args.name, b)
    return 0


def cmd_rm(args):
    store = load_store()
    if args.name not in store:
        print(f"ERROR: no brand '{args.name}'.", file=sys.stderr)
        return 1
    del store[args.name]
    write_store(store)
    print(f"OK  removed '{args.name}'")
    return 0


def _print_brand(name, b):
    print(f"\nBRAND  {name}\n" + "─" * 40)
    pal = b.get("palette", {})
    for k in ("bg", "surface", "text", "muted", "accent", "accent2"):
        if k in pal:
            print(f"  {k:<8} {pal[k]}")
    if b.get("font"):   print(f"  font     {b['font']}")
    if b.get("handle"): print(f"  handle   {b['handle']}")
    if b.get("logo"):   print(f"  logo     {b['logo']}")
    print()


def main():
    ap = argparse.ArgumentParser(description="Persist + reuse a brand across posts")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("save", help="create/update a brand")
    ps.add_argument("name")
    ps.add_argument("--hex", help="brand color → derive a full balanced palette")
    ps.add_argument("--light", action="store_true", help="derive a light palette")
    for k in ("bg", "surface", "text", "muted", "accent", "accent2", "gradient"):
        ps.add_argument(f"--{k}", help=f"set {k} explicitly")
    ps.add_argument("--font", help="font pairing id from data/fonts.json")
    ps.add_argument("--handle", help="@handle")
    ps.add_argument("--logo", help="Simple Icons slug for the brand logo")
    ps.set_defaults(fn=cmd_save)

    pl = sub.add_parser("list", help="list saved brands"); pl.set_defaults(fn=cmd_list)

    pg = sub.add_parser("get", help="print a brand (use --json for content.json)")
    pg.add_argument("name"); pg.add_argument("--json", action="store_true")
    pg.set_defaults(fn=cmd_get)

    pr = sub.add_parser("rm", help="delete a brand")
    pr.add_argument("name"); pr.set_defaults(fn=cmd_rm)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
