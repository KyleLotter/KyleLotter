#!/usr/bin/env python3
"""Generates the animated hero banner, in a light and a dark version.

The name fades up, a line draws itself, a role badge cycles through what I do and
a small train travels the line. All animation is SMIL, which GitHub plays inside <img>.
Run:  python3 scripts/make_hero.py
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_map import THEMES, contours  # noqa: E402

W, H = 1000, 300
ROLES = ["ANDROID DEVELOPER", ".NET DEVELOPER", "IOT BUILDER", "CLOUD + SECURITY"]
CYCLE = 12  # seconds for the full set of roles


def fade_up(delay, dur=1.0, rise=14):
    return ('<animate attributeName="opacity" from="0" to="1" begin="%ss" dur="%ss" fill="freeze"/>'
            '<animateTransform attributeName="transform" type="translate" from="0 %d" to="0 0" '
            'begin="%ss" dur="%ss" fill="freeze"/>' % (delay, dur, rise, delay, dur))


def role_cycle(i, n):
    """Opacity and a small slide for role i of n, looping every CYCLE seconds."""
    t0 = i / n
    a, b, c = t0 + 0.025, t0 + 1 / n - 0.035, t0 + 1 / n - 0.01
    kt = "0;%.3f;%.3f;%.3f;%.3f;1" % (t0, a, b, c)
    op = "0;0;1;1;0;0"
    ty = "0 10;0 10;0 0;0 0;0 -10;0 -10"
    return ('<animate attributeName="opacity" values="%s" keyTimes="%s" begin="1.6s" dur="%ds" repeatCount="indefinite"/>'
            '<animateTransform attributeName="transform" type="translate" values="%s" keyTimes="%s" '
            'begin="1.6s" dur="%ds" repeatCount="indefinite"/>' % (op, kt, CYCLE, ty, kt, CYCLE))


def build(t):
    text, muted, track, accent = t["text"], t["muted"], t["track"], t["accent"]
    css = """
.mono{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace}
.serif{font-family:Georgia,"Times New Roman","DejaVu Serif",serif}
.tiny{font-size:11px;fill:%s;letter-spacing:3px}
""" % muted
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img">' % (W, H, W, H),
         '<title>Kyle Lötter</title>',
         '<desc>Kyle Lötter. Android developer, .NET developer, IoT builder, cloud and security. '
         'Gqeberha, South Africa.</desc>',
         '<style>%s</style>' % css,
         '<defs><clipPath id="c"><rect width="%d" height="%d"/></clipPath></defs>' % (W, H),
         '<g clip-path="url(#c)">']
    o += contours(t, 120, 60, 5, 34, 40, 41)
    o += contours(t, 900, 270, 6, 34, 40, 44)
    o.append('</g>')

    # Name
    o.append('<text class="serif" x="500" y="118" font-size="72" text-anchor="middle" fill="%s" opacity="0">Kyle Lötter%s</text>'
             % (text, fade_up(0.2)))

    # Role badge, centred
    o.append('<g opacity="0"><rect x="290" y="148" width="420" height="58" rx="29" fill="none" stroke="%s" stroke-width="1.5"/>'
             '<circle cx="324" cy="177" r="5" fill="%s"><animate attributeName="opacity" values="1;.25;1" dur="2.4s" repeatCount="indefinite"/></circle>'
             '<animate attributeName="opacity" from="0" to="1" begin="0.8s" dur="0.8s" fill="freeze"/></g>' % (t["edge"], accent))
    for i, role in enumerate(ROLES):
        o.append('<text class="mono" x="510" y="185" font-size="21" font-weight="700" text-anchor="middle" fill="%s" opacity="%d" '
                 'style="letter-spacing:2px">%s%s</text>' % (text, 0, escape(role), role_cycle(i, len(ROLES))))

    # Place
    o.append('<text class="mono tiny" x="500" y="252" text-anchor="middle" opacity="0">GQEBERHA · SOUTH AFRICA%s</text>' % fade_up(1.3, 1.0, 6))

    # Line that draws itself, with one slow train
    o.append('<line x1="56" y1="284" x2="944" y2="284" stroke="%s" stroke-width="3" stroke-linecap="round" '
             'stroke-dasharray="888" stroke-dashoffset="888">'
             '<animate attributeName="stroke-dashoffset" from="888" to="0" begin="0.4s" dur="1.6s" fill="freeze"/></line>' % track)
    o.append('<circle r="4.5" fill="%s" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="2s" dur="0.4s" fill="freeze"/>'
             '<animateMotion dur="14s" begin="2s" repeatCount="indefinite" path="M56 284 L944 284" keyPoints="0;1;0" '
             'keyTimes="0;0.5;1" calcMode="linear"/></circle>' % accent)
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        f = out / ("hero-%s.svg" % name)
        f.write_text(build(theme), encoding="utf-8")
        print("wrote", f, f.stat().st_size, "bytes")
