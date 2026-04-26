import json, re, os, pathlib

BASE = pathlib.Path(r"C:\HuggingFace\Huggy model\replica")
with open(BASE / "extract.json", "r", encoding="utf-8") as f:
    data = json.load(f)

N, H, S = data["N"], data["H"], data["S"]

# Rewrite image/logo paths to local assets/
def rewrite(html):
    # logo
    html = html.replace("/front/assets/huggingface_logo-noborder.svg", "assets/huggingface_logo-noborder.svg")
    # enterprise images
    for name in ["SSO", "dark-SSO", "regions", "dark-regions", "audit-logs", "dark-audit-logs", "resource-groups", "dark-resource-groups"]:
        url = f"https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/enterprise/{name}.png"
        html = html.replace(url, f"assets/{name}.png")
    # expert images kept remote (they load from cdn)
    return html

N = rewrite(N)
H = rewrite(H)
S = rewrite(S)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Expert Support \u2013 Hugging Face</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:ital,wght@0,200;0,300;0,400;0,600;0,700;1,200;1,300;1,400;1,600;1,700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&display=swap">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="flex min-h-dvh flex-col">
{N}
<main class="flex flex-1 flex-col">
<div class="relative min-h-screen overflow-clip bg-white dark:bg-gray-950">
{H}
<section class="relative z-5 w-full border-b border-gray-200/70 px-4"><div class="relative mx-auto h-16 max-w-7xl border-x border-gray-200/70"></div></section>
{S}
</div>
</main>
</div>
</body>
</html>
"""

(BASE / "index.html").write_text(page, encoding="utf-8")
print("wrote", BASE / "index.html", len(page), "bytes")
