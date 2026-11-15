"""Cross-check data/ballon_dor 2000-2009 (from Wikipedia) against RSSSF's per-edition vote tables
(rsssf.org/miscellaneous/europa-poyYY.html, copying permitted with acknowledgement to the RSSSF):
every ranked player's rank and points. Prints every disagreement.
"""
import csv
import re

from fetch import web_page
from players import BD_DIR as BD, norm

URL = "https://www.rsssf.org/miscellaneous/europa-poy{:02d}.html"
YEARS = range(2000, 2010)


def rsssf_table(year):
    """[(rank, name, nickname, country, points)] in page order; tied rows inherit the rank above.
    points is None when the Total column cannot be read, so the row shows up as a disagreement."""
    html, _ = web_page(URL.format(year % 100))
    lines = re.sub(r"<[^>]+>", "", html).splitlines()
    head = next(i for i, l in enumerate(lines) if l.startswith("Pos") and "Total" in l)
    cols = {c: lines[head].index(c) for c in ("Player", "Country", "Club")}
    total_end = lines[head].index("Total") + len("Total")  # points are right-aligned under it
    rows, rank = [], None
    for line in lines[head + 2:]:
        if not line.strip():
            break
        pos = line[:cols["Player"]].strip().rstrip(".")
        if pos and not pos.isdigit():
            continue  # not a ranking row
        rank = int(pos) if pos else rank
        player = line[cols["Player"]:cols["Country"]].strip()
        nick = re.search(r'"([^"]+)"', player)
        total = (line[cols["Club"]:total_end + 1].split() or [""])[-1]
        points = int(total) if total.isdigit() else None
        rows.append((rank, norm(player.replace('"', "")), norm(nick.group(1)) if nick else None,
                     norm(line[cols["Country"]:cols["Club"]]), points))
    return rows


def match(ours, theirs):
    """Index into theirs for one of our rows: full name or nickname; else, same country and no
    other nickname, our name's words all in theirs ('Adriano' in 'Adriano Ribeiro Leite'); else
    the same surname ('Cesc Fàbregas' / 'Francesc Fabregas'). None unless unique."""
    n, country = norm(ours["name"]), norm(ours["country"])
    pool = [(i, t) for i, t in enumerate(theirs) if t[3] == country and not t[2]]
    hits = [i for i, t in enumerate(theirs) if n in (t[1], t[2])] or \
           [i for i, t in pool if set(n.split()) <= set(t[1].split())] or \
           [i for i, t in pool if t[1].split()[-1] == n.split()[-1]]
    return hits[0] if len(hits) == 1 else None


def main():
    problems, checked = [], 0
    for year in YEARS:
        ours = list(csv.DictReader(open(BD / f"{year}.csv", encoding="utf-8")))
        theirs = rsssf_table(year)
        used = set()
        for r in ours:
            i = match(r, theirs)
            if i is None:
                if float(r["points"]) > 0:  # players with no votes are not in RSSSF's table
                    problems.append(f"{year} {r['name']}: not found in RSSSF table")
                continue
            used.add(i)
            checked += 1
            rank, _, _, _, points = theirs[i]
            if int(r["rank"]) != rank or float(r["points"]) != points:
                problems.append(f"{year} {r['name']}: ours rank {r['rank']} / {r['points']} pts, "
                                f"RSSSF rank {rank} / {points} pts")
        cutoff = max(int(r["rank"]) for r in ours)
        problems += [f"{year} RSSSF rank {t[0]} '{t[1]}' ({t[4]} pts): not in our file"
                     for i, t in enumerate(theirs) if i not in used and t[0] <= cutoff]
    print("\n".join(problems))
    print(f"{checked} ranked players checked over {len(YEARS)} editions; {len(problems)} disagreements")


if __name__ == "__main__":
    main()
