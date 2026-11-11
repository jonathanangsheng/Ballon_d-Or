"""Extend data/ballon_dor 2000-2015 beyond the top 10, from the same Wikipedia ranking tables.

- 2010-2015: the full 23-player FIFA shortlist (percent of vote in `points`)
- 2008-2009: the full 30-player shortlist
- 2000-2007: every player who received votes, up to rank 30 (ties at 30th kept); nominees
  with no votes have no rank and are left out

Existing rows are kept exactly as they are. New rows follow the README's rules: age on the
ceremony day from the infobox birth date, first infobox position grouped into four, the later
club when two are listed, club names spelled as in existing rows for the same club.
"""
import csv
import re
from datetime import date

import wiki_stats as ws
from build_windows import article_title
from fetch import wiki_prefetch, wiki_wikitext
from players import BD_DIR, _infobox, _param, norm

YEARS = range(2000, 2016)
COLS = ["rank", "name", "age", "country", "position", "club", "points"]


def cutoff(year):
    return 30 if year < 2010 else 23


def ranking(year):
    """Men's ranking rows in document order, stopping when a table restarts at rank 1."""
    wt, _, _ = wiki_wikitext(article_title(year))
    rows, last = [], 0
    for t in ws.tables(wt):
        g = ws.grid(t)
        head = [ws.plain(c).lower() for _, c in g[0]] if g else []
        if not any("player" in h for h in head):
            continue
        ip = next(i for i, h in enumerate(head) if "player" in h)
        ic = next((i for i, h in enumerate(head) if "club" in h), None)
        inat = next((i for i, h in enumerate(head) if "nation" in h), None)
        ipts = next((i for k in ("total", "points", "percent") for i, h in enumerate(head) if h.startswith(k)), None)
        body = []
        for r in g:
            m = re.match(r"^=?(\d+)", ws.plain(r[0][1]))
            if m and len(r) > max(ip, ic or 0, inat or 0, ipts or 0):
                body.append({"rank": int(m.group(1)), "raw": r, "ip": ip, "ic": ic, "inat": inat, "ipts": ipts})
        if not body:
            continue
        if body[0]["rank"] < last:
            break  # next award's table (women, coaches)
        rows += body
        last = body[-1]["rank"]
    return rows


def player_link(cell):
    m = re.search(r"\[\[([^\]|#]+)(?:\|([^\]]*))?\]\]", cell)
    s = re.search(r"\{\{sortname\|([^|}]+)\|([^|}]*)(?:\|([^|}]+))?", cell, re.I)
    if s:
        first, last, link = (x.strip() if x else x for x in s.groups())
        name = f"{first} {last}".strip()
        return (link if link and "=" not in link else name), name
    return (m.group(1).strip(), (m.group(2) or m.group(1)).strip()) if m else (None, ws.plain(cell))


def country_of(cell, codes):
    m = re.search(r"\{\{\s*(?:flag|flagu|flagicon|fb|fbw|flagathlete)\s*\|\s*([^|}]+)", cell, re.I)
    if not m:
        return ws.plain(cell)
    v = m.group(1).strip()
    return codes.get(v, v) if re.fullmatch(r"[A-Z]{3}", v) else v


def club_of(cell, known):
    links = re.findall(r"\[\[([^\]|#]+)(?:\|([^\]]*))?\]\]", cell)
    if not links:
        return ws.plain(cell)
    target, label = links[-1]  # two clubs listed for the year: the later one
    return known.get(target.strip(), (label or target).strip())


def age_on(wt, day):
    m = re.search(r"\{\{\s*birth[ -]date(?: and age)?\s*\|([^}]*)\}\}", _param(wt, "birth_date"), re.I)  # first infobox with a birth date
    nums = [int(p) for p in (m.group(1).split("|") if m else []) if p.strip().isdigit()]
    if len(nums) < 3:
        return None
    b = date(*nums[:3])
    return day.year - b.year - ((day.month, day.day) < (b.month, b.day))


def position_of(wt):
    first = ws.plain(re.split(r"<br\s*/?>|,|/|\n|\band\b", _param(_infobox(wt), "position"))[0]).lower()
    if "goalkeeper" in first:
        return "goalkeeper"
    if re.search(r"back|defender|sweeper|libero", first):
        return "defender"
    if "midfield" in first:
        return "midfielder"
    if re.search(r"striker|forward|winger", first):
        return "forward"
    return None


def main():
    ceremony = {int(r["year"]): date.fromisoformat(r["ceremony_date"])
                for r in csv.DictReader(open(BD_DIR.parent / "features" / "windows.csv", encoding="utf-8"))}
    tables = {y: ranking(y) for y in YEARS}
    # FIFA codes ({{fb|ARG}}) -> the name the template displays, from Template:Country data XXX
    codes = {re.search(r"\{\{\s*fbw?\s*\|\s*([A-Z]{3})", r["raw"][r["inat"]][1]).group(1)
             for rows in tables.values() for r in rows
             if r["inat"] is not None and re.search(r"\{\{\s*fbw?\s*\|\s*[A-Z]{3}", r["raw"][r["inat"]][1])}
    wiki_prefetch({f"Template:Country data {c}" for c in codes})
    code_name = {}
    for c in codes:
        t, _, _ = wiki_wikitext(f"Template:Country data {c}")
        a = re.search(r"\|\s*alias\s*=\s*([^\n|]+)", t or "")
        if a:
            code_name[c] = a.group(1).strip()
    existing = {y: list(csv.DictReader(open(BD_DIR / f"{y}.csv", encoding="utf-8"))) for y in YEARS}
    # club spelling used by existing rows, keyed by the club link in the same article row
    known = {}
    for y, rows in tables.items():
        names = {norm(r["name"]): r["club"] for r in existing[y]}
        for r in rows:
            _, label = player_link(r["raw"][r["ip"]][1])
            if norm(label) in names and r["ic"] is not None:
                links = re.findall(r"\[\[([^\]|#]+)", r["raw"][r["ic"]][1])
                if links:
                    known.setdefault(links[-1].strip(), names[norm(label)])
    new_titles = {player_link(r["raw"][r["ip"]][1])[0] for y in YEARS for r in tables[y]
                  if r["rank"] <= cutoff(y)}
    wiki_prefetch(new_titles)

    for y in YEARS:
        have = {norm(r["name"]) for r in existing[y]}
        added, problems = [], []
        for r in tables[y]:
            if r["rank"] > cutoff(y):
                continue
            title, label = player_link(r["raw"][r["ip"]][1])
            if norm(label) in have:
                continue
            pts = ws.plain(r["raw"][r["ipts"]][1]).rstrip("%") if r["ipts"] is not None else ""
            if y < 2008 and pts in ("", "0"):
                continue  # 2000-2007: 0-point nominees have no real rank; 2008+ lists are complete
            wt, _, _ = wiki_wikitext(title) if title else (None, None, None)
            row = {"rank": r["rank"], "name": label,
                   "age": age_on(wt, ceremony[y]) if wt else None,
                   "country": country_of(r["raw"][r["inat"]][1], code_name) if r["inat"] is not None else None,
                   "position": position_of(wt) if wt else None,
                   "club": club_of(r["raw"][r["ic"]][1], known) if r["ic"] is not None else None,
                   "points": pts}
            if None in row.values() or "" in row.values():
                problems.append(row)
            added.append(row)
        if problems:
            raise SystemExit(f"{y}: incomplete new rows {problems}")
        with open(BD_DIR / f"{y}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
            w.writeheader()
            w.writerows(existing[y])
            w.writerows(sorted(added, key=lambda r: r["rank"]))
        print(f"{y}: {len(existing[y])} existing + {len(added)} new = {len(existing[y]) + len(added)} rows")


if __name__ == "__main__":
    main()
