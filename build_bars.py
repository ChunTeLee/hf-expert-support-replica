"""Generate bars.css with center-anchored positions, plus an inline-SVG iso-grid CSS."""
import pathlib, re, urllib.parse

BASE = pathlib.Path(r"C:\HuggingFace\Huggy model\replica")
W_REF = 1280  # Figma reference section width

# (suffix, svg, h, left_expr, right_expr, top_expr_center_offset, flip)
BARS = [
    ("2685", "v1",  260.032, "calc(5.18% - 0.6px)",   "calc(87.78% + 0.5px)",  119.03,  False),
    ("2686", "v2",  51.961,  "calc(89.58% + 0.53px)", "calc(3.38% - 0.62px)",  197.08,  False),
    ("2687", "v3",  77.941,  "calc(89.58% + 0.53px)", "calc(6.9% - 0.57px)",   233.96,  True),
    ("2688", "v4",  259.804, "calc(89.58% + 0.53px)", "calc(3.38% - 0.62px)",  145.12,  False),
    ("2689", "v5",  233.824, "calc(86.07% + 0.48px)", "calc(10.42% - 0.53px)", 132.13,  True),
    ("2690", "v6",  181.863, "calc(79.04% + 0.39px)", "calc(17.45% - 0.43px)", 158.11,  True),
    ("2691", "v7",  233.824, "calc(75.52% + 0.34px)", "calc(13.93% - 0.48px)", 184.09,  False),
    ("2692", "v8",  129.903, "calc(72.01% + 0.29px)", "calc(24.48% - 0.34px)", 236.05,  True),
    ("2693", "v9",  181.863, "calc(68.49% + 0.25px)", "calc(27.99% - 0.29px)", 210.07,  False),
    ("2694", "v10", 181.863, "calc(64.97% + 0.2px)",  "calc(31.51% - 0.25px)", 210.07,  True),
    ("2695", "v11", 78,      "calc(22.77% - 0.36px)", "calc(73.71% + 0.32px)", 236.05,  False),
    ("2696", "v12", 78,      "calc(19.26% - 0.41px)", "calc(77.23% + 0.36px)", 236.05,  True),
    ("2697", "v13", 129.98,  "calc(29.81% - 0.27px)", "calc(66.67% + 0.22px)", 210.06,  False),
    ("2698", "v14", 129.98,  "calc(26.29% - 0.32px)", "calc(70.19% + 0.27px)", 210.06,  True),
    ("2699", "v15", 78,      "calc(15.74% - 0.46px)", "calc(80.74% + 0.41px)", 184.05,  False),
    ("2700", "v16", 78,      "calc(12.22% - 0.5px)",  "calc(84.26% + 0.46px)", 184.05,  True),
    ("2701", "v17", 78,      "calc(1.66% - 0.64px)",  "calc(94.82% + 0.6px)",  210.05,  True),
    ("2702", "v18", 181.98,  "calc(5.18% - 0.6px)",   "calc(91.3% + 0.55px)",  80.06,   True),
    ("2703", "v19", 51.961,  "calc(79.04% + 0.39px)", "calc(13.93% - 0.48px)", 67.18,   False),
    ("2704", "v19", 51.961,  "calc(86.07% + 0.48px)", "calc(6.9% - 0.57px)",   15.22,   False),
    ("2705", "v19", 51.961,  "calc(75.52% + 0.34px)", "calc(17.45% - 0.43px)", 145.12,  False),
    ("2706", "v19", 51.961,  "calc(72.01% + 0.29px)", "calc(20.96% - 0.39px)", 171.10,  False),
    ("2707", "v20", 51.961,  "calc(64.97% + 0.2px)",  "calc(27.99% - 0.29px)", 119.14,  False),
    ("2708", "v21", 52,      "calc(19.26% - 0.41px)", "calc(73.71% + 0.32px)", 197.05,  False),
    ("2709", "v22", 51.98,   "calc(26.29% - 0.32px)", "calc(66.67% + 0.22px)", 145.06,  False),
    ("2710", "v23", 52,      "calc(12.22% - 0.5px)",  "calc(80.74% + 0.41px)", 145.05,  False),
    ("2711", "v23", 52,      "calc(1.69% - 0.64px)",  "calc(91.28% + 0.55px)", 171.05,  False),
    ("2712", "v24", 52.012,  "calc(5.18% - 0.6px)",   "calc(87.78% + 0.5px)",  -10.96,  False),
]

def parse_calc(expr):
    """Parse 'calc(X% +/- Ypx)' into (percent, px_offset)."""
    m = re.match(r"calc\(([\d.]+)%\s*([+\-])\s*([\d.]+)px\)", expr)
    pct = float(m.group(1)); sign = m.group(2); off = float(m.group(3))
    return pct, off if sign == '+' else -off

css_lines = [
    "/* Iso grid + bars share a fixed-size 1280x515 stage. */",
    "/* Tablet (<1280): native size, edges just clip. */",
    "/* Mobile (<768): each cluster translates inward via --mobile-shift. */",
    "section:has(.iso-stage) {",
    "  min-height: 515px;",
    "  justify-content: center;",
    "}",
    ".iso-stage {",
    "  position: absolute;",
    "  left: 50%; top: 50%;",
    "  width: 1280px; height: 515px;",
    "  transform: translate(-50%, -50%);",
    "  pointer-events: none;",
    "  z-index: -1;",
    "  --mobile-shift: 0px;",
    "}",
    ".iso-grid-bg { position: absolute; inset: 0; z-index: -1; "
    "background-image: url(iso-grid-tile.svg); background-repeat: repeat; background-position: center center; }",
    ".iso-grid-bg-cover { position: absolute; inset: 0; z-index: -2; background: white; }",
    "",
    ".bars-layer { position: absolute; inset: 0; pointer-events: none; z-index: 0; }",
    ".bars-layer .bar { position: absolute; display: block; --side-x: 0px; }",
    ".bars-layer .bar img { display: block; width: 100%; height: 100%; }",
    ".bars-layer .bar.flip { transform: translate(calc(-50% + var(--side-x)), -50%) scaleX(-1); }",
    ".bars-layer .bar:not(.flip) { transform: translate(calc(-50% + var(--side-x)), -50%); }",
    ".bars-layer .bar-left { --side-x: var(--mobile-shift, 0px); }",
    ".bars-layer .bar-right { --side-x: calc(-1 * var(--mobile-shift, 0px)); }",
    "",
    "/* Mobile: pull both clusters inward so partial cubes show on each edge */",
    "@media (max-width: 767px) {",
    "  .iso-stage { --mobile-shift: 320px; }",
    "}",
    "",
]

# Compute grid background-position offset so a tile diamond center coincides with
# a chosen reference bar's top-rhombus center. The grid then aligns to the bars
# without moving any bar (preserving cube seams).
REF_BAR = "2712"  # leftmost column's top rhombus
ref = next(b for b in BARS if b[0] == REF_BAR)
_, _, _, lexpr, rexpr, tcenter, _ = ref
lpct, loff = parse_calc(lexpr)
rpct, roff = parse_calc(rexpr)
ref_cx = (lpct * W_REF / 100 + loff - (rpct * W_REF / 100 + roff)) / 2
ref_cy = tcenter

def _wrap(v, period):
    v = v % period
    return v - period if v > period / 2 else v

# Want a tile diamond center (45 + 90n + Px, 26 + 52m + Py) = (ref_cx, ref_cy)
# Px = ref_cx - 45 - 90n; minimise |Px| via wrap mod 180 (tile width).
GRID_PX = _wrap(ref_cx - 45, 180)
# Shift grid Y by +26 so the dash-line intersections land on the rhombus's
# top AND bottom corners (instead of the rhombus center).
GRID_PY = _wrap(ref_cy, 104)

# Override iso-grid-bg with the computed offset so the lattice phases up with bars.
new_grid_rule = (
    ".iso-grid-bg { position: absolute; inset: 0; z-index: -1; "
    "background-image: url(iso-grid-tile.svg); background-repeat: repeat; "
    f"background-position: calc(50% + {GRID_PX:.3f}px) calc(50% + {GRID_PY:.3f}px); }}"
)
for i, line in enumerate(css_lines):
    if line.startswith(".iso-grid-bg "):
        css_lines[i] = new_grid_rule
        break
print(f"grid offset to align ref bar {REF_BAR}: ({GRID_PX:.3f}, {GRID_PY:.3f})")

html_parts = ['<div class="bars-layer" aria-hidden="true">']
for cls, svg, h, lexpr, rexpr, tcenter, flip in BARS:
    lpct, loff = parse_calc(lexpr)
    rpct, roff = parse_calc(rexpr)
    L = lpct * W_REF / 100 + loff
    R = rpct * W_REF / 100 + roff
    bar_w = W_REF - L - R
    cx = (L - R) / 2  # bar center x relative to section center; left as-is
    flip_cls = " flip" if flip else ""
    side_cls = " bar-left" if cx < 0 else " bar-right"
    css_lines.append(
        f".bar-{cls} {{ width: {bar_w:.3f}px; height: {h}px; "
        f"left: calc(50% + {cx:.3f}px); top: calc(50% + {tcenter}px); }}"
    )
    html_parts.append(
        f'<span class="bar bar-{cls}{flip_cls}{side_cls}"><img src="assets/figma/{svg}.svg" alt=""></span>'
    )
html_parts.append("</div>")

(BASE / "assets" / "bars.css").write_text("\n".join(css_lines) + "\n", encoding="utf-8")
(BASE / "_bars.html").write_text("\n".join(html_parts), encoding="utf-8")
print("wrote bars.css; bars:", len(BARS))
