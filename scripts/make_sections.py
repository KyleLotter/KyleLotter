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


def frame(t, h, inner, title, desc, seed, W=1000, art=True):
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
    if art:
        o += contours(t, 985, h + 30, 7, 34, 50, seed)
        o += contours(t, 20, h + 50, 4, 34, 40, seed + 5)
    o.append('</g>')
    o.append('<rect x="0.5" y="0.5" width="%d" height="%d" rx="16" fill="none" stroke="%s"/>' % (W - 1, h - 1, t["edge"]))
    o += inner
    o.append('</svg>')
    return "\n".join(o)


# Journey ------------------------------------------------------------------
YEARS = [
    ("2023", "First lines, first apps",
     "Built a skills-training site and a wildlife conservation site, then went native with Kotlin Android apps and a React Native book tracker."),
    ("2024", "Java, tested properly",
     "Learned to test what I build. Unit-tested Java applications, from a task manager to pet shop and bank apps."),
    ("2025", "C#, .NET and Azure",
     "Moved to .NET and the cloud. A venue booking system, a security awareness chatbot, an online shop and an inventory manager, with unit-tested code throughout."),
    ("2026", "Real systems, real users",
     "A live IoT hydroponics platform for a client on Azure. A real-time IoT mesh ecosystem. A travel planner with maps. A secure freelance marketplace with DevSecOps. A gamified budget tracker. A library app now used by a school. And teaching it all at Emeris."),
]


def journey(t):
    text, muted, track, accent = t["text"], t["muted"], t["track"], t["accent"]
    xs = [125, 330, 535, 790]
    widths = [24, 24, 24, 38]
    ly = 128
    o = ['<text class="mono tiny" x="56" y="50">THE JOURNEY SO FAR</text>',
         '<line x1="56" y1="%d" x2="944" y2="%d" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % (ly, ly, track)]
    maxlines = 0
    for i, (x, (yr, title, body)) in enumerate(zip(xs, YEARS)):
        last = i == len(YEARS) - 1
        col = accent if last else text
        o.append('<text class="serif" x="%d" y="%d" font-size="38" text-anchor="middle" fill="%s">%s</text>' % (x, ly - 30, col, yr))
        o.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (x, ly, 11 if last else 8, col))
        tl = wrap(title, 24)
        o.append('<text class="mono" x="%d" y="%d" font-size="13" font-weight="700" text-anchor="middle" fill="%s">%s</text>'
                 % (x, ly + 46, text, ''.join('<tspan x="%d" dy="%s">%s</tspan>' % (x, 0 if k == 0 else 17, escape(s)) for k, s in enumerate(tl))))
        body_y = ly + 46 + (len(tl) - 1) * 17 + 28
        lines = wrap(body, widths[i])
        maxlines = max(maxlines, len(lines) + len(tl) - 1)
        for j, ln in enumerate(lines):
            o.append('<text class="mono body" x="%d" y="%d" text-anchor="middle">%s</text>' % (x, body_y + j * 18, escape(ln)))
    h = ly + 46 + 28 + 18 * (maxlines + 1) + 36
    return frame(t, h, o, "The journey so far", "Four years of study, 2023 to 2026, and what was built each year", 27)


# Projects -----------------------------------------------------------------
PROJECTS = [
    ("Smart Hydro", "Live IoT hydroponics platform for a client, running on Azure.",
     "Kotlin, Compose, Room, ASP.NET Core, Azure, Neon PostgreSQL, ESP32", True),
    ("PiggyPromise", "Gamified budget tracker with charts.", "Kotlin, Compose, Firebase, MPAndroidChart, GitHub Actions", False),
    ("Odyssey", "Travel planner with maps and a backend.", "Android Compose, Mapbox, Firebase Auth and Storage, ASP.NET", False),
    ("Smart-X", "Real-time IoT mesh ecosystem.", "React, TypeScript, ASP.NET Core, EF Core, SignalR, Docker Compose", False),
    ("TechMove", "Containerised logistics platform with a Web API and CI/CD.", "ASP.NET MVC, Web API, Docker, GitHub Actions, DigitalOcean", False),
    ("HustleHub+", "Secure freelance marketplace with a DevSecOps pipeline.", "React, TypeScript, Express, MongoDB, JWT, HTTPS", False),
    ("Noble & Co.", "Cloud-native storefront.", "Azure Table, Blob, Queue and Functions", False),
    ("CMCS", "Claims system with AES-encrypted documents and PDF reports.", "ASP.NET Core, AES, QuestPDF", False),
    ("School Library", "Library management app in use at a school.", ".NET MAUI, EF Core, SQLite", False),
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


# In practice --------------------------------------------------------------
PRACTICE = [
    ("Accessibility", "TalkBack support, read-aloud, high-contrast modes and themes in a production Android app."),
    ("Offline-first", "Room-backed local storage that syncs when the connection returns, plus an offline hotspot relay and IoT box pairing."),
    ("Security", "OTP login with rate limiting, security-header middleware, JWT auth, HTTPS and AES document encryption."),
    ("Cloud", "Production deployments on Azure App Service in South Africa North with Neon PostgreSQL, containerised services and automated CI/CD."),
    ("Data and design", "ERDs and data models, relational and document schemas, PL/SQL, personas, double diamond, user-centred design and Figma prototypes."),
    ("Teaching", "Selected on academic performance as a contract tutor at Emeris across 8 modules, while serving as class representative."),
]


def practice(t):
    text, muted, accent = t["text"], t["muted"], t["accent"]
    cw, gap, top = 432, 24, 70
    o = ['<text class="mono tiny" x="56" y="44">IN PRACTICE</text>']
    y = top
    for r in range(0, len(PRACTICE), 2):
        pair = PRACTICE[r:r + 2]
        wrapped = [wrap(b, 46) for _, b in pair]
        ch = max(len(w) for w in wrapped) * 19 + 98
        for i, ((title, _), lines) in enumerate(zip(pair, wrapped)):
            x = 56 + i * (cw + gap)
            o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="none" stroke="%s" stroke-width="1.5"/>' % (x, y, cw, ch, t["edge"]))
            o.append('<rect x="%d" y="%d" width="28" height="4" rx="2" fill="%s"/>' % (x + 24, y + 26, accent))
            o.append('<text class="serif" x="%d" y="%d" font-size="22" fill="%s">%s</text>' % (x + 24, y + 62, text, escape(title)))
            for j, ln in enumerate(lines):
                o.append('<text class="mono body" x="%d" y="%d">%s</text>' % (x + 24, y + 92 + j * 19, escape(ln)))
        y += ch + gap
    h = y - gap + 40
    return frame(t, h, o, "In practice", "Accessibility, offline-first, security, cloud, data and design, and teaching", 31)


# Tools --------------------------------------------------------------------
TOOLS = [
    ("LANGUAGES", ["Kotlin", "C#", "TypeScript", "JavaScript", "Java", "SQL", "C++", "HTML", "CSS"]),
    ("MOBILE", ["Jetpack Compose", "Material 3", "Room", "Firebase", "Mapbox"]),
    ("BACKEND", ["ASP.NET Core", "EF Core", "SignalR", "Node", "Swagger", "Scalar"]),
    ("WEB", ["React", "Next.js", "Tailwind", "Bootstrap", "Vite"]),
    ("DATA", ["SQL Server", "Azure SQL", "PostgreSQL", "Supabase", "MongoDB", "Oracle PL/SQL"]),
    ("CLOUD + DEVOPS", ["Azure", "Docker", "GitHub Actions", "DigitalOcean"]),
    ("HARDWARE", ["ESP32", "Arduino IDE", "Raspberry Pi", "MQTT"]),
    ("TESTING + API", ["xUnit", "NUnit", "Postman"]),
    ("DESIGN + PLANNING", ["Figma", "Canva", "draw.io", "Excalidraw", "Lucidchart", "Notion"]),
]


def tools(t):
    text, muted, accent = t["text"], t["muted"], t["accent"]
    x0, xmax = 260, 944
    o = ['<text class="mono tiny" x="56" y="44">TOOLS</text>']
    y = 84
    for label, items in TOOLS:
        o.append('<text class="mono tiny" x="56" y="%d" style="fill:%s">%s</text>' % (y + 20, accent, escape(label)))
        x = x0
        for it in items:
            cwid = int(len(it) * 7.9 + 28)
            if x + cwid > xmax:
                x = x0
                y += 44
            o.append('<rect x="%d" y="%d" width="%d" height="32" rx="16" fill="none" stroke="%s" stroke-width="1.5"/>' % (x, y, cwid, t["edge"]))
            o.append('<text class="mono" x="%d" y="%d" font-size="13" text-anchor="middle" fill="%s">%s</text>' % (x + cwid / 2, y + 21, text, escape(it)))
            x += cwid + 10
        y += 54
    h = y + 10
    return frame(t, h, o, "Tools", "Languages, frameworks, data, cloud and design tools I use", 37, art=False)


# LinkedIn pill ------------------------------------------------------------
def linkedin(t):
    text, muted, accent = t["text"], t["muted"], t["accent"]
    w, h = 280, 56
    o = ['<rect x="1" y="1" width="%d" height="%d" rx="28" fill="none" stroke="%s" stroke-width="1.5"/>' % (w - 2, h - 2, t["edge"]),
         '<rect x="10" y="10" width="36" height="36" rx="18" fill="%s"/>' % accent,
         '<text class="mono" x="28" y="34" font-size="15" font-weight="700" text-anchor="middle" fill="#ffffff">in</text>',
         '<text class="mono tiny" x="62" y="26">LINKEDIN</text>',
         '<text class="mono" x="62" y="43" font-size="14" font-weight="700" fill="%s">kyle-lotter</text>' % text,
         '<line x1="214" y1="28" x2="246" y2="28" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % accent,
         '<polyline points="238,20 247,28 238,36" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % accent]
    css = '.mono{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace}.tiny{font-size:11px;fill:%s;letter-spacing:2.2px}' % muted
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img">'
            '<title>LinkedIn, kyle-lotter</title><style>%s</style>%s</svg>' % (w, h, w, h, css, "".join(o)))


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        (out / ("journey-%s.svg" % name)).write_text(journey(theme), encoding="utf-8")
        (out / ("projects-%s.svg" % name)).write_text(projects(theme), encoding="utf-8")
        (out / ("practice-%s.svg" % name)).write_text(practice(theme), encoding="utf-8")
        (out / ("tools-%s.svg" % name)).write_text(tools(theme), encoding="utf-8")
        (out / ("linkedin-%s.svg" % name)).write_text(linkedin(theme), encoding="utf-8")
    print("wrote 10 files to", out)
