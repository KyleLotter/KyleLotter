import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from term_common import *

H = 128
svg = panel(H)

svg.append(prompt_line(28, 44, "cat currently.md"))
svg.append(out_line(28, 74, "&gt; Cloud-native architecture and IoT systems right now, pulling toward", color=TEXT_PRIMARY, size=14))
svg.append(out_line(28, 98, "&gt; where secure backend engineering meets embedded hardware.", color=TEXT_PRIMARY, size=14))

svg.append(svg_close())
out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "t4_currently.svg")
with open(out_path, "w") as f:
    f.write("\n".join(svg))
print("wrote", out_path)
