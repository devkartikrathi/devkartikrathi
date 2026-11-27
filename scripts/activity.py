"""
activity.py — renders assets/{dark,light}/activity.svg from live GitHub data.

  GH_TOKEN=... python scripts/activity.py            # fetch via GraphQL
  python scripts/activity.py --from-json data.json   # render from a saved snapshot

Runs daily in .github/workflows/activity.yml. Replaces third-party stats cards
(rate-limited, off-brand, often down) with one panel drawn in the same system.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request

from hairline import SVG, THEMES, delay, measure

USER = os.environ.get("GH_USER", "devkartikrathi")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

QUERY = """
query($login:String!){
  user(login:$login){
    contributionsCollection{ contributionCalendar{ totalContributions
      weeks{ contributionDays{ date contributionCount } } } }
    repositories(ownerAffiliations:OWNER, isFork:false, first:100, privacy:PUBLIC){
      totalCount
      nodes{ stargazerCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name } } } }
    }
  }
}"""


def fetch() -> dict:
    token = os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "hairline-activity"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        u = json.load(r)["data"]["user"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = {d["date"]: d["contributionCount"]
            for w in cal["weeks"] for d in w["contributionDays"]}
    langs: dict[str, int] = {}
    stars = 0
    for n in u["repositories"]["nodes"]:
        stars += n["stargazerCount"]
        for e in n["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return dict(days=days, total=cal["totalContributions"], repos=u["repositories"]["totalCount"],
                stars=stars, langs=langs, lang_basis="bytes",
                updated=dt.date.today().isoformat())


def streaks(days: dict[str, int]):
    ds = sorted(days)
    longest = run = 0
    for d in ds:
        run = run + 1 if days[d] else 0
        longest = max(longest, run)
    cur, i = 0, len(ds) - 1
    if i >= 0 and days[ds[i]] == 0:  # today not logged yet doesn't break a streak
        i -= 1
    while i >= 0 and days[ds[i]]:
        cur += 1
        i -= 1
    best = max(ds, key=lambda d: days[d]) if ds else None
    return cur, longest, best


def render(theme: str, data: dict) -> SVG:
    days = data["days"]
    ds = sorted(days)
    end = dt.date.fromisoformat(ds[-1])
    start = end - dt.timedelta(days=7 * 53 - 1)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)  # align to Sunday
    cur, longest, best = streaks(days)
    vals = sorted(v for v in days.values() if v)
    q = [vals[int(len(vals) * f)] for f in (.25, .5, .75)] if vals else [1, 2, 3]

    W, H = 1200, 346
    s = SVG(W, H, theme, f"{data['total']} contributions in the last year; current streak {cur} days; "
                         f"longest streak {longest} days", pad=32)
    s.line(0, 12.5, W, 12.5, cls="dr")

    # left column — numbers
    s.text(0, 46, "LAST 12 MONTHS", "mono", 13, "dim", ls=1.6, cls="fi")
    s.text(-4, 128, f"{data['total']:,}", "serif", 96, "ink", ls=-1.5, cls="fu")
    s.text(0, 156, "contributions", "mono", 13, "dim", ls=.6, cls="fi", style=delay(.2))
    rows = [("CURRENT STREAK", f"{cur} d"), ("LONGEST STREAK", f"{longest} d"),
            ("BEST DAY", f"{days[best]}  ·  {dt.date.fromisoformat(best):%d %b}" if best else "—"),
            ("PUBLIC REPOS", f"{data['repos']}  ·  {data['stars']} stars")]
    for i, (k, v) in enumerate(rows):
        y = 172 + i * 35
        st = delay(.3 + i * .1)
        s.line(0, y + .5, 300, y + .5, cls="dr", style=st)
        s.text(0, y + 24, k, "mono", 12, "dim", ls=1.2, cls="fi", style=st)
        s.text(300, y + 24, v, "sans-m", 16, "ink", "end", cls="fi", style=st)

    # heatmap
    cell, gap = 13, 3
    hx, hy = 344, 54
    s.line(330.5, 26, 330.5, 312, stroke="rule", cls="dr", style=delay(.2))
    month_seen = set()
    weeks = 53
    for c in range(weeks):
        col_date = start + dt.timedelta(days=7 * c)
        if col_date.month not in month_seen and col_date.day <= 7:
            month_seen.add(col_date.month)
            s.text(hx + c * (cell + gap), hy - 12, f"{col_date:%b}".upper(), "mono", 11.5, "dim",
                   ls=.8, cls="fi")
        for r in range(7):
            d = col_date + dt.timedelta(days=r)
            if d > end:
                continue
            v = days.get(d.isoformat(), 0)
            x, y = hx + c * (cell + gap), hy + r * (cell + gap)
            st = delay(.3 + c * .018)
            if v == 0:
                s.rect(x + .5, y + .5, cell - 1, cell - 1, stroke="faint", cls="fi", style=st)
            else:
                lvl = sum(v > t for t in q)
                op = [.28, .5, .74, 1][lvl]
                s.rect(x, y, cell, cell, stroke="none", fill="accent", cls="fi",
                       style=st + f"fill-opacity:{op};")
    # legend
    ly = hy + 7 * (cell + gap) + 18
    s.text(hx, ly + 10, "LESS", "mono", 11, "dim", ls=1, cls="fi", style=delay(1.2))
    lx = hx + 44
    s.rect(lx + .5, ly + .5, 10, 10, stroke="faint")
    for i, op in enumerate([.28, .5, .74, 1]):
        s.rect(lx + 16 + i * 16, ly, 11, 11, stroke="none", fill="accent", style=f"fill-opacity:{op}")
    s.text(lx + 86, ly + 10, "MORE", "mono", 11, "dim", ls=1, cls="fi", style=delay(1.2))

    # languages
    total = sum(data["langs"].values()) or 1
    top = sorted(data["langs"].items(), key=lambda kv: -kv[1])[:5]
    by = ly + 46
    basis = "BY CODE SIZE" if data.get("lang_basis") == "bytes" else "BY REPOSITORY"
    s.text(W, ly + 10, f"LANGUAGES {basis}", "mono", 11, "dim", "end", ls=1, cls="fi", style=delay(1.2))
    x = hx
    bw = W - hx
    ops = [1, .7, .48, .3, .18]
    s.css += """.seg{transform-box:fill-box;transform-origin:left;animation:seg 1.2s cubic-bezier(.2,.7,.2,1) both}
    @keyframes seg{from{transform:scaleX(0)}to{transform:scaleX(1)}}"""
    lab_x = hx
    for i, (name, v) in enumerate(top):
        w = bw * v / total
        s.rect(round(x, 1), by, max(round(w - 3, 1), 2), 8, stroke="none", fill="accent", cls="seg",
               style=delay(1.3 + i * .12) + f"fill-opacity:{ops[i]};")
        label = f"{name} {v / total * 100:.0f}%"
        s.rect(lab_x, by + 26, 8, 8, stroke="none", fill="accent", style=f"fill-opacity:{ops[i]}")
        s.text(lab_x + 14, by + 34, label, "mono", 12.5, "ink", cls="fi", style=delay(1.5 + i * .1))
        lab_x += 14 + measure(label, "mono", 12.5) + 28
        x += w
    s.line(0, 312.5, W, 312.5, cls="dr", style=delay(.4))
    s.text(0, 338, "SOURCE: GITHUB GRAPHQL API", "mono", 11, "dim", ls=1.2, cls="fi", style=delay(1.6))
    s.text(W, 338, f"UPDATED {data['updated']}  ·  REDRAWN DAILY BY GITHUB ACTIONS", "mono", 11,
           "dim", "end", ls=1.2, cls="fi", style=delay(1.6))
    return s


def main():
    if "--from-json" in sys.argv:
        with open(sys.argv[sys.argv.index("--from-json") + 1]) as f:
            data = json.load(f)
    else:
        data = fetch()
    for theme in THEMES:
        render(theme, data).save(ROOT, "activity.svg")
    print(f"activity: {data['total']} contributions, updated {data['updated']}")


if __name__ == "__main__":
    main()
