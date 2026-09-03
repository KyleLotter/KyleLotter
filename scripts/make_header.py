import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from term_common import *

H = 158
svg = panel(H, top=True)

for i, cx in enumerate([34, 54, 74]):
    svg.append(f'<rect x="{cx}" y="22" width="10" height="10" rx="2" fill="{BORDER}"/>')
svg.append(f'<text x="{W/2}" y="31" font-family="{MONO}" font-size="12" fill="{TEXT_SECONDARY}" text-anchor="middle">kyle@dev &#8212; zsh</text>')
svg.append(f'<line x1="0" y1="46" x2="{W}" y2="46" stroke="{BORDER}" stroke-width="1"/>')

svg.append(prompt_line(28, 78, "whoami"))
svg.append(out_line(28, 106, "Kyle Lotter &#8212; full-stack developer who ships systems, not just screens.", color=TEXT_PRIMARY, size=15))
svg.append(out_line(28, 132, "focus: Android &#183; .NET / Azure &#183; IoT Systems", color=ACCENT, size=13.5))

svg.append(svg_close())
out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "t1_header.svg")
with open(out_path, "w") as f:
    f.write("\n".join(svg))
print("wrote", out_path)
