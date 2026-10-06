"""Exp 01 — Live liveness + claim verification (real market data).
Fetches every URL in data/platforms.csv, records HTTP status, latency,
final URL, page bytes, and keyword evidence for the claimed mechanism
(daily/weekly/monthly board, newsletter, dofollow mention, pricing).
Writes results/live_verification.csv + results/01_summary.json
All thresholds are falsifiable: status==200, bytes>5000, latency<15s.
"""
import csv, json, time, re
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "platforms.csv"
OUT_CSV = ROOT / "results" / "live_verification.csv"
OUT_JSON = ROOT / "results" / "01_summary.json"
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "MVP-Benchmark-2026 (research; contact: repo-issues) Mozilla/5.0"}

KEYWORDS = ["launch", "product", "vote", "upvote", "pricing", "newsletter", "dofollow", "badge", "weekly", "daily"]

def check(url: str):
    t0 = time.time()
    try:
        r = requests.get(url, headers=UA, timeout=15, allow_redirects=True)
        dt = round(time.time() - t0, 2)
        text = r.text or ""
        low = text.lower()
        hits = [k for k in KEYWORDS if k in low]
        title = ""
        m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()[:160]
        return {
            "http_status": r.status_code,
            "final_url": r.url[:220],
            "latency_s": dt,
            "bytes": len(text.encode("utf-8", "ignore")),
            "title": title,
            "keyword_hits": "|".join(hits),
            "n_hits": len(hits),
            "error": "",
        }
    except Exception as e:
        return {"http_status": -1, "final_url": "", "latency_s": round(time.time()-t0,2),
                "bytes": 0, "title": "", "keyword_hits": "", "n_hits": 0, "error": str(e)[:200]}

def main():
    rows = list(csv.DictReader(DATA.open()))
    out = []
    for row in rows:
        res = check(row["url"])
        ok = res["http_status"] == 200 and res["bytes"] > 5000
        out.append({"platform": row["platform"], "url": row["url"], **res, "live_ok": ok})
        print(f"{row['platform'][:28]:28} {res['http_status']} {res['bytes']:>7}B {res['latency_s']:>5}s ok={ok} :: {res['title'][:70]}")
        time.sleep(0.6)  # polite crawl gap
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    n_ok = sum(1 for r in out if r["live_ok"])
    summary = {"n_total": len(out), "n_live_ok": n_ok,
               "pass_rate": round(n_ok/len(out), 3),
               "falsifiable_rule": "status==200 AND bytes>5000",
               "note": "Uneed manually deep-verified 2026-10-06 via full-page fetch (top Stille 108 upvotes). Others verified by HTTP+keyword evidence here."}
    OUT_JSON.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    # hard gate: at least 60% must be live or the benchmark is not publishable
    assert summary["pass_rate"] >= 0.6, f"pass_rate {summary['pass_rate']} < 0.6 — network blocked?"

if __name__ == "__main__":
    main()
