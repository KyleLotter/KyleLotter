import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svg_common import *

W, H = 880, 120

svg = [svg_open(W, H)]
svg.append(card_frame(W, H))
svg.append(corner_brackets(W, H))
svg.append(section_label("Connect", W/2, 42, size=13, spacing="5px"))

box_w, box_h = 300, 48
x = (W - box_w) / 2
y = 58

svg.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="8" fill="#0f1626" stroke="{ACCENT_DIM}" stroke-width="1.2"/>')
svg.append(f'<rect x="{x+16}" y="{y+12}" width="24" height="24" rx="5" fill="{ACCENT}"/>')
svg.append(f'<text x="{x+28}" y="{y+29}" font-family="{SANS}" font-size="14" font-weight="700" fill="{CARD_BG}" text-anchor="middle">in</text>')
svg.append(f'<text x="{x+52}" y="{y+20}" font-family="{SANS}" font-size="10.5" font-weight="600" fill="{TEXT_SECONDARY}" letter-spacing="1.5px">LINKEDIN</text>')
svg.append(f'<text x="{x+52}" y="{y+36}" font-family="{MONO}" font-size="13" fill="{TEXT_PRIMARY}">in/kyle-lotter</text>')

svg.append(svg_close())

out = "\n".join(svg)
path = os.path.join(os.path.dirname(__file__), "..", "assets", "connect.svg")
with open(path, "w") as f:
    f.write(out)
print("wrote", path)
