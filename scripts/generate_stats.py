"""
Fetches all-time contribution data for GH_USERNAME via the GitHub GraphQL API
and renders assets/t5_stats.svg as a mini contribution heatmap + summary line,
in the same terminal-scrollback style as the rest of the panels.

Env vars required:
  GH_TOKEN     - a Personal Access Token with at least the read:user scope
  GH_USERNAME  - the GitHub username to fetch stats for
"""
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(__file__))
from term_common import (
    BG, BORDER, ACCENT, ACCENT_DIM, TEXT_PRIMARY, TEXT_SECONDARY, MONO, W,
    panel, svg_close, prompt_line, out_line,
)

LEVELS = ["#161b1f", "#1f4d34", "#2f6b46", "#3fa066", ACCENT]


def bucket(count):
    if count == 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 9:
        return 3
    return 4


def fmt(date_str):
    if not date_str:
        return "-"
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    day = str(d.day)
    return d.strftime(f"%b {day}")


def compute_streaks(days):
    idx = len(days) - 1
    if idx >= 0 and days[idx][1] == 0:
        idx -= 1
    current_streak = 0
    while idx >= 0 and days[idx][1] > 0:
        current_streak += 1
        idx -= 1

    longest = 0
    run = 0
    run_start = None
    best_start, best_end = None, None
    for date_str, count in days:
        if count > 0:
            if run == 0:
                run_start = date_str
            run += 1
            if run > longest:
                longest = run
                best_start, best_end = run_start, date_str
        else:
            run = 0
    return current_streak, longest, best_start, best_end


def render(days, total):
    cell, gap = 9, 2
    step = cell + gap
    recent = days[-371:] if days else []
    cols = [recent[i:i+7] for i in range(0, len(recent), 7)]

    grid_w = len(cols) * step
    grid_x = (W - grid_w) / 2
    grid_y = 66

    H = 200
    svg = panel(H)
    svg.append(prompt_line(28, 44, "./contrib --stats"))

    for ci, col in enumerate(cols):
        for ri, (date_str, count) in enumerate(col):
            lvl = bucket(count)
            x = grid_x + ci * step
            y = grid_y + ri * step
            svg.append(f'<rect x="{x:.1f}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{LEVELS[lvl]}"/>')

    current_streak, longest, l_start, l_end = compute_streaks(days) if days else ("-", "-", None, None)

    summary_y = grid_y + 7 * step + 30
    parts = [
        (f"{total}", ACCENT), (" total contributions    ", TEXT_SECONDARY),
        (f"{current_streak}", ACCENT), (" day streak    ", TEXT_SECONDARY),
        (f"{longest}", ACCENT),
        (f" day best ({fmt(l_start)} \u2013 {fmt(l_end)})" if l_start else " day best", TEXT_SECONDARY),
    ]
    x = grid_x
    spans = "".join(f'<tspan fill="{color}">{text}</tspan>' for text, color in parts)
    svg.append(
        f'<text x="{grid_x}" y="{summary_y}" font-family="{MONO}" font-size="13.5">{spans}</text>'
    )

    svg.append(svg_close())
    return "\n".join(svg)


def render_placeholder():
    return render([], "-")


def main():
    import requests

    API_URL = "https://api.github.com/graphql"
    TOKEN = os.environ["GH_TOKEN"]
    USERNAME = os.environ.get("GH_USERNAME", "KyleLotter")
    HEADERS = {"Authorization": f"bearer {TOKEN}"}

    CREATED_QUERY = "query($login: String!) { user(login: $login) { createdAt } }"
    CALENDAR_QUERY = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }
    """

    def gql(query, variables):
        r = requests.post(API_URL, json={"query": query, "variables": variables}, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
        if "errors" in data:
            raise RuntimeError(data["errors"])
        return data["data"]

    created = gql(CREATED_QUERY, {"login": USERNAME})["user"]["createdAt"]
    start_year = int(created[:4])
    now = datetime.datetime.utcnow()
    all_days, total = [], 0

    year = start_year
    while year <= now.year:
        frm = datetime.datetime(year, 1, 1)
        to = min(datetime.datetime(year, 12, 31, 23, 59, 59), now)
        data = gql(CALENDAR_QUERY, {"login": USERNAME, "from": frm.isoformat() + "Z", "to": to.isoformat() + "Z"})
        cal = data["user"]["contributionsCollection"]["contributionCalendar"]
        total += cal["totalContributions"]
        for week in cal["weeks"]:
            for day in week["contributionDays"]:
                all_days.append((day["date"], day["contributionCount"]))
        year += 1

    all_days.sort(key=lambda d: d[0])
    svg = render(all_days, total)
    out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "t5_stats.svg")
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"total={total}")


if __name__ == "__main__":
    main()
