# Ballon_d-Or
Predictor of the male Ballon d'Or, an annual football award presented by France Football to honor the best player of the season

See [BALLON_DOR.md](BALLON_DOR.md) for the voting criteria and how the vote works.

## Data

[`data/ballon_dor/`](data/ballon_dor/) holds the men's Ballon d'Or ranking for each edition from
2000 to 2026, one CSV per edition (`2000.csv` … `2026.csv`). There is no 2020 file: that edition
was cancelled. How far down each file goes:

| Editions | Rows | What is included |
|---|---|---|
| 2016–2026 | 30 | The full 30-player shortlist |
| 2010–2015 | 23 | The full 23-player FIFA shortlist |
| 2008–2009 | 30 | The full 30-player shortlist |
| 2000–2007 | 24–35 | Every player who received votes, down to 30th (ties at 30th kept). The rest of each 50-man shortlist got no votes and has no rank, so it is left out. |

Rows are in ranking order. The top-10 rows came first; [`expand_ballon_dor.py`](expand_ballon_dor.py)
added the 2000–2015 rows below them from the same Wikipedia tables without changing the top 10.

Columns: `rank,name,age,country,position,club,points`

| Column | Meaning |
|---|---|
| `rank` | Final placing. Tied players share a rank. |
| `name` | Player name as shown in the source ranking. |
| `age` | Age in whole years on the day of that edition's ceremony (date from the edition's Wikipedia infobox). |
| `country` | National team the player represents. |
| `position` | One of `goalkeeper`, `defender`, `midfielder`, `forward`. |
| `club` | Club at the time of the vote. When the source lists two clubs for the year, the later one is used. |
| `points` | Vote points for that edition (see the 2010–2015 note below). |

### Things to know

- **Ties.** 2000 (Maldini, Beckham) and 2005 (Eto'o, Terry) have two players tied for 10th, so
  their top 10 has 11 players. Lower down ties are common (e.g. eleven players tied at 20th with
  0 points in 2016 and 2022; six tied at 30th with 1 point in 2007), and from 2008 on the
  `points` column can be 0.
- **New rows' age and position** follow the same rules as the top 10: age from the player's
  infobox birth date on the ceremony day, first infobox position grouped as below. FIFA-coded
  countries (`{{fb|ARG}}`) use the name in Wikipedia's `Template:Country data <code>`.
- **2010–2015 are not points.** During the FIFA Ballon d'Or years FIFA published each player's
  share of the vote, not a points total, so `points` holds that **percentage** (e.g. `22.65`
  means 22.65%). Do not compare these values with points from other years.
- **Points scales change.** Even outside 2010–2015, the number of voters and the points per
  place changed over time, so raw points are only comparable within one edition.
- **Position.** 2022–2026 use the position given in the Wikipedia ranking table. Earlier years
  use the first position listed in the player's Wikipedia infobox, grouped as: goalkeeper →
  goalkeeper; any full-back/centre-back/defender → defender; any midfielder (defensive, central,
  attacking) → midfielder; striker, forward, second striker or winger → forward. A player can
  therefore have a different position in different eras of the data.

### Sources

- Rankings, clubs, nationality and points: the English Wikipedia article for each edition
  (`<year> Ballon d'Or`, or `<year> FIFA Ballon d'Or` for 2010–2015), fetched November 2026.
- Birth dates and pre-2022 positions: each player's English Wikipedia article infobox.
- One correction: Wikipedia's 2004 table lists Wayne Rooney's club as Everton only; his
  article shows he joined Manchester United on 31 August 2004, before the December ceremony, so
  his club is Manchester United.

## Performance features

[`data/features/`](data/features/) holds one row per nominee per edition with stats for that
edition's judging period (`<year>.csv`), the judging windows (`windows.csv`), what is missing
and why ([`gaps.md`](data/features/gaps.md)) and how many rows each column fills
([`coverage.md`](data/features/coverage.md)). Rebuild and check:

```bash
python build_windows.py && python build_features.py && python report.py && python check_features.py
```

### Feature sources

- Match event data (minutes, goals, assists, cards, xG and more) provided by
  [StatsBomb](https://statsbomb.com/) through their free
  [open data](https://github.com/statsbomb/open-data).
- International results and goalscorers:
  [martj42/international_results](https://github.com/martj42/international_results) (CC0).
- Tournament rounds and Champions League results: [openfootball](https://github.com/openfootball)
  (public domain).
- Trophies, awards, squads and edition dates: English Wikipedia (CC BY-SA), fetched November 2026.
