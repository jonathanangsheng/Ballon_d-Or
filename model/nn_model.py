"""Rank Ballon d'Or nominees with a small neural network (structure: one Dense hidden layer, 
linear output, full-batch gradient descent on MSE). Standard library only.

Target: (11 - rank) / 10 for the top 10, 0 below; each year's prediction is sorted and the top
10 scored with split.score(). Model choice uses leave-one-year-out on 2000-2015 only.

Ranking runs (RANK_RUNS) train on pairs instead: within a year, every (better, worse) pair whose
better player made the top 10, with a logistic loss on the score difference. Their epoch is
chosen on the same pairwise loss; one replaces the MSE pick only if it has more leave-one-year-out
top-10 hits.

    python model/nn_model.py           # select on 2000-2015, evaluate on 2016-2025
    python model/nn_model.py --final   # also refit on 2000-2025 and score 2026 (do this once)
"""
import csv
import math
import random
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from split import HIDDEN_YEAR, TEST_YEARS, TRAIN_YEARS, load_year, score

TROPHIES = ["trophies_league", "trophies_cup", "trophies_ucl", "trophies_uel", "trophies_world_cup",
            "trophies_euro", "trophies_copa_america", "trophies_intl_other", "trophies_club_intl_other"]
BASE = TROPHIES + ["intl_stage"]
CLUB_GOALS = ["league_goals", "ucl_goals", "club_other_goals"]
POSITIONS = ["goalkeeper", "defender", "midfielder", "forward"]
SEEDS = [8, 18, 28, 38, 48]
EPOCHS = 2000
ROOT = Path(__file__).parent.parent

RUNS = {  # name: (extra inputs, hidden layer sizes, activation, learning rate)
    "1 linear":          ([], (), None, 0.1),
    "3 nn4 softplus":    ([], (4,), "softplus", 0.01),
    "4 nn4 relu":        ([], (4,), "relu", 0.01),
    "5 nn8 softplus":    ([], (8,), "softplus", 0.01),
    "6 +age,position":   (["age", "position"], (4,), "softplus", 0.01),
    "7 +ucl_stage":      (["ucl_stage"], (4,), "softplus", 0.01),
    "8 +edition-centred": (["centred"], (4,), "softplus", 0.01),
    "9 nn4x4 softplus":  ([], (4, 4), "softplus", 0.01),
    "10 +national_goals": (["national_goals"], (4,), "softplus", 0.01),
    "11 linear +nat_goals": (["national_goals"], (), None, 0.1),
    "12 +nat,club goals": (["national_goals", "club_goals"], (4,), "softplus", 0.01),
    "13 linear +nat,club goals": (["national_goals", "club_goals"], (), None, 0.1),
    "14 rank nn +nat,club": (["national_goals", "club_goals"], (4,), "softplus", 0.01),
    "15 rank linear +nat,club": (["national_goals", "club_goals"], (), None, 0.1),
}
RANK_RUNS = {"14 rank nn +nat,club", "15 rank linear +nat,club"}


# ---------- data ----------

def load(years):
    rows = []
    for y in years:
        feats = {r["name"]: r for r in csv.DictReader(open(ROOT / f"data/features/{y}.csv", encoding="utf-8"))}
        for r in load_year(y):
            f = feats[r["name"]]
            rows.append({"year": y, "name": r["name"], "rank": r["rank"], "y": max(0.0, (11 - r["rank"]) / 10),
                         "age": r["age"], "position": r["position"],
                         **{c: float(f[c]) if f[c] != "" else None for c in BASE + ["ucl_stage", "national_goals"] + CLUB_GOALS}})
    return rows


def raw_matrix(rows, extra):
    """Input columns per run; None = missing. Edition-centred values use only that year's rows."""
    means = {}
    if "centred" in extra:
        for y in {r["year"] for r in rows}:
            yr = [r for r in rows if r["year"] == y]
            means[y] = {c: statistics.fmean([r[c] for r in yr if r[c] is not None] or [0]) for c in BASE}
    out = []
    for r in rows:
        x = [r[c] for c in BASE]
        if "age" in extra:
            x.append(float(r["age"]))
        if "position" in extra:
            x += [1.0 if r["position"] == p else 0.0 for p in POSITIONS]
        if "ucl_stage" in extra:
            x.append(r["ucl_stage"])
        if "national_goals" in extra:
            x.append(r["national_goals"])
        if "club_goals" in extra:
            x += [r[c] for c in CLUB_GOALS]
        if "centred" in extra:
            x += [None if r[c] is None else r[c] - means[r["year"]][c] for c in BASE]
        out.append(x)
    return out


def fit_prep(X):
    """Median imputation + a missing indicator per column with blanks + standardisation, fitted on X."""
    cols = list(zip(*X))
    med = [statistics.median([v for v in c if v is not None] or [0.0]) for c in cols]
    ind = [any(v is None for v in c) for c in cols]

    def impute(x):
        return [m if v is None else v for v, m in zip(x, med)] + \
               [1.0 if v is None else 0.0 for v, i in zip(x, ind) if i]
    filled = [impute(x) for x in X]
    mu = [statistics.fmean(c) for c in zip(*filled)]
    sd = [statistics.pstdev(c) or 1.0 for c in zip(*filled)]
    return lambda Z: [[(v - m) / s for v, m, s in zip(impute(z), mu, sd)] for z in Z]


# ---------- network ----------

ACT = {"softplus": (lambda z: z if z > 30 else math.log1p(math.exp(z)), lambda z: 1 / (1 + math.exp(-z))),
       "relu": (lambda z: max(0.0, z), lambda z: 1.0 if z > 0 else 0.0)}


def init(n, hidden, seed):
    """Layers [{'W': n_in x n_out, 'b': n_out}], hidden sizes then a 1-node linear output."""
    rnd = random.Random(seed)
    sizes = [n, *hidden, 1]
    layers = []
    for a, b in zip(sizes, sizes[1:]):
        lim = math.sqrt(6 / (a + b)) if hidden else 0.0  # Glorot uniform as Keras Dense; linear model starts at 0
        layers.append({"W": [[rnd.uniform(-lim, lim) for _ in range(b)] for _ in range(a)], "b": [0.0] * b})
    return layers


def n_params(p):
    return sum(len(L["b"]) + sum(map(len, L["W"])) for L in p)


def forward(p, x, act):
    """Activations per layer (input first), pre-activations per layer, and the output."""
    hs, zs = [x], []
    for k, L in enumerate(p):
        z = [b + sum(h * L["W"][i][j] for i, h in enumerate(hs[-1])) for j, b in enumerate(L["b"])]
        zs.append(z)
        hs.append(z if k == len(p) - 1 else [ACT[act][0](v) for v in z])
    return hs, zs, hs[-1][0]


def predict(p, X, act):
    return [forward(p, x, act)[2] for x in X]


def rank_pairs(rows):
    """(better, worse) row-index pairs within a year whose better player made the top 10."""
    return [(i, j) for i, a in enumerate(rows) for j, b in enumerate(rows)
            if a["year"] == b["year"] and a["rank"] <= 10 and a["rank"] < b["rank"]]


def pair_loss(preds, pairs):
    """Mean logistic loss log(1 + exp(-(s_better - s_worse))) over the pairs."""
    return statistics.fmean(ACT["softplus"][0](preds[j] - preds[i]) for i, j in pairs)


def grads(p, X, Y, act, pairs=None):
    """Loss and its gradients for the whole batch (full-batch gradient descent): MSE on Y, or,
    with pairs, the mean pairwise logistic loss."""
    g = [{"W": [[0.0] * len(r) for r in L["W"]], "b": [0.0] * len(L["b"])} for L in p]
    fw = [forward(p, x, act) for x in X]
    outs, n = [f[2] for f in fw], len(X)
    if pairs is None:
        loss = sum((o - y) ** 2 for o, y in zip(outs, Y)) / n
        dout = [2 * (o - y) / n for o, y in zip(outs, Y)]
    else:
        loss, dout = pair_loss(outs, pairs), [0.0] * n
        for i, j in pairs:
            s = ACT["softplus"][1](outs[j] - outs[i]) / len(pairs)  # sigmoid(-(s_i - s_j))
            dout[i] -= s
            dout[j] += s
    for (hs, zs, _), d0 in zip(fw, dout):
        d = [d0]  # dLoss/dz for the output layer
        for k in range(len(p) - 1, -1, -1):
            for j, dj in enumerate(d):
                g[k]["b"][j] += dj
                for i, h in enumerate(hs[k]):
                    g[k]["W"][i][j] += dj * h
            if k:
                d = [sum(p[k]["W"][i][j] * dj for j, dj in enumerate(d)) * ACT[act][1](zs[k - 1][i])
                     for i in range(len(hs[k]))]
    return loss, g


def train(X, Y, hidden, act, lr, epochs, seed, Xv=None, pairs=None):
    """Returns params, training-loss curve and (if Xv) validation predictions after every epoch."""
    p = init(len(X[0]), hidden, seed)
    sizes = [len(X[0]), *hidden, 1]
    assert n_params(p) == sum(a * b + b for a, b in zip(sizes, sizes[1:]))
    losses, val_preds = [], []
    for _ in range(epochs):
        loss, g = grads(p, X, Y, act, pairs)
        losses.append(loss)
        for L, G in zip(p, g):
            L["b"] = [b - lr * gb for b, gb in zip(L["b"], G["b"])]
            L["W"] = [[w - lr * gw for w, gw in zip(r, gr)] for r, gr in zip(L["W"], G["W"])]
        if Xv is not None:
            val_preds.append(predict(p, Xv, act))
    return p, losses, val_preds


def grad_check():
    """Backprop must match finite differences, for one and two hidden layers."""
    rnd = random.Random(0)
    X = [[rnd.gauss(0, 1) for _ in range(3)] for _ in range(5)]
    Y = [rnd.random() for _ in range(5)]
    for act in ACT:
        for hidden in [(2,), (2, 2)]:
            for pairs in [None, [(0, 1), (0, 2), (3, 4), (1, 4)]]:
                p = init(3, hidden, 1)
                _, g = grads(p, X, Y, act, pairs)
                for k, L in enumerate(p):
                    for i, j in [(len(L["W"]) - 1, 0)]:
                        v0, eps = L["W"][i][j], 1e-6
                        L["W"][i][j] = v0 + eps; up = grads(p, X, Y, act, pairs)[0]
                        L["W"][i][j] = v0 - eps; down = grads(p, X, Y, act, pairs)[0]
                        L["W"][i][j] = v0
                        assert abs((up - down) / (2 * eps) - g[k]["W"][i][j]) < 1e-6, (act, hidden, k, pairs)


# ---------- evaluation ----------

def top10(rows, preds, seed=0):
    """Predicted top 10 names. Ties go by a fixed per-edition shuffle: rows arrive in true rank
    order, so a stable sort would let the answer break them."""
    shuffled = sorted(r["name"] for r in rows)
    random.Random(rows[0]["year"] + 10000 * seed).shuffle(shuffled)
    tie = {n: i for i, n in enumerate(shuffled)}
    return [r["name"] for r, _ in sorted(zip(rows, preds), key=lambda t: (-t[1], tie[t[0]["name"]]))][:10]


def tie_check(rows):
    """With every prediction tied (bar one, so Spearman is defined), hits must sit at chance,
    10 * top-10 size / nominees per edition, not near the true top 10."""
    by_year = {}
    for r in rows:
        by_year.setdefault(r["year"], []).append(r)
    hits, chance = [], []
    for rs in by_year.values():
        first = min(r["name"] for r in rs)
        hits.append(year_metrics(rs, [float(r["name"] == first) for r in rs])[0])
        chance.append(10 * sum(r["rank"] <= 10 for r in rs) / len(rs))
    assert abs(statistics.fmean(hits) - statistics.fmean(chance)) < 1, (hits, chance)


def year_metrics(rows, preds, seed=0):
    """hits/exact via split.score, plus Spearman between prediction and target, for one year."""
    s = score(top10(rows, preds, seed), load_year(rows[0]["year"]))
    rho = statistics.correlation(preds, [r["y"] for r in rows], method="ranked")
    return s["hits"], s["exact"], rho


def mse(preds, rows):
    return statistics.fmean((p - r["y"]) ** 2 for p, r in zip(preds, rows))


def loyo(rows, extra, hidden, act, lr, seed, rank=False):
    """Leave-one-year-out on the training years. Returns mean train/val loss curves and the
    per-year metrics at the epoch with the lowest mean validation loss."""
    years = sorted({r["year"] for r in rows})
    tr_curves, va_curves, folds = [], [], []
    for y in years:
        tr = [r for r in rows if r["year"] != y]
        va = [r for r in rows if r["year"] == y]
        prep = fit_prep(raw_matrix(tr, extra))
        _, losses, vp = train(prep(raw_matrix(tr, extra)), [r["y"] for r in tr], hidden, act, lr, EPOCHS,
                              seed, prep(raw_matrix(va, extra)), rank_pairs(tr) if rank else None)
        tr_curves.append(losses)
        va_pairs = rank_pairs(va)
        va_curves.append([pair_loss(p, va_pairs) if rank else mse(p, va) for p in vp])
        folds.append((va, vp))
    tr_mean = [statistics.fmean(c) for c in zip(*tr_curves)]
    va_mean = [statistics.fmean(c) for c in zip(*va_curves)]
    best = min(range(EPOCHS), key=va_mean.__getitem__)
    per_year = [year_metrics(va, vp[best]) for va, vp in folds]
    return tr_mean, va_mean, best + 1, per_year


def test_eval(train_rows, test_rows, extra, hidden, act, lr, epochs, seed, rank=False):
    prep = fit_prep(raw_matrix(train_rows, extra))
    p, _, _ = train(prep(raw_matrix(train_rows, extra)), [r["y"] for r in train_rows], hidden, act, lr,
                    epochs, seed, pairs=rank_pairs(train_rows) if rank else None)
    preds = predict(p, prep(raw_matrix(test_rows, extra)), act)
    by_year = {}
    for r, v in zip(test_rows, preds):
        by_year.setdefault(r["year"], ([], []))
        by_year[r["year"]][0].append(r)
        by_year[r["year"]][1].append(v)
    per_year = {y: year_metrics(rs, vs) for y, (rs, vs) in sorted(by_year.items())}
    return (None if rank else mse(preds, test_rows)), per_year, n_params(p)


def heuristic(test_rows, seed=0):
    """Run 2: no learning. Sort by trophies won in the window, then tournament stage."""
    out = {}
    for y in sorted({r["year"] for r in test_rows}):
        rs = [r for r in test_rows if r["year"] == y]
        out[y] = year_metrics(rs, [sum(r[c] or 0 for c in TROPHIES) + (r["intl_stage"] or 0) / 10 for r in rs],
                              seed)
    return out


def avg(per_year, i):
    return statistics.fmean(m[i] for m in per_year)


def main():
    grad_check()
    train_rows, test_rows = load(TRAIN_YEARS), load(TEST_YEARS)
    tie_check(train_rows + test_rows)
    out = ROOT / "results"
    out.mkdir(exist_ok=True)

    print(f"Leave-one-year-out on {TRAIN_YEARS[0]}-{TRAIN_YEARS[-1]} ({len(train_rows)} rows), seed 8")
    print(f"{'run':26s} {'epoch':>5s} {'val loss':>8s} {'hits':>6s} {'exact':>6s} {'spearman':>8s}"
          "   (val loss: MSE, or pairwise loss for rank runs)")
    ex = ProcessPoolExecutor()  # every run and every test seed trains independently: one per core
    jobs = {name: ex.submit(loyo, train_rows, extra, hidden, act, lr, 8, name in RANK_RUNS)
            for name, (extra, hidden, act, lr) in RUNS.items()}
    chosen, curves, loyo_hits = {}, {}, {}
    for name in RUNS:
        tr, va, ep, per_year = jobs[name].result()
        chosen[name], curves[name], loyo_hits[name] = ep, (tr, va), avg(per_year, 0)
        print(f"{name:26s} {ep:5d} {va[ep - 1]:8.4f} {avg(per_year, 0):6.2f} {avg(per_year, 1):6.2f} "
              f"{avg(per_year, 2):8.3f}")
    tests = {name: [ex.submit(test_eval, train_rows, test_rows, extra, hidden, act, lr, chosen[name], s,
                              name in RANK_RUNS)
                    for s in (SEEDS if hidden else [8])]  # the linear model starts from zeros: seed-independent
             for name, (extra, hidden, act, lr) in RUNS.items()}
    with open(out / "nn_loyo_curves.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["epoch"] + [f"{n} {k}" for n in RUNS for k in ("train", "val")])
        for e in range(EPOCHS):
            w.writerow([e + 1] + [round(curves[n][k][e], 6) for n in RUNS for k in (0, 1)])

    # course-style 80/20 split, by year (3 of 16 years held out, seed 8), for the main model's curves
    val_years = set(random.Random(8).sample(TRAIN_YEARS, round(0.2 * len(TRAIN_YEARS))))
    tr = [r for r in train_rows if r["year"] not in val_years]
    va = [r for r in train_rows if r["year"] in val_years]
    prep = fit_prep(raw_matrix(tr, []))
    _, losses, vp = train(prep(raw_matrix(tr, [])), [r["y"] for r in tr], (4,), "softplus", 0.01, EPOCHS, 8,
                          prep(raw_matrix(va, [])))
    with open(out / "nn_8020_curves.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["epoch", "train_mse", "val_mse"])
        w.writerows([e + 1, round(a, 6), round(mse(p, va), 6)] for e, (a, p) in enumerate(zip(losses, vp)))
    print(f"80/20 by year: validation years {sorted(val_years)}; curves in results/nn_8020_curves.csv")

    print(f"\nTest {TEST_YEARS[0]}-{TEST_YEARS[-1]} ({len(test_rows)} rows): seed 8, then mean ± sd over seeds {SEEDS}")
    print(f"{'run':26s} {'params':>6s} {'MSE':>7s} {'hits':>6s} {'exact':>6s}   {'hits mean±sd':>13s} {'exact mean±sd':>13s}")
    h = heuristic(test_rows)
    print(f"{'2 heuristic':26s} {0:6d} {'-':>7s} {avg(h.values(), 0):6.2f} {avg(h.values(), 1):6.2f}")
    h20 = [heuristic(test_rows, s) for s in range(20)]  # it ties often, so show the tie-order spread
    print(f"{'2 heuristic, 20 tie orders':26s} {'':6s} {'':7s} "
          f"{statistics.fmean(avg(x.values(), 0) for x in h20):6.2f} "
          f"{statistics.fmean(avg(x.values(), 1) for x in h20):6.2f}   "
          f"hits {min(avg(x.values(), 0) for x in h20):.2f}-{max(avg(x.values(), 0) for x in h20):.2f}")
    results = {}
    for name in RUNS:
        runs = [f.result() for f in tests[name]]
        hits = [avg(r[1].values(), 0) for r in runs]
        exact = [avg(r[1].values(), 1) for r in runs]
        sd = (statistics.pstdev(hits), statistics.pstdev(exact))
        results[name] = (hits, exact, sd)
        mse_txt = "-" if runs[0][0] is None else f"{runs[0][0]:.4f}"
        print(f"{name:26s} {runs[0][2]:6d} {mse_txt:>7s} {hits[0]:6.2f} {exact[0]:6.2f}   "
              f"{statistics.fmean(hits):6.2f}±{sd[0]:.2f}   {statistics.fmean(exact):6.2f}±{sd[1]:.2f}")
        if name == "3 nn4 softplus":
            per_year = runs[0][1]
    ex.shutdown()
    print("\nMain model (3), seed 8, per test year: " +
          ", ".join(f"{y}: {m[0]} hits/{m[1]} exact" for y, m in per_year.items()))

    # best network and best linear model = lowest LOYO validation loss in each group; keep the
    # network only if it beats that linear model on test hits by more than its own seed spread
    def best(group):
        return min(group, key=lambda n: curves[n][1][chosen[n] - 1])
    nn = best([n for n in RUNS if RUNS[n][1] and n not in RANK_RUNS])
    lin = best([n for n in RUNS if not RUNS[n][1] and n not in RANK_RUNS])
    lin_hits = results[lin][0][0]
    nn_hits, _, nn_sd = results[nn]
    final = nn if statistics.fmean(nn_hits) - lin_hits > nn_sd[0] else lin
    print(f"\nBest on validation: network {nn}, linear {lin}. Test hits {statistics.fmean(nn_hits):.2f}"
          f"±{nn_sd[0]:.2f} vs {lin_hits:.2f} -> MSE pick: {final}")
    # a ranking run replaces it only with more leave-one-year-out hits (the losses differ in scale)
    rk = best(list(RANK_RUNS))
    print(f"Best ranking run on validation: {rk}. LOYO hits {loyo_hits[rk]:.2f} vs {loyo_hits[final]:.2f} "
          f"for {final} -> final model: {rk if loyo_hits[rk] > loyo_hits[final] else final}")
    if loyo_hits[rk] > loyo_hits[final]:
        final = rk

    if "--final" in sys.argv:
        extra, hidden, act, lr = RUNS[final]
        full, hidden_rows = train_rows + test_rows, load([HIDDEN_YEAR])
        _, per_year, _ = test_eval(full, hidden_rows, extra, hidden, act, lr, chosen[final], 8,
                                   final in RANK_RUNS)
        hits, exact, rho = per_year[HIDDEN_YEAR]
        print(f"{HIDDEN_YEAR} (refit on {TRAIN_YEARS[0]}-{TEST_YEARS[-1]}): {hits} hits, {exact} exact, "
              f"spearman {rho:.3f}")


if __name__ == "__main__":
    main()
