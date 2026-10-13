---
type: system-doc
supersedes: none — new layer, sits alongside the five-layer system (same relationship as Layer 4a and the concentration tracker)
version: 1.0
created: 2026-10-13
last-review: 2026-10-13
tags:
  - investing
  - cse
  - system
  - forward-case
  - pattern-recognition
---

# Layer 6 — Forward Developments & Pattern Overlay
*Version 1.0 — 2026-10-13. Raised by Kaveen: the arithmetic layers price only what has already been earned, and they cannot see a pattern that runs across a group of companies. Both criticisms are correct. This layer fixes them without letting either one contaminate the floor.*

---

## 0. The one rule that makes this safe

**Layer 6 may never set or move a floor, a second tranche, or a ceiling.** Its outputs are (a) a labelled *forward-case band*, (b) an *attention ranking* (which file to open first and what to look for), and (c) a *promotion list* (what evidence would move a forward item into sustainable EPS, and therefore into the ceiling through the normal Layer 4 route). It sits beside Layer 4a on the same terms: it may inform *where to look and what to ask*, never *what the number is*.

Why this matters: the system's discipline came from a failure mode named in the JKH file — narrative-driven buying. A forward story is exactly the thing that failure mode feeds on. The way to take the future seriously without repeating it is to make the future *explicit, staged and falsifiable*, rather than letting it leak into the multiple.

---

## 1. Part A — Forward developments register (per company)

Every research file gets one short section, **"Forward developments"**, with one row per development:

| Field | What goes in it |
|---|---|
| Development | What happened or was announced, with source and date |
| Stage | **Announced** (weight 25%) → **Commissioned / started** (50%) → **Ramping, first segment data visible** (75%) → **Proven, two consecutive quarters of segment evidence** (100%) |
| Size | The disclosed number (capex, capacity, contract value). If nothing is disclosed, say so — do not invent it |
| Incremental earnings | A low / base / high range with every assumption printed (return on invested capital, utilisation, tax rate, share count). The base case defaults to the **company's own current return**, not an optimistic one |
| Falsifier | The specific filing line that would show the development is not working, and when it will be visible |
| Check date | The interim or annual report where it will first be testable |

**Forward EPS = sustainable EPS + (stage weight × base-case incremental EPS).**
**Forward-case ceiling = forward EPS ÷ hurdle.** It is printed beside the Layer 4 ceiling, clearly labelled *forward case — not a trading level*.

Stage weights are judgement, shown openly so they can be argued with. They exist to stop an announcement being priced like a delivered result.

**Promotion rule.** A forward item enters sustainable EPS only when it reaches *Proven*: two consecutive quarters of segment-level evidence in primary filings. At that point the Layer 4 ceiling moves through the normal trigger route (a confirmed sustainable-EPS shift), and the item is removed from the register.

---

## 2. Part B — Pattern register

A pattern is a hypothesis about a company or group that the single-company arithmetic cannot see. Each pattern gets one entry:

| Field | What goes in it |
|---|---|
| Statement | One sentence, e.g. "Hayleys-group names trade at a persistent premium to their own hurdle-based ceilings" |
| Universe and evidence | Which names, at what dates, and the numbers |
| **Competing explanation** | Required. The most plausible reason the pattern is *not* a market mispricing (e.g. my sustainable EPS is too conservative for that name) |
| **Pre-registered falsifier** | Written *before* looking at the next data point: what outcome would show the pattern does not apply |
| Status | Hypothesis → Supported → Falsified. Never "Confirmed" |
| Review date | The next filing or date at which the falsifier can be read |

Rules:
1. **A pattern can rank, never price.** It tells me which file to open first and what to test. It cannot lift a ceiling.
2. **Dispersion inside a group is first a model-error test.** If one member's premium is much smaller than its peers', first ask whether my sustainable EPS for that name is the reason — rebuild the premium on the market-implied EPS (price ÷ neutral P/E) before reading it as an opportunity.
3. **A pattern that rests on price alone is not evidence.** It needs a mechanism that shows up in filings (group financing, dividends, asset values, export mix), otherwise it is momentum.
4. **No pattern justifies a buy below the floor rule.** Entry is still floor and second tranche; the concentration cap still binds, and a group-premium cluster is already a named cluster in the tracker.

---

## 3. Part C — The market-implied EPS test (use this first on any premium)

Before treating a premium to the ceiling as mispricing or as opportunity, compute:

**Market-implied EPS = price ÷ neutral P/E (= price × hurdle).**

Then compare it against (i) sustainable EPS, (ii) the latest quarter annualised, and (iii) the latest quarter annualised with obvious non-recurring items normalised (treasury income, FX, one-off gains). If the implied EPS sits close to (iii), the premium is the market capitalising the current run-rate — a question about the run-rate's durability, not a separate premium. If implied EPS sits far above every earnings measure, the premium is carrying something the arithmetic cannot see, and that is the case where Part B and a mechanism search are warranted.

---

## 4. First application — DIPD (13-Oct-2026), and the Hayleys-group premium pattern

### 4.1 Market-implied EPS and the group table (prices 30-Jun-2026; Q1 FY26/27 annualised ×4)

| Name | Price | Sustainable EPS | P/E on sustainable | × neutral (8.22) | Premium to ceiling | P/E on Q1 annualised |
|---|---|---|---|---|---|---|
| DIPD | 58.50 | 5.80 | 10.1× | 1.23× | ~23% | **7.1×** |
| HAYC | 175.00 | 12.15 | 14.4× | 1.75× | ~72% | 11.8× |
| HAYL | 238.00 | 17.36 | 13.7× | 1.67× | ~65% | 13.0× |

DIPD's market-implied EPS is 58.50 × 0.1217 = **Rs. 7.12**. DIPD's Q1 EPS annualised is 8.24, but Q1 finance income more than doubled (Rs. 593.9mn vs 284.4mn); normalising it to last year's level gives an annualised EPS of about **Rs. 6.93**. Price ÷ 8.22 on that figure ≈ 56.9 — within 3% of the 58.50 price.

### 4.2 What this says about the pattern

- **DIPD's premium to its ceiling is almost fully explained by the Q1 run-rate**, with no unexplained "group premium" left over. The market is pricing DIPD at roughly 7.1× EPS that it earned in the latest quarter, not at a multiple above neutral.
- **The unexplained premium sits in HAYC and HAYL.** HAYC at 14.4× sustainable and 11.8× even on its (FX-flattered) Q1 run-rate, and HAYL at 13–14×, are the names carrying a premium the earnings arithmetic cannot account for. That is where Part B (mechanism search) belongs.
- **So "DIPD can catch up to its peers" is not supported by the table.** DIPD is the *cheapest* of the three on every basis. The honest framing is the reverse of the catch-up idea: DIPD's upside, if any, depends on whether the Q1 run-rate persists and on the forward case below, not on peer premiums closing. If the peers' premium is a mispricing, it argues for caution about the group, not for DIPD rising to meet it.
- Caveat on the 47% figure Kaveen quoted: that implies a price near 67–70 (against the old or new ceiling), which I have not seen. At 67, market-implied EPS is 8.15, i.e. the full unadjusted Q1 annualised run-rate, with finance income at its Q1 peak and no allowance for seasonality. Send the current price and I will rerun §4.1.

### 4.3 DIPD forward developments register (first entry)

| Field | Entry |
|---|---|
| Development | Katunayake EPZ glove plant commenced operations 8-Oct-2026; investment Rs. 4.2bn; CSE disclosure dated 12-Oct-2026 |
| Stage | **Commissioned / started — weight 50%** |
| Size | Rs. 4.2bn (≈11% of Group PP&E, ≈9% of equity, ≈24% of Q1 debt). **No capacity, utilisation, funding or revenue disclosed** |
| Incremental earnings (assumptions printed) | PBT = Rs. 4.2bn × pre-tax return; tax 25%; 598.7mn shares (Q1 PAT owners ÷ Q1 EPS). **Low:** 0% return (start-up cost, depreciation and lost interest capitalisation offset volume) → +0.00. **Base:** 8% (≈ the Group's own current return on capital) → +0.42. **High:** 15% (export-grade plant, full utilisation) → +0.79 |
| Forward EPS / forward-case ceiling at 50% weight | Low 5.80 → **47.7**; Base 6.01 → **49.4**; High 6.19 → **50.9** |
| If the item reached "Proven" (100%) | Base 6.22 → 51.1; High 6.59 → 54.1 |
| Falsifier | Q3 FY26/27 (Oct–Dec) Hand Protection segment PBT margin not improving while Group finance costs and depreciation rise; or interim notes showing the plant debt-funded at short-term rates |
| Check date | Q3 FY26/27 interim (Feb 2027); cost side visible first |

**Read:** on stated assumptions the plant moves the ceiling by 0–3 rupees. It does not close the gap to 58.50. The gap is carried by the Q1 run-rate, not by Katunayake. Layer 4 ceiling unchanged: 47.50–47.75.

### 4.4 Pattern register — first entries

**P1 — Hayleys-group premium.** *Statement:* HAYL, HAYC (and, in the earlier files, ALUM, SINS, SERV, MGT) trade at a persistent premium to their hurdle-based ceilings; the premium is larger than earnings quality alone explains. *Evidence:* §4.1 for HAYC and HAYL; the other four from their own files (not re-run here). *Competing explanation:* my sustainable-EPS estimates for these names are too conservative (two-to-five-point averages in a recovery year); the market is capitalising run-rates I have deliberately not adopted. *Falsifier (pre-registered):* if HAYC's and HAYL's next two interims confirm run-rate EPS at or above current Q1 annualised levels, and their premiums to the *forward-adjusted* ceiling narrow below ~30%, the premium was run-rate pricing, not a group effect. *Status:* Hypothesis. *Review:* HAYC and HAYL Q2 interims. *Open:* DIPD does **not** show the premium once the run-rate is used, which is itself a data point against a pure group-effect reading.

**P2 — DIPD is the cheapest Hayleys-group name on market-implied EPS.** *Statement:* on every earnings basis DIPD trades at the lowest multiple of the three names tested. *Competing explanation:* Plantations (38% of revenue, contracting) and the debt/finance-cost build are why the market discounts it. *Falsifier:* Q2 finance costs growing faster than +48% YoY, or Plantations PBT falling past −10%, would remove the discount's mystery. *Status:* Hypothesis. *Review:* DIPD Q2 FY26/27 interim.

---

## 5. How this changes the working routine

- **Every file touched** gets a *Forward developments* section and, where relevant, a link to the pattern register entry. Existing files are retrofitted when next opened, as with Layer 3a — no backfill sweep.
- **Every premium to ceiling** gets the Part C market-implied EPS line before it is described as expensive or cheap.
- **Attention ranking:** when several watchlist names are open, order them by (a) distance to floor, (b) the date of their next falsifier, (c) forward-case ceiling vs price — in that order. Forward case is the third tiebreak, never the first.
- **Nothing here changes any held position's rules.** KHL, LIOC, JKH and JXG levels are unchanged by this layer.

## 6. What this layer deliberately does not do

- Does not raise any ceiling or lower any floor.
- Does not turn announcements into earnings; the 25/50/75/100% weights are a discipline, not a forecast.
- Does not treat a group pattern as a reason to buy a name that fails the floor test.
- Does not replace reading the annual report: the largest remaining gap in the DIPD file (a multi-year EPS series) is still the thing that would settle whether 5.80 or ~7 is the better base.

---

*One-line version: the floor says what the business has earned; this layer says what it might earn next and which hunches deserve testing — and keeps the second from ever quietly becoming the first.*
