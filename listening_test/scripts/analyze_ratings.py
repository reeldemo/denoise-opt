#!/usr/bin/env python3
"""Pre-specified analysis of the DenoiseOpt listening test (see PLAN.md section 8).

Input  ratings.csv (one row per answer): listener,session,type,tile,system,rating,expected,first,second,choice
         type = dcr | gold | trap | ab ; for ab rows `choice` in {first, second, none}; rating empty.
       rblend.csv (optional): tile,system,rblend   (objective score of the same clip)
Output Markdown report on stdout / --out.

Pre-specified rules (frozen before launch):
 * eligible listener = fewer than 2 failed gold/trap items AND mean rating of the hidden reference (IDEAL) >= 4
   (tolerance +-1 as in the P.808 toolkit);  headphone screening is a precondition handled before the main study.
 * confirmatory DCR contrasts: OURS-N2N, OURS-DUALCOSINE, OURS-NOBAKE, two-way cluster-robust t (listeners x tiles),
   Holm correction over the three p values, alpha = 0.05;  A/B: share of listeners' decisive answers for OURS,
   one-sample t test of listener-level shares against 0.5.
 * exploratory: Spearman correlation between tile x system mean DCR and R_blend.
"""
import argparse, csv, json, pathlib
import numpy as np
from scipy import stats

ROOT = pathlib.Path(__file__).resolve().parent.parent
DESIGN = json.loads((ROOT / "config" / "design.json").read_text())

def read_csv(path):
    rows = list(csv.DictReader(open(path, newline="")))
    for r in rows:
        for k in ("rating", "expected"):
            r[k] = float(r[k]) if r.get(k) not in (None, "") else None
    return rows

def eligible_listeners(rows, design=DESIGN):
    tol = design["exclusion"]["gold_tolerance"]; maxfail = design["exclusion"]["max_failed_attention_items"]
    ref = design["reference_system"]
    by = {}
    for r in rows:
        by.setdefault(r["listener"], []).append(r)
    ok, report = [], {}
    for l, rs in by.items():
        fails = sum(1 for r in rs if r["type"] in ("gold", "trap") and r["rating"] is not None and abs(r["rating"] - r["expected"]) > tol)
        ideal = [r["rating"] for r in rs if r["type"] == "dcr" and r["system"] == ref and r["rating"] is not None]
        mean_ref = float(np.mean(ideal)) if ideal else float("nan")
        good = fails <= maxfail and ideal and mean_ref >= 5 - tol
        report[l] = {"failed_attention": fails, "mean_hidden_reference": mean_ref, "eligible": bool(good)}
        if good: ok.append(l)
    return ok, report

def cell_table(rows, listeners, systems):
    """listener x tile x system -> rating (mean if repeated)."""
    lset = set(listeners); acc = {}
    for r in rows:
        if r["type"] == "dcr" and r["listener"] in lset and r["system"] in systems and r["rating"] is not None:
            acc.setdefault((r["listener"], r["tile"], r["system"]), []).append(r["rating"])
    return {k: float(np.mean(v)) for k, v in acc.items()}

def cgm(d, li, ti):
    d = np.asarray(d, float); n = d.size
    beta = d.mean(); r = d - beta
    L, T = li.max() + 1, ti.max() + 1
    v_l = (np.bincount(li, weights=r, minlength=L) ** 2).sum() / n ** 2
    v_t = (np.bincount(ti, weights=r, minlength=T) ** 2).sum() / n ** 2
    v = v_l + v_t - (r ** 2).sum() / n ** 2
    if v <= 0: v = max(v_l, v_t)
    t = beta / np.sqrt(v); df = max(min(L, T) - 1, 1)
    return beta, np.sqrt(v), t, df, 2 * stats.t.sf(abs(t), df)

def contrast(cells, a, b):
    keys = sorted({(l, t) for (l, t, s) in cells if (l, t, a) in cells and (l, t, b) in cells})
    if len(keys) < 3: return None
    ls = {l: i for i, l in enumerate(sorted({k[0] for k in keys}))}
    ts = {t: i for i, t in enumerate(sorted({k[1] for k in keys}))}
    d = [cells[(l, t, a)] - cells[(l, t, b)] for l, t in keys]
    li = np.array([ls[l] for l, _ in keys]); ti = np.array([ts[t] for _, t in keys])
    beta, se, t, df, p = cgm(d, li, ti)
    return {"a": a, "b": b, "diff": beta, "se": se, "t": t, "df": df, "p": p,
            "ci": (beta - stats.t.ppf(0.975, df) * se, beta + stats.t.ppf(0.975, df) * se), "n_pairs": len(keys),
            "n_listeners": len(ls), "n_tiles": len(ts)}

def holm(ps):
    order = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * ps[i]); adj[i] = min(1.0, run)
    return adj

def system_means(cells, systems, nboot=2000, seed=1):
    rng = np.random.default_rng(seed)
    listeners = sorted({k[0] for k in cells}); tiles = sorted({k[1] for k in cells})
    out = {}
    for s in systems:
        vals = {(l, t): v for (l, t, ss), v in cells.items() if ss == s}
        if not vals: continue
        mean = float(np.mean(list(vals.values())))
        boots = []
        for _ in range(nboot):
            ls = rng.choice(listeners, len(listeners)); ts = rng.choice(tiles, len(tiles))
            tset = {}
            for t in ts: tset[t] = tset.get(t, 0) + 1
            num = den = 0.0
            for l in ls:
                for t, c in tset.items():
                    v = vals.get((l, t))
                    if v is not None: num += v * c; den += c
            if den: boots.append(num / den)
        out[s] = (mean, float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)), len(vals))
    return out

def ab_analysis(rows, listeners, pair):
    a = pair[0]; share = []
    for l in listeners:
        dec = [r for r in rows if r["listener"] == l and r["type"] == "ab" and r["choice"] in ("first", "second")]
        if not dec: continue
        wins = sum(1 for r in dec if (r["choice"] == "first" and r["first"] == a) or (r["choice"] == "second" and r["second"] == a))
        share.append(wins / len(dec))
    if len(share) < 3: return None
    share = np.array(share); t, p = stats.ttest_1samp(share, 0.5)
    se = share.std(ddof=1) / np.sqrt(len(share)); h = stats.t.ppf(0.975, len(share) - 1) * se
    none = sum(1 for r in rows if r["type"] == "ab" and r["listener"] in set(listeners) and r["choice"] == "none")
    tot = sum(1 for r in rows if r["type"] == "ab" and r["listener"] in set(listeners))
    return {"mean_share": float(share.mean()), "ci": (float(share.mean() - h), float(share.mean() + h)), "t": float(t), "p": float(p),
            "n_listeners": len(share), "no_difference_rate": none / tot if tot else float("nan")}

def rblend_corr(cells, rb):
    per = {}
    for (l, t, s), v in cells.items():
        per.setdefault((t, s), []).append(v)
    xs, ys = [], []
    for (t, s), vs in per.items():
        if s == DESIGN["reference_system"] or (t, s) not in rb: continue
        xs.append(np.mean(vs)); ys.append(rb[(t, s)])
    if len(xs) < 5: return None
    rho, p = stats.spearmanr(xs, ys)
    return {"rho": float(rho), "p": float(p), "n_cells": len(xs)}

def report(rows, rb=None):
    ok, per = eligible_listeners(rows)
    systems = DESIGN["systems"]
    cells = cell_table(rows, ok, systems)
    L = ["# Listening test report (generated)", "",
         f"Listeners in file: {len(per)}; eligible after pre-specified exclusions: {len(ok)}.", ""]
    L += ["## DCR means per system (two-way bootstrap 95% CI)", "", "| system | mean DCR | 95% CI | n cells |", "|---|---|---|---|"]
    for s, (m, lo, hi, n) in system_means(cells, systems).items():
        L.append(f"| {s} | {m:.2f} | [{lo:.2f}, {hi:.2f}] | {n} |")
    cons = [contrast(cells, "OURS", b) for b in ("N2N", "DUALCOSINE", "NOBAKE")]
    cons = [c for c in cons if c]
    if cons:
        adj = holm(np.array([c["p"] for c in cons]))
        L += ["", "## Confirmatory contrasts (two-way cluster-robust t, Holm over 3)", "", "| contrast | diff | 95% CI | t (df) | p | p Holm | listeners x tiles |", "|---|---|---|---|---|---|---|"]
        for c, pa in zip(cons, adj):
            L.append(f"| {c['a']} - {c['b']} | {c['diff']:.2f} | [{c['ci'][0]:.2f}, {c['ci'][1]:.2f}] | {c['t']:.2f} ({c['df']}) | {c['p']:.4f} | {pa:.4f} | {c['n_listeners']} x {c['n_tiles']} |")
    ab = ab_analysis(rows, ok, DESIGN["ab_pair"])
    if ab:
        L += ["", "## Forced choice OURS vs N2N", "",
              f"Share of decisive answers for OURS (listener-level mean): {ab['mean_share']:.3f}, 95% CI [{ab['ci'][0]:.3f}, {ab['ci'][1]:.3f}], t = {ab['t']:.2f}, p = {ab['p']:.4f}, n = {ab['n_listeners']} listeners; 'no audible difference' rate {ab['no_difference_rate']:.2f}."]
    if rb:
        rc = rblend_corr(cells, rb)
        if rc: L += ["", "## Exploratory: R_blend vs mean DCR (tile x system cells, IDEAL excluded)", "", f"Spearman rho = {rc['rho']:.3f}, p = {rc['p']:.3g}, n = {rc['n_cells']}."]
    return "\n".join(L) + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ratings"); ap.add_argument("--rblend"); ap.add_argument("--out")
    a = ap.parse_args()
    rows = read_csv(a.ratings)
    rb = None
    if a.rblend:
        rb = {(r["tile"], r["system"]): float(r["rblend"]) for r in csv.DictReader(open(a.rblend, newline=""))}
    text = report(rows, rb)
    if a.out: pathlib.Path(a.out).write_text(text)
    print(text)

if __name__ == "__main__":
    main()
