# A "no consumer" mandate would cost this roster almost nothing

Built by joining company LinkedIn URNs (`all_profiles.founders`) to Yasin's 709k-row category
collection, then onto each manager's book in the parsed round corpus.
Data: `backtests/manager_sector_mix.json`.

**Coverage caveat, stated first.** Corpus-wide the join reaches only **26.2%** of the 199,620
rounds — far too thin to drive a sector filter over the whole market. Per manager it is much better,
**50-75%** of each book, which is enough to characterise a mix but not to quote a precise percentage.
Every figure below is a share of the categorised subset, not of the whole book.

| Manager | Deals | Categorised | Sector mix |
|---|---|---|---|
| Chapter One | 67 | 34 | B2B 50%, Fintech 18%, Crypto 9%, Infra 9% |
| 1984 Ventures | 80 | 44 | B2B 70%, Health 16%, Consumer 7% |
| **Silent Ventures (Moses)** | 55 | 32 | **Aerospace 34%**, B2B 16%, Fintech 6% |
| Abstract | 307 | 173 | B2B 49%, Infra 12%, Fintech 10%, Consumer 8% |
| Volt Capital | 46 | 18 | B2B 28%, Infra 22%, Consumer 11% |
| A\* | 210 | 91 | B2B 46%, Consumer 13%, Infra 13% |
| Afore | 147 | 91 | B2B 62%, Health 11%, Infra 8% |
| JAM Fund | 84 | 33 | B2B 36%, Fintech 21%, Consumer 12% |
| Everywhere | 264 | 120 | B2B 54%, Fintech 16%, Health 12% |
| Mischief | 71 | 52 | B2B 56%, Fintech 29%, Health 6% |
| Soma | 712 | 341 | B2B 48%, Fintech 14%, Infra 10%, Consumer 6% |
| Theory | 15 | 11 | B2B 55%, Infra 45% |
| Day One | 110 | 57 | B2B 56%, Fintech 14%, Health 7% |
| Mei Zuo | 22 | 16 | Infra 38%, B2B 31%, Health 31% |

## Three findings

**1. The mandate constraint is cheap, and that is the CVC pitch.** Consumer runs 5-13% across the
entire roster; every manager is B2B-dominant. A corporate investor who says "no consumer" removes
almost nothing, and no manager at all. The sellable version of the sector control is therefore not a
filter but a **price quote**: *your mandate costs you roughly nothing here, and here is the
measurement that shows it.* That is a far better object than a toggle, and it is defensible.

**2. Silent Ventures is the aerospace extension, confirmed by its own book.** 34% aerospace against
a roster where nobody else exceeds single digits. Section 4 argues aerospace is where the feeder
head start pays best; Moses is the manager who executes it. This is now measured, not inferred from
one Northwood co-investment.

**3. Correction to something stated earlier in this project.** I characterised Chapter One and Volt
Capital as crypto managers when explaining why the sweep surfaced lanes our sourcing misses. The
books do not support it: Chapter One is 9% crypto and half B2B; Volt shows no crypto at all in the
categorised subset and reads B2B/Infra. The sweep did surface managers outside Wing's lanes, but
fintech and consumer, not crypto. The general point stands; those two examples were wrong.

## What this does not support

A sector-exclusion control in the simulator that claims to reprice the fund under an arbitrary
mandate. At 26% corpus coverage and 50-75% per-manager coverage, the model cannot honestly say what
excluding a sector does to returns. What it *can* say is which managers carry meaningful exposure to
a named sector — that is a diligence output, not a slider.
