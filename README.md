# Ballon_d-Or
Predictor of the male Ballon d'Or, an annual football award presented by France Football to honor the best player of the season

See [BALLON_DOR.md](BALLON_DOR.md) for the voting criteria and how the vote works.

## Data

[`data/ballon_dor/`](data/ballon_dor/) holds the top 10 of the men's Ballon d'Or for each edition
from 2000 to 2026, one CSV per edition (`2000.csv` … `2026.csv`). There is no 2020 file: that
edition was cancelled.

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

- **Ties at 10th.** 2000 (Maldini, Beckham) and 2005 (Eto'o, Terry) have two players tied for
  10th, so those files have 11 rows. All other files have exactly 10.
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
