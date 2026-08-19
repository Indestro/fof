# Nine defects in the Wing sourcing pipeline, found and fixed 2026-08-19

*Written from the 2026-08-18/19 weekly-selection run. Canonical copy here; pointers in
`~/.claude/skills/weekly-selection/SKILL.md` and `~/.claude/skills/wing-selection/SKILL.md`.
Read this before trusting any count the pipeline reports.*

**Governing thought.** A full weekly run produced 29 ES rows and 43 stealth-sheet selects, but
almost none of the elapsed time went to sourcing. Nine defects were found, and every one of them
was **silent** — each produced a plausible number rather than an error. Four of the nine
systematically *under-reported* selections, and two of those four were filters written by the
analyst rather than faults in the data. The lesson that generalises: in this pipeline a low count
is not evidence of a thin week, it is the most common symptom of a bug. **Sanity-check every
count against its historical baseline before reporting it.**

---

## A. Defects that silently discarded real candidates

### 1. The founder regex omitted "founding" — cost ~39 rows

The title filter was `founder|co-?found|^ceo\b|^cto\b|chief exec`. **"Founding Engineer" matches
none of it**: `founder` requires the trailing "er", `co-?found` requires a literal "co". Every
Founding Engineer / Founding Member / Founding MTS / Founding Designer / Founding Research
Scientist was dropped without trace, across four separate sweeps:

| sweep | rows lost |
|---|---|
| stealth-sheet (Stealth-Emrah) | 10 |
| talent-marker | 14 |
| departure | 9 |
| conference | 6 |

The single highest-scoring row in the entire Aug-21 batch was among them — **Cheng Sheng, z=15.56**
(above every "Founder"-titled row), ex-Google DeepMind eng lead, Founding Engineer at a stealth
health-AI company, comp $682,500. A founding-engineer package at that level is not title inflation.

**Correct pattern:**
`found(er|ing)|co-?found|^ceo\b|^cto\b|chief exec|first engineer|employee #?[12]\b`

**Aggravating factor: the rule already existed.** `wing-selection/SKILL.md` rule #2 has stated for
some time that founding engineers and founding MTS *are* picks for Wing, with an explicit
instruction to drop the "not THE founder = drop" gate. It was written as prose, never as a regex,
and the analyst both failed to load that skill and then argued the opposite position out loud when
cutting a Founding Research Scientist. **A selection rule that lives only in prose will be
violated. Encode it in the filter.**

### 2. The stealth-sheet read was capped at 400 of 1,911 rows — cost 24 selections

`Stealth-Emrah` was read as `A2:V400`. The tab holds **1,911 populated rows** (grid 2,231). The run
triaged 21% of the batch and produced 9 selects against a normal week of 20–35. The full-tab pass
immediately recovered 24 more, including the batch's second-highest row (Robby Walker, ex-Apple,
z=14.27) at row 34 — inside the first 400, but only reachable once the founding-title fix landed.

Use open-ended ranges (`A2:V`) or read `gridProperties.rowCount` first. **The tab also re-sorts
between reads** — row numbers are not stable identifiers; match on name. Weekly files live in
Drive › Wing VC › Weekly Sample Files as `Stealth Sample - <date> - Test`, ~8 MB each.

### 3. gh-watch was blind to 39% of its own pool

`gh_watch_daily.py` reads the founder LinkedIn from column G only. 96 ES rows (band 2530–2663) still
carried it in column F, left from the 2026-08-11 A–N schema migration. Measured against gh-watch's
own filters: **161 eligible tech founders, 89 visible, 62 invisible.** After migrating F→G the pool
went **81 → 151 → 168** and findings went **1 → 7** in a single run.

The same gap made those 96 people invisible to `selector_append.py` dedupe, which also keys on G, so
they could be re-added as duplicates indefinitely.

### 4. ffn-watch's decay was a state bug, not pool exhaustion

Daily counts fell 96 → 84 → 78 → 74 → 66 → 0 and were reported as the tier-A rotation running dry.
It was not. A profile that failed to fetch `continue`d **before** the state write, so it was never
stamped; the batch is sorted by last-checked date, so unstamped failures re-sorted to the head of
the queue every day and consumed the top of every run. The wall grows monotonically. 45 such slugs
had accumulated.

Fix: stamp failures too, with a `fail` counter, and drop after 3 strikes. **A timeout is not a
strike** — `subprocess.TimeoutExpired` means slow, not gone, and counting it evicts good people
(this nearly removed Kumar Chellapilla, ex-LinkedIn/Uber ML leadership).

---

## B. Defects that would have fabricated or destroyed data

### 5. `bulk_get_crunchbase_data` invents a Series A — a false-positive funding generator

When a URN has no Crunchbase match the tool returns a garbage fallback instead of an empty record.
Reproduced first-hand on four URNs; three unrelated companies returned the **identical** stub:

```
Industries: "Artificial Intelligence (AI), Biotechnology, Genetics, Pharmaceutical"
Last Funding Type: "Series A"    Last Funding Date: "2025-03-24"
Founded Date: "2018-01-01"
Investors: Leading Capital, Linchuang Sinan, Puxin Capital, Broadcom Ventures, DFJ DragonFund
Crunchbase URL: ".../organization/"   permalink: null
```

This is pointed straight at the weekly funding sweep. Unnoticed it would stamp "already funded,
Series A" on every genuinely unfunded stealth company — exactly inverting the signal we source on.

**A record is real only when `permalink` is non-null.** Treat every null-permalink response as NO
DATA — never as "no funding" and never as "funded". Funding claims must come from EDGAR full-text,
company/press sources, or an agent sweep.

### 6. `find_slot()` was about to overwrite a live row — third recorded instance

The slot finder skipped rows blank in F, G and V. A catch whose LinkedIn never resolved is
identified **only** by its X handle and name, so it read as empty. It selected row 2777 — Blossom
Okonkwo, written hours earlier. Prior instances: 10 rows on 2026-08-11, Ariso on 2026-08-14. Now
also requires H (x_url) and L (founder) blank. **Any future "identified only by X" column reopens
this hole.**

### 7. psel3 cut notes at the first `·` — scored 0 of the highest-volume sources

`re.sub(r"·.*$", "", notes)` was meant to strip trailing metadata. But `·` is a general separator,
and the wing-x/yc-sweep format is `Wing-fit N · <GP> — <substance>`, so a 233-character note was
truncated to `Wing-fit 3` (10 chars) and skipped as "too thin to score". Every row produced by the
daily crons — the two highest-volume sources in the sheet — had been silently unscored.

Strip only known trailing markers, and never strip a note down to nothing (a single-segment note
beginning `COMPANY SIGNAL:` was the second failure mode, introduced by the first fix).

---

## C. Source-quality defects — the signal itself is weaker than labelled

### 8. Talent markers: two false-positive modes

The marker sweep matches keyword text anywhere on a profile. Markers are proxies for *a selection
event someone else ran* (Thiel, Rhodes, SAIL admission). Two things defeat that:

- **Executive-ed certificates.** "AI @ CMU" resolved to a non-degree CMU SCS professional
  certificate, alongside a Purdue GenAI certificate and a "Stanford Visiting Student" line. A
  certificate is a *purchase*, not a selection — it carries none of the signal.
- **Institution-name collisions.** "Marshall Scholar" matched **USC *Marshall School of Business***.
  Silent, because nothing on the profile looks wrong.

Same shape to watch: Stanford ACM (a club), *Sloan Research Fellow* vs *MIT Sloan*, "MIT Media Lab"
in a course line. Prize/fellowship markers are much harder to fake than institution-shaped ones.

**A third mode surfaced in the conference sweep: workshop vs main track.** Only 2 of 6 finalists had
main-track authorship; the rest were workshop-tier and three wrote it without the word "workshop".
One credit was **last-author from the org the person directed** — an executive-sponsor line, not
research output.

### 9. The departure sweep mis-attributes the employer ~50% of the time

Of six verified finalists, **three org tags were outright false and a fourth was materially
inflated**; only two were clean.

| person | tag | reality |
|---|---|---|
| Shubham Goel | ex-Figure | Figure appears **nowhere**; he is ex-CEO of Affinity CRM |
| Fausto Ibarra | ex-Scale AI | false — ex-VP/GM Nubank, ex-CPO Kueski |
| Arnav Mohan | ex-Anthropic | false |
| Vincent Alessi | ex-Anthropic/OpenAI | contractor-level, and still **current**, not "ex" |

`--keywords="stealth ex-<Org>"` matches the string anywhere — skills, recommendations, a
recommender's employer, aspirational text. The sweep's core claim is therefore unverified by
construction, and it is the only thing that makes the row interesting. **Confirm the org appears
with an END DATE inside the claimed window**, using the profile fetch already run for the
age/fake-profile gate.

---

## D. Contamination traps to hard-code

Three shared LinkedIn company URNs are catch-all pages, not companies. Joining on them attributes
one entity's data to unrelated people and, combined with defect #5, manufactures fake rounds.

| URN | title | what it actually is |
|---|---|---|
| 18583501 | "Stealth Startup" | *"Submit your information here so investors can find you: harmonic.ai/get-discovered"* |
| 96670793 | "Stealth AI Startup" | *"Founders tag themselves here to receive inbound interest from early-stage VCs"* — ~8,251 self-tagged members |
| 79372457 | "Stealth" | a **typo slug** `/company/steath/` that resolves to **TimelyAI**, an unrelated marketing SaaS |
| 91194134 | "Something new" | 42 unrelated people |

**This inverts the stealth inference.** We read a stealth tag as someone trying *not* to be seen. On
these pages it is a founder advertising to VCs — a marketing act that self-selects for people
already running a raise. It does not make them bad leads, but it removes the "we found them early"
edge that justifies the sweep, and the tag carries no information about the company at all.

Namesake decoys encountered the same day, all requiring a primary source to resolve: three distinct
companies named **Tenor** (the YC S26 one is `heytenor.com`; `tenor.com` is the Google GIF company);
two named **Proper Motion** (one a dance company, one a Redmond science-exhibits firm — neither the
ex-OpenAI startup); **Piris Labs** as a same-lane decoy for a photonics founder.

---

## E. Verification-tooling notes

- **Add OpenAlex** (`api.openalex.org/authors?search=`) to the standard publication check. DBLP and
  Semantic Scholar both returned nothing for a founder who had a NeurIPS workshop paper and an
  ICASSP 2026 paper. They systematically drop workshop and industry tracks — precisely where this
  population publishes — so "no publication record" from those two is a false negative.
- **Read author position.** Last-author from one's own org is a sponsorship credit.
- **Known fetch failures that produce false negatives:** Crunchbase person pages 403 to bots;
  x.com returns 402; WebFetch reports "not present" on large conference/techcommunity pages where
  raw `curl` + grep finds the string verbatim. Never conclude absence from these alone.
- **WebSearch budget is 200 calls per session, shared with every subagent.** Four verification
  agents drained it. Raise via `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`.
- **Sales Nav `flagshipProfileUrl` hydration currently returns null** for every profile, so
  profileId/authToken pairs cannot be converted to public slugs without an in-network view.

---

## F. What the run actually produced

29 ES rows (2778–2806), 43 stealth-sheet selects, 19 of 20 sources run. Highest-conviction:

| lead | why |
|---|---|
| **Cheng Sheng** | z=15.56, top of the batch; ex-Google DeepMind eng lead; $682.5k founding-engineer package |
| **Robby Walker** | ex-Apple, z=14.27 |
| **Shubham Goel** | Affinity CRM co-CEO ($600M valuation), pre-raise; found by two independent sweeps |
| **Rajesh Shenoy** | P(T1) 0.93; surfaced by Duke #366 **and** the AI@CMU marker sweep the same day |
| **Ian Fasel** | Emotient → Apple exit, verified on Emotient's own archived page; advertising the raise |
| **Avinash Mani** | left MatX's CDO-Silicon seat four months after its $500M Series B |

**Two-source convergence was the single best-performing signal shape of the run** — Shenoy, Goel and
Cheng Sheng each arrived via uncorrelated sources, and all three sit at or near the top on
independent measures.
