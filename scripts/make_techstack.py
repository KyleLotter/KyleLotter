import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svg_common import *

W = 880

items = [
    "C#", ".NET", "Kotlin", "Java", "React Native",
    "Azure", "Firebase", "Docker", "DigitalOcean", "SQL Server", "GitHub Actions",
]

pad_x = 18
font_size = 13.5
char_w = 7.6
pill_h = 32
gap = 10
max_row_w = W - 2*40

def pill_width(text):
    return int(len(text) * char_w) + pad_x*2

rows = []
cur_row, cur_w = [], 0
for it in items:
    pw = pill_width(it)
    if cur_row and cur_w + gap + pw > max_row_w:
        rows.append(cur_row)
        cur_row, cur_w = [], 0
    cur_row.append((it, pw))
    cur_w += pw + gap
if cur_row:
    rows.append(cur_row)

row_h = pill_h + 14
H = 74 + len(rows) * row_h

svg = [svg_open(W, H)]
svg.append(card_frame(W, H))
svg.append(corner_brackets(W, H))
svg.append(section_label("Tech Stack", W/2, 46, size=13, spacing="5px"))

start_y = 62
for ri, row in enumerate(rows):
    row_w = sum(pw for _, pw in row) + gap*(len(row)-1)
    x = (W - row_w) / 2
    y = start_y + ri * row_h
    for text, pw in row:
        svg.append(f'<rect x="{x}" y="{y}" width="{pw}" height="{pill_h}" rx="16" fill="#0f1626" stroke="{ACCENT_DIM}" stroke-width="1.2"/>')
        svg.append(f'<text x="{x+pw/2}" y="{y+pill_h/2+4.5}" font-family="{MONO}" font-size="{font_size}" fill="{ACCENT}" text-anchor="middle">{text}</text>')
        x += pw + gap

svg.append(svg_close())

out = "\n".join(svg)
path = os.path.join(os.path.dirname(__file__), "..", "assets", "techstack.svg")
with open(path, "w") as f:
    f.write(out)
print("wrote", path, "H=", H)
