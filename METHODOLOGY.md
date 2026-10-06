# METHODOLOGY.md — Zero-to-Hero Verification Protocol (no hand edits without evidence)

## Principle
Nothing in `data/` or `results/` is hand-enhanced. Every number traces to (a) a dated fetchable source in `verification_source`, or (b) a generated artifact under `results/`. Edits without re-running the pipeline are rejected in review.

## Search protocol (executed 2026-10-06, sequential — never parallel websearch)
1. `websearch`: “Product Hunt alternatives 2026 launch MVP startup” → saascity 25-table, smollaunch 16-table, launchllama 15-channel, getlaunchlist 12-verified, everfeatured SEO, kittylaunch, dev.to 9-platform, launchon.it.
2. `duckduckgo_search`: “MVP validation platforms BetaList SideProjectors Kernal best practice 2026” → MVP best-practice guides (gitnexa, gitscrum, vlstudio 7 techniques, editorialge, sprintlabs, soatech checklist, mtechzilla, rocket.new, speedmvps).
3. `openresearch web_search` (timed out — recorded as failed, fell through, no silent retry inflation).
4. `openresearch search_hacker_news`: “Product Hunt alternatives launch startup” → 8 threads incl. r/SideProject n=968 Claude-3-Opus analysis, PH cold-reality, tiny-PH-alternative $5.6k/mo.
5. `paper-search search_papers` (arxiv/semantic/crossref/openalex, “minimum viable product validation startup launch platforms”) → 9 papers: Duc & Abrahamsson MFP (84 cites), Reif 2017, Jain 2019, Subbarao 2019, Ackerman 2025, Wang SSFF 2024, PEGASUS ×2 (excluded as off-topic — kept in log for honesty), DOE PLATFORM (hardware analogue).
6. `agent-reach_search web`: “Uneed Fazier Peerlist Microlaunch DevHunt TinyLaunch review traffic” → saasrocket first-hand sessions, zplatform traffic medians, launchit.fast wait/price/link tables, tetriz.io P&L, husainjhalod playbook, peerlist launch stats (Uneed 40/3rd, Fazier 38/5th, Peerlist 76/12th + 561 views), saasreviews B2B, launchscaler dofollow-conditions, mazikbox Uneed review, launchit.fast 22-platform check.
7. `kaggle search_everything` (“startup success product hunt launch”) → no relevant dataset (recorded negative result).
8. `wiki_search` (“Product Hunt minimum viable product”) → Soft-launch article confirms PH+MVP pairing (weak signal, kept).
9. `gitmcp` devhunt/devhunt docs search → no match (negative result recorded).
10. `gsd_websearch` (“best practice MVP validation experiments 2026 benchmark”) → empty (negative result recorded).
11. `superpowers semantic_search_skills` → methodology-adjacent skills only (no content reuse).
12. `webfetch https://uneed.best/` (full-page, 2026-10-06) → daily board live: Stille #1 108, SuprPost #2 87, DoorHunter #3 73; 110k makers / 75 DR backlink / pricing / llms.txt claims captured.
13. `openresearch_read_url` / `webfetch` spot-checks + `experiments/01` full 25-URL sweep (see below).

Distinct keywords per engine; 429 backoff 5s→10s (max 3); DDG-lite fallback armed. Negative results are reported, not hidden.

## Live verification (Exp 01)
`experiments/01_live_liveness_check.py`: GET 25 URLs, UA `MVP-Benchmark-2026`, timeout 15 s, 0.6 s gap, record status/final-URL/latency/bytes/title/keyword-hits. Pass = 200 ∧ >5 kB. 2026-10-06: **22/25 = 0.88 ≥ 0.60 gate**. Failures: Startup Fame probe-timeout, AlternativeTo 403 Cloudflare, Kern.al DNS; warning: Twelve Tools parking page. Uneed deep-fetch cross-validates daily mechanism.

## Scoring (Exp 02), Patterns (Exp 03), Simulation (Exp 04)
As README §5. Weights declared in code; sensitivity in Exp 03; simulator priors = saasrocket Aug-2026 unfeatured counts; falsifiers stated in JSON outputs. Figures via matplotlib (Agg) — no hand-drawn charts.

## Reproduction gates
- `docker compose config` valid (32 lines).
- `pytest -q`: 6/6 green (25 rows, columns, https, ranked outputs, pattern verdict, lift ≥2.0).
- Results committed as generated JSON/CSV/PNG with code hash traceable via git (init + commit on publish).

## Upgrading this into a PhD paper
1. Pre-register H1–H5 + falsifiers (OSF) using this repo as pilot.
2. Replicate saasrocket protocol on ≥5 own MVPs stratified by ICP (dev-tool / micro-SaaS / AI-tool / non-tech buyer).
3. Add Ahrefs/Majestic backlink-index + newsletter-open longitudinals + Google/AI-citation tracking (PeerPush/LaunchOnIt SSR pattern).
4. Paired buyer-vs-maker WTP gap study (concierge + landing + 50–200 beta per redskydigital rule).
5. Submit pilot + replication as short paper; expand to full with RCT stagger experiment.
