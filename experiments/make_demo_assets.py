"""Make demo assets (verified, generated — not hand-made).
Outputs:
  docs/video/demo-bars.gif  — animated top-10 score build-up (matplotlib)
  docs/video/demo.mp4       — 12s slideshow: 3 live screenshots + DR-vs-traffic chart (ffmpeg)
  docs/screenshots/dr-vs-traffic.png — copy of results figure for README embedding
Run: /tmp/mvpvenv/bin/python experiments/make_demo_assets.py
Requires: matplotlib, pillow, ffmpeg on PATH.
"""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "results" / "benchmark_ranked.csv"
CHART = ROOT / "results" / "figures" / "dr_vs_traffic.png"
VID_DIR = ROOT / "docs" / "video"
SHOT_DIR = ROOT / "docs" / "screenshots"
VID_DIR.mkdir(parents=True, exist_ok=True)

def make_gif():
    rows = list(csv.DictReader(BENCH.open()))[:10]
    names = [r["platform"][:16] for r in rows][::-1]
    scores = [float(r["score"]) for r in rows][::-1]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    def frame(f):
        ax.clear()
        k = f / 100
        ax.barh(names, [s * k for s in scores], color="#f97316")
        ax.set_xlim(0, 1.05)
        ax.set_xlabel("Benchmark score (0.30 authority + 0.30 traffic + 0.20 cost + 0.20 velocity)")
        ax.set_title(f"Top-10 MVP launch platforms — build-up {int(k*100)}%")
        fig.tight_layout()
    anim = FuncAnimation(fig, frame, frames=list(range(5, 101, 5)), interval=120)
    out = VID_DIR / "demo-bars.gif"
    anim.save(out, writer="pillow", fps=8)
    print(f"saved {out} ({out.stat().st_size/1024:.0f} KB)")
    return out

def make_mp4():
    import subprocess, tempfile, shutil
    imgs = [SHOT_DIR / "uneed-live-2026-10-06.png",
            SHOT_DIR / "producthunt-live-2026-10-06.png",
            SHOT_DIR / "betalist-live-2026-10-06.png",
            CHART]
    for p in imgs:
        assert p.exists(), f"missing {p}"
    # copy chart next to screenshots for README embedding
    shutil.copy(CHART, SHOT_DIR / "dr-vs-traffic.png")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        seq = []
        for i, p in enumerate(imgs):
            q = td / f"img{i:03d}.png"
            shutil.copy(p, q)
            seq.append(q)
        # build ffmpeg concat: each image 3s, 1280x720 pad, 30fps
        import subprocess as sp
        inputs = []
        for q in seq:
            inputs += ["-loop", "1", "-t", "3", "-i", str(q)]
        fc = "".join(f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v{i}];" for i in range(len(seq)))
        fc += "".join(f"[v{i}]" for i in range(len(seq))) + f"concat=n={len(seq)}:v=1:a=0[out]"
        out = VID_DIR / "demo.mp4"
        cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-map", "[out]",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
        r = sp.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr[-3000:])
            raise SystemExit("ffmpeg failed")
        print(f"saved {out} ({out.stat().st_size/1024:.0f} KB)")
        return out

if __name__ == "__main__":
    g = make_gif()
    m = make_mp4()
    assert g.stat().st_size > 10_000 and m.stat().st_size > 10_000
    print("demo assets OK")
