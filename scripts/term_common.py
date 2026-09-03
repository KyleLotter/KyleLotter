BG = "#0b0d10"
BORDER = "#232a33"
ACCENT = "#5CE68C"
ACCENT_DIM = "#2f6b46"
TEXT_PRIMARY = "#d6dee8"
TEXT_SECONDARY = "#69737f"

MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

W = 880
RADIUS = 8


def svg_open(w, h):
    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )


def svg_close():
    return "</svg>"


def panel_fill(w, h, top=False, bottom=False, r=RADIUS):
    """Filled background shape, no stroke. Rounded only on the requested edge."""
    if top and not bottom:
        d = f"M0,{r} A{r},{r} 0 0 1 {r},0 H{w-r} A{r},{r} 0 0 1 {w},{r} V{h} H0 Z"
        return f'<path d="{d}" fill="{BG}"/>'
    if bottom and not top:
        d = f"M0,0 H{w} V{h-r} A{r},{r} 0 0 1 {w-r},{h} H{r} A{r},{r} 0 0 1 0,{h-r} Z"
        return f'<path d="{d}" fill="{BG}"/>'
    return f'<rect x="0" y="0" width="{w}" height="{h}" fill="{BG}"/>'


def side_borders(w, h, color=BORDER, sw=1.5):
    return (
        f'<line x1="0.75" y1="0" x2="0.75" y2="{h}" stroke="{color}" stroke-width="{sw}"/>'
        f'<line x1="{w-0.75}" y1="0" x2="{w-0.75}" y2="{h}" stroke="{color}" stroke-width="{sw}"/>'
    )


def top_border(w, r=RADIUS, color=BORDER, sw=1.5):
    d = f"M0,{r} A{r},{r} 0 0 1 {r},0 H{w-r} A{r},{r} 0 0 1 {w},{r}"
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"/>'


def bottom_border(w, h, r=RADIUS, color=BORDER, sw=1.5):
    d = f"M0,{h-r} A{r},{r} 0 0 0 {r},{h} H{w-r} A{r},{r} 0 0 0 {w},{h-r}"
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"/>'


def panel(h, top=False, bottom=False, w=W):
    """Returns opening svg tags for a panel with correct fill + borders."""
    out = [svg_open(w, h)]
    out.append(panel_fill(w, h, top=top, bottom=bottom))
    out.append(side_borders(w, h))
    if top:
        out.append(top_border(w))
    if bottom:
        out.append(bottom_border(w, h))
    return out


def prompt_line(x, y, command, size=14.5):
    return (
        f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}">'
        f'<tspan fill="{ACCENT}">kyle@dev</tspan>'
        f'<tspan fill="{TEXT_SECONDARY}">:~$ </tspan>'
        f'<tspan fill="{TEXT_PRIMARY}">{command}</tspan>'
        f'</text>'
    )


def out_line(x, y, text, size=13.5, color=TEXT_SECONDARY, weight="400"):
    return (
        f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}">{text}</text>'
    )
