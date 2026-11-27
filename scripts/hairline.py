"""
hairline.py — tiny SVG toolkit behind the profile README.

Every asset is drawn on the same system: 1px rules, crop marks, mono labels,
an editorial serif, and one accent colour. Fonts are subset per file and
embedded as base64 WOFF2, so the type renders identically on every OS
(GitHub serves README images as <img>, which can't load web fonts).
"""
from __future__ import annotations

import base64
import html
import io
import os
from collections import defaultdict

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# ── Design tokens ──────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg": "#0d1117",      # GitHub dark canvas, used only to mask lines
        "ink": "#ECE8E1",     # warm paper white
        "dim": "#8B949E",
        "faint": "#3D444D",
        "rule": "#30363D",
        "accent": "#FF6B3D",  # signal vermilion
        "live": "#3FB950",
        "accent_ink": "#0d1117",
    },
    "light": {
        "bg": "#ffffff",
        "ink": "#1B1A17",
        "dim": "#59636E",
        "faint": "#C9D1D9",
        "rule": "#D1D9E0",
        "accent": "#E4461B",
        "live": "#1A7F37",
        "accent_ink": "#ffffff",
    },
}

FONTS = {
    #  key       file            family-name  fallback stack
    "serif":   ("serif.woff2",   "hl-serif",  "'Iowan Old Style',Georgia,serif", "normal"),
    "serif-i": ("serif-i.woff2", "hl-serifi", "'Iowan Old Style',Georgia,serif", "italic"),
    "mono":    ("mono.woff2",    "hl-mono",   "ui-monospace,'SF Mono',Menlo,Consolas,monospace", "normal"),
    "mono-m":  ("mono-m.woff2",  "hl-monom",  "ui-monospace,'SF Mono',Menlo,Consolas,monospace", "normal"),
    "sans":    ("sans.woff2",    "hl-sans",   "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif", "normal"),
    "sans-m":  ("sans-m.woff2",  "hl-sansm",  "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif", "normal"),
    "sans-b":  ("sans-b.woff2",  "hl-sansb",  "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif", "normal"),
}

_ttf_cache: dict[str, TTFont] = {}


def _font(key: str) -> TTFont:
    if key not in _ttf_cache:
        _ttf_cache[key] = TTFont(os.path.join(FONT_DIR, FONTS[key][0]))
    return _ttf_cache[key]


def measure(text: str, font: str, size: float, ls: float = 0.0) -> float:
    """Advance width of `text` in px, using the real font metrics."""
    f = _font(font)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = f["head"].unitsPerEm
    w = 0
    for ch in text:
        g = cmap.get(ord(ch))
        w += hmtx[g][0] if g else upm * 0.5
    return w / upm * size + ls * max(len(text) - 1, 0)


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if measure(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _subset_b64(key: str, chars: set[str]) -> str:
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    opts.notdef_outline = True
    font = TTFont(os.path.join(FONT_DIR, FONTS[key][0]))
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(chars | {" "})))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


BASE_CSS = """
.fu{animation:fu .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes fu{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.fi{animation:fi 1.1s ease both}
@keyframes fi{from{opacity:0}to{opacity:1}}
.dr{stroke-dasharray:1;stroke-dashoffset:0;animation:dr 1.6s cubic-bezier(.65,0,.35,1) both}
@keyframes dr{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
.blink{animation:blink 1.05s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-out infinite}
@keyframes pulse{0%{opacity:.7;transform:scale(1)}80%,100%{opacity:0;transform:scale(3.2)}}
text{font-kerning:normal}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


class SVG:
    def __init__(self, w: int, h: int, theme: str, title: str, css: str = ""):
        self.w, self.h = w, h
        self.t = THEMES[theme]
        self.theme = theme
        self.title = title
        self.css = css
        self.parts: list[str] = []
        self.defs: list[str] = []
        self.used: dict[str, set[str]] = defaultdict(set)

    # colour lookup: token name or literal
    def c(self, v: str) -> str:
        return self.t.get(v, v)

    def add(self, raw: str):
        self.parts.append(raw)

    def text(self, x, y, s, font="mono", size=12, fill="ink", anchor="start",
             ls=0.0, cls="", style="", attrs="", upper=False):
        if upper:
            s = s.upper()
        self.used[font].add(s)
        fam = FONTS[font]
        css = f"font-family:{fam[1]},{fam[2]};font-size:{size}px;"
        if fam[3] == "italic":
            css += "font-style:italic;"
        if ls:
            css += f"letter-spacing:{ls}px;"
        css += style
        c = f' class="{cls}"' if cls else ""
        a = f" {attrs}" if attrs else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" fill="{self.c(fill)}" '
                 f'text-anchor="{anchor}" style="{css}"{c}{a}>{html.escape(s)}</text>')

    def line(self, x1, y1, x2, y2, stroke="rule", w=1, cls="", style="", attrs=""):
        pl = ' pathLength="1"' if "dr" in cls.split() else ""
        c = f' class="{cls}"' if cls else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{self.c(stroke)}" '
                 f'stroke-width="{w}"{pl}{c} style="{style}" {attrs}/>')

    def rect(self, x, y, w, h, stroke="rule", fill="none", sw=1, rx=0, cls="", style="", attrs=""):
        pl = ' pathLength="1"' if "dr" in cls.split() else ""
        c = f' class="{cls}"' if cls else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                 f'fill="{self.c(fill)}" stroke="{self.c(stroke)}" stroke-width="{sw}"{pl}{c} '
                 f'style="{style}" {attrs}/>')

    def path(self, d, stroke="rule", fill="none", sw=1, cls="", style="", attrs=""):
        pl = ' pathLength="1"' if "dr" in cls.split() else ""
        c = f' class="{cls}"' if cls else ""
        self.add(f'<path d="{d}" fill="{self.c(fill)}" stroke="{self.c(stroke)}" '
                 f'stroke-width="{sw}"{pl}{c} style="{style}" {attrs}/>')

    def circle(self, cx, cy, r, stroke="none", fill="ink", sw=1, cls="", style="", attrs=""):
        c = f' class="{cls}"' if cls else ""
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{self.c(fill)}" '
                 f'stroke="{self.c(stroke)}" stroke-width="{sw}"{c} style="{style}" {attrs}/>')

    def arrow_ne(self, x, y, s=7, stroke="accent", w=1.3):
        """A drawn ↗ (the latin font subsets have no arrow glyphs)."""
        self.path(f"M{x} {y} L{x+s} {y-s} M{x+2} {y-s} L{x+s} {y-s} L{x+s} {y-s+5}",
                  stroke=stroke, sw=w, attrs='stroke-linecap="square"')

    def arrow_e(self, x, y, s=10, stroke="accent", w=1.2):
        self.path(f"M{x} {y} L{x+s} {y} M{x+s-4} {y-4} L{x+s} {y} L{x+s-4} {y+4}",
                  stroke=stroke, sw=w)

    def crop_marks(self, x, y, w, h, len_=12, gap=6, stroke="dim"):
        for (cx, cy, dx, dy) in [(x, y, -1, -1), (x + w, y, 1, -1), (x, y + h, -1, 1), (x + w, y + h, 1, 1)]:
            self.line(cx + dx * gap, cy, cx + dx * (gap + len_), cy, stroke=stroke)
            self.line(cx, cy + dy * gap, cx, cy + dy * (gap + len_), stroke=stroke)

    def render(self) -> str:
        faces = []
        for key, strings in self.used.items():
            chars = set("".join(strings))
            fam = FONTS[key]
            faces.append(
                f"@font-face{{font-family:{fam[1]};font-style:{fam[3]};"
                f"src:url(data:font/woff2;base64,{_subset_b64(key, chars)}) format('woff2')}}"
            )
        style = "\n".join(faces) + BASE_CSS + self.css
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{html.escape(self.title)}">'
            f"<title>{html.escape(self.title)}</title><style>{style}</style>{defs}"
            + "".join(self.parts) + "</svg>"
        )

    def save(self, root: str, name: str):
        d = os.path.join(root, self.theme)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(self.render())


def delay(s: float) -> str:
    return f"animation-delay:{s:.2f}s;"
