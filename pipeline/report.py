"""Write data/features/gaps.md (every missing field with its reason) and
data/features/coverage.md (rows filled per column for 2000-2015 / 2016-2025 / 2026)."""
import csv
from collections import defaultdict
from pathlib import Path

from build_features import COLUMNS
from build_windows import YEARS

FEAT = Path(__file__).parent.parent / "data" / "features"
SPLITS = [("2000–2015", range(2000, 2016)), ("2016–2025", range(2016, 2026)), ("2026", range(2026, 2027))]

SOURCES = """## Source access (checked 2026-11-10)

| Source | Status | Effect |
|---|---|---|
| Transfermarkt | Every page, incl. robots.txt-allowed match logs, returns an AWS WAF CAPTCHA (HTTP 405) to an automated client | Not used. No match logs, minutes, assists, cards from it |
| FBref | Every page, incl. robots.txt, returns a Cloudflare challenge (HTTP 403) | Not used |
| Understat | Every URL returns a "We will come back soon" page (HTTP 200) | Not used. No xG for top-5 leagues 2014/15+ |
| Wikipedia (API) | OK, batched requests (50 pages/request), 3 s between requests | Windows, player articles, honours, trophy/award dates, tournament squads, career-statistics tables (club season totals, international year totals, dated goal lists) |
| StatsBomb open data (GitHub, attribution: StatsBomb) | OK | Match stats incl. xG for the competitions it releases in full |
| martj42/international_results (GitHub, CC0) | OK | Every international with dated goalscorers |
| openfootball (GitHub, public domain) | OK | Rounds of World Cups, Euros, some Copas; Champions League 2011-12 on |
| engsoccerdata `champs` (GitHub, James Curley; free for non-commercial use with credit, package licence GPL ≥ 2) | OK | Champions League rounds 1999-00 to 2010-11 |
| 21st Century Spanish Football League Dataset (Zenodo, Sergio Lois, CC BY-NC 4.0; match data from BeSoccer) | OK | La Liga 2000-01 to 2021-22: line-ups, substitutions, goals, assists, cards by minute. Fills the league bucket where StatsBomb does not; no xG |
| Fjelstul World Cup Database (GitHub, CC BY-SA 4.0) | OK | Not a feature source: `validate_worldcup.py` cross-checks StatsBomb World Cup records against it |

Bot challenges were not bypassed. StatsBomb, martj42, openfootball, engsoccerdata, the La Liga
dataset and Fjelstul were added with the user's approval because the listed sources were
unreachable.
"""

DEFINITIONS = """## Definitions and rules

- **Buckets.** `league`, `ucl`, `club_other` (cups, super cups, Club World Cup, UEL), `national`
  (all internationals), `intl_tournament` (World Cup, Euro, Copa América, AFCON matches only; a
  subset of `national`).
- **A bucket is filled only when every match of the player's team in it, inside the window, is in
  the source.** StatsBomb league seasons are checked for a full double round-robin for the club;
  tournaments are checked against martj42's match list. StatsBomb's Barcelona 2004/05–2020/21 La
  Liga seasons hold only the matches Messi played, so they fail this check for every player.
  The La Liga dataset is used for the league bucket when StatsBomb fails: the nominee is the
  player with his infobox birth date and nationality, and every season the window touches must
  hold all of his team's matches (2 × (teams − 1)). Its assists run slightly higher than
  StatsBomb's (see README).
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
  UCL qualifying rounds count as 0; the 1999–2003 second group stage (last 16 teams) counts as 2.
  `intl_stage` needs the player in the Wikipedia squad list. A dated title in the honours list
  sets 6 even when other data is missing.
- **Trophies**: honours entries marked as won, dated by the infobox of the linked edition article
  (or its "<year> … Final" article, a "Final ||" table row, or the latest date in the article
  inside the season). Counted when that date is in the window. Youth/Olympic honours excluded.
- **Awards**: entries in the honours section's individual-awards group whose label ends in the
  window's last year and whose date is on or after the window start and before the voting
  deadline. An entry with no dated link is dated through the award's own article: the winners
  row naming the player and year, by the edition it links to (e.g. a Golden Ball by the
  tournament's final). Ballon d'Or and its ceremony awards are never counted. Club-internal awards
  (linked only to a club-season article) are not counted. One undated award blanks the count.
- **Club apps from Wikipedia** (Aug–Jul windows only): the player's career-statistics row
  for that season. League counts when the league season's dates (its article's infobox) lie in
  the window; UCL and cups count when the club-season article dates at least as many competitive
  matches as his appearances, all in the window. A "Europe" column counts as UCL only when its
  footnote names the Champions League alone. Minutes, assists and cards are not in these tables.
- **Club goals match by match** (every window): every club-season article linked from the
  player's career table for a season overlapping the window (a split season counts as 1 Jul –
  30 Jun, so July qualifiers fall in the Aug–Jul window that holds them) is read match by
  match (Football boxes, or results tables with a Scorers column), and goals dated inside the
  window are counted. A bucket counts only when, for every such season, the article's goals for
  the player in that competition equal his career-table season total; own goals and friendlies
  are excluded. Apps are not counted (match lists do not give line-ups).
- **National goals**: the dated list of international goals (in the article or its "List of
  international goals scored by …" article), used only when its length equals the year table's
  goal total; else martj42; else the year table. **National apps**: the year table, only for
  calendar windows where the country played no match between the voting deadline and 31 Dec.
- **Totals** (`apps`, `goals`, …) are the sum of league, ucl, club_other and national, filled only
  when all four are.
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
        out.append(f"- {w['year']}: {w['window_start']} – {w['window_end']} — {w['notes']}")
    out += ["", "Windows shorter than 10 months (warning from check_features.py): 2005, 2006 and "
            "2021, whose ceremonies were in late November. A press report puts the real 2021 "
            "deadline at 24 Oct 2021, but the only source reachable was a low-quality blog, so the "
            "estimate is kept.", "",
            "## Columns that are always or mostly blank", "",
            "| Column(s) | Reason |", "|---|---|",
            "| `ucl_*`, `club_other_*`, `national_*` minutes, assists, cards, advanced | No permitted "
            "source has every line-up (Transfermarkt and FBref blocked); Wikipedia tables give apps "
            "and goals only |",
            "| `league_*` minutes, assists, cards outside La Liga | Only StatsBomb (complete seasons) "
            "and the La Liga dataset (2000-01 to 2021-22) have every league line-up |",
            "| `league_*` xG, shots, key passes | StatsBomb only; the La Liga dataset has none |",
            "| club apps for 2000–2021 outside La Liga | Calendar-year windows split two seasons; "
            "season totals cannot be cut at the voting deadline, and match lists give scorers, not "
            "line-ups. La Liga players get league apps from the La Liga dataset's line-ups. Club "
            "goals (all years) are filled where the match lists pass the season-total check |",
            "| `national_apps` for 2022+ | Year totals do not split at 1 August |",
            "| `apps`, `minutes`, `assists`, `decisive_ga`, cards, `gk_*` totals | Need club and "
            "national values in the same window, which only `goals` reaches (2022+) |",
            "| `match_rating_avg` | No permitted source publishes ratings |",
            "| Understat xG | Understat unreachable; xG comes only from StatsBomb where a bucket is complete |",
            "| `intl_tournament_*` for 2026 (29 of 30) | martj42 holds the 2026 World Cup, so each nominee's team has tournament matches in the window, but StatsBomb open data has not released that World Cup, so the bucket fails the completeness check. Kvaratskhelia is filled because Georgia played no tournament match. No model run uses these columns |",
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
