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
