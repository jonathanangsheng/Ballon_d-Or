"""StatsBomb open data (github.com/statsbomb/open-data): per-match player stats with dates.

Data source: StatsBomb (free open data; attribution required when published).
Only men's competitions. A bucket is filled for a (year, name) only when every match of the
player's team in that bucket inside the window is in the dataset (see bucket_matches()).
"""
import json
import re
from collections import defaultdict

from fetch import github_raw
from players import norm

REPO = "statsbomb/open-data"
LEAGUES = {"La Liga", "Premier League", "Serie A", "1. Bundesliga", "Ligue 1", "Major League Soccer"}
TOURNAMENTS = {"FIFA World Cup", "UEFA Euro", "Copa America", "African Cup of Nations"}
REGULAR = {"Regular Season", "Group Stage"}


def _json(path):
    text, url, fetched = github_raw(REPO, "data/" + path)
    return json.loads(text), url, fetched


def competitions():
    comps, _, _ = _json("competitions.json")
    return [c for c in comps if c["competition_gender"] == "male"
            and c["competition_name"] in LEAGUES | TOURNAMENTS]


def matches(comp):
    ms, url, fetched = _json(f"matches/{comp['competition_id']}/{comp['season_id']}.json")
    for m in ms:
        m["_comp"], m["_season"], m["_url"], m["_fetched"] = (
            comp["competition_name"], comp["season_name"], url, fetched)
    return ms


def season_span(season_name):
    """'2015/2016' -> (2015, 2016); '2023' -> (2023, 2023)."""
    years = [int(y) for y in re.findall(r"\d{4}", season_name)]
    return years[0], years[-1]


def team_complete(ms, team):
    """A league season is complete for `team` if it has a full double round-robin for it."""
    teams = {m["home_team"]["home_team_name"] for m in ms} | {m["away_team"]["away_team_name"] for m in ms}
    own = [m for m in ms if team in (m["home_team"]["home_team_name"], m["away_team"]["away_team_name"])]
    return len(own) == 2 * (len(teams) - 1)


# ---------- per-match player stats ----------

def _clock(period, mmss):
    """Clock time capped to regulation per period (stoppage time not counted, FBref-style)."""
    mm, ss = (int(x) for x in mmss.split(":"))
    t = mm + ss / 60
    lo, hi = {1: (0, 45), 2: (45, 90), 3: (90, 105), 4: (105, 120)}.get(period, (120, 120))
    return min(max(t, lo), hi)


def lineup_player(lineups, team, name):
    """Find the player in a match lineup by name (nickname or full name), within `team`."""
    target = norm(name)
    for side in lineups:
        if side["team_name"] != team:
            continue
        for p in side["lineup"]:
            names = {norm(p["player_name"]), norm(p.get("player_nickname") or "")}
            if target in names:
                return p
    return None


def player_match_stats(match, team, player, events):
    """Stats of one player in one match, from lineup positions and events."""
    last_period = max(e["period"] for e in events if e["period"] <= 4)
    end = {2: 90, 4: 120}.get(last_period, 90)
    pid = player["player_id"]
    # On/off times from events (lineup position lists can overlap): on = kick-off for the
    # Starting XI, else the substitution that brought him on; off = substitution, red card or end.
    def at(e):
        return _clock(e["period"], f"{e['minute']}:{e['second']}")
    on = 0.0 if any(p["start_reason"] == "Starting XI" for p in player["positions"]) else min(
        (at(e) for e in events if e["type"]["name"] == "Substitution"
         and e["substitution"]["replacement"]["id"] == pid), default=None)
    offs = [at(e) for e in events if e.get("player", {}).get("id") == pid and e["period"] <= 4 and (
        e["type"]["name"] == "Substitution"
        or e.get("foul_committed", {}).get("card", {}).get("name") in ("Red Card", "Second Yellow")
        or e.get("bad_behaviour", {}).get("card", {}).get("name") in ("Red Card", "Second Yellow"))]
    minutes = max(0.0, min(offs + [end]) - on) if on is not None else 0.0
    is_gk = any(p["position"] == "Goalkeeper" for p in player["positions"])
    s = defaultdict(float)
    s["apps"] = 1 if player["positions"] else 0
    s["minutes"] = round(minutes)
    shot_xg = {e["id"]: e["shot"].get("statsbomb_xg", 0) for e in events if e["type"]["name"] == "Shot"}
    key_pass_to_shot = {e["shot"]["key_pass_id"]: e["id"] for e in events
                        if e["type"]["name"] == "Shot" and e["shot"].get("key_pass_id")}
    for e in events:
        if e["period"] == 5:  # penalty shoot-out
            continue
        mine = e.get("player", {}).get("id") == pid
        t = e["type"]["name"]
        if mine and t == "Shot":
            s["shots"] += 1
            s["xg"] += e["shot"].get("statsbomb_xg", 0)
            if e["shot"]["type"]["name"] != "Penalty":
                s["npxg"] += e["shot"].get("statsbomb_xg", 0)
            if e["shot"]["outcome"]["name"] == "Goal":
                s["goals"] += 1
        elif mine and t == "Pass":
            if e["pass"].get("goal_assist"):
                s["assists"] += 1
            if e["pass"].get("goal_assist") or e["pass"].get("shot_assist"):
                s["key_passes"] += 1
            if e["id"] in key_pass_to_shot:
                s["xa"] += shot_xg[key_pass_to_shot[e["id"]]]
        card = None
        if mine and t == "Foul Committed":
            card = e.get("foul_committed", {}).get("card", {}).get("name")
        elif mine and t == "Bad Behaviour":
            card = e.get("bad_behaviour", {}).get("card", {}).get("name")
        if card == "Yellow Card":
            s["yellow"] += 1
        elif card in ("Red Card", "Second Yellow"):
            s["red"] += 1
    if is_gk:
        conceded = 0
        intervals = [(_clock(p["from_period"], p["from"]),
                      end if p["to"] is None else _clock(p["to_period"], p["to"]))
                     for p in player["positions"] if p["position"] == "Goalkeeper"]
        for e in events:
            if e["period"] == 5:
                continue
            opp_goal = (e["type"]["name"] == "Shot" and e["team"]["name"] != team
                        and e["shot"]["outcome"]["name"] == "Goal")
            own_goal = e["type"]["name"] == "Own Goal For" and e["team"]["name"] != team
            if opp_goal or own_goal:
                t = _clock(e["period"], f"{e['minute']}:{e['second']}")
                if any(a <= t <= b for a, b in intervals):
                    conceded += 1
        s["gk_goals_conceded"] = conceded
        full = intervals and intervals[0][0] == 0 and intervals[-1][1] == end
        s["gk_clean_sheets"] = 1 if full and conceded == 0 else 0
    s["ko_ga"] = (s["goals"] + s["assists"]) if match["competition_stage"]["name"] not in REGULAR else 0
    s["extra_time"] = 1 if end == 120 else 0
    return dict(s), is_gk


def match_record(match, team, name):
    """Return a per-match dict for `name` playing for `team`, or None if not in the lineup."""
    mid = match["match_id"]
    lineups, lu_url, _ = _json(f"lineups/{mid}.json")
    p = lineup_player(lineups, team, name)
    if p is None:
        return {"in_squad": False}
    if not p["positions"]:
        return {"in_squad": True, "apps": 0, "minutes": 0, "url": lu_url}
    events, ev_url, _ = _json(f"events/{mid}.json")
    stats, is_gk = player_match_stats(match, team, p, events)
    stats.update(in_squad=True, url=ev_url, is_gk=is_gk)
    return stats
