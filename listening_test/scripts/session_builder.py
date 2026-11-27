#!/usr/bin/env python3
"""Build balanced listening sessions (one JSON file per session) for hit/index.html.

Input : config/design.json and a clip manifest CSV with columns  tile,system,file
        (systems IDEAL, OURS, N2N, DUALCOSINE, NOBAKE for every tile in the pool, plus CRIPPLED for the gold
        tiles; training tiles are named  train01.. ; trapping clips are  trap01..  with an expected rating column
        'expected' in  clips_extra.csv  (tile=trap01, system=TRAP, file, expected)).
Output: sessions/sNNN.json  with an ordered item list. Deterministic for a given --seed.

    python3 scripts/session_builder.py --manifest manifest.csv --n-sessions 60 --out sessions/ --base-url https://HOST/clips
"""
import argparse, csv, json, pathlib, random

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load_design():
    return json.loads((ROOT / "config" / "design.json").read_text())

def read_manifest(path):
    rows = list(csv.DictReader(open(path, newline="")))
    return {(r["tile"], r["system"]): r["file"] for r in rows}, rows

def build(design, manifest, n_sessions, seed, base_url="clips", trap_expected=None):
    trap_expected = trap_expected or {}
    rng = random.Random(seed)
    systems = design["systems"]; ref = design["reference_system"]
    K = design["tiles_per_listener"]
    pool = sorted({t for (t, s) in manifest if s == ref and not t.startswith(("train", "trap"))})
    if len(pool) < K:
        raise ValueError(f"tile pool {len(pool)} smaller than tiles_per_listener {K}")
    train = sorted(t for (t, s) in manifest if t.startswith("train") and s == ref)
    traps = sorted(t for (t, s) in manifest if s == "TRAP")
    for t in pool:
        for s in systems:
            if (t, s) not in manifest:
                raise ValueError(f"manifest lacks {t}/{s}")
    url = lambda t, s: f"{base_url}/{manifest[(t, s)]}"
    # balanced tile usage: cycle through shuffled copies of the pool
    cycle, sessions = [], []
    for k in range(n_sessions):
        chosen = []
        while len(chosen) < K:
            if not cycle:
                cycle = pool[:]; rng.shuffle(cycle)
            c = cycle.pop()
            if c not in chosen: chosen.append(c)
            else: cycle.insert(0, c)
        items = []
        for t in chosen:
            for s in systems:
                items.append({"type": "dcr", "tile": t, "system": s, "ref": url(t, ref), "test": url(t, s), "expected": None})
        # explicit gold: strongly degraded clips on two of the chosen tiles (expected rating 1, tolerance in design)
        gold_tiles = rng.sample(chosen, 2)
        for t in gold_tiles:
            g = design["gold_extra"]
            if (t, g) in manifest:
                items.append({"type": "gold", "tile": t, "system": g, "ref": url(t, ref), "test": url(t, g), "expected": 1})
        for t in rng.sample(traps, min(design["trapping_items"], len(traps))):
            exp = int(trap_expected[t])
            items.append({"type": "trap", "tile": t, "system": "TRAP", "ref": url(chosen[0], ref), "test": url(t, "TRAP"), "expected": exp})
        rng.shuffle(items)
        # avoid showing the same tile twice in a row where possible (greedy repair pass)
        for i in range(1, len(items)):
            if items[i]["tile"] == items[i - 1]["tile"]:
                for j in range(i + 1, len(items)):
                    nxt = items[i + 1]["tile"] if i + 1 < len(items) else None
                    if items[j]["tile"] != items[i - 1]["tile"] and items[j]["tile"] != nxt:
                        items[i], items[j] = items[j], items[i]
                        break
        # A/B forced-choice: OURS vs N2N on the same tiles, left/right counterbalanced
        a, b = design["ab_pair"]
        ab = []
        sides = [True, False] * (design["ab_trials_per_listener"] // 2 + 1)
        rng.shuffle(sides)
        for t, flip in zip(rng.sample(chosen, design["ab_trials_per_listener"]), sides):
            first, second = (a, b) if flip else (b, a)
            ab.append({"type": "ab", "tile": t, "first": first, "second": second, "a_url": url(t, first), "b_url": url(t, second)})
        training = [{"type": "train", "tile": t, "system": systems[i % len(systems)], "ref": url(t, ref), "test": url(t, systems[i % len(systems)])}
                    for i, t in enumerate(train[: design["training_clips"]])]
        sessions.append({"session": k, "seed": seed, "training": training, "dcr": items, "ab": ab})
    return sessions

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--extra", help="CSV tile,system,file,expected for trapping clips")
    ap.add_argument("--n-sessions", type=int, default=60)
    ap.add_argument("--seed", type=int, default=20261118)
    ap.add_argument("--base-url", default="clips")
    ap.add_argument("--out", default="sessions")
    a = ap.parse_args()
    manifest, _ = read_manifest(a.manifest)
    trap_expected = {}
    if a.extra:
        for r in csv.DictReader(open(a.extra, newline="")):
            manifest[(r["tile"], "TRAP")] = r["file"]; trap_expected[r["tile"]] = r["expected"]
    sessions = build(load_design(), manifest, a.n_sessions, a.seed, a.base_url, trap_expected)
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    for s in sessions:
        (out / f"s{s['session']:03d}.json").write_text(json.dumps(s, indent=1))
    print(f"wrote {len(sessions)} sessions to {out}")

if __name__ == "__main__":
    main()
