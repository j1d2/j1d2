#!/usr/bin/env python3
"""Generate a public GitHub activity graph as an SVG.

The chart uses the contribution counts GitHub already shows on the public
profile. The image stores dates and counts only.
"""

import logging
import re
import urllib.request
from datetime import date, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

USERNAME = "j1d2"
OUTPUT_FILE = Path("assets/github-activity.svg")
WINDOW_DAYS = 31
CONTRIBUTIONS_URL = f"https://github.com/users/{USERNAME}/contributions"

COLORS = {
    "bg": "#0f172a",
    "title": "#a78bfa",
    "text": "#e2e8f0",
    "muted": "#94a3b8",
    "line": "#60a5fa",
    "area": "#60a5fa",
    "grid": "#2d3748",
}

DAY_RE = re.compile(
    r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*>\s*</td>\s*'
    r"<tool-tip[^>]*>\s*([^<]+)"
)


def fetch_public_contributions(username: str) -> list[tuple[date, int]]:
    """Download the public contribution calendar.

    Args:
        username: GitHub login whose public calendar to read.

    Returns:
        Date and contribution-count pairs, oldest first.

    Raises:
        RuntimeError: The calendar page did not contain contribution days.
    """
    url = f"https://github.com/users/{username}/contributions"
    request = urllib.request.Request(url, headers={"User-Agent": "j1d2-profile"})
    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")

    rows: list[tuple[date, int]] = []
    for raw_date, tip in DAY_RE.findall(html):
        tip = tip.strip()
        if tip.lower().startswith("no contribution"):
            count = 0
        else:
            match = re.search(r"(\d+)\s+contribution", tip)
            if match is None:
                continue
            count = int(match.group(1))
        rows.append((date.fromisoformat(raw_date), count))

    if not rows:
        raise RuntimeError(f"No public contribution days found for {username}")

    rows.sort()
    return rows


def _chart_path(days: list[tuple[date, int]]) -> str:
    """Build the area-chart SVG.

    Args:
        days: Date and count pairs, oldest first. One row per day.

    Returns:
        A complete SVG document.
    """
    width = 720
    height = 220
    left, right = 44, 696
    top, bottom = 52, 168
    counts = [count for _, count in days]
    peak = max(counts) if counts else 1
    ceiling = max(peak, 1)

    def x_at(index: int) -> float:
        if len(days) == 1:
            return (left + right) / 2
        return left + (right - left) * index / (len(days) - 1)

    def y_at(count: int) -> float:
        return bottom - (bottom - top) * (count / ceiling)

    coords = [(x_at(i), y_at(count)) for i, (_, count) in enumerate(days)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    area = (
        f"M {coords[0][0]:.1f},{bottom} "
        + " ".join(f"L {x:.1f},{y:.1f}" for x, y in coords)
        + f" L {coords[-1][0]:.1f},{bottom} Z"
    )

    grid = []
    for fraction in (0, 0.5, 1):
        y = bottom - (bottom - top) * fraction
        label = int(round(ceiling * fraction))
        grid.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" '
            f'stroke="{COLORS["grid"]}" stroke-width="1"/>'
            f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" '
            f'fill="{COLORS["muted"]}" font-size="11">{label}</text>'
        )

    labels = []
    step = 5
    for index, (day, _) in enumerate(days):
        if index % step != 0 and index != len(days) - 1:
            continue
        labels.append(
            f'<text x="{x_at(index):.1f}" y="{bottom + 22}" text-anchor="middle" '
            f'fill="{COLORS["muted"]}" font-size="11">{day.strftime("%b %-d")}</text>'
        )

    updated = datetime.now().strftime("%Y-%m-%d")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{USERNAME} GitHub activity">
  <rect width="{width}" height="{height}" rx="6" fill="{COLORS["bg"]}"/>
  <text x="{left}" y="28" fill="{COLORS["title"]}" font-size="16" font-weight="600" font-family="Segoe UI, Ubuntu, Sans-Serif">{USERNAME}'s Activity</text>
  <text x="{right}" y="28" text-anchor="end" fill="{COLORS["muted"]}" font-size="12" font-family="Segoe UI, Ubuntu, Sans-Serif">Last {len(days)} days</text>
  {"".join(grid)}
  <path d="{area}" fill="{COLORS["area"]}" fill-opacity="0.22"/>
  <polyline points="{line}" fill="none" stroke="{COLORS["line"]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
  {"".join(labels)}
  <text x="{right}" y="{height - 8}" text-anchor="end" fill="{COLORS["muted"]}" font-size="10" font-family="Segoe UI, Ubuntu, Sans-Serif">Updated: {updated}</text>
</svg>
'''


def main() -> None:
    """Write the activity SVG for the profile README."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    days = fetch_public_contributions(USERNAME)[-WINDOW_DAYS:]
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(_chart_path(days), encoding="utf-8")
    logger.info("Wrote %s (%s days)", OUTPUT_FILE, len(days))


if __name__ == "__main__":
    main()
