"""Resolve each (year, name) in data/ballon_dor to its English Wikipedia article and parse
the parts we use: infobox club spells and the Honours section.

Only names and links are read from the edition articles; rank and points are never used.
"""
import csv
import re
import unicodedata
from pathlib import Path

from build_windows import YEARS, article_title
from fetch import wiki_prefetch, wiki_wikitext

BD_DIR = Path(__file__).parent / "data" / "ballon_dor"


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).strip()


def ballon_dor_rows():
    """[(year, name, country)] for every edition. Only identity columns are read."""
    out = []
    for y in YEARS:
        with open(BD_DIR / f"{y}.csv", encoding="utf-8") as f:
            out += [(y, r["name"], r["country"]) for r in csv.DictReader(f)]
    return out


def positions():
    """{(year, name): position} — identity column used only to decide whether GK columns apply."""
    out = {}
    for y in YEARS:
        with open(BD_DIR / f"{y}.csv", encoding="utf-8") as f:
            out.update({(y, r["name"]): r["position"] for r in csv.DictReader(f)})
    return out


def _edition_links(year):
    wt, _, _ = wiki_wikitext(article_title(year))
    links = {}
    for target, label in re.findall(r"\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]", wt):
        for key in (label or target, target):
            links.setdefault(norm(re.sub(r"\(.*?\)", "", key)), target.strip())
    for m in re.finditer(r"\{\{sortname\|([^|}]+)\|([^|}]+)(?:\|([^|}]+))?[^}]*\}\}", wt, re.I):
        first, last, link = (g.strip() if g else g for g in m.groups())
        title = link if link and "=" not in link else f"{first} {last}"
        links.setdefault(norm(f"{first} {last}"), title)
    return links


def resolve_titles():
    """{(year, name): wikipedia title or None}"""
    cache, out = {}, {}
    for year, name, _ in ballon_dor_rows():
        if year not in cache:
            cache[year] = _edition_links(year)
        out[(year, name)] = cache[year].get(norm(name))
    # A name not linked in its own edition (e.g. '{{sortname|Rodri|}}') takes the link of the
    # same name from another edition.
    by_name = {name: t for (_, name), t in out.items() if t}
    out = {k: v or by_name.get(k[1]) for k, v in out.items()}
    country = {(y, n): c for y, n, c in ballon_dor_rows()}
    return {k: _disambiguate(v, country[k]) if v else v for k, v in out.items()}


def _disambiguate(title, country):
    """If `title` is a disambiguation page, pick the footballer whose infobox lists `country`
    among his national teams. Returns the title unchanged if it already is a footballer."""
    wt, _, _ = wiki_wikitext(title)
    if not wt or player_article(title):
        return title
    cands = [t for line in wt.splitlines() if "footballer" in line
             for t in re.findall(r"\[\[([^\]|#]+)", line)[:1]]
    wiki_prefetch(cands)
    hits = []
    for t in cands:
        a = player_article(t)
        if a and re.search(r"\|\s*national_?team\d+\s*=[^\n]*" + re.escape(country), _infobox(a[0])):
            hits.append(t)
    return hits[0] if len(hits) == 1 else title


def player_article(title):
    """(wikitext, url, fetched_date) following redirects; None if missing or not a footballer."""
    wt, url, fetched = wiki_wikitext(title)
    if not wt or not re.search(r"\{\{\s*Infobox football biography", wt, re.I):
        return None
    return wt, url, fetched


# ---------- infobox club spells ----------

def _infobox(wt):
    start = re.search(r"\{\{\s*Infobox football biography", wt, re.I).start()
    depth, i = 0, start
    while i < len(wt):
        if wt.startswith("{{", i):
            depth, i = depth + 1, i + 2
        elif wt.startswith("}}", i):
            depth, i = depth - 1, i + 2
            if depth == 0:
                return wt[start:i]
        else:
            i += 1
    return wt[start:]


def _param(box, key):
    m = re.search(r"\|\s*" + re.escape(key) + r"\s*=([^\n]*)", box)
    return m.group(1).strip() if m else ""


def _years(s):
    """'2004–2021' -> (2004, 2021); '2021–' -> (2021, None); '2008' -> (2008, 2008)."""
    s = re.sub(r"<[^>]+>|\{\{[^}]*\}\}", "", s)
    m = re.search(r"(\d{4})\s*(?:[–-]\s*(\d{4})?)?", s)
    if not m:
        return None
    a = int(m.group(1))
    if m.group(2):
        return a, int(m.group(2))
    return (a, None) if re.search(r"\d{4}\s*[–-]", s) else (a, a)


def _link_target(s):
    m = re.search(r"\[\[([^\]|#]+)", s)
    return m.group(1).strip() if m else None


def club_spells(wt):
    """Senior club spells from the infobox: [(start_year, end_year_or_None, club_title, is_loan)]."""
    box = _infobox(wt)
    spells = []
    for i in range(1, 40):
        yrs, club = _years(_param(box, f"years{i}")), _param(box, f"clubs{i}")
        if yrs and club:
            spells.append((yrs[0], yrs[1], _link_target(club) or club, "loan" in club.lower()))
    return spells


# ---------- honours ----------

def honours_section(wt):
    m = re.search(r"^==\s*Honours\s*==\s*$(.*?)(?=^==[^=]|\Z)", wt, re.M | re.S)
    return m.group(1) if m else ""


def honours_entries(wt):
    """Parse '* [[Competition]]: [[target|label]], ...; runner-up: ...' bullet lines.

    Returns [(group, competition, season_target, season_label, result, competition_article)]
    where result is 'winner', 'runner-up' or 'third'. group is the nearest heading or bold line
    above (club, national team, 'Individual').
    """
    out, group = [], ""
    sec = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", honours_section(wt), flags=re.S)
    for line in sec.splitlines():
        line = line.strip()
        h = re.match(r"^(?:=+\s*(.*?)\s*=+\s*$|'''(.*?)'''|;\s*(.*)$)", line)
        if h:
            g = h.group(1) or h.group(2) or h.group(3)
            group = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", g).strip()
            continue
        if not line.startswith("*"):
            continue
        body = line.lstrip("*").strip()
        comp_m = re.match(r"\[\[([^\]|]+)(?:\|([^\]]*))?\]\]", body)
        comp = (comp_m.group(2) or comp_m.group(1)).split("#")[0].strip() if comp_m \
            else re.split(r":", body)[0].strip()
        comp_title = comp_m.group(1).split("#")[0].strip() if comp_m else ""
        rest = body[comp_m.end():] if comp_m else body.split(":", 1)[-1]
        result = "winner"
        for tok in re.split(r"(\[\[[^\]]+\]\]|runner-up|runners-up|second place|third place)", rest, flags=re.I):
            low = tok.lower()
            if low in ("runner-up", "runners-up", "second place"):
                result = "runner-up"
            elif low == "third place":
                result = "third"
            elif tok.startswith("[["):
                tm = re.match(r"\[\[([^\]|#]+)(?:\|([^\]]*))?\]\]", tok)
                if not tm or ":" in tm.group(1):
                    continue
                out.append((group, comp, tm.group(1).strip(), (tm.group(2) or tm.group(1)).strip(), result,
                            comp_title))
            else:
                # years written as plain text, e.g. '* [[FIFA World Cup Golden Ball]]: 2018'
                plain = re.sub(r"<[^>]+>|\{\{[^}]*\}\}|\([^)]*\)", " ", tok)
                for y in re.findall(r"(?<!\d)(\d{4}(?:\s*[–−-]\s*\d{2,4})?)(?!\d)", plain):
                    out.append((group, comp, "", y.strip(), result, comp_title))
    return out
