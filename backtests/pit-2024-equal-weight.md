# Point-in-time backtest: Aug-2024 signal-selected managers, equal weight
Selected as of 2024-08-14 (signals verifiably live then). Outcome = pre-cutoff portfolio
company entering the Aug-2025→Aug-2026 new-unicorn cohort. Base ≈ 1–1.5%/2yr for random early portfolios.

| manager | pre-cutoff cos | unicorns | rate |
|---|---|---|---|
| JAM Fund (Mateen) | 82 | 6 | **7.3%** |
| Theory (Tunguz) | 5 | 1 | 20% (n=5) |
| Quiet Capital | 344 | 8 | 2.3% |
| Cota | 132 | 3 | 2.3% |
| Day One | 99 | 2 | 2.0% |
| SGH | 112 | 2 | 1.8% |
| Soma | 803 | 10 | 1.2% |
| Humba / Wischoff | 10 / 10 | 0 | 0% (lane mismatch) |
| Mei Zuo (known positions ONLY — numerator-selected, excluded from averages) | 3 | 3 | — |

Pooled 32/1,597 = **2.0%** (~1.3–2× base). Equal-weight ex-Zuo ≈ **4.1%** (~3× base).

**Findings:** (1) equal-weighting ALL signal-flagged managers ≈ modest 1.5–2× lift — spray-heavy
books (Soma 803 checks) drag the pool to base-rate. (2) The spread WITHIN the selected class
(JAM 7.3% vs Soma 1.2%) exceeds selected-vs-base — tiered concentration, not binary selection,
is where the alpha is; this is what the lift/conversion scoring does. (3) Lane matters: Wischoff/
Humba 0 unicorns ≠ bad funds — wrong outcome metric for their lanes; the FoF metric must be
lane-adjusted. (4) Caveats: unicorn-membership misses sub-unicorn markups (Novig $500M);
Perceptive tape unresolved; 294-cohort has known gaps; 2-yr window favors fast AI lanes.

**Simulator calibration implication:** selection toggle should be tiered — "all-signals equal
weight" ≈ 1.5–2× hit-rate lift; "top-tier concentrated" ≈ 3–5×.

## Reconciliation with the simulator's construction rules (2026-08-15)
Applying the sim's OWN rules to the real 2024-vintage books (marks @ Aug 2026, yr 2 of 10):
| manager | class | n | 2024-vintage TVPI |
|---|---|---|---|
| Quiet | B | 40 | 2.66x |
| Wischoff | D | 15 | 2.40x |
| Soma | D | 148 | 2.09x |
| Humba | B | 13 | 1.97x |
| Day One | B | 21 | 1.58x |
| Theory | B | 11 | 1.17x |
| SGH / Cota / JAM | B | 7/11/5 | 1.06x / 1.00x / 0.96x |

**equal weight 1.60x · tiered 1.51x · with a random-pick 30% co-invest sleeve 1.43-1.49x** (sleeve
median 1.27x from 12 random positions of 271, incl. the no-manager-fee uplift).

TWO FINDINGS AGAINST OUR OWN MODEL:
1. Tiering HURT in this window — top 2024 books were Wischoff (D-class in our weights) and Quiet;
   JAM (our best pre-2024 performer, 5.4x) sits at 0.96x on 5 young positions. Weights fitted on one
   period misfire on the next -> start near equal weight, concentrate as fresh evidence accrues,
   re-tier at Fund II. (Also: 5 positions at yr 2 is not evidence of anything.)
2. Co-invest WITHOUT selection skill hurt (random sleeve 1.27x). The sim credits co-invest with
   precursor-informed picking; this window cannot prove that skill. Treat the sleeve premium as an
   assumption, and say so to LPs.
