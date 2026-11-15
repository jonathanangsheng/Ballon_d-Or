"""UEFA Champions League matches with dates and rounds, from openfootball/champions-league
(public domain, seasons 2011-12 onward) and, for earlier seasons, jalapic/engsoccerdata's
champs.csv (James Curley, free for non-commercial use with credit)."""
import csv
import re
import urllib.error
from collections import defaultdict
from datetime import date
from functools import lru_cache

from fetch import github_raw

REPO = "openfootball/champions-league"
FIRST_OPENFOOTBALL = 2011  # earlier seasons come from engsoccerdata
FIRST_CHAMPS = 1999  # earliest season a window needs (the 2000 edition); older rounds aren't mapped
CHAMPS = ("jalapic/engsoccerdata", "data-raw/champs.csv")
MON = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
STOP = {"fc", "cf", "ac", "afc", "sc", "club", "de", "futbol", "football", "calcio", "sv", "ssc",
        "as", "ss", "cd", "ud", "sl", "fk", "sk", "pfc", "bc", "osc", "rc", "the", "f", "c", "04",
        "1899", "1900", "1909", "1913", "clube", "sport", "sporting", "e"}
# spelling differences between openfootball / engsoccerdata / StatsBomb and Wikipedia titles
TRANSLIT = {"munchen": "munich", "internazionale": "inter milan", "kiev": "kyiv", "kyiv": "kyiv",
            "dinamo": "dynamo", "milano": "milan", "olympique": "", "lyonnais": "lyon",
            "saintgermain": "saint germain"}
NAMES = {"Inter (ITA)": "Inter Milan"}  # whole-name aliases, where a word-level one would catch other clubs


@lru_cache(maxsize=None)
def club_tokens(name):
    from players import norm
    name = NAMES.get(name.strip(), name)
    toks = []
    for t in norm(re.sub(r"\(.*?\)", "", name)).split():
        t = TRANSLIT.get(t, t)
        toks += [x for x in t.split() if x not in STOP]
    return frozenset(toks)


def same_club(a, b):
    ta, tb = club_tokens(a), club_tokens(b)
    return bool(ta) and ta == tb  # exact: subset matching would equate 'AC Milan' with 'Inter Milan'


def _stage(heading):
    h = heading.lower()
    if "final" in h and not re.search(r"semi|quarter|round of|finals,\s*(semi|quarter|round)", h):
        if re.search(r"(^|,\s*)final$", h.strip()):
            return 5
    if "semi" in h:
        return 4
    if "quarter" in h:
        return 3
    if "round of 16" in h:
        return 2
    if "group" in h or "league" in h or "playoff" in h:
        return 1
    return None


def _champs_stage(rnd):
    """Stage 1-5 for an engsoccerdata group or knockout round. The 1999-2003 second group stage
    ('GroupX-inter') had the last 16 teams, so it counts as 2."""
    if rnd.endswith("-inter"):
        return 2
    if rnd.startswith("Group"):
        return 1
    return {"R16": 2, "QF": 3, "SF": 4, "final": 5}[rnd]


@lru_cache(maxsize=None)
def _champs():
    """({season start year: [csv row]}, url): engsoccerdata's champs.csv, read once."""
    text, url, _ = github_raw(*CHAMPS)
    by = defaultdict(list)
    for r in csv.DictReader(text.splitlines()):
        by[int(r["Season"])].append(r)
    return dict(by), url


@lru_cache(maxsize=None)
def season_matches(start_year):
    """[(date, stage, home, away)] for the season starting in start_year; None if no file."""
    if start_year < FIRST_OPENFOOTBALL:
        by, url = _champs()
        if start_year not in by:
            return None, None
        # qualifying rounds left out, as openfootball starts at the group stage
        return [(date.fromisoformat(r["Date"]), _champs_stage(r["round"]), r["home"], r["visitor"])
                for r in by[start_year] if not r["round"].startswith("Q-")], url
    path = f"{start_year}-{str(start_year + 1)[2:]}/cl.txt"
    try:
        text, url, fetched = github_raw(REPO, path)
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        return None, None  # no file for this season; network failures still raise
    out, stage, cur, year, last_month = [], None, None, start_year, None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("▪"):
            stage = _stage(s.lstrip("▪ "))
            continue
        m = re.match(r"^(?:[A-Z][a-z]{2}\s+)?([A-Z][a-z]{2})/?\s*(\d{1,2})(?:\s+(\d{4}))?$", s)
        if m and m.group(1).lower() in MON:
            mon = MON[m.group(1).lower()]
            if m.group(3):
                year = int(m.group(3))
            elif last_month and mon < last_month:
                year += 1
            last_month = mon
            cur = date(year, mon, int(m.group(2)))
            continue
        mm = re.search(r"(?:\d{1,2}[.:]\d{2}\s+)?(.+?)\s+v\s+(.+?)\s+\d+-\d+", s)
        if mm and stage and cur:
            out.append((cur, stage, mm.group(1).strip(), mm.group(2).strip()))
    return out, url


def _seasons(start, end):
    """Start years of the seasons overlapping [start, end] (group stage Sep, final by June)."""
    return [sy for sy in range(start.year - 1, end.year + 1)
            if date(sy + 1, 6, 30) >= start and date(sy, 8, 1) <= end]


def club_stage(club_title, start, end):
    """(stage 0-5, urls) for the club's UCL matches dated in [start, end]; (None, reason) if a
    needed season file is missing. 6 (won) is set by the caller from the dated honours entry."""
    best, urls = 0, []
    for sy in _seasons(start, end):
        ms, url = season_matches(sy)
        if ms is None:
            return None, f"no Champions League match file for {sy}-{str(sy + 1)[2:]}"
        urls.append(url)
        for d, stage, h, a in ms:
            if start <= d <= end and (same_club(club_title, h) or same_club(club_title, a)):
                best = max(best, stage)
    return best, urls


def club_known(club_title, start, end):
    """True if the club name matches a team of each source the window's seasons come from, so a
    stage of 0 means 'not in the competition' rather than 'name never matched' (openfootball
    writes 'Inter (ITA)', which engsoccerdata's 'Internazionale' must not vouch for)."""
    return all(_known_in(club_title, sy < FIRST_OPENFOOTBALL) for sy in _seasons(start, end))


@lru_cache(maxsize=None)
def _known_in(club_title, champs):
    years = range(FIRST_CHAMPS, FIRST_OPENFOOTBALL) if champs else range(FIRST_OPENFOOTBALL, date.today().year)
    return any(ms and any(same_club(club_title, h) or same_club(club_title, a) for _, _, h, a in ms)
               for ms, _ in map(season_matches, years))
