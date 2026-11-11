# Gaps in data/features

Every field left blank, and why. Per-row detail: `data/features/row_gaps.csv`.

## Source access (checked 2026-11-10)

| Source | Status | Effect |
|---|---|---|
| Transfermarkt | Every page, incl. robots.txt-allowed match logs, returns an AWS WAF CAPTCHA (HTTP 405) to an automated client | Not used. No match logs, minutes, assists, cards from it |
| FBref | Every page, incl. robots.txt, returns a Cloudflare challenge (HTTP 403) | Not used |
| Understat | Every URL returns a "We will come back soon" page (HTTP 200) | Not used. No xG for top-5 leagues 2014/15+ |
| Wikipedia (API) | OK, batched requests (50 pages/request), 3 s between requests | Windows, player articles, honours, trophy/award dates, tournament squads, career-statistics tables (club season totals, international year totals, dated goal lists) |
| StatsBomb open data (GitHub, attribution: StatsBomb) | OK | Match stats incl. xG for the competitions it releases in full |
| martj42/international_results (GitHub, CC0) | OK | Every international with dated goalscorers |
| openfootball (GitHub, public domain) | OK | Rounds of World Cups, Euros, some Copas; Champions League 2011-12 on |

Bot challenges were not bypassed. StatsBomb, martj42 and openfootball were added with the
user's approval because the listed sources were unreachable.

## Definitions and rules

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

## Judging windows

- 2000: 2000-01-01 – 2000-11-19 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2001: 2001-01-01 – 2001-11-18 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2002: 2002-01-01 – 2002-11-12 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2003: 2003-01-01 – 2003-11-22 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2004: 2004-01-01 – 2004-11-13 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2005: 2005-01-01 – 2005-10-29 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2006: 2006-01-01 – 2006-10-28 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2007: 2007-01-01 – 2007-11-02 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2008: 2008-01-01 – 2008-11-02 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2009: 2009-01-01 – 2009-11-01 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2010: 2010-01-01 – 2010-12-11 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2011: 2011-01-01 – 2011-12-10 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2012: 2012-01-01 – 2012-12-08 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2013: 2013-01-01 – 2013-11-29 — Wikipedia: "voting was extended to 29 November 2013"
- 2014: 2014-01-01 – 2014-12-13 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2015: 2015-01-01 – 2015-12-12 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2016: 2016-01-01 – 2016-11-12 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2017: 2017-01-01 – 2017-11-07 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2018: 2018-01-01 – 2018-11-03 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2019: 2019-01-01 – 2019-11-02 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2021: 2021-01-01 – 2021-10-30 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2022: 2021-08-01 – 2022-07-31 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2023: 2022-08-01 – 2023-07-31 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2024: 2023-08-01 – 2024-07-31 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2025: 2024-08-01 – 2025-07-31 — voting deadline estimated (ceremony − 30 days, no deadline found)
- 2026: 2025-08-01 – 2026-07-31 — voting deadline estimated (ceremony − 30 days, no deadline found)

Windows shorter than 10 months (warning from check_features.py): 2005, 2006 and 2021, whose ceremonies were in late November. A press report puts the real 2021 deadline at 24 Oct 2021, but the only source reachable was a low-quality blog, so the estimate is kept.

## Columns that are always or mostly blank

| Column(s) | Reason |
|---|---|
| `ucl_*`, `club_other_*`, `national_*` minutes, assists, cards, advanced | No permitted source has every line-up (Transfermarkt and FBref blocked); Wikipedia tables give apps and goals only |
| club apps for 2000–2021 | Calendar-year windows split two seasons; season totals cannot be cut at the voting deadline, and match lists give scorers, not line-ups. Club goals (all years) are filled where the match lists pass the season-total check |
| `national_apps` for 2022+ | Year totals do not split at 1 August |
| `apps`, `minutes`, `assists`, `decisive_ga`, cards, `gk_*` totals | Need club and national values in the same window, which only `goals` reaches (2022+) |
| `match_rating_avg` | No permitted source publishes ratings |
| Understat xG | Understat unreachable; xG comes only from StatsBomb where a bucket is complete |

## Missing fields by reason

| Field | Reason | Rows | Editions |
|---|---|---|---|
| `apps` | needs league, ucl, club_other and national all filled | 721 | 2000–2026 (26) |
| `assists` | needs league, ucl, club_other and national all filled | 721 | 2000–2026 (26) |
| `awards_count` | undated award IFFHS Men's World Team 2024: no date found in linked article; award row has no dated edition link | 10 | 2024–2024 (1) |
| `awards_count` | undated award FIFPRO World 11 2025: no date found in linked article; award row has no dated edition link | 10 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2025: no date found in linked article; award row has no dated edition link | 9 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2023: no date found in linked article; award row has no dated edition link | 8 | 2023–2023 (1) |
| `awards_count` | undated award FIFPRO World 11 2026: no date found in linked article; award row has no dated edition link | 8 | 2026–2026 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2017: no date found in linked article; award row has no dated edition link | 6 | 2017–2017 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2018: no date found in linked article; award row has no dated edition link | 6 | 2018–2018 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2021: no date found in linked article; award row has no dated edition link | 6 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2022: no date found in linked article; award row has no dated edition link | 6 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS 2024: no date found in linked article; player not found in the award article's row for this year | 6 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' European Men's Team of the Season 2024–25: no date found in linked article; no row for this year in the award article | 6 | 2025–2025 (1) |
| `awards_count` | undated award UEFA Team of the Year 2003: no date found in linked article; player not found in the award article's row for this year | 5 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Team of the Year 2005: no date found in linked article; player not found in the award article's row for this year | 5 | 2005–2005 (1) |
| `awards_count` | undated award ESM Team of the Year 2008–09: no date found in linked article; award row has no dated edition link | 5 | 2009–2009 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2019: no date found in linked article; award row has no dated edition link | 5 | 2019–2019 (1) |
| `awards_count` | undated award IFFHS 2024: no date found in linked article; award row has no dated edition link | 5 | 2024–2024 (1) |
| `awards_count` | undated award UNFP 2024–25: no date found in linked article; no row for this year in the award article | 5 | 2025–2025 (1) |
| `awards_count` | undated award FIFA 100 2004: no date found in linked article; player not found in the award article's row for this year | 4 | 2004–2004 (1) |
| `awards_count` | undated award FIFPro World XI 2007: no date found in linked article; award row has no dated edition link | 4 | 2007–2007 (1) |
| `awards_count` | undated award ESM Team of the Year 2009–10: no date found in linked article; award row has no dated edition link | 4 | 2010–2010 (1) |
| `awards_count` | undated award UEFA 2015–16: no date found in linked article; player not found in the award article's row for this year | 4 | 2016–2016 (1) |
| `awards_count` | undated award UEFA 2016–17: no date found in linked article; player not found in the award article's row for this year | 4 | 2017–2017 (1) |
| `awards_count` | undated award CAF Team of the Year 2019: no date found in linked article; award row has no dated edition link | 4 | 2019–2019 (1) |
| `awards_count` | undated award IFFHS 2022: no date found in linked article; player not found in the award article's row for this year | 4 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS 2023: no date found in linked article; player not found in the award article's row for this year | 4 | 2023–2023 (1) |
| `awards_count` | undated award FIFPRO Men's World 11 2024: no date found in linked article; award row has no dated edition link | 4 | 2024–2024 (1) |
| `awards_count` | undated award PFA Team of the Year 2025–26 Premier League: no date found in linked article; no row for this year in the award article | 4 | 2026–2026 (1) |
| `awards_count` | undated award ESM Team of the Year 1999–2000: no date found in linked article; award row has no dated edition link | 3 | 2000–2000 (1) |
| `awards_count` | undated award Onze Mondial 2000: no date found in linked article; player not found in the award article's row for this year | 3 | 2000–2000 (1) |
| `awards_count` | undated award ESM Team of the Year 2000–01: no date found in linked article; award row has no dated edition link | 3 | 2001–2001 (1) |
| `awards_count` | undated award UEFA Team of the Year 2001: no date found in linked article; player not found in the award article's row for this year | 3 | 2001–2001 (1) |
| `awards_count` | undated award ESM Team of the Year 2001–02: no date found in linked article; award row has no dated edition link | 3 | 2002–2002 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' [[Bundesliga]] Team of the Season 2001–02: no date found in linked article; no row for this year in the award article | 3 | 2002–2002 (1) |
| `awards_count` | undated award ESM Team of the Year 2002–03: no date found in linked article; award row has no dated edition link | 3 | 2003–2003 (1) |
| `awards_count` | undated award FIFPro World XI 2005: no date found in linked article; award row has no dated edition link | 3 | 2005–2005 (1) |
| `awards_count` | undated award ESM Team of the Year 2004–05: no date found in linked article; award row has no dated edition link | 3 | 2005–2005 (1) |
| `awards_count` | undated award CAF Team of the Year 2005: no date found in linked article; award row has no dated edition link | 3 | 2005–2005 (1) |
| `awards_count` | undated award FIFPro World XI 2006: no date found in linked article; award row has no dated edition link | 3 | 2006–2006 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2006: no date found in linked article; player not found in the award article's row for this year | 3 | 2006–2006 (1) |
| `awards_count` | undated award ESM Team of the Year 2005–06: no date found in linked article; award row has no dated edition link | 3 | 2006–2006 (1) |
| `awards_count` | undated award FIFPro World XI 2006: no date found in linked article; player not found in the award article's row for this year | 3 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Team of the Year 2007: no date found in linked article; player not found in the award article's row for this year | 3 | 2007–2007 (1) |
| `awards_count` | undated award FIFPro World XI 2007: no date found in linked article; player not found in the award article's row for this year | 3 | 2007–2007 (1) |
| `awards_count` | undated award CAF Team of the Year 2009: no date found in linked article; award row has no dated edition link | 3 | 2009–2009 (1) |
| `awards_count` | undated award CAF Team of the Year 2010: no date found in linked article; award row has no dated edition link | 3 | 2010–2010 (1) |
| `awards_count` | undated award Goal of the Month in Germany 2010: no date found in linked article; award row has no dated edition link | 3 | 2010–2010 (1) |
| `awards_count` | undated award ESM Team of the Year 2010–11: no date found in linked article; award row has no dated edition link | 3 | 2011–2011 (1) |
| `awards_count` | undated award Ligue 1 Player of the Month 2014: no date found in linked article; player not found in the award article's row for this year | 3 | 2014–2014 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' World Team 2015: no date found in linked article; no row for this year in the award article | 3 | 2015–2015 (1) |
| `awards_count` | undated award Paris Saint-Germain 2015: no date found in linked article; award row has no dated edition link | 3 | 2015–2015 (1) |
| `awards_count` | undated award PFA Player of the Month 2018: no date found in linked article; player not found in the award article's row for this year | 3 | 2018–2018 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2019: no date found in linked article; player not found in the award article's row for this year | 3 | 2019–2019 (1) |
| `awards_count` | undated award Sports Illustrated 2010–2019: no date found in linked article; player not found in the award article's row for this year | 3 | 2019–2019 (1) |
| `awards_count` | undated award ESM Team of the Year 2020–21: no date found in linked article; award row has no dated edition link | 3 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS 2021: no date found in linked article; player not found in the award article's row for this year | 3 | 2021–2021 (1) |
| `awards_count` | undated award PFA 2022: no date found in linked article; player not found in the award article's row for this year | 3 | 2022–2022 (1) |
| `awards_count` | undated award Bundesliga Player of the Month 2022: no date found in linked article; no row for this year in the award article | 3 | 2022–2022 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2023: no date found in linked article; player not found in the award article's row for this year | 3 | 2023–2023 (1) |
| `awards_count` | undated award FIFPRO World 11 2024: no date found in linked article; award row has no dated edition link | 3 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' Premier League Team of the Season 2024–25: no date found in linked article; no row for this year in the award article | 3 | 2025–2025 (1) |
| `awards_count` | undated award UEFA Team of the Year 2002: no date found in linked article; player not found in the award article's row for this year | 2 | 2002–2002 (1) |
| `awards_count` | undated award FIFA XI 2002: no date found in linked article; player not found in the award article's row for this year | 2 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Team of the Year 2004: no date found in linked article; player not found in the award article's row for this year | 2 | 2004–2004 (1) |
| `awards_count` | undated award Ligue 1 Player of the Month 2004: no date found in linked article; player not found in the award article's row for this year | 2 | 2004–2004 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2005: no date found in linked article; award row has no dated edition link | 2 | 2005–2005 (1) |
| `awards_count` | undated award FIFA World Player of the Year 2006: no date found in linked article; award row has no dated edition link | 2 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Team of the Year 2006: no date found in linked article; player not found in the award article's row for this year | 2 | 2006–2006 (1) |
| `awards_count` | undated award CAF Team of the Year 2006: no date found in linked article; award row has no dated edition link | 2 | 2006–2006 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2007: no date found in linked article; player not found in the award article's row for this year | 2 | 2007–2007 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2008: no date found in linked article; player not found in the award article's row for this year | 2 | 2008–2008 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' Bundesliga Team of the Season 2007–08: no date found in linked article; no row for this year in the award article | 2 | 2008–2008 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2008: no date found in linked article; player not found in the award article's row for this year | 2 | 2008–2008 (1) |
| `awards_count` | undated award BBC Goal of the Month 2009: no date found in linked article; player not found in the award article's row for this year | 2 | 2009–2009 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2009: no date found in linked article; player not found in the award article's row for this year | 2 | 2009–2009 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' Bundesliga Team of the Season 2008–09: no date found in linked article; no row for this year in the award article | 2 | 2009–2009 (1) |
| `awards_count` | undated award IFFHS Best Goalkeeper of the Past 25 Years 1987–2012: no date found in linked article; award row has no dated edition link | 2 | 2012–2012 (1) |
| `awards_count` | undated award CAF Team of the Year 2012: no date found in linked article; award row has no dated edition link | 2 | 2012–2012 (1) |
| `awards_count` | undated award Paris Saint-Germain 2012: no date found in linked article; award row has no dated edition link | 2 | 2012–2012 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' Bundesliga Team of the Season 2012–13: no date found in linked article; no row for this year in the award article | 2 | 2013–2013 (1) |
| `awards_count` | undated award FIFA Confederations Cup Castrol Index Top XI 2013: no date found in linked article; no row for this year in the award article | 2 | 2013–2013 (1) |
| `awards_count` | undated award Premios Univision Deportes 2014: no date found in linked article; player not found in the award article's row for this year | 2 | 2014–2014 (1) |
| `awards_count` | undated award Silbernes Lorbeerblatt 2014: no date found in linked article; player not found in the award article's row for this year | 2 | 2014–2014 (1) |
| `awards_count` | undated award ''[[France Football]]'' World XI 2015: no date found in linked article; no row for this year in the award article | 2 | 2015–2015 (1) |
| `awards_count` | undated award La Liga Player of the Month 2016: no date found in linked article; award row has no dated edition link | 2 | 2016–2016 (1) |
| `awards_count` | undated award CAF Team of the Year 2016: no date found in linked article; award row has no dated edition link | 2 | 2016–2016 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2018: no date found in linked article; player not found in the award article's row for this year | 2 | 2018–2018 (1) |
| `awards_count` | undated award CAF Team of the Year 2018: no date found in linked article; award row has no dated edition link | 2 | 2018–2018 (1) |
| `awards_count` | undated award Premier League Player of the Month 2018: no date found in linked article; award row has no dated edition link | 2 | 2018–2018 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2018: no date found in linked article; player not found in the award article's row for this year | 2 | 2018–2018 (1) |
| `awards_count` | undated award ''[[Sports Illustrated]]'' Premier League Team of the Decade 2010–2019: no date found in linked article; no row for this year in the award article | 2 | 2019–2019 (1) |
| `awards_count` | undated award PFA Player of the Month 2019: no date found in linked article; player not found in the award article's row for this year | 2 | 2019–2019 (1) |
| `awards_count` | undated award BBC Goal of the Month 2019: no date found in linked article; player not found in the award article's row for this year | 2 | 2019–2019 (1) |
| `awards_count` | undated award UNFP 2018–19: no date found in linked article; no row for this year in the award article | 2 | 2019–2019 (1) |
| `awards_count` | undated award Bundesliga 2019: no date found in linked article; player not found in the award article's row for this year | 2 | 2019–2019 (1) |
| `awards_count` | undated award UEFA Nations League Finals Team of the Tournament 2019: no date found in linked article; no row for this year in the award article | 2 | 2019–2019 (1) |
| `awards_count` | undated award La Liga Player of the Month 2021: no date found in linked article; award row has no dated edition link | 2 | 2021–2021 (1) |
| `awards_count` | undated award PFA Player of the Month 2021: no date found in linked article; player not found in the award article's row for this year | 2 | 2021–2021 (1) |
| `awards_count` | undated award BBC Goal of the Month 2021: no date found in linked article; player not found in the award article's row for this year | 2 | 2021–2021 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2021: no date found in linked article; player not found in the award article's row for this year | 2 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS 2021: no date found in linked article; award row has no dated edition link | 2 | 2021–2021 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2022: no date found in linked article; player not found in the award article's row for this year | 2 | 2022–2022 (1) |
| `awards_count` | undated award ESPN 2022–23: no date found in linked article; player not found in the award article's row for this year | 2 | 2023–2023 (1) |
| `awards_count` | undated award ESM Team of the Season 2022–23: no date found in linked article; award row has no dated edition link | 2 | 2023–2023 (1) |
| `awards_count` | undated award CAF Team of the Year 2023: no date found in linked article; award row has no dated edition link | 2 | 2023–2023 (1) |
| `awards_count` | undated award PFA Player of the Month 2023: no date found in linked article; player not found in the award article's row for this year | 2 | 2023–2023 (1) |
| `awards_count` | undated award Serie A Player of the Month 2023: no date found in linked article; award row has no dated edition link | 2 | 2023–2023 (1) |
| `awards_count` | undated award Bundesliga 2023: no date found in linked article; player not found in the award article's row for this year | 2 | 2023–2023 (1) |
| `awards_count` | undated award ''The Athletic'' Premier League Team of the Season 2023–24: no date found in linked article; no row for this year in the award article | 2 | 2024–2024 (1) |
| `awards_count` | undated award UNFP 2023–24: no date found in linked article; no row for this year in the award article | 2 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' Ligue 1 Team of the Season 2023–24: no date found in linked article; no row for this year in the award article | 2 | 2024–2024 (1) |
| `awards_count` | undated award Globe Soccer Awards – Emerging Player 2024: no date found in linked article; award row has no dated edition link | 2 | 2024–2024 (1) |
| `awards_count` | undated award Bundesliga 2024: no date found in linked article; player not found in the award article's row for this year | 2 | 2024–2024 (1) |
| `awards_count` | undated award IFFHS 2025: no date found in linked article; player not found in the award article's row for this year | 2 | 2025–2025 (1) |
| `awards_count` | undated award Bundesliga Player of the Month 2025: no date found in linked article; no row for this year in the award article | 2 | 2025–2025 (1) |
| `awards_count` | undated award FIFPRO Men's World 11 2026: no date found in linked article; award row has no dated edition link | 2 | 2026–2026 (1) |
| `awards_count` | undated award UNFP 2025–26: no date found in linked article; no row for this year in the award article | 2 | 2026–2026 (1) |
| `awards_count` | undated award Portuguese Footballer of the Year 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award La Liga Foreign Player of the Year 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award World Soccer Player of the Year 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award El País King of European Soccer 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award RSSSF 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award FIFA 2000: no date found in linked article; player not found in the award article's row for this year | 1 | 2000–2000 (1) |
| `awards_count` | undated award Onze d'Or 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award 2nd French Player of the Century (France Football) 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award Ukrainian Footballer of the Year 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award ADN Eastern European Footballer of the Season 2000: no date found in linked article; no row for this year in the award article | 1 | 2000–2000 (1) |
| `awards_count` | undated award French Player of the Year 2000: no date found in linked article; no row for this year in the award article | 1 | 2000–2000 (1) |
| `awards_count` | undated award Serie A Defender of the Year 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award IFFHS World's Top Goal Scorer 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award UEFA Club Football Awards 1999–2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award La Liga's Team of the Decade 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award Most assists in the Premier League 1999–2000: no date found in linked article; no row for this year in the award article | 1 | 2000–2000 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award ESM Team of the Year 1999–00: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award Turkish Footballer of the Year 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award Primeira Liga top goalscorer 1999–2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award Taça de Portugal top goalscorer 1999–00: no date found in linked article; player not found in the award article's row for this year | 1 | 2000–2000 (1) |
| `awards_count` | undated award Golden Ball (Czech Republic) 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award Czech Footballer of the Year 2000: no date found in linked article; player not found in the award article's row for this year | 1 | 2000–2000 (1) |
| `awards_count` | undated award Onze de Onze 2000: no date found in linked article; no row for this year in the award article | 1 | 2000–2000 (1) |
| `awards_count` | undated award Best Bundesliga Keeper 2000: no date found in linked article; no row for this year in the award article | 1 | 2000–2000 (1) |
| `awards_count` | undated award Best European Goalkeeper 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award UEFA Club Goalkeeper of the Year 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award German Footballer of the Year 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award Pirata d'Oro (Inter Milan Player of the Year) 2000: no date found in linked article; no row for this year in the award article | 1 | 2000–2000 (1) |
| `awards_count` | undated award Sir Matt Busby Player of the Year 2000: no date found in linked article; award row has no dated edition link | 1 | 2000–2000 (1) |
| `awards_count` | undated award FWA Footballer of the Year 2000: no date found in linked article; player not found in the award article's row for this year | 1 | 2000–2000 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2000: no date found in linked article; player not found in the award article's row for this year | 1 | 2000–2000 (1) |
| `awards_count` | undated award ''World Soccer'' World Player of the Year 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award Onze d'Argent 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award 2nd place 2001: no date found in linked article; no row for this year in the award article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Sportske Novosti award 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award Best Bundesliga Keeper 2001: no date found in linked article; no row for this year in the award article | 1 | 2001–2001 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award Best European Goalkeeper 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award UEFA Club Goalkeeper of the Year 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award UEFA Champions League Final Man of the Match 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award German Footballer of the Year 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award UEFA Fair-Play Award 2001: no date found in linked article; no row for this year in the award article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Most assists in the Premier League 2000–01: no date found in linked article; no row for this year in the award article | 1 | 2001–2001 (1) |
| `awards_count` | undated award BBC Sports Personality of the Year 2001: no date found in linked article; player not found in the award article's row for this year | 1 | 2001–2001 (1) |
| `awards_count` | undated award Serie A Italian Footballer of the Year 2001: no date found in linked article; player not found in the award article's row for this year | 1 | 2001–2001 (1) |
| `awards_count` | undated award La Liga top assist provider 2000–01: no date found in linked article; no row for this year in the award article | 1 | 2001–2001 (1) |
| `awards_count` | undated award La Liga Foreign Player of the Year 2001: no date found in linked article; player not found in the award article's row for this year | 1 | 2001–2001 (1) |
| `awards_count` | undated award Ukrainian Footballer of the Year 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award Onze d'Or 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award El País European Player of the Year 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award UEFA Club Footballer of the Year 2001: no date found in linked article; player not found in the award article's row for this year | 1 | 2001–2001 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2001: no date found in linked article; no row for this year in the award article | 1 | 2001–2001 (1) |
| `awards_count` | undated award SFWA Footballer of the Year 2001: no date found in linked article; player not found in the award article's row for this year | 1 | 2001–2001 (1) |
| `awards_count` | undated award SPFA Players' Player of the Year 2001: no date found in linked article; player not found in the award article's row for this year | 1 | 2001–2001 (1) |
| `awards_count` | undated award Serie A Defender of the Year 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award Onze de Onze 2001: no date found in linked article; player not found in the award article's row for this year | 1 | 2001–2001 (1) |
| `awards_count` | undated award UEFA Club Football Awards 2000–01: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award ESM Team of the Season 2000–01: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award Onze Mondial 2001: no date found in linked article; player not found in the award article's row for this year | 1 | 2001–2001 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award Danish Footballer of the Year 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award Premio Nazionale Carriera Esemplare "Gaetano Scirea" 2001: no date found in linked article; award row has no dated edition link | 1 | 2001–2001 (1) |
| `awards_count` | undated award Gran Galà del Calcio 'Best Football Book' Award 2001: no date found in linked article; player not found in the award article's row for this year | 1 | 2001–2001 (1) |
| `awards_count` | undated award Eurochampion Prize Serie A Foreign Footballer of the Year - 2000-01 2000-01: no date found in linked article; no row for this year in the award article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Serie A Team of the Season 1994–95, 1998-99, 2000-01 2000-01: no date found in linked article; no row for this year in the award article | 1 | 2001–2001 (1) |
| `awards_count` | undated award ''[[World Soccer (magazine)/World Soccer]]'' magazine [[World Soccer Player of the Year/World Player of the Year]] (3) 2002: no date found in linked article; no row for this year in the award article | 1 | 2002–2002 (1) |
| `awards_count` | undated award RSSSF 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award Onze d'Or 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award Intercontinental Cup Most Valuable Player 2002: no date found in linked article; no row for this year in the award article | 1 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Team of the Year 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award BBC World Sport Star of the Year 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award Onze Mondial 2002: no date found in linked article; player not found in the award article's row for this year | 1 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Club Defender of the Year 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award Best Bundesliga Keeper 2002: no date found in linked article; no row for this year in the award article | 1 | 2002–2002 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' Bundesliga Team of the Season 2001–02: no date found in linked article; no row for this year in the award article | 1 | 2002–2002 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award Best European Goalkeeper 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Club Goalkeeper of the Year 2002: no date found in linked article; player not found in the award article's row for this year | 1 | 2002–2002 (1) |
| `awards_count` | undated award Onze d'Argent 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award FIFA 2002: no date found in linked article; player not found in the award article's row for this year | 1 | 2002–2002 (1) |
| `awards_count` | undated award ''ESM'' Team of the Year 2001–02: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award France Football French Player of the Year 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award El País European Player of the Year 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Club Footballer of the Year 2002: no date found in linked article; player not found in the award article's row for this year | 1 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2002: no date found in linked article; player not found in the award article's row for this year | 1 | 2002–2002 (1) |
| `awards_count` | undated award Footballer of the Year (Germany) 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award kicker Man of the Year (Mann des Jahres) 2002: no date found in linked article; no row for this year in the award article | 1 | 2002–2002 (1) |
| `awards_count` | undated award World XI 2002: no date found in linked article; player not found in the award article's row for this year | 1 | 2002–2002 (1) |
| `awards_count` | undated award Premier League Player of the Month 2002: no date found in linked article; player not found in the award article's row for this year | 1 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Champions League Top Assist Provider 2001–02: no date found in linked article; no row for this year in the award article | 1 | 2002–2002 (1) |
| `awards_count` | undated award IFFHS World's Top Goal Scorer of the Year 2002: no date found in linked article; player not found in the award article's row for this year | 1 | 2002–2002 (1) |
| `awards_count` | undated award FIFA World Cup Fans' All-Star Team 2002: no date found in linked article; no row for this year in the award article | 1 | 2002–2002 (1) |
| `awards_count` | undated award African Footballer of the Year 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award BBC African Footballer of the Year 2002: no date found in linked article; award row has no dated edition link | 1 | 2002–2002 (1) |
| `awards_count` | undated award Golden Ball (Czech Republic) 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award Czech Footballer of the Year 2003: no date found in linked article; player not found in the award article's row for this year | 1 | 2003–2003 (1) |
| `awards_count` | undated award Serie A Foreign Footballer of the Year 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award Guerin d'Oro 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Club Best Midfielder of the Year 2002–03: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award World Soccer Awards Player of the Year 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award RSSSF 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award Onze d'Or 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award French Player of the Year 2003: no date found in linked article; no row for this year in the award article | 1 | 2003–2003 (1) |
| `awards_count` | undated award IFFHS 2003: no date found in linked article; player not found in the award article's row for this year | 1 | 2003–2003 (1) |
| `awards_count` | undated award Onze de Onze 2003: no date found in linked article; no row for this year in the award article | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA President's Award 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award Onze d'Argent 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award ''ESM'' Team of the Year 2002–03: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award El País European Player of the Year 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award BBC Goal of the Month 2003: no date found in linked article; player not found in the award article's row for this year | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Club Forward of the Year 2002–03: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award 3rd place 2003: no date found in linked article; no row for this year in the award article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Onze Mondial 2003: no date found in linked article; player not found in the award article's row for this year | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Club Defender of the Year 2003: no date found in linked article; player not found in the award article's row for this year | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Club Goalkeeper of the Year 2002–03: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award Best European Goalkeeper 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award England Player of the Year 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award Laureus World Sports Awards 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2003: no date found in linked article; no row for this year in the award article | 1 | 2003–2003 (1) |
| `awards_count` | undated award European Golden Shoe 2002–03: no date found in linked article; player not found in the award article's row for this year | 1 | 2003–2003 (1) |
| `awards_count` | undated award Serie A Defender of the Year 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award Onze de Onze 2003: no date found in linked article; player not found in the award article's row for this year | 1 | 2003–2003 (1) |
| `awards_count` | undated award Serie A Italian Footballer of the Year 2003: no date found in linked article; player not found in the award article's row for this year | 1 | 2003–2003 (1) |
| `awards_count` | undated award Footballer of the Year (Germany) 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' [[Bundesliga]] Team of the Season 2002–03: no date found in linked article; no row for this year in the award article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Romanian Footballer of the Year 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award Ligue 1 Goal of The Year 2003: no date found in linked article; award row has no dated edition link | 1 | 2003–2003 (1) |
| `awards_count` | undated award Ukrainian Footballer of the Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award ADN Eastern European Footballer of the Season 2004: no date found in linked article; no row for this year in the award article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Serie A Goal of the Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Baltic and Commonwealth of Independent States Footballer of the Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Year 2004: no date found in linked article; no row for this year in the award article | 1 | 2004–2004 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2003–04: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Portuguese League Footballer of the Year 2003–04: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award World Soccer Magazine World Player of The Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award RSSSF 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award European Golden Shoe 2003–04: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Premier League Player of the Month 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award French Player of the Year 2004: no date found in linked article; player not found in the award article's row for this year | 1 | 2004–2004 (1) |
| `awards_count` | undated award Greek Male Athlete of the Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Pirata d'Oro ([[Inter Milan/Internazionale]] Player of the Year) 2004: no date found in linked article; no row for this year in the award article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Copa América Golden Shoe 2004: no date found in linked article; no row for this year in the award article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Golden Ball (Czech Republic) 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Czech Footballer of the Year 2004: no date found in linked article; player not found in the award article's row for this year | 1 | 2004–2004 (1) |
| `awards_count` | undated award UEFA European Championship Team of the Tournament 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Golden Foot 2004: no date found in linked article; player not found in the award article's row for this year | 1 | 2004–2004 (1) |
| `awards_count` | undated award Golden Boy Award 2004: no date found in linked article; player not found in the award article's row for this year | 1 | 2004–2004 (1) |
| `awards_count` | undated award UEFA Club Best Defender of the Year 2003–04: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Eurosport 2004: no date found in linked article; player not found in the award article's row for this year | 1 | 2004–2004 (1) |
| `awards_count` | undated award Pegasus Award 2004: no date found in linked article; no row for this year in the award article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Stor Grabb 2004: no date found in linked article; no row for this year in the award article | 1 | 2004–2004 (1) |
| `awards_count` | undated award African Player of the Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Serie A Foreign Footballer of the Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award England Player of the Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Chelsea Player of the Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Onze d'Or 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award ''ESM'' Team of the Year 2003–04: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award UEFA Best European Player of the Past 50 Years 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award UEFA Super Cup Man of the Match 2004: no date found in linked article; no row for this year in the award article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Serie A Defender of the Year 2004: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award Don Balón Award 2003–04: no date found in linked article; award row has no dated edition link | 1 | 2004–2004 (1) |
| `awards_count` | undated award World Soccer Magazine World Player of The Year 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award RSSSF 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award UEFA Club Forward of the Year 2004–05: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award Onze d'Or 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award FIFPro Player of the Season 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award FWA Footballer of the Year 2005: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award PFA Fans' Player of the Year 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award England Player of the Year 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award Chelsea Player of the Year 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award UEFA Club Footballer of the Year 2005: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award Onze d'Argent 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award Liverpool Fans Online Player of the Season 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award European Golden Shoe 2004–05: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award French Player of the Year 2005: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award Ukrainian Footballer of the Year 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award ADN Eastern European Footballer of the Season 2005: no date found in linked article; no row for this year in the award article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Baltic and Commonwealth of Independent States Footballer of the Year 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award Golden Foot 2005: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Year 2005: no date found in linked article; no row for this year in the award article | 1 | 2005–2005 (1) |
| `awards_count` | undated award IFFHS World's Top Goal Scorer 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award Serie A Most Loved Player 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award Guldbollen 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2005: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2004–05: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award African Player of the Year 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2004–05: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award UEFA Club Defender of the Year 2005: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award FIFPro World XI 2005: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award Most Artistic Player by [[Marca (newspaper)/Marca]] 2005: no date found in linked article; no row for this year in the award article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Czech Footballer of the Year 2005: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award Golden Ball (Czech Republic) 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award Best European Goalkeeper 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award UEFA Club Football Awards 2005: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award Footballer of the Year (Germany) 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' [[Bundesliga]] Team of the Season 2004–05: no date found in linked article; no row for this year in the award article | 1 | 2005–2005 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2005: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2005: no date found in linked article; award row has no dated edition link | 1 | 2005–2005 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2005: no date found in linked article; no row for this year in the award article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Ligue 1 Player of the Year 2004–05: no date found in linked article; player not found in the award article's row for this year | 1 | 2005–2005 (1) |
| `awards_count` | undated award Serie A Defender of the Year 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award World Soccer Player of the Year 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award Serie A Italian Footballer of the Year 2006: no date found in linked article; player not found in the award article's row for this year | 1 | 2006–2006 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award Serie A "Fan" Award 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award Onze d'Or 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award French Player of the Year 2006: no date found in linked article; no row for this year in the award article | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFPro Player of the Season 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Team of the Year 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award African Cup of Nations top goalscorer 2006: no date found in linked article; player not found in the award article's row for this year | 1 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Club Forward of the Year 2006: no date found in linked article; player not found in the award article's row for this year | 1 | 2006–2006 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award Bundesliga Player of the Season 2005–06: no date found in linked article; player not found in the award article's row for this year | 1 | 2006–2006 (1) |
| `awards_count` | undated award Bundesliga top assist provider 2005–06: no date found in linked article; no row for this year in the award article | 1 | 2006–2006 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' Bundesliga Team of the Season 2005–06: no date found in linked article; no row for this year in the award article | 1 | 2006–2006 (1) |
| `awards_count` | undated award African Footballer of the Year 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award Ivory Coast Player of the Year 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFA World Cup top assists provider 2006: no date found in linked article; no row for this year in the award article | 1 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Goalkeeper of the Year 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Club Football Awards 2005–06: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFA World Cup All-Star Team 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2005–06: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award CNID Best Portuguese Athlete Abroad 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award Serie A Foreign Footballer of the Year 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2006: no date found in linked article; player not found in the award article's row for this year | 1 | 2006–2006 (1) |
| `awards_count` | undated award Etoile d'Or 2006: no date found in linked article; no row for this year in the award article | 1 | 2006–2006 (1) |
| `awards_count` | undated award Onze de Bronze 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFA World Cup All-star team 2006: no date found in linked article; no row for this year in the award article | 1 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Club Best Defender 2006: no date found in linked article; player not found in the award article's row for this year | 1 | 2006–2006 (1) |
| `awards_count` | undated award Serie A Goalscorer of the Year 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award Guerin d'Oro 2006: no date found in linked article; award row has no dated edition link | 1 | 2006–2006 (1) |
| `awards_count` | undated award European Golden Shoe 2005–06: no date found in linked article; player not found in the award article's row for this year | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2005–06: no date found in linked article; player not found in the award article's row for this year | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFPro World Player of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award UEFA Club Forward of the Year 2006–07: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award World Soccer Player of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A Foreign Footballer of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A Footballer of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award IAAF Latin Sportsman of the Year 2007: no date found in linked article; player not found in the award article's row for this year | 1 | 2007–2007 (1) |
| `awards_count` | undated award Onze d'Or 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award FIFPRO World 11 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Chelsea Players' Player of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Ivory Coast Player of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Onze de Bronze 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award UEFA Team of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A Player of the Month 2007: no date found in linked article; no row for this year in the award article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Guldbollen 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2007: no date found in linked article; no row for this year in the award article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Copa América Golden Boot 2007: no date found in linked article; no row for this year in the award article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A Italian Footballer of the Year 2007: no date found in linked article; player not found in the award article's row for this year | 1 | 2007–2007 (1) |
| `awards_count` | undated award European Golden Shoe 2006–07: no date found in linked article; player not found in the award article's row for this year | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A Goalscorer of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award African Footballer of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award ESM Team of the Season 2006–07: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award FA England Player of the Year Award 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Liverpool Player of the Season 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Liverpool Fans Online Player of the Season 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Copa Libertadores Finals Most Valuable Player 2007: no date found in linked article; no row for this year in the award article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Premio Nazionale Carriera Esemplare "Gaetano Scirea" 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award French Player of the Year 2007: no date found in linked article; no row for this year in the award article | 1 | 2007–2007 (1) |
| `awards_count` | undated award UEFA Club Defender of the Year 2007: no date found in linked article; player not found in the award article's row for this year | 1 | 2007–2007 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A "Fan" Award 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Golden Ball (Czech Republic) 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Best European Goalkeeper 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award UEFA Club Football Awards 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Time 100 Heroes & Pioneers no.16 2007: no date found in linked article; player not found in the award article's row for this year | 1 | 2007–2007 (1) |
| `awards_count` | undated award UEFA Best Midfielder Award 2006–07: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Ghana Player of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Chelsea Player of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Premier League top assist provider 2006–07: no date found in linked article; no row for this year in the award article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Qatar Stars League 2006–07: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award Asian Footballer of the Year 2007: no date found in linked article; player not found in the award article's row for this year | 1 | 2007–2007 (1) |
| `awards_count` | undated award Premio internazionale Giacinto Facchetti 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award South American Team of the Year 2007: no date found in linked article; no row for this year in the award article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Bulgarian Footballer of the Year 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award PFA 1997–2007: no date found in linked article; player not found in the award article's row for this year | 1 | 2007–2007 (1) |
| `awards_count` | undated award Premier League Player of the Month 2007: no date found in linked article; award row has no dated edition link | 1 | 2007–2007 (1) |
| `awards_count` | undated award UEFA Champions League top assist provider 2006–07: no date found in linked article; no row for this year in the award article | 1 | 2007–2007 (1) |
| `awards_count` | undated award FWA Tribute Award 2007: no date found in linked article; player not found in the award article's row for this year | 1 | 2007–2007 (1) |
| `awards_count` | undated award European Golden Shoe 2007–08: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFPRO World 11 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award ESM Team of the Year 2007–08: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award Premier League Player of the Year by Northwest Football Awards 2008: no date found in linked article; no row for this year in the award article | 1 | 2008–2008 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFA FIFPro World11 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award Baltic and Commonwealth of Independent States Footballer of the Year 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award ADN Eastern European Footballer of the Season 2008: no date found in linked article; no row for this year in the award article | 1 | 2008–2008 (1) |
| `awards_count` | undated award L'Équipe 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award Serie A Player of the Month 2008: no date found in linked article; no row for this year in the award article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Serie A Goal of the Year 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award Golden Tapir 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award Guldbollen 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award Fotbollskanalens hederspris 2008: no date found in linked article; no row for this year in the award article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2008: no date found in linked article; no row for this year in the award article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Swedish Male Athlete of the Year 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFPro World XI 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award Time 100 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award Maracanã Hall of Fame 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award Samba Gold 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award Honorary Fellowship 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award Don Balón Award 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award African Player of the Year 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award BBC Goal of the Season 2007–08: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award England Senior Men's Player of the Year 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award Don Balón Award 2007–08: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award UEFA Midfielder of the Year 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award Onze de Bronze 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award French Player of the Year 2008: no date found in linked article; no row for this year in the award article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award CAF Team of the Year 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award African Cup of Nations top goalscorer 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2008: no date found in linked article; no row for this year in the award article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Footballer of the Year (Germany) 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award Goal of the Year (Germany) 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award PFA Young Player of the Year 2007–08: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award Serbian Footballer of the Year 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award Serbia's Overseas Player of the Year 2008: no date found in linked article; no row for this year in the award article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Bravo Award 2008: no date found in linked article; award row has no dated edition link | 1 | 2008–2008 (1) |
| `awards_count` | undated award Golden Lion for the best Lyon sportsman 2008: no date found in linked article; no row for this year in the award article | 1 | 2008–2008 (1) |
| `awards_count` | undated award ''Étoile d'Or'' 2007–08: no date found in linked article; no row for this year in the award article | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFPro World XI 2008: no date found in linked article; player not found in the award article's row for this year | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFPRO World 11 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2008–09: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award FIFA FIFPro World11 2009: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award La Liga Best Spanish Player 2009: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award La Liga Best Midfielder 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Onze de Bronze 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award UEFA Team of the Year 2009: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award Time 100 2009: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award MARCA Legend Award 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Guldbollen 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2009: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award England Senior Men's Player of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award African Footballer of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award BBC African Footballer of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Liverpool Player of the Season 2009: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Bosnian Sportsman of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Bosnian Footballer of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Bundesliga Players' Player of the Year 2008–09: no date found in linked article; no row for this year in the award article | 1 | 2009–2009 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2008–09: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award BBC Sports Personality of the Year 2009: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award BBC Wales Sports Personality of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Samba Gold 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award FIFA Confederations Cup Silver Ball 2009: no date found in linked article; no row for this year in the award article | 1 | 2009–2009 (1) |
| `awards_count` | undated award FIFA Confederations Cup Best XI 2009: no date found in linked article; no row for this year in the award article | 1 | 2009–2009 (1) |
| `awards_count` | undated award Manchester United Players' Player of the Year 2008–09: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award La Liga Best Goalkeeper 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award European Golden Shoe 2008–09: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award Ligue 1 Player of the Month 2009: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award French Player of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Baltic and Commonwealth of Independent States Footballer of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award Chelsea Player of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2008–09: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award UEFA Club Defender of the Year 2009: no date found in linked article; player not found in the award article's row for this year | 1 | 2009–2009 (1) |
| `awards_count` | undated award Ivory Coast Player of the Year 2009: no date found in linked article; award row has no dated edition link | 1 | 2009–2009 (1) |
| `awards_count` | undated award European Golden Shoe 2009–10: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFPRO World 11 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award Don Balón Team of the Decade 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award ESPN Deportes Player of the Year 2010: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2009–10: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award Goal 50 2010: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award UEFA Team of the Year 2010: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFA World Cup top goalscorer 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award Best European Goalkeeper 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award IFFHS Best Goalkeeper of the Decade 2001–2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award USSA Male Athlete of the Year 2010: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award Chelsea Player of the Year 2010: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award ''Time'' Top 100 2010: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award West African Footballer of the Year 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award African Player of the Year 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award ''kicker'' Attacking Midfielder of the Year 2010: no date found in linked article; no row for this year in the award article | 1 | 2010–2010 (1) |
| `awards_count` | undated award Bundesliga top assists provider 2009–10: no date found in linked article; no row for this year in the award article | 1 | 2010–2010 (1) |
| `awards_count` | undated award UEFA Europa League top assists provider 2009–10: no date found in linked article; no row for this year in the award article | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFA World Cup top assists provider 2010: no date found in linked article; no row for this year in the award article | 1 | 2010–2010 (1) |
| `awards_count` | undated award The kicker Man of the Year 2010: no date found in linked article; no row for this year in the award article | 1 | 2010–2010 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award World Soccer Young Player of the Year 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award Bravo Award 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award VDV 2010: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award VDV 2009–10: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award Silbernes Lorbeerblatt 2010: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFA World Cup top assist provider 2010: no date found in linked article; no row for this year in the award article | 1 | 2010–2010 (1) |
| `awards_count` | undated award Germany national team 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2010: no date found in linked article; player not found in the award article's row for this year | 1 | 2010–2010 (1) |
| `awards_count` | undated award Samba d'Or 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award BBC African Footballer of the Year 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award Ghana Player of the Year 2010: no date found in linked article; award row has no dated edition link | 1 | 2010–2010 (1) |
| `awards_count` | undated award Pirata d'Oro (Internazionale Player Of The Year) 2010: no date found in linked article; no row for this year in the award article | 1 | 2010–2010 (1) |
| `awards_count` | undated award Argentine Sportsperson of the Year 2011: no date found in linked article; award row has no dated edition link | 1 | 2011–2011 (1) |
| `awards_count` | undated award European Golden Shoe 2010–11: no date found in linked article; award row has no dated edition link | 1 | 2011–2011 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2011: no date found in linked article; player not found in the award article's row for this year | 1 | 2011–2011 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2011: no date found in linked article; award row has no dated edition link | 1 | 2011–2011 (1) |
| `awards_count` | undated award La Liga Midfielder of the Year 2011: no date found in linked article; player not found in the award article's row for this year | 1 | 2011–2011 (1) |
| `awards_count` | undated award Onze d'Argent 2011: no date found in linked article; player not found in the award article's row for this year | 1 | 2011–2011 (1) |
| `awards_count` | undated award Marca Legend Award 2011: no date found in linked article; award row has no dated edition link | 1 | 2011–2011 (1) |
| `awards_count` | undated award CAF Team of the Year 2011: no date found in linked article; award row has no dated edition link | 1 | 2011–2011 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2011: no date found in linked article; award row has no dated edition link | 1 | 2011–2011 (1) |
| `awards_count` | undated award Bola de Prata 2011: no date found in linked article; award row has no dated edition link | 1 | 2011–2011 (1) |
| `awards_count` | undated award Copa Libertadores top assist provider 2011: no date found in linked article; no row for this year in the award article | 1 | 2011–2011 (1) |
| `awards_count` | undated award Troféu Mesa Redonda 2011: no date found in linked article; award row has no dated edition link | 1 | 2011–2011 (1) |
| `awards_count` | undated award Germany national team 2011: no date found in linked article; award row has no dated edition link | 1 | 2011–2011 (1) |
| `awards_count` | undated award LFP Defender of the Year 2011: no date found in linked article; player not found in the award article's row for this year | 1 | 2011–2011 (1) |
| `awards_count` | undated award French Player of the Year 2011: no date found in linked article; award row has no dated edition link | 1 | 2011–2011 (1) |
| `awards_count` | undated award Premier League top assist provider 2010–11: no date found in linked article; no row for this year in the award article | 1 | 2011–2011 (1) |
| `awards_count` | undated award European Golden Shoe 2011–12: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2012: no date found in linked article; player not found in the award article's row for this year | 1 | 2012–2012 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award ESM Team of the Year 2011–12: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award ''[[The Guardian]]'' European Team of the Year 2011–12: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award ''[[Bleacher Report]]'' La Liga Player of the Season 2011–12: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award ''Bleacher Report'' La Liga Starting XI 2011–12: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award UEFA Super Cup Man of the Match 2012: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Globe Soccer 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Premio Bulgarelli Number 8 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Pallone Azzurro 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Guerin d'Oro 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Serie A Midfielder of the Year 2012: no date found in linked article; player not found in the award article's row for this year | 1 | 2012–2012 (1) |
| `awards_count` | undated award Serie A Footballer of the Year 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award GQ Sportsman of the Year 2012: no date found in linked article; player not found in the award article's row for this year | 1 | 2012–2012 (1) |
| `awards_count` | undated award Ivory Coast Player of the Year 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2011–12: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award PFA Fans' Player of the Year 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award FWA Footballer of the Year 2011–12: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Golden Foot 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Serie A Player of the Month 2012: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Golden Tapir 2012: no date found in linked article; player not found in the award article's row for this year | 1 | 2012–2012 (1) |
| `awards_count` | undated award Sportschau Goal of the Month Award 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Sportschau Goal of the Year Award 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Ligue 1 Player of the Month 2012: no date found in linked article; player not found in the award article's row for this year | 1 | 2012–2012 (1) |
| `awards_count` | undated award Ligue 1 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Guldbollen 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Malmö 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2012: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Swedish Goal of the Year 2012: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award African Footballer of the Year 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Troféu Mesa Redonda 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award Campeonato Paulista Best Player 2012: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award IFFHS World's Best International Goal Scorer 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award La Liga top assists provider 2011–12: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award UEFA European Championship 2012: no date found in linked article; player not found in the award article's row for this year | 1 | 2012–2012 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2012: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Castrol Performance Index 2012: no date found in linked article; no row for this year in the award article | 1 | 2012–2012 (1) |
| `awards_count` | undated award French Player of the Year 2012: no date found in linked article; award row has no dated edition link | 1 | 2012–2012 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award European Golden Shoe 2012–13: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award FIFPRO World 11 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award French Player of the Year 2013: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award UEFA Super Cup Man of the Match 2013: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Bundesliga top assist provider 2012–13: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Bundesliga Player of the Year 2012–13: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award The kicker Man of the Year 2013: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award Globe Soccer Best Footballer of the Year 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award GQ Men of the Year 2013: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award Ligue 1 2013: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award Paris Saint-Germain 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Guldbollen 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award International Swede of the Year Award 2013: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2013: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Swedish Male Athlete of the Year 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Swedish Goal of the Year 2013: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Campeonato Paulista Best Player 2013: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award FIFA Confederations Cup Bronze Shoe 2013: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award FIFA Confederations Cup Dream Team 2013: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Premier League Player of the Month 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award BBC Goal of the Season 2012–13: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award Goal of the Month in Germany 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Welsh Footballer of the Year 2013: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award Serie A Footballer of the Year 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Premio Nazionale Carriera Esemplare "Gaetano Scirea" 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award ESPN 2012–13: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award CAF Team of the Year 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award African Footballer of the Year 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Premio Bulgarelli Number 8 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award BBC African Footballer of the Year 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Globe Soccer Awards Player Career Award 2013: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award Germany national team 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award UEFA Best Player in Europe Award 2013: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2013: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award Samba Gold 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award UNFP 2012–13: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award UNFP Ligue 1 [[UNFP Player of the Month/Player of the Month]] 2013: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award UEFA Team of the Year 2013: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Best European Goalkeeper 2013: no date found in linked article; award row has no dated edition link | 1 | 2013–2013 (1) |
| `awards_count` | undated award Bundesliga Team of the Season 2012–13: no date found in linked article; no row for this year in the award article | 1 | 2013–2013 (1) |
| `awards_count` | undated award VDV Bundesliga Team of the Season 2012–13: no date found in linked article; player not found in the award article's row for this year | 1 | 2013–2013 (1) |
| `awards_count` | undated award European Golden Shoe 2013–14: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2014: no date found in linked article; player not found in the award article's row for this year | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFPRO World 11 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award ''kicker'' Goalkeeper of the Year 2013–14: no date found in linked article; no row for this year in the award article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award Best European Goalkeeper 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award AIPS 2014: no date found in linked article; player not found in the award article's row for this year | 1 | 2014–2014 (1) |
| `awards_count` | undated award AIPS Europe Athlete of the Year – ''Frank Taylor Trophy'' 2014: no date found in linked article; no row for this year in the award article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Bundesliga Team of the Season 2013–14: no date found in linked article; no row for this year in the award article | 1 | 2014–2014 (1) |
| `awards_count` | undated award VDV Bundesliga Team of the Season 2013–14: no date found in linked article; player not found in the award article's row for this year | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2014: no date found in linked article; player not found in the award article's row for this year | 1 | 2014–2014 (1) |
| `awards_count` | undated award IFFHS World's Best International Goal Scorer 2014: no date found in linked article; player not found in the award article's row for this year | 1 | 2014–2014 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' World Team 2014: no date found in linked article; no row for this year in the award article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Samba de Ouro 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award Globe Revelation Player 2014: no date found in linked article; player not found in the award article's row for this year | 1 | 2014–2014 (1) |
| `awards_count` | undated award Bloomberg Sports 2014: no date found in linked article; player not found in the award article's row for this year | 1 | 2014–2014 (1) |
| `awards_count` | undated award ESPN FC 2014: no date found in linked article; no row for this year in the award article | 1 | 2014–2014 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award UEFA Team of the Year 2014: no date found in linked article; player not found in the award article's row for this year | 1 | 2014–2014 (1) |
| `awards_count` | undated award Welsh Footballer of the Year 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award Ligue 1 2014: no date found in linked article; player not found in the award article's row for this year | 1 | 2014–2014 (1) |
| `awards_count` | undated award Étoile d'Or [[France Football]] 2014: no date found in linked article; no row for this year in the award article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Paris Saint-Germain 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award Guldbollen 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2014: no date found in linked article; no row for this year in the award article | 1 | 2014–2014 (1) |
| `awards_count` | undated award CAF Team of the Year 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award African Footballer of the Year 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award Goal of the Year (Germany) 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award French Player of the Year 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award La Liga Best Midfielder 2014: no date found in linked article; player not found in the award article's row for this year | 1 | 2014–2014 (1) |
| `awards_count` | undated award Golden Foot 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 4th team 2014: no date found in linked article; no row for this year in the award article | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFA FIFPro Men's World XI 4th team 2014: no date found in linked article; no row for this year in the award article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Best Belgian Player Abroad 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award Bravo Award 2014: no date found in linked article; award row has no dated edition link | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFPRO World 11 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award European Golden Shoe 2014–15: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2015: no date found in linked article; player not found in the award article's row for this year | 1 | 2015–2015 (1) |
| `awards_count` | undated award FPF Portuguese Player of the Year 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award Samba de Ouro 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Top 100 Players in the World second place 2015: no date found in linked article; no row for this year in the award article | 1 | 2015–2015 (1) |
| `awards_count` | undated award IFFHS World's Best International Goal Scorer 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award ESM Team of the Year 2014–15: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award ''kicker'' Goalkeeper of the Year 2014–15: no date found in linked article; no row for this year in the award article | 1 | 2015–2015 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award Best European Goalkeeper 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award Bundesliga Team of the Season 2014–15: no date found in linked article; no row for this year in the award article | 1 | 2015–2015 (1) |
| `awards_count` | undated award VDV Bundesliga Team of the Season 2014–15: no date found in linked article; player not found in the award article's row for this year | 1 | 2015–2015 (1) |
| `awards_count` | undated award Premier League Player of the Season 2014–15: no date found in linked article; player not found in the award article's row for this year | 1 | 2015–2015 (1) |
| `awards_count` | undated award Chelsea Players' Player of the Year 2014–15: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award ESM Team of the Season 2014–15: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2014–15: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award PFA Fans' Premier League Player of the Month 2015: no date found in linked article; player not found in the award article's row for this year | 1 | 2015–2015 (1) |
| `awards_count` | undated award BBC Goal of the Month 2015: no date found in linked article; player not found in the award article's row for this year | 1 | 2015–2015 (1) |
| `awards_count` | undated award FSF Player of the Year 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award SportAccord 'Play for Change' Award 2015: no date found in linked article; no row for this year in the award article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Ligue 1 Player of the Month 2015: no date found in linked article; player not found in the award article's row for this year | 1 | 2015–2015 (1) |
| `awards_count` | undated award Guldbollen 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2015: no date found in linked article; no row for this year in the award article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Swedish Male Athlete of the Year 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award CAF Team of the Year 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award BBC African Footballer of the Year 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award Africa Cup of Nations Team of the Tournament 2015: no date found in linked article; no row for this year in the award article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Eurosport 2014–15: no date found in linked article; player not found in the award article's row for this year | 1 | 2015–2015 (1) |
| `awards_count` | undated award Premier League Player of the Year by Northwest Football Awards 2015: no date found in linked article; no row for this year in the award article | 1 | 2015–2015 (1) |
| `awards_count` | undated award FIFA FIFPro Men's World XI 2015: no date found in linked article; player not found in the award article's row for this year | 1 | 2015–2015 (1) |
| `awards_count` | undated award Welsh Footballer of the Year 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award Footballer of the Year (Germany) 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award Best Belgian Player Abroad 2015: no date found in linked article; award row has no dated edition link | 1 | 2015–2015 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2015: no date found in linked article; player not found in the award article's row for this year | 1 | 2015–2015 (1) |
| `awards_count` | undated award Croatian Sportsman of the Year 2015: no date found in linked article; player not found in the award article's row for this year | 1 | 2015–2015 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2016: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award FPF Portuguese Player of the Year 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award FIFPRO World 11 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award French Player of the Year 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award IFFHS World's Best Top Division Goalscorer 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award European Golden Shoe 2015–16: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award ESM Team of the Year 2015–16: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award La Liga top assist provider 2015–16: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2nd team 2016: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award UEFA Champions League Player of the Week 2016: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award ''WhoScored'' 2015–16: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Welsh Footballer of the Year 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award CAF African Footballer of the Year 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award BBC African Footballer of the Year 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Algerian Footballer of the Year 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award PFA Team of the Year 2015–16 Premier League: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2015–16: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award El Heddaf Arab Footballer of the Year 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Lion d'Or African Footballer of the Year 2016: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Best European Goalkeeper 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2016: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Pallone Azzurro 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Premio Nazionale Carriera Esemplare "Gaetano Scirea" 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Golden Foot 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award VDV Team of the Season 2015–16: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award ''DW'' 2016: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award Most clean sheets in Liga Portugal 2015-2016: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Étoile d'Or [[France Football]] 2016: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Eurosport 2016: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award PFA Fans' Premier League Player of the Month 2016: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award Manchester United 2016: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award Guldbollen 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2016: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award Serie A top assist provider 2015–16: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Chilean Footballer of the Year 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Football Oscar 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Premier League Player of the Month 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Best Belgian Player Abroad 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award CIES Football Observatory 2015–16: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award UEFA La Liga Team of the Season 2015–16: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award European Sports Media 2015–16: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2016: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award VDV 2015–16: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' Bundesliga Team of the Season 2015–16: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award ''kicker'' Goalkeeper of the Year 2015–16: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2016: no date found in linked article; award row has no dated edition link | 1 | 2016–2016 (1) |
| `awards_count` | undated award Bundesliga Team of the Season 2015–16: no date found in linked article; no row for this year in the award article | 1 | 2016–2016 (1) |
| `awards_count` | undated award VDV Bundesliga Team of the Season 2015–16: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award Luis Aragones 2016: no date found in linked article; player not found in the award article's row for this year | 1 | 2016–2016 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award FPF Portuguese Player of the Year 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award European Golden Shoe 2016–17: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award FIFPRO World 11 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2017: no date found in linked article; player not found in the award article's row for this year | 1 | 2017–2017 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' World Team 2017: no date found in linked article; no row for this year in the award article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Samba de Ouro 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award ''WhoScored'' 2016–17: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2017: no date found in linked article; player not found in the award article's row for this year | 1 | 2017–2017 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Best European Goalkeeper 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Gazzetta Sports Awards 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Juventus Greatest XI of All Time 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Football Oscar 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award La Liga Best Defender 2016–17: no date found in linked article; player not found in the award article's row for this year | 1 | 2017–2017 (1) |
| `awards_count` | undated award Golden Boy 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award UNFP 2016–17: no date found in linked article; no row for this year in the award article | 1 | 2017–2017 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2017: no date found in linked article; player not found in the award article's row for this year | 1 | 2017–2017 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Year 2017: no date found in linked article; no row for this year in the award article | 1 | 2017–2017 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award French Player of the Year 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Premier League Player of the Month 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award England Player of the Year Award 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award IFFHS World's Best Top Goal Scorer 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award UNFP [[Trophées UNFP du football#Player of the Year/Ligue 1 Player of the Year]] 2016–17: no date found in linked article; no row for this year in the award article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Coupe de la Ligue top goalscorer 2016–17: no date found in linked article; no row for this year in the award article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Ligue 1 Best Foreign Player 2017: no date found in linked article; no row for this year in the award article | 1 | 2017–2017 (1) |
| `awards_count` | undated award UEFA Champions League Forward of the Season 2016–17: no date found in linked article; player not found in the award article's row for this year | 1 | 2017–2017 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Season 2017: no date found in linked article; no row for this year in the award article | 1 | 2017–2017 (1) |
| `awards_count` | undated award ESPN 2017: no date found in linked article; player not found in the award article's row for this year | 1 | 2017–2017 (1) |
| `awards_count` | undated award Onze de Bronze 2016–17: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award La Liga Player of the Month 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Chelsea Goal of the Year 2016–17: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award Belgium Player of the Year 2017: no date found in linked article; no row for this year in the award article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Best Belgian Abroad 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award ''[[Der Spiegel]]'' Best Player in the Bundesliga (winter period) 2016–17: no date found in linked article; no row for this year in the award article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Liverpool Players' Player of the Season Award 2016–17: no date found in linked article; player not found in the award article's row for this year | 1 | 2017–2017 (1) |
| `awards_count` | undated award UNFP 2017: no date found in linked article; no row for this year in the award article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Slovenian Footballer of the Year 2017: no date found in linked article; award row has no dated edition link | 1 | 2017–2017 (1) |
| `awards_count` | undated award UEFA Men's Player of the Year Award 2017–18: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award Football Oscar 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award Franjo Bučar State Award for Sport 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award HNS 2018: no date found in linked article; player not found in the award article's row for this year | 1 | 2018–2018 (1) |
| `awards_count` | undated award HOO 2018: no date found in linked article; no row for this year in the award article | 1 | 2018–2018 (1) |
| `awards_count` | undated award SN Sportsman of the Year 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2018: no date found in linked article; player not found in the award article's row for this year | 1 | 2018–2018 (1) |
| `awards_count` | undated award FPF Portuguese Player of the Year 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award French Player of the Year 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award UNFP 2017–18: no date found in linked article; no row for this year in the award article | 1 | 2018–2018 (1) |
| `awards_count` | undated award European Golden Shoe 2017–18: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award El Heddaf Arab Footballer of the Year 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award BBC African Footballer of the Year 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award African Footballer of the Year 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award UEFA Champions League Forward of the Season 2017–18: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award Onze d'Argent 2017–18: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award FSA Player of the Year 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award BBC Goal of the Month 2018: no date found in linked article; player not found in the award article's row for this year | 1 | 2018–2018 (1) |
| `awards_count` | undated award Belgium Player of the Year 2018: no date found in linked article; no row for this year in the award article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Best Belgian Abroad 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award England Player of the Year Award 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award London Football Awards Premier League Player of the Year 2018: no date found in linked article; no row for this year in the award article | 1 | 2018–2018 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Year 2018: no date found in linked article; no row for this year in the award article | 1 | 2018–2018 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2018: no date found in linked article; player not found in the award article's row for this year | 1 | 2018–2018 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2nd team 2018: no date found in linked article; no row for this year in the award article | 1 | 2018–2018 (1) |
| `awards_count` | undated award ''WhoScored'' 2017–18: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award Ligue 1 top assist provider 2017–18: no date found in linked article; no row for this year in the award article | 1 | 2018–2018 (1) |
| `awards_count` | undated award UNFP [[Ligue 1 Player of the Year]] 2017–18: no date found in linked article; no row for this year in the award article | 1 | 2018–2018 (1) |
| `awards_count` | undated award La Liga Player of the Month 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award UEFA Champions League Goal of the Season 2017–18: no date found in linked article; no row for this year in the award article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Samba Gold 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award FIFA FIFPro World11 2018: no date found in linked article; player not found in the award article's row for this year | 1 | 2018–2018 (1) |
| `awards_count` | undated award Trofeo EFE 2017–18: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award Golden Foot 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award PFA 2018: no date found in linked article; player not found in the award article's row for this year | 1 | 2018–2018 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Season 2018: no date found in linked article; no row for this year in the award article | 1 | 2018–2018 (1) |
| `awards_count` | undated award ESPN 2018: no date found in linked article; player not found in the award article's row for this year | 1 | 2018–2018 (1) |
| `awards_count` | undated award Globe Soccer Awards Best Goalkeeper of the Year 2018: no date found in linked article; player not found in the award article's row for this year | 1 | 2018–2018 (1) |
| `awards_count` | undated award UEFA 2017–18: no date found in linked article; player not found in the award article's row for this year | 1 | 2018–2018 (1) |
| `awards_count` | undated award Slovenian Footballer of the Year 2018: no date found in linked article; award row has no dated edition link | 1 | 2018–2018 (1) |
| `awards_count` | undated award European Golden Shoe 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award FIFPRO World 11 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Premier League Player of the Year by Northwest Football Awards 2019: no date found in linked article; no row for this year in the award article | 1 | 2019–2019 (1) |
| `awards_count` | undated award UEFA Men's Player of the Year Award 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Liverpool Players' Player of the Season Award 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2019: no date found in linked article; no row for this year in the award article | 1 | 2019–2019 (1) |
| `awards_count` | undated award PFA 2019: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award African Footballer of the Year 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Onze d'Or 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award ''Time'' 100 2019: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award Ligue 1 Player of the Year 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award French Player of the Year 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Onze de Bronze 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Globe Soccer Awards Best Goalkeeper of the Year 2019: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award Samba Gold 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Polish Football Association 1919–2019: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award Alan Hardaker Trophy 2019: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award African Goal of the Year 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Eredivisie Player of the Month 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Johan Cruyff Trophy 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Chelsea Players' Player of the Year 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award ESM Team of the Season 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Chelsea Goal of the Year 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Belgium Player of the Year 2019: no date found in linked article; no row for this year in the award article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Best Belgian Abroad 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Premier League Playmaker of the Season 2018–19: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award Dutch Footballer of the Year 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award ''Goal'' 2019: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award Serbian Footballer of the Year 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award AFC Asian International Player of the Year 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Korean FA Player of the Year 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Gallup Korea's Athlete of the Year 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award London Football Award for Premier League Player of the Year 2019: no date found in linked article; no row for this year in the award article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Premi Barça Jugadors 2018–19: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award SJPF Young Player of the Month 2019: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award CNID Best Revelation Footballer of the Year 2019: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award Golden Globes 2019: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award ''[[A Bola]]'' Player of the Year 2019: no date found in linked article; no row for this year in the award article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Golden Boy 2019: no date found in linked article; award row has no dated edition link | 1 | 2019–2019 (1) |
| `awards_count` | undated award Globe Revelation Player 2019: no date found in linked article; player not found in the award article's row for this year | 1 | 2019–2019 (1) |
| `awards_count` | undated award Argentine Sportsperson of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award European Golden Shoe 2020–21: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best Man Player 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best Top Goal Scorer 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best International Goal Scorer 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best Top Division Goal Scorer 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award ''World Soccer'' Player of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award ''FourFourTwo'' Player of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award ''Tuttosport'' Golden Player 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award ''The Guardian'' Best Footballer in the World 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Globe Soccer Fans' Player of the Year 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award Globe Soccer Maradona Award 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Polish Sports Personality of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Bundesliga 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award German Sports Journalists' Footballer of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World Team 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Onze d'Or 2020–21: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award French Player of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award AS 2021: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award L'Équipe 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award FSA Player of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS CAF Men's Team of The Year 2021: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Laureus Sporting Inspiration Award 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award Golden Foot 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS Best CAF Men's Player of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Globe Soccer Best Player of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Globe Soccer Awards Best Goalkeeper of the Year 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Bundesliga Player of the Month 2021: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Bundesliga Goal of the Month 2021: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Gullballen 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Best Belgian Abroad 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Globe Soccer Awards Best Defender of the Year 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award Samba de Ouro 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2nd team 2021: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award UEFA Champions League Player of the Week 2021: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award CIES Football Observatory 2020–21: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS Best Playmaker of the Copa América 2021: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Danish Player of the Year 2021: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award The Guardian Footballer of the Year 2021: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award PFA 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award Alan Hardaker Trophy 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS CAF World's Best Playmaker 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award Premier League Goal of the Month 2021: no date found in linked article; player not found in the award article's row for this year | 1 | 2021–2021 (1) |
| `awards_count` | undated award Manchester United Goal of the Season 2020–21: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award London Football Awards Premier League Player of the Year 2021: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Golden Boy 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Trofeo Aldo Rovira 2020–21: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award UEFA Europa League top assists provider 2020–21: no date found in linked article; no row for this year in the award article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Gazzetta Sports Awards 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award Football Oscar 2021: no date found in linked article; award row has no dated edition link | 1 | 2021–2021 (1) |
| `awards_count` | undated award UEFA Men's Player of the Year 2021–22: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Golden Player Man Award 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Onze d'Or 2021–22: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Globe Soccer Best Player of the Year 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2022: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award La Liga Player of the Month 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Kicker 2022: no date found in linked article; no row for this year in the award article | 1 | 2022–2022 (1) |
| `awards_count` | undated award L'Équipe 2022: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award African Footballer of the Year 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS Best CAF Men's Player of the Year 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Best Belgian Player Abroad 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Premier League Player of the Year by Northwest Football Awards 2022: no date found in linked article; no row for this year in the award article | 1 | 2022–2022 (1) |
| `awards_count` | undated award FSA Player of the Year 2022: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award European Golden Shoe 2021–22: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Laureus 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Golden Foot 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award ESM Team of the Year 2021–22: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award ESPN 2021–22: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award PFA Player of the Month 2022: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS CAF Men's Team of The Year 2022: no date found in linked article; no row for this year in the award article | 1 | 2022–2022 (1) |
| `awards_count` | undated award BBC Goal of the Season 2021–22: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award Globe Soccer Fans' Player of the Year 2022: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award Ligue 1 Player of the Year 2021–22: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS World's Best Top Goal Scorer 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Ligue 1 top assist provider 2021–22: no date found in linked article; no row for this year in the award article | 1 | 2022–2022 (1) |
| `awards_count` | undated award ''WhoScored'' 2021–22: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award UNFP 2021–22: no date found in linked article; no row for this year in the award article | 1 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Football Oscar 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award SN Sportsman of the Year 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Gullballen 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award ''FourFourTwo'' Player of the Year 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS Asian Men's Player of the Year 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Eurosport 2021–22: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award Korean FA Player of the Year 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Gallup Korea's Athlete of the Year 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Cheongnyong Medal 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Alan Hardaker Trophy 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award Futbolista Colombiano del Año 2022: no date found in linked article; no row for this year in the award article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Manchester City Goal of the Season 2022: no date found in linked article; no row for this year in the award article | 1 | 2022–2022 (1) |
| `awards_count` | undated award UEFA Champions League Fantasy Football Team of the Season 2021–22: no date found in linked article; no row for this year in the award article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2022: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award VDV Bundesliga Team of the Season 2021–22: no date found in linked article; award row has no dated edition link | 1 | 2022–2022 (1) |
| `awards_count` | undated award SJPF Player of the Month 2022: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award CNID Footballer of the Year 2022: no date found in linked article; player not found in the award article's row for this year | 1 | 2022–2022 (1) |
| `awards_count` | undated award Laureus World Sportsman of the Year 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award ''TIME'' Athlete of the Year 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award FIFPRO World 11 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award European Golden Shoe 2022–23: no date found in linked article; player not found in the award article's row for this year | 1 | 2023–2023 (1) |
| `awards_count` | undated award UEFA Men's Player of the Year 2022–23: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Premier League Player of the Month 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Golden Player Man Award 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Gullballen 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2022–23: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award ''The Guardian'' Best Footballer in the World 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award ''World Soccer'' Player of the Year 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award ''FourFourTwo'' Player of the Year 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS World's Best Player 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Onze d'Or 2022–23: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Idrettsgallaen 2023: no date found in linked article; player not found in the award article's row for this year | 1 | 2023–2023 (1) |
| `awards_count` | undated award French Player of the Year 2022–23: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award UNFP 2022–23: no date found in linked article; player not found in the award article's row for this year | 1 | 2023–2023 (1) |
| `awards_count` | undated award Best Belgian Player Abroad 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Samba Gold 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Ghana Football Awards 2023: no date found in linked article; no row for this year in the award article | 1 | 2023–2023 (1) |
| `awards_count` | undated award African Footballer of the Year 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Football Oscar 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award FSA Player of the Year 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS CAF Men's Team of The Year 2023: no date found in linked article; no row for this year in the award article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Znicz Pruszków 2023: no date found in linked article; player not found in the award article's row for this year | 1 | 2023–2023 (1) |
| `awards_count` | undated award "Lion d'Or" African Footballer of the Year 2023: no date found in linked article; no row for this year in the award article | 1 | 2023–2023 (1) |
| `awards_count` | undated award "Africa d'Or" African Footballer of the Year 2023: no date found in linked article; no row for this year in the award article | 1 | 2023–2023 (1) |
| `awards_count` | undated award African Goalkeeper of the Year 2023: no date found in linked article; player not found in the award article's row for this year | 1 | 2023–2023 (1) |
| `awards_count` | undated award UMFP Best Moroccan goalkeeper abroad 2022–23: no date found in linked article; no row for this year in the award article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Marca Leyenda Award 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2023: no date found in linked article; player not found in the award article's row for this year | 1 | 2023–2023 (1) |
| `awards_count` | undated award Georgian Footballer of the Year 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Serie A Goal of the Month 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Golden Boy 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS World's Best Top Division Goal Scorer 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Gazzetta Sports Awards 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award Korean FA Player of the Year 2023: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award England Men's Player of the Year 2022–23: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award PFA Young Player of the Year 2022–23: no date found in linked article; award row has no dated edition link | 1 | 2023–2023 (1) |
| `awards_count` | undated award London Football Awards Men's Young Player of the Year 2023: no date found in linked article; no row for this year in the award article | 1 | 2023–2023 (1) |
| `awards_count` | undated award London Football Awards Premier League Player of the Year 2023: no date found in linked article; no row for this year in the award article | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS World's Best Player 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''World Soccer'' Player of the Year 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''FourFourTwo'' Player of the Year 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''The Guardian'' Best Footballer in the World 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award CIES Football Observatory 2023–24: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''[[The Athletic]]'' Premier League Player of the Season 2023–24: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' European Men's Team of the Season 2023–24: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Samba Gold 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award Globe Soccer Best Player of the Year 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award Globe Soccer Best Forward 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award Laureus World Breakthrough of the Year 2024: no date found in linked article; player not found in the award article's row for this year | 1 | 2024–2024 (1) |
| `awards_count` | undated award Ligue 1 Player of the Year 2023–24: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award Ligue 1 top goalscorer 2023–24: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award French Player of the Year 2023–24: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award Globe Soccer Best Player of the Year 2024: no date found in linked article; player not found in the award article's row for this year | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''[[The Athletic]]'' European Men's Team of the Season 2023–24: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' Ligue 1 Player of the Season 2023–24: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Golden Foot 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award Golden Boy 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award German Footballer of the Year 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award Golden Player Man Award 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award European Golden Shoe 2023–24: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award Bundesliga Player of the Month 2024: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award VDV Team of the Season 2023–24: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award African Footballer of the Year 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''[[The Athletic]]'' Premier League Team of the Season 2023–24: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award Footballer of the Year of Argentina 2024: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''[[Opta Sports#Association football/WhoScored]]'' Top Rated Player in Europe (performance data by [[Opta Sports/Opta]]) 2024: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award England's Men's Player of the Year 2023–24: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award London Football Awards Men's Young Player of the Year 2024: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Chelsea Player's Player of the Season 2023–24: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award PFA Young Player of the Year 2023–24: no date found in linked article; award row has no dated edition link | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' Premier League Insiders Signing of the Season 2023–24: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' Premier League Young Player of the Season 2023–24: no date found in linked article; no row for this year in the award article | 1 | 2024–2024 (1) |
| `awards_count` | undated award London Football 2024: no date found in linked article; player not found in the award article's row for this year | 1 | 2024–2024 (1) |
| `awards_count` | undated award IFFHS World's Best Player 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Globe Soccer Awards Forward of the Year 2025: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''[[Opta Sports#Association football/WhoScored]]'' European Player of the Season (performance data by [[Opta Sports/Opta]]) 2024–25: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award CIES Football Observatory 2024–25: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award Laureus World Sports Award for Breakthrough of the Year 2025: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award Maradona Award 2025: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Globe Soccer Awards Midfielder of the Year 2025: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award Premier League Player of the Month 2025: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award PFA Player of the Month 2025: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award CIES Football Observatory 2024–25: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World Men's Player of the Month 2025: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award FPL Pod Player of the Year 2025: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''[[The Athletic]]''<nowiki/>'s Premier League Player of the Year 2024–25: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award EA Sports 2024–25: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''The Athletic'' European Men's Player of the Season 2024–25: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''The Athletic'' La Liga  Team of the Season 2024–25: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award African Footballer of the Year 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Lion d'Or African Footballer of the Year 2025: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Ghana Football Awards 2025: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award UMFP Best Moroccan player abroad 2024–25: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best Top Goal Scorer 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best Top Division Goal Scorer 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award La Liga Player of the Month 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award London Football Awards Premier League Player of the Year 2025: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award London Football Awards Goal of the season 2025: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award EA Sports FC 2024–25: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award FIFPRO Men's World 11 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award The Athletic 2024–25: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award Premi Barça Jugadors 2024–25: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''The Athletic'' La Liga Player of the Season 2024–25: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''The Athletic'' La Liga Team of the Season 2024–25: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Georgian Footballer of the Year 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Golden Boy 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Globe Soccer Awards Emerging Player of the Year 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2025: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ESM Team of the Year 2024–25: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Serie A Most Valuable Player 2024–25: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''[[The Athletic]]'' Serie A Team of the Season 2024–25: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award BBC Goal of the Month 2025: no date found in linked article; player not found in the award article's row for this year | 1 | 2025–2025 (1) |
| `awards_count` | undated award England Men's Player of the Year 2024–25: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Norwegian Sportsperson of the Year 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best International Goal Scorer 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award German Footballer of the Year 2025: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Bundesliga Goal of the Month 2025: no date found in linked article; no row for this year in the award article | 1 | 2025–2025 (1) |
| `awards_count` | undated award VDV Team of the Season 2024–25: no date found in linked article; award row has no dated edition link | 1 | 2025–2025 (1) |
| `awards_count` | undated award Bundesliga Player of the Month 2026: no date found in linked article; no row for this year in the award article | 1 | 2026–2026 (1) |
| `awards_count` | undated award Laureus World Sports Award for Young Sportsperson of the Year 2026: no date found in linked article; award row has no dated edition link | 1 | 2026–2026 (1) |
| `awards_count` | undated award IFFHS 2026: no date found in linked article; player not found in the award article's row for this year | 1 | 2026–2026 (1) |
| `awards_count` | undated award Golden Boy 2026: no date found in linked article; award row has no dated edition link | 1 | 2026–2026 (1) |
| `awards_count` | undated award ''The Athletic'' European Men's Team of the Season 2025–26: no date found in linked article; no row for this year in the award article | 1 | 2026–2026 (1) |
| `awards_count` | undated award The Athletic 2025-2026: no date found in linked article; player not found in the award article's row for this year | 1 | 2026–2026 (1) |
| `awards_count` | undated award Serie A Player of the Month 2026: no date found in linked article; award row has no dated edition link | 1 | 2026–2026 (1) |
| `awards_count` | undated award UEFA 2026: no date found in linked article; player not found in the award article's row for this year | 1 | 2026–2026 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2025–26: no date found in linked article; award row has no dated edition link | 1 | 2026–2026 (1) |
| `club minutes/assists/cards` | Wikipedia club tables list apps and goals only; Transfermarkt and FBref blocked | 721 | 2000–2026 (26) |
| `club_other_apps` | season total not verifiably inside the window | 603 | 2000–2026 (26) |
| `club_other_goals` | match-by-match goals did not pass the season-total check | 330 | 2000–2026 (26) |
| `decisive_ga` | needs league, ucl, club_other and national all filled | 721 | 2000–2026 (26) |
| `gk_clean_sheets` | needs league, ucl, club_other and national all filled | 721 | 2000–2026 (26) |
| `gk_goals_conceded` | needs league, ucl, club_other and national all filled | 721 | 2000–2026 (26) |
| `goals` | needs league, ucl, club_other and national all filled | 445 | 2000–2026 (26) |
| `intl_stage` | UEFA Euro 2000: no round data | 15 | 2000–2000 (1) |
| `intl_stage` | Copa América 2016: no round data | 7 | 2016–2016 (1) |
| `intl_stage` | Copa América 2015: no round data | 5 | 2015–2015 (1) |
| `intl_stage` | Copa América 2007: no round data | 4 | 2007–2007 (1) |
| `intl_stage` | African Cup of Nations 2010: no round data | 3 | 2010–2010 (1) |
| `intl_stage` | African Cup of Nations 2019: no round data | 3 | 2019–2019 (1) |
| `intl_stage` | African Cup of Nations 2002: no round data | 2 | 2002–2002 (1) |
| `intl_stage` | African Cup of Nations 2006: no round data | 2 | 2006–2006 (1) |
| `intl_stage` | African Cup of Nations 2008: no round data | 2 | 2008–2008 (1) |
| `intl_stage` | African Cup of Nations 2012: no round data | 2 | 2012–2012 (1) |
| `intl_stage` | African Cup of Nations 2017: no round data | 2 | 2017–2017 (1) |
| `intl_stage` | Copa América 2019: no round data | 2 | 2019–2019 (1) |
| `intl_stage` | African Cup of Nations 2004: no round data | 1 | 2004–2004 (1) |
| `intl_stage` | African Cup of Nations 2013: no round data | 1 | 2013–2013 (1) |
| `intl_stage` | African Cup of Nations 2026: no round data | 1 | 2026–2026 (1) |
| `intl_tournament_*` | StatsBomb has no FIFA World Cup 2026 | 29 | 2026–2026 (1) |
| `intl_tournament_*` | StatsBomb has no FIFA World Cup 2006 | 25 | 2006–2006 (1) |
| `intl_tournament_*` | StatsBomb has no FIFA World Cup 2002 | 24 | 2002–2002 (1) |
| `intl_tournament_*` | StatsBomb has no UEFA Euro 2004 | 23 | 2004–2004 (1) |
| `intl_tournament_*` | StatsBomb has no FIFA World Cup 2010 | 23 | 2010–2010 (1) |
| `intl_tournament_*` | StatsBomb has no UEFA Euro 2000 | 21 | 2000–2000 (1) |
| `intl_tournament_*` | StatsBomb has no FIFA World Cup 2014 | 21 | 2014–2014 (1) |
| `intl_tournament_*` | StatsBomb has no UEFA Euro 2008 | 20 | 2008–2008 (1) |
| `intl_tournament_*` | StatsBomb has no UEFA Euro 2016 | 20 | 2016–2016 (1) |
| `intl_tournament_*` | StatsBomb has no UEFA Euro 2012 | 17 | 2012–2012 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2007 | 9 | 2007–2007 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2015 | 8 | 2015–2015 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2016 | 8 | 2016–2016 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2011 | 6 | 2011–2011 (1) |
| `intl_tournament_*` | player name not found in StatsBomb tournament lineups | 6 | 2018–2024 (3) |
| `intl_tournament_*` | StatsBomb has no Copa América 2019 | 5 | 2019–2019 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2019 | 4 | 2019–2019 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2021 | 4 | 2021–2021 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2022 | 4 | 2022–2022 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2001 | 3 | 2001–2001 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2004 | 3 | 2004–2004 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2008 | 2 | 2008–2008 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2012 | 2 | 2012–2012 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2017 | 2 | 2017–2017 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2004 | 1 | 2004–2004 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2006 | 1 | 2006–2006 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2013 | 1 | 2013–2013 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2015 | 1 | 2015–2015 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | calendar-year window: club tables are per season | 571 | 2000–2021 (21) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2022, 8, 5), datetime.date(2023, 5, 28))] / club-season match dates [(datetime.date(2022, 7, 30), datetime.date(2023, 6, 10))] vs window 2022-08-01–2023-07-31 | 7 | 2023–2023 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [None] / club-season match dates [(datetime.date(2021, 8, 14), datetime.date(2022, 5, 28))] vs window 2021-08-01–2022-07-31 | 5 | 2022–2022 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [None] / club-season match dates [(datetime.date(2021, 8, 7), datetime.date(2022, 5, 22))] vs window 2021-08-01–2022-07-31 | 5 | 2022–2022 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2023, 8, 11), datetime.date(2024, 5, 19))] / club-season match dates [None] vs window 2023-08-01–2024-07-31 | 4 | 2024–2024 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [None] / club-season match dates [(datetime.date(2021, 8, 15), datetime.date(2022, 5, 22))] vs window 2021-08-01–2022-07-31 | 2 | 2022–2022 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2022, 8, 5), datetime.date(2023, 6, 3))] / club-season match dates [(datetime.date(2022, 7, 31), datetime.date(2023, 6, 3))] vs window 2022-08-01–2023-07-31 | 2 | 2023–2023 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2022, 8, 5), datetime.date(2023, 5, 28))] / club-season match dates [(datetime.date(2022, 7, 20), datetime.date(2023, 5, 28))] vs window 2022-08-01–2023-07-31 | 2 | 2023–2023 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2023, 8, 11), datetime.date(2024, 5, 26))] / club-season match dates [(datetime.date(2023, 8, 12), datetime.date(2024, 6, 1))] vs window 2023-08-01–2024-07-31 | 2 | 2024–2024 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2021, 8, 13), datetime.date(2022, 5, 22))] / club-season match dates [(datetime.date(2021, 8, 14), datetime.date(2022, 5, 28))] vs window 2021-08-01–2022-07-31 | 1 | 2022–2022 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2021, 8, 6), datetime.date(2022, 5, 15)), None] / club-season match dates [(datetime.date(2021, 8, 8), datetime.date(2022, 5, 22)), (datetime.date(2021, 8, 14), datetime.date(2022, 5, 28))] vs window 2021-08-01–2022-07-31 | 1 | 2022–2022 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2021, 8, 21), datetime.date(2022, 5, 22)), None] / club-season match dates [(datetime.date(2021, 8, 22), datetime.date(2022, 5, 21)), None] vs window 2021-08-01–2022-07-31 | 1 | 2022–2022 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [None] / club-season match dates [(datetime.date(2021, 8, 1), datetime.date(2022, 5, 22))] vs window 2021-08-01–2022-07-31 | 1 | 2022–2022 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2022, 8, 5), datetime.date(2023, 5, 28))] / club-season match dates [(datetime.date(2022, 7, 30), datetime.date(2023, 5, 28))] vs window 2022-08-01–2023-07-31 | 1 | 2023–2023 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2022, 8, 5), datetime.date(2023, 5, 27))] / club-season match dates [(datetime.date(2022, 7, 29), datetime.date(2023, 5, 27))] vs window 2022-08-01–2023-07-31 | 1 | 2023–2023 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2022, 8, 5), datetime.date(2023, 5, 27))] / club-season match dates [(datetime.date(2022, 7, 30), datetime.date(2023, 6, 3))] vs window 2022-08-01–2023-07-31 | 1 | 2023–2023 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2022, 8, 5), datetime.date(2023, 5, 27))] / club-season match dates [(datetime.date(2022, 7, 30), datetime.date(2023, 5, 27))] vs window 2022-08-01–2023-07-31 | 1 | 2023–2023 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2022, 8, 13), datetime.date(2023, 6, 4))] / club-season match dates [(datetime.date(2022, 8, 13), datetime.date(2023, 6, 10))] vs window 2022-08-01–2023-07-31 | 1 | 2023–2023 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2022, 8, 5), datetime.date(2023, 5, 27))] / club-season match dates [(datetime.date(2022, 5, 20), datetime.date(2023, 6, 3))] vs window 2022-08-01–2023-07-31 | 1 | 2023–2023 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2024, 8, 15), datetime.date(2025, 5, 25))] / club-season match dates [(datetime.date(2024, 8, 17), datetime.date(2025, 5, 25))] vs window 2024-08-01–2025-07-31 | 1 | 2025–2025 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2024, 8, 16), datetime.date(2025, 5, 25)), (datetime.date(2024, 8, 17), datetime.date(2025, 5, 25))] / club-season match dates [None, (datetime.date(2024, 8, 10), datetime.date(2025, 5, 23))] vs window 2024-08-01–2025-07-31 | 1 | 2025–2025 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2024, 8, 17), datetime.date(2025, 5, 25))] / club-season match dates [(datetime.date(2024, 8, 17), datetime.date(2025, 6, 30))] vs window 2024-08-01–2025-07-31 | 1 | 2025–2025 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | no 2025–26 row in the club statistics table | 1 | 2026–2026 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2025, 8, 15), datetime.date(2026, 5, 24))] / club-season match dates [(datetime.date(2025, 8, 16), datetime.date(2026, 5, 23))] vs window 2025-08-01–2026-07-31 | 1 | 2026–2026 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2025, 8, 15), datetime.date(2026, 5, 24))] / club-season match dates [None] vs window 2025-08-01–2026-07-31 | 1 | 2026–2026 (1) |
| `league/ucl/club_other apps+goals (Wikipedia)` | league season dates [(datetime.date(2025, 8, 28), datetime.date(2026, 5, 21))] / club-season match dates [None] vs window 2025-08-01–2026-07-31 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2009-01-01 | 5 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2004-01-01 | 4 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2007-01-01 | 4 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 league: article lists 23 goals, career table 24 | 2 | 2000–2001 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 ucl: article lists 6 goals, career table 0; 2000–01 club_other: article lists 7 goals, career table 13 | 2 | 2000–2001 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 league: article lists 4 goals, career table 3 | 2 | 2000–2001 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2001-01-01 | 2 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2003-01-01 | 2 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 ucl: article lists 0 goals, career table unknown; 2003–04 club_other: article lists 0 goals, career table unknown | 2 | 2003–2004 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07: scoring match not assignable (18 November 2006, competition None, goals 0) | 2 | 2006–2007 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2006-01-01 | 2 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 club_other: article lists 3 goals, career table 2 | 2 | 2007–2008 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 ucl: article lists 0 goals, career table unknown; 2006–07 club_other: article lists 0 goals, career table unknown; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown | 2 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 league: article lists 0 goals, career table 14; 2008–09 ucl: article lists 2 goals, career table 0 | 2 | 2008–2009 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 league: article lists 0 goals, career table 16; 2008–09 ucl: article lists 6 goals, career table 7 | 2 | 2008–2009 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2008-01-01 | 2 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 league: article lists 18 goals, career table 17 | 2 | 2008–2009 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 club_other: article lists 1 goals, career table 0 | 2 | 2010–2011 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13 league: article lists 6 goals, career table 5 | 2 | 2012–2013 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14 league: article lists 0 goals, career table 1 | 2 | 2013–2014 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 club_other: article lists 4 goals, career table 3 | 2 | 2014–2015 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2015–16 club_other: article lists 10 goals, career table 7 | 2 | 2015–2016 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 league: article lists 7 goals, career table 6 | 2 | 2016–2017 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 ucl: article lists 2 goals, career table 0; 2017–18 club_other: article lists 8 goals, career table 10 | 2 | 2017–2018 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 league: article lists 24 goals, career table 23; 2022–23 ucl: article lists 5 goals, career table 0; 2022–23 club_other: article lists 5 goals, career table 10 | 2 | 2022–2023 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 league: article lists 30 goals, career table 29; 2022–23 club_other: article lists 6 goals, career table 5 | 2 | 2022–2023 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 club_other: article lists 2 goals, career table 0 | 2 | 2022–2023 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 club_other: article lists 3 goals, career table 1 | 2 | 2022–2023 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2023–24 league: article lists 9 goals, career table 8 | 2 | 2023–2024 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 2 goals, career table 3; 2024–25 club_other: article lists 4 goals, career table 3 | 2 | 2024–2025 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 3 goals, career table 7; 2024–25 club_other: article lists 10 goals, career table 6 | 2 | 2024–2025 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 ucl: article lists 0 goals, career table 1; 2025–26 club_other: article lists 1 goals, career table 0 | 2 | 2025–2026 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 ucl: article lists 3 goals, career table 5; 2025–26 club_other: article lists 3 goals, career table 1 | 2 | 2025–2026 (2) |
| `league/ucl/club_other goals (Wikipedia matches)` | 1999–2000 ucl: article lists 0 goals, career table unknown; 1999–2000 club_other: article lists 1 goals, career table unknown; 2000–01 ucl: article lists 0 goals, career table unknown; 2000–01 club_other: article lists 0 goals, career table unknown | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 1999–2000 league: article lists 11 goals, career table 17; 1999–2000 ucl: article lists 1 goals, career table 0; 1999–2000 club_other: article lists 8 goals, career table 9; 2000–01 league: article lists 15 goals, career table 17 | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 1999–2000 league: article lists 4 goals, career table 13; 1999–2000 ucl: article lists 3 goals, career table unknown; 1999–2000 club_other: article lists 0 goals, career table unknown; 2000–01 league: article lists 8 goals, career table 10; 2000–01 ucl: article lists 4 goals, career table unknown; 2000–01 club_other: article lists 0 goals, career table unknown | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 1999–2000 ucl: article lists 10 goals, career table unknown; 1999–2000 club_other: article lists 3 goals, career table unknown; 2000–01 ucl: article lists 7 goals, career table unknown; 2000–01 club_other: article lists 1 goals, career table unknown | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 1999–2000 league: article lists 2 goals, career table 1 | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 1999–2000: scoring match not assignable (15 October 1999, competition None, goals 1); 2000–01 ucl: article lists 1 goals, career table unknown; 2000–01 club_other: article lists 2 goals, career table unknown | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 ucl: article lists 2 goals, career table 0; 2000–01 club_other: article lists 5 goals, career table 7 | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 1999–2000: scoring match not assignable (17 September 1999, competition None, goals 2); 2000–01 ucl: article lists 0 goals, career table unknown; 2000–01 club_other: article lists 1 goals, career table unknown | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 1999–2000 league: article lists 0 goals, career table 37; 1999–2000 ucl: article lists 10 goals, career table unknown; 1999–2000 club_other: article lists 8 goals, career table unknown; 2000–01: scoring match not assignable (6 February 2001, competition None, goals 1) | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2000-01-01 | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2000-11-19 | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 1999–2000 ucl: article lists 0 goals, career table unknown; 1999–2000 club_other: article lists 0 goals, career table unknown; 2000–01 ucl: article lists 0 goals, career table unknown; 2000–01 club_other: article lists 0 goals, career table unknown | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 ucl: article lists 0 goals, career table unknown; 2000–01 club_other: article lists 0 goals, career table unknown | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 1999–2000 league: article lists 8 goals, career table 11; 1999–2000 ucl: article lists 3 goals, career table unknown; 1999–2000 club_other: article lists 0 goals, career table unknown; 2000–01 ucl: article lists 5 goals, career table unknown; 2000–01 club_other: article lists 2 goals, career table unknown | 1 | 2000–2000 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 ucl: article lists 7 goals, career table unknown; 2000–01 club_other: article lists 1 goals, career table unknown; 2001–02 ucl: article lists 6 goals, career table unknown; 2001–02 club_other: article lists 9 goals, career table unknown | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 league: article lists 15 goals, career table 17; 2001–02 ucl: article lists 8 goals, career table 7 | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 ucl: article lists 0 goals, career table unknown; 2000–01 club_other: article lists 0 goals, career table unknown; 2001–02 ucl: article lists 3 goals, career table unknown; 2001–02 club_other: article lists 2 goals, career table unknown | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 league: article lists 0 goals, career table 1 | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 league: article lists 0 goals, career table 4; 2000–01 ucl: article lists 1 goals, career table unknown; 2000–01 club_other: article lists 0 goals, career table unknown; 2001–02 league: article lists 0 goals, career table 2; 2001–02 ucl: article lists 1 goals, career table unknown; 2001–02 club_other: article lists 0 goals, career table unknown | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 ucl: article lists 0 goals, career table unknown; 2000–01 club_other: article lists 18 goals, career table unknown; 2001–02 ucl: article lists 3 goals, career table unknown; 2001–02 club_other: article lists 3 goals, career table unknown | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 league: article lists 25 goals, career table 26 | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 league: article lists 0 goals, career table 15; 2000–01 ucl: article lists 6 goals, career table 0; 2000–01 club_other: article lists 0 goals, career table 6; 2001–02 league: article lists 0 goals, career table 17; 2001–02 ucl: article lists 6 goals, career table 0; 2001–02 club_other: article lists 1 goals, career table 7 | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 league: article lists 8 goals, career table 10; 2000–01 ucl: article lists 4 goals, career table unknown; 2000–01 club_other: article lists 0 goals, career table unknown; 2001–02 ucl: article lists 0 goals, career table unknown; 2001–02 club_other: article lists 0 goals, career table unknown | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 ucl: article lists 0 goals, career table unknown; 2000–01 club_other: article lists 1 goals, career table unknown | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 league: article lists 0 goals, career table 3; 2000–01 club_other: article lists 0 goals, career table 6; 2000–01: scoring match not assignable (24 February 2001, competition None, goals 1); 2001–02: scoring match not assignable (23 September 2001, competition None, goals 1) | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 league: article lists 0 goals, career table 22; 2000–01 club_other: article lists 0 goals, career table 4; 2001–02 league: article lists 0 goals, career table 11; 2001–02 ucl: article lists 0 goals, career table unknown; 2001–02 club_other: article lists 0 goals, career table unknown | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 league: article lists 3 goals, career table 10; 2001–02 league: article lists 9 goals, career table 11 | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2000–01 ucl: article lists 0 goals, career table unknown; 2000–01 club_other: article lists 3 goals, career table unknown | 1 | 2001–2001 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 league: article lists 6 goals, career table 7 | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 ucl: article lists 3 goals, career table unknown; 2001–02 club_other: article lists 2 goals, career table unknown; 2002–03 ucl: article lists 3 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 ucl: article lists 5 goals, career table 6; 2002–03 league: article lists 0 goals, career table 10 | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 ucl: article lists 8 goals, career table 7; 2002–03 ucl: article lists 0 goals, career table 7 | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 ucl: article lists 6 goals, career table unknown; 2001–02 club_other: article lists 9 goals, career table unknown; 2002–03 ucl: article lists 9 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2002-01-01 | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 league: article lists 0 goals, career table 2; 2001–02 ucl: article lists 0 goals, career table unknown; 2001–02 club_other: article lists 0 goals, career table unknown; 2002–03 league: article lists 0 goals, career table 1; 2002–03 ucl: article lists 0 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 ucl: article lists 0 goals, career table unknown; 2001–02 club_other: article lists 4 goals, career table unknown; 2002–03 league: article lists 0 goals, career table 8; 2002–03 ucl: article lists 0 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 ucl: article lists 4 goals, career table 0; 2002–03 club_other: article lists 5 goals, career table 9 | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 league: article lists 22 goals, career table 23; 2002–03 league: article lists 24 goals, career table 25; 2002–03 club_other: article lists 4 goals, career table 5 | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 ucl: article lists 2 goals, career table unknown; 2001–02 club_other: article lists 2 goals, career table unknown; 2002–03 league: article lists 0 goals, career table 2; 2002–03 ucl: article lists 0 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 league: article lists 0 goals, career table 3; 2001–02 ucl: article lists 0 goals, career table unknown; 2001–02 club_other: article lists 0 goals, career table unknown; 2002–03 league: article lists 0 goals, career table 2; 2002–03 ucl: article lists 0 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 ucl: article lists 1 goals, career table unknown; 2001–02 club_other: article lists 0 goals, career table unknown; 2002–03 ucl: article lists 1 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 league: article lists 0 goals, career table 3; 2002–03 club_other: article lists 0 goals, career table 1 | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 league: article lists 0 goals, career table 4; 2001–02 ucl: article lists 0 goals, career table unknown; 2001–02 club_other: article lists 0 goals, career table unknown; 2002–03 league: article lists 0 goals, career table 3; 2002–03 ucl: article lists 0 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 league: article lists 0 goals, career table 10; 2002–03 ucl: article lists 0 goals, career table unknown; 2002–03 club_other: article lists 3 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 ucl: article lists 0 goals, career table unknown; 2001–02 club_other: article lists 0 goals, career table unknown; 2002–03 league: article lists 1 goals, career table 5; 2002–03 ucl: article lists 4 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2001–02 league: article lists 0 goals, career table 12; 2001–02 ucl: article lists 0 goals, career table unknown; 2001–02 club_other: article lists 0 goals, career table unknown; 2002–03 league: article lists 0 goals, career table 29; 2002–03 ucl: article lists 0 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown | 1 | 2002–2002 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 ucl: article lists 0 goals, career table 7 | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 ucl: article lists 3 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown; 2003–04 ucl: article lists 3 goals, career table unknown; 2003–04 club_other: article lists 1 goals, career table unknown | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 league: article lists 24 goals, career table 25; 2002–03 club_other: article lists 4 goals, career table 5; 2003–04 club_other: article lists 5 goals, career table 6 | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 ucl: article lists 9 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown; 2003–04 ucl: article lists 2 goals, career table unknown; 2003–04 club_other: article lists 7 goals, career table unknown | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03: scoring table row not assignable (3 August 2002, competition None, goals 2); 2003–04: scoring table row not assignable (30 July 2003, competition None, goals 1) | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 league: article lists 0 goals, career table 29; 2002–03 ucl: article lists 0 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown; 2003–04 league: article lists 0 goals, career table 23; 2003–04 ucl: article lists 0 goals, career table unknown; 2003–04 club_other: article lists 0 goals, career table unknown | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 league: article lists 14 goals, career table 23; 2003–04 league: article lists 0 goals, career table 14 | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 league: article lists 0 goals, career table 10; 2003–04 league: article lists 0 goals, career table 7 | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 league: article lists 0 goals, career table 13; 2002–03 ucl: article lists 2 goals, career table 5; 2002–03 club_other: article lists 0 goals, career table 3; 2003–04 league: article lists 0 goals, career table 13 | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 league: article lists 0 goals, career table 13; 2002–03 ucl: article lists 0 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown; 2003–04 league: article lists 0 goals, career table 16; 2003–04 ucl: article lists 0 goals, career table unknown; 2003–04 club_other: article lists 0 goals, career table unknown | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 league: article lists 17 goals, career table 18 | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2002–03 league: article lists 0 goals, career table 8; 2002–03 ucl: article lists 0 goals, career table unknown; 2002–03 club_other: article lists 0 goals, career table unknown; 2003–04 league: article lists 14 goals, career table 15; 2003–04 ucl: article lists 0 goals, career table unknown; 2003–04 club_other: article lists 7 goals, career table unknown | 1 | 2003–2003 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 league: article lists 14 goals, career table 15; 2003–04 ucl: article lists 0 goals, career table unknown; 2003–04 club_other: article lists 7 goals, career table unknown; 2004–05 league: article lists 8 goals, career table 9; 2004–05 ucl: article lists 4 goals, career table unknown; 2004–05 club_other: article lists 0 goals, career table unknown | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 league: article lists 9 goals, career table 8 | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 club_other: article lists 5 goals, career table 6; 2004–05 ucl: article lists 6 goals, career table 8 | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 ucl: article lists 0 goals, career table unknown; 2003–04 club_other: article lists 2 goals, career table unknown; 2004–05 league: article lists 0 goals, career table 5; 2004–05 ucl: article lists 0 goals, career table unknown; 2004–05 club_other: article lists 0 goals, career table unknown; 2004–05: no club-season article linked | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2004–05 league: article lists 1 goals, career table 9; 2004–05 ucl: article lists 1 goals, career table 2 | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 league: article lists 0 goals, career table 13; 2004–05: scoring match not assignable (30 July 2004, competition None, goals 1) | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 league: article lists 0 goals, career table 17; 2003–04 club_other: article lists 0 goals, career table 5; 2004–05 league: article lists 24 goals, career table 25 | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 ucl: article lists 3 goals, career table 4 | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 ucl: article lists 2 goals, career table 0; 2004–05 league: article lists 2 goals, career table 3 | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 league: article lists 18 goals, career table 19; 2003–04 ucl: article lists 5 goals, career table 0; 2003–04 club_other: article lists 8 goals, career table 13 | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 ucl: article lists 3 goals, career table unknown; 2003–04 club_other: article lists 1 goals, career table unknown; 2004–05 ucl: article lists 0 goals, career table unknown; 2004–05 club_other: article lists 0 goals, career table unknown | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 ucl: article lists 0 goals, career table unknown; 2003–04 club_other: article lists 5 goals, career table unknown; 2004–05 league: article lists 0 goals, career table 7; 2004–05 ucl: article lists 1 goals, career table unknown; 2004–05 club_other: article lists 1 goals, career table unknown | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 league: article lists 0 goals, career table 7; 2003–04 ucl: article lists 0 goals, career table unknown; 2003–04 club_other: article lists 0 goals, career table unknown; 2004–05 league: article lists 0 goals, career table 3; 2004–05 ucl: article lists 0 goals, career table unknown; 2004–05 club_other: article lists 0 goals, career table unknown | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 ucl: article lists 0 goals, career table unknown; 2003–04 club_other: article lists 0 goals, career table unknown; 2004–05 ucl: article lists 0 goals, career table unknown; 2004–05 club_other: article lists 0 goals, career table unknown | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2003–04 league: article lists 0 goals, career table 12; 2003–04 ucl: article lists 0 goals, career table unknown; 2003–04 club_other: article lists 0 goals, career table unknown; 2004–05 league: article lists 0 goals, career table 3; 2004–05 ucl: article lists 0 goals, career table unknown; 2004–05 club_other: article lists 0 goals, career table unknown | 1 | 2004–2004 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2004–05 league: article lists 8 goals, career table 9; 2004–05 ucl: article lists 4 goals, career table unknown; 2004–05 club_other: article lists 0 goals, career table unknown; 2005–06 league: article lists 18 goals, career table 17; 2005–06 ucl: article lists 7 goals, career table unknown; 2005–06 club_other: article lists 2 goals, career table unknown | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2004–05 league: article lists 1 goals, career table 7; 2004–05 ucl: article lists 2 goals, career table 4; 2005–06 ucl: article lists 10 goals, career table 7; 2005–06 club_other: article lists 8 goals, career table 6 | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2004–05: scoring match not assignable (30 July 2004, competition None, goals 1) | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2004–05 league: article lists 24 goals, career table 25 | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2004–05 league: article lists 0 goals, career table 15; 2004–05 ucl: article lists 0 goals, career table unknown; 2004–05 club_other: article lists 0 goals, career table unknown; 2005–06 league: article lists 0 goals, career table 12; 2005–06 ucl: article lists 2 goals, career table unknown; 2005–06 club_other: article lists 0 goals, career table unknown | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2004–05: scoring match not assignable (10 November 2004, competition None, goals 1); 2005–06: scoring match not assignable (, competition league, goals 1) | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2004–05 ucl: article lists 0 goals, career table unknown; 2004–05 club_other: article lists 0 goals, career table unknown; 2005–06: scoring match not assignable (27 November 2005/tim, competition None, goals 1) | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2005–06 ucl: article lists 2 goals, career table 1 | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2004–05 ucl: article lists 5 goals, career table unknown; 2004–05 club_other: article lists 0 goals, career table unknown; 2005–06 ucl: article lists 0 goals, career table unknown; 2005–06 club_other: article lists 0 goals, career table unknown | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2004–05 league: article lists 1 goals, career table 8; 2004–05 ucl: article lists 1 goals, career table 5; 2005–06 ucl: article lists 2 goals, career table unknown; 2005–06 club_other: article lists 2 goals, career table unknown | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2005-01-01 | 1 | 2005–2005 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2005–06 ucl: article lists 0 goals, career table unknown; 2005–06 club_other: article lists 0 goals, career table unknown; 2006–07 ucl: article lists 0 goals, career table unknown; 2006–07 club_other: article lists 0 goals, career table unknown | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2005–06 league: article lists 18 goals, career table 17; 2005–06 ucl: article lists 7 goals, career table unknown; 2005–06 club_other: article lists 2 goals, career table unknown; 2006–07 league: article lists 11 goals, career table 21; 2006–07 ucl: article lists 2 goals, career table unknown; 2006–07 club_other: article lists 1 goals, career table unknown | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2006-10-28 | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 club_other: article lists 0 goals, career table 1 | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2005–06 league: article lists 0 goals, career table 25; 2005–06 ucl: article lists 0 goals, career table 4; 2005–06 club_other: article lists 0 goals, career table 2; 2006–07 league: article lists 0 goals, career table 13; 2006–07 ucl: article lists 0 goals, career table unknown; 2006–07 club_other: article lists 2 goals, career table unknown | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2005–06 league: article lists 3 goals, career table 0; 2006–07 league: article lists 1 goals, career table 0 | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2005–06 ucl: article lists 0 goals, career table unknown; 2005–06 club_other: article lists 0 goals, career table unknown; 2006–07 ucl: article lists 1 goals, career table unknown; 2006–07 club_other: article lists 2 goals, career table unknown | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2005–06 league: article lists 0 goals, career table 12; 2006–07: scoring match not assignable (, competition league, goals 1) | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 ucl: article lists 1 goals, career table 0; 2006–07 club_other: article lists 0 goals, career table 1 | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2005–06 ucl: article lists 1 goals, career table unknown; 2005–06 club_other: article lists 1 goals, career table unknown; 2006–07 ucl: article lists 1 goals, career table unknown; 2006–07 club_other: article lists 0 goals, career table unknown | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07: scoring match not assignable (, competition league, goals 1) | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2005–06 league: article lists 0 goals, career table 25; 2005–06 ucl: article lists 0 goals, career table unknown; 2005–06 club_other: article lists 2 goals, career table unknown; 2006–07 league: article lists 0 goals, career table 16; 2006–07 ucl: article lists 0 goals, career table unknown; 2006–07 club_other: article lists 0 goals, career table unknown | 1 | 2006–2006 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 club_other: article lists 2 goals, career table 3 | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 ucl: article lists 1 goals, career table unknown; 2006–07 club_other: article lists 0 goals, career table unknown; 2007–08 league: article lists 0 goals, career table 10; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 16; 2007–08 ucl: article lists 0 goals, career table 4 | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 club_other: article lists 1 goals, career table 0; 2007–08 club_other: article lists 1 goals, career table 0 | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 ucl: article lists 1 goals, career table unknown; 2006–07 club_other: article lists 1 goals, career table unknown; 2007–08 league: article lists 0 goals, career table 11; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 league: article lists 11 goals, career table 21; 2006–07 ucl: article lists 2 goals, career table unknown; 2006–07 club_other: article lists 1 goals, career table unknown; 2007–08 league: article lists 0 goals, career table 8; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 ucl: article lists 2 goals, career table 3; 2006–07 club_other: article lists 0 goals, career table 1 | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 league: article lists 0 goals, career table 1; 2007 league: article lists 0 goals, career table 2; 2007 ucl: article lists 0 goals, career table unknown; 2007 club_other: article lists 0 goals, career table unknown; 2007–08 league: article lists 0 goals, career table 1; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 club_other: article lists 0 goals, career table 2; 2007–08 league: article lists 0 goals, career table 2; 2007–08 ucl: article lists 0 goals, career table 2 | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 league: article lists 1 goals, career table 0; 2007–08 league: article lists 1 goals, career table 0 | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 12; 2007–08 ucl: article lists 0 goals, career table 3; 2007–08 club_other: article lists 0 goals, career table 4 | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 club_other: article lists 2 goals, career table 1 | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 ucl: article lists 2 goals, career table unknown; 2006–07 club_other: article lists 2 goals, career table unknown; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007: scoring match not assignable (11 February, competition None, goals 1) | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 ucl: article lists 0 goals, career table unknown; 2006–07 club_other: article lists 11 goals, career table unknown; 2007–08 league: article lists 1 goals, career table 15; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 5 goals, career table unknown | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2006–07 club_other: article lists 0 goals, career table 1; 2007–08 league: article lists 0 goals, career table 16; 2007–08 ucl: article lists 0 goals, career table 1; 2007–08 club_other: article lists 0 goals, career table 1 | 1 | 2007–2007 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 club_other: article lists 2 goals, career table 3; 2008–09 league: article lists 17 goals, career table 18 | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 10; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown; 2008–09 ucl: article lists 9 goals, career table unknown; 2008–09 club_other: article lists 6 goals, career table unknown | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 7; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown; 2008–09 ucl: article lists 3 goals, career table unknown; 2008–09 club_other: article lists 1 goals, career table unknown | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 18; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown; 2008–09 league: article lists 10 goals, career table 28; 2008–09 ucl: article lists 0 goals, career table unknown; 2008–09 club_other: article lists 2 goals, career table unknown | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 club_other: article lists 1 goals, career table 0 | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 4; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown; 2008–09 league: article lists 0 goals, career table 2; 2008–09 ucl: article lists 0 goals, career table unknown; 2008–09 club_other: article lists 0 goals, career table unknown | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 league: article lists 4 goals, career table 10; 2008–09 ucl: article lists 3 goals, career table 6 | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 19; 2007–08 club_other: article lists 0 goals, career table 8; 2008–09 league: article lists 0 goals, career table 17; 2008–09 ucl: article lists 0 goals, career table 4 | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 club_other: article lists 5 goals, career table 6 | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 16; 2007–08 ucl: article lists 0 goals, career table 1; 2007–08 club_other: article lists 0 goals, career table 1 | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 league: article lists 2 goals, career table 3 | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 5; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown; 2008–09 league: article lists 1 goals, career table 4; 2008–09 ucl: article lists 1 goals, career table unknown; 2008–09 club_other: article lists 0 goals, career table unknown | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown; 2008–09 ucl: article lists 1 goals, career table unknown; 2008–09 club_other: article lists 2 goals, career table unknown | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 0 goals, career table unknown; 2008–09 ucl: article lists 0 goals, career table unknown; 2008–09 club_other: article lists 0 goals, career table unknown | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 16; 2007–08 ucl: article lists 0 goals, career table 4; 2008–09 league: article lists 0 goals, career table 4; 2008–09 club_other: article lists 0 goals, career table 3 | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09: scoring match not assignable (, competition league, goals 1) | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2007–08 league: article lists 0 goals, career table 12; 2007–08 ucl: article lists 0 goals, career table unknown; 2007–08 club_other: article lists 5 goals, career table unknown; 2008–09 league: article lists 1 goals, career table 5 | 1 | 2008–2008 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 ucl: article lists 9 goals, career table unknown; 2008–09 club_other: article lists 6 goals, career table unknown; 2009–10 ucl: article lists 8 goals, career table unknown; 2009–10 club_other: article lists 5 goals, career table unknown | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 league: article lists 17 goals, career table 18; 2009–10 club_other: article lists 2 goals, career table 0 | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 ucl: article lists 3 goals, career table unknown; 2008–09 club_other: article lists 1 goals, career table unknown; 2009–10 ucl: article lists 1 goals, career table unknown; 2009–10 club_other: article lists 3 goals, career table unknown | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 league: article lists 24 goals, career table 26 | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 league: article lists 2 goals, career table 3; 2009–10 league: article lists 0 goals, career table 15 | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10: scoring match not assignable (, competition league, goals 1) | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 ucl: article lists 1 goals, career table unknown; 2008–09 club_other: article lists 2 goals, career table unknown; 2009–10 ucl: article lists 0 goals, career table unknown; 2009–10 club_other: article lists 0 goals, career table unknown | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 league: article lists 0 goals, career table 32; 2008–09 ucl: article lists 0 goals, career table unknown; 2008–09 club_other: article lists 0 goals, career table unknown; 2009–10 league: article lists 0 goals, career table 18; 2009–10 ucl: article lists 0 goals, career table unknown; 2009–10 club_other: article lists 10 goals, career table unknown | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 ucl: article lists 2 goals, career table unknown; 2008–09 club_other: article lists 1 goals, career table unknown; 2009–10 league: article lists 0 goals, career table 6; 2009–10 ucl: article lists 2 goals, career table unknown; 2009–10 club_other: article lists 1 goals, career table unknown | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 ucl: article lists 0 goals, career table unknown; 2008–09 club_other: article lists 0 goals, career table unknown; 2009–10 ucl: article lists 0 goals, career table unknown; 2009–10 club_other: article lists 0 goals, career table unknown | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 league: article lists 0 goals, career table 12; 2008–09 club_other: article lists 0 goals, career table 9; 2009–10 club_other: article lists 3 goals, career table 2 | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2008–09 league: article lists 10 goals, career table 28; 2008–09 ucl: article lists 0 goals, career table unknown; 2008–09 club_other: article lists 2 goals, career table unknown; 2009–10 ucl: article lists 0 goals, career table unknown; 2009–10 club_other: article lists 7 goals, career table unknown | 1 | 2009–2009 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 ucl: article lists 8 goals, career table unknown; 2009–10 club_other: article lists 5 goals, career table unknown; 2010–11 ucl: article lists 12 goals, career table unknown; 2010–11 club_other: article lists 10 goals, career table unknown | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 ucl: article lists 1 goals, career table unknown; 2009–10 club_other: article lists 3 goals, career table unknown; 2010–11 ucl: article lists 2 goals, career table unknown; 2010–11 club_other: article lists 0 goals, career table unknown | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 league: article lists 0 goals, career table 18; 2009–10 ucl: article lists 0 goals, career table unknown; 2009–10 club_other: article lists 10 goals, career table unknown; 2010–11 ucl: article lists 0 goals, career table unknown; 2010–11 club_other: article lists 3 goals, career table unknown | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 club_other: article lists 2 goals, career table 0 | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 ucl: article lists 0 goals, career table unknown; 2009–10 club_other: article lists 7 goals, career table unknown; 2010–11 ucl: article lists 4 goals, career table unknown; 2010–11 club_other: article lists 1 goals, career table unknown | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 ucl: article lists 0 goals, career table unknown; 2009–10 club_other: article lists 0 goals, career table unknown; 2010–11 ucl: article lists 0 goals, career table unknown; 2010–11 club_other: article lists 1 goals, career table unknown | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 ucl: article lists 7 goals, career table 8 | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 league: article lists 10 goals, career table 9; 2009–10 club_other: article lists 1 goals, career table 2 | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 league: article lists 0 goals, career table 16; 2009–10 ucl: article lists 4 goals, career table unknown; 2009–10 club_other: article lists 3 goals, career table unknown; 2010–11 league: article lists 0 goals, career table 12; 2010–11 ucl: article lists 0 goals, career table unknown; 2010–11 club_other: article lists 1 goals, career table unknown | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 league: article lists 0 goals, career table 13; 2010–11 league: article lists 0 goals, career table 12 | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 league: article lists 0 goals, career table 2; 2010–11 league: article lists 0 goals, career table 4 | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2010-01-01 | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 ucl: article lists 0 goals, career table unknown; 2009–10 club_other: article lists 0 goals, career table unknown; 2010–11 ucl: article lists 0 goals, career table unknown; 2010–11 club_other: article lists 0 goals, career table unknown | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 league: article lists 0 goals, career table 15; 2010–11 league: article lists 1 goals, career table 3 | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 league: article lists 0 goals, career table 3; 2010–11 league: article lists 0 goals, career table 1 | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2009–10 club_other: article lists 2 goals, career table 1; 2010–11 league: article lists 0 goals, career table 3 | 1 | 2010–2010 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 ucl: article lists 12 goals, career table unknown; 2010–11 club_other: article lists 10 goals, career table unknown; 2011–12 ucl: article lists 14 goals, career table unknown; 2011–12 club_other: article lists 9 goals, career table unknown | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 ucl: article lists 2 goals, career table unknown; 2010–11 club_other: article lists 0 goals, career table unknown; 2011–12 ucl: article lists 1 goals, career table unknown; 2011–12 club_other: article lists 3 goals, career table unknown | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 league: article lists 25 goals, career table 27; 2011–12 ucl: article lists 1 goals, career table 0; 2011–12 club_other: article lists 5 goals, career table 7 | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 ucl: article lists 3 goals, career table 4; 2010–11 club_other: article lists 2 goals, career table 1 | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 ucl: article lists 0 goals, career table unknown; 2010–11 club_other: article lists 3 goals, career table unknown; 2011–12 ucl: article lists 0 goals, career table unknown; 2011–12 club_other: article lists 0 goals, career table unknown; 2011–12 ucl: article lists 0 goals, career table unknown; 2011–12 club_other: article lists 0 goals, career table unknown | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 ucl: article lists 7 goals, career table 8; 2011–12 club_other: article lists 2 goals, career table 0 | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011: scoring match not assignable (9 March, competition None, goals 2) | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 league: article lists 0 goals, career table 12; 2011–12 league: article lists 0 goals, career table 7 | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 ucl: article lists 4 goals, career table unknown; 2010–11 club_other: article lists 1 goals, career table unknown; 2011–12 ucl: article lists 3 goals, career table unknown; 2011–12 club_other: article lists 1 goals, career table unknown | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 league: article lists 0 goals, career table 4; 2011–12 league: article lists 0 goals, career table 3; 2011–12 ucl: article lists 0 goals, career table 1; 2011–12 club_other: article lists 2 goals, career table 1 | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 ucl: article lists 0 goals, career table unknown; 2010–11 club_other: article lists 1 goals, career table unknown; 2011–12 ucl: article lists 0 goals, career table unknown; 2011–12 club_other: article lists 1 goals, career table unknown | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 club_other: article lists 11 goals, career table 7; 2011–12 league: article lists 23 goals, career table 34; 2011–12 ucl: article lists 1 goals, career table unknown; 2011–12 club_other: article lists 6 goals, career table unknown | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 club_other: article lists 7 goals, career table 5; 2011–12 club_other: article lists 5 goals, career table 4 | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2010–11 league: article lists 1 goals, career table 3 | 1 | 2011–2011 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 ucl: article lists 14 goals, career table unknown; 2011–12 club_other: article lists 9 goals, career table unknown; 2012–13 ucl: article lists 8 goals, career table unknown; 2012–13 club_other: article lists 7 goals, career table unknown | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 ucl: article lists 1 goals, career table unknown; 2011–12 club_other: article lists 3 goals, career table unknown; 2012–13 ucl: article lists 1 goals, career table unknown; 2012–13 club_other: article lists 1 goals, career table unknown | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 league: article lists 4 goals, career table 5; 2012 league: article lists 0 goals, career table 8; 2012 club_other: article lists 8 goals, career table 0 | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 league: article lists 18 goals, career table 30; 2011–12 ucl: article lists 3 goals, career table 5; 2011–12 club_other: article lists 3 goals, career table 2 | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 ucl: article lists 0 goals, career table unknown; 2011–12 club_other: article lists 1 goals, career table unknown; 2012–13 ucl: article lists 0 goals, career table unknown; 2012–13 club_other: article lists 0 goals, career table unknown | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 ucl: article lists 3 goals, career table 0; 2011–12 club_other: article lists 0 goals, career table 3; 2012–13 club_other: article lists 3 goals, career table 2 | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012: scoring match not assignable (5 February, competition None, goals 1) | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 league: article lists 25 goals, career table 27; 2011–12 ucl: article lists 1 goals, career table 0; 2011–12 club_other: article lists 5 goals, career table 7; 2012–13 league: article lists 11 goals, career table 12 | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 league: article lists 23 goals, career table 34; 2011–12 ucl: article lists 1 goals, career table unknown; 2011–12 club_other: article lists 6 goals, career table unknown; 2012–13 league: article lists 12 goals, career table 30; 2012–13 ucl: article lists 2 goals, career table 0; 2012–13 club_other: article lists 3 goals, career table 5 | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 ucl: article lists 1 goals, career table unknown; 2011–12 club_other: article lists 0 goals, career table unknown; 2012–13 ucl: article lists 1 goals, career table unknown; 2012–13 club_other: article lists 0 goals, career table unknown | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 club_other: article lists 5 goals, career table 4; 2012–13 club_other: article lists 5 goals, career table 4 | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2011–12 ucl: article lists 2 goals, career table 0; 2011–12 club_other: article lists 3 goals, career table 4 | 1 | 2012–2012 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13 ucl: article lists 8 goals, career table unknown; 2012–13 club_other: article lists 7 goals, career table unknown; 2013–14 ucl: article lists 8 goals, career table unknown; 2013–14 club_other: article lists 6 goals, career table unknown | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2013-01-01 | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013: scoring match not assignable (19 January, competition None, goals 0) | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14 ucl: article lists 2 goals, career table 4 | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13 league: article lists 0 goals, career table 5; 2012–13 ucl: article lists 4 goals, career table unknown; 2012–13 club_other: article lists 4 goals, career table unknown; 2013–14: scoring table row not assignable (27 July – 20:30, competition None, goals 2) | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13: scoring match not assignable (14 February 2013, competition None, goals 2) | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13 club_other: article lists 3 goals, career table 2 | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13 club_other: article lists 4 goals, career table 2 | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13 ucl: article lists 1 goals, career table unknown; 2012–13 club_other: article lists 1 goals, career table unknown; 2013–14 ucl: article lists 1 goals, career table unknown; 2013–14 club_other: article lists 0 goals, career table unknown | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13 league: article lists 0 goals, career table 7; 2013–14 league: article lists 0 goals, career table 4; 2013–14 ucl: article lists 2 goals, career table 3 | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13 league: article lists 0 goals, career table 13; 2013–14: scoring table row not assignable (25 September, competition None, goals 1) | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13 ucl: article lists 0 goals, career table unknown; 2012–13 club_other: article lists 9 goals, career table unknown; 2013–14 ucl: article lists 4 goals, career table unknown; 2013–14 club_other: article lists 5 goals, career table unknown | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2012–13 ucl: article lists 1 goals, career table 0 | 1 | 2013–2013 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14 ucl: article lists 8 goals, career table unknown; 2013–14 club_other: article lists 6 goals, career table unknown; 2014–15 ucl: article lists 11 goals, career table unknown; 2014–15 club_other: article lists 5 goals, career table unknown | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14: scoring table row not assignable (27 July – 20:30, competition None, goals 2); 2014–15 ucl: article lists 2 goals, career table unknown; 2014–15 club_other: article lists 0 goals, career table unknown | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14: scoring table row not assignable (25 September, competition None, goals 1) | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 club_other: article lists 8 goals, career table 7 | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14 league: article lists 0 goals, career table 2; 2013–14 ucl: article lists 1 goals, career table unknown; 2013–14 club_other: article lists 1 goals, career table unknown; 2014–15 ucl: article lists 0 goals, career table unknown; 2014–15 club_other: article lists 0 goals, career table unknown | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14 ucl: article lists 3 goals, career table unknown; 2013–14 club_other: article lists 4 goals, career table unknown | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 ucl: article lists 0 goals, career table unknown; 2014–15 club_other: article lists 1 goals, career table unknown | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14: scoring table row not assignable (17 December – 20:30, competition None, goals 1) | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14 club_other: article lists 4 goals, career table 2; 2014–15 club_other: article lists 2 goals, career table 1 | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14 league: article lists 0 goals, career table 4; 2013–14 ucl: article lists 2 goals, career table 3 | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2014-01-01 | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2013–14 ucl: article lists 3 goals, career table unknown; 2013–14 club_other: article lists 0 goals, career table unknown; 2014–15 ucl: article lists 0 goals, career table unknown; 2014–15 club_other: article lists 3 goals, career table unknown | 1 | 2014–2014 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 ucl: article lists 11 goals, career table unknown; 2014–15 club_other: article lists 5 goals, career table unknown; 2015–16 ucl: article lists 6 goals, career table unknown; 2015–16 club_other: article lists 9 goals, career table unknown | 1 | 2015–2015 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 club_other: article lists 8 goals, career table 7; 2015–16 ucl: article lists 4 goals, career table 3; 2015–16 club_other: article lists 5 goals, career table 4 | 1 | 2015–2015 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 ucl: article lists 3 goals, career table 4; 2014–15 club_other: article lists 6 goals, career table 5 | 1 | 2015–2015 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 league: article lists 26 goals, career table 33; 2014–15 ucl: article lists 6 goals, career table 0; 2014–15 club_other: article lists 0 goals, career table 2; 2015–16 league: article lists 24 goals, career table 30; 2015–16 ucl: article lists 3 goals, career table unknown; 2015–16 club_other: article lists 3 goals, career table unknown | 1 | 2015–2015 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2015-01-01 | 1 | 2015–2015 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 league: article lists 8 goals, career table 7; 2014–15 ucl: article lists 3 goals, career table 1 | 1 | 2015–2015 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 club_other: article lists 2 goals, career table 1 | 1 | 2015–2015 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 ucl: article lists 0 goals, career table unknown; 2014–15 club_other: article lists 0 goals, career table unknown; 2015–16 ucl: article lists 0 goals, career table unknown; 2015–16 club_other: article lists 0 goals, career table unknown | 1 | 2015–2015 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2014–15 ucl: article lists 2 goals, career table unknown; 2014–15 club_other: article lists 0 goals, career table unknown; 2015–16 ucl: article lists 2 goals, career table unknown; 2015–16 club_other: article lists 1 goals, career table unknown | 1 | 2015–2015 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2015–16 ucl: article lists 6 goals, career table unknown; 2015–16 club_other: article lists 9 goals, career table unknown; 2016–17 ucl: article lists 11 goals, career table unknown; 2016–17 club_other: article lists 7 goals, career table unknown | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2015–16 league: article lists 23 goals, career table 22; 2015–16 ucl: article lists 8 goals, career table 7 | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 club_other: article lists 6 goals, career table 5 | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2015–16 ucl: article lists 4 goals, career table 3; 2015–16 club_other: article lists 5 goals, career table 4; 2016–17 club_other: article lists 4 goals, career table 3 | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2015–16 league: article lists 19 goals, career table 17 | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 club_other: article lists 3 goals, career table 4 | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2015–16 ucl: article lists 0 goals, career table unknown; 2015–16 club_other: article lists 0 goals, career table unknown; 2016–17 ucl: article lists 1 goals, career table unknown; 2016–17 club_other: article lists 0 goals, career table unknown | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2015–16 league: article lists 24 goals, career table 30; 2015–16 ucl: article lists 3 goals, career table unknown; 2015–16 club_other: article lists 3 goals, career table unknown; 2016–17 league: article lists 21 goals, career table 31; 2016–17 ucl: article lists 5 goals, career table 0; 2016–17 club_other: article lists 9 goals, career table 6 | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 ucl: article lists 4 goals, career table unknown; 2016–17 club_other: article lists 5 goals, career table unknown | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2015–16 ucl: article lists 0 goals, career table unknown; 2015–16 club_other: article lists 0 goals, career table unknown; 2016–17 ucl: article lists 0 goals, career table unknown; 2016–17 club_other: article lists 1 goals, career table unknown | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2015–16 ucl: article lists 1 goals, career table unknown; 2015–16 club_other: article lists 0 goals, career table unknown; 2016–17 ucl: article lists 1 goals, career table unknown; 2016–17 club_other: article lists 2 goals, career table unknown | 1 | 2016–2016 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 ucl: article lists 11 goals, career table unknown; 2016–17 club_other: article lists 7 goals, career table unknown; 2017–18: scoring match not assignable (26 August 2017, competition None, goals 2) | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 club_other: article lists 4 goals, career table 3; 2017–18 ucl: article lists 5 goals, career table 6 | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 ucl: article lists 1 goals, career table unknown; 2016–17 club_other: article lists 2 goals, career table unknown; 2017–18 ucl: article lists 1 goals, career table unknown; 2017–18 club_other: article lists 0 goals, career table unknown | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 league: article lists 0 goals, career table 2 | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 league: article lists 0 goals, career table 29; 2017–18 ucl: article lists 2 goals, career table 5; 2017–18 club_other: article lists 0 goals, career table 7 | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 ucl: article lists 2 goals, career table 0; 2016–17 club_other: article lists 4 goals, career table 6; 2017–18 club_other: article lists 5 goals, career table 4 | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 ucl: article lists 8 goals, career table unknown; 2016–17 club_other: article lists 6 goals, career table unknown; 2017–18 ucl: article lists 7 goals, career table unknown; 2017–18 club_other: article lists 5 goals, career table unknown | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 ucl: article lists 1 goals, career table unknown; 2016–17 club_other: article lists 0 goals, career table unknown; 2017–18 ucl: article lists 0 goals, career table unknown; 2017–18 club_other: article lists 2 goals, career table unknown | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 club_other: article lists 6 goals, career table 5; 2017–18: scoring match not assignable (9 September 2017, competition None, goals 1) | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 ucl: article lists 4 goals, career table unknown; 2016–17 club_other: article lists 5 goals, career table unknown; 2017–18 league: article lists 23 goals, career table 22; 2017–18 ucl: article lists 1 goals, career table unknown; 2017–18 club_other: article lists 3 goals, career table unknown | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 ucl: article lists 0 goals, career table unknown; 2016–17 club_other: article lists 1 goals, career table unknown; 2017–18 ucl: article lists 3 goals, career table unknown; 2017–18 club_other: article lists 0 goals, career table unknown | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 ucl: article lists 1 goals, career table unknown; 2016–17 club_other: article lists 0 goals, career table unknown; 2017–18 ucl: article lists 0 goals, career table unknown; 2017–18 club_other: article lists 0 goals, career table unknown | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 league: article lists 0 goals, career table 13; 2017–18 ucl: article lists 0 goals, career table 4; 2017–18 club_other: article lists 0 goals, career table 4 | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2016–17 ucl: article lists 8 goals, career table 7 | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 league: article lists 0 goals, career table 1; 2017–18 ucl: article lists 0 goals, career table 1; 2017–18 club_other: article lists 0 goals, career table 1 | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 club_other: article lists 1 goals, career table 0 | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 club_other: article lists 1 goals, career table 0; 2017–18: scoring match not assignable (24 February 2018, competition None, goals 1) | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 ucl: article lists 2 goals, career table 0; 2017–18 club_other: article lists 2 goals, career table 4 | 1 | 2017–2017 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 league: article lists 22 goals, career table 21; 2018–19 ucl: article lists 5 goals, career table 6 | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18: scoring match not assignable (26 August 2017, competition None, goals 2); 2018–19 ucl: article lists 12 goals, career table unknown; 2018–19 club_other: article lists 3 goals, career table unknown | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 league: article lists 33 goals, career table 32; 2017–18 ucl: article lists 10 goals, career table 11; 2017–18 club_other: article lists 3 goals, career table 1 | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 club_other: article lists 5 goals, career table 4 | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 ucl: article lists 5 goals, career table 6 | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18: scoring match not assignable (9 September 2017, competition None, goals 1) | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 league: article lists 12 goals, career table 13 | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 league: article lists 21 goals, career table 25; 2017–18 ucl: article lists 4 goals, career table unknown; 2017–18 club_other: article lists 6 goals, career table unknown; 2018–19 league: article lists 21 goals, career table 33; 2018–19 ucl: article lists 7 goals, career table unknown; 2018–19 club_other: article lists 5 goals, career table unknown | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 ucl: article lists 10 goals, career table 11; 2017–18 club_other: article lists 2 goals, career table 1 | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18: scoring match not assignable (14 October 2017, competition None, goals 0) | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 ucl: article lists 1 goals, career table unknown; 2017–18 club_other: article lists 0 goals, career table unknown; 2018–19 ucl: article lists 0 goals, career table unknown; 2018–19 club_other: article lists 5 goals, career table unknown | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 ucl: article lists 7 goals, career table unknown; 2017–18 club_other: article lists 5 goals, career table unknown; 2018–19 ucl: article lists 2 goals, career table unknown; 2018–19 club_other: article lists 3 goals, career table unknown | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 ucl: article lists 3 goals, career table unknown; 2017–18 club_other: article lists 0 goals, career table unknown; 2018–19 ucl: article lists 1 goals, career table unknown; 2018–19 club_other: article lists 0 goals, career table unknown | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2018-01-01 | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2017–18 ucl: article lists 0 goals, career table unknown; 2017–18 club_other: article lists 2 goals, career table unknown; 2018–19 ucl: article lists 1 goals, career table unknown; 2018–19 club_other: article lists 2 goals, career table unknown | 1 | 2018–2018 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 ucl: article lists 12 goals, career table unknown; 2018–19 club_other: article lists 3 goals, career table unknown; 2019–20 ucl: article lists 3 goals, career table unknown; 2019–20 club_other: article lists 3 goals, career table unknown | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 league: article lists 22 goals, career table 21; 2018–19 ucl: article lists 5 goals, career table 6; 2019–20 club_other: article lists 3 goals, career table 2 | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 league: article lists 0 goals, career table 22; 2018–19 ucl: article lists 0 goals, career table 8; 2018–19 club_other: article lists 0 goals, career table 10 | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 league: article lists 8 goals, career table 7 | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 ucl: article lists 0 goals, career table unknown; 2018–19 club_other: article lists 0 goals, career table unknown; 2019–20 ucl: article lists 0 goals, career table unknown; 2019–20 club_other: article lists 0 goals, career table unknown | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2019–20 club_other: article lists 8 goals, career table 5 | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2019–20 club_other: article lists 2 goals, career table 1 | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 league: article lists 21 goals, career table 33; 2018–19 ucl: article lists 7 goals, career table unknown; 2018–19 club_other: article lists 5 goals, career table unknown; 2019–20 league: article lists 17 goals, career table 24; 2019–20 ucl: article lists 2 goals, career table unknown; 2019–20 club_other: article lists 5 goals, career table unknown | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2019–20 club_other: article lists 5 goals, career table 4 | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 ucl: article lists 8 goals, career table 9; 2018–19 club_other: article lists 4 goals, career table 1; 2019–20 ucl: article lists 2 goals, career table 0; 2019–20 club_other: article lists 3 goals, career table 5 | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 club_other: article lists 5 goals, career table 4 | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2019–20 club_other: article lists 1 goals, career table 0 | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2018–19 ucl: article lists 3 goals, career table 4; 2018–19 club_other: article lists 6 goals, career table 4; 2019–20 ucl: article lists 2 goals, career table 0; 2019–20 club_other: article lists 0 goals, career table 2 | 1 | 2019–2019 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2020–21 ucl: article lists 5 goals, career table unknown; 2020–21 club_other: article lists 3 goals, career table unknown; 2021–22 ucl: article lists 6 goals, career table unknown; 2021–22 club_other: article lists 0 goals, career table unknown | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2020–21 league: article lists 42 goals, career table 41 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2020–21 league: article lists 8 goals, career table 7; 2020–21 ucl: article lists 2 goals, career table 1; 2021–22 league: article lists 7 goals, career table 6 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2021–22 league: article lists 24 goals, career table 23 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2020–21 league: article lists 7 goals, career table 6 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2020–21 league: article lists 29 goals, career table 27 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2020–21 league: article lists 11 goals, career table 10 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2020–21 league: article lists 10 goals, career table 9 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2021-01-01 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2021–22 league: article lists 12 goals, career table 11 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2020–21 ucl: article lists 4 goals, career table 0; 2020–21 club_other: article lists 6 goals, career table 10 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2021–22 league: article lists 22 goals, career table 21 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2020–21 ucl: article lists 0 goals, career table unknown; 2020–21 club_other: article lists 7 goals, career table unknown; 2021–22 league: article lists 10 goals, career table 9 | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2020–21 ucl: article lists 0 goals, career table unknown; 2020–21 club_other: article lists 0 goals, career table unknown; 2021–22 ucl: article lists 0 goals, career table unknown; 2021–22 club_other: article lists 1 goals, career table unknown | 1 | 2021–2021 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2021–22 league: article lists 24 goals, career table 23; 2022–23 league: article lists 20 goals, career table 19; 2022–23 club_other: article lists 5 goals, career table 3 | 1 | 2022–2022 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2021–22 league: article lists 12 goals, career table 11; 2022–23 ucl: article lists 5 goals, career table 3 | 1 | 2022–2022 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 league: article lists 10 goals, career table 9 | 1 | 2022–2022 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2021–22 ucl: article lists 0 goals, career table unknown; 2021–22 club_other: article lists 0 goals, career table unknown | 1 | 2022–2022 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2021–22 league: article lists 15 goals, career table 14 | 1 | 2022–2022 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 league: article lists 11 goals, career table 10; 2022–23 ucl: article lists 1 goals, career table 0; 2022–23 club_other: article lists 3 goals, career table 4 | 1 | 2022–2022 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2021–22 ucl: article lists 7 goals, career table 0; 2021–22 club_other: article lists 8 goals, career table 15 | 1 | 2022–2022 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 club_other: article lists 4 goals, career table 2 | 1 | 2022–2022 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 ucl: article lists 4 goals, career table unknown; 2022–23 club_other: article lists 2 goals, career table unknown | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2023–24 league: article lists 29 goals, career table 27 | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022 league: article lists 0 goals, career table 11; 2022 ucl: article lists 0 goals, career table unknown; 2022 club_other: article lists 0 goals, career table unknown; 2023–24 league: article lists 12 goals, career table 11 | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 ucl: article lists 6 goals, career table 5; 2023–24 league: article lists 17 goals, career table 15 | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 league: article lists 20 goals, career table 19; 2022–23 club_other: article lists 5 goals, career table 3 | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2023–24 league: article lists 6 goals, career table 5 | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022 league: article lists 0 goals, career table 8; 2022–23 ucl: article lists 4 goals, career table 2 | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 league: article lists 22 goals, career table 21; 2023–24 club_other: article lists 2 goals, career table 1 | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 ucl: article lists 2 goals, career table 1; 2022–23 club_other: article lists 1 goals, career table 0; 2023–24 club_other: article lists 3 goals, career table 2 | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 league: article lists 15 goals, career table 14; 2022–23 club_other: article lists 2 goals, career table 1 | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2022–23 ucl: article lists 3 goals, career table unknown; 2022–23 club_other: article lists 0 goals, career table unknown; 2023–24 ucl: article lists 0 goals, career table unknown; 2023–24 club_other: article lists 0 goals, career table unknown | 1 | 2023–2023 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2023–24 ucl: article lists 1 goals, career table unknown; 2023–24 club_other: article lists 1 goals, career table unknown; 2024–25 ucl: article lists 0 goals, career table unknown; 2024–25 club_other: article lists 0 goals, career table unknown | 1 | 2024–2024 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2023–24 league: article lists 29 goals, career table 27; 2024–25 league: article lists 23 goals, career table 22; 2024–25 ucl: article lists 7 goals, career table 8; 2024–25 club_other: article lists 6 goals, career table 4 | 1 | 2024–2024 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2023–24 club_other: article lists 2 goals, career table 1 | 1 | 2024–2024 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2024-07-31 | 1 | 2024–2024 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 10 goals, career table 11; 2024–25 club_other: article lists 5 goals, career table 4 | 1 | 2024–2024 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 4 goals, career table 5; 2024–25 club_other: article lists 1 goals, career table 0 | 1 | 2024–2024 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 club_other: article lists 1 goals, career table 0 | 1 | 2024–2024 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2023–24 league: article lists 1 goals, career table 0; 2024–25 league: article lists 16 goals, career table 15 | 1 | 2024–2024 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 1 goals, career table 2; 2024–25 club_other: article lists 3 goals, career table 1 | 1 | 2024–2024 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 6 goals, career table 8; 2024–25 club_other: article lists 8 goals, career table 6; 2025–26 league: article lists 11 goals, career table 10; 2025–26 ucl: article lists 9 goals, career table 8 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 league: article lists 17 goals, career table 16 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 1 goals, career table 2; 2024–25 club_other: article lists 3 goals, career table 1; 2025–26 club_other: article lists 1 goals, career table 0 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 4 goals, career table 3; 2025–26 club_other: article lists 3 goals, career table 2 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 league: article lists 16 goals, career table 15; 2025–26 league: article lists 11 goals, career table 10 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 3 goals, career table 4; 2024–25 club_other: article lists 1 goals, career table 0 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 0 goals, career table unknown; 2024–25 club_other: article lists 2 goals, career table unknown; 2025–26 ucl: article lists 0 goals, career table unknown; 2025–26 club_other: article lists 0 goals, career table unknown | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 2 goals, career table 3; 2024–25 club_other: article lists 2 goals, career table 1; 2025–26 ucl: article lists 9 goals, career table 10; 2025–26 club_other: article lists 2 goals, career table 1 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 10 goals, career table 11; 2024–25 club_other: article lists 5 goals, career table 4; 2025–26 club_other: article lists 12 goals, career table 11 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 4 goals, career table 5; 2024–25 club_other: article lists 6 goals, career table 5; 2025–26 league: article lists 8 goals, career table 7; 2025–26 ucl: article lists 3 goals, career table 5; 2025–26 club_other: article lists 3 goals, career table 1 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 league: article lists 16 goals, career table 14 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 12 goals, career table 13; 2024–25 club_other: article lists 6 goals, career table 4; 2025–26 ucl: article lists 3 goals, career table 4; 2025–26 club_other: article lists 2 goals, career table 1 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 2 goals, career table unknown; 2024–25 club_other: article lists 2 goals, career table unknown; 2025–26 ucl: article lists 2 goals, career table unknown; 2025–26 club_other: article lists 0 goals, career table unknown | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 league: article lists 23 goals, career table 22; 2024–25 ucl: article lists 7 goals, career table 8; 2024–25 club_other: article lists 6 goals, career table 4; 2025–26 club_other: article lists 4 goals, career table 3 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 league: article lists 6 goals, career table 5 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2024–25 ucl: article lists 4 goals, career table 5; 2024–25 club_other: article lists 4 goals, career table 3 | 1 | 2025–2025 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 club_other: article lists 12 goals, career table 11 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 league: article lists 17 goals, career table 16; 2026–27 ucl: article lists 0 goals, career table 3 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025 league: article lists 30 goals, career table 29; 2025 ucl: article lists 0 goals, career table unknown; 2025 club_other: article lists 14 goals, career table unknown; 2026 ucl: article lists 0 goals, career table unknown; 2026 club_other: article lists 4 goals, career table unknown | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 ucl: article lists 9 goals, career table 10; 2025–26 club_other: article lists 2 goals, career table 1 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 league: article lists 11 goals, career table 10; 2025–26 ucl: article lists 9 goals, career table 8 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 club_other: article lists 4 goals, career table 3 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 ucl: article lists 0 goals, career table unknown; 2025–26 club_other: article lists 0 goals, career table unknown; 2026–27 ucl: article lists 0 goals, career table unknown; 2026–27 club_other: article lists 0 goals, career table unknown | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 club_other: article lists 1 goals, career table 0 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2026–27 ucl: article lists 4 goals, career table 3 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2026–27 club_other: article lists 1 goals, career table 0 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 ucl: article lists 1 goals, career table 2; 2025–26 club_other: article lists 1 goals, career table 0 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2026–27 league: article lists 3 goals, career table 4 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 league: article lists 24 goals, career table 33; 2026–27 league: article lists 0 goals, career table 4; 2026–27 ucl: article lists 0 goals, career table 1 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | 2025–26 league: article lists 13 goals, career table 10; 2025–26 ucl: article lists 0 goals, career table 3 | 1 | 2026–2026 (1) |
| `league/ucl/club_other goals (Wikipedia matches)` | career table has no season row covering 2026-07-31 | 1 | 2026–2026 (1) |
| `league_* (StatsBomb)` | club not in StatsBomb league data | 23 | 2000–2026 (15) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2018/2019 | 15 | 2019–2019 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2016/2017 does not hold every Real Madrid match | 13 | 2016–2017 (2) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2016/2017 | 13 | 2016–2017 (2) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2020/2021 | 12 | 2021–2021 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2004-2004 | 11 | 2004–2004 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2004/2005 | 11 | 2004–2005 (2) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2007/2008 | 11 | 2008–2008 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2021/2022 | 11 | 2022–2022 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 1999/2000 | 10 | 2000–2000 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2002/2003 | 10 | 2003–2003 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2006/2007 | 10 | 2007–2007 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2008/2009 | 10 | 2009–2009 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2017/2018 | 10 | 2018–2018 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2021-2022 | 10 | 2022–2022 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2023-2024 | 10 | 2024–2024 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2024-2025 | 10 | 2025–2025 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2000-2000 | 9 | 2000–2000 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2006/2007 | 9 | 2007–2007 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2022-2023 | 9 | 2023–2023 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2022/2023 | 8 | 2023–2023 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2023/2024 | 8 | 2024–2024 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2025/2026 | 8 | 2026–2026 (1) |
| `league_* (StatsBomb)` | StatsBomb has no La Liga 2001/2002 | 7 | 2002–2002 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2004/2005 | 7 | 2005–2005 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2010/2011 does not hold every Barcelona match | 7 | 2011–2011 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2012/2013 | 7 | 2013–2013 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2017/2018 does not hold every Real Madrid match | 7 | 2018–2018 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2000/2001 | 6 | 2001–2001 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2002-2002 | 6 | 2002–2002 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2003/2004 | 6 | 2004–2004 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2005/2006 | 6 | 2006–2006 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2009-2009 | 6 | 2009–2009 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2011/2012 does not hold every Real Madrid match | 6 | 2012–2012 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2013/2014 | 6 | 2014–2014 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2016/2017 does not hold every Barcelona match | 6 | 2016–2017 (2) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2016/2017 | 6 | 2016–2017 (2) |
| `league_* (StatsBomb)` | 3 club spells in the infobox overlap 2022-2023 | 6 | 2023–2023 (1) |
| `league_* (StatsBomb)` | StatsBomb has no La Liga 2024/2025 | 6 | 2025–2025 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2024/2025 | 6 | 2025–2025 (1) |
| `league_* (StatsBomb)` | StatsBomb has no La Liga 1999/2000 | 5 | 2000–2000 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2000/2001 | 5 | 2001–2001 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2000/2001 | 5 | 2001–2001 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2001-2001 | 5 | 2001–2001 (1) |
| `league_* (StatsBomb)` | StatsBomb has no La Liga 2002/2003 | 5 | 2003–2003 (1) |
| `league_* (StatsBomb)` | StatsBomb has no La Liga 2003/2004 | 5 | 2004–2004 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2005/2006 does not hold every Barcelona match | 5 | 2006–2006 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2008/2009 does not hold every Barcelona match | 5 | 2009–2009 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2009/2010 does not hold every Barcelona match | 5 | 2010–2010 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2009/2010 | 5 | 2010–2010 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2010/2011 does not hold every Real Madrid match | 5 | 2011–2011 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2011-2011 | 5 | 2011–2011 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2011/2012 does not hold every Barcelona match | 5 | 2012–2012 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2013-2013 | 5 | 2013–2013 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2014-2014 | 5 | 2014–2014 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2014/2015 does not hold every Real Madrid match | 5 | 2015–2015 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2016/2017 does not hold every Atlético Madrid match | 5 | 2016–2017 (2) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2019-2019 | 5 | 2019–2019 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2020/2021 | 5 | 2021–2021 (1) |
| `league_* (StatsBomb)` | StatsBomb has no La Liga 2023/2024 | 5 | 2024–2024 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2024/2025 | 5 | 2025–2025 (1) |
| `league_* (StatsBomb)` | StatsBomb has no La Liga 2025/2026 | 5 | 2026–2026 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2025-2026 | 5 | 2026–2026 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2025/2026 | 5 | 2026–2026 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 1999/2000 | 4 | 2000–2000 (1) |
| `league_* (StatsBomb)` | StatsBomb has no La Liga 2000/2001 | 4 | 2001–2001 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2001/2002 | 4 | 2002–2002 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2001/2002 | 4 | 2002–2002 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2003-2003 | 4 | 2003–2003 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2006-2006 | 4 | 2006–2006 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2005/2006 | 4 | 2006–2006 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2006/2007 does not hold every Real Madrid match | 4 | 2007–2007 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2007/2008 does not hold every Real Madrid match | 4 | 2008–2008 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2009/2010 | 4 | 2010–2010 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2011/2012 | 4 | 2012–2012 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2012/2013 | 4 | 2013–2013 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2013/2014 does not hold every Real Madrid match | 4 | 2014–2014 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2013/2014 does not hold every Barcelona match | 4 | 2014–2014 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2014/2015 | 4 | 2015–2015 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2014/2015 | 4 | 2015–2015 (1) |
| `league_* (StatsBomb)` | StatsBomb 1. Bundesliga 2015/2016 does not hold every Bayern Munich match | 4 | 2016–2016 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2021-2021 | 4 | 2021–2021 (1) |
| `league_* (StatsBomb)` | StatsBomb has no La Liga 2021/2022 | 4 | 2022–2022 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2001/2002 | 3 | 2002–2002 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2006/2007 does not hold every Barcelona match | 3 | 2007–2007 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2007-2007 | 3 | 2007–2007 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2007/2008 does not hold every Barcelona match | 3 | 2008–2008 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2007/2008 | 3 | 2008–2008 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2009/2010 does not hold every Real Madrid match | 3 | 2010–2010 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2010-2010 | 3 | 2010–2010 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2012-2012 | 3 | 2012–2012 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2012/2013 does not hold every Barcelona match | 3 | 2013–2013 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2016-2016 | 3 | 2016–2016 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2017-2017 | 3 | 2017–2017 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2016/2017 | 3 | 2017–2017 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2018-2018 | 3 | 2018–2018 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2017/2018 does not hold every Atlético Madrid match | 3 | 2018–2018 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2017/2018 does not hold every Barcelona match | 3 | 2018–2018 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2022/2023 | 3 | 2023–2023 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2023/2024 | 3 | 2024–2024 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2025/2026 | 3 | 2026–2026 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2002/2003 | 2 | 2003–2003 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2002/2003 | 2 | 2003–2003 (1) |
| `league_* (StatsBomb)` | StatsBomb Premier League 2003/2004 does not hold every Manchester United match | 2 | 2004–2004 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2004/2005 does not hold every Barcelona match | 2 | 2005–2005 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2005/2006 | 2 | 2006–2006 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2005/2006 | 2 | 2006–2006 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2006/2007 does not hold every Sevilla match | 2 | 2007–2007 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2007/2008 | 2 | 2008–2008 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2008/2009 | 2 | 2009–2009 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2009/2010 | 2 | 2010–2010 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2010/2011 | 2 | 2011–2011 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2010/2011 | 2 | 2011–2011 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2011/2012 | 2 | 2012–2012 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2012/2013 | 2 | 2013–2013 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Premier League 2013/2014 | 2 | 2014–2014 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2015-2015 | 2 | 2015–2015 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2016/2017 | 2 | 2017–2017 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2017/2018 | 2 | 2018–2018 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2018/2019 does not hold every Barcelona match | 2 | 2019–2019 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2018/2019 | 2 | 2019–2019 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2018/2019 | 2 | 2019–2019 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2020/2021 | 2 | 2021–2021 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2020/2021 does not hold every Real Madrid match | 2 | 2021–2021 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2020/2021 | 2 | 2021–2021 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2021/2022 | 2 | 2022–2022 (1) |
| `league_* (StatsBomb)` | StatsBomb has no La Liga 2022/2023 | 2 | 2023–2023 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2024/2025 | 2 | 2025–2025 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 1999/2000 | 1 | 2000–2000 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2001/2002 | 1 | 2002–2002 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2003/2004 | 1 | 2004–2004 (1) |
| `league_* (StatsBomb)` | StatsBomb Premier League 2003/2004 does not hold every Liverpool match | 1 | 2004–2004 (1) |
| `league_* (StatsBomb)` | StatsBomb Premier League 2003/2004 does not hold every Chelsea match | 1 | 2004–2004 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2004/2005 | 1 | 2005–2005 (1) |
| `league_* (StatsBomb)` | 3 club spells in the infobox overlap 2005-2005 | 1 | 2005–2005 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2004/2005 | 1 | 2005–2005 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2004/2005 does not hold every Real Madrid match | 1 | 2005–2005 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2005-2005 | 1 | 2005–2005 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2005/2006 does not hold every Real Madrid match | 1 | 2006–2006 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2005/2006 does not hold every Valencia match | 1 | 2006–2006 (1) |
| `league_* (StatsBomb)` | 3 club spells in the infobox overlap 2007-2007 | 1 | 2007–2007 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2007/2008 does not hold every Valencia match | 1 | 2008–2008 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2007/2008 does not hold every Villarreal match | 1 | 2008–2008 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2007/2008 does not hold every Atlético Madrid match | 1 | 2008–2008 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2007/2008 | 1 | 2008–2008 (1) |
| `league_* (StatsBomb)` | 2 club spells in the infobox overlap 2008-2008 | 1 | 2008–2008 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2008/2009 does not hold every Sevilla match | 1 | 2009–2009 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2008/2009 does not hold every Real Madrid match | 1 | 2009–2009 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2008/2009 does not hold every Atlético Madrid match | 1 | 2009–2009 (1) |
| `league_* (StatsBomb)` | 3 club spells in the infobox overlap 2009-2009 | 1 | 2009–2009 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2008/2009 does not hold every Valencia match | 1 | 2009–2009 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2008/2009 | 1 | 2009–2009 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2009/2010 does not hold every Atlético Madrid match | 1 | 2010–2010 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2010/2011 | 1 | 2011–2011 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2011/2012 does not hold every Atlético Madrid match | 1 | 2012–2012 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2011/2012 | 1 | 2012–2012 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2012/2013 does not hold every Real Madrid match | 1 | 2013–2013 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2012/2013 | 1 | 2013–2013 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2013/2014 | 1 | 2014–2014 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2013/2014 | 1 | 2014–2014 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2014/2015 | 1 | 2015–2015 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2014/2015 | 1 | 2015–2015 (1) |
| `league_* (StatsBomb)` | StatsBomb 1. Bundesliga 2015/2016 does not hold every Borussia Dortmund match | 1 | 2016–2016 (1) |
| `league_* (StatsBomb)` | 3 club spells in the infobox overlap 2018-2018 | 1 | 2018–2018 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2017/2018 | 1 | 2018–2018 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2018/2019 | 1 | 2019–2019 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2018/2019 does not hold every Real Madrid match | 1 | 2019–2019 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2020/2021 does not hold every Atlético Madrid match | 1 | 2021–2021 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2020/2021 does not hold every Barcelona match | 1 | 2021–2021 (1) |
| `league_* (StatsBomb)` | StatsBomb La Liga 2020/2021 does not hold every Villarreal match | 1 | 2021–2021 (1) |
| `league_* (StatsBomb)` | StatsBomb Ligue 1 2021/2022 does not hold every Paris Saint-Germain match | 1 | 2022–2022 (1) |
| `league_* (StatsBomb)` | 3 club spells in the infobox overlap 2021-2022 | 1 | 2022–2022 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2021/2022 | 1 | 2022–2022 (1) |
| `league_* (StatsBomb)` | StatsBomb Ligue 1 2022/2023 does not hold every Paris Saint-Germain match | 1 | 2023–2023 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2022/2023 | 1 | 2023–2023 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Ligue 1 2023/2024 | 1 | 2024–2024 (1) |
| `league_* (StatsBomb)` | 3 club spells in the infobox overlap 2023-2024 | 1 | 2024–2024 (1) |
| `league_* (StatsBomb)` | StatsBomb has no 1. Bundesliga 2024/2025 | 1 | 2025–2025 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Major League Soccer 2025 | 1 | 2026–2026 (1) |
| `league_* (StatsBomb)` | StatsBomb has no Serie A 2025/2026 | 1 | 2026–2026 (1) |
| `league_apps` | season total not verifiably inside the window | 581 | 2000–2026 (23) |
| `league_goals` | match-by-match goals did not pass the season-total check | 242 | 2000–2026 (26) |
| `match_rating_avg` | no permitted source publishes per-match ratings (FBref/Transfermarkt blocked) | 721 | 2000–2026 (26) |
| `minutes` | needs league, ucl, club_other and national all filled | 721 | 2000–2026 (26) |
| `national minutes/assists/cards` | no permitted source lists national-team line-ups, minutes or assists for every match | 721 | 2000–2026 (26) |
| `national_apps` | Aug-Jul window: the year table does not split at 1 Aug | 150 | 2022–2026 (5) |
| `national_apps` | France played 2 match(es) after the window end in 2018 | 7 | 2018–2018 (1) |
| `national_apps` | Spain played 1 match(es) after the window end in 2008 | 6 | 2008–2008 (1) |
| `national_apps` | Spain played 2 match(es) after the window end in 2009 | 6 | 2009–2009 (1) |
| `national_apps` | Brazil played 1 match(es) after the window end in 2002 | 5 | 2002–2002 (1) |
| `national_apps` | Portugal played 1 match(es) after the window end in 2004 | 5 | 2004–2004 (1) |
| `national_apps` | Italy played 1 match(es) after the window end in 2006 | 5 | 2006–2006 (1) |
| `national_apps` | no 2007 row in the international year table | 5 | 2007–2007 (1) |
| `national_apps` | Netherlands played 2 match(es) after the window end in 2019 | 5 | 2019–2019 (1) |
| `national_apps` | Italy played 2 match(es) after the window end in 2021 | 5 | 2021–2021 (1) |
| `national_apps` | no 2000 row in the international year table | 4 | 2000–2000 (1) |
| `national_apps` | no 2001 row in the international year table | 4 | 2001–2001 (1) |
| `national_apps` | no 2003 row in the international year table | 4 | 2003–2003 (1) |
| `national_apps` | Greece played 1 match(es) after the window end in 2004 | 4 | 2004–2004 (1) |
| `national_apps` | England played 1 match(es) after the window end in 2005 | 4 | 2005–2005 (1) |
| `national_apps` | France played 1 match(es) after the window end in 2006 | 4 | 2006–2006 (1) |
| `national_apps` | Germany played 1 match(es) after the window end in 2006 | 4 | 2006–2006 (1) |
| `national_apps` | Brazil played 2 match(es) after the window end in 2007 | 4 | 2007–2007 (1) |
| `national_apps` | England played 1 match(es) after the window end in 2009 | 4 | 2009–2009 (1) |
| `national_apps` | no 2009 row in the international year table | 4 | 2009–2009 (1) |
| `national_apps` | Argentina played 1 match(es) after the window end in 2016 | 4 | 2016–2016 (1) |
| `national_apps` | France played 1 match(es) after the window end in 2016 | 4 | 2016–2016 (1) |
| `national_apps` | France played 2 match(es) after the window end in 2017 | 4 | 2017–2017 (1) |
| `national_apps` | Brazil played 2 match(es) after the window end in 2018 | 4 | 2018–2018 (1) |
| `national_apps` | France played 2 match(es) after the window end in 2019 | 4 | 2019–2019 (1) |
| `national_apps` | England played 2 match(es) after the window end in 2021 | 4 | 2021–2021 (1) |
| `national_apps` | Argentina played 1 match(es) after the window end in 2000 | 3 | 2000–2000 (1) |
| `national_apps` | Germany played 1 match(es) after the window end in 2002 | 3 | 2002–2002 (1) |
| `national_apps` | France played 1 match(es) after the window end in 2002 | 3 | 2002–2002 (1) |
| `national_apps` | Spain played 1 match(es) after the window end in 2002 | 3 | 2002–2002 (1) |
| `national_apps` | France played 1 match(es) after the window end in 2004 | 3 | 2004–2004 (1) |
| `national_apps` | Spain played 1 match(es) after the window end in 2004 | 3 | 2004–2004 (1) |
| `national_apps` | Brazil played 1 match(es) after the window end in 2005 | 3 | 2005–2005 (1) |
| `national_apps` | France played 2 match(es) after the window end in 2005 | 3 | 2005–2005 (1) |
| `national_apps` | Brazil played 1 match(es) after the window end in 2006 | 3 | 2006–2006 (1) |
| `national_apps` | Argentina played 2 match(es) after the window end in 2007 | 3 | 2007–2007 (1) |
| `national_apps` | Italy played 2 match(es) after the window end in 2007 | 3 | 2007–2007 (1) |
| `national_apps` | Netherlands played 2 match(es) after the window end in 2007 | 3 | 2007–2007 (1) |
| `national_apps` | England played 1 match(es) after the window end in 2008 | 3 | 2008–2008 (1) |
| `national_apps` | Netherlands played 1 match(es) after the window end in 2008 | 3 | 2008–2008 (1) |
| `national_apps` | Brazil played 2 match(es) after the window end in 2009 | 3 | 2009–2009 (1) |
| `national_apps` | France played 2 match(es) after the window end in 2009 | 3 | 2009–2009 (1) |
| `national_apps` | Portugal played 1 match(es) after the window end in 2016 | 3 | 2016–2016 (1) |
| `national_apps` | Germany played 1 match(es) after the window end in 2016 | 3 | 2016–2016 (1) |
| `national_apps` | Spain played 1 match(es) after the window end in 2016 | 3 | 2016–2016 (1) |
| `national_apps` | Brazil played 2 match(es) after the window end in 2017 | 3 | 2017–2017 (1) |
| `national_apps` | Spain played 2 match(es) after the window end in 2017 | 3 | 2017–2017 (1) |
| `national_apps` | Belgium played 2 match(es) after the window end in 2017 | 3 | 2017–2017 (1) |
| `national_apps` | Croatia played 2 match(es) after the window end in 2018 | 3 | 2018–2018 (1) |
| `national_apps` | Belgium played 2 match(es) after the window end in 2018 | 3 | 2018–2018 (1) |
| `national_apps` | Uruguay played 2 match(es) after the window end in 2018 | 3 | 2018–2018 (1) |
| `national_apps` | Portugal played 2 match(es) after the window end in 2019 | 3 | 2019–2019 (1) |
| `national_apps` | Brazil played 2 match(es) after the window end in 2019 | 3 | 2019–2019 (1) |
| `national_apps` | France played 2 match(es) after the window end in 2021 | 3 | 2021–2021 (1) |
| `national_apps` | Portugal played 2 match(es) after the window end in 2021 | 3 | 2021–2021 (1) |
| `national_apps` | Spain played 2 match(es) after the window end in 2021 | 3 | 2021–2021 (1) |
| `national_apps` | no 2002 row in the international year table | 2 | 2002–2002 (1) |
| `national_apps` | Turkey played 1 match(es) after the window end in 2002 | 2 | 2002–2002 (1) |
| `national_apps` | Netherlands played 1 match(es) after the window end in 2002 | 2 | 2002–2002 (1) |
| `national_apps` | Senegal played 1 match(es) after the window end in 2002 | 2 | 2002–2002 (1) |
| `national_apps` | Brazil played 1 match(es) after the window end in 2004 | 2 | 2004–2004 (1) |
| `national_apps` | no 2004 row in the international year table | 2 | 2004–2004 (1) |
| `national_apps` | Czech Republic played 1 match(es) after the window end in 2004 | 2 | 2004–2004 (1) |
| `national_apps` | England played 1 match(es) after the window end in 2004 | 2 | 2004–2004 (1) |
| `national_apps` | no 2005 row in the international year table | 2 | 2005–2005 (1) |
| `national_apps` | Czech Republic played 2 match(es) after the window end in 2005 | 2 | 2005–2005 (1) |
| `national_apps` | Portugal played 1 match(es) after the window end in 2006 | 2 | 2006–2006 (1) |
| `national_apps` | England played 1 match(es) after the window end in 2006 | 2 | 2006–2006 (1) |
| `national_apps` | Spain played 1 match(es) after the window end in 2006 | 2 | 2006–2006 (1) |
| `national_apps` | Spain played 2 match(es) after the window end in 2007 | 2 | 2007–2007 (1) |
| `national_apps` | England played 2 match(es) after the window end in 2007 | 2 | 2007–2007 (1) |
| `national_apps` | France played 2 match(es) after the window end in 2007 | 2 | 2007–2007 (1) |
| `national_apps` | Portugal played 1 match(es) after the window end in 2008 | 2 | 2008–2008 (1) |
| `national_apps` | Argentina played 1 match(es) after the window end in 2008 | 2 | 2008–2008 (1) |
| `national_apps` | no 2008 row in the international year table | 2 | 2008–2008 (1) |
| `national_apps` | France played 1 match(es) after the window end in 2008 | 2 | 2008–2008 (1) |
| `national_apps` | Italy played 1 match(es) after the window end in 2008 | 2 | 2008–2008 (1) |
| `national_apps` | Ivory Coast played 2 match(es) after the window end in 2009 | 2 | 2009–2009 (1) |
| `national_apps` | Uruguay played 1 match(es) after the window end in 2016 | 2 | 2016–2016 (1) |
| `national_apps` | Argentina played 2 match(es) after the window end in 2017 | 2 | 2017–2017 (1) |
| `national_apps` | Italy played 2 match(es) after the window end in 2017 | 2 | 2017–2017 (1) |
| `national_apps` | Uruguay played 2 match(es) after the window end in 2017 | 2 | 2017–2017 (1) |
| `national_apps` | Germany played 2 match(es) after the window end in 2017 | 2 | 2017–2017 (1) |
| `national_apps` | Argentina played 2 match(es) after the window end in 2018 | 2 | 2018–2018 (1) |
| `national_apps` | Spain played 2 match(es) after the window end in 2018 | 2 | 2018–2018 (1) |
| `national_apps` | Argentina played 2 match(es) after the window end in 2019 | 2 | 2019–2019 (1) |
| `national_apps` | Senegal played 2 match(es) after the window end in 2019 | 2 | 2019–2019 (1) |
| `national_apps` | England played 2 match(es) after the window end in 2019 | 2 | 2019–2019 (1) |
| `national_apps` | Belgium played 2 match(es) after the window end in 2019 | 2 | 2019–2019 (1) |
| `national_apps` | Argentina played 2 match(es) after the window end in 2021 | 2 | 2021–2021 (1) |
| `national_apps` | Belgium played 2 match(es) after the window end in 2021 | 2 | 2021–2021 (1) |
| `national_apps` | Italy played 1 match(es) after the window end in 2002 | 1 | 2002–2002 (1) |
| `national_apps` | Portugal played 1 match(es) after the window end in 2002 | 1 | 2002–2002 (1) |
| `national_apps` | Ukraine played 1 match(es) after the window end in 2004 | 1 | 2004–2004 (1) |
| `national_apps` | Netherlands played 1 match(es) after the window end in 2004 | 1 | 2004–2004 (1) |
| `national_apps` | Sweden played 1 match(es) after the window end in 2004 | 1 | 2004–2004 (1) |
| `national_apps` | Cameroon played 1 match(es) after the window end in 2004 | 1 | 2004–2004 (1) |
| `national_apps` | Italy played 1 match(es) after the window end in 2004 | 1 | 2004–2004 (1) |
| `national_apps` | Sweden played 1 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_apps` | Cameroon played 2 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_apps` | Argentina played 2 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_apps` | Ivory Coast played 2 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_apps` | Germany played 1 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_apps` | Italy played 2 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_apps` | Portugal played 2 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_apps` | Ghana played 1 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_apps` | Spain played 2 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_apps` | Ivory Coast played 1 match(es) after the window end in 2006 | 1 | 2006–2006 (1) |
| `national_apps` | no 2006 row in the international year table | 1 | 2006–2006 (1) |
| `national_apps` | Portugal played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_apps` | Ivory Coast played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_apps` | Sweden played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_apps` | Mali played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_apps` | Czech Republic played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_apps` | Ghana played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_apps` | Bulgaria played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_apps` | Cameroon played 1 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_apps` | Wales played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_apps` | Sweden played 1 match(es) after the window end in 2008 | 1 | 2008–2008 (1) |
| `national_apps` | Brazil played 1 match(es) after the window end in 2008 | 1 | 2008–2008 (1) |
| `national_apps` | Cameroon played 1 match(es) after the window end in 2008 | 1 | 2008–2008 (1) |
| `national_apps` | Germany played 1 match(es) after the window end in 2008 | 1 | 2008–2008 (1) |
| `national_apps` | Ivory Coast played 1 match(es) after the window end in 2008 | 1 | 2008–2008 (1) |
| `national_apps` | Serbia played 2 match(es) after the window end in 2008 | 1 | 2008–2008 (1) |
| `national_apps` | Argentina played 2 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_apps` | Portugal played 2 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_apps` | Cameroon played 1 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_apps` | Sweden played 1 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_apps` | Bosnia and Herzegovina played 2 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_apps` | Serbia played 2 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_apps` | Uruguay played 2 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_apps` | Russia played 2 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_apps` | no 2010 row in the international year table | 1 | 2010–2010 (1) |
| `national_apps` | Cameroon played 1 match(es) after the window end in 2011 | 1 | 2011–2011 (1) |
| `national_apps` | no 2014 row in the international year table | 1 | 2014–2014 (1) |
| `national_apps` | no 2015 row in the international year table | 1 | 2015–2015 (1) |
| `national_apps` | Brazil played 1 match(es) after the window end in 2016 | 1 | 2016–2016 (1) |
| `national_apps` | England played 1 match(es) after the window end in 2016 | 1 | 2016–2016 (1) |
| `national_apps` | Italy played 1 match(es) after the window end in 2016 | 1 | 2016–2016 (1) |
| `national_apps` | Gabon played 1 match(es) after the window end in 2016 | 1 | 2016–2016 (1) |
| `national_apps` | Chile played 1 match(es) after the window end in 2016 | 1 | 2016–2016 (1) |
| `national_apps` | Poland played 1 match(es) after the window end in 2016 | 1 | 2016–2016 (1) |
| `national_apps` | Croatia played 1 match(es) after the window end in 2016 | 1 | 2016–2016 (1) |
| `national_apps` | Belgium played 1 match(es) after the window end in 2016 | 1 | 2016–2016 (1) |
| `national_apps` | Portugal played 2 match(es) after the window end in 2017 | 1 | 2017–2017 (1) |
| `national_apps` | Croatia played 2 match(es) after the window end in 2017 | 1 | 2017–2017 (1) |
| `national_apps` | Poland played 2 match(es) after the window end in 2017 | 1 | 2017–2017 (1) |
| `national_apps` | England played 2 match(es) after the window end in 2017 | 1 | 2017–2017 (1) |
| `national_apps` | Gabon played 2 match(es) after the window end in 2017 | 1 | 2017–2017 (1) |
| `national_apps` | Senegal played 2 match(es) after the window end in 2017 | 1 | 2017–2017 (1) |
| `national_apps` | Colombia played 2 match(es) after the window end in 2017 | 1 | 2017–2017 (1) |
| `national_apps` | Portugal played 2 match(es) after the window end in 2018 | 1 | 2018–2018 (1) |
| `national_apps` | Egypt played 1 match(es) after the window end in 2018 | 1 | 2018–2018 (1) |
| `national_apps` | England played 2 match(es) after the window end in 2018 | 1 | 2018–2018 (1) |
| `national_apps` | Wales played 2 match(es) after the window end in 2018 | 1 | 2018–2018 (1) |
| `national_apps` | Senegal played 1 match(es) after the window end in 2018 | 1 | 2018–2018 (1) |
| `national_apps` | Slovenia played 2 match(es) after the window end in 2018 | 1 | 2018–2018 (1) |
| `national_apps` | Egypt played 3 match(es) after the window end in 2019 | 1 | 2019–2019 (1) |
| `national_apps` | Poland played 2 match(es) after the window end in 2019 | 1 | 2019–2019 (1) |
| `national_apps` | Algeria played 2 match(es) after the window end in 2019 | 1 | 2019–2019 (1) |
| `national_apps` | Gabon played 2 match(es) after the window end in 2019 | 1 | 2019–2019 (1) |
| `national_apps` | Serbia played 2 match(es) after the window end in 2019 | 1 | 2019–2019 (1) |
| `national_apps` | South Korea played 5 match(es) after the window end in 2019 | 1 | 2019–2019 (1) |
| `national_apps` | Germany played 2 match(es) after the window end in 2019 | 1 | 2019–2019 (1) |
| `national_apps` | Poland played 2 match(es) after the window end in 2021 | 1 | 2021–2021 (1) |
| `national_apps` | Egypt played 8 match(es) after the window end in 2021 | 1 | 2021–2021 (1) |
| `national_apps` | Norway played 2 match(es) after the window end in 2021 | 1 | 2021–2021 (1) |
| `national_apps` | Brazil played 2 match(es) after the window end in 2021 | 1 | 2021–2021 (1) |
| `national_apps` | Uruguay played 2 match(es) after the window end in 2021 | 1 | 2021–2021 (1) |
| `national_apps` | Denmark played 2 match(es) after the window end in 2021 | 1 | 2021–2021 (1) |
| `national_apps` | Algeria played 8 match(es) after the window end in 2021 | 1 | 2021–2021 (1) |
| `national_apps` | Croatia played 2 match(es) after the window end in 2021 | 1 | 2021–2021 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2004-02-18 Portugal v England; year table: Portugal played 1 match(es) after the window end in 2004 | 3 | 2004–2004 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2006-03-01 Italy v Germany; year table: Italy played 1 match(es) after the window end in 2006 | 2 | 2006–2006 (1) |
| `national_goals` | goal list has 51 goals, year table 46; martj42: goalscorers incomplete for 2000-02-23 France v Poland; year table: no 2000 row in the international year table | 1 | 2000–2000 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2000-02-23 Thailand v Brazil; year table: no 2000 row in the international year table | 1 | 2000–2000 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2000-02-23 Netherlands v Germany; year table: no 2000 row in the international year table | 1 | 2000–2000 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2001-03-03 United States v Brazil; year table: no 2001 row in the international year table | 1 | 2001–2001 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2001-02-28 Italy v Argentina; year table: no 2001 row in the international year table | 1 | 2001–2001 (1) |
| `national_goals` | no international year table; martj42: player name never appears among this country's goalscorers; year table: no 2001 row in the international year table | 1 | 2001–2001 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2002-01-31 Brazil v Bolivia; year table: Brazil played 1 match(es) after the window end in 2002 | 1 | 2002–2002 (1) |
| `national_goals` | goal list has 51 goals, year table 46; martj42: goalscorers incomplete for 2002-02-13 France v Romania; year table: France played 1 match(es) after the window end in 2002 | 1 | 2002–2002 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2002-01-31 Brazil v Bolivia; year table: no 2002 row in the international year table | 1 | 2002–2002 (1) |
| `national_goals` | goal list has 28 goals, year table 35; martj42: goalscorers incomplete for 2002-02-13 Netherlands v England; year table: Netherlands played 1 match(es) after the window end in 2002 | 1 | 2002–2002 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2002-02-13 Italy v United States; year table: no 2002 row in the international year table | 1 | 2002–2002 (1) |
| `national_goals` | no international year table; martj42: player name never appears among this country's goalscorers; year table: no 2003 row in the international year table | 1 | 2003–2003 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2003-08-20 Turkey v Moldova; year table: no 2003 row in the international year table | 1 | 2003–2003 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2003-02-12 Italy v Portugal; year table: no 2003 row in the international year table | 1 | 2003–2003 (1) |
| `national_goals` | goal list has 51 goals, year table 46; martj42: goalscorers incomplete for 2004-02-18 Belgium v France; year table: France played 1 match(es) after the window end in 2004 | 1 | 2004–2004 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2004-04-28 Hungary v Brazil; year table: no 2004 row in the international year table | 1 | 2004–2004 (1) |
| `national_goals` | goal list has 28 goals, year table 35; martj42: goalscorers incomplete for 2004-02-18 Netherlands v United States; year table: Netherlands played 1 match(es) after the window end in 2004 | 1 | 2004–2004 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2004-02-18 Portugal v England; year table: Portugal played 1 match(es) after the window end in 2004 | 1 | 2004–2004 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2004-02-18 Greece v Bulgaria; year table: Greece played 1 match(es) after the window end in 2004 | 1 | 2004–2004 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2004-02-18 Belgium v France; year table: France played 1 match(es) after the window end in 2004 | 1 | 2004–2004 (1) |
| `national_goals` | goal list has 51 goals, year table 46; martj42: goalscorers incomplete for 2005-02-09 France v Sweden; year table: France played 2 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2005-02-09 Hong Kong v Brazil; year table: no 2005 row in the international year table | 1 | 2005–2005 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2005-03-26 Portugal v Canada; year table: Portugal played 2 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2005-03-26 Spain v China; year table: Spain played 2 match(es) after the window end in 2005 | 1 | 2005–2005 (1) |
| `national_goals` | goal list has 51 goals, year table 46; martj42: goalscorers incomplete for 2006-03-01 France v Slovakia; year table: France played 1 match(es) after the window end in 2006 | 1 | 2006–2006 (1) |
| `national_goals` | goal list has 4 goals, year table 71; martj42: goalscorers incomplete for 2006-03-01 Italy v Germany; year table: Germany played 1 match(es) after the window end in 2006 | 1 | 2006–2006 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2006-03-01 Saudi Arabia v Portugal; year table: Portugal played 1 match(es) after the window end in 2006 | 1 | 2006–2006 (1) |
| `national_goals` | no international year table; martj42: player name never appears among this country's goalscorers; year table: no 2006 row in the international year table | 1 | 2006–2006 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2006-03-01 Saudi Arabia v Portugal; year table: Portugal played 1 match(es) after the window end in 2006 | 1 | 2006–2006 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2007-02-06 Portugal v Brazil; year table: Portugal played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2007-08-22 Hungary v Italy; year table: Italy played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_goals` | goal list has 28 goals, year table 35; martj42: goalscorers incomplete for 2007-02-07 Netherlands v Russia; year table: Netherlands played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2007-08-22 Hungary v Italy; year table: no 2007 row in the international year table | 1 | 2007–2007 (1) |
| `national_goals` | no international year table; martj42: player name never appears among this country's goalscorers; year table: no 2007 row in the international year table | 1 | 2007–2007 (1) |
| `national_goals` | goal list has 51 goals, year table 46; martj42: goalscorers incomplete for 2007-03-28 France v Austria; year table: France played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_goals` | goal list has 14 goals, year table 13; martj42: goalscorers incomplete for 2007-05-26 Wales v New Zealand; year table: Wales played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_goals` | goal list has 13 goals, year table 9; martj42: goalscorers incomplete for 2007-02-07 France v Argentina; year table: Argentina played 2 match(es) after the window end in 2007 | 1 | 2007–2007 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2008-02-06 Italy v Portugal; year table: Portugal played 1 match(es) after the window end in 2008 | 1 | 2008–2008 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2008-02-06 Spain v France; year table: no 2008 row in the international year table | 1 | 2008–2008 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2008-08-20 DR Congo v Togo; year table: no 2008 row in the international year table | 1 | 2008–2008 (1) |
| `national_goals` | goal list has 28 goals, year table 35; martj42: goalscorers incomplete for 2008-02-06 Croatia v Netherlands; year table: Netherlands played 1 match(es) after the window end in 2008 | 1 | 2008–2008 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2008-02-06 Italy v Portugal; year table: Italy played 1 match(es) after the window end in 2008 | 1 | 2008–2008 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2009-02-11 Portugal v Finland; year table: Portugal played 2 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_goals` | goal list has 14 goals, year table 13; martj42: goalscorers incomplete for 2009-05-29 Wales v Estonia; year table: no 2009 row in the international year table | 1 | 2009–2009 (1) |
| `national_goals` | goal list has 51 goals, year table 46; martj42: goalscorers incomplete for 2009-06-05 France v Turkey; year table: France played 2 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2009-02-10 Brazil v Italy; year table: no 2009 row in the international year table | 1 | 2009–2009 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2009-02-11 Libya v Uruguay; year table: Uruguay played 2 match(es) after the window end in 2009 | 1 | 2009–2009 (1) |
| `national_goals` | goal list has 4 goals, year table 1; martj42: goalscorers incomplete for 2009-06-05 France v Turkey; year table: no 2009 row in the international year table | 1 | 2009–2009 (1) |
| `national_goals` | no international year table; martj42: player name never appears among this country's goalscorers; year table: no 2009 row in the international year table | 1 | 2009–2009 (1) |
| `national_goals` | no international year table; martj42: player name never appears among this country's goalscorers; year table: no 2010 row in the international year table | 1 | 2010–2010 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2014-06-04 Argentina v Trinidad and Tobago; year table: no 2014 row in the international year table | 1 | 2014–2014 (1) |
| `national_goals` | no international year table; martj42: goalscorers incomplete for 2015-03-28 Argentina v El Salvador; year table: no 2015 row in the international year table | 1 | 2015–2015 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2016-03-29 Portugal v Belgium; year table: Portugal played 1 match(es) after the window end in 2016 | 1 | 2016–2016 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2016-09-06 Chile v Bolivia; year table: Chile played 1 match(es) after the window end in 2016 | 1 | 2016–2016 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2017-03-28 Portugal v Sweden; year table: Portugal played 2 match(es) after the window end in 2017 | 1 | 2017–2017 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2017-06-07 Spain v Colombia; year table: Colombia played 2 match(es) after the window end in 2017 | 1 | 2017–2017 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2018-03-23 Portugal v Egypt; year table: Portugal played 2 match(es) after the window end in 2018 | 1 | 2018–2018 (1) |
| `national_goals` | goal list has 40 goals, year table 41; martj42: goalscorers incomplete for 2018-03-22 China v Wales; year table: Wales played 2 match(es) after the window end in 2018 | 1 | 2018–2018 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2021-06-09 Portugal v Israel; year table: Portugal played 2 match(es) after the window end in 2021 | 1 | 2021–2021 (1) |
| `national_goals` | no dated list of international goals; martj42: goalscorers incomplete for 2021-06-02 Germany v Denmark; year table: Denmark played 2 match(es) after the window end in 2021 | 1 | 2021–2021 (1) |
| `national_goals` | goal list has 18 goals, year table 146; martj42: goalscorers incomplete for 2021-09-04 Qatar v Portugal; year table: Aug-Jul window: the year table does not split at 1 Aug | 1 | 2022–2022 (1) |
| `national_goals` | goal list has 15 goals, year table 16; martj42: goalscorers incomplete for 2022-06-02 Mexico v Uruguay; year table: Aug-Jul window: the year table does not split at 1 Aug | 1 | 2022–2022 (1) |
| `red_cards` | needs league, ucl, club_other and national all filled | 721 | 2000–2026 (26) |
| `trophies_cup` | undated honours entry The second player <small>(after [[Javier Hernández]] in the [[2010–11 Manchester United F.C. season/2010–11 season]])</small> to score in the Premier League, [[FA Cup]], [[EFL Cup/League Cup]], European competition and [[FA Community Shield/Community Shield]] in a single season <small>([[2016–17 Manchester United F.C. season/2016–17 season]])</small> 2010–11 season: club season article | 2 | 2009–2012 (2) |
| `trophies_cup` | undated honours entry The second player <small>(after [[Javier Hernández]] in the [[2010–11 Manchester United F.C. season/2010–11 season]])</small> to score in the Premier League, [[FA Cup]], [[EFL Cup/League Cup]], European competition and [[FA Community Shield/Community Shield]] in a single season <small>([[2016–17 Manchester United F.C. season/2016–17 season]])</small> 2016–17 season: club season article | 2 | 2015–2016 (2) |
| `trophies_cup` | undated honours entry Polish Super Cup 2000: no date found in linked article | 1 | 2001–2001 (1) |
| `trophies_cup` | undated honours entry Polish League Cup 1999–2000: no date found in linked article | 1 | 2001–2001 (1) |
| `trophies_cup` | undated honours entry Dutch Super Cup 2005–06: no date found in linked article | 1 | 2004–2004 (1) |
| `trophies_cup` | undated honours entry Sheikh Jassim Cup 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `trophies_cup` | undated honours entry Sheikh Jassim Cup 2008: no date found in linked article | 1 | 2007–2007 (1) |
| `trophies_cup` | undated honours entry Copa do Brasil 2010: no date found in linked article | 1 | 2011–2011 (1) |
| `trophies_league` | undated honours entry The most expensive footballer in history 2001–2009: no date found in linked article | 7 | 2000–2006 (7) |
| `trophies_league` | undated honours entry IFFHS World Team of the Decade 2011–2020: no date found in linked article | 5 | 2016–2022 (5) |
| `trophies_league` | undated honours entry IFFHS UEFA Team of the Decade 2011–2020: no date found in linked article | 5 | 2016–2022 (5) |
| `trophies_league` | undated honours entry Longest goalscoring run in Ligue 1 2015–16: no date found in linked article | 3 | 2014–2016 (3) |
| `trophies_league` | undated honours entry Most goals scored in a single season (all competitions) 2015–16 season: club season article | 3 | 2014–2016 (3) |
| `trophies_league` | undated honours entry IFFHS Men's World Team 2017: no date found in linked article | 3 | 2016–2018 (3) |
| `trophies_league` | undated honours entry ESPN 2017: no date found in linked article | 3 | 2016–2018 (3) |
| `trophies_league` | undated honours entry Goal 50 2017–18: no date found in linked article | 3 | 2016–2018 (3) |
| `trophies_league` | undated honours entry IFFHS Men's World Team 2022: no date found in linked article | 3 | 2021–2023 (3) |
| `trophies_league` | undated honours entry Marca Leyenda Award 2022: no date found in linked article | 3 | 2021–2023 (3) |
| `trophies_league` | undated honours entry Honorary [[Master of Arts]] degree from the [[University of Salford]] for contributions to football and charity work in developing countries 2008: no date found in linked article | 2 | 2007–2009 (2) |
| `trophies_league` | undated honours entry Fastest Ligue 1 hat-trick 2016: no date found in linked article | 2 | 2015–2016 (2) |
| `trophies_league` | undated honours entry ESPN 2016: no date found in linked article | 2 | 2016–2017 (2) |
| `trophies_league` | undated honours entry IFFHS Men's World Team 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry ESPN 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry IFFHS World's Best Playmaker 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry ''The Guardian'' Best Footballer in the World 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry ''World Soccer'' Player of the Year 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry ''Dongqiudi'' Player of the Year 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry AIPS 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry Vyshcha Liha 1998–99: no date found in linked article | 1 | 2000–2000 (1) |
| `trophies_league` | undated honours entry Süper Lig 1998–99: no date found in linked article | 1 | 2000–2000 (1) |
| `trophies_league` | undated honours entry Süper Lig 1999–2000: no date found in linked article | 1 | 2000–2000 (1) |
| `trophies_league` | undated honours entry Ekstraklasa 1999–2000: no date found in linked article | 1 | 2001–2001 (1) |
| `trophies_league` | undated honours entry Turkish League 2001–02: no date found in linked article | 1 | 2002–2002 (1) |
| `trophies_league` | undated honours entry Campeonato Brasileiro Série A 2008: no date found in linked article | 1 | 2007–2007 (1) |
| `trophies_league` | undated honours entry Qatar Stars League 2007–08: no date found in linked article | 1 | 2007–2007 (1) |
| `trophies_league` | undated honours entry OBE 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `trophies_league` | undated honours entry Four Nations Tournament (Ghana) third place 2007: no date found in linked article | 1 | 2008–2008 (1) |
| `trophies_league` | undated honours entry Freedom of the City of Salford 2010: no date found in linked article | 1 | 2009–2009 (1) |
| `trophies_league` | undated honours entry Campeón de Campeones 2024: no date found in linked article | 1 | 2026–2026 (1) |
| `ucl_apps` | season total not verifiably inside the window | 603 | 2000–2026 (26) |
| `ucl_goals` | match-by-match goals did not pass the season-total check | 305 | 2000–2026 (26) |
| `ucl_stage` | no openfootball file for 2006-07 | 25 | 2007–2007 (1) |
| `ucl_stage` | no openfootball file for 2007-08 | 24 | 2008–2008 (1) |
| `ucl_stage` | no openfootball file for 1999-00 | 19 | 2000–2000 (1) |
| `ucl_stage` | no openfootball file for 2004-05 | 19 | 2005–2005 (1) |
| `ucl_stage` | no openfootball file for 2000-01 | 18 | 2001–2001 (1) |
| `ucl_stage` | no openfootball file for 2008-09 | 18 | 2009–2009 (1) |
| `ucl_stage` | no openfootball file for 2002-03 | 17 | 2003–2003 (1) |
| `ucl_stage` | no openfootball file for 2003-04 | 17 | 2004–2004 (1) |
| `ucl_stage` | no openfootball file for 2005-06 | 17 | 2006–2006 (1) |
| `ucl_stage` | no openfootball file for 2001-02 | 16 | 2002–2002 (1) |
| `ucl_stage` | no openfootball file for 2009-10 | 16 | 2010–2010 (1) |
| `ucl_stage` | no openfootball file for 2010-11 | 11 | 2011–2011 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2021-2022 | 9 | 2022–2022 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2023-2024 | 9 | 2024–2024 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2000-2000 | 8 | 2000–2000 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2004-2004 | 8 | 2004–2004 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2022-2023 | 7 | 2023–2023 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2002-2002 | 6 | 2002–2002 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2024-2025 | 6 | 2025–2025 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2001-2001 | 5 | 2001–2001 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2009-2009 | 5 | 2009–2009 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2011-2011 | 5 | 2011–2011 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2013-2013 | 5 | 2013–2013 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2019-2019 | 5 | 2019–2019 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2022-2023 | 5 | 2023–2023 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2003-2003 | 4 | 2003–2003 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2006-2006 | 4 | 2006–2006 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2014-2014 | 4 | 2014–2014 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2021-2021 | 4 | 2021–2021 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2025-2026 | 4 | 2026–2026 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2007-2007 | 3 | 2007–2007 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2010-2010 | 3 | 2010–2010 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2016-2016 | 3 | 2016–2016 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2017-2017 | 3 | 2017–2017 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2012-2012 | 2 | 2012–2012 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2015-2015 | 2 | 2015–2015 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2018-2018 | 2 | 2018–2018 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2005-2005 | 1 | 2005–2005 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2005-2005 | 1 | 2005–2005 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2007-2007 | 1 | 2007–2007 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2008-2008 | 1 | 2008–2008 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2009-2009 | 1 | 2009–2009 (1) |
| `ucl_stage` | club 'Santos FC' never matched an openfootball team name | 1 | 2012–2012 (1) |
| `ucl_stage` | club 'West Ham United F.C.' never matched an openfootball team name | 1 | 2016–2016 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2018-2018 | 1 | 2018–2018 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2021-2022 | 1 | 2022–2022 (1) |
| `ucl_stage` | club 'Athletic Bilbao' never matched an openfootball team name | 1 | 2024–2024 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2023-2024 | 1 | 2024–2024 (1) |
| `ucl_stage` | club 'Inter Miami CF' never matched an openfootball team name | 1 | 2026–2026 (1) |
| `ucl_stage` | club 'Al Qadsiah FC' never matched an openfootball team name | 1 | 2026–2026 (1) |
| `ucl_stage` | club 'Al-Nassr FC' never matched an openfootball team name | 1 | 2026–2026 (1) |
| `yellow_cards` | needs league, ucl, club_other and national all filled | 721 | 2000–2026 (26) |
