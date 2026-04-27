#!/usr/bin/env python3
"""
Generate dark-theme variants of every SVG asset under assets/figma/.
Swaps light-theme color values for dark-theme equivalents:

  body bars:
    fill="var(--fill-0, white)"             -> #1f2937 (gray-800, body fill)
    stroke="var(--stroke-0, #DFE5EE)"       -> #374151 (gray-700, pattern stroke)
    stop-color="white"                      -> #1f2937 (gradient stops)

  top-poly diamonds (v2, v19..v24):
    fill="#FBFCFC"                          -> #d1d5dc (gray-300, lit-top highlight)

Outputs to assets/figma/<name>-dark.svg.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "figma"

TOP_POLYS = {"v2", "v19", "v20", "v21", "v22", "v23", "v24"}

DARK_FILL = "#1f2937"
DARK_STROKE = "#374151"
DARK_TOP = "#d1d5dc"
DARK_GRADIENT_STOP = "#1f2937"

generated = []
for f in sorted(SRC.glob("v*.svg")):
    name = f.stem
    if name.endswith("-dark"):
        continue

    text = f.read_text(encoding="utf-8")

    if name in TOP_POLYS:
        text = text.replace('fill="#FBFCFC"', f'fill="{DARK_TOP}"')
    else:
        text = text.replace('var(--fill-0, white)', f'var(--fill-0, {DARK_FILL})')
        text = text.replace('var(--stroke-0, #DFE5EE)', f'var(--stroke-0, {DARK_STROKE})')
        text = text.replace('stop-color="white"', f'stop-color="{DARK_GRADIENT_STOP}"')

    out = SRC / f"{name}-dark.svg"
    out.write_text(text, encoding="utf-8")
    generated.append(out.name)

print(f"Generated {len(generated)} dark-theme SVGs:")
for n in generated:
    print(f"  {n}")
