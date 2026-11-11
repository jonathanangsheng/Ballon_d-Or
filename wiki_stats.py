"""Stats from a player's Wikipedia 'Career statistics' section.

- club_seasons(): apps/goals per club, season and competition column (club table)
- intl_years():  apps/goals per year (international table)
- intl_goal_dates(): the date of every international goal (goal list, in the article or in a
  separate 'List of international goals scored by ...' article); None if the list's length does
  not equal the goal total in the year table
"""
import re
from datetime import date

from fetch import wiki_prefetch, wiki_wikitext
from honours import MONTHS, _dates_in


def _split_top(s, sep):
    """Split on `sep` outside [[...]] and {{...}}."""
    out, depth, cur, i = [], 0, "", 0
    while i < len(s):
        if s.startswith(("[[", "{{"), i):
            depth += 1; cur += s[i:i + 2]; i += 2; continue
        if s.startswith(("]]", "}}"), i):
            depth -= 1; cur += s[i:i + 2]; i += 2; continue
        if depth == 0 and s.startswith(sep, i):
            out.append(cur); cur = ""; i += len(sep); continue
        cur += s[i]; i += 1
    return out + [cur]


def _cell(raw):
    """(attrs, content) of one cell: 'rowspan="2"|text' -> ('rowspan="2"', 'text')."""
    parts = _split_top(raw, "|")
    if len(parts) > 1 and re.search(r"\b(row|col)span|style|align|scope|class", parts[0]):
        return parts[0], "|".join(parts[1:])
    return "", raw


def grid(table):
    """Rows of (is_header, text) with rowspan/colspan expanded."""
    raw_rows = []
    for chunk in re.split(r"\n\|-[^\n]*", table):
        cells = []
        for line in chunk.split("\n"):
            s = line.strip()
            if not s or s.startswith(("{|", "|}", "|+")):
                continue
            if s[0] in "|!":
                sep = "!!" if s[0] == "!" else "||"
                for part in _split_top(s[1:], sep) if sep == "||" else re.split(r"!!|\|\|", s[1:]):
                    cells.append((s[0] == "!",) + _cell(part))
            elif cells:
                h, a, c = cells[-1]
                cells[-1] = (h, a, c + "\n" + s)
        if cells:
            raw_rows.append(cells)
    out, carry = [], {}  # col -> (remaining rows, cell)
    for cells in raw_rows:
        row, col, it = [], 0, iter(cells)
        while True:
            while col in carry:
                n, cell = carry[col]
                row.append(cell)
                carry[col] = (n - 1, cell)
                if n - 1 == 0:
                    del carry[col]
                col += 1
            nxt = next(it, None)
            if nxt is None:
                break
            h, attrs, text = nxt
            rs = int((re.search(r'rowspan\s*=\s*"?(\d+)', attrs) or [0, 1])[1])
            cs = int((re.search(r'colspan\s*=\s*"?(\d+)', attrs) or [0, 1])[1])
            for _ in range(cs):
                row.append((h, text.strip()))
                if rs > 1:
                    carry[col] = (rs - 1, (h, text.strip()))
                col += 1
        out.append(row)
    return out


def plain(text):
    text = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", text, flags=re.S)
    text = re.sub(r"\{\{(efn|refn|sfn|cref|nbsp)[^{}]*(\{\{[^{}]*\}\}[^{}]*)*\}\}", "", text, flags=re.I)
    text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", text)
    return re.sub(r"'''?|<[^>]+>", "", text).strip()


def num(text):
    t = plain(text).replace(",", "")
    return int(t) if re.fullmatch(r"\d+", t) else None


def tables(section):
    return re.findall(r"\{\|.*?\n\|\}", section, re.S)


def stats_section(wt):
    m = re.search(r"^==\s*Career statistics\s*==\s*$(.*?)(?=^==[^=]|\Z)", wt, re.M | re.S)
    return m.group(1) if m else ""


def club_seasons(wt):
    """[{club, season, season_link, cols: {(group, sub): (value, raw)}}] from the club table."""
    sec = stats_section(wt)
    for t in tables(sec):
        if not re.search(r"by club|Club", t.split("\n", 2)[1] if "\n" in t else ""):
            continue
        g = grid(t)
        heads = [r for r in g if r and all(h for h, _ in r)]
        if len(heads) < 2:
            continue
        top, sub = heads[0], heads[1]
        n = len(top)
        labels = [(plain(top[i][1]), plain(sub[i][1]) if i < len(sub) else "") for i in range(n)]
        out = []
        for r in g:
            if len(r) < n or r[1][0] or not re.search(r"\d{4}", plain(r[1][1])):
                continue
            season_raw = r[1][1]
            link = re.search(r"\[\[([^\]|#]+)", season_raw)
            out.append({"club": plain(r[0][1]), "season": plain(season_raw),
                        "season_link": link.group(1).strip() if link else None,
                        "cols": {labels[i]: (num(r[i][1]), r[i][1]) for i in range(2, n)}})
        return out
    return []


def intl_years(wt):
    """{year: (apps, goals)} summed over senior national-team rows of the year table, from the
    article's statistics section or, failing that, its 'List of international goals' article."""
    found = _year_table(stats_section(wt))
    if not found and goal_list_title(wt):
        found = _year_table(wiki_wikitext(goal_list_title(wt))[0] or "")
    return found


def _year_table(sec):
    for t in tables(sec):
        if "by national team and year" not in t and "Year" not in t:
            continue
        g = grid(t)
        heads = []
        for r in g:  # leading all-header rows; two of them when columns are grouped
            if not (r and all(h for h, _ in r)):
                break
            heads.append([plain(c) for _, c in r])
        if not heads:
            continue
        labels = [(heads[0][i], heads[-1][i] if i < len(heads[-1]) else "") for i in range(len(heads[0]))]

        def col(sub):  # the Total group's column if columns are grouped, else the plain one
            hits = [i for i, (grp, s) in enumerate(labels) if s == sub]
            return next((i for i in hits if labels[i][0] == "Total"), hits[-1] if hits else None)
        iy = next((i for i, (grp, _) in enumerate(labels) if grp == "Year"), None)
        ia, ig = col("Apps"), col("Goals")
        if None in (iy, ia, ig):
            continue
        out = {}
        for r in g:
            if len(r) <= max(iy, ia, ig) or r[iy][0]:
                continue
            if re.search(r"\bU-?\d{2}\b|under-\d{2}|olympic", plain(r[0][1]), re.I):
                continue
            y, a, gl = num(r[iy][1]), num(r[ia][1]), num(r[ig][1])
            if y and a is not None and gl is not None:
                pa, pg = out.get(y, (0, 0))
                out[y] = (pa + a, pg + gl)
        return out
    return {}


def _goal_table_dates(text):
    for t in tables(text):
        g = grid(t)
        head = next((r for r in g if r and all(h for h, _ in r)), None)
        if not head:
            continue
        names = [plain(c).lower() for _, c in head]
        if "date" not in names or not any("opponent" in n for n in names):
            continue
        idate = names.index("date")
        dates = []
        for r in g:
            if len(r) <= idate or r[idate][0] or not num(r[0][1]):
                continue
            ds = _dates_in(r[idate][1], 0)
            if not ds or ds[0].year < 1900:
                return None  # a goal row without a readable date: list unusable
            dates.append(ds[0])
        if dates:
            return dates
    return None


def goal_list_title(wt):
    m = re.search(r"\[\[(List of international goals scored by [^\]|#]+)", wt)
    return m.group(1).strip() if m else None


def intl_goal_dates(wt, years=None):
    """(dates, source title or None, reason). Valid only when the list length equals the
    year table's goal total (both cover the same 'updated' period)."""
    years = years if years is not None else intl_years(wt)
    total = sum(g for _, g in years.values())
    if total == 0:
        return ([], None, None) if years else (None, None, "no international year table")
    dates, src = _goal_table_dates(stats_section(wt)), None
    if dates is None and goal_list_title(wt):
        src = goal_list_title(wt)
        lwt, _, _ = wiki_wikitext(src)
        dates = _goal_table_dates(lwt or "")
    if dates is None:
        return None, src, "no dated list of international goals"
    if len(dates) != total:
        return None, src, f"goal list has {len(dates)} goals, year table {total}"
    return dates, src, None


# ---------- club season -> window ----------

EUROPE = re.compile(r"Europe|Continental|UEFA|Champions|CONCACAF|CONMEBOL|AFC|CAF", re.I)
NOT_UCL = re.compile(r"Europa|UEFA Cup|Conference|Super Cup|Intertoto|Club World Cup", re.I)


def _efn_defs(table):
    return {m.group(1).strip(): m.group(2) for m in re.finditer(r"\{\{efn\|name\s*=\s*([^|}]+)\|([^{}]*)\}\}", table)}


def europe_is_ucl(raw, defs):
    """True if the Europe cell's footnote names only the Champions League, False if it names
    another competition, None if there is no footnote to tell."""
    notes = re.findall(r"\{\{efn\|([^{}]*)\}\}", raw)
    text = " ".join(defs.get(re.sub(r"^name\s*=\s*", "", n).strip(), n) if n.startswith("name") and "|" not in n
                    else n for n in notes)
    if not text:
        return None
    if NOT_UCL.search(text):
        return False
    return True if re.search(r"Champions League", text) else None


def season_buckets(rows, defs):
    """Sum one season's table rows into {'league'|'ucl'|'club_other': (apps, goals)}; a bucket is
    None when a column cannot be attributed (Europe cell without a telling footnote)."""
    out = {"league": [0, 0], "ucl": [0, 0], "club_other": [0, 0]}
    known = {"league": True, "ucl": True, "club_other": True}
    for r in rows:
        groups = {}
        for (grp, sub), (v, raw) in r["cols"].items():
            if sub in ("Apps", "Goals"):
                groups.setdefault(grp, {})[sub] = (v, raw)
        for grp, vals in groups.items():
            apps, goals = (vals.get("Apps") or (None, ""))[0], (vals.get("Goals") or (None, ""))[0]
            raw = (vals.get("Apps") or (None, ""))[1]
            if grp == "Total":
                continue
            if grp == "League":
                b = ["league"]
            elif EUROPE.search(grp):
                if apps in (None, 0):
                    b = []  # did not play in Europe that season
                else:
                    u = europe_is_ucl(raw, defs)
                    b = ["ucl"] if u else ["club_other"] if u is False else None
            else:
                b = ["club_other"]
            if b is None:
                known["ucl"] = known["club_other"] = False
                continue
            for k in b:
                out[k][0] += apps or 0
                out[k][1] += goals or 0
    return {k: tuple(v) if known[k] else None for k, v in out.items()}


def club_table_defs(wt):
    sec = stats_section(wt)
    return _efn_defs(sec)


def football_box_dates(wt):
    """Competitive match dates from the {{Football box ...}} templates of a club-season article
    (boxes under a friendlies / pre-season heading are skipped)."""
    out = []
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"^=+\s*(.*?)\s*=+\s*$", wt, re.M)]
    for m in re.finditer(r"\{\{\s*Football box", wt, re.I):
        head = next((h for pos, h in reversed(heads) if pos < m.start()), "")
        if re.search(r"friendl|pre-?season|tour|exhibition", head, re.I):
            continue
        depth, i = 0, m.start()
        while i < len(wt):
            if wt.startswith("{{", i):
                depth, i = depth + 1, i + 2
            elif wt.startswith("}}", i):
                depth, i = depth - 1, i + 2
                if depth == 0:
                    break
            else:
                i += 1
        d = re.search(r"\|\s*date\s*=([^\n|{]*(?:\{\{[^}]*\}\}[^\n|]*)?)", wt[m.start():i])
        ds = _dates_in(d.group(1), 0) if d else []
        out += [x for x in ds[:1] if x.year > 1900]
    return out


def league_season_dates(title):
    from honours import _infobox_text
    wt, url, _ = wiki_wikitext(title)
    if not wt:
        return None, None
    m = re.search(r"\|\s*dates\s*=([^\n]*)", _infobox_text(wt))
    if not m:
        return None, url
    yrs = [int(y) for y in re.findall(r"\d{4}", title)[:1]]
    ds = [d for d in _dates_in(m.group(1), yrs[0] + 1 if yrs else 0) if d.year > 1900]
    return (min(ds), max(ds)) if len(ds) >= 2 else None, url
