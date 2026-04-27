#!/usr/bin/env python3
"""
Bake the dark-theme colour palette into a static set of SVG variants
under `assets/figma/dark/`. The dark file at `assets/figma/dark/vN.svg`
keeps the exact filename of its light counterpart (`assets/figma/vN.svg`),
so the runtime swap is just `figma/X.svg` <-> `figma/dark/X.svg`.

Colour mapping (matches the previous `html.dark .iso-stage` overrides):

  Body bars (v1, v3..v18):
    fill="var(--fill-0, white)"        -> fill="#0B0F19"
    stroke="var(--stroke-0, #DFE5EE)"  -> stroke="#171C2E"
    <stop stop-color="white" ...>      -> <stop stop-color="#0B0F19" ...>
       (the stop-opacity attributes on each stop are preserved as-is,
        so the gradient shape -- transparent at the top, opaque at the
        bottom -- carries over unchanged.)

  Top-poly diamonds (v2, v19..v24):
    fill="#FBFCFC"                     -> fill="#171C2E"

Run: `python scripts/gen_dark_svgs.py` from the repo root.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "figma"
OUT = SRC / "dark"

TOP_POLYS = {"v2", "v19", "v20", "v21", "v22", "v23", "v24"}

DARK_FILL = "#0B0F19"     # bar body base + gradient stop colour
DARK_STROKE = "#171C2E"   # diagonal pattern stroke
DARK_TOP = "#171C2E"      # top-poly diamond fill

OUT.mkdir(parents=True, exist_ok=True)

generated = []
for f in sorted(SRC.glob("v*.svg")):
    name = f.stem
    text = f.read_text(encoding="utf-8")

    if name in TOP_POLYS:
        text = text.replace('fill="#FBFCFC"', f'fill="{DARK_TOP}"')
    else:
        text = text.replace('var(--fill-0, white)', f'var(--fill-0, {DARK_FILL})')
        text = text.replace('var(--stroke-0, #DFE5EE)', f'var(--stroke-0, {DARK_STROKE})')
        text = text.replace('stop-color="white"', f'stop-color="{DARK_FILL}"')

    out = OUT / f"{name}.svg"
    out.write_text(text, encoding="utf-8")
    generated.append(out.relative_to(ROOT).as_posix())

print(f"Generated {len(generated)} dark-theme SVGs:")
for n in generated:
    print(f"  {n}")
