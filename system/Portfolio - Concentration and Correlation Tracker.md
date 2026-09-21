---
type: system-doc
supersedes: none — new file, sits alongside the five-layer system as a portfolio-level (not per-stock) check
version: 1.2
created: 2026-09-19
last-review: 2026-09-21
tags:
  - investing
  - cse
  - system
  - portfolio-risk
  - concentration
---

# Portfolio — Concentration & Correlation Tracker
*Version 1.2 — 2026-09-21. Every existing layer of the system operates per-stock. This file is the one place that looks across the whole book at once: how much of the actual capital is riding on the same underlying macro driver, dressed up as different tickers — and, corrected this version, how much is riding on just one ticker outright.*

> **Correction from v1.1, found 19-Sep-2026 (Kaveen):** the original cap was written only for correlated clusters — two or more tickers sharing a driver. That left out the degenerate case: a single ticker held alone *is* a cluster of size one, and the same ≤50%-of-total-invested-capital ceiling has to bind on it directly, not just on multi-ticker clusters. §3 is rewritten to state both cases as one rule. §1/§2 are updated with LIOC and a **live breach under the corrected rule** — see §2a.

---

## 0. Why this exists

Layer 4/5 discipline (floor, second tranche, max ½ cash per name) already caps how much goes into any *one* ticker. Nothing in the system caps how much goes into one **driver** wearing several tickers. The vault's own queue makes this concrete: seven of the fifteen tracked names (HAYL, DIPD, HAYC, ALUM, SINS, SERV, MGT) are Hayleys-linked and have, so far, moved together as a group-wide valuation premium — buying two of them isn't diversification, it's one bet twice. The only existing rule of this kind in the vault is narrow and single-purpose: JXG's file caps future JINS orders against a shared Janashakthi-group exposure. This file generalizes that instinct into a standing check.

**This file does not replace anything.** It runs *after* Layer 4/5 clears a name for purchase, as the last check before capital actually moves, and again at any standalone portfolio review.

---

## 1. Live position table

*(Update this table at every portfolio review — it is the one place actual position sizes live outside the individual research files' own thesis logs.)*

| Ticker | Shares | Avg cost | Cost basis | % of total invested | Primary driver | Secondary driver |
|---|---|---|---|---|---|---|
| JXG | 800 | ~9.04 effective | ~7,232 | ~32% | Rate-cycle via First Capital Holdings (bond trading gains/losses) | JINS embedded-value/equity-book mark |
| JKH | 100 | 20.53 | ~2,053 | ~9% | Retail/EV mean-reversion + Leisure financing-phase drag | Tourism/oil-Hormuz war-windfall (Transportation), LKR/CODSL loan |
| LIOC | 100 | 132.97 | ~13,297 | **~59%** | Fuel retail margin / oil-price pass-through | Concessionary-tax dependency, CPSTL governance limitation |
| SUN | 0 (closed) | — | — | — | — | closed 13-Aug-2026, realized −10.37% |
| **Total invested** | | | **~22,582** | **100%** | | |

**Cash / uncommitted:** not tracked in this file — pull from the trade-logging chat before relying on this table for a sizing decision.

---

## 2. Driver-overlap read on the current book

**JXG vs. JKH — soft overlap, not a hard one.** Both carry *some* interest-rate sensitivity (JXG directly via FCH's bond-trading book; JKH indirectly via Financial Services' Union Assurance stake and its own thin interest cover, 2.5×) — but it is a secondary factor for JKH, not the primary one, and their dominant drivers (JXG: rate-cycle; JKH: Retail/EV + tourism/war-windfall + Leisure recovery) are genuinely different. **Read: acceptable overlap, not a cluster.** Worth re-checking if either file's dominant-driver framing changes.

**Verdict on cluster overlap: no correlated-cluster breach.** This part of the check exists mainly for what it will need to catch next, not because the current book has a cluster problem.

---

## 2a. Live breach — single-name ceiling (LIOC)

LIOC shares no cluster with anything else in the book — it's the deliberately-unrelated control case in its own research file, and that finding still holds. But the *cluster* test was never the only test. **LIOC alone is ~59% of total invested capital** (~13,297 of ~22,582, cost basis, as of the 19-Sep-2026 first-tranche fill) — a single name, on its own, past the same ≤50% ceiling the cluster rule was always meant to enforce (§3).

**Per the confirmed breach protocol:** the position is kept as-is, not unwound. The only consequence is that the standing **second LIOC tranche (122.50) is paused** — no further LIOC buys — until LIOC's share of total invested capital falls back to ≤50%, whether that's from new capital going into other names or LIOC's relative weight declining on its own.

---

## 3. The rule — concentration cap (single names and correlated clusters, stated as one rule)

**No single company — whether represented by one ticker held alone, or by a correlated cluster of tickers sharing a primary driver — may exceed 50% of total invested capital.**

A lone ticker with no correlated peers is not exempt from this; it's a cluster of size one, and the same ceiling binds on it directly. This is the corrected, complete statement of the rule — the multi-ticker version below is the special case where the cluster has more than one member, not a separate rule.

Named driver-clusters already visible in the vault, to check against before any new buy:
- **Hayleys-group ownership premium** — HAYL, DIPD, HAYC, ALUM, SINS, SERV, MGT. Confirmed in every one of these files' own verdicts: each trades at a large, independent premium to its own hurdle-rate ceiling, and the premium's persistence *across* the group (not just within one name) is the standing hypothesis LIOC was built specifically to test. Buying a second name from this list is not diversification within the book.
- **Rate-cycle / bond-yield sensitivity** — JXG (via FCH), AAIC, UAL, JINS (insurers, duration/reinvestment plays). All four are explicitly the same Layer 2 sector thesis in this vault, just expressed with different torque.
- **Tourism/Hormuz-Middle-East war-windfall** — JKH (Transportation tailwind + Leisure/tourism drag, opposite signs, same regime), KHL (same regime, hospitality side only).

**Cap, restated on a total-invested-capital basis:** a company or correlated cluster, in aggregate, may not exceed 50% of total invested capital — measured against the whole portfolio's cost basis, not just against available cash for a single new order. This is stricter than (and supersedes, for this specific test) Layer 5's "max ½ of available cash into one name" framing, which only governs the sizing of a single new purchase at the moment it's placed — it says nothing about what the position grows to represent afterward as the rest of the portfolio changes. This file's job is exactly that after-the-fact, whole-portfolio view.

**This is a generalization of an existing rule, not a new one.** JXG's file already states the JINS-specific version of the cluster case; this section is that same logic written once, for every cluster *and* for any single name on its own, instead of re-derived per file.

---

## 4. When this file actually bites — and the real timing constraint

**Not dormant — one live breach.** LIOC alone breaches the single-name ceiling as of 19-Sep-2026 (§2a). The cluster-cap side (§3's multi-ticker case) is clear: no two open positions currently share a primary driver.

**Honest limitation, named rather than glossed over:** orders are placed as limit orders at the broker, independent of this chat — Kaveen executes, then logs the fill here afterward. There is no point at which this file can sit between a decision and an order the way §4's original framing implied ("checked before any new buy") — by the time a fill is logged, the trade has already happened. A cap check that only runs at the logging step is a check that can only ever report a breach that already occurred, never prevent one.

Two consequences, both real:

1. **The only place this can actually be preventive is earlier, during company research** — when a name from a cluster in §3 is approaching its own floor and gets discussed as a live candidate, that is the moment to say "this would be the Nth position in the Hayleys/rate-cycle/Hormuz cluster" — before Kaveen ever places the order, not after. This is now the primary trigger, replacing "before any new buy" as originally written.
2. **At the logging step, this file's job changes from gate to backstop.** If a fill is logged that turns out to breach the cluster cap, the response is not "undo the trade" — it's already done, and the position is kept as-is, full stop, never unwound over a cap breach alone. **The confirmed protocol (19-Sep-2026):** the breach gets stated plainly, the position stays, and the only consequence is that no further buys go into that same cluster until the cap is no longer breached — whether by the position being trimmed for an unrelated reason, or by a deliberate, explicit decision to widen the cap.

**Review cadence, revised:** (a) flagged proactively whenever a clustered name is discussed as nearing its floor, in whatever chat that discussion happens in; (b) checked against every logged fill, as a backstop that reports rather than blocks; (c) reviewed in full at any standalone portfolio review Kaveen asks for.

---

## 5. What this file deliberately does not do

- Does not touch any individual floor, ceiling, or verdict. A name can still be a legitimate buy on its own merits and still be capped by this file once it (alone or as part of a cluster) exceeds 50% of total invested capital.
- Does not add a sixth layer to the five-layer system — this sits alongside it as a portfolio-level gate, the same relationship Layer 4a (technical analysis) has to Layers 1/4/5.
- Does not unwind a breach. LIOC stays at its current size (§2a) — the cap only ever pauses *further* buys, never forces a sale.

---

*One-line version: one ticker or several dressed-up as different ones — either way, no single company gets more than half the portfolio, and this file is where that gets caught, before or after the money moves.*
