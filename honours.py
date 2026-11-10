"""Trophies and individual awards from the player's Wikipedia 'Honours' section.

Each honours entry links to a season / edition / final article; the entry is dated by the latest
date in that article's infobox (competition end = final or last matchday; award = ceremony or
season end). Undated entries are never guessed: the affected count is left blank.
"""
import re
from datetime import date

from fetch import wiki_prefetch, wiki_wikitext

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august", "september",
     "october", "november", "december"], start=1)}
YOUTH = re.compile(r"\bU-?\d{2}\b|under-\d{2}|youth|olympic", re.I)
EXCLUDED_AWARD = re.compile(r"ballon d'or|kopa trophy|yashin trophy|gerd müller trophy|"
                            r"socrates award|orders?\b|decorations?|medal of|knight|commander", re.I)
TROPHY_CATEGORIES = [
    ("ucl", re.compile(r"UEFA Champions League|European Cup", re.I)),
    ("uel", re.compile(r"UEFA Europa League|UEFA Cup", re.I)),
    ("world_cup", re.compile(r"^FIFA World Cup$", re.I)),
    ("euro", re.compile(r"UEFA European Championship|UEFA Euro\b", re.I)),
    ("copa_america", re.compile(r"Copa Am[ée]rica", re.I)),
    ("afcon", re.compile(r"Africa(n)? Cup of Nations", re.I)),
    ("intl_other", re.compile(r"Confederations Cup|Nations League|Gold Cup|Asian Cup|Finalissima|"
                              r"Olympic|Artemio Franchi", re.I)),
    ("club_intl_other", re.compile(r"UEFA Super Cup|Club World Cup|Intercontinental Cup|"
                                   r"Conference League|Intertoto", re.I)),
    ("cup", re.compile(r"Cup|Copa|Coppa|Pokal|Coupe|Super|Shield|Trophy|Taça|Beker|Supercopa|"
                       r"Trophée|Troph|Supercoppa|Supercup|DFL|Leagues Cup|Community", re.I)),
]
TROPHY_COLS = ["league"] + [c for c, _ in TROPHY_CATEGORIES]


def trophy_category(comp):
    for cat, pat in TROPHY_CATEGORIES:
        if pat.search(comp):
            return cat
    return "league"


def label_years(label):
    """'2008–09' -> (2008, 2009); '2009' -> (2009, 2009); None if no year."""
    m = re.search(r"(\d{4})(?:\s*[–/−-]\s*(\d{2,4}))?", label)
    if not m:
        return None
    a = int(m.group(1))
    b = m.group(2)
    if b is None:
        return a, a
    b = int(b) if len(b) == 4 else (a // 100) * 100 + int(b)
    return a, (b if b >= a else b + 100)


def _infobox_text(wt):
    m = re.search(r"\{\{\s*Infobox", wt, re.I)
    if not m:
        return ""
    depth, i = 0, m.start()
    while i < len(wt):
        if wt.startswith("{{", i):
            depth, i = depth + 1, i + 2
        elif wt.startswith("}}", i):
            depth, i = depth - 1, i + 2
            if depth == 0:
                return wt[m.start():i]
        else:
            i += 1
    return wt[m.start():]


def _dates_in(text, default_year):
    out = []
    text = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", text, flags=re.S)
    for tpl in re.findall(r"\{\{\s*(?:start|end|start and end|birth|dts)[a-z ]*\|([^}]*)\}\}", text, re.I):
        nums = [int(x) for x in re.findall(r"(?<![=\w])(\d{1,4})(?![\w=])", tpl)]
        for i in range(0, len(nums) - 2, 3):
            y, mo, d = nums[i:i + 3]
            if 1800 < y < 2100 and 1 <= mo <= 12 and 1 <= d <= 31:
                out.append(date(y, mo, d))
    for d, mon, y in re.findall(r"(\d{1,2}) ([A-Z][a-z]+)(?:,? (\d{4}))?", text):
        if mon.lower() in MONTHS:
            out.append(_safe(int(y) if y else default_year, MONTHS[mon.lower()], int(d)))
    for mon, d, y in re.findall(r"([A-Z][a-z]+) (\d{1,2}),? (\d{4})", text):
        if mon.lower() in MONTHS:
            out.append(_safe(int(y), MONTHS[mon.lower()], int(d)))
    return [d for d in out if d]


def _safe(y, m, d):
    try:
        return date(y, m, d)
    except ValueError:
        return None


EDITION_INFOBOX = re.compile(r"\{\{\s*Infobox (football (tournament|league|match)|sports? award|award|"
                             r"international football competition)", re.I)


def _range(yrs):
    """Plausible end-date range for an edition labelled with years yrs."""
    if yrs[0] == yrs[1]:
        return date(yrs[0], 1, 1), date(yrs[1] + 1, 2, 28)  # Dec/Jan ceremonies of a year's award
    return date(yrs[0], 7, 1), date(yrs[1], 8, 31)


def candidate_titles(comp, target, label):
    """Articles that may date an entry: the linked one, then '<label> <competition>'."""
    yrs = label_years(label) or label_years(target)
    out = [target] if re.search(r"\d{4}", target) else []
    lab = re.sub(r"[−-]", "–", label.strip())
    if yrs and re.fullmatch(r"\d{4}(–\d{2,4})?", lab):
        out.append(f"{lab} {comp}")
    return out


def final_links(wt, yrs):
    """Links to '<year> ... Final' articles for the edition's end year."""
    return [t for t in re.findall(r"\[\[([^\]|#]+)", wt)
            if re.search(r"\bfinals?$", t.strip(), re.I) and str(yrs[1]) in t]


def _date_of(title, yrs, allow_body=True):
    """(date, url, method) from one article, or None."""
    wt, url, _ = wiki_wikitext(title)
    if not wt:
        return None
    lo, hi = _range(yrs)
    box = _infobox_text(wt)
    if box and re.match(r"\{\{\s*Infobox football club season", box, re.I):
        return "club season"
    if box and not EDITION_INFOBOX.match(box):
        return None
    # A single-year edition can be played the next summer (Euro 2020 / Copa América 2020 in
    # 2021, AFCON 2023 in 2024): the infobox may date it up to 31 Aug of the following year.
    box_hi = date(yrs[1] + 1, 8, 31) if yrs[0] == yrs[1] else hi
    ds = [d for d in _dates_in(box, yrs[1]) if lo <= d <= box_hi]
    if ds:
        return max(ds), url, "infobox"
    for f in final_links(wt, yrs):
        got = _date_of(f, yrs, allow_body=False)
        if got and got != "club season":
            return got[0], got[1], "final article"
    text = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", wt, flags=re.S)
    for line in text.splitlines():
        if re.match(r"^\|\s*'*Final'*\s*\|\|", line):
            ds = [d for d in _dates_in(line, yrs[1]) if lo <= d <= hi]
            if ds:
                return max(ds), url, "final table row"
    if allow_body:
        ds = [d for d in _dates_in(text, yrs[1]) if lo <= d <= hi]
        if ds:
            return max(ds), url, "latest date in article"
    return None


def prefetch_entries(entries):
    """Pre-load (in batches) every article entry_date may read for (comp, target, label) entries."""
    first = {t for c, tg, lab in entries for t in candidate_titles(c, tg, lab)}
    wiki_prefetch(first)
    finals = set()
    for c, tg, lab in entries:
        yrs = label_years(lab) or label_years(tg)
        for t in candidate_titles(c, tg, lab):
            wt, _, _ = wiki_wikitext(t)
            if wt and yrs:
                finals.update(final_links(wt, yrs))
    wiki_prefetch(finals)


_date_cache = {}


def entry_date(comp, target, label):
    """(date, url, method) for the event an honours entry links to; (None, url, reason) if undated."""
    key = (comp, target, label)
    if key not in _date_cache:
        yrs = label_years(label) or label_years(target)
        result = (None, None, "no year in label")
        for i, t in enumerate(candidate_titles(comp, target, label) if yrs else []):
            got = _date_of(t, yrs)
            if got == "club season":
                result = (None, None, "club season article")
                continue
            if got:
                result = got
                break
            if i == 0 or result[2] != "club season article":
                result = (None, None, "no date found in linked article")
        _date_cache[key] = result
    return _date_cache[key]


SKIP_GROUP = re.compile(r"record|order|achievement|manager|coach|overall|decoration|special", re.I)


def classify(entries):
    """Split honours entries into (trophies, awards); drop youth, managerial and non-football
    honours, and entries that name no year (links to a list, not to an edition)."""
    trophies, awards = [], []
    for group, comp, target, label, result in entries:
        if YOUTH.search(group) or YOUTH.search(comp) or SKIP_GROUP.search(group):
            continue
        if not (label_years(label) or label_years(target)):
            continue
        if re.search(r"individual|award", group, re.I):
            if not EXCLUDED_AWARD.search(comp) and not EXCLUDED_AWARD.search(target):
                awards.append((comp, target, label))
        elif not EXCLUDED_AWARD.search(group):
            trophies.append((comp, target, label, result))
    return trophies, awards
