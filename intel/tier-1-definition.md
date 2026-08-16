# The tier-1 list is now fixed, and our measured list agrees with two thirds of it

**Canonical definition (2026-08-16):** the 29 firms Emrah hand-picked in the "Tier One List"
sheet (`18xv96q_Z9f-8_jAKMTj4WqZ1g5BdK3aIbT8yyTWseEM`, tab *Tier 1 List*, `Select = TRUE`),
drawn from a 175-firm universe. Stored at `~/sourcing/t1-sensor/t1_canonical_handpicked.json`.

Accel · Andreessen Horowitz · Benchmark · Bessemer · Coatue · CRV · Felicis · First Round ·
Founders Fund · General Catalyst · Greylock · GV · Iconiq · Index · Insight · IVP · Khosla ·
Kleiner Perkins · Lightspeed · Lux · Menlo · NEA · Norwest · Redpoint · Sequoia · Spark ·
Thrive · Tiger Global · Union Square

## Yasin's corpus already uses this definition

The `has_tier_1_investor` flag on `eyup_test.cb_funding_rounds_parsed` (199,620 parsed rounds)
agrees with the hand-picked list on **98.7% of 40,000 rounds** tested. The residual is a short
tail of firms his flag counts and ours does not — Battery (265 rounds), 8VC (160), Meritech (57),
SoftBank (19). Nothing structural. **Consequence: we can query the flag directly instead of
re-deriving membership, and our backtests and his model share one definition of the label.**

## Our measured live-T1 list agrees on 20 of 29

`t1_live_list.json` was derived bottom-up — firms that *led* Series A/B rounds in the 294-company
unicorn cohort of the last twelve months. After alias fixes (GV, NEA, Tiger Global), 20 names
appear on both lists. The two nine-name disagreements are informative, not errors.

**On the hand list, absent from ours:** CRV, Coatue, Felicis, Greylock, Iconiq, IVP, Norwest,
Thrive, Union Square. Four of these — Coatue, Iconiq, IVP, Thrive — are growth firms that write
Series C and later, so a list built from *A/B lead slots* structurally cannot see them. The other
five (CRV, Felicis, Greylock, Norwest, USV) carry the brand but led few or no A/B rounds into the
last twelve months of unicorns. That is a real finding about who is currently converting, and it
is exactly the fund-cycle state the sensor should track rather than a reason to drop them.

**Measured live, off the hand list:** Altimeter, B Capital, Caffeinated, CapitalG, Eclipse,
NVIDIA, Premji Invest, Temasek, Valor. Most are crossover, sovereign, or corporate money —
Emrah's list is deliberately a *venture* list. Caffeinated is the one genuine early-stage omission:
it ranked #10 by A/B lead volume in the cohort.

## How each list gets used

- **Label for backtests and models:** the hand-picked 29. It is the definition Yasin's corpus
  already encodes, so results stay comparable.
- **Sensor target set:** the measured list, refreshed. A firm that stops leading A/B rounds is a
  fund-cycle state, and the crossover names tell us who is arriving late in a company's life.
- **Never merge them into one number.** They answer different questions: *who is prestigious*
  versus *who is currently buying*.
