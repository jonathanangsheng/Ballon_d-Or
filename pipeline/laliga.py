"""La Liga, 22 seasons from 2000-01, every match with line-ups, bench, substitutions, goals, assists and
cards by minute: the 21st Century Spanish Football League Dataset (Sergio Lois, Zenodo,
doi:10.5281/zenodo.7341037, CC BY-NC 4.0; match data from BeSoccer). Fills the league bucket
where StatsBomb does not hold every match. No xG.

A nominee is the dataset player with his Wikipedia birth date, his nationality and a word of his
name (birth date and nationality alone matched Kluivert for van Nistelrooy). Event minutes are
capped at 90 in the source, so minutes exclude stoppage time as elsewhere.
"""
import json
import re
from collections import Counter
from datetime import date
from functools import lru_cache

import sb
from fetch import web_page
from intl import ALIASES
from players import norm

RECORD = "https://zenodo.org/api/records/7341037/files"
FILE = "season_{}-{:02d}.json"
GOALS = {"Goal", "Goal from penalty", "Free-kick goal"}
CONCEDED = GOALS | {"Own goal"}  # an own goal is listed under the team it counts for
REDS = {"Red card", "2nd yellow card leads to red card"}
OFF = REDS | {"Goes off"}
ACTIVE = GOALS | {"Assist", "Goes off"}  # only a player on the pitch can have these
PARTICLES = {"van", "der", "den", "de", "da", "do", "dos", "del", "di", "la", "le", "el"}


@lru_cache(maxsize=None)
def _held():
    """File names in the Zenodo record (cached like any page, so no request per run)."""
    text, _ = web_page(RECORD)
    return {f["key"] for f in json.loads(text)["entries"]}


@lru_cache(maxsize=4)  # a window touches at most two seasons; editions are built in year order
def season(start_year):
    """(data, url, fetched) for the season starting in start_year; (None, None, None) if not held."""
    name = FILE.format(start_year, (start_year + 1) % 100)
    if name not in _held():
        return None, None, None
    url = f"https://zenodo.org/records/7341037/files/{name}?download=1"
    text, fetched = web_page(url)
    return json.loads(text), url, fetched


def _squad(m, side):
    return (m[f"{side}_lineup"] or []) + (m[f"{side}_bench"] or [])  # a few matches lack one


def _word_re(word):
    """A dataset name word as a pattern: letters the source lost to U+FFFD match any letter."""
    return re.compile("".join("." if c == "�" else re.escape(norm(c)) for c in word))


def _same_name(name, p):
    """A word of the nominee's name (particles aside) is a word of the player's name or full name."""
    ours = [t for t in norm(name).split() if t not in PARTICLES]
    pats = [_word_re(word) for s in (p["name"], p["fullname"]) for word in (s or "").lower().split()]
    return any(pat.fullmatch(t) for pat in pats for t in ours)


def _player_record(m, side, href):
    """Stats of one player in one match; {'in_squad': False} if not in the line-up or bench;
    {'incomplete': True} if he scored, assisted or went off without a 'Comes on' event."""
    opp = "away" if side == "home" else "home"
    lineup = m[f"{side}_lineup"]
    ev = [e for e in m["events"] if e["player"] == href and e["team"] == side]
    if href not in _squad(m, side) and not ev:  # benches miss some subs (Messi, Mallorca 29 Jan 2006)
        return {"in_squad": False}
    on = 0 if href in lineup else min((e["minute"] for e in ev if e["type"] == "Comes on"), default=None)
    s = {"in_squad": True, "apps": 0, "minutes": 0}
    if on is None:
        if any(e["type"] in ACTIVE for e in ev):
            return {"in_squad": True, "incomplete": True}
        return s  # unused substitute
    off = min([e["minute"] for e in ev if e["type"] in OFF] + [90])
    conceded = sum(1 for e in m["events"]
                   if e["team"] == opp and e["type"] in CONCEDED and on <= e["minute"] <= off)
    s.update(apps=1, minutes=max(0, off - on),
             goals=sum(e["type"] in GOALS for e in ev), assists=sum(e["type"] == "Assist" for e in ev),
             yellow=sum(e["type"] == "Yellow card" for e in ev), red=sum(e["type"] in REDS for e in ev),
             ko_ga=0, gk_goals_conceded=conceded,
             gk_clean_sheets=int(on == 0 and off == 90 and conceded == 0))
    return s


def league_records(name, birth, country, w, seasons, wiki_apps):
    """(records, urls, None) or (None, urls, reason): every La Liga match of the player's team in
    the window, when the dataset holds all of that team's matches, with both line-ups and
    benches, in each of `seasons` (start years of the seasons the window touches).
    wiki_apps {season start year: league apps from his Wikipedia career table}: where given, his
    full-season apps here must equal it (the source leaves some substitutes off every list)."""
    countries = {norm(c) for c in [country] + ALIASES.get(country, [])}
    recs, urls = [], []
    for y in seasons:
        label = f"{y}-{(y + 1) % 100:02d}"
        data, url, fetched = season(y)
        if data is None:
            return None, urls, f"La Liga dataset has no {label} season"
        urls.append(url)
        hrefs = [p["href"] for p in data["players"] if p["dob"] == birth.isoformat()
                 and norm(p["country"]) in countries and _same_name(name, p)]
        if len(hrefs) != 1:
            return None, urls, f"{len(hrefs)} players in La Liga {label} with his name, birth date and nationality"
        href = hrefs[0]
        ms = [m for r in data["rounds"] for m in r["matches"]]
        sides = Counter(m[f"{s}_team"] for m in ms for s in ("home", "away") if href in _squad(m, s))
        if len(sides) != 1:
            return None, urls, f"listed for {len(sides)} teams in La Liga {label}"
        team = next(iter(sides))
        own = [m for m in ms if team in (m["home_team"], m["away_team"]) and m["status"] == "1"]
        teams = {m["home_team"] for m in ms} | {m["away_team"] for m in ms}
        if not sb.full_season(len(own), len(teams)):
            return None, urls, f"La Liga dataset {label}: {len(own)} played {team} matches"
        apps = 0
        for m in own:
            side = "home" if m["home_team"] == team else "away"
            if not m[f"{side}_lineup"] or m[f"{side}_bench"] is None:
                return None, urls, f"La Liga dataset {label}: a {team} match has no line-up or bench"
            r = _player_record(m, side, href)
            apps += r.get("apps", 0)
            d = date.fromisoformat(m["date_time"][:10])
            if w["start"] <= d <= w["end"]:
                if r.get("incomplete"):
                    return None, urls, f"La Liga dataset {label}: a substitute appearance has no 'Comes on' event"
                r.update(match_id=m["id"], date=d, team=team, bucket="league", source="zenodo_laliga",
                         competition="La Liga", season=label, stage="Regular Season", extra_time=0,
                         fetched=fetched)
                recs.append(r)
        if y in wiki_apps and apps != wiki_apps[y]:
            return None, urls, f"La Liga dataset {label}: {apps} apps, Wikipedia career table {wiki_apps[y]}"
    if not recs:
        return None, urls, "no La Liga season overlaps the window"
    return recs, urls, None
