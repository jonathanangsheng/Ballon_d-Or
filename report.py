"""Write data/features/gaps.md (every missing field with its reason) and
data/features/coverage.md (rows filled per column for 2000-2015 / 2016-2025 / 2026)."""
import csv
from collections import defaultdict
from pathlib import Path

from build_features import COLUMNS
from build_windows import YEARS

FEAT = Path(__file__).parent / "data" / "features"
SPLITS = [("2000–2015", range(2000, 2016)), ("2016–2025", range(2016, 2026)), ("2026", range(2026, 2027))]

SOURCES = """## Source access (checked 2026-11-10)

| Source | Status | Effect |
|---|---|---|
| Transfermarkt | Every page, incl. robots.txt-allowed match logs, returns an AWS WAF CAPTCHA (HTTP 405) to an automated client | Not used. No match logs, minutes, assists, cards from it |
| FBref | Every page, incl. robots.txt, returns a Cloudflare challenge (HTTP 403) | Not used |
| Understat | Every URL returns a "We will come back soon" page (HTTP 200) | Not used. No xG for top-5 leagues 2014/15+ |
| Wikipedia (API) | OK, batched requests (50 pages/request), 3 s between requests | Windows, player articles, honours, trophy/award dates, tournament squads |
| StatsBomb open data (GitHub, attribution: StatsBomb) | OK | Match stats incl. xG for the competitions it releases in full |
| martj42/international_results (GitHub, CC0) | OK | Every international with dated goalscorers |
| openfootball (GitHub, public domain) | OK | Rounds of World Cups, Euros, some Copas; Champions League 2011-12 on |

Bot challenges were not bypassed. StatsBomb, martj42 and openfootball were added with the
user's approval because the listed sources were unreachable.
"""

DEFINITIONS = """## Definitions and rules

- **Buckets.** `league`, `ucl`, `club_other` (cups, super cups, Club World Cup, UEL), `national`
  (all internationals), `intl_tournament` (World Cup, Euro, Copa América, AFCON matches only; a
  subset of `national`).
- **A bucket is filled only when every match of the player's team in it, inside the window, is in
  the source.** StatsBomb league seasons are checked for a full double round-robin for the club;
  tournaments are checked against martj42's match list. StatsBomb's Barcelona 2004/05–2020/21 La
  Liga seasons hold only the matches Messi played, so they fail this check for every player.
- **Club for the window** (league bucket, UCL stage): used only when exactly one senior club spell
  in the player's Wikipedia infobox overlaps the window's years. Any transfer or loan in those
  years leaves the club unknown.
- **Minutes**: clock time on the pitch with stoppage time not counted (≤ 90, or ≤ 120 with extra
  time). Penalty shoot-outs are excluded from every stat. `red` includes second yellows; `yellow`
  counts only first yellows.
- **ko_ga / decisive_ga**: goals + assists in matches whose StatsBomb stage is not group/regular
  season. `decisive_ga` (all competitions) needs every club and national bucket complete.
- **GK columns** are filled only for players listed as goalkeeper; clean sheet = played the whole
  match in goal with no goal conceded.
- **Stage (0–6)**: 0 none / not in squad, 1 group or league phase (incl. UCL knockout play-offs),
  2 round of 32 or 16, 3 quarter-final, 4 semi-final or third-place match, 5 lost final, 6 won.
  `intl_stage` needs the player in the Wikipedia squad list. A dated title in the honours list
  sets 6 even when other data is missing.
- **Trophies**: honours entries marked as won, dated by the infobox of the linked edition article
  (or its "<year> … Final" article, a "Final ||" table row, or the latest date in the article
  inside the season). Counted when that date is in the window. Youth/Olympic honours excluded.
- **Awards**: entries in the honours section's individual-awards group whose label ends in the
  window's last year and whose date is on or after the window start and before the voting
  deadline. Ballon d'Or and its ceremony awards are never counted. Club-internal awards (linked
  only to a club-season article) are not counted.
"""


def main():
    gaps = list(csv.DictReader(open(FEAT / "row_gaps.csv", encoding="utf-8")))
    rows = {y: list(csv.DictReader(open(FEAT / f"{y}.csv", encoding="utf-8"))) for y in YEARS}
    windows = list(csv.DictReader(open(FEAT / "windows.csv", encoding="utf-8")))

    by = defaultdict(lambda: {"rows": 0, "years": set()})
    for g in gaps:
        e = by[(g["field"], g["reason"])]
        e["rows"] += 1
        e["years"].add(int(g["year"]))

    out = ["# Gaps in data/features", "",
           "Every field left blank, and why. Per-row detail: `data/features/row_gaps.csv`.", "",
           SOURCES, DEFINITIONS, "## Judging windows", ""]
    for w in windows:
        flag = w["voting_deadline_estimated"] == "true"
        out.append(f"- {w['year']}: {w['window_start']} – {w['window_end']}"
                   + (" — voting deadline estimated (ceremony − 30 days, no deadline found)" if flag else
                      f" — {w['notes']}"))
    out += ["", "Windows shorter than 10 months (warning from check_features.py): 2005, 2006 and "
            "2021, whose ceremonies were in late November. A press report puts the real 2021 "
            "deadline at 24 Oct 2021, but the only source reachable was a low-quality blog, so the "
            "estimate is kept.", "",
            "## Columns that are always blank", "",
            "| Column(s) | Reason |", "|---|---|",
            "| `ucl_*`, `club_other_*` match stats | No permitted source holds every UCL / cup match "
            "(Transfermarkt and FBref blocked; StatsBomb releases UCL finals only) |",
            "| `national_apps/minutes/assists/ko_ga/yellow/red`, national advanced | martj42 lists goals "
            "only; no permitted source has national-team line-ups for every match |",
            "| `apps`, `minutes`, `goals`, `assists`, `decisive_ga`, `yellow_cards`, `red_cards`, "
            "`gk_*` totals | Need every club and national bucket complete, never the case |",
            "| `match_rating_avg` | No permitted source publishes ratings |",
            "| Understat xG | Understat unreachable; xG comes only from StatsBomb where a bucket is complete |",
            "", "## Missing fields by reason", "",
            "| Field | Reason | Rows | Editions |", "|---|---|---|---|"]
    for (field, reason), e in sorted(by.items(), key=lambda kv: (kv[0][0], -kv[1]["rows"])):
        ys = sorted(e["years"])
        out.append(f"| `{field}` | {reason.replace('|', '/')} | {e['rows']} | "
                   f"{ys[0]}–{ys[-1]} ({len(ys)}) |")
    (FEAT / "gaps.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    cov = ["# Coverage of data/features", "",
           "Rows with a value in each column (blank = missing).", "",
           "| Column | " + " | ".join(f"{label} (n={sum(len(rows[y]) for y in yrs if y in rows)})"
                                      for label, yrs in SPLITS) + " |",
           "|---|" + "---|" * len(SPLITS)]
    for c in COLUMNS:
        if c in ("year", "name") or c.endswith("_coverage"):
            continue
        cells = []
        for _, yrs in SPLITS:
            rs = [r for y in yrs if y in rows for r in rows[y]]
            cells.append(str(sum(1 for r in rs if r[c] != "")))
        cov.append(f"| `{c}` | " + " | ".join(cells) + " |")
    (FEAT / "coverage.md").write_text("\n".join(cov) + "\n", encoding="utf-8")
    print("wrote gaps.md and coverage.md")


if __name__ == "__main__":
    main()
