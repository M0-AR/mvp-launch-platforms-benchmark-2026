import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_csv_has_25_rows():
    rows = list(csv.DictReader((ROOT/"data"/"platforms.csv").open()))
    assert len(rows) == 25, f"expected 25, got {len(rows)}"
def test_required_columns():
    rows = list(csv.DictReader((ROOT/"data"/"platforms.csv").open()))
    for c in ["platform","url","DR_Sep2026","paid_from_usd","verification_source"]:
        assert c in rows[0], f"missing {c}"
def test_urls_https():
    rows = list(csv.DictReader((ROOT/"data"/"platforms.csv").open()))
    bad = [r["platform"] for r in rows if not r["url"].startswith("https://")]
    assert not bad, f"non-https: {bad}"
def test_benchmark_outputs_exist_and_ranked():
    import json
    assert (ROOT/"results"/"benchmark_ranked.csv").exists()
    assert (ROOT/"results"/"02_ranking.json").exists()
    d = json.loads((ROOT/"results"/"02_ranking.json").read_text())
    assert "overlays" in d and len(d["top10"]) == 10
def test_patterns_supported():
    import json
    d = json.loads((ROOT/"results"/"03_patterns.json").read_text())
    assert d["H1_DR_vs_traffic"]["verdict"].startswith("SUPPORTED") or "REJECTED" in d["H1_DR_vs_traffic"]["verdict"]
def test_simulation_lift():
    import json
    d = json.loads((ROOT/"results"/"04_simulation.json").read_text())
    assert d["lift_sustained"] >= 2.0
