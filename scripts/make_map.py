#!/usr/bin/env python3
"""Generates assets/network-map.svg, the skills map that heads the profile README.

Each line is a discipline, each station is a skill, and an interchange is a skill
that serves two lines. Edit ROWS, STATIONS and LINKS below, then run
    python3 scripts/make_map.py
No dependencies. Everything is drawn from system fonts so GitHub renders it as is.
"""
import math
import random
from pathlib import Path
from xml.sax.saxutils import escape

W, H = 1000, 880

# Palette
BG = "#0d1811"
PANEL = "#1b3123"
CONTOUR_MAJOR = "#244030"
BONE = "#d9cfc1"
SOFT = "#9c8e80"
TAUPE = "#73665c"
RUST = "#693721"
COPPER = "#d07f3e"
MOSS = "#86b07c"
OCHRE = "#d6b04e"
HEATHER = "#a98fa6"
ROSE = "#c98f86"
DUST = "#b9ac9a"

TRACK_START = 200

# One horizontal track per discipline, top to bottom.
ROWS = [
    dict(key="web", name="WEB", colour=ROSE, y=270, train="-6s"),
    dict(key="net", name=".NET", colour=COPPER, y=350, train="-19s"),
    dict(key="mobile", name="MOBILE", colour=MOSS, y=430, train="-11s"),
    dict(key="iot", name="IOT", colour=OCHRE, y=510, train="-30s"),
    dict(key="cloud", name="CLOUD", colour=BONE, y=590, train="-3s"),
    dict(key="design", name="DATA + DESIGN", colour=HEATHER, y=670, train="-24s"),
    dict(key="teach", name="TEACHING", colour=DUST, y=750, dotted=True),
]

# row, x, skill, label side (A above the track, B below it)
STATIONS = [
    ("web", 250, "HTML + CSS", "A"),
    ("web", 380, "React + TS", "A"),
    ("web", 510, "Node + Express", "A"),
    ("web", 650, "MongoDB", "A"),
    ("web", 910, "Web security", "A"),

    ("net", 250, "C#", "A"),
    ("net", 380, "ASP.NET MVC", "A"),
    ("net", 650, "EF Core", "A"),

    ("mobile", 250, "Kotlin", "B"),
    ("mobile", 380, "Compose", "B"),
    ("mobile", 650, "Accessibility", "B"),
    ("mobile", 910, "Firebase", "A"),

    ("iot", 250, "ESP32", "B"),
    ("iot", 380, "LoRa", "B"),
    ("iot", 650, "Edge ML", "B"),
    ("iot", 910, "Sensors", "B"),

    ("cloud", 250, "Azure", "B"),
    ("cloud", 380, "Docker", "B"),
    ("cloud", 650, "CI/CD", "B"),

    ("design", 250, "Data models", "B"),
    ("design", 380, "SQL", "B"),
    ("design", 510, "UCD + Figma", "B"),
    ("design", 650, "Research", "B"),
    ("design", 910, "Change mgmt", "B"),

    ("teach", 250, "Tutoring", "B"),
    ("teach", 380, "Class rep", "B"),
    ("teach", 510, "Documentation", "B"),
]

# Shared skills. Two adjacent rows, the x position and the skill name.
LINKS = [
    ("web", "net", 790, "JWT auth"),
    ("net", "mobile", 510, "REST APIs"),
    ("mobile", "iot", 790, "Offline-first"),
    ("iot", "cloud", 510, "Telemetry"),
    ("cloud", "design", 790, "Cloud architecture"),
]

CSS = """
.mono{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace}
.serif{font-family:Georgia,"Times New Roman","DejaVu Serif",serif}
.st{font-size:14px;font-weight:700;fill:%s}
.tiny{font-size:11px;fill:%s;letter-spacing:2.2px}
""" % (BONE, SOFT)


def contours(cx, cy, count, step, first, seed):
    """Wobbly closed rings, like the contour lines on a topographic map."""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(3)]
    out = []
    for i in range(count):
        r = first + i * step
        pts = []
        for k in range(120):
            t = k / 120 * 2 * math.pi
            wob = (1 + 0.11 * math.sin(2 * t + ph[0] + i * 0.25)
                   + 0.07 * math.sin(3 * t + ph[1] - i * 0.18)
                   + 0.035 * math.sin(5 * t + ph[2] + i * 0.4))
            pts.append((cx + r * wob * math.cos(t), cy + r * wob * 0.82 * math.sin(t)))
        d = "M" + " L".join("%.1f %.1f" % p for p in pts) + "Z"
        major = (i % 4 == 3)
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (
            d, CONTOUR_MAJOR if major else PANEL, "1.6" if major else "1"))
    return out


def build():
    rows = {r["key"]: r for r in ROWS}

    # Track extents, from the stations and links that sit on each row.
    last_x = {}
    for key, x, _, _ in STATIONS:
        last_x[key] = max(last_x.get(key, 0), x)
    for a, b, x, _ in LINKS:
        for k in (a, b):
            last_x[k] = max(last_x.get(k, 0), x)

    o = []
    o.append('<?xml version="1.0" encoding="UTF-8"?>')
    o.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img">' % (W, H, W, H))
    o.append('<title>Kyle Lötter, skills map</title>')
    o.append('<desc>A transit-style map of Kyle Lötter\'s skills. Seven lines, Web, .NET, Mobile, IoT, Cloud, '
             'Data and design, and Teaching. Stations are skills and interchanges are skills shared by two lines.</desc>')
    o.append('<style>%s</style>' % CSS)
    o.append('<defs><clipPath id="card"><rect width="%d" height="%d" rx="16"/></clipPath></defs>' % (W, H))
    o.append('<rect width="%d" height="%d" rx="16" fill="%s"/>' % (W, H, BG))

    # Contours, clipped to the card
    o.append('<g clip-path="url(#card)">')
    o += contours(930, 900, 16, 36, 60, 4)
    o += contours(40, 910, 9, 36, 50, 11)
    o += contours(1010, 30, 5, 28, 40, 7)
    o += contours(1020, 520, 6, 30, 40, 23)
    o.append('</g>')
    o.append('<rect x="0.5" y="0.5" width="%d" height="%d" rx="16" fill="none" stroke="%s"/>' % (W - 1, H - 1, PANEL))

    # Title block
    o.append('<text class="mono tiny" x="56" y="68">SKILLS MAP</text>')
    o.append('<text class="mono tiny" x="170" y="68" style="fill:%s">REV. 10/2026</text>' % TAUPE)
    o.append('<text class="serif" x="56" y="124" font-size="52" fill="%s">Kyle Lötter</text>' % BONE)
    o.append('<text class="serif" x="58" y="156" font-size="19" font-style="italic" fill="%s">'
             'Building things that talk to each other.</text>' % SOFT)

    # How to read it, top right
    for i, line in enumerate(["Lines are the disciplines I work in.",
                              "Stations are the skills.",
                              "Interchanges are shared skills."]):
        o.append('<text class="serif" x="690" y="%d" font-size="16" font-style="italic" fill="%s">%s</text>'
                 % (70 + i * 24, SOFT, line))
    o.append('<line x1="56" y1="188" x2="944" y2="188" stroke="%s" stroke-width="1"/>' % RUST)

    # Tracks and row names
    for r in ROWS:
        y = r["y"]
        end = last_x.get(r["key"], 400) + 30
        if r.get("dotted"):
            o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="6" '
                     'stroke-linecap="round" stroke-dasharray="0.1 12"/>' % (TRACK_START + 20, y, end, y, r["colour"]))
        else:
            o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="8" stroke-linecap="round"/>'
                     % (TRACK_START, y, end, y, r["colour"]))
        o.append('<text class="mono tiny" x="56" y="%d" style="fill:%s">%s</text>' % (y + 4, r["colour"], escape(r["name"])))

    # Trains, slow and small
    for r in ROWS:
        if r.get("dotted"):
            continue
        y = r["y"]
        end = last_x.get(r["key"], 400) + 30
        o.append('<circle r="3.2" fill="%s"><animateMotion dur="46s" begin="%s" repeatCount="indefinite" '
                 'path="M%d %d L%d %d" keyPoints="0;1;0" keyTimes="0;0.5;1" calcMode="linear"/></circle>'
                 % (BG, r["train"], TRACK_START, y, end, y))

    # Plain stations and their labels
    for key, x, name, side in STATIONS:
        y = rows[key]["y"]
        o.append('<circle cx="%d" cy="%d" r="7" fill="%s" stroke="%s" stroke-width="3.5"/>' % (x, y, BG, BONE))
        ty = y - 18 if side == "A" else y + 32
        o.append('<text class="mono st" x="%d" y="%d" text-anchor="middle">%s</text>' % (x, ty, escape(name)))

    # Interchanges, drawn as a capsule joining the two rows
    for a, b, x, name in LINKS:
        y1, y2 = rows[a]["y"], rows[b]["y"]
        o.append('<rect x="%d" y="%d" width="18" height="%d" rx="9" fill="%s"/>' % (x - 9, y1 - 11, y2 - y1 + 22, BONE))
        o.append('<circle cx="%d" cy="%d" r="4.5" fill="%s"/>' % (x, y1, BG))
        o.append('<circle cx="%d" cy="%d" r="4.5" fill="%s"/>' % (x, y2, BG))
        o.append('<text class="mono st" x="%d" y="%d">%s</text>' % (x + 22, (y1 + y2) // 2 + 5, escape(name)))

    # Footer
    o.append('<line x1="56" y1="826" x2="944" y2="826" stroke="%s" stroke-width="1"/>' % RUST)
    o.append('<text class="mono tiny" x="56" y="854">GQEBERHA · SOUTH AFRICA · 33.96° S 25.60° E</text>')
    o.append('<text class="mono tiny" x="640" y="854" text-anchor="middle">GITHUB.COM/KYLELOTTER</text>')
    o.append('<text class="mono tiny" x="944" y="854" text-anchor="end">NOT TO SCALE</text>')

    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "network-map.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print("wrote", out, out.stat().st_size, "bytes")
