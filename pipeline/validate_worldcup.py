"""Cross-check the StatsBomb World Cup match records in data/features/logs/matches.csv against the
Fjelstul World Cup Database (github.com/jfjelstul/worldcup, CC BY-SA 4.0): appearance, minutes,
goals, first yellows and sendings-off per nominee per match. Prints every disagreement.
Run after build_features.py.
"""
import csv
from collections import defaultdict
from pathlib import Path

from fetch import github_raw
from players import norm

REPO = "jfjelstul/worldcup"
LOG = Path(__file__).parent.parent / "data" / "features" / "logs" / "matches.csv"
MINUTE_TOLERANCE = 2  # StatsBomb clocks seconds; Fjelstul records whole minutes


def table(name):
    text, _, _ = github_raw(REPO, f"data-csv/{name}.csv")
    return list(csv.DictReader(text.splitlines()))


def fjelstul_players():
    """{(date, team, player_id): stats} plus {(date, team): [(player_id, full, family, given)]}."""
    def key_of(r, team="team_name"):
        return r["match_date"], norm(r[team]), r["player_id"]

    extra_time = {m["match_id"]: m["extra_time"] == "1" for m in table("matches")}
    stats, roster = defaultdict(lambda: defaultdict(int)), defaultdict(list)
    on, off = {}, {}
    for r in table("player_appearances"):
        key = key_of(r)
        given = "" if r["given_name"] == "not applicable" else r["given_name"]
        roster[key[:2]].append((r["player_id"], norm(f"{given} {r['family_name']}"),
                                norm(r["family_name"]), norm(given)))
        stats[key]["apps"] = 1
        stats[key]["end"] = 120 if extra_time[r["match_id"]] else 90
        if r["starter"] == "1":
            on[key] = 0
    for r in table("substitutions"):
        (on if r["coming_on"] == "1" else off)[key_of(r)] = int(r["minute_regulation"])
    for r in table("bookings"):
        key = key_of(r)
        if r["yellow_card"] == "1" and r["second_yellow_card"] == "0":
            stats[key]["yellow"] += 1
        if r["sending_off"] == "1":
            stats[key]["red"] += 1
            off[key] = min(off.get(key, 999), int(r["minute_regulation"]))
    for r in table("goals"):
        if r["own_goal"] == "0":
            stats[key_of(r, "player_team_name")]["goals"] += 1
    for key, s in stats.items():
        s["minutes"] = max(0, min(off.get(key, s["end"]), s["end"]) - on[key]) if key in on else 0
    return stats, roster


def find(roster, date, team, name):
    """Fjelstul player_id for a nominee who played in the match: full name, else the name is the
    family name alone ('Neymar'), else same first given name and family name ('Kevin De Bruyne').
    None if he did not play (Fjelstul lists only players who took the field) or is ambiguous."""
    players = roster.get((date, norm(team)), [])
    n = norm(name)
    hits = [p for p, full, _, _ in players if full == n] or \
           [p for p, _, fam, _ in players if fam == n] or \
           [p for p, _, fam, given in players
            if fam and given and n.endswith(" " + fam) and n.split()[0] == given.split()[0]]
    return hits[0] if len(hits) == 1 else None


def main():
    stats, roster = fjelstul_players()
    rows = [r for r in csv.DictReader(open(LOG, encoding="utf-8"))
            if r["competition"] == "FIFA World Cup" and r["in_squad"] == "True"]
    checked, problems = 0, []
    for r in rows:
        pid = find(roster, r["date"], r["team"], r["name"])
        f = stats[(r["date"], norm(r["team"]), pid)] if pid else defaultdict(int)  # unused sub: all 0
        checked += 1
        for k in ("apps", "minutes", "goals", "yellow", "red"):
            sb = int(float(r[k] or 0))
            tol = MINUTE_TOLERANCE if k == "minutes" else 0
            if abs(sb - f[k]) > tol:
                problems.append(f"{r['date']} {r['team']} {r['name']}: {k} StatsBomb {sb}, Fjelstul {f[k]}")
    print("\n".join(problems))
    print(f"{checked} nominee World Cup matches checked; {len(problems)} disagreements")


if __name__ == "__main__":
    main()
