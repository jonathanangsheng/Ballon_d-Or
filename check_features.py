"""Step 4: checks on data/features. Exits 1 if any hard check fails.

Window length outside 10-13 months is a warning (the real 2005, 2006 and 2021 windows are
shorter); the spot check reports mismatches without failing.
"""
import csv
import random
import re
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
FEAT = ROOT / "data" / "features"
LOGS = ROOT / "data" / "features" / "logs"
BD = ROOT / "data" / "ballon_dor"
FEATURE_CODE = ["build_features.py", "players.py", "honours.py", "intl.py", "sb.py", "ucl.py",
                "fetch.py", "build_windows.py"]

failures, warnings = [], []


def fail(msg):
    failures.append(msg)


def read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(v):
    return float(v) if v not in ("", None) else None


windows = {int(r["year"]): r for r in read(FEAT / "windows.csv")}
for r in windows.values():
    for k in ("window_start", "window_end", "voting_deadline", "ceremony_date"):
        r[k] = date.fromisoformat(r[k])
years = sorted(windows)


def in_window(year, d):
    w = windows[year]
    return w["window_start"] <= date.fromisoformat(d) <= w["window_end"]


# 1. exactly one feature row per (year, name)
features = {}
for y in years:
    bd = [(y, r["name"]) for r in read(BD / f"{y}.csv")]
    fr = read(FEAT / f"{y}.csv")
    keys = [(int(r["year"]), r["name"]) for r in fr]
    for k in set(bd) | set(keys):
        if keys.count(k) != 1 or k not in bd:
            fail(f"row count for {k}: {keys.count(k)} in features, {'in' if k in bd else 'not in'} ballon_dor")
    features.update({(int(r["year"]), r["name"]): r for r in fr})
print(f"[1] {len(features)} feature rows for {len(years)} editions")

# 2. every counted match is dated inside its edition's window
matches = read(LOGS / "matches.csv") if (LOGS / "matches.csv").exists() else []
nat = read(LOGS / "national_matches.csv") if (LOGS / "national_matches.csv").exists() else []
stages = read(LOGS / "stages.csv") if (LOGS / "stages.csv").exists() else []
for m in matches + nat:
    if not in_window(int(m["year"]), m["date"]):
        fail(f"match outside window: {m['year']} {m['name']} {m['date']}")
for s in stages:
    for k in ("first_match", "last_match"):
        if s[k] and not in_window(int(s["year"]), s[k]):
            fail(f"tournament match outside window: {s['year']} {s['name']} {s['competition']} {s[k]}")
# feature values must equal the sum of the logged matches
agg = defaultdict(float)
for m in matches:
    for s in ("apps", "minutes", "goals", "assists", "yellow", "red"):
        agg[(int(m["year"]), m["name"], m["bucket"], s)] += float(m[s] or 0)
for (y, n, b, s), v in agg.items():
    got = num(features[(y, n)][f"{b}_{s}"])
    if got is None or abs(got - v) > 1e-6:
        fail(f"{y} {n} {b}_{s}: feature {got} != logged {v}")
sys.path.insert(0, str(ROOT))
import intl  # noqa: E402
from players import norm  # noqa: E402

country = {(y, r["name"]): r["country"] for y in years for r in read(BD / f"{y}.csv")}
logged = {k[:3] for k in agg}

def log_rows(name):
    return read(LOGS / f"{name}.csv") if (LOGS / f"{name}.csv").exists() else []

# Wikipedia season totals (Aug-Jul windows): the season's dates must lie inside the window
season = {(int(s["year"]), s["name"], s["bucket"]): s for s in log_rows("season_stats")}
for (y, n, b), s in season.items():
    if not (in_window(y, s["first_match"]) and in_window(y, s["last_match"])):
        fail(f"season total outside window: {s}")
    for stat in ("apps", "goals"):
        if num(features[(y, n)][f"{b}_{stat}"]) != float(s[stat]):
            fail(f"{y} {n} {b}_{stat} != logged season total")
for (y, n), r in features.items():
    for b in ("league", "ucl", "club_other"):
        if r[f"{b}_apps"] != "" and (y, n, b) not in logged and (y, n, b) not in season:
            fail(f"{y} {n} {b}_apps filled without logged matches or season total")
# national stats: goal-list dates inside the window; year-table values only when the country
# played nothing between the window end and 31 December
goal_dates = defaultdict(list)
for g in log_rows("intl_goals"):
    goal_dates[(int(g["year"]), g["name"])].append(g["date"])
    if not in_window(int(g["year"]), g["date"]):
        fail(f"international goal outside window: {g}")
national_stats = log_rows("national_stats")
for s in national_stats:
    k, w = (int(s["year"]), s["name"]), windows[int(s["year"])]
    if num(features[k][f"national_{s['stat']}"]) != float(s["value"]):
        fail(f"{k} national_{s['stat']} != logged value")
    if s["source"] == "wikipedia goal list" and len(goal_dates[k]) != int(s["value"]):
        fail(f"{k} national goals {s['value']} but {len(goal_dates[k])} dated goals logged")
    if s["source"] == "wikipedia year table":
        y = w["window_end"].year
        if w["window_start"].month != 1 or intl.country_matches(
                country[k], w["window_end"] + timedelta(days=1), date(y, 12, 31)):
            fail(f"{k} year-table value used but the year does not equal the window")
for (y, n), r in features.items():
    for stat in ("goals", "apps"):
        if r[f"national_{stat}"] != "" and not any(
                (int(s["year"]), s["name"], s["stat"]) == (y, n, stat) for s in national_stats):
            fail(f"{y} {n} national_{stat} filled without a logged source")
print(f"[2b] {len(season)} season totals, {sum(map(len, goal_dates.values()))} dated international goals, "
      f"{len(national_stats)} national values checked")
for (y, n), r in features.items():
    if r["intl_tournament_apps"] != "" and (y, n, "intl_tournament") not in logged:
        # allowed only as a true zero: the country played no major-tournament match in the window
        w = windows[y]
        played = [m for ms in intl.tournament_instances(w["window_start"], w["window_end"]).values()
                  for m in ms if country[(y, n)] in (m["home_team"], m["away_team"])
                  and w["window_start"] <= m["date"] <= w["window_end"]]
        if played or num(r["intl_tournament_apps"]) != 0:
            fail(f"{y} {n} intl_tournament_apps filled without logged matches")
print(f"[2] {len(matches)} StatsBomb player-matches, {len(nat)} national matches, {len(stages)} stage entries checked")

# 3. no award counted after the voting deadline; no trophy counted outside the window
awards = read(LOGS / "awards.csv")
trophies = read(LOGS / "trophies.csv")
for a in awards:
    if a["counted"] == "True":
        y = int(a["year"])
        if not a["date"] or date.fromisoformat(a["date"]) >= windows[y]["voting_deadline"]:
            fail(f"award counted at/after deadline: {a}")
        if re.search(r"ballon d'or", a["award"], re.I):
            fail(f"Ballon d'Or-derived award counted: {a}")
for t in trophies:
    if t["counted"] == "True" and not in_window(int(t["year"]), t["date"]):
        fail(f"trophy counted outside window: {t}")
print(f"[3] {sum(a['counted'] == 'True' for a in awards)} awards, "
      f"{sum(t['counted'] == 'True' for t in trophies)} trophies checked")

# 4. nothing derived from Ballon d'Or rank/points or from after the ceremony
cols = list(next(iter(features.values())).keys())
if any(re.search(r"rank|points|ballon", c, re.I) for c in cols):
    fail("feature column named after rank/points/ballon d'or")
for fn in FEATURE_CODE:
    src = (ROOT / fn).read_text(encoding="utf-8")
    if re.search(r"""\[\s*["'](rank|points)["']\s*\]""", src):
        fail(f"{fn} reads the rank or points column")
for log, key in ((awards, "date"), (trophies, "date")):
    for e in log:
        if e["counted"] == "True" and date.fromisoformat(e[key]) >= windows[int(e["year"])]["ceremony_date"]:
            fail(f"counted item dated after the ceremony: {e}")
print("[4] no rank/points columns or reads; nothing counted after a ceremony")

# 5. same code path for every split; no year-specific constants for test/hidden years
# build_windows.py is exempt from the literal scan: its 2020 (cancelled) and 2022 (season
# windows) constants are the window rules given in the task, not tuning.
for fn in FEATURE_CODE:
    src = (ROOT / fn).read_text(encoding="utf-8")
    if re.search(r"^\s*(from split|import split)", src, re.M):
        fail(f"{fn} imports the train/test split")
    code = "\n".join(l.split("#")[0] for l in src.splitlines() if not l.strip().startswith(('"', "'")))
    if fn == "build_windows.py":
        continue
    lits = sorted({int(x) for x in re.findall(r"(?<![\w.])(20[12]\d)(?![\w])", code)} & set(range(2016, 2027)))
    if lits:
        fail(f"{fn} contains year literals from test/hidden years: {lits}")
print("[5] one code path; no test/hidden-year constants")

# 6. spot check: 10 random rows, goals and trophies against a second source
# Rows where the player played a major-tournament match in the window (StatsBomb log), so both
# checks are non-trivial. Goals: StatsBomb vs martj42 goalscorers for the same matches.
# Trophies: Wikipedia honours vs the martj42 result of each tournament final the player's
# country played in the window.
random.seed(0)
played = defaultdict(list)
for m in matches:
    if m["bucket"] == "intl_tournament" and float(m["apps"] or 0) > 0:
        played[(int(m["year"]), m["name"])].append(m)
pool = sorted(played)
sample = random.sample(pool, min(10, len(pool)))
d = intl.data()
res_by_date = defaultdict(list)
for x in d["results"]:
    res_by_date[x["date"].isoformat()].append(x)
mism = []
print(f"[6] spot check on {len(sample)} random rows (pool {len(pool)}):")
for k in sample:
    r = features[k]
    c = country[k]
    mj = 0
    for m in played[k]:
        for x in res_by_date[m["date"]]:
            if c in (x["home_team"], x["away_team"]):
                mj += sum(1 for g in d["by_match"].get((m["date"], x["home_team"], x["away_team"]), [])
                          if g["team"] == c and norm(g["scorer"]) == norm(k[1]) and g["own_goal"] == "FALSE")
    sbg = int(float(r["intl_tournament_goals"]))
    intl_tr = sum(int(float(r[f"trophies_{t}"] or 0)) for t in ("world_cup", "euro", "copa_america", "afcon"))
    w = windows[k[0]]
    won_final = any(intl.final_result(ms, c) == 6 for ms in
                    intl.tournament_instances(w["window_start"], w["window_end"]).values()
                    if w["window_start"] <= max(m["date"] for m in ms) <= w["window_end"])
    line = f"    {k[0]} {k[1]}: tournament goals StatsBomb={sbg} martj42={mj}; " \
           f"intl trophies honours={intl_tr} final-won={won_final}"
    if sbg != mj or (intl_tr > 0) != won_final:
        mism.append(line)
        line += "  <-- MISMATCH"
    print(line)
print(f"    {len(mism)} mismatching rows")

# 6b. national goals: Wikipedia's dated goal list vs martj42, where martj42 is complete
pool2 = []
for s in national_stats:
    k = (int(s["year"]), s["name"])
    if s["stat"] == "goals" and s["source"] == "wikipedia goal list":
        w = windows[k[0]]
        mj = intl.national_goals(country[k], k[1], w["window_start"], w["window_end"])[0]
        if mj is not None:
            pool2.append((k, int(s["value"]), mj))
sample2 = random.sample(pool2, min(10, len(pool2)))
print(f"[6b] national goals, Wikipedia goal list vs martj42, {len(sample2)} random rows (pool {len(pool2)}):")
for k, wiki, mj in sample2:
    line = f"    {k[0]} {k[1]}: Wikipedia={wiki} martj42={mj}"
    if wiki != mj:
        mism.append(line)
        line += "  <-- MISMATCH"
    print(line)
print(f"    all {len(pool2)} comparable rows: {sum(w != m for _, w, m in pool2)} differ")

# 7. sanity
for m in matches:
    cap = 120 if m["extra_time"] == "1" else 90
    if float(m["minutes"] or 0) > cap:
        fail(f"match minutes > {cap}: {m}")
for k, r in features.items():
    for c, v in r.items():
        if c.endswith("_goals") or c == "goals":
            if v != "" and float(v) < 0:
                fail(f"negative goals {k} {c}")
    for b in ("league", "intl_tournament", ""):
        p = f"{b}_" if b else ""
        a, mi = num(r[f"{p}apps"]), num(r[f"{p}minutes"])
        if a is not None and mi is not None and mi > 90 * a + 30 * a:
            fail(f"minutes > 90*apps + extra time: {k} {p}")
for y, w in windows.items():
    months = ((w["window_end"] - w["window_start"]).days + 1) / 30.4375
    if not 10 <= months <= 13:
        warnings.append(f"window {y}: {months:.2f} months (outside 10-13)")
print("[7] sanity: minutes, goals >= 0, window lengths")

for wmsg in warnings:
    print("WARNING", wmsg)
for f in failures[:50]:
    print("FAIL", f)
print(f"{len(failures)} failures, {len(warnings)} warnings, {len(mism)} spot-check mismatches")
sys.exit(1 if failures else 0)
