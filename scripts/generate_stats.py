"""
Fetches all-time contribution data for GH_USERNAME via the GitHub GraphQL API
and renders assets/stats.svg in the same visual style as the rest of the
profile cards. Intended to run on a schedule via .github/workflows/update-stats.yml

Env vars required:
  GH_TOKEN     - a Personal Access Token with at least the read:user scope
  GH_USERNAME  - the GitHub username to fetch stats for
"""
import os
import sys
import datetime
import requests

sys.path.insert(0, os.path.dirname(__file__))
from svg_common import (
    BG, CARD_BG, BORDER, ACCENT, ACCENT_DIM, TEXT_PRIMARY, TEXT_SECONDARY,
    SANS, MONO, corner_brackets, card_frame, svg_open, svg_close, section_label,
)

API_URL = "https://api.github.com/graphql"
TOKEN = os.environ["GH_TOKEN"]
USERNAME = os.environ.get("GH_USERNAME", "KyleLotter")

HEADERS = {"Authorization": f"bearer {TOKEN}"}

CREATED_QUERY = """
query($login: String!) {
  user(login: $login) { createdAt }
}
"""

CALENDAR_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount }
        }
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


def fetch_all_days():
    created = gql(CREATED_QUERY, {"login": USERNAME})["user"]["createdAt"]
    start_year = int(created[:4])
    now = datetime.datetime.utcnow()
    all_days = []
    total = 0

    year = start_year
    while year <= now.year:
        frm = datetime.datetime(year, 1, 1)
        to = min(datetime.datetime(year, 12, 31, 23, 59, 59), now)
        data = gql(CALENDAR_QUERY, {
            "login": USERNAME,
            "from": frm.isoformat() + "Z",
            "to": to.isoformat() + "Z",
        })
        cal = data["user"]["contributionsCollection"]["contributionCalendar"]
        total += cal["totalContributions"]
        for week in cal["weeks"]:
            for day in week["contributionDays"]:
                all_days.append((day["date"], day["contributionCount"]))
        year += 1

    all_days.sort(key=lambda d: d[0])
    return all_days, total


def compute_streaks(days):
    # days: list of (date_str, count), ascending
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


def fmt(date_str):
    if not date_str:
        return ""
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return d.strftime("%b %-d") if os.name != "nt" else d.strftime("%b %d").replace(" 0", " ")


def render_svg(total, first_date, current_streak, longest, longest_start, longest_end):
    W, H = 880, 200
    col_w = W / 3

    svg = [svg_open(W, H)]
    svg.append(card_frame(W, H))
    svg.append(corner_brackets(W, H))
    svg.append(section_label("Contribution Stats", W / 2, 44, size=13, spacing="5px"))

    svg.append(f'<line x1="{col_w}" y1="66" x2="{col_w}" y2="{H-30}" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<line x1="{col_w*2}" y1="66" x2="{col_w*2}" y2="{H-30}" stroke="{BORDER}" stroke-width="1"/>')

    cx1, cx2, cx3 = col_w * 0.5, col_w * 1.5, col_w * 2.5

    svg.append(f'<text x="{cx1}" y="120" font-family="{SANS}" font-size="34" font-weight="700" fill="{TEXT_PRIMARY}" text-anchor="middle">{total}</text>')
    svg.append(f'<text x="{cx1}" y="145" font-family="{SANS}" font-size="12.5" fill="{TEXT_SECONDARY}" text-anchor="middle">Total Contributions</text>')
    svg.append(f'<text x="{cx1}" y="168" font-family="{MONO}" font-size="11" fill="{TEXT_SECONDARY}" text-anchor="middle">{fmt(first_date)} \u2013 Present</text>')

    r = 34
    svg.append(f'<circle cx="{cx2}" cy="102" r="{r}" fill="none" stroke="{ACCENT}" stroke-width="3"/>')
    svg.append(f'<text x="{cx2}" y="110" font-family="{SANS}" font-size="26" font-weight="700" fill="{TEXT_PRIMARY}" text-anchor="middle">{current_streak}</text>')
    svg.append(f'<text x="{cx2}" y="153" font-family="{SANS}" font-size="12.5" fill="{TEXT_SECONDARY}" text-anchor="middle">Current Streak</text>')
    today = datetime.datetime.utcnow().strftime("%b %-d")
    svg.append(f'<text x="{cx2}" y="176" font-family="{MONO}" font-size="11" fill="{TEXT_SECONDARY}" text-anchor="middle">{today}</text>')

    svg.append(f'<text x="{cx3}" y="120" font-family="{SANS}" font-size="34" font-weight="700" fill="{TEXT_PRIMARY}" text-anchor="middle">{longest}</text>')
    svg.append(f'<text x="{cx3}" y="145" font-family="{SANS}" font-size="12.5" fill="{TEXT_SECONDARY}" text-anchor="middle">Longest Streak</text>')
    rng = f"{fmt(longest_start)} \u2013 {fmt(longest_end)}" if longest_start else "\u2013"
    svg.append(f'<text x="{cx3}" y="168" font-family="{MONO}" font-size="11" fill="{TEXT_SECONDARY}" text-anchor="middle">{rng}</text>')

    svg.append(svg_close())
    return "\n".join(svg)


def main():
    days, total = fetch_all_days()
    first_date = days[0][0] if days else None
    current_streak, longest, l_start, l_end = compute_streaks(days)
    svg = render_svg(total, first_date, current_streak, longest, l_start, l_end)
    out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "stats.svg")
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"total={total} current_streak={current_streak} longest={longest} ({l_start} - {l_end})")


if __name__ == "__main__":
    main()
