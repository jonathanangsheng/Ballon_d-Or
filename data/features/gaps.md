# Gaps in data/features

Every field left blank, and why. Per-row detail: `data/features/row_gaps.csv`.

## Source access (checked 2026-11-10)

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
  deadline. Ballon d'Or and its ceremony awards are never counted. Club-internal awards (linked
  only to a club-season article) are not counted.

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

## Columns that are always blank

| Column(s) | Reason |
|---|---|
| `ucl_*`, `club_other_*` match stats | No permitted source holds every UCL / cup match (Transfermarkt and FBref blocked; StatsBomb releases UCL finals only) |
| `national_apps/minutes/assists/ko_ga/yellow/red`, national advanced | martj42 lists goals only; no permitted source has national-team line-ups for every match |
| `apps`, `minutes`, `goals`, `assists`, `decisive_ga`, `yellow_cards`, `red_cards`, `gk_*` totals | Need every club and national bucket complete, never the case |
| `match_rating_avg` | No permitted source publishes ratings |
| Understat xG | Understat unreachable; xG comes only from StatsBomb where a bucket is complete |

## Missing fields by reason

| Field | Reason | Rows | Editions |
|---|---|---|---|
| `awards_count` | undated award IFFHS 2024: no date found in linked article | 11 | 2024–2024 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2024: no date found in linked article | 10 | 2024–2024 (1) |
| `awards_count` | undated award FIFPRO World 11 2025: no date found in linked article | 10 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2025: no date found in linked article | 9 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2018: no date found in linked article | 8 | 2018–2018 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2019: no date found in linked article | 8 | 2019–2019 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2023: no date found in linked article | 8 | 2023–2023 (1) |
| `awards_count` | undated award FIFPRO World 11 2026: no date found in linked article | 8 | 2026–2026 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2017: no date found in linked article | 7 | 2017–2017 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2021: no date found in linked article | 6 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS Men's World Team 2022: no date found in linked article | 6 | 2022–2022 (1) |
| `awards_count` | undated award ''The Athletic'' European Men's Team of the Season 2024–25: no date found in linked article | 6 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS 2021: no date found in linked article | 5 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS 2023: no date found in linked article | 5 | 2023–2023 (1) |
| `awards_count` | undated award UNFP 2024–25: no date found in linked article | 5 | 2025–2025 (1) |
| `awards_count` | undated award UEFA Team of the Year 2003: no date found in linked article | 4 | 2003–2003 (1) |
| `awards_count` | undated award FIFA World Cup All-Star Team 2006: no date found in linked article | 4 | 2006–2006 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2006: no date found in linked article | 4 | 2006–2006 (1) |
| `awards_count` | undated award UEFA 2015–16: no date found in linked article | 4 | 2016–2016 (1) |
| `awards_count` | undated award UEFA 2016–17: no date found in linked article | 4 | 2017–2017 (1) |
| `awards_count` | undated award CAF Team of the Year 2019: no date found in linked article | 4 | 2019–2019 (1) |
| `awards_count` | undated award IFFHS 2022: no date found in linked article | 4 | 2022–2022 (1) |
| `awards_count` | undated award FIFPRO Men's World 11 2024: no date found in linked article | 4 | 2024–2024 (1) |
| `awards_count` | undated award PFA Team of the Year 2025–26 Premier League: no date found in linked article | 4 | 2026–2026 (1) |
| `awards_count` | undated award UEFA Team of the Year 2002: no date found in linked article | 3 | 2002–2002 (1) |
| `awards_count` | undated award FIFA World Cup All-Star Team 2002: no date found in linked article | 3 | 2002–2002 (1) |
| `awards_count` | undated award FIFA 100 2004: no date found in linked article | 3 | 2004–2004 (1) |
| `awards_count` | undated award UEFA Team of the Year 2005: no date found in linked article | 3 | 2005–2005 (1) |
| `awards_count` | undated award FIFPro World XI 2005: no date found in linked article | 3 | 2005–2005 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2008: no date found in linked article | 3 | 2008–2008 (1) |
| `awards_count` | undated award ESM Team of the Year 2008–09: no date found in linked article | 3 | 2009–2009 (1) |
| `awards_count` | undated award ESM Team of the Year 2010–11: no date found in linked article | 3 | 2011–2011 (1) |
| `awards_count` | undated award PFA Player of the Month 2018: no date found in linked article | 3 | 2018–2018 (1) |
| `awards_count` | undated award Sports Illustrated 2010–2019: no date found in linked article | 3 | 2019–2019 (1) |
| `awards_count` | undated award ESM Team of the Year 2020–21: no date found in linked article | 3 | 2021–2021 (1) |
| `awards_count` | undated award PFA 2022: no date found in linked article | 3 | 2022–2022 (1) |
| `awards_count` | undated award Bundesliga Player of the Month 2022: no date found in linked article | 3 | 2022–2022 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2023: no date found in linked article | 3 | 2023–2023 (1) |
| `awards_count` | undated award FIFPRO World 11 2024: no date found in linked article | 3 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' Premier League Team of the Season 2024–25: no date found in linked article | 3 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS 2025: no date found in linked article | 3 | 2025–2025 (1) |
| `awards_count` | undated award UEFA Team of the Year 2001: no date found in linked article | 2 | 2001–2001 (1) |
| `awards_count` | undated award ESM Team of the Year 2002–03: no date found in linked article | 2 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Team of the Year 2004: no date found in linked article | 2 | 2004–2004 (1) |
| `awards_count` | undated award ESM Team of the Year 2004–05: no date found in linked article | 2 | 2005–2005 (1) |
| `awards_count` | undated award FIFA World Player of the Year 2006: no date found in linked article | 2 | 2006–2006 (1) |
| `awards_count` | undated award FIFPro World XI 2006: no date found in linked article | 2 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Team of the Year 2006: no date found in linked article | 2 | 2006–2006 (1) |
| `awards_count` | undated award CAF Team of the Year 2006: no date found in linked article | 2 | 2006–2006 (1) |
| `awards_count` | undated award FIFPro World XI 2007: no date found in linked article | 2 | 2007–2007 (1) |
| `awards_count` | undated award UEFA Team of the Year 2007: no date found in linked article | 2 | 2007–2007 (1) |
| `awards_count` | undated award CAF Team of the Year 2009: no date found in linked article | 2 | 2009–2009 (1) |
| `awards_count` | undated award Premier League Golden Boot Landmark Award 2011–12: no date found in linked article | 2 | 2012–2012 (1) |
| `awards_count` | undated award Paris Saint-Germain 2012: no date found in linked article | 2 | 2012–2012 (1) |
| `awards_count` | undated award Premios Univision Deportes 2014: no date found in linked article | 2 | 2014–2014 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' World Team 2015: no date found in linked article | 2 | 2015–2015 (1) |
| `awards_count` | undated award La Liga Player of the Month 2016: no date found in linked article | 2 | 2016–2016 (1) |
| `awards_count` | undated award CAF Team of the Year 2016: no date found in linked article | 2 | 2016–2016 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2016: no date found in linked article | 2 | 2016–2016 (1) |
| `awards_count` | undated award Paris Saint-Germain 2016: no date found in linked article | 2 | 2016–2016 (1) |
| `awards_count` | undated award La Liga Player of the Month 2017: no date found in linked article | 2 | 2017–2017 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2018: no date found in linked article | 2 | 2018–2018 (1) |
| `awards_count` | undated award CAF Team of the Year 2018: no date found in linked article | 2 | 2018–2018 (1) |
| `awards_count` | undated award Premier League Player of the Month 2018: no date found in linked article | 2 | 2018–2018 (1) |
| `awards_count` | undated award ''[[Sports Illustrated]]'' Premier League Team of the Decade 2010–2019: no date found in linked article | 2 | 2019–2019 (1) |
| `awards_count` | undated award PFA Player of the Month 2019: no date found in linked article | 2 | 2019–2019 (1) |
| `awards_count` | undated award BBC Goal of the Month 2019: no date found in linked article | 2 | 2019–2019 (1) |
| `awards_count` | undated award UNFP 2018–19: no date found in linked article | 2 | 2019–2019 (1) |
| `awards_count` | undated award Bundesliga 2019: no date found in linked article | 2 | 2019–2019 (1) |
| `awards_count` | undated award UEFA Nations League Finals Team of the Tournament 2019: no date found in linked article | 2 | 2019–2019 (1) |
| `awards_count` | undated award La Liga Player of the Month 2021: no date found in linked article | 2 | 2021–2021 (1) |
| `awards_count` | undated award PFA Player of the Month 2021: no date found in linked article | 2 | 2021–2021 (1) |
| `awards_count` | undated award BBC Goal of the Month 2021: no date found in linked article | 2 | 2021–2021 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2021: no date found in linked article | 2 | 2021–2021 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2022: no date found in linked article | 2 | 2022–2022 (1) |
| `awards_count` | undated award ESPN 2022–23: no date found in linked article | 2 | 2023–2023 (1) |
| `awards_count` | undated award ESM Team of the Season 2022–23: no date found in linked article | 2 | 2023–2023 (1) |
| `awards_count` | undated award CAF Team of the Year 2023: no date found in linked article | 2 | 2023–2023 (1) |
| `awards_count` | undated award PFA Player of the Month 2023: no date found in linked article | 2 | 2023–2023 (1) |
| `awards_count` | undated award Serie A Player of the Month 2023: no date found in linked article | 2 | 2023–2023 (1) |
| `awards_count` | undated award Bundesliga 2023: no date found in linked article | 2 | 2023–2023 (1) |
| `awards_count` | undated award ''The Athletic'' Premier League Team of the Season 2023–24: no date found in linked article | 2 | 2024–2024 (1) |
| `awards_count` | undated award Globe Soccer Best Player of the Year 2024: no date found in linked article | 2 | 2024–2024 (1) |
| `awards_count` | undated award UNFP 2023–24: no date found in linked article | 2 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' Ligue 1 Team of the Season 2023–24: no date found in linked article | 2 | 2024–2024 (1) |
| `awards_count` | undated award Globe Soccer Awards – Emerging Player 2024: no date found in linked article | 2 | 2024–2024 (1) |
| `awards_count` | undated award Bundesliga 2024: no date found in linked article | 2 | 2024–2024 (1) |
| `awards_count` | undated award Premier League Goal of the Month 2024: no date found in linked article | 2 | 2024–2024 (1) |
| `awards_count` | undated award CIES Football Observatory 2024–25: no date found in linked article | 2 | 2025–2025 (1) |
| `awards_count` | undated award Bundesliga Player of the Month 2025: no date found in linked article | 2 | 2025–2025 (1) |
| `awards_count` | undated award FIFPRO Men's World 11 2026: no date found in linked article | 2 | 2026–2026 (1) |
| `awards_count` | undated award UNFP 2025–26: no date found in linked article | 2 | 2026–2026 (1) |
| `awards_count` | undated award Portuguese Footballer of the Year 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award La Liga Foreign Player of the Year 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award World Soccer Player of the Year 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award El País King of European Soccer 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award RSSSF 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award FIFA 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award Onze d'Or 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award 2nd French Player of the Century (France Football) 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award UEFA European Championship Player of the Tournament 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award UEFA European Championship Team of the Tournament 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award Ukrainian Footballer of the Year 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award ADN Eastern European Footballer of the Season 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award Serie A Foreign Footballer of the Year 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award French Player of the Year 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award Serie A Defender of the Year 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award ESM Team of the Year 1999–2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award IFFHS World's Top Goal Scorer 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award UEFA Club Football Awards 1999–2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award La Liga's Team of the Decade 2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award Most assists in the Premier League 1999–2000: no date found in linked article | 1 | 2000–2000 (1) |
| `awards_count` | undated award ''World Soccer'' World Player of the Year 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Onze d'Argent 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award 2nd place 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Sportske Novosti award 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Best Bundesliga Keeper 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Best European Goalkeeper 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award UEFA Club Goalkeeper of the Year 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award ESM Team of the Year 2000–01: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award UEFA Champions League Final Man of the Match 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award German Footballer of the Year 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award UEFA Fair-Play Award 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Most assists in the Premier League 2000–01: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award BBC Sports Personality of the Year 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Serie A Italian Footballer of the Year 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award La Liga top assist provider 2000–01: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award La Liga Foreign Player of the Year 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Ukrainian Footballer of the Year 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award Onze d'Or 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award El País European Player of the Year 2001: no date found in linked article | 1 | 2001–2001 (1) |
| `awards_count` | undated award ''[[World Soccer (magazine)/World Soccer]]'' magazine [[World Soccer Player of the Year/World Player of the Year]] (3) 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award RSSSF 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award Onze d'Or 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award Intercontinental Cup Most Valuable Player 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award BBC World Sport Star of the Year 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award ESM Team of the Year 2001–02: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award Onze Mondial 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Club Defender of the Year 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award Best Bundesliga Keeper 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' Bundesliga Team of the Season 2001–02: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award Best European Goalkeeper 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Club Goalkeeper of the Year 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award FIFA World Cup Yashin Award 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award Onze d'Argent 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award FIFA 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award ''ESM'' Team of the Year 2001–02: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award France Football French Player of the Year 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award El País European Player of the Year 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Club Footballer of the Year 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award FIFA World Cup Dream Team 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award Footballer of the Year (Germany) 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' [[Bundesliga]] Team of the Season 2001–02: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award kicker Man of the Year (Mann des Jahres) 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award FIFA XI 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award FIFA World Cup Silver Shoe 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award World XI 2002: no date found in linked article | 1 | 2002–2002 (1) |
| `awards_count` | undated award Golden Ball (Czech Republic) 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Czech Footballer of the Year 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Sportsperson of the Year (Czech Republic) 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Serie A Footballer of the Year 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Serie A Foreign Footballer of the Year 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Guerin d'Oro 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Club Best Midfielder of the Year 2002–03: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award World Soccer Awards Player of the Year 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award RSSSF 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Onze d'Or 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award French Player of the Year 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award IFFHS 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Onze de Onze 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA President's Award 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Onze d'Argent 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award ''ESM'' Team of the Year 2002–03: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award El País European Player of the Year 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award BBC Goal of the Month 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Club Forward of the Year 2002–03: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award 3rd place 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Onze Mondial 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Club Defender of the Year 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Club Goalkeeper of the Year 2002–03: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award UEFA Club Footballer of the Year 2002–03: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Best European Goalkeeper 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award England Player of the Year 2003: no date found in linked article | 1 | 2003–2003 (1) |
| `awards_count` | undated award Ukrainian Footballer of the Year 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award ADN Eastern European Footballer of the Season 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Serie A Goal of the Year 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Baltic and Commonwealth of Independent States Footballer of the Year 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Pallone d'Argento 2003–04: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Year 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award UEFA Club Footballer of the Year 2003–04: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2003–04: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Portuguese League Footballer of the Year 2003–04: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award World Soccer Magazine World Player of The Year 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award RSSSF 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award European Golden Shoe 2003–04: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Premier League Player of the Month 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award French Player of the Year 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Greek Male Athlete of the Year 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Pirata d'Oro ([[Inter Milan/Internazionale]] Player of the Year) 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Copa América Golden Shoe 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Golden Ball (Czech Republic) 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Czech Footballer of the Year 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award UEFA European Championship Team of the Tournament 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Golden Foot 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award Golden Boy Award 2004: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award UEFA Club Best Defender of the Year 2003–04: no date found in linked article | 1 | 2004–2004 (1) |
| `awards_count` | undated award World Soccer Magazine World Player of The Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award RSSSF 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award UEFA Club Forward of the Year 2004–05: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Onze d'Or 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award FIFPro Player of the Season 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award FWA Footballer of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award PFA Fans' Player of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award England Player of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Chelsea Player of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award UEFA Club Footballer of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Onze d'Argent 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Liverpool Fans Online Player of the Season 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award European Golden Shoe 2004–05: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award French Player of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Ukrainian Footballer of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award ADN Eastern European Footballer of the Season 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Baltic and Commonwealth of Independent States Footballer of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Golden Foot 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award IFFHS World's Top Goal Scorer 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Serie A Most Loved Player 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Guldbollen 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2004–05: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award African Player of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award CAF Team of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2004–05: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award UEFA Club Defender of the Year 2005: no date found in linked article | 1 | 2005–2005 (1) |
| `awards_count` | undated award Serie A Defender of the Year 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFA World Cup Silver Ball 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award World Soccer Player of the Year 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award Serie A Footballer of the Year 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award Serie A Italian Footballer of the Year 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award Serie A "Fan" Award 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award Onze d'Or 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award French Player of the Year 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFPro Player of the Season 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Club Footballer of the Year 2005–06: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFA World Cup Golden Ball 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award ESM Team of the Year 2005–06: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award African Cup of Nations top goalscorer 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Club Forward of the Year 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award Bundesliga Player of the Season 2005–06: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award Bundesliga top assist provider 2005–06: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' Bundesliga Team of the Season 2005–06: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award African Footballer of the Year 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award Ivory Coast Player of the Year 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFA World Cup Bronze Ball 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFA World Cup top assists provider 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Goalkeeper of the Year 2006: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award UEFA Club Football Awards 2005–06: no date found in linked article | 1 | 2006–2006 (1) |
| `awards_count` | undated award FIFPro World Player of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award UEFA Club Forward of the Year 2006–07: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award UEFA Club Footballer of the Year 2006–07: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Pallone d'Argento 2006–07: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award World Soccer Player of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A Foreign Footballer of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A Footballer of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award IAAF Latin Sportsman of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Onze d'Or 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award FIFPRO World 11 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Chelsea Players' Player of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Ivory Coast Player of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Onze de Bronze 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A Player of the Month 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Guldbollen 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Jerringpriset 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Copa América Golden Boot 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A Italian Footballer of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award European Golden Shoe 2006–07: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award Serie A Goalscorer of the Year 2007: no date found in linked article | 1 | 2007–2007 (1) |
| `awards_count` | undated award European Golden Shoe 2007–08: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFPRO World 11 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award ESM Team of the Year 2007–08: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Premier League Player of the Year by Northwest Football Awards 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFA FIFPro World11 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Baltic and Commonwealth of Independent States Footballer of the Year 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award ADN Eastern European Footballer of the Season 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award L'Équipe 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Serie A Player of the Month 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Serie A Goal of the Year 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Golden Tapir 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Guldbollen 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Fotbollskanalens hederspris 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Swedish Male Athlete of the Year 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFPro World XI 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Time 100 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Maracanã Hall of Fame 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Samba Gold 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award Honorary Fellowship 2008: no date found in linked article | 1 | 2008–2008 (1) |
| `awards_count` | undated award FIFPRO World 11 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2008–09: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award La Liga Midfielder of the Year 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award FIFA FIFPro World11 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award La Liga Best Spanish Player 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award La Liga Best Midfielder 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award Onze de Bronze 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award UEFA Team of the Year 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award Time 100 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award MARCA Legend Award 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award Guldbollen 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award England Senior Men's Player of the Year 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award African Footballer of the Year 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award BBC African Footballer of the Year 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award BBC Goal of the Month 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award Liverpool Player of the Season 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2009: no date found in linked article | 1 | 2009–2009 (1) |
| `awards_count` | undated award European Golden Shoe 2009–10: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFPRO World 11 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award La Liga Midfielder of the Year 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award Don Balón Team of the Decade 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award ESPN Deportes Player of the Year 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award UEFA Club Midfielder of the Year 2009–10: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFA World Cup Bronze Boot 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award Goal 50 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award UEFA Team of the Year 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award ESM Team of the Year 2009–10: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFA World Cup Goal of the Tournament 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFA World Cup top goalscorer 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award Best European Goalkeeper 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award IFFHS Best Goalkeeper of the Decade 2001–2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award USSA Male Athlete of the Year 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award CAF Team of the Year 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award Chelsea Player of the Year 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award ''Time'' Top 100 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award West African Footballer of the Year 2010: no date found in linked article | 1 | 2010–2010 (1) |
| `awards_count` | undated award FIFPRO World 11 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award Argentine Sportsperson of the Year 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award European Golden Shoe 2010–11: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award La Liga Midfielder of the Year 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award La Liga Best Midfielder 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award Onze d'Argent 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award Marca Legend Award 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award CAF Team of the Year 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award Bola de Prata 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award Copa Libertadores Best Player 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award Copa Libertadores top assist provider 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award Troféu Mesa Redonda 2011: no date found in linked article | 1 | 2011–2011 (1) |
| `awards_count` | undated award European Golden Shoe 2011–12: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award FIFPRO World 11 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award La Liga Best Midfielder 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award ESM Team of the Year 2011–12: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award ''[[The Guardian]]'' European Team of the Year 2011–12: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award ''[[Bleacher Report]]'' La Liga Player of the Season 2011–12: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award ''Bleacher Report'' La Liga Starting XI 2011–12: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award UEFA Super Cup Man of the Match 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Globe Soccer 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award La Liga Best Goalkeeper 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award IFFHS Best Goalkeeper of the Past 25 Years 1987–2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Premio Bulgarelli Number 8 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Pallone d'Argento 2011–12: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Pallone Azzurro 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Guerin d'Oro 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Serie A Midfielder of the Year 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Serie A Footballer of the Year 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award CAF Team of the Year 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award GQ Sportsman of the Year 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Ivory Coast Player of the Year 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2011–12: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award PFA Fans' Player of the Year 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award FWA Footballer of the Year 2011–12: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Golden Foot 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Serie A Player of the Month 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Golden Tapir 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Sportschau Goal of the Month Award 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Sportschau Goal of the Year Award 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Ligue 1 Player of the Month 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Ligue 1 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Guldbollen 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Malmö 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award Swedish Goal of the Year 2012: no date found in linked article | 1 | 2012–2012 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award European Golden Shoe 2012–13: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award FIFPRO World 11 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award French Player of the Year 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award UEFA Super Cup Man of the Match 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' Bundesliga Team of the Season 2012–13: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Bundesliga top assist provider 2012–13: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Bundesliga Player of the Year 2012–13: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award The kicker Man of the Year 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Globe Soccer Best Footballer of the Year 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award FIFA Club World Cup Golden Ball 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award GQ Men of the Year 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award UNFP Just Fontaine Trophy Ligue 1 Best Forward of the Season 2012–13: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Ligue 1 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Paris Saint-Germain 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Guldbollen 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award International Swede of the Year Award 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Swedish Male Athlete of the Year 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Swedish Goal of the Year 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Campeonato Paulista Best Player 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award FIFA Confederations Cup Bronze Shoe 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award FIFA Confederations Cup Dream Team 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award La Liga Best Midfielder 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Premier League Player of the Month 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award BBC Goal of the Season 2012–13: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Goal of the Month in Germany 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Welsh Footballer of the Year 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Serie A Footballer of the Year 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award Premio Nazionale Carriera Esemplare "Gaetano Scirea" 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award FIFA Confederations Cup Castrol Index Top XI 2013: no date found in linked article | 1 | 2013–2013 (1) |
| `awards_count` | undated award European Golden Shoe 2013–14: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFPRO World 11 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award ''kicker'' Goalkeeper of the Year 2013–14: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Best European Goalkeeper 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award AIPS 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award AIPS Europe Athlete of the Year – ''Frank Taylor Trophy'' 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Bundesliga Team of the Season 2013–14: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award VDV Bundesliga Team of the Season 2013–14: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award IFFHS World's Best International Goal Scorer 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' World Team 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Samba de Ouro 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Globe Revelation Player 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFA World Cup All-Star Team 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Bloomberg Sports 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award ESPN FC 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Silbernes Lorbeerblatt 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award German 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award UEFA Team of the Year 2014: no date found in linked article | 1 | 2014–2014 (1) |
| `awards_count` | undated award FIFPRO World 11 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award European Golden Shoe 2014–15: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award FPF Portuguese Player of the Year 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Samba de Ouro 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Top 100 Players in the World second place 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award IFFHS World's Best International Goal Scorer 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Polish Sports Personality of the Year 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Trofeo EFE 2014–15: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award ESM Team of the Year 2014–15: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award ''kicker'' Goalkeeper of the Year 2014–15: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Best European Goalkeeper 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Bundesliga Team of the Season 2014–15: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award VDV Bundesliga Team of the Season 2014–15: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Premier League Player of the Season 2014–15: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award Chelsea Players' Player of the Year 2014–15: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award ESM Team of the Season 2014–15: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2014–15: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award ''[[France Football]]'' World XI 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award PFA Fans' Premier League Player of the Month 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award BBC Goal of the Month 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award FSF Player of the Year 2015: no date found in linked article | 1 | 2015–2015 (1) |
| `awards_count` | undated award UEFA European Championship All-Time XI 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award FPF Portuguese Player of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award FIFPRO World 11 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award La Liga Best Player 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award La Liga Fan's Five-Star Player 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award UEFA European Championship Golden Boot 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award UEFA European Championship Team of the Tournament 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award French Player of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award IFFHS World's Best Top Division Goalscorer 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award European Golden Shoe 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award ESM Team of the Year 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award La Liga top assist provider 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2nd team 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award UEFA Champions League Player of the Week 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award ''WhoScored'' 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Welsh Footballer of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award CAF African Footballer of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award BBC African Footballer of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Algerian Footballer of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award PFA Team of the Year 2015–16 Premier League: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Leicester City Player of the Year 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award El Heddaf Arab Footballer of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Lion d'Or African Footballer of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Best European Goalkeeper 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Pallone Azzurro 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Premio Nazionale Carriera Esemplare "Gaetano Scirea" 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Golden Foot 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award VDV Team of the Season 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award ''DW'' 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Most clean sheets in Liga Portugal 2015-2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Étoile d'Or [[France Football]] 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Eurosport 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award PFA Fans' Premier League Player of the Month 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Manchester United 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Guldbollen 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Serie A top assist provider 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Chilean Footballer of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Football Oscar 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Premier League Player of the Month 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Best Belgian Player Abroad 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award CIES Football Observatory 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award UEFA La Liga Team of the Season 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award European Sports Media 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award VDV 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award ''[[Kicker (sports magazine)/kicker]]'' Bundesliga Team of the Season 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award ''kicker'' Goalkeeper of the Year 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Bundesliga Team of the Season 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award VDV Bundesliga Team of the Season 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award Luis Aragones 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award FPF Portuguese Player of the Year 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award European Golden Shoe 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award FIFPRO World 11 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' World Team 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Samba de Ouro 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award ''WhoScored'' 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Best European Goalkeeper 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Gazzetta Sports Awards 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Juventus Greatest XI of All Time 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Football Oscar 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award La Liga Best Defender 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Golden Boy 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Ligue 1 Young Player of the Year 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award UNFP 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Year 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award French Player of the Year 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Premier League Player of the Month 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award England Player of the Year Award 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award IFFHS World's Best Top Goal Scorer 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award UNFP [[Trophées UNFP du football#Player of the Year/Ligue 1 Player of the Year]] 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Ligue 1 top goalscorer 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Coupe de la Ligue top goalscorer 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Ligue 1 Best Foreign Player 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award UEFA Champions League Forward of the Season 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Season 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award ESPN 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Onze de Bronze 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Chelsea Goal of the Year 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Belgium Player of the Year 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Best Belgian Abroad 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award ''[[Der Spiegel]]'' Best Player in the Bundesliga (winter period) 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Liverpool Players' Player of the Season Award 2016–17: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award UNFP 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award Slovenian Footballer of the Year 2017: no date found in linked article | 1 | 2017–2017 (1) |
| `awards_count` | undated award UEFA Men's Player of the Year Award 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Football Oscar 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Franjo Bučar State Award for Sport 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award HNS 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award HOO 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award SN Sportsman of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award FPF Portuguese Player of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award FIFA World Cup Silver Boot 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Ligue 1 Young Player of the Year 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award French Player of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award UNFP 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award European Golden Shoe 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award FIFPRO World 11 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award El Heddaf Arab Footballer of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award BBC African Footballer of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award African Footballer of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award UEFA Champions League Forward of the Season 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Onze d'Argent 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award FSA Player of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award BBC Goal of the Month 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Belgium Player of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Best Belgian Abroad 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award FIFA World Cup Fantasy Team 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Belgian Sportsman of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award England Player of the Year Award 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award London Football Awards Premier League Player of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2nd team 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award ''WhoScored'' 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Ligue 1 top assist provider 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award UNFP [[Ligue 1 Player of the Year]] 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award La Liga Player of the Month 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award UEFA Champions League Goal of the Season 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Samba Gold 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award FIFA FIFPro World11 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Ligue 1 top goalscorer 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Trofeo EFE 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Golden Foot 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award PFA 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award ''[[L'Équipe]]'' Team of the Season 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award ESPN 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Globe Soccer Awards Best Goalkeeper of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award UEFA 2017–18: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award Slovenian Footballer of the Year 2018: no date found in linked article | 1 | 2018–2018 (1) |
| `awards_count` | undated award European Golden Shoe 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award FIFPRO World 11 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Premier League Player of the Year by Northwest Football Awards 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award UEFA Men's Player of the Year Award 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Liverpool Players' Player of the Season Award 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Portuguese Sportsman of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award FPF Portuguese Player of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award PFA 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award African Footballer of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Onze d'Or 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award ''Time'' 100 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Ligue 1 Player of the Year 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Ligue 1 top goalscorer 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Ligue 1 Young Player of the Year 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award French Player of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Onze de Bronze 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award UNFP Ligue 1 Player of the Month 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Globe Soccer Awards Best Goalkeeper of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Samba Gold 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Polish Football Association 1919–2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Alan Hardaker Trophy 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award African Goal of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Eredivisie Player of the Month 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Johan Cruyff Trophy 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Chelsea Players' Player of the Year 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award ESM Team of the Season 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Chelsea Goal of the Year 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Belgium Player of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Best Belgian Abroad 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Premier League Playmaker of the Season 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Dutch Footballer of the Year 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award ''Goal'' 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Serbian Footballer of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award AFC Asian International Player of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Korean FA Player of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Gallup Korea's Athlete of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award London Football Award for Premier League Player of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Premi Barça Jugadors 2018–19: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award SJPF Young Player of the Month 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award CNID Best Revelation Footballer of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Golden Globes 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award ''[[A Bola]]'' Player of the Year 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Golden Boy 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award Globe Revelation Player 2019: no date found in linked article | 1 | 2019–2019 (1) |
| `awards_count` | undated award FIFPRO World 11 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Argentine Sportsperson of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award European Golden Shoe 2020–21: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best Man Player 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best Top Goal Scorer 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best International Goal Scorer 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best Top Division Goal Scorer 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award ''World Soccer'' Player of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award ''FourFourTwo'' Player of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award ''Tuttosport'' Golden Player 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award ''The Guardian'' Best Footballer in the World 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Globe Soccer Fans' Player of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Globe Soccer Maradona Award 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Polish Sports Personality of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Bundesliga 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award German Sports Journalists' Footballer of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World Team 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award FIFA FIFPro World11 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Onze d'Or 2020–21: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award French Player of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award AS 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award L'Équipe 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award FSA Player of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS CAF Men's Team of The Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Laureus Sporting Inspiration Award 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Golden Foot 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS Best CAF Men's Player of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Ligue 1 Player of the Year 2020–21: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Ligue 1 top goalscorer 2020–21: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Globe Soccer Best Player of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Globe Soccer Awards Best Goalkeeper of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Serie A Goalkeeper of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Bundesliga Player of the Month 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Bundesliga Goal of the Month 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Gullballen 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Serie A Footballer of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Best Belgian Abroad 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Globe Soccer Awards Best Defender of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Samba de Ouro 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award FIFA FIFPRO World 11 2nd team 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award UEFA Champions League Player of the Week 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award CIES Football Observatory 2020–21: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Copa América Golden Ball 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS Best Playmaker of the Copa América 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Danish Player of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award The Guardian Footballer of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award PFA 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Alan Hardaker Trophy 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award IFFHS CAF World's Best Playmaker 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Premier League Goal of the Month 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Manchester United Goal of the Season 2020–21: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award London Football Awards Premier League Player of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Golden Boy 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Trofeo Aldo Rovira 2020–21: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award UEFA Europa League Player of the Season 2020–21: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award UEFA Europa League top assists provider 2020–21: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Gazzetta Sports Awards 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award Football Oscar 2021: no date found in linked article | 1 | 2021–2021 (1) |
| `awards_count` | undated award UEFA Men's Player of the Year 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Golden Player Man Award 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Onze d'Or 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Globe Soccer Best Player of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award La Liga Player of the Month 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Kicker 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award L'Équipe 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Sócrates Award 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award African Footballer of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS Best CAF Men's Player of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Best Belgian Player Abroad 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Premier League Player of the Year by Northwest Football Awards 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award FSA Player of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award European Golden Shoe 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Laureus 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Golden Foot 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award ESM Team of the Year 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award ESPN 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Lech Poznań 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award PFA Player of the Month 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS CAF Men's Team of The Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award BBC Goal of the Season 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Globe Soccer Fans' Player of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Ligue 1 Player of the Year 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Ligue 1 top goalscorer 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS World's Best Top Goal Scorer 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Ligue 1 top assist provider 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award ''WhoScored'' 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award UNFP 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Football Oscar 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award SN Sportsman of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Gullballen 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award ''FourFourTwo'' Player of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award IFFHS Asian Men's Player of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Eurosport 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Korean FA Player of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Gallup Korea's Athlete of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Cheongnyong Medal 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Alan Hardaker Trophy 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Futbolista Colombiano del Año 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Manchester City Goal of the Season 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award UEFA Champions League Fantasy Football Team of the Season 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award VDV Bundesliga Team of the Season 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award LPFP Primeira Liga Player of the Year 2021–22: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award SJPF Player of the Month 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award CNID Footballer of the Year 2022: no date found in linked article | 1 | 2022–2022 (1) |
| `awards_count` | undated award Laureus World Sportsman of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award ''TIME'' Athlete of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award FIFPRO World 11 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Argentine Sportsperson of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Argentine Footballer of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award European Golden Shoe 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award UEFA Men's Player of the Year 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Premier League Player of the Month 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Golden Player Man Award 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Gullballen 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award ''The Guardian'' Best Footballer in the World 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award ''World Soccer'' Player of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award ''FourFourTwo'' Player of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS World's Best Player 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Onze d'Or 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Idrettsgallaen 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Ligue 1 Player of the Year 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Ligue 1 top goalscorer 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award French Player of the Year 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award UNFP 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Best Belgian Player Abroad 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Samba Gold 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Ghana Football Awards 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award African Footballer of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award FIFA FIFPro World XI 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Croatian Footballer of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Football Oscar 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award FSA Player of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS CAF Men's Team of The Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Znicz Pruszków 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award "Lion d'Or" African Footballer of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award "Africa d'Or" African Footballer of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award African Goalkeeper of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award UMFP Best Moroccan goalkeeper abroad 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Footballer of the Year in Germany 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Marca Leyenda Award 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Georgian Footballer of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Serie A Goal of the Month 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Golden Boy 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award La Liga Player of the Month 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS World's Best Top Division Goal Scorer 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Gazzetta Sports Awards 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award Korean FA Player of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award England Men's Player of the Year 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award PFA Young Player of the Year 2022–23: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award London Football Awards Men's Young Player of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award London Football Awards Premier League Player of the Year 2023: no date found in linked article | 1 | 2023–2023 (1) |
| `awards_count` | undated award IFFHS World's Best Player 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''World Soccer'' Player of the Year 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''FourFourTwo'' Player of the Year 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''The Guardian'' Best Footballer in the World 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award CIES Football Observatory 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''[[The Athletic]]'' Premier League Player of the Season 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' European Men's Team of the Season 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Samba Gold 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Globe Soccer Best Forward 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Laureus World Breakthrough of the Year 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Ligue 1 Player of the Year 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Ligue 1 top goalscorer 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award French Player of the Year 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''[[The Athletic]]'' European Men's Team of the Season 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' Ligue 1 Player of the Season 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Golden Foot 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Golden Boy 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award German Footballer of the Year 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Golden Player Man Award 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award European Golden Shoe 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Bundesliga Player of the Month 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award VDV Team of the Season 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award African Footballer of the Year 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''[[The Athletic]]'' Premier League Team of the Season 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Olimpia de Oro 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Footballer of the Year of Argentina 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''[[Opta Sports#Association football/WhoScored]]'' Top Rated Player in Europe (performance data by [[Opta Sports/Opta]]) 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award England's Men's Player of the Year 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award London Football Awards Men's Young Player of the Year 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Chelsea Player's Player of the Season 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award PFA Young Player of the Year 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' Premier League Insiders Signing of the Season 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award ''The Athletic'' Premier League Young Player of the Season 2023–24: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award London Football 2024: no date found in linked article | 1 | 2024–2024 (1) |
| `awards_count` | undated award Ligue 1 Team of the Year 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best Player 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Globe Soccer Awards Forward of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''[[Opta Sports#Association football/WhoScored]]'' European Player of the Season (performance data by [[Opta Sports/Opta]]) 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Laureus World Sports Award for Breakthrough of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Maradona Award 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best Playmaker 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Globe Soccer Awards Midfielder of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Premier League Player of the Month 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award PFA Player of the Month 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World Men's Player of the Month 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award FPL Pod Player of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''[[The Athletic]]''<nowiki/>'s Premier League Player of the Year 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award EA Sports 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''The Athletic'' European Men's Player of the Season 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''The Athletic'' La Liga  Team of the Season 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award African Footballer of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Lion d'Or African Footballer of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Ghana Football Awards 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award UMFP Best Moroccan player abroad 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Prix Marc-Vivien Foé 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award European Golden Shoe 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best Top Goal Scorer 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best Top Division Goal Scorer 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award La Liga Player of the Month 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award London Football Awards Premier League Player of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award London Football Awards Goal of the season 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award EA Sports FC 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award FIFPRO Men's World 11 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best Goalkeeper 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award The Athletic 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Premi Barça Jugadors 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''The Athletic'' La Liga Player of the Season 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''The Athletic'' La Liga Team of the Season 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Georgian Footballer of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Golden Boy 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Globe Soccer Awards Emerging Player of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Swedish Forward of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ESM Team of the Year 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Polish Footballer of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Serie A Most Valuable Player 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award ''[[The Athletic]]'' Serie A Team of the Season 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Serie A Team of the Year 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Serie A Footballer of the Year 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award BBC Goal of the Month 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award England Men's Player of the Year 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Norwegian Sportsperson of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award IFFHS World's Best International Goal Scorer 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award German Footballer of the Year 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award Bundesliga Goal of the Month 2025: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award VDV Team of the Season 2024–25: no date found in linked article | 1 | 2025–2025 (1) |
| `awards_count` | undated award European Golden Shoe 2025–26: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award Bundesliga Player of the Month 2026: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award Laureus World Sports Award for Young Sportsperson of the Year 2026: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award IFFHS 2026: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award Ligue 1 Team of the Year 2025–26: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award Ligue 1 Goal of the Year 2025–26: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award UNFP Best French Player Playing Abroad 2025–26: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award Golden Boy 2026: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award ''The Athletic'' European Men's Team of the Season 2025–26: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award The Athletic 2025-2026: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award Serie A Player of the Month 2026: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award UEFA 2026: no date found in linked article | 1 | 2026–2026 (1) |
| `awards_count` | undated award PFA Players' Player of the Year 2025–26: no date found in linked article | 1 | 2026–2026 (1) |
| `intl_stage` | Copa América 2016: no round data | 7 | 2016–2016 (1) |
| `intl_stage` | UEFA Euro 2000: no round data | 6 | 2000–2000 (1) |
| `intl_stage` | African Cup of Nations 2019: no round data | 3 | 2019–2019 (1) |
| `intl_stage` | African Cup of Nations 2006: no round data | 2 | 2006–2006 (1) |
| `intl_stage` | Copa América 2015: no round data | 2 | 2015–2015 (1) |
| `intl_stage` | African Cup of Nations 2017: no round data | 2 | 2017–2017 (1) |
| `intl_stage` | Copa América 2019: no round data | 2 | 2019–2019 (1) |
| `intl_stage` | Copa América 2007: no round data | 1 | 2007–2007 (1) |
| `intl_stage` | African Cup of Nations 2010: no round data | 1 | 2010–2010 (1) |
| `intl_stage` | African Cup of Nations 2012: no round data | 1 | 2012–2012 (1) |
| `intl_stage` | African Cup of Nations 2026: no round data | 1 | 2026–2026 (1) |
| `intl_tournament_*` | StatsBomb has no FIFA World Cup 2026 | 29 | 2026–2026 (1) |
| `intl_tournament_*` | StatsBomb has no UEFA Euro 2016 | 20 | 2016–2016 (1) |
| `intl_tournament_*` | StatsBomb has no FIFA World Cup 2002 | 10 | 2002–2002 (1) |
| `intl_tournament_*` | StatsBomb has no FIFA World Cup 2010 | 10 | 2010–2010 (1) |
| `intl_tournament_*` | StatsBomb has no FIFA World Cup 2014 | 10 | 2014–2014 (1) |
| `intl_tournament_*` | StatsBomb has no FIFA World Cup 2006 | 9 | 2006–2006 (1) |
| `intl_tournament_*` | StatsBomb has no UEFA Euro 2000 | 8 | 2000–2000 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2016 | 8 | 2016–2016 (1) |
| `intl_tournament_*` | StatsBomb has no UEFA Euro 2004 | 7 | 2004–2004 (1) |
| `intl_tournament_*` | StatsBomb has no UEFA Euro 2008 | 7 | 2008–2008 (1) |
| `intl_tournament_*` | StatsBomb has no UEFA Euro 2012 | 7 | 2012–2012 (1) |
| `intl_tournament_*` | player name not found in StatsBomb tournament lineups | 6 | 2018–2024 (3) |
| `intl_tournament_*` | StatsBomb has no Copa América 2019 | 5 | 2019–2019 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2011 | 4 | 2011–2011 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2015 | 4 | 2015–2015 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2019 | 4 | 2019–2019 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2021 | 4 | 2021–2021 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2022 | 4 | 2022–2022 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2007 | 3 | 2007–2007 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2004 | 2 | 2004–2004 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2017 | 2 | 2017–2017 (1) |
| `intl_tournament_*` | StatsBomb has no Copa América 2001 | 1 | 2001–2001 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2006 | 1 | 2006–2006 (1) |
| `intl_tournament_*` | StatsBomb has no African Cup of Nations 2012 | 1 | 2012–2012 (1) |
| `league_*` | StatsBomb has no Premier League 2018/2019 | 15 | 2019–2019 (1) |
| `league_*` | StatsBomb La Liga 2016/2017 does not hold every Real Madrid match | 13 | 2016–2017 (2) |
| `league_*` | StatsBomb has no Premier League 2016/2017 | 13 | 2016–2017 (2) |
| `league_*` | StatsBomb has no Premier League 2020/2021 | 12 | 2021–2021 (1) |
| `league_*` | StatsBomb has no Premier League 2021/2022 | 11 | 2022–2022 (1) |
| `league_*` | StatsBomb has no Premier League 2017/2018 | 10 | 2018–2018 (1) |
| `league_*` | 2 club spells in the infobox overlap 2021-2022 | 10 | 2022–2022 (1) |
| `league_*` | 2 club spells in the infobox overlap 2023-2024 | 10 | 2024–2024 (1) |
| `league_*` | 2 club spells in the infobox overlap 2024-2025 | 10 | 2025–2025 (1) |
| `league_*` | 2 club spells in the infobox overlap 2022-2023 | 9 | 2023–2023 (1) |
| `league_*` | club not in StatsBomb league data | 8 | 2008–2026 (6) |
| `league_*` | StatsBomb has no Premier League 2022/2023 | 8 | 2023–2023 (1) |
| `league_*` | StatsBomb has no Premier League 2023/2024 | 8 | 2024–2024 (1) |
| `league_*` | StatsBomb has no Ligue 1 2025/2026 | 8 | 2026–2026 (1) |
| `league_*` | StatsBomb La Liga 2017/2018 does not hold every Real Madrid match | 7 | 2018–2018 (1) |
| `league_*` | StatsBomb La Liga 2016/2017 does not hold every Barcelona match | 6 | 2016–2017 (2) |
| `league_*` | StatsBomb has no Serie A 2016/2017 | 6 | 2016–2017 (2) |
| `league_*` | 3 club spells in the infobox overlap 2022-2023 | 6 | 2023–2023 (1) |
| `league_*` | StatsBomb has no La Liga 2024/2025 | 6 | 2025–2025 (1) |
| `league_*` | StatsBomb has no Premier League 2024/2025 | 6 | 2025–2025 (1) |
| `league_*` | 2 club spells in the infobox overlap 2004-2004 | 5 | 2004–2004 (1) |
| `league_*` | StatsBomb has no Premier League 2004/2005 | 5 | 2004–2005 (2) |
| `league_*` | StatsBomb has no Serie A 2004/2005 | 5 | 2005–2005 (1) |
| `league_*` | StatsBomb La Liga 2016/2017 does not hold every Atlético Madrid match | 5 | 2016–2017 (2) |
| `league_*` | 2 club spells in the infobox overlap 2019-2019 | 5 | 2019–2019 (1) |
| `league_*` | StatsBomb has no Serie A 2020/2021 | 5 | 2021–2021 (1) |
| `league_*` | StatsBomb has no La Liga 2023/2024 | 5 | 2024–2024 (1) |
| `league_*` | StatsBomb has no Ligue 1 2024/2025 | 5 | 2025–2025 (1) |
| `league_*` | StatsBomb has no La Liga 2025/2026 | 5 | 2026–2026 (1) |
| `league_*` | 2 club spells in the infobox overlap 2025-2026 | 5 | 2026–2026 (1) |
| `league_*` | StatsBomb has no Premier League 2025/2026 | 5 | 2026–2026 (1) |
| `league_*` | StatsBomb has no Serie A 1999/2000 | 4 | 2000–2000 (1) |
| `league_*` | StatsBomb has no Serie A 2002/2003 | 4 | 2003–2003 (1) |
| `league_*` | StatsBomb has no Serie A 2006/2007 | 4 | 2007–2007 (1) |
| `league_*` | 2 club spells in the infobox overlap 2009-2009 | 4 | 2009–2009 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2013/2014 | 4 | 2014–2014 (1) |
| `league_*` | StatsBomb 1. Bundesliga 2015/2016 does not hold every Bayern Munich match | 4 | 2016–2016 (1) |
| `league_*` | 2 club spells in the infobox overlap 2021-2021 | 4 | 2021–2021 (1) |
| `league_*` | StatsBomb has no La Liga 2021/2022 | 4 | 2022–2022 (1) |
| `league_*` | StatsBomb has no La Liga 1999/2000 | 3 | 2000–2000 (1) |
| `league_*` | StatsBomb has no Premier League 2000/2001 | 3 | 2001–2001 (1) |
| `league_*` | StatsBomb has no La Liga 2000/2001 | 3 | 2001–2001 (1) |
| `league_*` | 2 club spells in the infobox overlap 2002-2002 | 3 | 2002–2002 (1) |
| `league_*` | StatsBomb has no La Liga 2001/2002 | 3 | 2002–2002 (1) |
| `league_*` | StatsBomb has no La Liga 2002/2003 | 3 | 2003–2003 (1) |
| `league_*` | StatsBomb has no Premier League 2005/2006 | 3 | 2006–2006 (1) |
| `league_*` | StatsBomb has no Premier League 2006/2007 | 3 | 2007–2007 (1) |
| `league_*` | StatsBomb has no Premier League 2007/2008 | 3 | 2008–2008 (1) |
| `league_*` | StatsBomb La Liga 2008/2009 does not hold every Barcelona match | 3 | 2009–2009 (1) |
| `league_*` | StatsBomb has no Premier League 2008/2009 | 3 | 2009–2009 (1) |
| `league_*` | StatsBomb La Liga 2009/2010 does not hold every Barcelona match | 3 | 2010–2010 (1) |
| `league_*` | StatsBomb La Liga 2009/2010 does not hold every Real Madrid match | 3 | 2010–2010 (1) |
| `league_*` | StatsBomb La Liga 2010/2011 does not hold every Barcelona match | 3 | 2011–2011 (1) |
| `league_*` | 2 club spells in the infobox overlap 2011-2011 | 3 | 2011–2011 (1) |
| `league_*` | StatsBomb La Liga 2011/2012 does not hold every Barcelona match | 3 | 2012–2012 (1) |
| `league_*` | 2 club spells in the infobox overlap 2012-2012 | 3 | 2012–2012 (1) |
| `league_*` | 2 club spells in the infobox overlap 2014-2014 | 3 | 2014–2014 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2014/2015 | 3 | 2015–2015 (1) |
| `league_*` | 2 club spells in the infobox overlap 2016-2016 | 3 | 2016–2016 (1) |
| `league_*` | 2 club spells in the infobox overlap 2017-2017 | 3 | 2017–2017 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2016/2017 | 3 | 2017–2017 (1) |
| `league_*` | 2 club spells in the infobox overlap 2018-2018 | 3 | 2018–2018 (1) |
| `league_*` | StatsBomb La Liga 2017/2018 does not hold every Atlético Madrid match | 3 | 2018–2018 (1) |
| `league_*` | StatsBomb La Liga 2017/2018 does not hold every Barcelona match | 3 | 2018–2018 (1) |
| `league_*` | StatsBomb has no Serie A 2022/2023 | 3 | 2023–2023 (1) |
| `league_*` | StatsBomb has no Serie A 2023/2024 | 3 | 2024–2024 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2025/2026 | 3 | 2026–2026 (1) |
| `league_*` | 2 club spells in the infobox overlap 2000-2000 | 2 | 2000–2000 (1) |
| `league_*` | StatsBomb has no Premier League 1999/2000 | 2 | 2000–2000 (1) |
| `league_*` | StatsBomb has no Serie A 2000/2001 | 2 | 2001–2001 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2001/2002 | 2 | 2002–2002 (1) |
| `league_*` | StatsBomb has no Premier League 2002/2003 | 2 | 2003–2003 (1) |
| `league_*` | StatsBomb has no Serie A 2003/2004 | 2 | 2004–2004 (1) |
| `league_*` | StatsBomb La Liga 2004/2005 does not hold every Barcelona match | 2 | 2005–2005 (1) |
| `league_*` | StatsBomb has no Serie A 2005/2006 | 2 | 2006–2006 (1) |
| `league_*` | StatsBomb La Liga 2005/2006 does not hold every Barcelona match | 2 | 2006–2006 (1) |
| `league_*` | StatsBomb La Liga 2006/2007 does not hold every Real Madrid match | 2 | 2007–2007 (1) |
| `league_*` | StatsBomb La Liga 2007/2008 does not hold every Barcelona match | 2 | 2008–2008 (1) |
| `league_*` | StatsBomb has no Serie A 2007/2008 | 2 | 2008–2008 (1) |
| `league_*` | StatsBomb La Liga 2010/2011 does not hold every Real Madrid match | 2 | 2011–2011 (1) |
| `league_*` | StatsBomb La Liga 2011/2012 does not hold every Real Madrid match | 2 | 2012–2012 (1) |
| `league_*` | StatsBomb La Liga 2012/2013 does not hold every Barcelona match | 2 | 2013–2013 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2012/2013 | 2 | 2013–2013 (1) |
| `league_*` | 2 club spells in the infobox overlap 2013-2013 | 2 | 2013–2013 (1) |
| `league_*` | StatsBomb La Liga 2013/2014 does not hold every Barcelona match | 2 | 2014–2014 (1) |
| `league_*` | StatsBomb has no Premier League 2014/2015 | 2 | 2015–2015 (1) |
| `league_*` | StatsBomb has no Ligue 1 2016/2017 | 2 | 2017–2017 (1) |
| `league_*` | StatsBomb has no Ligue 1 2017/2018 | 2 | 2018–2018 (1) |
| `league_*` | StatsBomb La Liga 2018/2019 does not hold every Barcelona match | 2 | 2019–2019 (1) |
| `league_*` | StatsBomb has no Serie A 2018/2019 | 2 | 2019–2019 (1) |
| `league_*` | StatsBomb has no Ligue 1 2018/2019 | 2 | 2019–2019 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2020/2021 | 2 | 2021–2021 (1) |
| `league_*` | StatsBomb La Liga 2020/2021 does not hold every Real Madrid match | 2 | 2021–2021 (1) |
| `league_*` | StatsBomb has no Ligue 1 2020/2021 | 2 | 2021–2021 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2021/2022 | 2 | 2022–2022 (1) |
| `league_*` | StatsBomb has no La Liga 2022/2023 | 2 | 2023–2023 (1) |
| `league_*` | StatsBomb has no Serie A 2024/2025 | 2 | 2025–2025 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2000/2001 | 1 | 2001–2001 (1) |
| `league_*` | 2 club spells in the infobox overlap 2001-2001 | 1 | 2001–2001 (1) |
| `league_*` | StatsBomb has no Premier League 2001/2002 | 1 | 2002–2002 (1) |
| `league_*` | StatsBomb has no Serie A 2001/2002 | 1 | 2002–2002 (1) |
| `league_*` | 2 club spells in the infobox overlap 2003-2003 | 1 | 2003–2003 (1) |
| `league_*` | StatsBomb has no La Liga 2003/2004 | 1 | 2004–2004 (1) |
| `league_*` | StatsBomb Premier League 2003/2004 does not hold every Manchester United match | 1 | 2004–2004 (1) |
| `league_*` | 2 club spells in the infobox overlap 2006-2006 | 1 | 2006–2006 (1) |
| `league_*` | StatsBomb La Liga 2005/2006 does not hold every Real Madrid match | 1 | 2006–2006 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2005/2006 | 1 | 2006–2006 (1) |
| `league_*` | StatsBomb La Liga 2006/2007 does not hold every Barcelona match | 1 | 2007–2007 (1) |
| `league_*` | StatsBomb La Liga 2007/2008 does not hold every Real Madrid match | 1 | 2008–2008 (1) |
| `league_*` | StatsBomb La Liga 2007/2008 does not hold every Valencia match | 1 | 2008–2008 (1) |
| `league_*` | StatsBomb has no Serie A 2009/2010 | 1 | 2010–2010 (1) |
| `league_*` | StatsBomb La Liga 2009/2010 does not hold every Atlético Madrid match | 1 | 2010–2010 (1) |
| `league_*` | 2 club spells in the infobox overlap 2010-2010 | 1 | 2010–2010 (1) |
| `league_*` | StatsBomb has no Premier League 2009/2010 | 1 | 2010–2010 (1) |
| `league_*` | StatsBomb has no Premier League 2010/2011 | 1 | 2011–2011 (1) |
| `league_*` | StatsBomb La Liga 2011/2012 does not hold every Atlético Madrid match | 1 | 2012–2012 (1) |
| `league_*` | StatsBomb has no Serie A 2011/2012 | 1 | 2012–2012 (1) |
| `league_*` | StatsBomb La Liga 2012/2013 does not hold every Real Madrid match | 1 | 2013–2013 (1) |
| `league_*` | StatsBomb has no Ligue 1 2012/2013 | 1 | 2013–2013 (1) |
| `league_*` | StatsBomb has no Premier League 2012/2013 | 1 | 2013–2013 (1) |
| `league_*` | StatsBomb has no Serie A 2012/2013 | 1 | 2013–2013 (1) |
| `league_*` | StatsBomb La Liga 2013/2014 does not hold every Real Madrid match | 1 | 2014–2014 (1) |
| `league_*` | StatsBomb La Liga 2014/2015 does not hold every Real Madrid match | 1 | 2015–2015 (1) |
| `league_*` | StatsBomb 1. Bundesliga 2015/2016 does not hold every Borussia Dortmund match | 1 | 2016–2016 (1) |
| `league_*` | 3 club spells in the infobox overlap 2018-2018 | 1 | 2018–2018 (1) |
| `league_*` | StatsBomb has no Serie A 2017/2018 | 1 | 2018–2018 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2018/2019 | 1 | 2019–2019 (1) |
| `league_*` | StatsBomb La Liga 2018/2019 does not hold every Real Madrid match | 1 | 2019–2019 (1) |
| `league_*` | StatsBomb La Liga 2020/2021 does not hold every Atlético Madrid match | 1 | 2021–2021 (1) |
| `league_*` | StatsBomb La Liga 2020/2021 does not hold every Barcelona match | 1 | 2021–2021 (1) |
| `league_*` | StatsBomb La Liga 2020/2021 does not hold every Villarreal match | 1 | 2021–2021 (1) |
| `league_*` | StatsBomb Ligue 1 2021/2022 does not hold every Paris Saint-Germain match | 1 | 2022–2022 (1) |
| `league_*` | 3 club spells in the infobox overlap 2021-2022 | 1 | 2022–2022 (1) |
| `league_*` | StatsBomb has no Serie A 2021/2022 | 1 | 2022–2022 (1) |
| `league_*` | StatsBomb Ligue 1 2022/2023 does not hold every Paris Saint-Germain match | 1 | 2023–2023 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2022/2023 | 1 | 2023–2023 (1) |
| `league_*` | StatsBomb has no Ligue 1 2023/2024 | 1 | 2024–2024 (1) |
| `league_*` | 3 club spells in the infobox overlap 2023-2024 | 1 | 2024–2024 (1) |
| `league_*` | StatsBomb has no 1. Bundesliga 2024/2025 | 1 | 2025–2025 (1) |
| `league_*` | StatsBomb has no Major League Soccer 2025 | 1 | 2026–2026 (1) |
| `league_*` | StatsBomb has no Serie A 2025/2026 | 1 | 2026–2026 (1) |
| `match_rating_avg` | no permitted source publishes per-match ratings (FBref/Transfermarkt blocked) | 462 | 2000–2026 (26) |
| `national_apps/minutes/assists/cards` | martj42 has goals only; no permitted source lists national-team line-ups, minutes or assists for every match | 462 | 2000–2026 (26) |
| `national_goals` | player name never appears among this country's goalscorers | 45 | 2000–2026 (21) |
| `national_goals` | goalscorers incomplete for 2018-03-23 France v Colombia | 6 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2023-09-12 Scotland v England | 6 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2024-03-26 Spain v Brazil | 5 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2026-03-27 Spain v Serbia | 5 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2010-03-03 France v Spain | 4 | 2010–2010 (1) |
| `national_goals` | goalscorers incomplete for 2017-06-02 France v Paraguay | 4 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2021-05-28 Italy v San Marino | 4 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2021-06-02 England v Austria | 4 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2022-03-25 France v Ivory Coast | 4 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2021-09-04 Qatar v Portugal | 4 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2023-09-09 Germany v Japan | 4 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2025-06-10 England v Senegal | 4 | 2025–2025 (1) |
| `national_goals` | goalscorers incomplete for 2026-03-26 Brazil v France | 4 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2002-01-31 Brazil v Bolivia | 3 | 2002–2002 (1) |
| `national_goals` | goalscorers incomplete for 2004-02-18 Portugal v England | 3 | 2004–2004 (1) |
| `national_goals` | goalscorers incomplete for 2005-02-09 Hong Kong v Brazil | 3 | 2005–2005 (1) |
| `national_goals` | goalscorers incomplete for 2005-05-28 United States v England | 3 | 2005–2005 (1) |
| `national_goals` | goalscorers incomplete for 2008-02-06 Spain v France | 3 | 2008–2008 (1) |
| `national_goals` | goalscorers incomplete for 2013-02-06 Netherlands v Italy | 3 | 2013–2013 (1) |
| `national_goals` | goalscorers incomplete for 2014-03-05 Germany v Chile | 3 | 2014–2014 (1) |
| `national_goals` | goalscorers incomplete for 2016-03-29 Portugal v Belgium | 3 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2016-03-25 Netherlands v France | 3 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2016-03-26 Germany v England | 3 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2017-01-26 Brazil v Colombia | 3 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-03-28 Russia v Belgium | 3 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2018-03-27 Mexico v Croatia | 3 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2018-03-23 Russia v Brazil | 3 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2018-03-23 Uruguay v Czech Republic | 3 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2019-06-02 France v Bolivia | 3 | 2019–2019 (1) |
| `national_goals` | goalscorers incomplete for 2021-06-02 France v Wales | 3 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2021-06-09 Portugal v Israel | 3 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2021-06-08 Spain v Lithuania | 3 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2022-03-26 England v Switzerland | 3 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-09-23 Argentina v Honduras | 3 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2025-10-09 England v Wales | 3 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2025-10-10 South Korea v Brazil | 3 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2026-03-31 United States v Portugal | 3 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2000-02-23 France v Poland | 2 | 2000–2000 (1) |
| `national_goals` | goalscorers incomplete for 2000-01-26 Spain v Poland | 2 | 2000–2000 (1) |
| `national_goals` | goalscorers incomplete for 2001-02-28 England v Spain | 2 | 2001–2001 (1) |
| `national_goals` | goalscorers incomplete for 2001-02-27 France v Germany | 2 | 2001–2001 (1) |
| `national_goals` | goalscorers incomplete for 2002-02-13 France v Romania | 2 | 2002–2002 (1) |
| `national_goals` | goalscorers incomplete for 2003-04-30 France v Egypt | 2 | 2003–2003 (1) |
| `national_goals` | goalscorers incomplete for 2004-04-28 Hungary v Brazil | 2 | 2004–2004 (1) |
| `national_goals` | goalscorers incomplete for 2006-03-01 France v Slovakia | 2 | 2006–2006 (1) |
| `national_goals` | goalscorers incomplete for 2006-03-01 Italy v Germany | 2 | 2006–2006 (1) |
| `national_goals` | goalscorers incomplete for 2007-03-24 Brazil v Chile | 2 | 2007–2007 (1) |
| `national_goals` | goalscorers incomplete for 2007-08-22 Hungary v Italy | 2 | 2007–2007 (1) |
| `national_goals` | goalscorers incomplete for 2009-02-11 Spain v England | 2 | 2009–2009 (1) |
| `national_goals` | goalscorers incomplete for 2009-03-28 England v Slovakia | 2 | 2009–2009 (1) |
| `national_goals` | goalscorers incomplete for 2011-02-09 Argentina v Portugal | 2 | 2011–2011 (1) |
| `national_goals` | goalscorers incomplete for 2011-02-09 Spain v Colombia | 2 | 2011–2011 (1) |
| `national_goals` | goalscorers incomplete for 2011-03-29 Republic of Ireland v Uruguay | 2 | 2011–2011 (1) |
| `national_goals` | goalscorers incomplete for 2012-02-29 Spain v Venezuela | 2 | 2012–2012 (1) |
| `national_goals` | goalscorers incomplete for 2014-06-04 Argentina v Trinidad and Tobago | 2 | 2014–2014 (1) |
| `national_goals` | goalscorers incomplete for 2016-05-27 Uruguay v Trinidad and Tobago | 2 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2016-03-24 Italy v Spain | 2 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2017-06-09 Argentina v Brazil | 2 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-03-28 France v Spain | 2 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-06-04 Republic of Ireland v Uruguay | 2 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-03-22 Germany v England | 2 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2018-03-23 Portugal v Egypt | 2 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2018-03-23 Italy v Argentina | 2 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2018-03-27 Belgium v Saudi Arabia | 2 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2018-03-23 Germany v Spain | 2 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2019-03-22 Argentina v Venezuela | 2 | 2019–2019 (1) |
| `national_goals` | goalscorers incomplete for 2019-03-23 Senegal v Madagascar | 2 | 2019–2019 (1) |
| `national_goals` | goalscorers incomplete for 2019-03-23 Brazil v Panama | 2 | 2019–2019 (1) |
| `national_goals` | goalscorers incomplete for 2021-06-03 Belgium v Greece | 2 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2022-06-02 South Korea v Brazil | 2 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-03-26 Germany v Israel | 2 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-11-17 Republic of Ireland v Norway | 2 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2022-11-17 Portugal v Nigeria | 2 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2022-11-16 Saudi Arabia v Croatia | 2 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2022-11-16 Oman v Germany | 2 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2023-09-07 Norway v Jordan | 2 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2025-10-10 Argentina v Venezuela | 2 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2000-02-23 Belgium v Portugal | 1 | 2000–2000 (1) |
| `national_goals` | goalscorers incomplete for 2000-04-26 Bulgaria v Ukraine | 1 | 2000–2000 (1) |
| `national_goals` | goalscorers incomplete for 2000-02-23 Thailand v Brazil | 1 | 2000–2000 (1) |
| `national_goals` | goalscorers incomplete for 2000-02-23 Italy v Sweden | 1 | 2000–2000 (1) |
| `national_goals` | goalscorers incomplete for 2000-05-27 England v Brazil | 1 | 2000–2000 (1) |
| `national_goals` | goalscorers incomplete for 2001-03-28 Spain v France | 1 | 2001–2001 (1) |
| `national_goals` | goalscorers incomplete for 2001-02-28 Italy v Argentina | 1 | 2001–2001 (1) |
| `national_goals` | goalscorers incomplete for 2001-08-15 Portugal v Moldova | 1 | 2001–2001 (1) |
| `national_goals` | goalscorers incomplete for 2001-03-03 United States v Brazil | 1 | 2001–2001 (1) |
| `national_goals` | goalscorers incomplete for 2001-02-28 Cyprus v Ukraine | 1 | 2001–2001 (1) |
| `national_goals` | goalscorers incomplete for 2002-02-13 Germany v Israel | 1 | 2002–2002 (1) |
| `national_goals` | goalscorers incomplete for 2002-02-13 Spain v Portugal | 1 | 2002–2002 (1) |
| `national_goals` | goalscorers incomplete for 2002-04-17 Turkey v Chile | 1 | 2002–2002 (1) |
| `national_goals` | goalscorers incomplete for 2002-02-13 Italy v United States | 1 | 2002–2002 (1) |
| `national_goals` | goalscorers incomplete for 2003-02-12 France v Czech Republic | 1 | 2003–2003 (1) |
| `national_goals` | goalscorers incomplete for 2003-02-12 Italy v Portugal | 1 | 2003–2003 (1) |
| `national_goals` | goalscorers incomplete for 2003-04-02 Ukraine v Latvia | 1 | 2003–2003 (1) |
| `national_goals` | goalscorers incomplete for 2003-02-12 Netherlands v Argentina | 1 | 2003–2003 (1) |
| `national_goals` | goalscorers incomplete for 2003-02-12 Spain v Germany | 1 | 2003–2003 (1) |
| `national_goals` | goalscorers incomplete for 2003-03-29 Portugal v Brazil | 1 | 2003–2003 (1) |
| `national_goals` | goalscorers incomplete for 2003-02-12 England v Australia | 1 | 2003–2003 (1) |
| `national_goals` | goalscorers incomplete for 2004-02-18 Libya v Ukraine | 1 | 2004–2004 (1) |
| `national_goals` | goalscorers incomplete for 2004-02-18 Belgium v France | 1 | 2004–2004 (1) |
| `national_goals` | goalscorers incomplete for 2004-02-18 Greece v Bulgaria | 1 | 2004–2004 (1) |
| `national_goals` | goalscorers incomplete for 2004-02-18 Italy v Czech Republic | 1 | 2004–2004 (1) |
| `national_goals` | goalscorers incomplete for 2004-02-18 Netherlands v United States | 1 | 2004–2004 (1) |
| `national_goals` | goalscorers incomplete for 2005-02-09 France v Sweden | 1 | 2005–2005 (1) |
| `national_goals` | goalscorers incomplete for 2005-08-17 Ukraine v Serbia | 1 | 2005–2005 (1) |
| `national_goals` | goalscorers incomplete for 2005-02-09 Italy v Russia | 1 | 2005–2005 (1) |
| `national_goals` | goalscorers incomplete for 2005-01-22 Sweden v South Korea | 1 | 2005–2005 (1) |
| `national_goals` | goalscorers incomplete for 2005-02-09 Cameroon v Senegal | 1 | 2005–2005 (1) |
| `national_goals` | goalscorers incomplete for 2006-03-01 Russia v Brazil | 1 | 2006–2006 (1) |
| `national_goals` | goalscorers incomplete for 2006-08-16 Cameroon v Guinea | 1 | 2006–2006 (1) |
| `national_goals` | goalscorers incomplete for 2006-01-17 Ivory Coast v Jordan | 1 | 2006–2006 (1) |
| `national_goals` | goalscorers incomplete for 2007-02-06 Portugal v Brazil | 1 | 2007–2007 (1) |
| `national_goals` | goalscorers incomplete for 2007-02-07 France v Argentina | 1 | 2007–2007 (1) |
| `national_goals` | goalscorers incomplete for 2007-02-06 Ivory Coast v Guinea | 1 | 2007–2007 (1) |
| `national_goals` | goalscorers incomplete for 2007-02-07 Netherlands v Russia | 1 | 2007–2007 (1) |
| `national_goals` | goalscorers incomplete for 2007-01-18 Ecuador v Sweden | 1 | 2007–2007 (1) |
| `national_goals` | goalscorers incomplete for 2007-02-07 England v Spain | 1 | 2007–2007 (1) |
| `national_goals` | goalscorers incomplete for 2008-02-06 Italy v Portugal | 1 | 2008–2008 (1) |
| `national_goals` | goalscorers incomplete for 2008-03-26 Egypt v Argentina | 1 | 2008–2008 (1) |
| `national_goals` | goalscorers incomplete for 2008-05-23 Russia v Kazakhstan | 1 | 2008–2008 (1) |
| `national_goals` | goalscorers incomplete for 2008-01-13 Costa Rica v Sweden | 1 | 2008–2008 (1) |
| `national_goals` | goalscorers incomplete for 2008-02-06 Republic of Ireland v Brazil | 1 | 2008–2008 (1) |
| `national_goals` | goalscorers incomplete for 2008-02-06 England v Switzerland | 1 | 2008–2008 (1) |
| `national_goals` | goalscorers incomplete for 2009-02-11 France v Argentina | 1 | 2009–2009 (1) |
| `national_goals` | goalscorers incomplete for 2009-02-11 Portugal v Finland | 1 | 2009–2009 (1) |
| `national_goals` | goalscorers incomplete for 2009-02-11 Cameroon v Guinea | 1 | 2009–2009 (1) |
| `national_goals` | goalscorers incomplete for 2009-02-10 Brazil v Italy | 1 | 2009–2009 (1) |
| `national_goals` | goalscorers incomplete for 2009-01-24 United States v Sweden | 1 | 2009–2009 (1) |
| `national_goals` | goalscorers incomplete for 2009-02-11 Turkey v Ivory Coast | 1 | 2009–2009 (1) |
| `national_goals` | goalscorers incomplete for 2010-01-26 Argentina v Costa Rica | 1 | 2010–2010 (1) |
| `national_goals` | goalscorers incomplete for 2010-03-03 Netherlands v United States | 1 | 2010–2010 (1) |
| `national_goals` | goalscorers incomplete for 2010-03-03 Switzerland v Uruguay | 1 | 2010–2010 (1) |
| `national_goals` | goalscorers incomplete for 2010-03-03 Portugal v China | 1 | 2010–2010 (1) |
| `national_goals` | goalscorers incomplete for 2010-01-04 Tanzania v Ivory Coast | 1 | 2010–2010 (1) |
| `national_goals` | goalscorers incomplete for 2011-02-09 Denmark v England | 1 | 2011–2011 (1) |
| `national_goals` | goalscorers incomplete for 2011-02-09 North Macedonia v Cameroon | 1 | 2011–2011 (1) |
| `national_goals` | goalscorers incomplete for 2011-03-27 Brazil v Scotland | 1 | 2011–2011 (1) |
| `national_goals` | goalscorers incomplete for 2012-02-29 Switzerland v Argentina | 1 | 2012–2012 (1) |
| `national_goals` | goalscorers incomplete for 2012-06-02 Portugal v Turkey | 1 | 2012–2012 (1) |
| `national_goals` | goalscorers incomplete for 2012-02-29 Mexico v Colombia | 1 | 2012–2012 (1) |
| `national_goals` | goalscorers incomplete for 2012-08-15 England v Italy | 1 | 2012–2012 (1) |
| `national_goals` | goalscorers incomplete for 2012-01-13 Tunisia v Ivory Coast | 1 | 2012–2012 (1) |
| `national_goals` | goalscorers incomplete for 2012-02-29 England v Netherlands | 1 | 2012–2012 (1) |
| `national_goals` | goalscorers incomplete for 2012-01-18 Bahrain v Sweden | 1 | 2012–2012 (1) |
| `national_goals` | goalscorers incomplete for 2013-02-06 Portugal v Ecuador | 1 | 2013–2013 (1) |
| `national_goals` | goalscorers incomplete for 2013-02-06 Sweden v Argentina | 1 | 2013–2013 (1) |
| `national_goals` | goalscorers incomplete for 2013-02-06 France v Germany | 1 | 2013–2013 (1) |
| `national_goals` | goalscorers incomplete for 2013-01-23 Sweden v North Korea | 1 | 2013–2013 (1) |
| `national_goals` | goalscorers incomplete for 2013-02-06 England v Brazil | 1 | 2013–2013 (1) |
| `national_goals` | goalscorers incomplete for 2013-02-06 Spain v Uruguay | 1 | 2013–2013 (1) |
| `national_goals` | goalscorers incomplete for 2013-02-06 Wales v Austria | 1 | 2013–2013 (1) |
| `national_goals` | goalscorers incomplete for 2014-03-05 Portugal v Cameroon | 1 | 2014–2014 (1) |
| `national_goals` | goalscorers incomplete for 2014-05-17 Netherlands v Ecuador | 1 | 2014–2014 (1) |
| `national_goals` | goalscorers incomplete for 2014-03-05 South Africa v Brazil | 1 | 2014–2014 (1) |
| `national_goals` | goalscorers incomplete for 2014-03-05 Colombia v Tunisia | 1 | 2014–2014 (1) |
| `national_goals` | goalscorers incomplete for 2015-03-28 Argentina v El Salvador | 1 | 2015–2015 (1) |
| `national_goals` | goalscorers incomplete for 2015-06-16 Italy v Portugal | 1 | 2015–2015 (1) |
| `national_goals` | goalscorers incomplete for 2015-03-26 France v Brazil | 1 | 2015–2015 (1) |
| `national_goals` | goalscorers incomplete for 2015-11-13 Poland v Iceland | 1 | 2015–2015 (1) |
| `national_goals` | goalscorers incomplete for 2015-03-28 Morocco v Uruguay | 1 | 2015–2015 (1) |
| `national_goals` | goalscorers incomplete for 2015-03-25 Germany v Australia | 1 | 2015–2015 (1) |
| `national_goals` | goalscorers incomplete for 2015-06-07 France v Belgium | 1 | 2015–2015 (1) |
| `national_goals` | goalscorers incomplete for 2015-06-11 Spain v Costa Rica | 1 | 2015–2015 (1) |
| `national_goals` | goalscorers incomplete for 2015-01-28 Chile v United States | 1 | 2015–2015 (1) |
| `national_goals` | goalscorers incomplete for 2016-03-24 Wales v Northern Ireland | 1 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2016-03-25 Algeria v Ethiopia | 1 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2016-03-25 Gabon v Sierra Leone | 1 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2016-01-06 Sweden v Estonia | 1 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2016-09-06 Chile v Bolivia | 1 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2016-03-23 Poland v Serbia | 1 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2016-03-23 Croatia v Israel | 1 | 2016–2016 (1) |
| `national_goals` | goalscorers incomplete for 2017-03-28 Portugal v Sweden | 1 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-01-11 Chile v Croatia | 1 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-06-13 France v England | 1 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-03-24 Guinea v Gabon | 1 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-03-28 Netherlands v Italy | 1 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-01-08 Libya v Senegal | 1 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-06-07 Spain v Colombia | 1 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2017-03-28 Albania v Bosnia and Herzegovina | 1 | 2017–2017 (1) |
| `national_goals` | goalscorers incomplete for 2018-03-23 Netherlands v England | 1 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2018-03-22 China v Wales | 1 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2018-03-23 Senegal v Uzbekistan | 1 | 2018–2018 (1) |
| `national_goals` | goalscorers incomplete for 2019-03-23 Niger v Egypt | 1 | 2019–2019 (1) |
| `national_goals` | goalscorers incomplete for 2019-03-22 Algeria v Gambia | 1 | 2019–2019 (1) |
| `national_goals` | goalscorers incomplete for 2019-03-23 Burundi v Gabon | 1 | 2019–2019 (1) |
| `national_goals` | goalscorers incomplete for 2019-03-20 Germany v Serbia | 1 | 2019–2019 (1) |
| `national_goals` | goalscorers incomplete for 2019-03-22 South Korea v Bolivia | 1 | 2019–2019 (1) |
| `national_goals` | goalscorers incomplete for 2021-06-01 Poland v Russia | 1 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2021-03-25 Kenya v Egypt | 1 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2021-06-02 Norway v Luxembourg | 1 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2021-06-02 Germany v Denmark | 1 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2021-03-25 Zambia v Algeria | 1 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2021-06-01 Croatia v Armenia | 1 | 2021–2021 (1) |
| `national_goals` | goalscorers incomplete for 2022-06-04 Senegal v Benin | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-03-26 Republic of Ireland v Belgium | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-03-24 Scotland v Poland | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2021-09-30 Egypt v Liberia | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-03-26 Croatia v Slovenia | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-03-25 Norway v Slovakia | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-01-15 South Korea v Iceland | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2021-12-01 Algeria v Sudan | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-03-26 Netherlands v Denmark | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-01-16 Colombia v Honduras | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2021-09-01 Qatar v Serbia | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-06-02 Mexico v Uruguay | 1 | 2022–2022 (1) |
| `national_goals` | goalscorers incomplete for 2022-11-18 Egypt v Belgium | 1 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2022-11-17 Jordan v Spain | 1 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2022-09-23 Brazil v Ghana | 1 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2022-09-27 Algeria v Nigeria | 1 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2022-09-23 Egypt v Niger | 1 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2022-11-16 Poland v Chile | 1 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2023-03-25 Georgia v Mongolia | 1 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2022-09-23 South Korea v Costa Rica | 1 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2022-11-16 Albania v Italy | 1 | 2023–2023 (1) |
| `national_goals` | goalscorers incomplete for 2024-03-23 England v Brazil | 1 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2023-09-12 Germany v France | 1 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2024-03-22 Argentina v El Salvador | 1 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2023-09-10 Nigeria v São Tomé and Príncipe | 1 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2024-03-26 Republic of Ireland v Switzerland | 1 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2024-03-26 Ivory Coast v Uruguay | 1 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2023-09-12 Japan v Turkey | 1 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2024-03-21 Portugal v Sweden | 1 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2024-06-07 Poland v Ukraine | 1 | 2024–2024 (1) |
| `national_goals` | goalscorers incomplete for 2024-09-06 Egypt v Cape Verde | 1 | 2025–2025 (1) |
| `national_goals` | goalscorers incomplete for 2024-09-06 Morocco v Gabon | 1 | 2025–2025 (1) |
| `national_goals` | goalscorers incomplete for 2025-06-05 Georgia v Faroe Islands | 1 | 2025–2025 (1) |
| `national_goals` | goalscorers incomplete for 2025-03-25 Sweden v Northern Ireland | 1 | 2025–2025 (1) |
| `national_goals` | goalscorers incomplete for 2025-06-06 Poland v Moldova | 1 | 2025–2025 (1) |
| `national_goals` | goalscorers incomplete for 2025-06-06 Scotland v Iceland | 1 | 2025–2025 (1) |
| `national_goals` | goalscorers incomplete for 2024-09-10 Guinea v Tanzania | 1 | 2025–2025 (1) |
| `national_goals` | goalscorers incomplete for 2026-03-26 Georgia v Israel | 1 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2025-09-04 Norway v Finland | 1 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2025-10-09 Morocco v Bahrain | 1 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2025-10-11 Mexico v Colombia | 1 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2025-09-09 Mexico v South Korea | 1 | 2026–2026 (1) |
| `national_goals` | goalscorers incomplete for 2025-11-18 Kenya v Senegal | 1 | 2026–2026 (1) |
| `total apps/minutes/goals/assists/decisive_ga/cards/gk` | needs every bucket complete; UCL and other club competitions have no complete source | 462 | 2000–2026 (26) |
| `trophies_cup` | undated honours entry The second player <small>(after [[Javier Hernández]] in the [[2010–11 Manchester United F.C. season/2010–11 season]])</small> to score in the Premier League, [[FA Cup]], [[EFL Cup/League Cup]], European competition and [[FA Community Shield/Community Shield]] in a single season <small>([[2016–17 Manchester United F.C. season/2016–17 season]])</small> 2010–11 season: club season article | 2 | 2009–2012 (2) |
| `trophies_cup` | undated honours entry Copa do Brasil 2010: no date found in linked article | 1 | 2011–2011 (1) |
| `trophies_cup` | undated honours entry The second player <small>(after [[Javier Hernández]] in the [[2010–11 Manchester United F.C. season/2010–11 season]])</small> to score in the Premier League, [[FA Cup]], [[EFL Cup/League Cup]], European competition and [[FA Community Shield/Community Shield]] in a single season <small>([[2016–17 Manchester United F.C. season/2016–17 season]])</small> 2016–17 season: club season article | 1 | 2016–2016 (1) |
| `trophies_league` | undated honours entry The most expensive footballer in history 2001–2009: no date found in linked article | 5 | 2000–2006 (5) |
| `trophies_league` | undated honours entry IFFHS World Team of the Decade 2011–2020: no date found in linked article | 5 | 2016–2022 (5) |
| `trophies_league` | undated honours entry IFFHS UEFA Team of the Decade 2011–2020: no date found in linked article | 5 | 2016–2022 (5) |
| `trophies_league` | undated honours entry IFFHS Men's World Team 2017: no date found in linked article | 3 | 2016–2018 (3) |
| `trophies_league` | undated honours entry ESPN 2017: no date found in linked article | 3 | 2016–2018 (3) |
| `trophies_league` | undated honours entry Goal 50 2017–18: no date found in linked article | 3 | 2016–2018 (3) |
| `trophies_league` | undated honours entry IFFHS Men's World Team 2022: no date found in linked article | 3 | 2021–2023 (3) |
| `trophies_league` | undated honours entry Marca Leyenda Award 2022: no date found in linked article | 3 | 2021–2023 (3) |
| `trophies_league` | undated honours entry ESPN 2016: no date found in linked article | 2 | 2016–2017 (2) |
| `trophies_league` | undated honours entry IFFHS Men's World Team 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry ESPN 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry IFFHS World's Best Playmaker 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry ''The Guardian'' Best Footballer in the World 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry ''World Soccer'' Player of the Year 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry ''Dongqiudi'' Player of the Year 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry AIPS 2018: no date found in linked article | 2 | 2017–2018 (2) |
| `trophies_league` | undated honours entry Vyshcha Liha 1998–99: no date found in linked article | 1 | 2000–2000 (1) |
| `trophies_league` | undated honours entry Fastest Ligue 1 hat-trick 2016: no date found in linked article | 1 | 2016–2016 (1) |
| `trophies_league` | undated honours entry Longest goalscoring run in Ligue 1 2015–16: no date found in linked article | 1 | 2016–2016 (1) |
| `trophies_league` | undated honours entry Most goals scored in a single season (all competitions) 2015–16 season: club season article | 1 | 2016–2016 (1) |
| `trophies_league` | undated honours entry Campeón de Campeones 2024: no date found in linked article | 1 | 2026–2026 (1) |
| `ucl_* / club_other_* (match stats)` | no permitted source with every UCL / cup match (Transfermarkt, FBref blocked; StatsBomb has finals only) | 462 | 2000–2026 (26) |
| `ucl_stage` | no openfootball file for 2004-05 | 10 | 2005–2005 (1) |
| `ucl_stage` | no openfootball file for 2007-08 | 9 | 2008–2008 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2021-2022 | 9 | 2022–2022 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2023-2024 | 9 | 2024–2024 (1) |
| `ucl_stage` | no openfootball file for 1999-00 | 8 | 2000–2000 (1) |
| `ucl_stage` | no openfootball file for 2000-01 | 8 | 2001–2001 (1) |
| `ucl_stage` | no openfootball file for 2006-07 | 8 | 2007–2007 (1) |
| `ucl_stage` | no openfootball file for 2009-10 | 8 | 2010–2010 (1) |
| `ucl_stage` | no openfootball file for 2002-03 | 7 | 2003–2003 (1) |
| `ucl_stage` | no openfootball file for 2005-06 | 7 | 2006–2006 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2022-2023 | 7 | 2023–2023 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2024-2025 | 6 | 2025–2025 (1) |
| `ucl_stage` | no openfootball file for 2003-04 | 5 | 2004–2004 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2019-2019 | 5 | 2019–2019 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2022-2023 | 5 | 2023–2023 (1) |
| `ucl_stage` | no openfootball file for 2001-02 | 4 | 2002–2002 (1) |
| `ucl_stage` | no openfootball file for 2010-11 | 4 | 2011–2011 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2021-2021 | 4 | 2021–2021 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2025-2026 | 4 | 2026–2026 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2002-2002 | 3 | 2002–2002 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2004-2004 | 3 | 2004–2004 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2009-2009 | 3 | 2009–2009 (1) |
| `ucl_stage` | no openfootball file for 2008-09 | 3 | 2009–2009 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2011-2011 | 3 | 2011–2011 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2016-2016 | 3 | 2016–2016 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2017-2017 | 3 | 2017–2017 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2000-2000 | 2 | 2000–2000 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2012-2012 | 2 | 2012–2012 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2013-2013 | 2 | 2013–2013 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2014-2014 | 2 | 2014–2014 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2018-2018 | 2 | 2018–2018 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2001-2001 | 1 | 2001–2001 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2003-2003 | 1 | 2003–2003 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2006-2006 | 1 | 2006–2006 (1) |
| `ucl_stage` | 2 club spells in the infobox overlap 2010-2010 | 1 | 2010–2010 (1) |
| `ucl_stage` | club 'West Ham United F.C.' never matched an openfootball team name | 1 | 2016–2016 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2018-2018 | 1 | 2018–2018 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2021-2022 | 1 | 2022–2022 (1) |
| `ucl_stage` | club 'Athletic Bilbao' never matched an openfootball team name | 1 | 2024–2024 (1) |
| `ucl_stage` | 3 club spells in the infobox overlap 2023-2024 | 1 | 2024–2024 (1) |
| `ucl_stage` | club 'Inter Miami CF' never matched an openfootball team name | 1 | 2026–2026 (1) |
| `ucl_stage` | club 'Al Qadsiah FC' never matched an openfootball team name | 1 | 2026–2026 (1) |
| `ucl_stage` | club 'Al-Nassr FC' never matched an openfootball team name | 1 | 2026–2026 (1) |
