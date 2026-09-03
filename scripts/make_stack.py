import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from term_common import *

groups = [
    ("mobile", ["Kotlin", "Java", "React Native"]),
    ("backend", ["C#", ".NET"]),
    ("cloud", ["Azure", "Firebase", "Docker", "DigitalOcean"]),
    ("data", ["SQL Server"]),
    ("ci", ["GitHub Actions"]),
]

KEY = ACCENT
STR = "#c9d4e0"
PUNC = TEXT_SECONDARY

row_h = 24
H = 66 + 20 + len(groups) * row_h + 20
svg = panel(H)

svg.append(prompt_line(28, 44, "cat stack.json"))

y = 78
svg.append(out_line(28, y, "{", color=PUNC, size=14))
y += row_h
for i, (key, vals) in enumerate(groups):
    comma = "," if i < len(groups) - 1 else ""
    vals_str = ", ".join(f'<tspan fill="{STR}">&quot;{v}&quot;</tspan>' for v in vals)
    line = (
        f'<text x="52" y="{y}" font-family="{MONO}" font-size="14">'
        f'<tspan fill="{KEY}">&quot;{key}&quot;</tspan>'
        f'<tspan fill="{PUNC}">: [</tspan>'
        f'{vals_str}'
        f'<tspan fill="{PUNC}">]{comma}</tspan>'
        f'</text>'
    )
    svg.append(line)
    y += row_h
svg.append(out_line(28, y, "}", color=PUNC, size=14))

svg.append(svg_close())
out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "t3_stack.svg")
with open(out_path, "w") as f:
    f.write("\n".join(svg))
print("wrote", out_path, "H=", H)
