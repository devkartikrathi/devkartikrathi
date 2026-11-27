"""
Builds every static SVG in assets/{dark,light}/.
Edit the CONTENT section, then:  python scripts/build_assets.py
"""
from __future__ import annotations

import math
import os

from hairline import SVG, THEMES, delay, measure, wrap

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# ── CONTENT ────────────────────────────────────────────────────────────────
NAME = "Kartik Rathi"
ROLE_LINE = "Software Engineer — AI/ML Systems"
TAGLINES = [
    "Building production RAG & multi-agent systems.",
    "Turning LLMs into reliable, shipped software.",
    "Measuring everything: RAGAS, P95, error budgets.",
]
SPEC = [
    ("ROLE", "Software Engineer"),
    ("BASE", "Global Payments, Pune"),
    ("FOCUS", "RAG · Agents · LLM infra"),
    ("PREV", "Arcap · NeedCFO · IIT Mandi"),
    ("STATUS", "Open to collaborations"),
]

METRICS = [
    ("300+", "inference requests", "per day, in production"),
    ("<800ms", "P95 latency on", "GCP Cloud Run"),
    ("<1%", "error rate across", "LLM pipelines"),
    ("−25%", "low-quality answers,", "week over week"),
    ("100+", "financial docs a day", "through OCR + LLM"),
    ("−50%", "manual review time", "after automation"),
]

TIMELINE = [
    dict(date=("FEB 2026", "PRESENT"), role="Software Engineer",
         org="Global Payments  ·  Pune, India", current=True,
         desc="Engineering in Java and Python on payments software. Also building internal "
              "automation that turns team tracking, reporting and comms into reusable, "
              "configurable workflows other teams can adopt.",
         tags="Java · Python · Workflow automation"),
    dict(date=("AUG 2025", "JAN 2026"), role="Software Engineer, AI Systems",
         org="Arcap REIT AI Solutions  ·  Remote",
         desc="Designed ML/LLM pipelines on GCP (Cloud Run, GCS, Pub/Sub) serving 300+ inference "
              "requests a day at P95 under 800 ms and under 1% errors. Built LangChain + Qdrant "
              "RAG with RAGAS evaluation, cutting low-quality responses 25% week over week.",
         tags="FastAPI · LangChain · Qdrant · GCP · Pub/Sub · RAGAS"),
    dict(date=("DEC 2024", "JUN 2025"), role="Software Developer Intern",
         org="NeedCFO  ·  Gurugram, India",
         desc="Built an OCR + LLM pipeline processing 100+ financial documents a day, cutting "
              "manual review time by half, on FastAPI, MongoDB and Celery/Redis workers.",
         tags="FastAPI · MongoDB · Celery · Redis · OCR"),
    dict(date=("JUN 2024", "JUL 2024"), role="Research Intern, LLM & NLP",
         org="IIT Mandi  ·  Center for AI & Robotics",
         desc="Fine-tuned transformer models for Sanskrit-to-English translation and explored "
              "RAG architectures for knowledge-augmented question answering.",
         tags="PyTorch · Hugging Face · NLP · RAG"),
    dict(date=("2021", "2025"), role="B.Tech, CSE (AI & ML)",
         org="K.R. Mangalam University  ·  GPA 8.6 / 10", edu=True,
         desc="Data structures, algorithms, operating systems, DBMS, networks, distributed "
              "systems, ML, DL, NLP and system design.",
         tags="Education"),
]

PROJECTS = [
    dict(slug="vimlearn", name="VimLearn", kind="EDTECH", motif="vim",
         desc="An interactive Vim course: 52 lessons drilled inside a modal editor built from "
              "scratch. Keys unlock as you learn; goals are judged by buffer state, not keystrokes.",
         stack="Next.js · TypeScript · shadcn/ui"),
    dict(slug="delhi", name="Reimagining Delhi", kind="CIVIC DESIGN", motif="bars",
         desc="A conceptual redesign of Delhi's public record: budget, policy, heritage and "
              "services on one bilingual page, with light, dark and high-contrast themes.",
         stack="Next.js 16 · React 19 · CSS Modules"),
    dict(slug="chronos", name="Chronos", kind="PRODUCT", motif="grid",
         desc="A time tracker for the 24 hours you actually have. Log a day in twenty seconds "
              "and watch a month of real life appear as a grid, read by an insight engine.",
         stack="Next.js 16 · Prisma 7 · Neon · Clerk"),
    dict(slug="pathgenie", name="PathGenie", kind="MULTI-AGENT", motif="graph",
         desc="An AI career mentor built as a crew of agents: profile analysis, goal setting, "
              "resource curation and interview prep, with persistent memory.",
         stack="Next.js · CrewAI · LangChain · RAG"),
    dict(slug="codeassist", name="Code Assist", kind="DEV TOOLS", motif="stream",
         desc="A full-stack IDE in the browser. Node.js runs client-side via WebContainers while "
              "Claude streams code generation and multi-file edits.",
         stack="React · WebContainers · Monaco · Vite"),
    dict(slug="finsight", name="FinSight One", kind="RAG · FINANCE", motif="doc",
         desc="Privacy-first RAG over 100+ page financial reports. Hybrid semantic and keyword "
              "search, with every answer cited back to its source page.",
         stack="FastAPI · LangChain · Qdrant · Docker"),
    dict(slug="statly", name="Statly", kind="FINTECH SAAS", motif="candles",
         desc="Trade analytics for Indian retail traders: performance metrics, pattern "
              "recognition and AI insights to end blind trading.",
         stack="Next.js · FastAPI · PostgreSQL · Gemini"),
    dict(slug="chatgita", name="ChatGita", kind="RAG · NLP", motif="sun",
         desc="Semantic search over the Bhagavad Gita. Ask a question, get the verses that "
              "answer it, with transliteration and context.",
         stack="Python · Embeddings · Vector search"),
]

TOOLKIT = [
    ("LANGUAGES", ["Python", "TypeScript", "Java", "Go", "JavaScript", "SQL"]),
    ("LLM & AGENTS", ["LangChain", "CrewAI", "RAG", "RAGAS", "Hugging Face", "PyTorch", "MCP"]),
    ("BACKEND", ["FastAPI", "Node.js", "Celery", "Redis", "Prisma", "REST"]),
    ("DATA", ["PostgreSQL", "Qdrant", "MongoDB", "Neon", "Pub/Sub"]),
    ("CLOUD & OPS", ["GCP", "Cloud Run", "AWS", "Docker", "Vercel", "n8n"]),
    ("FRONTEND", ["Next.js", "React", "Tailwind", "shadcn/ui", "Clerk"]),
]

PIPELINE = [
    ("01", "Sources", "PDF · API · DB"),
    ("02", "Ingest", "OCR · parse"),
    ("03", "Index", "chunk · embed"),
    ("04", "Retrieve", "BM25 + vector"),
    ("05", "Rerank", "cross-encoder"),
    ("06", "Generate", "cited answer"),
    ("07", "Evaluate", "RAGAS · P95"),
]

SECTIONS = [
    ("01", "Index", "who I am"),
    ("02", "Record", "where I've worked"),
    ("03", "Selected work", "things I've shipped"),
    ("04", "How I build", "a RAG loop, as I ship it"),
    ("05", "Toolkit", "what I reach for"),
    ("06", "Activity", "auto-updated daily"),
    ("07", "Contact", "say hello"),
]

BUTTONS = [
    ("linkedin", "LINKEDIN", False),
    ("portfolio", "PORTFOLIO", False),
    ("email", "EMAIL", False),
    ("x", "X / TWITTER", False),
    ("call", "BOOK A CALL", True),
]

W = 1200


# ── HEADER ─────────────────────────────────────────────────────────────────
def header(theme):
    css = """
    .rot{animation:rot 12s ease infinite both}
    .r1{opacity:1}.r2,.r3{opacity:0}
    .r2{animation-delay:4s}.r3{animation-delay:8s}
    @keyframes rot{0%{opacity:0;transform:translateY(8px)}3%,30%{opacity:1;transform:none}
      33%,100%{opacity:0;transform:translateY(-8px)}}
    .scan{opacity:0;animation:scan 2.8s cubic-bezier(.6,0,.3,1) .3s both}
    @keyframes scan{0%{opacity:0;transform:translateX(0)}12%{opacity:.85}
      100%{opacity:0;transform:translateX(1120px)}}
    .name{stroke-dasharray:900;stroke-dashoffset:0;fill-opacity:1;
      animation:nm 2.6s cubic-bezier(.65,0,.35,1) .1s both}
    @keyframes nm{0%{stroke-dashoffset:900;fill-opacity:0}60%{fill-opacity:0}
      100%{stroke-dashoffset:0;fill-opacity:1}}
    """
    s = SVG(W, 460, theme, f"{NAME} — {ROLE_LINE}", css)
    X0, Y0, X1, Y1 = 40, 40, 1160, 420
    s.crop_marks(X0, Y0, X1 - X0, Y1 - Y0)
    s.rect(X0 + .5, Y0 + .5, X1 - X0 - 1, Y1 - Y0 - 1, cls="dr", style=delay(0))

    # meta row + ruler
    s.text(64, 70, "KR / PROFILE — FIG. 01", "mono", 13, "dim", ls=1.6, cls="fi")
    s.text(600, 70, "28.61° N   77.21° E   ·   NEW DELHI", "mono", 13, "dim", "middle", ls=1.6, cls="fi")
    s.text(1136, 70, "REV. 2026.11", "mono", 13, "dim", "end", ls=1.6, cls="fi")
    s.line(X0, 86.5, X1, 86.5, cls="dr", style=delay(.2))
    for i, x in enumerate(range(X0 + 10, X1, 10)):
        h = 7 if x % 100 == 40 else (4 if x % 50 == 40 else 2)
        s.line(x + .5, 87, x + .5, 87 + h, stroke="faint", cls="fi", style=delay(.4 + i * .003))

    # faint blueprint grid
    for x in range(140, 1100, 100):
        s.line(x + .5, 104, x + .5, 368, stroke="faint", style="opacity:.45", attrs='stroke-dasharray="1 5"')

    # name — drawn as an outline, then inked
    nx, ny, nsize = 72, 236, 132
    s.text(nx, ny, NAME, "serif", nsize, "ink", cls="name",
           attrs=f'stroke="{s.c("ink")}" stroke-width="0.8"', ls=-1.5)
    nw = measure(NAME, "serif", nsize, -1.5)
    s.rect(nx + nw + 6, ny - 16, 16, 16, stroke="none", fill="accent", cls="fu", style=delay(2.2))

    s.text(76, 284, ROLE_LINE, "mono-m", 16, "dim", ls=2.2, upper=True, cls="fu", style=delay(.9))

    # rotating taglines with caret
    for i, t in enumerate(TAGLINES):
        g_cls = f"rot r{i+1}"
        tw = measure(t, "sans", 25)
        s.add(f'<g class="{g_cls}">')
        s.text(76, 338, ">", "mono-m", 22, "accent")
        s.text(104, 338, t, "sans", 25, "ink")
        s.rect(round(104 + tw + 7), 316, 12, 26, stroke="none", fill="accent", cls="blink")
        s.add("</g>")

    # spec block
    sx, vx, top, rh = 806, 884, 116, 50
    s.line(782.5, 112, 782.5, 360, cls="dr", style=delay(.6))
    for i, (k, v) in enumerate(SPEC):
        y = top + i * rh
        st = delay(1.0 + i * .12)
        s.add(f'<g class="fu" style="{st}">')
        s.text(sx, y + 31, k, "mono", 12.5, "dim", ls=1.4)
        if k == "STATUS":
            s.circle(vx + 5, y + 26, 5, fill="live", cls="pulse")
            s.circle(vx + 5, y + 26, 5, fill="live")
            s.text(vx + 18, y + 32, v, "sans-m", 18, "ink")
        else:
            s.text(vx, y + 32, v, "sans-m", 18, "ink")
        s.add("</g>")
        s.line(sx, y + rh - .5, 1136, y + rh - .5, cls="dr", style=delay(1.0 + i * .12))

    # bottom strip
    s.line(X0, 380.5, X1, 380.5, cls="dr", style=delay(.3))
    s.line(X0, 380.5, 360, 380.5, stroke="accent", w=2, cls="dr", style=delay(1.4))
    s.text(64, 407, "LLM SYSTEMS  /  RETRIEVAL  /  EVALUATION  /  SHIPPED SOFTWARE",
           "mono", 13, "dim", ls=1.6, cls="fi", style=delay(1.2))
    s.text(1136, 407, "KR—001", "mono-m", 13, "accent", "end", ls=1.6, cls="fi", style=delay(1.2))

    # load-in scan line
    s.line(X0, Y0, X0, Y1, stroke="accent", cls="scan")
    return s


# ── SECTION HEADS ──────────────────────────────────────────────────────────
def section(theme, num, title, sub):
    s = SVG(W, 92, theme, f"§{num} {title}")
    s.text(2, 60, f"§ {num}", "mono-m", 15, "accent", ls=1.5, cls="fi")
    s.text(74, 64, title, "serif", 54, "ink", cls="fu", ls=-.5)
    tw = measure(title, "serif", 54, -.5)
    sw = measure(sub.upper(), "mono", 14, 1.8)
    x1, x2 = 74 + tw + 28, W - sw - 26
    s.circle(x1, 50.5, 3, fill="accent", cls="fi", style=delay(.3))
    s.line(x1 + 10, 50.5, x2, 50.5, cls="dr", style=delay(.25))
    s.line(x2 + .5, 43, x2 + .5, 58, stroke="dim", cls="fi", style=delay(1.2))
    s.text(W - 1, 55, sub, "mono", 14, "dim", "end", ls=1.8, upper=True, cls="fi", style=delay(.8))
    return s


# ── METRICS STRIP ──────────────────────────────────────────────────────────
def metrics(theme):
    s = SVG(W, 200, theme, "Impact: " + ", ".join(f"{m[0]} {m[1]} {m[2]}" for m in METRICS))
    cw = W / len(METRICS)
    s.line(0, 12.5, W, 12.5, cls="dr")
    s.line(0, 187.5, W, 187.5, cls="dr", style=delay(.15))
    for i, (num, l1, l2) in enumerate(METRICS):
        x = i * cw
        if i:
            s.line(round(x) + .5, 13, round(x) + .5, 187, cls="dr", style=delay(.3 + i * .06))
        d = .35 + i * .11
        s.text(x + 22, 44, f"0{i+1}", "mono", 12.5, "dim", ls=1.2, cls="fi", style=delay(d))
        size = 58
        while measure(num, "serif", size) > cw - 40:
            size -= 2
        s.text(x + 20, 106, num, "serif", size, "ink", cls="fu", style=delay(d), ls=-.5)
        s.line(x + 22, 122.5, x + 48, 122.5, stroke="accent", w=2, cls="dr", style=delay(d + .3))
        s.text(x + 22, 150, l1, "mono", 13, "dim", cls="fi", style=delay(d + .2))
        s.text(x + 22, 169, l2, "mono", 13, "dim", cls="fi", style=delay(d + .2))
    return s


# ── TIMELINE ───────────────────────────────────────────────────────────────
def timeline(theme):
    DX, RAIL, CX, CW = 0, 214, 252, 940
    blocks, y = [], 24
    for e in TIMELINE:
        lines = wrap(e["desc"], "sans", 19, CW)
        h = 50 + 34 + len(lines) * 29 + 40
        blocks.append((y, lines, h))
        y += h + 22
    H = y + 4
    s = SVG(W, H, theme, "Experience timeline")
    s.line(RAIL + .5, 24, RAIL + .5, H - 20, cls="dr", style="animation-duration:2.4s;")
    for idx, (e, (y, lines, h)) in enumerate(zip(TIMELINE, blocks)):
        d = .25 + idx * .22
        st = delay(d)
        s.text(DX, y + 30, e["date"][0], "mono-m", 14, "ink", ls=1.6, cls="fi", style=st)
        s.text(DX, y + 52, "— " + e["date"][1], "mono", 14,
               "accent" if e.get("current") else "dim", ls=1.6, cls="fi", style=st)
        ny = y + 24
        if e.get("current"):
            s.circle(RAIL + .5, ny, 6, fill="accent", cls="pulse")
            s.circle(RAIL + .5, ny, 6, fill="accent", cls="fi", style=st)
        else:
            s.circle(RAIL + .5, ny, 5, fill="bg", stroke="dim" if not e.get("edu") else "faint",
                     sw=1.2, cls="fi", style=st)
        s.line(RAIL + 12, ny + .5, CX - 10, ny + .5, stroke="faint", cls="dr", style=st)
        s.add(f'<g class="fu" style="{st}">')
        s.text(CX, y + 36, e["role"], "serif", 38, "ink", ls=-.3)
        s.text(CX, y + 68, e["org"], "mono-m", 15, "accent" if e.get("current") else "dim", ls=.6)
        for j, ln in enumerate(lines):
            s.text(CX, y + 106 + j * 29, ln, "sans", 19, "dim")
        ty = y + 106 + len(lines) * 29 + 12
        s.text(CX, ty, e["tags"], "mono", 14, "ink", ls=.6, style="opacity:.75")
        s.add("</g>")
        if idx < len(TIMELINE) - 1:
            s.line(CX, y + h + 10.5, W, y + h + 10.5, stroke="faint", cls="dr", style=delay(d + .2),
                   attrs='stroke-dasharray="2 4"' if False else "")
    return s


# ── PROJECT CARDS ──────────────────────────────────────────────────────────
def motif(s: SVG, kind: str, ox: int, oy: int):
    """Small animated hairline illustration, ~130×96 box at (ox, oy)."""
    A, I, F, D = "accent", "ink", "faint", "dim"
    if kind == "vim":
        for i, w in enumerate([118, 84, 104, 60]):
            s.rect(ox, oy + i * 14, w, 6, stroke="none", fill=F)
        s.css += """.cur{animation:cur 4s steps(1) infinite}
        @keyframes cur{0%{transform:translate(0,0)}25%{transform:translate(36px,14px)}
        50%{transform:translate(72px,28px)}75%{transform:translate(20px,42px)}}"""
        s.rect(ox, oy - 3, 9, 12, stroke="none", fill=A, cls="cur")
        for i, k in enumerate("hjkl"):
            x = ox + i * 30
            s.rect(x + .5, oy + 66.5, 24, 24, stroke=D, rx=3)
            s.text(x + 12, oy + 83, k, "mono-m", 12, I, "middle")
    elif kind == "bars":
        vals = [40, 64, 52, 88, 70, 30, 58]
        s.line(ox, oy + 92.5, ox + 130, oy + 92.5, stroke=D)
        s.css += """.bar{transform-box:fill-box;transform-origin:bottom;animation:bar 1.4s cubic-bezier(.2,.7,.2,1) both}
        @keyframes bar{from{transform:scaleY(0)}to{transform:scaleY(1)}}"""
        for i, v in enumerate(vals):
            s.rect(ox + 4 + i * 18, oy + 92 - v, 8, v, stroke="none",
                   fill=A if i == 3 else F, cls="bar", style=delay(.3 + i * .08))
    elif kind == "grid":
        import random
        rnd = random.Random(7)
        s.css += ".gc{animation:fi .5s ease both}"
        for r in range(6):
            for c in range(10):
                lvl = rnd.choice([0, 0, 1, 1, 2, 3, 4])
                op = [0, .25, .45, .7, 1][lvl]
                x, y = ox + c * 13, oy + 4 + r * 13
                if lvl == 0:
                    s.rect(x + .5, y + .5, 9, 9, stroke=F)
                else:
                    s.rect(x, y, 10, 10, stroke="none", fill=A, cls="gc",
                           style=f"fill-opacity:{op};" + delay(.2 + (r + c) * .05))
    elif kind == "graph":
        pts = [(10, 48), (52, 14), (52, 82), (96, 34), (122, 70)]
        edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (2, 4)]
        for a, b in edges:
            s.line(ox + pts[a][0], oy + pts[a][1], ox + pts[b][0], oy + pts[b][1], stroke=D, cls="dr")
        route = "M{} {} L{} {} L{} {} L{} {}".format(
            ox + 10, oy + 48, ox + 52, oy + 14, ox + 96, oy + 34, ox + 122, oy + 70)
        for i, (x, y) in enumerate(pts):
            s.circle(ox + x, oy + y, 5, fill="bg", stroke=I, sw=1.2)
        s.add(f'<circle r="3.5" fill="{s.c(A)}"><animateMotion dur="3.2s" repeatCount="indefinite" '
              f'path="{route}"/></circle>')
    elif kind == "stream":
        s.text(ox, oy + 30, "{", "mono", 34, D)
        s.text(ox + 130, oy + 92, "}", "mono", 34, D, "end")
        s.css += """.sl{transform-box:fill-box;transform-origin:left;animation:sl 4.5s ease infinite both}
        @keyframes sl{0%{transform:scaleX(0)}25%,85%{transform:scaleX(1)}100%{transform:scaleX(1);opacity:0}}"""
        for i, w in enumerate([70, 94, 52, 80]):
            s.rect(ox + 26, oy + 26 + i * 14, w, 5, stroke="none",
                   fill=A if i == 1 else F, cls="sl", style=delay(i * .45))
    elif kind == "doc":
        s.path(f"M{ox+20} {oy} H{ox+86} L{ox+104} {oy+18} V{oy+96} H{ox+20} Z", stroke=D)
        s.path(f"M{ox+86} {oy} V{oy+18} H{ox+104}", stroke=D)
        for i, w in enumerate([60, 70, 48, 66, 54]):
            s.rect(ox + 30, oy + 26 + i * 12, w, 4, stroke="none",
                   fill=A if i == 2 else F, cls="fi", style=delay(.2 + i * .1))
        s.path(f"M{ox+80} {oy+52} C{ox+104} {oy+52} {ox+108} {oy+40} {ox+118} {oy+40}",
               stroke=A, cls="dr", style=delay(.9))
        s.text(ox + 120, oy + 44, "[1]", "mono-m", 11, A, cls="fi", style=delay(1.4))
    elif kind == "candles":
        data = [(60, 40, 70, 30), (42, 58, 64, 36), (58, 36, 62, 28), (38, 50, 56, 30),
                (50, 24, 54, 18), (26, 34, 40, 20), (34, 14, 38, 8), (16, 22, 28, 10)]
        pts = []
        for i, (o, c, lo, hi) in enumerate(data):
            x = ox + 6 + i * 16
            up = c < o
            col = A if up else D
            s.line(x + 3.5, oy + hi, x + 3.5, oy + lo, stroke=col, cls="fi", style=delay(.1 + i * .07))
            s.rect(x, oy + min(o, c), 7, max(abs(o - c), 2), stroke="none", fill=col,
                   cls="fi", style=delay(.1 + i * .07))
            pts.append(f"{x+3.5},{oy + (o + c) / 2 + 30}")
        s.path("M" + " L".join(pts), stroke=I, cls="dr", style=delay(.6) + "opacity:.6")
    elif kind == "sun":
        cx, cy = ox + 66, oy + 48
        s.css += """.spin{transform-box:view-box;transform-origin:%dpx %dpx;animation:spin 60s linear infinite}
        @keyframes spin{to{transform:rotate(360deg)}}""" % (cx, cy)
        s.add('<g class="spin">')
        for i in range(36):
            a = i * math.tau / 36
            r1, r2 = 14, (44 if i % 2 == 0 else 34)
            s.line(round(cx + r1 * math.cos(a), 2), round(cy + r1 * math.sin(a), 2),
                   round(cx + r2 * math.cos(a), 2), round(cy + r2 * math.sin(a), 2),
                   stroke=A if i % 9 == 0 else F)
        s.add("</g>")
        s.circle(cx, cy, 8, fill="none", stroke=I, sw=1.2)
        s.text(cx, oy + 108, "18 · 700", "mono", 10, D, "middle", ls=1)


def card(theme, i, p):
    CW, CH = 580, 372
    s = SVG(CW, CH, theme, f"{p['name']} — {p['desc']}")
    s.rect(.5, .5, CW - 1, CH - 1, cls="dr", style="animation-duration:2s;")
    for (x, y, dx, dy) in [(0, 0, 1, 1), (CW, 0, -1, 1), (0, CH, 1, -1), (CW, CH, -1, -1)]:
        s.path(f"M{x + dx*.75} {y + dy*14} V{y + dy*.75} H{x + dx*14}", stroke="accent", sw=1.5,
               cls="fi", style=delay(.6))
    s.text(28, 46, f"P/0{i+1}", "mono-m", 15, "accent", ls=1.6, cls="fi")
    kw = measure(p["kind"], "mono", 13, 1.4)
    s.rect(round(552 - kw - 26) + .5, 27.5, round(kw + 26), 28, stroke="dim", rx=14, cls="fi")
    s.text(552 - 13, 46, p["kind"], "mono", 13, "dim", "end", ls=1.4, cls="fi")

    s.text(28, 122, p["name"], "serif", 54, "ink", cls="fu", style=delay(.15), ls=-.4)
    lines = wrap(p["desc"], "sans", 18.5, 372)[:5]
    s.add(f'<g class="fu" style="{delay(.3)}">')
    for j, ln in enumerate(lines):
        s.text(28, 166 + j * 27, ln, "sans", 18.5, "dim")
    s.add("</g>")
    motif(s, p["motif"], 424, 150)

    s.line(28, 308.5, 552, 308.5, cls="dr", style=delay(.4))
    s.text(28, 342, p["stack"], "mono", 14, "ink", ls=.2, cls="fi", style=delay(.6) + "fill-opacity:.8")
    s.text(552 - 16, 342, "VIEW", "mono-m", 14, "accent", "end", ls=1.6, cls="fi", style=delay(.6))
    s.arrow_ne(552 - 9, 341, 9)
    return s


# ── PIPELINE ───────────────────────────────────────────────────────────────
def pipeline(theme):
    s = SVG(W, 318, theme, "RAG pipeline: " + " → ".join(p[1] for p in PIPELINE))
    n, bw, bh = len(PIPELINE), 140, 100
    gap = (W - 2 - n * bw) / (n - 1)
    by, cy = 76, 76 + 50
    xs = [1 + i * (bw + gap) for i in range(n)]
    s.text(0, 32, "INPUT", "mono", 13, "dim", ls=1.8, cls="fi")
    s.text(W, 32, "SHIPPED ANSWER", "mono", 13, "dim", "end", ls=1.8, cls="fi")
    s.line(0, 48.5, W, 48.5, stroke="faint", cls="dr")
    # flow line + packets (drawn beneath the boxes so they slip "through" them)
    s.line(xs[0] + bw / 2, cy + .5, xs[-1] + bw / 2, cy + .5, stroke="dim", cls="dr", style=delay(.2))
    main = f"M{xs[0]+bw/2} {cy+.5} H{xs[-1]+bw/2}"
    for k in range(3):
        s.add(f'<circle r="3.5" fill="{s.c("accent")}"><animateMotion dur="6s" begin="{k*2}s" '
              f'repeatCount="indefinite" path="{main}"/></circle>')
    # feedback arc Evaluate → Index
    fx1, fx2 = xs[6] + bw / 2, xs[2] + bw / 2
    fb = f"M{fx1} {by+bh} C{fx1} {by+bh+86} {fx2} {by+bh+86} {fx2} {by+bh}"
    s.path(fb, stroke="accent", cls="dr", style=delay(1.4), attrs='stroke-dasharray="3 4"')
    s.path(fb, stroke="accent", style="opacity:.0")
    s.add(f'<circle r="3" fill="{s.c("accent")}"><animateMotion dur="4s" repeatCount="indefinite" '
          f'path="{fb}"/></circle>')
    s.path(f"M{fx2-5} {by+bh+8} L{fx2} {by+bh+1} L{fx2+5} {by+bh+8}", stroke="accent", sw=1.2)
    s.text((fx1 + fx2) / 2, by + bh + 82, "FEEDBACK — evals drive chunking, retrieval & prompt changes",
           "mono", 13, "dim", "middle", ls=.4, cls="fi", style=delay(1.8))
    for i, (num, title, sub) in enumerate(PIPELINE):
        x = xs[i]
        st = delay(.2 + i * .12)
        s.add(f'<g class="fu" style="{st}">')
        s.rect(round(x) + .5, by + .5, bw - 1, bh - 1, stroke="ink" if i in (3, 6) else "rule", fill="bg")
        s.text(x + 15, by + 26, num, "mono-m", 13, "accent", ls=1)
        s.text(x + 15, by + 60, title, "serif", 30, "ink")
        s.text(x + 15, by + 82, sub, "mono", 12.5, "dim")
        s.add("</g>")
    return s


# ── TOOLKIT ────────────────────────────────────────────────────────────────
def toolkit(theme):
    rh = 64
    H = len(TOOLKIT) * rh + 16
    s = SVG(W, H, theme, "Toolkit: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in TOOLKIT))
    s.line(0, 8.5, W, 8.5, cls="dr")
    for i, (label, items) in enumerate(TOOLKIT):
        y = 8 + i * rh
        st = delay(.2 + i * .1)
        s.add(f'<g class="fu" style="{st}">')
        s.text(0, y + 39, f"0{i+1}", "mono", 13, "faint" if theme == "light" else "dim", ls=1)
        s.text(40, y + 39, label, "mono-m", 14, "accent", ls=1.4)
        x = 236
        for j, it in enumerate(items):
            s.text(x, y + 40, it, "sans-m", 20, "ink")
            x += measure(it, "sans-m", 20)
            if j < len(items) - 1:
                s.text(x + 15, y + 40, "/", "sans", 20, "faint" if theme == "dark" else "faint")
                x += 38
        s.text(W, y + 39, f"{len(items):02d}", "mono", 13, "dim", "end", ls=1)
        s.add("</g>")
        s.line(0, y + rh + .5, W, y + rh + .5, cls="dr", style=delay(.25 + i * .1))
    return s


# ── CONTACT ────────────────────────────────────────────────────────────────
def statement(theme):
    s = SVG(W, 270, theme, "If you care about correctness, maintainability and real engineering "
                          "trade-offs over buzzwords, let's talk.")
    s.crop_marks(0, 20, W, 230, len_=12, gap=0)
    s.text(0, 104, "Correctness, maintainability,", "serif", 66, "ink", cls="fu", ls=-.6)
    w1 = measure("and ", "serif", 66, -.6)
    s.text(0, 176, "and", "serif", 66, "ink", cls="fu", style=delay(.15), ls=-.6)
    s.text(w1, 176, "real trade-offs", "serif-i", 66, "accent", cls="fu", style=delay(.3), ls=-.6)
    w2 = w1 + measure("real trade-offs ", "serif-i", 66, -.6)
    s.text(w2, 176, "over buzzwords.", "serif", 66, "ink", cls="fu", style=delay(.45), ls=-.6)
    s.text(0, 232, "IF THAT'S HOW YOU BUILD TOO — LET'S TALK", "mono", 14, "dim", ls=1.8,
           cls="fi", style=delay(.8))
    s.arrow_e(W - 20, 227, 16)
    return s


def button(theme, key, label, primary):
    tw = measure(label, "mono-m", 12.5, 1.6)
    w = round(tw + 64)
    s = SVG(w, 46, theme, label.title())
    if primary:
        s.rect(.5, .5, w - 1, 45, stroke="accent", fill="accent", rx=23)
        s.text(24, 27.5, label, "mono-m", 12.5, "accent_ink", ls=1.6)
        s.arrow_ne(w - 30, 27, 7, stroke="accent_ink")
    else:
        s.rect(.5, .5, w - 1, 45, stroke="rule", rx=23)
        s.circle(18, 23, 2.5, fill="accent")
        s.text(28, 27.5, label, "mono-m", 12.5, "ink", ls=1.6)
        s.arrow_ne(w - 28, 27, 7)
    return s


def footer(theme):
    s = SVG(W, 76, theme, "End of record")
    s.line(0, 20.5, W, 20.5, cls="dr")
    s.line(W - 240, 20.5, W, 20.5, stroke="accent", w=2, cls="dr", style=delay(.5))
    s.text(0, 56, "END OF RECORD  ·  KARTIK RATHI  ·  NEW DELHI", "mono", 13, "dim", ls=1.8, cls="fi")
    s.text(W, 56, "SET IN INSTRUMENT SERIF, INTER & JETBRAINS MONO", "mono", 13, "dim", "end",
           ls=1.8, cls="fi")
    return s


def main():
    for theme in THEMES:
        header(theme).save(ROOT, "header.svg")
        for num, title, sub in SECTIONS:
            section(theme, num, title, sub).save(ROOT, f"section-{num}.svg")
        metrics(theme).save(ROOT, "metrics.svg")
        timeline(theme).save(ROOT, "timeline.svg")
        for i, p in enumerate(PROJECTS):
            card(theme, i, p).save(ROOT, f"card-{p['slug']}.svg")
        pipeline(theme).save(ROOT, "pipeline.svg")
        toolkit(theme).save(ROOT, "toolkit.svg")
        statement(theme).save(ROOT, "statement.svg")
        for key, label, primary in BUTTONS:
            button(theme, key, label, primary).save(ROOT, f"btn-{key}.svg")
        footer(theme).save(ROOT, "footer.svg")
    print("built", sum(len(fs) for _, _, fs in os.walk(ROOT)), "files")


if __name__ == "__main__":
    main()
