"""Steps 2-3: per-player performance features for every (year, name) in data/ballon_dor.

One code path for every year. Nothing reads Ballon d'Or rank or points. Every counted match,
trophy, award and tournament stage is written with its date to data/features/logs/ so
check_features.py can verify it against the window.

Output: data/features/<year>.csv, data/features/logs/*.csv, data/features/row_gaps.csv
"""
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path

import honours as H
import intl
import sb
import ucl
from build_windows import YEARS
from fetch import wiki_prefetch
from players import (ballon_dor_rows, club_spells, honours_entries, norm, player_article,
                     positions, resolve_titles)

ROOT = Path(__file__).parent
FEAT = ROOT / "data" / "features"
LOGS = ROOT / "data" / "features" / "logs"
BUCKETS = ["league", "ucl", "club_other", "national", "intl_tournament"]
BASIC = ["apps", "minutes", "goals", "assists", "ko_ga", "yellow", "red",
         "gk_clean_sheets", "gk_goals_conceded"]
ADV = ["xg", "npxg", "xa", "shots", "key_passes"]
TOTAL_PARTS = ["league", "ucl", "club_other", "national"]  # intl_tournament is inside national
SB_TOURNAMENT = {"FIFA World Cup": "FIFA World Cup", "UEFA Euro": "UEFA Euro",
                 "Copa América": "Copa America", "African Cup of Nations": "African Cup of Nations"}
SB_STAGE = {"Group Stage": 1, "Round of 16": 2, "Quarter-finals": 3, "Semi-finals": 4,
            "3rd Place Final": 4, "Final": 5}
INTL_TROPHY = {"FIFA World Cup": "world_cup", "UEFA Euro": "euro", "Copa América": "copa_america",
               "African Cup of Nations": "afcon"}

COLUMNS = (["year", "name"]
           + [f"{b}_{s}" for b in BUCKETS for s in BASIC]
           + [c for b in BUCKETS for s in ADV for c in (f"{b}_{s}", f"{b}_{s}_coverage")]
           + ["apps", "minutes", "goals", "assists", "decisive_ga", "yellow_cards", "red_cards",
              "gk_clean_sheets", "gk_goals_conceded", "match_rating_avg", "match_rating_avg_coverage"]
           + [f"trophies_{c}" for c in H.TROPHY_COLS] + ["trophies_total"]
           + ["ucl_stage", "intl_stage", "awards_count", "awards_list", "source_urls", "fetched_date"])


def load_windows():
    with open(FEAT / "windows.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {int(r["year"]): {"start": date.fromisoformat(r["window_start"]),
                             "end": date.fromisoformat(r["window_end"]),
                             "deadline": date.fromisoformat(r["voting_deadline"])} for r in rows}


def single_club(spells, w):
    """The club if exactly one infobox club spell overlaps the window's years, else (None, reason)."""
    lo, hi = w["start"].year, w["end"].year
    over = [s for s in spells if s[0] <= hi and (s[1] is None or s[1] >= lo)]
    if len(over) != 1:
        return None, f"{len(over)} club spells in the infobox overlap {lo}-{hi}"
    return over[0][2], None


# ---------- StatsBomb ----------

class SBData:
    def __init__(self):
        self.comps = sb.competitions()
        self._m = {}

    def matches(self, comp):
        key = (comp["competition_id"], comp["season_id"])
        if key not in self._m:
            self._m[key] = sb.matches(comp)
        return self._m[key]

    def league_comps(self):
        return [c for c in self.comps if c["competition_name"] in sb.LEAGUES]

    def tournament_comps(self, name):
        return [c for c in self.comps if c["competition_name"] == name]


def _season_overlaps(season_name, w):
    y0, y1 = sb.season_span(season_name)
    lo, hi = (date(y0, 8, 1), date(y1, 6, 30)) if y0 != y1 else (date(y0, 1, 1), date(y0, 12, 31))
    return lo <= w["end"] and hi >= w["start"]


def _needed_seasons(fmt_split, w):
    years = range(w["start"].year - 1, w["end"].year + 1)
    names = [f"{y}/{y + 1}" for y in years] if fmt_split else [str(y + 1) for y in years]
    return [n for n in names if _season_overlaps(n, w)]


def sb_league(data, club, name, w):
    """(records, urls, None) or (None, urls, reason)."""
    found = []
    for comp in data.league_comps():
        ms = data.matches(comp)
        teams = {m["home_team"]["home_team_name"] for m in ms}
        for t in teams:
            if ucl.same_club(club, t):
                found.append((comp, t))
    if not found:
        return None, [], "club not in StatsBomb league data"
    league = found[0][0]["competition_name"]
    team = found[0][1]
    avail = {c["season_name"]: c for c in data.league_comps() if c["competition_name"] == league}
    split = "/" in next(iter(avail))
    recs, urls = [], []
    for season in _needed_seasons(split, w):
        comp = avail.get(season)
        if comp is None:
            return None, urls, f"StatsBomb has no {league} {season}"
        ms = data.matches(comp)
        urls.append(ms[0]["_url"])
        if not sb.team_complete(ms, team):
            return None, urls, f"StatsBomb {league} {season} does not hold every {team} match"
        for m in ms:
            d = date.fromisoformat(m["match_date"])
            if w["start"] <= d <= w["end"] and team in (m["home_team"]["home_team_name"],
                                                       m["away_team"]["away_team_name"]):
                recs.append((m, team, d))
    out = [_record(m, team, d, name, "league") for m, team, d in recs]
    if not any(r["in_squad"] for r in out):
        return None, urls, "player name not found in any StatsBomb lineup of his club"
    return out, urls, None


def _record(m, team, d, name, bucket):
    r = sb.match_record(m, team, name)
    r.update(match_id=m["match_id"], date=d, team=team, bucket=bucket, source="statsbomb",
             competition=m["_comp"], season=m["_season"], stage=m["competition_stage"]["name"],
             fetched=m["_fetched"])
    return r


def _sb_team(ms, country):
    names = {norm(n) for n in [country] + intl.ALIASES.get(country, [])}
    for m in ms:
        for t in (m["home_team"]["home_team_name"], m["away_team"]["away_team_name"]):
            if norm(t) in names:
                return t
    return None


def sb_tournaments(data, country, name, w, editions):
    """StatsBomb records for the country's major-tournament matches in the window."""
    recs, urls = [], []
    for (tour, key), ms in editions.items():
        cms = [m for m in ms if country in (m["home_team"], m["away_team"])
               and w["start"] <= m["date"] <= w["end"]]
        if not cms:
            continue
        dates = {m["date"] for m in cms}
        hit = None
        for comp in data.tournament_comps(SB_TOURNAMENT[tour]):
            sms = data.matches(comp)
            if dates & {date.fromisoformat(m["match_date"]) for m in sms}:
                hit = sms
        if hit is None:
            return None, urls, f"StatsBomb has no {tour} {key}"
        team = _sb_team(hit, country)
        own = [m for m in hit if team in (m["home_team"]["home_team_name"], m["away_team"]["away_team_name"])
               and w["start"] <= date.fromisoformat(m["match_date"]) <= w["end"]] if team else []
        urls.append(hit[0]["_url"])
        if len(own) != len(cms):
            return None, urls, f"StatsBomb {tour} {key}: {len(own)} of {len(cms)} {country} matches"
        recs += [_record(m, team, date.fromisoformat(m["match_date"]), name, "intl_tournament") for m in own]
    if recs and not any(r["in_squad"] for r in recs):
        return None, urls, "player name not found in StatsBomb tournament lineups"
    return recs, urls, None


def aggregate(recs, is_gk):
    tot = {s: 0 for s in BASIC + ADV}
    for r in recs:
        for s in BASIC + ADV:
            tot[s] += r.get(s, 0) or 0
    for s in ADV:
        tot[s] = round(tot[s], 2)
    if not is_gk:
        tot["gk_clean_sheets"] = tot["gk_goals_conceded"] = ""
    return tot


# ---------- tournament stage ----------

def intl_stage(country, title, name, w, editions, folders, data, logs, key):
    """(stage, urls, reason). Uses only matches inside the window."""
    best, urls, unknown = 0, [], []
    for (tour, ek), ms in editions.items():
        cms = [m for m in ms if country in (m["home_team"], m["away_team"])]
        inside = [m for m in cms if w["start"] <= m["date"] <= w["end"]]
        if not inside:
            continue
        if len(inside) != len(cms):
            unknown.append(f"{tour} {ek} straddles the window")
            continue
        first = min(m["date"] for m in ms)
        swt, surl = intl.squad_titles(tour, ek, first)
        member = intl.in_squad(swt, country, title, name) if swt and title else None
        if member is None:
            unknown.append(f"{tour} {ek}: squad list not found")
            continue
        urls.append(surl)
        if not member:
            st = 0
        else:
            st, src = None, None
            of = intl.openfootball_rounds(tour, first.year, folders)
            if of:
                st = intl.team_stage(of[0], country) or None
                src = of[1]
            if st is None and tour in SB_TOURNAMENT:
                for comp in data.tournament_comps(SB_TOURNAMENT[tour]):
                    sms = data.matches(comp)
                    if {m["date"] for m in cms} & {date.fromisoformat(m["match_date"]) for m in sms}:
                        team = _sb_team(sms, country)
                        st = max((SB_STAGE.get(m["competition_stage"]["name"], 0) for m in sms
                                  if team in (m["home_team"]["home_team_name"], m["away_team"]["away_team_name"])),
                                 default=None)
                        src = [sms[0]["_url"]]
            if st is None:
                unknown.append(f"{tour} {ek}: no round data")
                continue
            urls += src
            if st >= 5:
                st = intl.final_result(ms, country) or st
        logs["stages"].append({"year": key[0], "name": key[1], "competition": tour, "edition": ek,
                               "first_match": min(m["date"] for m in inside),
                               "last_match": max(m["date"] for m in inside), "in_squad": member,
                               "stage": st})
        best = max(best, st)
    if unknown and best < 6:
        return None, urls, "; ".join(unknown)
    return best, urls, None


# ---------- main ----------

def build():
    windows = load_windows()
    rows = ballon_dor_rows()
    pos = positions()
    titles = resolve_titles()
    data = SBData()
    folders = intl.openfootball_folders()
    logs = defaultdict(list)
    gaps = []

    # batch-load every Wikipedia article we will read
    articles = {t: player_article(t) for t in set(titles.values()) if t}
    entries = set()
    for a in articles.values():
        if a:
            tr, aw = H.classify(honours_entries(a[0]))
            entries |= {(c, t, l) for c, t, l, *_ in tr} | set(aw)
    H.prefetch_entries(entries)
    squad_titles = set()
    for (tour, ek), ms in intl.tournament_instances(date(1999, 1, 1), date.today()).items():
        first = min(m["date"] for m in ms)
        for y in {first.year, ek, ek - 1}:
            squad_titles.add(f"UEFA Euro {y} squads" if tour == "UEFA Euro" else f"{y} {intl.MAJOR[tour]} squads")
    wiki_prefetch(squad_titles)

    out = defaultdict(list)
    for year, name, country in rows:
        key = (year, name)
        w = windows[year]
        row = {c: "" for c in COLUMNS}
        row.update(year=year, name=name)
        urls, fetched = [], set()

        def gap(field, reason):
            gaps.append({"year": year, "name": name, "field": field, "reason": reason})

        title = titles.get(key)
        art = articles.get(title) if title else None
        if art:
            urls.append(art[1])
            fetched.add(art[2])
        else:
            gap("wikipedia_article", "no footballer article resolved for this name")
        is_gk = pos[key] == "goalkeeper"

        # --- club bucket: league (StatsBomb, single club only) ---
        club, club_why = single_club(club_spells(art[0]), w) if art else (None, "no article")
        why = club_why
        recs_by_bucket = {}
        if club:
            recs, u, why = sb_league(data, club, name, w)
            urls += u
            if recs is not None:
                recs_by_bucket["league"] = recs
        if "league" not in recs_by_bucket:
            gap("league_*", why)
        gap("ucl_* / club_other_* (match stats)", "no permitted source with every UCL / cup match "
            "(Transfermarkt, FBref blocked; StatsBomb has finals only)")

        # --- national team ---
        editions = intl.tournament_instances(w["start"], w["end"])
        recs, u, why = sb_tournaments(data, country, name, w, editions)
        urls += u
        if recs is not None:
            recs_by_bucket["intl_tournament"] = recs
        else:
            gap("intl_tournament_*", why)
        goals, nms, why = intl.national_goals(country, name, w["start"], w["end"])
        d = intl.data()
        if goals is not None:
            row["national_goals"] = goals
            urls += d["urls"][:2]
            fetched.add(d["fetched"])
            for m in nms:
                logs["national_matches"].append({"year": year, "name": name, "date": m["date"],
                                                 "home": m["home_team"], "away": m["away_team"],
                                                 "tournament": m["tournament"]})
        else:
            gap("national_goals", why)
        gap("national_apps/minutes/assists/cards", "martj42 has goals only; no permitted source lists "
            "national-team line-ups, minutes or assists for every match")

        for b, recs in recs_by_bucket.items():
            agg = aggregate(recs, is_gk)
            for s in BASIC + ADV:
                row[f"{b}_{s}"] = agg[s]
            for s in ADV:
                row[f"{b}_{s}_coverage"] = "statsbomb"
            for r in recs:
                logs["matches"].append({"year": year, "name": name, **{k: r.get(k, "") for k in
                                        ["bucket", "source", "match_id", "date", "competition", "season",
                                         "stage", "team", "in_squad", "extra_time"] + BASIC + ADV}})
            fetched.update(r["fetched"] for r in recs if r.get("fetched"))
        for b in BUCKETS:
            for s in ADV:
                if not row[f"{b}_{s}_coverage"]:
                    row[f"{b}_{s}_coverage"] = "none"
        row["match_rating_avg_coverage"] = "none"
        gap("match_rating_avg", "no permitted source publishes per-match ratings (FBref/Transfermarkt blocked)")
        gap("total apps/minutes/goals/assists/decisive_ga/cards/gk", "needs every bucket complete; "
            "UCL and other club competitions have no complete source")

        # --- honours: trophies and awards ---
        trophies = {c: 0 for c in H.TROPHY_COLS}
        unknown_cats, award_names, awards_unknown = set(), [], False
        ucl_won = intl_won = False
        if art:
            tr, aw = H.classify(honours_entries(art[0]))
            for comp, target, label, result in tr:
                yrs = H.label_years(label) or H.label_years(target)
                if not yrs or yrs[1] < w["start"].year - 1 or yrs[0] > w["end"].year + 1:
                    continue
                cat = H.trophy_category(comp)
                dt, src, method = H.entry_date(comp, target, label)
                counted = bool(dt and w["start"] <= dt <= w["end"] and result == "winner")
                if dt is None and result == "winner":
                    unknown_cats.add(cat)
                    gap(f"trophies_{cat}", f"undated honours entry {comp} {label}: {method}")
                if counted:
                    trophies[cat] += 1
                    urls.append(src)
                    ucl_won |= cat == "ucl"
                    intl_won |= cat in INTL_TROPHY.values()
                logs["trophies"].append({"year": year, "name": name, "competition": comp, "category": cat,
                                         "label": label, "result": result, "date": dt or "",
                                         "method": method, "source": src or "", "counted": counted})
            for comp, target, label in aw:
                yrs = H.label_years(label) or H.label_years(target)
                if not yrs or yrs[1] != w["end"].year:
                    continue
                dt, src, method = H.entry_date(comp, target, label)
                counted = bool(dt and w["start"] <= dt < w["deadline"])
                if dt is None and method != "club season article":
                    awards_unknown = True
                    gap("awards_count", f"undated award {comp} {label}: {method}")
                if counted:
                    award_names.append(f"{comp} {label}")
                    urls.append(src)
                logs["awards"].append({"year": year, "name": name, "award": comp, "label": label,
                                       "date": dt or "", "method": method, "source": src or "",
                                       "voting_deadline": w["deadline"], "counted": counted})
        if art:
            for c in H.TROPHY_COLS:
                row[f"trophies_{c}"] = "" if c in unknown_cats else trophies[c]
            row["trophies_total"] = "" if unknown_cats else sum(trophies.values())
            row["awards_count"] = "" if awards_unknown else len(award_names)
            row["awards_list"] = "; ".join(award_names)

        # --- UCL stage ---
        if ucl_won:
            row["ucl_stage"] = 6
        elif club:
            st, info = ucl.club_stage(club, w["start"], w["end"])
            if st is None:
                gap("ucl_stage", info)
            elif st == 0 and not ucl.club_known(club):
                gap("ucl_stage", f"club '{club}' never matched an openfootball team name")
            else:
                row["ucl_stage"] = st
                urls += info
                logs["stages"].append({"year": year, "name": name, "competition": "UEFA Champions League",
                                       "edition": "", "first_match": "", "last_match": "",
                                       "in_squad": "", "stage": st})
        else:
            gap("ucl_stage", club_why)

        # --- international tournament stage ---
        st, u, why = intl_stage(country, title, name, w, editions, folders, data, logs, key)
        if intl_won:
            st = 6
        if st is None:
            gap("intl_stage", why)
        else:
            row["intl_stage"] = st
            urls += u

        row["source_urls"] = " ".join(dict.fromkeys(u for u in urls if u))
        row["fetched_date"] = max(fetched) if fetched else ""
        out[year].append(row)

    for year, rs in out.items():
        with open(FEAT / f"{year}.csv", "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=COLUMNS)
            wr.writeheader()
            wr.writerows(rs)
    LOGS.mkdir(parents=True, exist_ok=True)
    for name, rs in logs.items():
        if rs:
            with open(LOGS / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
                wr = csv.DictWriter(f, fieldnames=list(rs[0]))
                wr.writeheader()
                wr.writerows(rs)
    with open(FEAT / "row_gaps.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["year", "name", "field", "reason"])
        wr.writeheader()
        wr.writerows(g for g in gaps if g["reason"])
    print(f"wrote {sum(len(v) for v in out.values())} rows for {len(out)} editions")


if __name__ == "__main__":
    build()
