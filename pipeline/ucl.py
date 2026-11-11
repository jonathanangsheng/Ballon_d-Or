"""UEFA Champions League matches with dates and rounds, from openfootball/champions-league
(public domain, seasons 2011-12 onward)."""
import re
from datetime import date
from functools import lru_cache

from fetch import github_raw

REPO = "openfootball/champions-league"
MON = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
STOP = {"fc", "cf", "ac", "afc", "sc", "club", "de", "futbol", "football", "calcio", "sv", "ssc",
        "as", "ss", "cd", "ud", "sl", "fk", "sk", "pfc", "bc", "osc", "rc", "the", "f", "c", "04",
        "1899", "1900", "1909", "1913", "clube", "sport", "sporting", "e"}
# spelling differences between openfootball / StatsBomb and Wikipedia titles
TRANSLIT = {"munchen": "munich", "internazionale": "inter", "kiev": "kyiv", "kyiv": "kyiv",
            "milano": "milan", "olympique": "", "lyonnais": "lyon", "saintgermain": "saint germain"}


def club_tokens(name):
    from players import norm
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


@lru_cache(maxsize=None)
def season_matches(start_year):
    """[(date, stage, home, away)] for the season starting in start_year; None if no file."""
    path = f"{start_year}-{str(start_year + 1)[2:]}/cl.txt"
    try:
        text, url, fetched = github_raw(REPO, path)
    except Exception:
        return None, None
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


def club_stage(club_title, start, end):
    """(stage 0-5, urls) for the club's UCL matches dated in [start, end]; (None, reason) if a
    needed season file is missing. 6 (won) is set by the caller from the dated honours entry."""
    best, urls = 0, []
    for sy in range(start.year - 1, end.year + 1):
        season_lo, season_hi = date(sy, 8, 1), date(sy + 1, 6, 30)  # cl.txt starts at the group stage (Sep)
        if season_hi < start or season_lo > end:
            continue
        ms, url = season_matches(sy)
        if ms is None:
            return None, f"no openfootball file for {sy}-{str(sy + 1)[2:]}"
        urls.append(url)
        for d, stage, h, a in ms:
            if start <= d <= end and (same_club(club_title, h) or same_club(club_title, a)):
                best = max(best, stage)
    return best, urls


def club_known(club_title):
    """True if the club name matches a team in any openfootball season file (2011-12 on)."""
    for sy in range(2011, date.today().year):
        ms, _ = season_matches(sy)
        if ms and any(same_club(club_title, h) or same_club(club_title, a) for _, _, h, a in ms):
            return True
    return False
