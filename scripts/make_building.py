import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svg_common import *

W, H = 880, 140

svg = [svg_open(W, H)]
svg.append(card_frame(W, H))
svg.append(corner_brackets(W, H))
svg.append(section_label("Currently Exploring", W/2, 44, size=13, spacing="5px"))

svg.append(f'<rect x="60" y="64" width="3" height="50" fill="{ACCENT}"/>')
line1 = "Cloud-native architecture and IoT systems right now, with a growing pull"
line2 = "toward where secure backend engineering meets embedded hardware."
svg.append(f'<text x="84" y="86" font-family="{SANS}" font-size="15" fill="{TEXT_PRIMARY}">{line1}</text>')
svg.append(f'<text x="84" y="112" font-family="{SANS}" font-size="15" fill="{TEXT_PRIMARY}">{line2}</text>')

svg.append(svg_close())

out = "\n".join(svg)
path = os.path.join(os.path.dirname(__file__), "..", "assets", "building.svg")
with open(path, "w") as f:
    f.write(out)
print("wrote", path)
