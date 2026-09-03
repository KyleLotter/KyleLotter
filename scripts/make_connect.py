import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from term_common import *

H = 130
svg = panel(H, bottom=True)

svg.append(prompt_line(28, 44, "cat connect.txt"))
svg.append(out_line(28, 72, "linkedin: in/kyle-lotter", color=TEXT_PRIMARY, size=14.5))

y2 = 104
svg.append(
    f'<text x="28" y="{y2}" font-family="{MONO}" font-size="14.5">'
    f'<tspan fill="{ACCENT}">kyle@dev</tspan>'
    f'<tspan fill="{TEXT_SECONDARY}">:~$ </tspan>'
    f'</text>'
)
svg.append(
    f'<rect x="136" y="{y2-13}" width="8" height="16" fill="{ACCENT}">'
    f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.4;0.5;0.9;1" dur="1.1s" repeatCount="indefinite"/>'
    f'</rect>'
)

svg.append(svg_close())
out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "t6_connect.svg")
with open(out_path, "w") as f:
    f.write("\n".join(svg))
print("wrote", out_path)
