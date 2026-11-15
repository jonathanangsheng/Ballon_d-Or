# Ballon_d-Or
Predictor of the male Ballon d'Or, an annual football award presented by France Football to honor the best player of the season

See [BALLON_DOR.md](BALLON_DOR.md) for the voting criteria and how the vote works.

## Code

| What it does | Files |
|---|---|
| Fetch and parse sources (cached under `data/raw/`) | [`pipeline/`](pipeline/): `fetch`, `players`, `honours`, `intl`, `sb`, `ucl`, `wiki_stats` |
| Build and check the features | [`pipeline/`](pipeline/): `build_windows` → `build_features` → `report` → `check_features`; one-off `expand_ballon_dor` |
| Model | [`model/`](model/): `split`, `nn_model` |

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

Rows are in ranking order. The top-10 rows came first; [`pipeline/expand_ballon_dor.py`](pipeline/expand_ballon_dor.py)
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
python pipeline/build_windows.py && python pipeline/build_features.py && python pipeline/report.py && python pipeline/check_features.py
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

## Model

[`model/nn_model.py`](model/nn_model.py) predicts each edition's top 10 from the performance features. It uses
only the Python standard library and is a small dense network, as in the DSA312 lectures: one
hidden layer, a linear output and full-batch gradient descent. A linear model (no hidden layer)
is trained the same way as a baseline.

```bash
python model/nn_model.py           # choose the model on 2000–2015, report 2016–2025
python model/nn_model.py --final   # also refit on 2000–2025 and score 2026
```

### Setup

- **Split** ([`model/split.py`](model/split.py)): train 2000–2015 (421 rows), test 2016–2025 (270 rows, no
  2020), hidden 2026. Nothing is tuned by looking at 2026.
- **Inputs**: trophies won in the window (9 columns) and international tournament stage. Some runs
  add national goals, club goals (league, UCL, other cups), UCL stage, age and position. Blanks
  get the training median plus a missing flag; every column is standardised on the training
  rows only.
- **Target**: `(11 − rank) / 10` for the top 10, 0 below, trained with MSE. Ranking runs train
  instead on pairs from the same edition whose better player made the top 10. They use a
  logistic loss on the difference between the two scores.
- **Scoring** (`split.score`): each edition's predictions are sorted. *Hits* = how many of the
  predicted top 10 are in the real top 10; *exact* = how many are at their real rank. Tied
  predictions are broken by a fixed per-edition shuffle, never by file order (which is the true
  ranking). For the final model and best baseline it also gives *NDCG@10* (gain 11 − true rank,
  so the order near the top counts) and *winner* (1 if the predicted number one won).
- **Choosing a model**: leave-one-year-out on 2000–2015, holding out each training year in turn.
  The training length (epoch) is set where the mean validation loss is lowest. The best network
  and best linear model are those with the lowest validation loss (seed 8), and so is the best
  ranking run. Starting from the linear model, the network and then the ranking run each replace
  the pick only if they beat it on held-out top-10 hits, paired by edition: the 95% bootstrap
  interval of the mean per-edition difference over the 16 editions must lie entirely above 0.
  A network's hits are averaged over 5 seeds, each scored at seed 8's epoch, the epoch its test
  runs use. Hits, not loss, because the ranking runs' loss is on a different scale. No test
  number feeds any of these choices.
  The rule was committed on its own, before the code that applies it was written or run (commit
  `33fd341`, "State the LOYO-only model selection rule before implementing it (#5)"). After a
  code review, and still before any run, it was amended in a second README-only commit ("Amend
  the selection rule after review (#5)"): the ranking step used to need any gain in mean hits,
  and the extra seeds were scored at their own best epochs. Before these commits, test 2016–2025
  decided network vs linear: the network had to beat the linear model on test hits by more than
  its own spread over 5 seeds.
  That does not make the test score clean: 2016–2025 had already been looked at many times,
  across all the runs below and the old rule. The first edition no choice here has seen is 2027
  (issue #6).
  Each time the script runs, backprop is first checked against finite differences.

### Results

Seed 8; networks also show the mean ± sd over seeds 8, 18, 28, 38 and 48 (the linear models
start from zero, so seeds don't change them). Learning curves per run:
`results/nn_loyo_curves.csv`.

Selected model, by the rule above:

| Run | Held-out 2000–2015: hits / exact | Test 2016–2025: hits / exact | Test hits, 5 seeds |
|---|---|---|---|
| **13 linear + national, club goals** | **5.75 / 0.69** | **5.44 / 0.89** | – |

The comparisons behind it, on held-out hits per edition (network averaged over 5 seeds):
run 12, the best network, 5.61 vs 5.75, diff −0.14 [−0.44, +0.23], so run 13 stays; run 15, the
best ranking run, 5.88 vs 5.75, diff +0.12 [−0.31, +0.62], so run 13 stays.

Exploratory runs and baselines (not used for selection):

| Run | Held-out 2000–2015: hits / exact | Test 2016–2025: hits / exact | Test hits, 5 seeds |
|---|---|---|---|
| Heuristic (sort by trophies, then stage; no learning) | – | 4.67 / 0.78 | – |
| Previous edition's rank, unlisted players last (no learning) | 5.87 / 1.00 (2001–2015) | 5.33 / 0.78 | – |
| Major winners first: UCL, World Cup, Euro and Copa titles, then the heuristic (no learning) | 4.75 / 1.06 | 5.00 / 0.67 | – |
| 1 linear | 4.44 / 0.81 | 4.78 / 1.22 | – |
| 3 network, 4 softplus nodes | 4.44 / 0.62 | 3.89 / 0.44 | 4.56 ± 0.39 |
| 6 network + age, position | 5.19 / 0.56 | 5.33 / 0.89 | 5.02 ± 0.30 |
| 9 network, two layers of 4 | 4.12 / 0.44 | 4.33 / 0.56 | 4.58 ± 0.20 |
| 11 linear + national goals | 4.62 / 0.44 | 5.44 / 0.89 | – |
| 12 network + national, club goals | 5.69 / 1.06 | 5.00 / 1.22 | 5.11 ± 0.16 |
| 14 ranking network + national, club goals | 5.62 / 0.62 | 5.33 / 0.89 | 5.16 ± 0.13 |
| 15 ranking linear + national, club goals | 5.88 / 0.81 | 5.00 / 0.56 | – |

- **The final model does not clearly beat the simplest baseline.** Ranking nominees by where
  they finished in the previous edition gets 5.33 test hits to run 13's 5.44, and ranking by
  major titles gets 5.00. The paired test against previous-edition rank (below) finds no clear
  difference either way.
  Previous-edition rank's test hits per year: 2016: 4, 2017: 6, 2018: 5, 2019: 4, 2021: 7,
  2022: 6, 2023: 6, 2024: 7, 2025: 3. Its held-out figure starts at 2001, since 2000 has no
  previous edition in the data.
- The heuristic ties often (its scores are whole trophy counts plus stage / 10), so its number
  depends on the tie order: over 20 tie orders it averages 4.44 hits (range 4.11–4.67). The
  baselines tie too: previous-edition rank averages 5.34 (5.33–5.44) and major winners 5.01
  (4.78–5.33).
- **Final model: run 13**, where the old rule picked run 15. The change comes from the ranking
  step now needing the same margin as network vs linear. That amendment was made while run 15's
  lower test score (5.00 vs 5.44) was already in this README, and the rule as a whole was rewritten
  after the test years had been seen (see "Choosing a model"), so run 13's test score is not a
  clean estimate either.
- Club goals were the biggest gain on the held-out years: Spearman rose from 0.21 to 0.37 (runs 11 →
  13). On test, they and training to rank roughly tie with national goals alone.
- Networks never clearly beat the linear models. Wider or deeper networks had higher validation
  loss and no clear gain in hits, and results vary between seeds by up to half a hit per edition.
- Blanks are not spread the same way in training and test. In 2016–2025 a missing club-goal value
  is more often a top-10 player than in 2000–2015 (45% vs 30%). Some of the gain on the held-out
  years may not carry over to test for that reason.

### How sure are these numbers?

The test set has only 9 editions, and a model's hits move by more than one from edition to
edition. A test mean is therefore known only to about ±0.9 hits (95% bootstrap over editions):
run 13 gets 5.44 hits [4.56, 6.22] and 0.89 exact [0.44, 1.33]. Most rows of the table are within
that margin of each other, so read them as roughly equal, not as a ranking. The 5-seed spreads in
the table are far smaller and do not measure this.

The final model and the best baseline (previous-edition rank, the best on held-out 2000–2015
hits) are also compared edition by edition, which is more sensitive than comparing two intervals.
Each side is first averaged over its seeds or its 20 tie orders. Run 13 minus the baseline:

| | Mean diff | Bootstrap 95% | t-interval 95% | Verdict |
|---|---|---|---|---|
| Hits | +0.10 | [−0.92, +1.00] | [−1.15, +1.35] | no clear difference |
| Exact | +0.04 | [−0.56, +0.71] | [−0.74, +0.82] | no clear difference |

A win or loss is called only if both intervals exclude 0, because a percentile bootstrap runs
narrow on 9 editions. NDCG@10 is 0.587 for run 13 and 0.618 for the baseline. Run 13 named the
winner in 5 of 9 editions and the baseline in 2 of 9, the one place the model looks better, but 9
editions is too few to rely on. Per-edition numbers: `results/per_edition.csv`.

Hits are raw counts, not hits above chance. Every test edition has 30 nominees (chance: 3.33
hits), so this only matters next to the held-out 2000–2015 figures, where lists ran 23–35.

### 2026

2026 has been scored once, with an earlier model: run 11, refit on 2000–2025 before the
2000–2015 rankings were extended past the top 10 and before club goals were added. It got 7 hits,
0 exact and Spearman 0.43.

It was then scored a second time, once, with the final model of the time (run 15, refit on 2000–2025 at the
epoch chosen on 2000–2015): **6 hits, 2 exact, Spearman 0.51.** Nothing was changed after this
result. Both 2026 scores predate the tie-break fix (ties went to the player who really finished
higher); 2026 was not re-scored, to avoid a third look.

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Predicted (actual rank) | Kane (1) | Mbappé (2) | Haaland (8) | Fabián Ruiz (10) | Dembélé (7) | Ferran Torres (16) | Lautaro Martínez (22) | Kvaratskhelia (6) | Vitinha (14) | Nuno Mendes (23) |
| Actual | Kane | Mbappé | Yamal | Rodri | Messi | Kvaratskhelia | Dembélé | Haaland | Olise | Fabián Ruiz |
