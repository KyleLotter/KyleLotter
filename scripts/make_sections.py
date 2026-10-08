#!/usr/bin/env python3
"""Generates the journey and projects graphics, in a light and a dark version.

Run:  python3 scripts/make_sections.py
No dependencies. System fonts only, transparent background, colours from THEMES.
"""
import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_map import THEMES, contours  # noqa: E402

W = 1000


def wrap(text, width):
    return textwrap.wrap(text, width=width, break_long_words=False)


def frame(t, h, inner, title, desc, seed):
    css = """
.mono{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace}
.serif{font-family:Georgia,"Times New Roman","DejaVu Serif",serif}
.tiny{font-size:11px;fill:%s;letter-spacing:2.2px}
.body{font-size:13px;fill:%s}
""" % (t["muted"], t["muted"])
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img">' % (W, h, W, h),
         '<title>%s</title><desc>%s</desc>' % (escape(title), escape(desc)),
         '<style>%s</style>' % css,
         '<defs><clipPath id="c"><rect width="%d" height="%d" rx="16"/></clipPath></defs>' % (W, h),
         '<g clip-path="url(#c)">']
    o += contours(t, 985, h + 30, 7, 34, 50, seed)
    o += contours(t, 20, h + 50, 4, 34, 40, seed + 5)
    o.append('</g>')
    o.append('<rect x="0.5" y="0.5" width="%d" height="%d" rx="16" fill="none" stroke="%s"/>' % (W - 1, h - 1, t["edge"]))
    o += inner
    o.append('</svg>')
    return "\n".join(o)


# Journey ------------------------------------------------------------------
YEARS = [
    ("2023", "HTML, Kotlin and React Native",
     "A skills-training website, a wildlife conservation site, native Kotlin Android apps and a React Native book tracker."),
    ("2024", "Java",
     "A unit-tested task manager, unit-tested labs, pet shop and bank apps."),
    ("2025", "C# and Azure",
     "A venue booking system, a security awareness chatbot, a unit-tested student manager, an online shop and an inventory manager."),
    ("2026", "Everything, together",
     "A Docker multi-container lab, Decorator and Strategy pattern exercises, a live currency calculator, Emeris Kotlin training and the Smart Hydro build."),
]


def journey(t):
    text, muted, track, accent = t["text"], t["muted"], t["track"], t["accent"]
    xs = [130, 372, 614, 856]
    ly = 128
    o = ['<text class="mono tiny" x="56" y="50">THE JOURNEY SO FAR</text>',
         '<line x1="56" y1="%d" x2="944" y2="%d" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % (ly, ly, track)]
    maxlines = 0
    for i, (x, (yr, title, body)) in enumerate(zip(xs, YEARS)):
        last = i == len(YEARS) - 1
        col = accent if last else text
        o.append('<text class="serif" x="%d" y="%d" font-size="38" text-anchor="middle" fill="%s">%s</text>' % (x, ly - 30, col, yr))
        o.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (x, ly, 11 if last else 8, col))
        tl = wrap(title, 22)
        o.append('<text class="mono" x="%d" y="%d" font-size="13" font-weight="700" text-anchor="middle" fill="%s">%s</text>'
                 % (x, ly + 46, text, ''.join('<tspan x="%d" dy="%s">%s</tspan>' % (x, 0 if k == 0 else 17, escape(s)) for k, s in enumerate(tl))))
        body_y = ly + 46 + (len(tl) - 1) * 17 + 28
        lines = wrap(body, 27)
        maxlines = max(maxlines, len(lines) + len(tl) - 1)
        for j, ln in enumerate(lines):
            o.append('<text class="mono body" x="%d" y="%d" text-anchor="middle">%s</text>' % (x, body_y + j * 18, escape(ln)))
    h = ly + 46 + 28 + 18 * (maxlines + 1) + 36
    return frame(t, h, o, "The journey so far", "Four years of study, 2023 to 2026, and what was built each year", 27)


# Projects -----------------------------------------------------------------
PROJECTS = [
    ("Smart Hydro", "Hydroponics monitoring and dosing for a real client (Emeris), live on Azure. My work was mainly the Android app, the MVC web app and the API.",
     "Kotlin, Compose, Room, ASP.NET Core, Azure, Neon PostgreSQL, ESP32", True),
    ("PiggyPromise", "Personal budgeting app with charts.", "Kotlin, Compose, Firebase, MPAndroidChart, GitHub Actions", False),
    ("Odyssey", "Travel app with maps and a backend.", "Android Compose, Mapbox, Firebase Auth and Storage, ASP.NET", False),
    ("Smart-X", "Real-time web platform.", "React, TypeScript, ASP.NET Core, EF Core, SignalR, Docker Compose", False),
    ("TechMove", "Logistics web app and API with 34 unit tests.", "ASP.NET MVC, Web API, Docker, GitHub Actions, DigitalOcean", False),
    ("HustleHub+", "Marketplace for small businesses.", "React, TypeScript, Express, MongoDB, JWT, HTTPS", False),
    ("Noble & Co.", "Cloud-native storefront.", "Azure Table, Blob, Queue and Functions", False),
    ("CMCS", "Claims system with encrypted documents.", "ASP.NET Core, AES, QuestPDF", False),
    ("School Library", "Library management desktop app.", ".NET MAUI, EF Core, SQLite", False),
]


def projects(t):
    text, muted, track, accent = t["text"], t["muted"], t["track"], t["accent"]
    x = 74
    y = 84
    o = ['<text class="mono tiny" x="56" y="50">SELECTED WORK</text>',
         '<text class="mono tiny" x="640" y="50">BUILT WITH</text>']
    first_y = y
    stops = []
    for name, what, stack, flag in PROJECTS:
        a, b = wrap(what, 52), wrap(stack, 38)
        n = max(len(a) + 1, len(b))
        hh = n * 20 + 34
        stops.append((y, name, a, b, flag))
        y += hh
    last_y = stops[-1][0]
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % (x, first_y, x, last_y, track))
    for sy, name, a, b, flag in stops:
        col = accent if flag else text
        o.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (x, sy, 10 if flag else 7.5, col))
        o.append('<text class="serif" x="108" y="%d" font-size="21" fill="%s">%s</text>' % (sy + 7, text, escape(name)))
        if flag:
            o.append('<text class="mono tiny" x="%d" y="%d" style="fill:%s">FLAGSHIP</text>' % (108 + 14 + len(name) * 11, sy + 5, accent))
        for j, ln in enumerate(a):
            o.append('<text class="serif" x="108" y="%d" font-size="15" font-style="italic" fill="%s">%s</text>' % (sy + 30 + j * 20, muted, escape(ln)))
        for j, ln in enumerate(b):
            o.append('<text class="mono body" x="640" y="%d">%s</text>' % (sy + 6 + j * 18, escape(ln)))
    h = last_y + 20 * (len(stops[-1][2]) + 1) + 60
    return frame(t, h, o, "Selected work", "Nine projects with what each is and what it is built with", 21)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        (out / ("journey-%s.svg" % name)).write_text(journey(theme), encoding="utf-8")
        (out / ("projects-%s.svg" % name)).write_text(projects(theme), encoding="utf-8")
    print("wrote 4 files to", out)
