# What the FoF/t1-sensor work changes about Wing lead generation

*Written 2026-08-18 from the 2026-08-16/17 FoF sessions. Canonical copy here; pointer in
`~/.claude/skills/weekly-selection/SKILL.md`. Any agent doing Wing sourcing should read this before
ranking a week's catches.*

**Governing thought.** Every Wing sourcing surface that uses investor attention as a signal — the X
follow sweep's `n_vcs`, the daily_catches VC-follow graph, hook enrichment, engagement scanning —
currently counts *how many* investors moved. The FoF work measured *which* investors are worth
counting, and the answer is not uniform: measured hit rates against a common base spread from below
1x to above 4x. Re-weighting by measured rate is the single cheapest improvement available, and the
measurement engine already exists.

Order below is what to change first, by size of effect over cost.

---

## 1. `n_vcs` counts cheque volume, exactly like the preceder list we already discredited

Yasin's Top Preceders sheet ranked investors by deal count wearing two disguises (`Success Rate` divided
every investor by the same constant 2,610; `Investment Quality Score` was n²/2,610). Re-ranked by each
investor's own rate the list nearly inverted. **The X sweep repeats the same mistake in a different
coordinate system**: `n_vcs` is a count of follows from a 539-handle list where every handle carries
equal weight.

That list is not a list of investors — it is a list of *people*, and the number of people a firm puts on
it tracks firm headcount, not firm signal:

| Fund | Handles on the list | Measured lift |
|---|---|---|
| a16z | 38 | 7.53x |
| Bessemer | 36 | 6.65x |
| Accel | 30 | 5.92x |
| Sequoia | 26 | 6.34x |
| **SV Angel** | **1** | **6.34x** |
| Radical Ventures | 7 | below base |

A founder followed by three a16z associates scores `n_vcs=3`; a founder followed by SV Angel scores
`n_vcs=1`. On measured rate those are the same event, and the second is the rarer one.

**Fix.** Collapse follows to the firm before counting, then weight by measured firm lift. Two lines in
`enrich_and_filter.py`: map handle → fund via the existing `vc_directory.json`, dedupe by fund, score
`sum(log(lift))` over distinct funds instead of `len(follows)`. Weight table written to
`~/sourcing/fof/backtests/xlist_firm_lift.json` (160 funds on the list, 84 measurable at ≥5 seed
entries, covering 366 of 539 handles).

## 2. Weight at the firm, never at the person — individual track records do not survive re-measurement

This is the load-bearing finding and it is new as of today. I rebuilt the lift computation from scratch
on an independent tape (`yasin_test.crunchbase_investments`, 159,846 investor-round rows) and
rank-correlated it against the FoF tables:

- **Firms: Spearman rho = +0.69** (n=41 preceders), +0.50 (n=8 roster managers). The ordering is real.
- **Individuals: Spearman rho = +0.22** (n=20). The ordering is noise.

Individual entry counts differ wildly between tapes — Kevin Hartz 16 entries vs 6, Justin Mateen 30 vs 9
— because personal angel cheques are unevenly recorded. A person's "book" is whatever the tape happened
to capture.

This converges with the walk-forward result from 2026-08-17, which found the same thing by a different
route: **SV Angel 3.31x → 5.28x forward, while Naval Ravikant went 2.35x → 0.00x on 29 bets** and Ameet
Patel 2.84x → 0.00x on 10. Aggregate persistence measured 0.87; individual persistence is not
demonstrated at all.

**Consequence for Wing.** Any hook or trigger that reads "X, a well-known angel, followed them" carries
much less information than the same signal attributed to a firm. Do not build a per-person credibility
score. Do not let a single famous individual's attention promote a row.

## 3. Only two names survive a two-tape de-weighting test — and Gaingels and Goodwater are not among them

**Correction to `preceder-ranking-and-sector-map.md`.** That file asserts Gaingels (0.84x), Nadav
Ben-Chanoch (0.42x) and Goodwater (0.43x) sit below base, i.e. their presence is a mild negative signal.
Re-measured on the second tape, only two of those hold:

| Investor | FoF tape | Second tape | Verdict |
|---|---|---|---|
| Nadav Ben-Chanoch | 0.42x / 75 | 0.73x / 83 | below base in both — **de-weight** |
| Outset Ventures | 0.61x / 16 | 0.69x / 11 | below base in both — **de-weight** |
| Gaingels | 0.84x / 106 | **1.32x / 200** | disagrees — **do not act** |
| Goodwater Capital | 0.43x / 193 | **1.23x / 303** | disagrees — **do not act** |
| Charlie Songhurst | 1.08x / 61 | 0.40x / 37 | disagrees — do not act |

Above 2x on **both** tapes, so safe to up-weight: SV Angel, Chapter One, Amplify Partners, 1984 Ventures,
Abstract, Volt Capital, Liquid 2 Ventures, A.Capital, Afore, Bain Capital Ventures, Craft Ventures.

**Standing rule: never de-weight an investor on one tape's measurement.** A below-base claim is a claim
that attention from a real firm is evidence *against* a founder — an expensive mistake to make on
sampling noise.

## 4. The event the sensor predicts is worth predicting — 5.3x on outcomes, not just on fashion

Measured over 15,090 companies seeded 2019–21: a company that draws a **new** top-29 investor within 24
months is **5.3x** more likely to reach a $100M outcome, 6.9x at $250M, ~9x on median capital raised.
This is the justification for the whole front-run frame — "a tier-1 firm showed up" is not a popularity
metric, it is an outcome proxy with a measured multiple. Quote this when anyone asks why we optimise for
tier-1 arrival rather than for revenue signals we cannot see at pre-seed.

It also validates the premium formula used in the FoF model, `0.35 × ln(lift)`, to within 2%.

## 5. Point the preceder-style sensors only at sectors where a front-run window exists

From Yasin's `speed data` (days from seed to Series A, preceders vs tier-1 firms):

| Sector | Preceder window | T1 deals 24→25 | Read for Wing sourcing |
|---|---|---|---|
| **Aerospace / defense** | **+113 d** | **28 → 41 (+46%)** | the extension to build — wide window, demand rising, median cheque $20M→$50M |
| Cybersecurity | +145 d | 70 → 73 | Jake's #1 lane, window healthy |
| Infra | +122 d | 117 → 110 | **compressing fastest** — T1 seed→A fell 481d → 283d YoY |
| B2B | +113 d | 284 → 317 | healthy |
| Health | +50 d | 178 → 177 | narrow — Sara's lane needs earlier sources |
| Consumer | −19 d | 125 → 103 | no edge |
| **Robotics** | **−158 d** | 9 → 12 | **no preceder edge — T1 is at seed first** |
| **Crypto** | **−181 d** | 17 → 20 | **no preceder edge** |

Two operational consequences:

- **Robotics is a blind spot for follow-graph sourcing**, and robotics is exactly what the `unusual`
  flag adds on top of Wing. There is nobody to front-run there — tier-1 firms are already at seed. Cover
  robotics through the sensors that do not depend on investor attention: departure sweep (Tesla
  Autopilot / Waymo / Figure / Physical Intelligence / Skild are already on the 30-org roster), talent
  markers, repo velocity, accelerator cohorts.
- **Our home lane's lead is shrinking fastest.** The 8.6-month median lead measured across the signal log
  will decay soonest in infra. That is a quantitative argument for the claim-decay rule already in the
  rubric: an unclaimed infra row ages faster than an unclaimed health row.

## 6. Report every hit rate against a base, and state which base

The FoF work found the same number quoted against two different denominators on adjacent charts (5.88%
seed-only vs 13.43% all-entries) and the two told opposite stories. Wing deliverables have the same
exposure: "N of our picks raised" means nothing without the rate a random comparable cohort achieved.

Definition to standardise on when making a lift claim: **seed/pre-seed entries, common window, a NEW
tier-1 investor arriving within 24 months, shrunk toward base at prior strength 25.** Always print
`hits/entries` next to the lift so the reader can see the sample. Never put two bases on one page.

## 7. A new lead source: rank *individuals* by book, then watch their next positions

The Mei Zuo work established that an individual's investment book is reconstructable from LinkedIn
(one experience entry per portfolio company). `individuals_ranked.json` holds 122 people ranked this
way, with `active24` = positions in the last 24 months.

Note the tension with §2: this ranking is **fragile as a scoring input** but useful as a **discovery
input**. The claim "this person picks well" does not survive re-measurement; the claim "this person is
actively writing cheques into stealth companies right now" does, and is exactly the sourcing hook.
Their *new* positions are a trigger stream nobody else is watching, because it is invisible to
Crunchbase at pre-seed — same logic as the micro-fund portfolio sweep (weekly-selection source 17),
applied to individuals instead of funds. `active24` picks the ones still writing: Guillermo Rauch (32),
Scott Belsky (22), Nat Friedman (18), Jackson Moses (11).

Known blind spot in `mei_detector.py`: it catches Mei's profile shape (one experience per company) but
misses Ameet Patel's (whole portfolio compressed into one description as initials).

## 8. What did not transfer, and the gaps a follow-up must close

- **The lift engine was never persisted.** The script producing the 5.88% base and the 26,636-company
  universe was run inline and lost; only its JSON outputs survive. Today's reproduction is a *different*
  script on a *different* tape and gets base 1.84% on 16,389 companies, because
  `crunchbase_investments` under-observes investor lists. **Relative ranking transfers; absolute lift
  numbers are not comparable across the two.** Never mix them in one table. Rebuilding the engine as a
  committed script is the prerequisite for everything in §1.
- **151 of 539 X handles match no investor record at all**, and another set match only through an
  abbreviated fund name (`a16z`, `Boldstart`, `Lightspeed`). The alias map in
  `xlist_firm_lift.json`'s generator handles the common cases; it needs finishing before the weights go
  live.
- **Boldstart measures 0/18 on the reproduction tape** but 2.66x fit / 1.82x forward on the FoF tape.
  That is a tape artifact, not a finding, and it is the clearest illustration of why §3's two-tape rule
  exists.
- Sector-exclusion control is not buildable at 26% category coverage of the corpus.
- Our convergence claim was over-counted 3x on audit: 22 claimed cases → **7 confirmed, 1 reversed**
  (Paces — Soma entered twenty-one months *before* our signal). Any Wing-facing convergence number must
  be the audited 7, not the raw match count.

---

## 9. Lift alone does not find preceders — it is uncorrelated with actually being early

*Added 2026-08-18 (second session). The engine from Next action #1 is now committed at
`~/sourcing/fof/scripts/measure_lift.py`; this section is what running it showed.*

§1 fixed *counting the wrong unit* (handles instead of funds). There is a second unit error one
level down: **a "hit" says tier-1 later appeared on the cap table, not that our investor got there
first.** A crossover writing a Series B cheque alongside Sequoia scores exactly the same hit as an
angel who was three years early. Ranking preceders by lift therefore promotes late money.

Measured on the dated tape (`syndicates.csv`, 250 companies, earliness = entered >60d before the
first tier-1 entry, both terms beta-shrunk):

**corr(lift, earliness) = −0.14 across 53 investors.** Not weak-positive — *nothing*, tilting
negative. The two rankings barely overlap:

| Ranked by lift | | Ranked by lift x earliness | |
|---|---|---|---|
| SV Angel | 1.35 | Soma Capital | 46% early |
| NVIDIA | 1.34 | Plug and Play | 42% early |
| BoxGroup | 1.31 | Evolution VC | 42% early |
| Y Combinator | 1.26 | Scott Belsky | 28% early |
| Quiet Capital | 1.26 | Justin Mateen | 28% early |

The lift column's top names are near-base on earliness; the early names are near-base on lift.
An earlier cut of this analysis ranked on lift alone and returned Coatue, CRV, IVP, Meritech,
Bain, Databricks Ventures and Salesforce Ventures as "preceders" — every one of them a growth or
strategic investor whose presence is a *consequence* of the company already winning. Their
earliness rows read 0/4, 0/3, 0/6, 0/8. The signal was entirely an artifact.

**Fix.** Any preceder-derived weight must be `lift x earliness`, and any investor with no dated
opportunities is unranked, not top-ranked. `measure_lift.py --earliness` prints both columns plus
the correlation so this cannot silently regress.

**Two traps this exposed, both worth carrying forward:**

- **`t1_live_list.json` is not the tier-1 list** and must never be used for this. It omits Coatue,
  Greylock, CRV, Felicis, IVP, Thrive, Norwest, USV and Iconiq — so those firms get scored *as
  preceders of themselves*, which is circular and inflates them straight to the top. The canonical
  29 is `intel/t1_canonical_handpicked.json`; `measure_lift.py` loads it with an alias map and
  refuses the other file. `analyze_precursors.py` in `~/sourcing/t1-sensor/` still uses the wrong
  list — its output is not safe to quote.
- **Base rate is a property of the tape, not of the world.** Same engine, same definition:
  showcase gives base 25.9% on 1,257 companies, `syndicates.csv` gives **50.8%** — because that
  tape is unicorns-only and has no negatives at all. Lift there is compressed toward 1 and means
  nothing in absolute terms. Use showcase (or the big Mongo tape) for lift, `syndicates.csv` only
  for earliness, and never put the two in one table — the §8 rule, now with a worked example.

**Operationally for the weekly run:** the preceders worth watching are small and individual —
Soma, Plug and Play, Scott Belsky, Justin Mateen, K5, Mei Z., Operator Partners, JAM Fund — not
the brand funds that top the lift table. That is the same conclusion §7 reached from the book
side, arrived at independently from the timing side, which is the strongest form this evidence
takes.

## Next actions, in order

1. ~~Rebuild and commit the lift engine as `~/sourcing/fof/scripts/measure_lift.py`~~ **DONE
   2026-08-18** — committed, tape-agnostic, canonical-T1 only, `--earliness` and `--seed-only`
   flags, writes `backtests/measured_lift.json`. Still needs repointing at the big Mongo tape;
   the two local tapes are small (1,257 and 250 companies).
2. Finish the fund alias map, re-measure all 539 handles, write `xlist_firm_lift.json` as the live
   weight table.
3. Change `enrich_and_filter.py` to dedupe follows by fund and score `sum(log(lift))`; keep raw `n_vcs`
   in the sheet alongside so the change is auditable for a few weeks before trusting it.
4. Fold the aerospace/defense lane into the conference and departure sweeps; stop expecting the follow
   graph to cover robotics.
5. Add `active24`-ranked individuals from `individuals_ranked.json` as a watchlist for new-position
   diffs — a new weekly-selection source, discovery only, never a score.
6. Re-rank every preceder-derived weight on `lift x earliness` (§9), and fix or retire
   `~/sourcing/t1-sensor/analyze_precursors.py`, which still ranks raw counts against the wrong
   tier-1 list.

Related: [[t1-canonical-list]], [[preceder-rank-volume]], [[t1-arrival-worth]], [[scout-fund-in-a-box]],
[[weekly-selection]], [[tier1-round-too-late]].

---

## 10. Nine pipeline defects (2026-08-19) — read before trusting any count

A full weekly run surfaced nine silent defects, four of which systematically UNDER-report
selections. Two of the four were analyst-written filters, not data faults: a founder regex that
omitted "founding" (cost ~39 rows across four sweeps, including the batch's top row at z=15.56) and
a sheet read capped at 400 of 1,911 rows (cost 24 selects). One tool, `bulk_get_crunchbase_data`,
actively FABRICATES a Series A for any unmatched URN and is pointed straight at the funding sweep.
The departure sweep mis-attributes the employer ~50% of the time.

**Operating rule that generalises: in this pipeline a low count is not a thin week, it is the most
common symptom of a bug. Sanity-check every count against its baseline before reporting it.**

Full detail, including the four catch-all URNs and the verification-tooling failure modes:
`intel/sourcing-pipeline-defects-2026-08-19.md`.
