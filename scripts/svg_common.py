BG = "#0a0e17"
CARD_BG = "#0d1320"
BORDER = "#1c2740"
ACCENT = "#2dd4bf"
ACCENT_DIM = "#1a7f73"
TEXT_PRIMARY = "#e6edf3"
TEXT_SECONDARY = "#8593a8"

SANS = "'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"


def corner_brackets(w, h, pad=18, size=16, color=ACCENT, stroke=2):
    """Four L-shaped corner brackets, sci-fi framing style."""
    x0, y0, x1, y1 = pad, pad, w - pad, h - pad
    paths = [
        f"M{x0},{y0+size} L{x0},{y0} L{x0+size},{y0}",
        f"M{x1-size},{y0} L{x1},{y0} L{x1},{y0+size}",
        f"M{x0},{y1-size} L{x0},{y1} L{x0+size},{y1}",
        f"M{x1-size},{y1} L{x1},{y1} L{x1},{y1-size}",
    ]
    return "\n".join(
        f'<path d="{p}" stroke="{color}" stroke-width="{stroke}" fill="none" stroke-linecap="round"/>'
        for p in paths
    )


def card_frame(w, h, pad=18, radius=10):
    return (
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{radius}" '
        f'fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1.5"/>'
    )


def svg_open(w, h):
    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'<rect width="{w}" height="{h}" fill="{BG}"/>'
    )


def svg_close():
    return "</svg>"


def section_label(text, x, y, size=12, color=TEXT_SECONDARY, anchor="middle", spacing="4px"):
    return (
        f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" '
        f'font-weight="600" fill="{color}" text-anchor="{anchor}" '
        f'letter-spacing="{spacing}">{text.upper()}</text>'
    )
