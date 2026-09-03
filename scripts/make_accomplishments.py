import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svg_common import *

W, H = 880, 300

items = [
    ("Monolith \u2192 Microservices", "One legacy app, split, containerised, and shipped via CI/CD."),
    ("98% Delivered", "Encrypted docs, automated reporting, multi-stage approvals. Solo build."),
    ("300-Mark IoT Build", "Ingestion, mesh, and dashboard, wired as one system."),
    ("Grows Its Own Data", "A hydroponic tower that watches itself and adjusts."),
]

svg = [svg_open(W, H)]
svg.append(card_frame(W, H))
svg.append(corner_brackets(W, H))
svg.append(section_label("Accomplishments", W/2, 46, size=13, spacing="5px"))

cell_w, cell_h = 396, 96
gap_x, gap_y = 24, 20
start_x, start_y = (W - (cell_w*2 + gap_x)) / 2, 66

def wrap(text, max_chars):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

for i, (title, desc) in enumerate(items):
    col, row = i % 2, i // 2
    x = start_x + col * (cell_w + gap_x)
    y = start_y + row * (cell_h + gap_y)
    svg.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="#0f1626" stroke="{BORDER}" stroke-width="1" rx="6"/>')
    svg.append(f'<rect x="{x}" y="{y+10}" width="3" height="{cell_h-20}" fill="{ACCENT}"/>')
    tx = x + 22
    svg.append(f'<text x="{tx}" y="{y+32}" font-family="{SANS}" font-size="16" font-weight="700" fill="{TEXT_PRIMARY}">{title}</text>')
    lines = wrap(desc, 44)
    for li, line in enumerate(lines[:2]):
        svg.append(f'<text x="{tx}" y="{y+56 + li*20}" font-family="{SANS}" font-size="12.5" fill="{TEXT_SECONDARY}">{line}</text>')

svg.append(svg_close())

out = "\n".join(svg)
path = os.path.join(os.path.dirname(__file__), "..", "assets", "accomplishments.svg")
with open(path, "w") as f:
    f.write(out)
print("wrote", path)
