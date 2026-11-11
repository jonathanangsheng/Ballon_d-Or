"""National-team features.

- Goals: martj42/international_results (CC0), every men's international with dated goalscorers.
  Filled only when every match of the country in the window has all its goals attributed.
- Major-tournament stage: rounds from openfootball (public domain) World Cup / Euro / Copa
  América files, or StatsBomb competition stages; dates and the final's result from martj42;
  squad membership from the Wikipedia '<edition> squads' article.
"""
import csv
import json
import io
import re
from collections import defaultdict
from datetime import date

from fetch import github_raw, web_page, wiki_wikitext
from players import norm

MARTJ = "martj42/international_results"
MAJOR = {"FIFA World Cup": "FIFA World Cup", "UEFA Euro": "UEFA Euro",
         "Copa América": "Copa América", "African Cup of Nations": "Africa Cup of Nations"}
# openfootball spells a few teams differently from martj42
ALIASES = {"United States": ["USA"], "South Korea": ["Korea Republic", "Korea"],
           "Ivory Coast": ["Côte d'Ivoire", "Cote d'Ivoire"], "Czech Republic": ["Czechia"],
           "Bosnia and Herzegovina": ["Bosnia-Herzegovina", "Bosnia"]}


def _csv(path):
    text, url, fetched = github_raw(MARTJ, path)
    return list(csv.DictReader(io.StringIO(text))), url, fetched


_cache = {}


def data():
    if not _cache:
        results, r_url, fetched = _csv("results.csv")
        scorers, g_url, _ = _csv("goalscorers.csv")
        shootouts, s_url, _ = _csv("shootouts.csv")
        for r in results:
            r["date"] = date.fromisoformat(r["date"])
        by_match = defaultdict(list)
        for g in scorers:
            by_match[(g["date"], g["home_team"], g["away_team"])].append(g)
        so = {(s["date"], s["home_team"], s["away_team"]): s["winner"] for s in shootouts}
        _cache.update(results=results, by_match=by_match, shootouts=so,
                      urls=[r_url, g_url, s_url], fetched=fetched)
    return _cache


def country_matches(country, start, end):
    d = data()
    return [r for r in d["results"] if start <= r["date"] <= end
            and country in (r["home_team"], r["away_team"]) and r["home_score"] != "NA"]


def national_goals(country, name, start, end):
    """(goals, matches, None) or (None, matches, reason)."""
    d = data()
    ms = country_matches(country, start, end)
    target = norm(name)
    known = any(norm(g["scorer"]) == target for gs in d["by_match"].values() for g in gs if g["team"] == country)
    if not known:
        return None, ms, "player name never appears among this country's goalscorers"
    goals = 0
    for m in ms:
        key = (m["date"].isoformat(), m["home_team"], m["away_team"])
        team_goals = int(m["home_score"] if m["home_team"] == country else m["away_score"])
        rows = [g for g in d["by_match"].get(key, []) if g["team"] == country]
        if len(rows) != team_goals:
            return None, ms, f"goalscorers incomplete for {key[0]} {key[1]} v {key[2]}"
        goals += sum(1 for g in rows if norm(g["scorer"]) == target and g["own_goal"] == "FALSE")
    return goals, ms, None


# ---------- tournament stage ----------

STAGE_NAMES = "0 none, 1 group, 2 first knockout round (R32/R16), 3 QF, 4 SF/3rd place, 5 final, 6 won"


def _round_stage(heading):
    h = heading.lower()
    if "group" in h or "matchday" in h:
        return 1
    if "round of 32" in h or "round of 16" in h or "eighth" in h:
        return 2
    if "quarter" in h:
        return 3
    if "semi" in h or "third" in h:
        return 4
    if re.match(r"^final\b", h.strip()):
        return 5
    return None


OPENFOOTBALL_FILES = {
    "FIFA World Cup": ("openfootball/worldcup", ["cup.txt", "cup_finals.txt"]),
    "UEFA Euro": ("openfootball/euro", ["euro.txt"]),
    "Copa América": ("openfootball/copa-america", ["copa.txt"]),
}


def openfootball_folders():
    """{repo: [top-level folder names]} via the GitHub tree API (cached)."""
    out = {}
    for repo, _ in OPENFOOTBALL_FILES.values():
        tree, _ = web_page(f"https://api.github.com/repos/{repo}/git/trees/master")
        out[repo] = [t["path"] for t in json.loads(tree)["tree"] if t["type"] == "tree"]
    return out


def openfootball_rounds(tournament, year, folders):
    """{team: deepest stage} from openfootball, plus the file urls; None if not available."""
    if tournament not in OPENFOOTBALL_FILES:
        return None
    repo, files = OPENFOOTBALL_FILES[tournament]
    folder = next((f for f in folders.get(repo, []) if f.startswith(f"{year}--")), None)
    if folder is None:
        return None
    sections, urls = [], []
    for fn in files:
        try:
            text, url, _ = github_raw(repo, f"{folder}/{fn}")
        except Exception:
            continue
        urls.append(url)
        stage = None
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("▪"):
                if "|" in s:  # schedule summary line, not a section
                    continue
                stage = _round_stage(s.lstrip("▪ ").strip())
                continue
            if stage and re.search(r"\d+\s*-\s*\d+", s) and not s.startswith("#"):
                sections.append((stage, s.split("@")[0].split("#")[0]))
    return (sections, urls) if sections else None


def team_stage(sections, country):
    names = [country] + ALIASES.get(country, [])
    best = 0
    for stage, line in sections:
        if any(re.search(r"(?<![A-Za-z])" + re.escape(n) + r"(?![A-Za-z])", line) for n in names):
            best = max(best, stage)
    return best


def tournament_instances(start, end):
    """Major tournament editions with any match in [start, end]: {(tournament, last_year): [matches]}."""
    return {k: v for k, v in _editions().items() if any(start <= m["date"] <= end for m in v)}


def _editions():
    """Split each tournament's matches into editions at gaps of more than 120 days; key each
    edition by the year of its last match (a Nov-Dec World Cup is keyed by that year)."""
    if "editions" not in _cache:
        by_t = defaultdict(list)
        for r in data()["results"]:
            if r["tournament"] in MAJOR and r["home_score"] != "NA":
                by_t[r["tournament"]].append(r)
        editions = {}
        for t, ms in by_t.items():
            ms.sort(key=lambda m: m["date"])
            cur = [ms[0]]
            for m in ms[1:]:
                if (m["date"] - cur[-1]["date"]).days > 120:
                    editions[(t, cur[-1]["date"].year)] = cur
                    cur = []
                cur.append(m)
            editions[(t, cur[-1]["date"].year)] = cur
        _cache["editions"] = editions
    return _cache["editions"]


def final_result(matches, country):
    """6 if country won the final, 5 if lost it, None if not in the final."""
    final = max(matches, key=lambda m: m["date"])
    if country not in (final["home_team"], final["away_team"]):
        return None
    hs, as_ = int(final["home_score"]), int(final["away_score"])
    if hs == as_:
        winner = data()["shootouts"].get((final["date"].isoformat(), final["home_team"], final["away_team"]))
    else:
        winner = final["home_team"] if hs > as_ else final["away_team"]
    return 6 if winner == country else 5


def squad_titles(tournament, edition_key, first_date):
    base = MAJOR[tournament]
    years = sorted({first_date.year, edition_key, edition_key - 1}, reverse=True)
    for y in years:
        title = f"UEFA Euro {y} squads" if tournament == "UEFA Euro" else f"{y} {base} squads"
        wt, url, fetched = wiki_wikitext(title)
        if wt:
            return wt, url
    return None, None


def in_squad(squad_wt, country, player_title, player_name):
    """True/False if the country's section was found, None if it wasn't."""
    names = "|".join(re.escape(n) for n in [country] + ALIASES.get(country, []))
    sec = re.search(r"^=+\s*(?:\[\[[^\]|]*\|)?(?:" + names + r")(?:\]\])?\s*=+\s*$(.*?)(?=^=+[^=]|\Z)",
                    squad_wt, re.M | re.S)
    if not sec:
        return None
    body = sec.group(1)
    want = {norm(re.sub(r"\(.*?\)", "", player_title)), norm(player_name)}
    for target, label in re.findall(r"\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]", body):
        if target.strip() == player_title or norm(re.sub(r"\(.*?\)", "", target)) in want \
                or (label and norm(label) in want):
            return True
    return False
