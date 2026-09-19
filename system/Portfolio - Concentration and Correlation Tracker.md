---
type: system-doc
supersedes: none — new file, sits alongside the five-layer system as a portfolio-level (not per-stock) check
version: 1.0
created: 2026-09-19
last-review: 2026-09-19
tags:
  - investing
  - cse
  - system
  - portfolio-risk
  - concentration
---

# Portfolio — Concentration & Correlation Tracker
*Version 1.0 — 2026-09-19. Every existing layer of the system operates per-stock. This file is the one place that looks across the whole book at once: how much of the actual capital is riding on the same underlying macro driver, dressed up as different tickers.*

---

## 0. Why this exists

Layer 4/5 discipline (floor, second tranche, max ½ cash per name) already caps how much goes into any *one* ticker. Nothing in the system caps how much goes into one **driver** wearing several tickers. The vault's own queue makes this concrete: seven of the fifteen tracked names (HAYL, DIPD, HAYC, ALUM, SINS, SERV, MGT) are Hayleys-linked and have, so far, moved together as a group-wide valuation premium — buying two of them isn't diversification, it's one bet twice. The only existing rule of this kind in the vault is narrow and single-purpose: JXG's file caps future JINS orders against a shared Janashakthi-group exposure. This file generalizes that instinct into a standing check.

**This file does not replace anything.** It runs *after* Layer 4/5 clears a name for purchase, as the last check before capital actually moves, and again at any standalone portfolio review.

---

## 1. Live position table

*(Update this table at every portfolio review — it is the one place actual position sizes live outside the individual research files' own thesis logs.)*

| Ticker | Shares | Avg cost | Primary driver | Secondary driver |
|---|---|---|---|---|
| JXG | 800 | ~9.04 effective | Rate-cycle via First Capital Holdings (bond trading gains/losses) | JINS embedded-value/equity-book mark |
| JKH | 100 | 20.53 | Retail/EV mean-reversion + Leisure financing-phase drag | Tourism/oil-Hormuz war-windfall (Transportation), LKR/CODSL loan |
| SUN | 0 (closed) | — | — | closed 13-Aug-2026, realized −10.37% |

**Cash / uncommitted:** not tracked in this file — pull from the trade-logging chat before relying on this table for a sizing decision.

---

## 2. Driver-overlap read on the current book

**JXG vs. JKH — soft overlap, not a hard one.** Both carry *some* interest-rate sensitivity (JXG directly via FCH's bond-trading book; JKH indirectly via Financial Services' Union Assurance stake and its own thin interest cover, 2.5×) — but it is a secondary factor for JKH, not the primary one, and their dominant drivers (JXG: rate-cycle; JKH: Retail/EV + tourism/war-windfall + Leisure recovery) are genuinely different. **Read: acceptable overlap, not a cluster.** Worth re-checking if either file's dominant-driver framing changes.

**Verdict on the current 2-position book: no correlated-cluster breach.** This section exists mainly for what it will need to catch next, not because the current book has a problem.

---

## 3. The rule — correlated-cluster cap

**Any two or more open positions sharing a named primary macro driver count against one shared cap, not two separate ones.**

Named driver-clusters already visible in the vault, to check against before any new buy:
- **Hayleys-group ownership premium** — HAYL, DIPD, HAYC, ALUM, SINS, SERV, MGT. Confirmed in every one of these files' own verdicts: each trades at a large, independent premium to its own hurdle-rate ceiling, and the premium's persistence *across* the group (not just within one name) is the standing hypothesis LIOC was built specifically to test. Buying a second name from this list is not diversification within the book.
- **Rate-cycle / bond-yield sensitivity** — JXG (via FCH), AAIC, UAL, JINS (insurers, duration/reinvestment plays). All four are explicitly the same Layer 2 sector thesis in this vault, just expressed with different torque.
- **Tourism/Hormuz-Middle-East war-windfall** — JKH (Transportation tailwind + Leisure/tourism drag, opposite signs, same regime), KHL (same regime, hospitality side only).

**Cap:** a correlated cluster, in aggregate, is sized like a single name under Layer 5's existing rule — max ½ of available cash across the *whole cluster*, not per ticker inside it. Two tranches maximum across the cluster, not two tranches per name in it.

**This is a generalization of an existing rule, not a new one.** JXG's file already states the JINS-specific version of this; this section is that same logic written once, for every cluster, instead of re-derived per file.

---

## 4. When this file actually bites — and the real timing constraint

**Dormant at 3 positions (JXG, JKH, LIOC).** None of the three share a primary driver, so no cap is currently active.

**Honest limitation, named rather than glossed over:** orders are placed as limit orders at the broker, independent of this chat — Kaveen executes, then logs the fill here afterward. There is no point at which this file can sit between a decision and an order the way §4's original framing implied ("checked before any new buy") — by the time a fill is logged, the trade has already happened. A cap check that only runs at the logging step is a check that can only ever report a breach that already occurred, never prevent one.

Two consequences, both real:

1. **The only place this can actually be preventive is earlier, during company research** — when a name from a cluster in §3 is approaching its own floor and gets discussed as a live candidate, that is the moment to say "this would be the Nth position in the Hayleys/rate-cycle/Hormuz cluster" — before Kaveen ever places the order, not after. This is now the primary trigger, replacing "before any new buy" as originally written.
2. **At the logging step, this file's job changes from gate to backstop.** If a fill is logged that turns out to breach the cluster cap, the response is not "undo the trade" — it's already done, and the position is kept as-is, full stop, never unwound over a cap breach alone. **The confirmed protocol (19-Sep-2026):** the breach gets stated plainly, the position stays, and the only consequence is that no further buys go into that same cluster until the cap is no longer breached — whether by the position being trimmed for an unrelated reason, or by a deliberate, explicit decision to widen the cap.

**Review cadence, revised:** (a) flagged proactively whenever a clustered name is discussed as nearing its floor, in whatever chat that discussion happens in; (b) checked against every logged fill, as a backstop that reports rather than blocks; (c) reviewed in full at any standalone portfolio review Kaveen asks for.

---

## 5. What this file deliberately does not do

- Does not touch any individual floor, ceiling, or verdict. A name can still be a legitimate buy on its own merits and still be capped by this file once a second correlated position exists.
- Does not add a sixth layer to the five-layer system — this sits alongside it as a portfolio-level gate, the same relationship Layer 4a (technical analysis) has to Layers 1/4/5.
- Does not require action today. The current 2-position book clears with no changes.

---

*One-line version: two tickers can be one bet — this file is where that gets caught before the money moves, not after.*
