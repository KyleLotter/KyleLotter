import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from term_common import *

items = [
    ("Monolith &#8594; Microservices", "split, containerised, shipped via CI/CD"),
    ("98% Delivered", "encrypted docs, automated reporting, solo build"),
    ("300-Mark IoT Build", "ingestion, mesh, dashboard as one system"),
    ("Grows Its Own Data", "a hydroponic tower that watches itself"),
]

row_h = 40
H = 66 + len(items) * row_h + 20
svg = panel(H)

svg.append(prompt_line(28, 44, "cat accomplishments.log"))

y = 78
for title, desc in items:
    svg.append(out_line(28, y, "[&#10003;]", color=ACCENT, size=13.5))
    svg.append(out_line(66, y, title, color=TEXT_PRIMARY, size=14.5, weight="600"))
    svg.append(out_line(66, y + 19, desc, color=TEXT_SECONDARY, size=12.5))
    y += row_h

svg.append(svg_close())
out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "t2_accomplishments.svg")
with open(out_path, "w") as f:
    f.write("\n".join(svg))
print("wrote", out_path, "H=", H)
