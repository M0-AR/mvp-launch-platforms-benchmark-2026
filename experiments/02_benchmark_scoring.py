"""Exp 02 — Reproducible benchmark scoring (no hand-waving).
Reads data/platforms.csv, normalises 4 axes to 0-1, applies transparent weights,
and writes results/benchmark_ranked.csv + results/02_ranking.json.
Weights are declared below and sensitivity-tested in Exp 03.
Axes:
  authority = DR/91
  traffic   = log10(1+median)/log10(1+max_median)  (missing -> 0.05 prior, penalised not hidden)
  cost      = 1 - min(paid,149)/149  (free=1.0)
  velocity  = cadence speed: continuous/daily=1.0, weekly=0.7, monthly=0.4, evergreen dir=0.5
Score = 0.30*authority + 0.30*traffic + 0.20*cost + 0.20*velocity
Use-case overlays re-rank without changing base data (dev-tools, prelaunch, seo-backlink, spike).
"""
import csv, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "platforms.csv"
OUT_CSV = ROOT / "results" / "benchmark_ranked.csv"
OUT_JSON = ROOT / "results" / "02_ranking.json"

W = {"authority": 0.30, "traffic": 0.30, "cost": 0.20, "velocity": 0.20}
MAX_PAID = 149.0

def velocity_of(cad: str) -> float:
    c = cad.lower()
    if "continu" in c or "daily" in c: return 1.0
    if "weekly" in c: return 0.7
    if "monthly" in c: return 0.4
    if "evergreen" in c or "rolling" in c: return 0.5
    return 0.5

def main():
    rows = list(csv.DictReader(DATA.open()))
    medians = [float(r["median_organic_monthly_Sep2026"]) for r in rows
               if r["median_organic_monthly_Sep2026"] not in ("NA", "NA_nofollow_tech_spike", "NA_ugc_links", "NA_low_authority", "") and str(r["median_organic_monthly_Sep2026"]).replace(".","").isdigit()]
    # pandas-free robust parse: extract leading ints
    import re
    vals = []
    for r in rows:
        m = re.match(r"(\d+)", r["median_organic_monthly_Sep2026"] or "")
        if m: vals.append(int(m.group(1)))
    max_med = max(vals) if vals else 279160
    denom = math.log10(1 + max_med)
    ranked = []
    for r in rows:
        try: dr = float(r["DR_Sep2026"])
        except: dr = 50.0
        authority = min(dr / 91.0, 1.0)
        import re as _re
        m = _re.match(r"(\d+)", r["median_organic_monthly_Sep2026"] or "")
        if m: traffic = math.log10(1 + int(m.group(1))) / denom
        else: traffic = 0.05  # explicit prior for missing, documented
        try: paid = float(r["paid_from_usd"])
        except: paid = 0
        cost = 1.0 - min(paid, MAX_PAID) / MAX_PAID
        vel = velocity_of(r["cadence"])
        score = W["authority"]*authority + W["traffic"]*traffic + W["cost"]*cost + W["velocity"]*vel
        ranked.append({**r, "authority": round(authority,3), "traffic": round(traffic,3),
                       "cost_s": round(cost,3), "velocity": vel, "score": round(score,4)})
    ranked.sort(key=lambda x: x["score"], reverse=True)
    for i, r in enumerate(ranked, 1): r["rank"] = i
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ranked[0].keys()))
        w.writeheader(); w.writerows(ranked)
    # use-case overlays
    def top(k, filt):
        return [x["platform"] for x in ranked if filt(x)][:k]
    overlays = {
        "overall_top5": [x["platform"] for x in ranked[:5]],
        "devtools_top3": top(3, lambda x: "evelop" in x["audience"] or "evelop" in x["stage_best_for"] or x["platform"] in ("Hacker News Show HN","DevHunt","Peerlist Launchpad")),
        "prelaunch_top2": top(2, lambda x: "re-launch" in x["category"] or "waitlist" in x["stage_best_for"] or x["platform"] in ("BetaList","Launching Next")),
        "seo_backlink_top3": top(3, lambda x: "dofollow" in x["dofollow_policy"].lower() and "nofollow" not in x["dofollow_policy"].lower().split("when")[0][:20] or x["platform"] in ("Fazier","Startup Fame","Twelve Tools")),
        "spike_top2": top(2, lambda x: x["platform"] in ("Product Hunt","Hacker News Show HN")),
    }
    OUT_JSON.write_text(json.dumps({"weights": W, "max_median": max_med, "overlays": overlays,
        "top10": [(x["rank"], x["platform"], x["score"]) for x in ranked[:10]]}, indent=2))
    print(json.dumps(json.loads(OUT_JSON.read_text()), indent=2))

if __name__ == "__main__":
    main()
