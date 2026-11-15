"""Step 1: judging window per edition -> data/features/windows.csv.

Ceremony date: the edition's Wikipedia infobox. Voting deadline: a sentence in the same article
("voting was extended to <date>" / "deadline for voting was <date>"), else a press report in
PRESS_DEADLINES; if none, ceremony - 30 days and flagged as estimated. Season windows (2022 on):
the period the same article states ("from <date> to <date>"), else 1 Aug - 31 Jul.
"""
import csv
import re
from datetime import date, datetime, timedelta
from pathlib import Path

from fetch import wiki_wikitext

OUT = Path(__file__).parent.parent / "data" / "features" / "windows.csv"
YEARS = [y for y in range(2000, 2027) if y != 2020]
DATE_RE = r"(\d{1,2} [A-Z][a-z]+ \d{4})"
ANY_DATE = r"(\d{1,2} [A-Z][a-z]+ \d{4}|[A-Z][a-z]+ \d{1,2}, \d{4})"  # '1 August 2023' or 'August 1, 2023'
WINDOW_RE = (r"(?:period|season)[^.\n]{0,20}?(?:from|starting on) " + ANY_DATE
             + r",? (?:to|and ending(?: on)?) " + ANY_DATE)
# Deadlines reported in the press, citing France Football (its own pages were not reachable).
PRESS_DEADLINES = {
    2026: (date(2026, 9, 28), "voting closed 28 Sep 2026 (foot-africa.com, beinsports.com)"),
}


def article_title(year):
    return f"{year} FIFA Ballon d'Or" if 2010 <= year <= 2015 else f"{year} Ballon d'Or"


def parse_ceremony(wikitext):
    infobox = re.search(r"\{\{Infobox.*?\n\}\}", wikitext, re.S).group(0)
    line = re.search(r"^\s*\|\s*date\s*=(.*)$", infobox, re.M).group(1)
    m = re.search(r"\{\{start date\|(\d{4})\|(\d{1,2})\|(\d{1,2})", line, re.I)
    if m:
        return date(*map(int, m.groups()))
    return datetime.strptime(re.search(DATE_RE, line).group(1), "%d %B %Y").date()


def _plain(wikitext):
    """Text without refs, and with [[target|label]] links reduced to their label."""
    text = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", wikitext, flags=re.S)
    return re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", text)


def _date(s):
    return datetime.strptime(s, "%d %B %Y" if s[0].isdigit() else "%B %d, %Y").date()


def parse_deadline(wikitext):
    text = _plain(wikitext)
    for pat in (r"voting was extended to " + DATE_RE, r"deadline for voting was " + DATE_RE):
        m = re.search(pat, text)
        if m:
            return datetime.strptime(m.group(1), "%d %B %Y").date(), m.group(0)
    return None, None


def parse_window(wikitext, year):
    """(start, end, quote): the first period the article states that can be the season judged
    (starts Jul-Sep of year - 1, ends Jun-Aug of year), so a nomination or loan period is skipped;
    (None, None, None) if none."""
    for m in re.finditer(WINDOW_RE, _plain(wikitext)):
        start, end = map(_date, m.groups())
        if start.year == year - 1 and 7 <= start.month <= 9 and end.year == year and 6 <= end.month <= 8:
            return start, end, m.group(0)
    return None, None, None


def window(year):
    wikitext, url, _ = wiki_wikitext(article_title(year))
    ceremony = parse_ceremony(wikitext)
    deadline, quote = parse_deadline(wikitext)
    notes = [f'Wikipedia: "{quote}"'] if quote else []
    if deadline is None and year in PRESS_DEADLINES:
        deadline, press = PRESS_DEADLINES[year]
        notes.append(press)
    deadline_est = deadline is None
    if deadline_est:
        deadline = ceremony - timedelta(days=30)
        notes.append("deadline not stated in source; ceremony - 30 days")
    if year < 2022:
        start = date(year, 1, 1)
        end = min(deadline, date(year, 12, 31))  # FIFA years: ceremony next January, cut-off stays in `year`
        end_est = deadline_est
    else:
        start, end, wquote = parse_window(wikitext, year)
        end_est = not wquote
        if wquote:
            notes.append(f'window, Wikipedia: "{wquote}"')
        else:
            start, end = date(year - 1, 8, 1), date(year, 7, 31)
            notes.append("no judging period found in source text; 1 Aug - 31 Jul assumed")
    return {
        "year": year, "window_start": start, "window_end": end, "voting_deadline": deadline,
        "ceremony_date": ceremony, "window_end_estimated": str(end_est).lower(),
        "voting_deadline_estimated": str(deadline_est).lower(), "source_url": url, "notes": "; ".join(notes),
    }


def main():
    rows = [window(y) for y in YEARS]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} ({len(rows)} editions)")


if __name__ == "__main__":
    main()
