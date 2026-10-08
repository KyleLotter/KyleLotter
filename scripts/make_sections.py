#!/usr/bin/env python3
"""Generates the dropdown panels in assets/sections/ for the profile README.

Each section has a slim header (shown as the dropdown summary) and a body panel.
Run:  python3 scripts/make_sections.py
No dependencies. System fonts only, so GitHub renders them as is.
"""
import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_map import (BG, PANEL, BONE, SOFT, TAUPE, RUST, COPPER, MOSS, OCHRE,  # noqa: E402
                      HEATHER, ROSE, DUST, contours)

W = 1000
CSS = """
.mono{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace}
.serif{font-family:Georgia,"Times New Roman","DejaVu Serif",serif}
.tiny{font-size:11px;fill:%s;letter-spacing:2.2px}
.body{font-size:13px;fill:%s}
.bold{font-weight:700}
""" % (SOFT, BONE)


def wrap(text, width):
    return textwrap.wrap(text, width=width, break_long_words=False)


def frame(h, inner, title, desc, art=True, seed=3):
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img">' % (W, h, W, h),
         '<title>%s</title><desc>%s</desc>' % (escape(title), escape(desc)),
         '<style>%s</style>' % CSS,
         '<defs><clipPath id="c"><rect width="%d" height="%d" rx="16"/></clipPath></defs>' % (W, h),
         '<rect width="%d" height="%d" rx="16" fill="%s"/>' % (W, h, BG)]
    if art:
        o.append('<g clip-path="url(#c)">')
        o += contours(980, h + 40, 8, 36, 50, seed)
        o += contours(30, h + 60, 5, 34, 40, seed + 5)
        o.append('</g>')
    o.append('<rect x="0.5" y="0.5" width="%d" height="%d" rx="16" fill="none" stroke="%s"/>' % (W - 1, h - 1, PANEL))
    o += inner
    o.append('</svg>')
    return "\n".join(o)


def header(num, title, colour, hint):
    h = 76
    inner = [
        '<g clip-path="url(#c)"><rect x="0" y="0" width="10" height="%d" fill="%s"/></g>' % (h, colour),
        '<line x1="10" y1="38" x2="52" y2="38" stroke="%s" stroke-width="8" stroke-linecap="round"/>' % colour,
        '<circle cx="52" cy="38" r="9" fill="%s" stroke="%s" stroke-width="4"/>' % (BG, BONE),
        '<text class="mono tiny" x="84" y="32" style="fill:%s">STOP %s</text>' % (colour, num),
        '<text class="serif" x="84" y="58" font-size="26" fill="%s">%s</text>' % (BONE, escape(title)),
        '<text class="mono tiny" x="944" y="43" text-anchor="end">%s</text>' % escape(hint),
    ]
    return frame(h, inner, title, "Dropdown header, " + title, art=False)


# 1. Languages -------------------------------------------------------------
LANGS = [
    ("Kotlin", MOSS, "Jetpack Compose, Room, Retrofit, Firebase, Mapbox, MPAndroidChart"),
    ("C#", COPPER, "ASP.NET Core MVC and Web API, EF Core, SignalR, JWT, .NET MAUI, xUnit"),
    ("TypeScript + JavaScript", ROSE, "React, Vite, Node, Express, MongoDB"),
    ("Java", DUST, "Unit-tested applications and labs"),
    ("SQL", HEATHER, "SQL Server, MySQL, PostgreSQL, Oracle PL/SQL"),
    ("C + C++", OCHRE, "ESP32 firmware, LoRa, sensors and edge ML"),
    ("HTML + CSS", ROSE, "Where it all started"),
    ("Cloud + tooling", BONE, "Azure App Service, Storage and Functions, Docker Compose, GitHub Actions, Git"),
]


def languages():
    top, step = 70, 58
    h = top + step * len(LANGS) + 20
    o = ['<text class="mono tiny" x="56" y="42">LANGUAGE</text>',
         '<text class="mono tiny" x="360" y="42">STACK</text>']
    x = 82
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (x, top, x, top + step * (len(LANGS) - 1), PANEL))
    for i, (name, col, stack) in enumerate(LANGS):
        y = top + i * step
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="8" stroke-linecap="round"/>' % (x - 26, y, x + 26, y, col))
        o.append('<circle cx="%d" cy="%d" r="8" fill="%s" stroke="%s" stroke-width="3.5"/>' % (x, y, BG, BONE))
        o.append('<text class="serif" x="130" y="%d" font-size="21" fill="%s">%s</text>' % (y + 7, BONE, escape(name)))
        for j, ln in enumerate(wrap(stack, 76)):
            o.append('<text class="mono body" x="360" y="%d">%s</text>' % (y + 5 + j * 17, escape(ln)))
    return frame(h, o, "Languages and stacks", "Languages with the frameworks used in each", seed=8)


# 2. Skills ----------------------------------------------------------------
SKILLS = [
    ("ACCESSIBILITY", "MOBILE", MOSS,
     "TalkBack support, read-aloud and high-contrast modes in a production Android app."),
    ("OFFLINE-FIRST", "MOBILE", MOSS,
     "Room-backed local storage that syncs when the connection returns, plus an offline hotspot relay and box pairing for hardware."),
    ("SECURITY", "WEB + .NET", COPPER,
     "OTP login with rate limiting, security-header middleware, JWT auth, HTTPS and AES document encryption."),
    ("CLOUD", "CLOUD", BONE,
     "Azure App Service in South Africa North, Neon PostgreSQL, containerised services and CI pipelines."),
    ("DATA DESIGN", "DATA", HEATHER,
     "ERDs and data models, relational and document schemas, PL/SQL."),
    ("RESEARCH + DESIGN", "DESIGN", HEATHER,
     "Personas, double diamond, user-centred design and Figma prototypes."),
    ("TEACHING", "TEACHING", DUST,
     "Contract tutor at Emeris across 8 modules, class representative, technical documentation."),
]


def skills():
    y = 60
    o = ['<text class="mono tiny" x="56" y="42">SKILL</text>',
         '<text class="mono tiny" x="330" y="42">WHAT IT LOOKS LIKE IN PRACTICE</text>']
    for name, line, col, text in SKILLS:
        lines = wrap(text, 68)
        hh = max(66, len(lines) * 19 + 26)
        o.append('<rect x="56" y="%d" width="6" height="%d" rx="3" fill="%s"/>' % (y + 6, hh - 18, col))
        o.append('<text class="mono bold" x="78" y="%d" font-size="14" fill="%s">%s</text>' % (y + 22, col, escape(name)))
        o.append('<text class="mono tiny" x="78" y="%d">%s LINE</text>' % (y + 40, escape(line)))
        for j, ln in enumerate(lines):
            o.append('<text class="mono body" x="330" y="%d">%s</text>' % (y + 22 + j * 19, escape(ln)))
        y += hh
        o.append('<line x1="56" y1="%d" x2="944" y2="%d" stroke="%s" stroke-width="1"/>' % (y - 4, y - 4, PANEL))
    return frame(y + 24, o, "Skills in depth", "Seven skills with how each shows up in real work", seed=14)


# 3. Projects --------------------------------------------------------------
PROJECTS = [
    ("Smart Hydro", OCHRE, "Hydroponics monitoring and dosing for a real client (Emeris), live on Azure. My work was mainly the Android app, MVC web app and API.",
     "Kotlin, Compose, Room, ASP.NET Core, Azure, Neon PostgreSQL, ESP32"),
    ("PiggyPromise", MOSS, "Personal budgeting app with charts.", "Kotlin, Compose, Firebase, MPAndroidChart, GitHub Actions"),
    ("Odyssey", MOSS, "Travel app with maps and a backend.", "Android Compose, Mapbox, Firebase Auth and Storage, ASP.NET"),
    ("Smart-X", COPPER, "Real-time web platform.", "React, TypeScript, ASP.NET Core, EF Core, SignalR, Docker Compose"),
    ("TechMove", COPPER, "Logistics web app and API with 34 unit tests.", "ASP.NET MVC, Web API, Docker, GitHub Actions, DigitalOcean"),
    ("HustleHub+", ROSE, "Marketplace for small businesses.", "React, TypeScript, Express, MongoDB, JWT, HTTPS"),
    ("Noble & Co.", BONE, "Cloud-native storefront.", "Azure Table, Blob, Queue and Functions"),
    ("CMCS", COPPER, "Claims system with encrypted documents.", "ASP.NET Core, AES, QuestPDF"),
    ("School Library", COPPER, "Library management desktop app.", ".NET MAUI, EF Core, SQLite"),
]


def projects():
    y = 62
    o = ['<text class="mono tiny" x="56" y="42">PROJECT</text>',
         '<text class="mono tiny" x="270" y="42">WHAT IT IS</text>',
         '<text class="mono tiny" x="660" y="42">BUILT WITH</text>']
    for name, col, what, stack in PROJECTS:
        a, b = wrap(what, 44), wrap(stack, 36)
        n = max(len(a), len(b), 1)
        hh = n * 18 + 26
        o.append('<circle cx="64" cy="%d" r="6" fill="%s"/>' % (y + 15, col))
        o.append('<text class="serif" x="82" y="%d" font-size="19" fill="%s">%s</text>' % (y + 21, BONE, escape(name)))
        for j, ln in enumerate(a):
            o.append('<text class="mono body" x="270" y="%d">%s</text>' % (y + 19 + j * 18, escape(ln)))
        for j, ln in enumerate(b):
            o.append('<text class="mono body" x="660" y="%d" style="fill:%s">%s</text>' % (y + 19 + j * 18, SOFT, escape(ln)))
        y += hh
        o.append('<line x1="56" y1="%d" x2="944" y2="%d" stroke="%s" stroke-width="1"/>' % (y - 5, y - 5, PANEL))
    return frame(y + 24, o, "Projects", "Nine projects with what each is and what it is built with", seed=21)


# 4. Timeline --------------------------------------------------------------
YEARS = [
    ("2023", MOSS, "HTML, Kotlin and React Native",
     "A skills-training website, a wildlife conservation site, native Kotlin Android apps and a React Native book tracker."),
    ("2024", OCHRE, "Java",
     "A unit-tested task manager, unit-tested labs, pet shop and bank apps."),
    ("2025", COPPER, "C# and Azure",
     "A venue booking system, a security awareness chatbot, a unit-tested student manager, an online shop and an inventory manager."),
    ("2026", ROSE, "Everything, together",
     "A Docker multi-container lab, Decorator and Strategy pattern exercises, a live currency calculator, Emeris Kotlin training and the Smart Hydro build."),
]


def timeline():
    xs = [130, 372, 614, 856]
    ly = 120
    o = ['<line x1="56" y1="%d" x2="944" y2="%d" stroke="%s" stroke-width="8" stroke-linecap="round"/>' % (ly, ly, BONE)]
    maxlines = 0
    for x, (yr, col, title, text) in zip(xs, YEARS):
        o.append('<text class="serif" x="%d" y="%d" font-size="38" text-anchor="middle" fill="%s">%s</text>' % (x, ly - 30, col, yr))
        o.append('<circle cx="%d" cy="%d" r="11" fill="%s" stroke="%s" stroke-width="5"/>' % (x, ly, BG, col))
        o.append('<text class="mono bold" x="%d" y="%d" font-size="13" text-anchor="middle" fill="%s">' % (x, ly + 46, BONE))
        tl = wrap(title, 22)
        o.append(''.join('<tspan x="%d" dy="%s">%s</tspan>' % (x, 0 if i == 0 else 17, escape(t)) for i, t in enumerate(tl)))
        o.append('</text>')
        body_y = ly + 46 + (len(tl) - 1) * 17 + 28
        lines = wrap(text, 27)
        maxlines = max(maxlines, len(lines) + (len(tl) - 1) * 1)
        for j, ln in enumerate(lines):
            o.append('<text class="mono body" x="%d" y="%d" text-anchor="middle" style="fill:%s">%s</text>' % (x, body_y + j * 18, SOFT, escape(ln)))
    h = ly + 46 + 28 + 18 * (maxlines + 1) + 36
    return frame(h, o, "Timeline", "Four years of study, 2023 to 2026, with what was built each year", seed=27)


# 5. Beyond the code --------------------------------------------------------
BEYOND = [
    ("DATA", HEATHER, "ERDs and data models, MySQL and MongoDB design, Oracle PL/SQL."),
    ("NETWORKS", OCHRE, "WAN design and network labs in Cisco Packet Tracer."),
    ("DESIGN", ROSE, "Personas and double diamond, a Figma landing page, UCD for DealFinder."),
    ("ARCHITECTURE + PLANNING", BONE, "Cloud architecture diagrams, a change management plan, WBS and project planning."),
]


def beyond():
    o = []
    pw, ph, gap = 432, 122, 24
    for i, (name, col, text) in enumerate(BEYOND):
        x = 56 + (i % 2) * (pw + gap)
        y = 40 + (i // 2) * (ph + gap)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" opacity="0.75"/>' % (x, y, pw, ph, PANEL))
        o.append('<rect x="%d" y="%d" width="6" height="%d" rx="3" fill="%s"/>' % (x + 16, y + 18, ph - 36, col))
        o.append('<text class="mono bold" x="%d" y="%d" font-size="13" fill="%s" style="letter-spacing:1.6px">%s</text>' % (x + 36, y + 34, col, escape(name)))
        for j, ln in enumerate(wrap(text, 44)):
            o.append('<text class="mono body" x="%d" y="%d">%s</text>' % (x + 36, y + 62 + j * 19, escape(ln)))
    h = 40 + 2 * ph + gap + 40
    return frame(h, o, "Beyond the code", "Data, networks, design and planning work outside programming", seed=33)


SECTIONS = [
    ("languages", "Languages and stacks", MOSS, languages),
    ("skills", "Skills in depth", COPPER, skills),
    ("projects", "Projects", OCHRE, projects),
    ("timeline", "Timeline", ROSE, timeline),
    ("beyond", "Beyond the code", HEATHER, beyond),
]

if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "sections"
    out.mkdir(parents=True, exist_ok=True)
    for i, (key, title, col, fn) in enumerate(SECTIONS, 1):
        (out / ("%s-head.svg" % key)).write_text(header("%02d" % i, title, col, "%02d / %02d" % (i, len(SECTIONS))), encoding="utf-8")
        (out / ("%s.svg" % key)).write_text(fn(), encoding="utf-8")
    print("wrote", len(SECTIONS) * 2, "files to", out)
