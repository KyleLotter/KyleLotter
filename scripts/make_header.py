import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svg_common import *

W, H = 880, 240

dots = [
    (110, 55), (150, 40), (190, 70),
    (700, 45), (740, 65), (770, 35),
    (95, 150), (760, 150),
]
lines = [
    ((110, 55), (150, 40)), ((150, 40), (190, 70)),
    ((700, 45), (740, 65)), ((740, 65), (770, 35)),
]

svg = [svg_open(W, H)]
svg.append(card_frame(W, H))
svg.append(corner_brackets(W, H))

svg.append(f'<text x="60" y="42" font-family="{MONO}" font-size="12" fill="{TEXT_SECONDARY}">kylelotter / README.md</text>')
svg.append(f'<line x1="60" y1="54" x2="{W-60}" y2="54" stroke="{BORDER}" stroke-width="1"/>')

for (x1, y1), (x2, y2) in lines:
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ACCENT_DIM}" stroke-width="1"/>')
for x, y in dots:
    svg.append(f'<circle cx="{x}" cy="{y}" r="2" fill="{ACCENT}" opacity="0.7"/>')

svg.append(
    f'<text x="{W/2}" y="118" font-family="{SANS}" font-size="38" font-weight="700" '
    f'fill="{TEXT_PRIMARY}" text-anchor="middle" letter-spacing="6px">KYLE LOTTER</text>'
)
svg.append(
    f'<text x="{W/2}" y="150" font-family="{SANS}" font-size="16" fill="{ACCENT}" '
    f'text-anchor="middle">Full-stack developer who ships systems, not just screens.</text>'
)

svg.append(f'<line x1="{W/2-70}" y1="172" x2="{W/2-14}" y2="172" stroke="{BORDER}" stroke-width="1"/>')
svg.append(f'<circle cx="{W/2}" cy="172" r="2.5" fill="{ACCENT}"/>')
svg.append(f'<line x1="{W/2+14}" y1="172" x2="{W/2+70}" y2="172" stroke="{BORDER}" stroke-width="1"/>')

svg.append(section_label("Android  ·  .NET / Azure  ·  IoT Systems", W/2, 200, size=12, color=TEXT_SECONDARY, spacing="3px"))

svg.append(svg_close())

out = "\n".join(svg)
path = os.path.join(os.path.dirname(__file__), "..", "assets", "header.svg")
with open(path, "w") as f:
    f.write(out)
print("wrote", path)
