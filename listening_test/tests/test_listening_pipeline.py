import csv, json, pathlib, random, sys
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import session_builder as sb, analyze_ratings as ar, cost_model as cm, power_analysis as pa

DESIGN = sb.load_design()

def make_manifest(n_tiles=24):
    m = {}
    for i in range(n_tiles):
        t = f"tile{i:02d}"
        for s in DESIGN["systems"] + [DESIGN["gold_extra"]]:
            m[(t, s)] = f"{t}_{s.lower()}.wav"
    for i in range(5):
        for s in DESIGN["systems"]:
            m[(f"train{i:02d}", s)] = f"train{i:02d}_{s.lower()}.wav"
    for i in range(4):
        m[(f"trap{i:02d}", "TRAP")] = f"trap{i:02d}.wav"
    return m, {f"trap{i:02d}": i % 5 + 1 for i in range(4)}

def test_sessions_balanced_and_complete():
    m, te = make_manifest()
    ss = sb.build(DESIGN, m, 48, seed=1, trap_expected=te)
    usage = {}
    for s in ss:
        tiles = {i["tile"] for i in s["dcr"] if i["type"] == "dcr"}
        assert len(tiles) == DESIGN["tiles_per_listener"]
        assert sum(i["type"] == "dcr" for i in s["dcr"]) == len(tiles) * len(DESIGN["systems"])
        assert sum(i["type"] == "gold" for i in s["dcr"]) == 2
        assert sum(i["type"] == "trap" for i in s["dcr"]) == DESIGN["trapping_items"]
        assert len(s["ab"]) == DESIGN["ab_trials_per_listener"] and len(s["training"]) == DESIGN["training_clips"]
        firsts = [a["first"] for a in s["ab"]]
        assert 2 <= firsts.count("OURS") <= 6          # left/right counterbalanced
        for t in tiles: usage[t] = usage.get(t, 0) + 1
    assert max(usage.values()) - min(usage.values()) <= 2   # near-uniform tile usage

def test_sessions_deterministic():
    m, te = make_manifest()
    a = sb.build(DESIGN, m, 5, seed=7, trap_expected=te); b = sb.build(DESIGN, m, 5, seed=7, trap_expected=te)
    assert json.dumps(a) == json.dumps(b)

def synth_rows(n_listeners=40, effect=0.6, seed=3, cheaters=3):
    rng = np.random.default_rng(seed); m, te = make_manifest(); rows = []
    base = {"IDEAL": 4.8, "OURS": 4.2, "N2N": 4.2 - effect, "DUALCOSINE": 2.5, "NOBAKE": 1.8}
    tile_eff = rng.normal(0, 0.3, 24)
    sess = sb.build(DESIGN, m, n_listeners, seed=5, trap_expected=te)
    for li, s in enumerate(sess):
        cheat = li < cheaters
        for it in s["dcr"]:
            if it["type"] == "dcr":
                mu = base[it["system"]] + tile_eff[int(it["tile"][4:])]
                r = rng.integers(1, 6) if cheat else int(np.clip(round(mu + rng.normal(0, 0.7)), 1, 5))
            else:
                r = rng.integers(1, 6) if cheat else int(np.clip(it["expected"] + rng.integers(-1, 2), 1, 5))
            rows.append({"listener": f"l{li}", "session": li, "type": it["type"], "tile": it["tile"], "system": it["system"], "rating": float(r), "expected": float(it["expected"]) if it["expected"] else None, "first": "", "second": "", "choice": ""})
        for a in s["ab"]:
            p_ours = 0.5 if cheat else 0.5 + 0.2
            pick_ours = rng.random() < p_ours
            ch = "first" if (a["first"] == "OURS") == pick_ours else "second"
            rows.append({"listener": f"l{li}", "session": li, "type": "ab", "tile": a["tile"], "system": "", "rating": None, "expected": None, "first": a["first"], "second": a["second"], "choice": ch})
    return rows

def test_exclusions_remove_random_raters():
    rows = synth_rows()
    ok, rep = ar.eligible_listeners(rows)
    assert all(f"l{i}" not in ok for i in range(3))
    assert len(ok) >= 30

def test_contrast_detects_true_effect_and_ab_direction():
    rows = synth_rows(n_listeners=60, effect=0.6)
    ok, _ = ar.eligible_listeners(rows)
    cells = ar.cell_table(rows, ok, DESIGN["systems"])
    c = ar.contrast(cells, "OURS", "N2N")
    assert c["diff"] > 0.3 and c["p"] < 0.05
    ab = ar.ab_analysis(rows, ok, DESIGN["ab_pair"])
    assert ab["mean_share"] > 0.55
    txt = ar.report(rows)
    assert "OURS - NOBAKE" in txt and "Holm" in txt

def test_null_effect_not_rejected_most_of_the_time():
    rej = 0
    for seed in range(20):
        rows = synth_rows(n_listeners=40, effect=0.0, seed=100 + seed, cheaters=0)
        ok, _ = ar.eligible_listeners(rows)
        cells = ar.cell_table(rows, ok, DESIGN["systems"])
        rej += ar.contrast(cells, "OURS", "N2N")["p"] < 0.05
    assert rej <= 5

def test_holm_monotone():
    adj = ar.holm(np.array([0.01, 0.04, 0.03]))
    assert adj[0] == 0.03 and adj[2] <= adj[1] + 1e-12 and (adj <= 1).all()

def test_pay_is_above_german_minimum_wage():
    P = DESIGN["pay"]
    floor = P["german_min_wage_eur_per_hour_2026"] * P["ecb_gbp_per_eur_2026_11_17"]
    assert P["hourly_gbp"] > floor
    m, _ = cm.session_minutes()
    assert cm.reward(m, P["hourly_gbp"]) / (m / 60) >= floor
    s = cm.scenario(60)
    assert s["corp"] > s["acad"] > s["rewards"]

def test_power_type1_near_nominal():
    rng = np.random.default_rng(1)
    t1 = pa.power(60, 24, 8, 0.0, 0.3, 0.35, 0.8, 400, rng)
    assert 0.02 <= t1 <= 0.09
