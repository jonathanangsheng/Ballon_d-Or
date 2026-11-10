"""Step 1: judging window per edition -> data/features/windows.csv.

Ceremony date: the edition's Wikipedia infobox. Voting deadline: a sentence in the same article
("voting was extended to <date>" / "deadline for voting was <date>"); if none, ceremony - 30 days
and flagged as estimated.
"""
import csv
import re
from datetime import date, datetime, timedelta
from pathlib import Path

from fetch import wiki_wikitext

OUT = Path(__file__).parent / "data" / "features" / "windows.csv"
YEARS = [y for y in range(2000, 2027) if y != 2020]
DATE_RE = r"(\d{1,2} [A-Z][a-z]+ \d{4})"


def article_title(year):
    return f"{year} FIFA Ballon d'Or" if 2010 <= year <= 2015 else f"{year} Ballon d'Or"


def parse_ceremony(wikitext):
    infobox = re.search(r"\{\{Infobox.*?\n\}\}", wikitext, re.S).group(0)
    line = re.search(r"^\s*\|\s*date\s*=(.*)$", infobox, re.M).group(1)
    m = re.search(r"\{\{start date\|(\d{4})\|(\d{1,2})\|(\d{1,2})", line, re.I)
    if m:
        return date(*map(int, m.groups()))
    return datetime.strptime(re.search(DATE_RE, line).group(1), "%d %B %Y").date()


def parse_deadline(wikitext):
    text = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", wikitext, flags=re.S)
    for pat in (r"voting was extended to " + DATE_RE, r"deadline for voting was " + DATE_RE):
        m = re.search(pat, text)
        if m:
            return datetime.strptime(m.group(1), "%d %B %Y").date(), m.group(0)
    return None, None


def window(year):
    wikitext, url, _ = wiki_wikitext(article_title(year))
    ceremony = parse_ceremony(wikitext)
    deadline, quote = parse_deadline(wikitext)
    deadline_est = deadline is None
    if deadline_est:
        deadline = ceremony - timedelta(days=30)
    notes = f'Wikipedia: "{quote}"' if quote else "deadline not stated in source; ceremony - 30 days"
    if year < 2022:
        start = date(year, 1, 1)
        end = min(deadline, date(year, 12, 31))  # FIFA years: ceremony next January, cut-off stays in `year`
        end_est = deadline_est
    else:
        start, end, end_est = date(year - 1, 8, 1), date(year, 7, 31), False
    return {
        "year": year, "window_start": start, "window_end": end, "voting_deadline": deadline,
        "ceremony_date": ceremony, "window_end_estimated": str(end_est).lower(),
        "voting_deadline_estimated": str(deadline_est).lower(), "source_url": url, "notes": notes,
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
