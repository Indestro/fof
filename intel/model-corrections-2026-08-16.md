# Four corrections that changed the fund model, and one finding that survived them

Session of 2026-08-16. Each item below was a real error found by checking the model against
something outside it. Recorded so they are not reintroduced.

## 1. The page contradicted itself on tiering

The backtest said concentrating capital into our highest-conviction managers **lost** (1.51x
against 1.60x equal weight). The simulator's default was tiered and showed the best number.
Same page, opposite claims.

Fix: **selection and weighting are now separate controls.** Selection decides whether we earn the
measured premium and reach oversubscribed funds; weighting only splits capital. The default is
signal-selected and **equal weight**, because equal weight is what our own evidence supports.
Re-tiering waits for Fund II, when there is a second period to fit against.

## 2. The backtest and the simulator were measuring different things

Simulator year-2 median was 0.89x (TVPI on committed capital, through the J-curve). The backtest
chart said 1.60x at year 2. Both were labelled "net TVPI". The backtest was marking **deployed**
capital; the simulator was on **committed**.

Fix: the backtest is restated on committed capital — 45% of commitments called by year two,
uncalled held at par, fees drawn. 1.60x deployed becomes **1.25x committed**; tiered 1.51x becomes
1.21x; the benchmark 1.05x becomes 1.00x. The simulator's value ramp was also too slow (nothing
accrued before year 3); it now follows a Weibull curve normalised at year 10 with an early fee dip.
Year-2 median is 1.14x with a middle half of 1.03x–1.31x, so **the real 2024 book at 1.25x lands
inside the model's band, slightly ahead of the median.** That is now a calibration test rather
than a second story.

## 3. Two lift tables on adjacent charts used different base rates

The manager table used a 13.43% base (seed *and* Series A entries, any follow-on window). The
preceder re-rank used 5.88% (seed only, new tier-1 within 24 months). Putting them side by side
would have repeated the error in item 2.

Fix: **one definition everywhere** — seed and pre-seed entries 2019-2023, a *new* tier-1 investor
within 24 months, shrunk toward base at prior strength 25. Base = 1,566/26,636 = **5.88%**.
Recomputed roster in `backtests/roster_lift_unified.json`.

## 4. The model was 20% optimistic before selection even started

With selection switched off it returned 1.83x and 9.9%, against a published fund-of-funds median
of 1.4–1.6x. A calibration note claiming the model reproduced a known number was simply false.

Fix: the unselected access cap drops from 3.0x to **2.0x** — without selection or relationships an
LP cannot buy a fund that returns more than about 2x, which is the actual mechanism. Selection-off
now returns **1.55x and 7.1%**, inside the published TVPI band and a little under on IRR. That
calibration was not fitted, so it is the check on everything else.

Also added: **per-scenario estimation error on each manager's premium**, with spread set by the
number of seed entries the measurement rests on (five entries wide, 177 tight, unmeasured widest).

## The finding that survived: manager count is not a return lever

With estimation error in, six managers still returns about the same as twelve (3.27x vs 3.21x).
The dominant risks — the vintage factor and the direct sleeve — are common to every manager, so
holding more of them diversifies almost nothing. The return only falls past twelve because the
roster runs out of *measured* names.

So the case for twelve is not diversification of returns. It is that our premiums rest on samples
as small as five, and a concentrated fund is a bet that a handful of those estimates are right.
The page now says this instead of a concentration warning the numbers contradict.

## Default configuration after the corrections

$40M, 12 managers, 35% direct sleeve, signal-selected, equal weight →
**3.21x median net TVPI, 3.85x mean, 20.3% median net IRR, 2% chance of losing money.**
Selection off → 1.55x / 7.1%.


---

# Second pass: the IRR was too high and the loss rate too low

Emrah pushed back on 20.3% net IRR and a 2% chance of losing money. Both were right to challenge.
Four further corrections, all of which lower the answer.

**1. Persistence.** The roster is the top 12 of 816 measured investors, so its lifts are in-sample
maxima — selecting on the outcome variable and then assuming full persistence. Our own Seed-100
persistence test found 48/100 top performers persisted with a median 22-place move, so the measured
premium is now **discounted 50%** before use, and the haircut is exposed as a slider.

**2. The direct sleeve was invented.** It carried a 4.05x mean. Our 2024 window measured *random*
co-investment into the same companies at **1.27x**. The sleeve is now calibrated to return 1.27x
unselected and **2.20x** selected — a stated 1.7x skill premium, and the largest single assumption
on the page.

**3. Distribution timing.** Cash was returning from year four. Seed funds do not distribute before
roughly year six; the schedule now starts there. The old timing was worth about two points of IRR.

**4. Vintage risk was thin-tailed.** A lognormal with sigma 0.46 puts a fund-halving vintage at
6.5%, yet 2000 and 2021 both happened inside 25 years. Replaced with a **regime switch: 18% of
vintages are busts** centred near a 55% haircut. That moves a fund-halving vintage to 12% and is
the dominant driver of the chance of losing money — no amount of manager selection diversifies it.

Base return also lifted (MU 0.50 -> 0.58, unselected cap 2.0 -> 2.3) so the calibration case still
lands on the published benchmark after the four haircuts above.

## Where it lands now

| Configuration | Net TVPI | Net IRR | Chance of loss |
|---|---|---|---|
| **Default** — $40M, 12 managers, 35% sleeve, selected, equal weight | **2.74x** (mean 3.08x) | **15.4%** | **8%** |
| Persistence at 100% | 3.04x | 17.1% | 7% |
| Persistence at 0% — picking edge gone, access kept | 2.48x | 13.7% | 10% |
| **Calibration** — selection off, no sleeve | **1.60x** | 6.9% | **21%** |

Published benchmarks: fund-of-funds median 1.4-1.6x / 8-10%; top quartile 1.9-2.2x / 12-15%.
The calibration case now lands on the median for TVPI and loss rate, slightly under on IRR (the
year-six distribution schedule costs it). The default sits at top-quartile, which is a claim we can
defend, where 3.21x / 20.3% was not.

**The edge now decomposes**, which is worth more in a meeting than the headline: access alone is
worth 1.60x -> 2.48x; picking on top of access is worth 2.48x -> 2.74x at the persistence we assume,
3.04x if it persists fully.

---

# Third pass: truth-in-research audit of every assertion on the page

Emrah asked that every claim be scientifically defensible. Twelve failed. Recorded so they are
not reintroduced by a later edit.

**Overclaims of capability**
1. Headline read *"We can see which start-ups the top venture firms will back."* We cannot. 137 of
   5,323 flagged founders converted — a 2.6% rate. Replaced with the measured fact: *"We flagged
   137 founders before the top venture firms funded them — by a median of nine months."*
2. *"On average a top firm shows up nine months later"* — a conditioning error. Nine months is the
   median **among converters only**; for ~97% no top firm arrives. Now stated conditionally.
3. *"Three rounds we would have been offered"* — we cannot know that. Now *"three rounds where a
   co-investment slot plausibly existed"*, with an explicit line saying the exercise cannot show
   whether we would have been offered them.
4. *"This is the offer no other limited partner can make"* — unfalsifiable. Now *"we know of no
   other limited partner making this offer."*

**Statistical overclaims**
5. *"Gaingels... a company it seeds is less likely to draw top-firm money than average."* False.
   5 hits on 106 entries against 6.2 expected is **z = −0.51** — inside the noise. Now states the
   defensible negative: nothing in its record supports treating it as a positive signal.
6. *"Mei Zuo... does not survive measurement."* It was never measured — 0 hits on **4** entries,
   z = −0.50. Now *"cannot be assessed at all."*
7. Added the significance frame: of 41 measurable names, five clear base by >2 SE (SV Angel z=+10.8,
   Chapter One +5.9, Abstract +4.8, Silent Ventures +4.3, YC +5.0) and one falls below by >2 SE
   (Goodwater z=−2.25). Gaingels, Ben-Chanoch, Day One and Mei Zuo are all indistinguishable.

**Arithmetic and sourcing errors**
8. *"Deal count 28→41, the biggest jump on the board."* B2B went 284→317 = +33, larger outright.
   Corrected to *biggest proportional rise*, with the B2B caveat.
9. *"A four-month head start"* for energy, cyber and aerospace. They are 270, 145 and 113 days.
   Corrected to nine, five and four months respectively.
10. Decacorn claim asserted *18 of 19 minted in falling-count sectors*; the published chart's own
    source note says 18 of 19 were **mappable**. Softened to match the published wording.
11. Benchmark rows were sourced to *"Cambridge Associates-style vintage statistics"* — weasel
    wording implying a series we do not cite. Now labelled indicative ranges from published
    industry statistics.
12. Founder counts were inconsistent (5,329 / 5,323). Now stated once: 5,329 signals, 5,323
    distinct founders, 5,290 matched to a profile, 1,875 with a named company.

**An internal inconsistency I had created**
The co-invest chart still carried numbers computed before the sleeve was recalibrated — it showed
median 1.88x→2.83x and a 3% loss rate at twelve positions. Under the current calibration (sleeve
mean 2.20x, dispersion 1.45) the true curve is **median 1.31x→1.98x, with loss falling 39% at three
positions to 13% at twelve and 6% at twenty.** Chart, title, aria-label and takeaway all corrected.
The chart's source line now names the calibration anchor explicitly.

**Added:** a visible measured-versus-assumed panel above section 1, so a reader does not have to
open the model notes to see that all of section 6 rests on four assumptions, none of which the
evidence above establishes.

---

# Fourth pass: two assumptions tested against data, one of them fatal to a headline

## Persistence is 0.87, not the 0.50 we guessed — walk-forward tested

Fitted hit rates on seed/pre-seed entries 2019-2021, then scored the same investors on entries
2022-2023, 272 investors with at least 15 entries in the fit window and 10 in the test window.
Base rates: 7.99% fit, 3.22% test.

| Fit-window quartile | Fit lift | Forward lift |
|---|---|---|
| Top | 2.00x | **1.95x** |
| Second | 1.37x | 1.59x |
| Third | 1.00x | 1.16x |
| Bottom | 0.60x | **0.65x** |

Monotone, threefold top-to-bottom spread, correlation +0.30. Regression to the mean at the extreme
is mild: top decile 0.82, top 5% 0.86, **top twelve (our roster size) 2.65x -> 2.33x = 0.87.**
Model default moved 50% -> 85%, which raises the default fund from 2.74x/15.4% to **2.95x/16.5%**.

**But the aggregate persists where individuals do not.** Inside that top twelve, SV Angel went
3.31x -> 5.28x while Naval Ravikant went 2.35x -> 0.00x on 29 entries, and Ameet Patel 2.84x -> 0.00x
on 10. This is the empirical case for keeping estimation error in the model and for not concentrating.

Data: `backtests/walkforward_lift_validation.json`.

## The 22 convergence cases do not survive checking. Seven do.

Re-verified every case against the parsed round corpus:

- **7 confirmed** — Modus, Pax AI, Artemis, Filed, FirstWork, Candid Intelligence, freightmate AI.
  Median lead **8.7 months** (was 8.2 across the unverified 22).
- **1 reversed** — Paces. We claimed a +4-month lead; Soma's seed was **2022-06-02**, twenty-one
  months *before* our 2024-03-12 signal. The case runs the wrong way.
- 3 carry a Crunchbase date of exactly 2026-01-01 (year-granularity artifact): dmodel, 1849 Bio,
  Apex Compute. Lead times unusable.
- 3 name a manager the round record does not list: Boardy, Minerva, Petual.
- 4 absent from the corpus: Haplotype, Pepr, MindFort, Atum.

Absence from this corpus is not disproof — the original match used a different Crunchbase pull. But
none of it is quotable. **The page now claims seven, names all seven with both dates, and states in
full what the check discarded and what it reversed.** The per-manager share chart (Theory 18% etc.)
rested on the unverified set and has been removed.

This is the single most important correction of the session: the strongest claim on the page was
three times overstated, and it sat in the first section.
