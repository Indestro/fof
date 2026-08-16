# The preceder list ranks volume, not skill — and the sector data says where to point the sensor next

Two of Yasin's sheets landed on 2026-08-16: **Top Preceders**
(`1TnXzrqItZqXhFT5HzUOAqZFFgi5GVYc31t6uXQznCGQ`) and **cat_stats**
(`1tlPGR28pqi6h4fuhNNYLbx7IPmzY91tRiXNzSjezTqg`, 19 tabs). Both change what we do next.

## The list is sorted by deal count, and its two score columns are the same number twice

`Success Rate (%)` divides every investor by the same constant. 326 / 12.49% = 2,610, and
149 / 5.71% = 2,610. The denominator is the total count of tier-1 companies, not the investor's
own deal count — so the column measures **market share of tier-1 companies touched**, not hit
rate. `Investment Quality Score` is then n x that share, i.e. n²/2,610, which is monotone in n.
The three columns therefore carry one piece of information between them: how many deals the
investor did. Rank 1 to 50 is raw volume, top to bottom.

That is why the podium is Y Combinator, Alumni Ventures, and Liquid 2 — the highest-volume seed
platforms in the market. An investor who writes 2,254 seed checks precedes tier-1 rounds more
often than one who writes 40, whether or not they are any good at picking.

## Re-ranked by rate, the list nearly inverts

Denominator: each investor's own seed and pre-seed entries, 2019-2023, with a fixed 24-month
window for a **new** tier-1 investor to arrive (one not already in the round). Base rate on that
definition is **5.88%** across 26,636 companies. Shrunk toward base at prior strength 25.
Full table in `backtests/yasin_preceders_reranked.json`.

**Fell:**

| Investor | His rank | Ours | Seed entries | Raw | Lift |
|---|---|---|---|---|---|
| Y Combinator | 1 | 25 | 2,254 | 8.3% | 1.41x |
| Alumni Ventures | 2 | 26 | 279 | 7.9% | 1.31x |
| Pioneer Fund | 4 | 37 | 162 | 6.2% | 1.04x |
| Soma Capital | 5 | 32 | 177 | 7.3% | 1.22x |
| Edward Lando | 7 | 24 | 174 | 9.2% | 1.49x |
| Pareto Holdings | 8 | 23 | 191 | 9.4% | 1.53x |
| **Gaingels** | 9 | 38 | 106 | 4.7% | **0.84x** |
| Nadav Ben-Chanoch | 18 | 41 | 75 | 1.3% | **0.42x** |
| Goodwater Capital | 46 | 40 | 193 | 2.1% | **0.43x** |

Gaingels, Ben-Chanoch and Goodwater sit **below** the base rate. A company they seeded is *less*
likely to attract a new tier-1 investor within two years than a randomly chosen seeded company.
On a volume-ranked list they read as strong signals; they are mild negative ones.

**Rose:**

| Investor | His rank | Ours | Seed entries | Raw | Lift |
|---|---|---|---|---|---|
| SV Angel | 37 | 1 | 151 | 26.5% | 4.01x |
| Nat Friedman | 42 | 7 | 15 | 26.7% | 2.33x |
| Dylan Field | 43 | 12 | 26 | 19.2% | 2.16x |
| A\* (Kevin Hartz) | 27 | 5 | 51 | 17.6% | 2.34x |
| A.Capital Ventures | 32 | 6 | 51 | 17.6% | 2.34x |
| Everywhere Ventures | 41 | 15 | 113 | 12.4% | 1.91x |
| Asymmetric Capital | 45 | 18 | 17 | 17.6% | 1.81x |
| Mandeep Singh | 39 | 14 | 20 | 20.0% | 2.07x |

**What to do with it.** Use the rate ranking as the sensor's edge weight, and keep Yasin's counts
as the coverage weight — they answer different questions and both are needed. An investor with a
2x rate and 15 entries fires rarely; YC at 1.41x on 2,254 entries fires constantly. The sensor
wants the product, the FoF roster wants the rate.

## Where the front-run window actually exists, by sector

`speed data` measures days from seed date to Series A separately for preceders and for tier-1
firms. The difference is the front-run window: how much earlier the preceder layer gets in.
Joined to tier-1 deal-count growth from `TierOne Chart 24-25`:

| Sector | Preceder window | T1 deals 24 -> 25 | Median T1 check 2025 |
|---|---|---|---|
| Energy | +270 d | 29 -> 23 | $35M |
| Cybersecurity | +145 d | 70 -> 73 | $26M |
| DevOps | +137 d | 18 -> 14 | $20M |
| Infra | +122 d | 117 -> 110 | $49M |
| **Aerospace** | **+113 d** | **28 -> 41** | **$50M** |
| B2B | +113 d | 284 -> 317 | $23M |
| Health | +50 d | 178 -> 177 | $39M |
| Consumer | −19 d | 125 -> 103 | $24M |
| Robotics | −158 d | 9 -> 12 | $50M |
| Crypto | −181 d | 17 -> 20 | $15M |

**Aerospace is the extension to make.** It is the only sector with a wide preceder window *and*
tier-1 demand rising — deal count up 46%, the largest proportional jump on the board, with the
median check going $20M to $50M. Tier-1 firms are arriving in force and still arriving late.

**Negative windows are a finding, not noise.** In robotics and crypto the tier-1 firms are at
seed *before* the preceder layer. A preceder-based sensor has no edge in those sectors because
there is nobody to front-run — build coverage there some other way, or not at all. (Caveat: the
robotics and crypto cells rest on 9-20 tier-1 deals; agriculture's −2,112 days is 3 deals and is
noise, not signal.)

**Our home lane is compressing.** Infra shows a +122-day window, but tier-1 days from seed to
Series A fell from 481 to 283 year over year — the sharpest acceleration of any sector. The
8.6-month median lead we measured across the whole signal log will shrink fastest exactly where
we source hardest.

## Selection bias this makes visible

Our 5,329-founder log is sourced through Wing's lanes — AI infra, data, cloud, cyber, enterprise,
health/bio. Consumer, fintech, crypto, space and defense are absent from the denominator. Two
consequences, and only one is a problem:

- The manager front-run table (`backtests/manager_t1_frontrun.json`) runs on the full round corpus
  and is lane-neutral. It is fine.
- The **convergence** metric is Wing-conditional by construction. Pebblebed's 1-of-55 measured
  what we do not look at, not Pebblebed. Relabel it: it scores "share of book inside Wing's
  thesis," not manager quality.

A fund-of-funds picks its own sectors. The sweep is already surfacing managers in the lanes we
are blind to — Chapter One and Volt in crypto, Slow in consumer, **Jackson Moses / Silent Ventures
in defense** at 2.70x. Moses is the cleanest first extension: defense-native, already in
`quiet_coinvestors.json` as a Quiet co-investor, still writing.
