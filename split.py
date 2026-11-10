"""Train / test / hidden split of the men's Ballon d'Or top-10 data.

- train:  2000-2015
- test:   2016-2025 (2020 was cancelled, so there is no file for it)
- hidden: 2026 - the ranking we try to replicate. Only load it for the final check.

Each split is a dict {year: [row, ...]}, where a row is a dict with the CSV columns
(rank, age and points converted to numbers). Rows are in ranking order.
"""
import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "ballon_dor"

TRAIN_YEARS = list(range(2000, 2016))
TEST_YEARS = [y for y in range(2016, 2026) if y != 2020]
HIDDEN_YEAR = 2026


def load_year(year):
    with open(DATA_DIR / f"{year}.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["rank"] = int(r["rank"])
        r["age"] = int(r["age"])
        r["points"] = float(r["points"])
    return rows


def load_train():
    return {y: load_year(y) for y in TRAIN_YEARS}


def load_test():
    return {y: load_year(y) for y in TEST_YEARS}


def load_hidden():
    return {HIDDEN_YEAR: load_year(HIDDEN_YEAR)}


def score(predicted_names, actual_rows):
    """Compare a predicted top 10 (names, best first) with the actual ranking.

    hits:  how many predicted names are in the actual top 10
    exact: how many predicted names sit at their actual rank (ties count for every tied position)
    """
    actual_rank = {r["name"]: r["rank"] for r in actual_rows}
    hits = sum(name in actual_rank for name in predicted_names)
    exact = 0
    for pos, name in enumerate(predicted_names, start=1):
        rank = actual_rank.get(name)
        tied = sum(1 for r in actual_rows if r["rank"] == rank)
        if rank is not None and rank <= pos < rank + tied:
            exact += 1
    return {"hits": hits, "exact": exact}


if __name__ == "__main__":
    for label, split in [("train", load_train()), ("test", load_test())]:
        years = sorted(split)
        rows = sum(len(v) for v in split.values())
        print(f"{label}: {years[0]}-{years[-1]}, {len(years)} editions, {rows} rows")
    print(f"hidden: {HIDDEN_YEAR} (not loaded)")
