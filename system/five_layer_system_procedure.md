# The Five-Layer System — Operating Procedure
*Version 2.0 — procedure-specific. Supersedes the general version.*
*Principle: the company chooses itself when all five layers say yes at once. My only job is to refuse when any layer says no.*

---

## Layer 1 — Macro Reading
**Question answered:** What is the tide doing? What is my hurdle rate?

**Inputs:** CBSL releases (inflation, policy rates, external sector), weekly T-bill auction yields, LKR/USD, daily broker report (Senfin or equivalent).

**Procedure:**
1. Daily (10 min): scan the broker daily report. Record four numbers: turnover vs YTD average, RSI, breadth (positive vs negative contributors), foreign net flow — and decompose foreign flow (one block can distort the headline).
2. Weekly: update the macro sheet — 12-month T-bill yield, headline & non-food inflation, LKR YTD move, IMF/policy news.
3. Verify any single data table before building on it (broker reports contain spreadsheet errors).

**Output:** a hurdle rate (12M T-bill yield, currently ~10%) and a one-line tape verdict (e.g., "thin drawdown, RSI near oversold, foreign selling concentrated").

---

## Layer 2 — Sector Selection
**Question answered:** Where should I hunt?

**Procedure:**
1. For each macro force, write the **causal chain** to a sector: who mechanically receives money, who mechanically pays. A mechanism is required; a story is not enough. (Example: LKR −8% → exporter revenue in USD, costs in LKR → margin expansion. Arithmetic, not narrative.)
2. Produce a **shortlist** (1–2 sectors max) and an **anti-list** (sectors the macro actively punishes). The anti-list is as binding as the shortlist.
3. Pick ONE sector per research cycle. Two companies, not six.

**Frequency:** monthly, or when a macro variable breaks trend.

---

## Layer 3 — Company Research
**Question answered:** Is this a good business?

**Procedure:**
1. Annual report + latest interims from CSE site. Segment revenue breakdown first — know what the company actually is.
2. Earnings quality: is EPS rising or falling, cash-backed or accrual, payout sustainable?
3. Balance-sheet risk specific to the sector (e.g., banks: government securities exposure → rate-hike mark-to-market risk).
4. Write the markdown research file (SUN/JKH/JXG format).

**Output — the file is incomplete without:**
- Thesis in ONE sentence.
- Named **trigger events** that would confirm or break it (results dates, policy decisions, management actions). If I cannot name the triggers, I do not have a thesis.

---

## Layer 4 — Valuation
**Question answered:** Is it a good buy at this price?

**Procedure:**
1. Earnings yield vs hurdle rate. Market context check: if market E/Y < T-bill yield, the average stock is worse than a T-bill — floors stay strict.
2. Write three numbers **before** placing any order:
   - **Floor** — price at which the stock is demonstrably cheap vs earnings and assets. *The floor is a BUY level. It is never, under any framing, a sell level.*
   - **Second tranche level** — floor minus ~10%.
   - **Ceiling** — exit-into-strength level, derived from MY valuation, never from someone else's target.
3. Suspicion rule: any "floor" sitting within a few percent of today's close is not a valuation — it's an anchor to the current price. Recompute from the business.

---

## Layer 5 — Decision & Tracking
**Question answered:** What do I do today, and did I follow my own rules?

### Buy rules
- Buy ONLY at or below the written floor. Limit orders at my number; the market decides timing, I decide price.
- "Lower than yesterday" is never a buy signal. Path is not value.
- Sizing: max ½ of available cash into one name; max two tranches (floor, floor −10%); no third averaging-down.
- Cost awareness: at Rs. 5,000 order size the round-trip hurdle is ~3–4%. Acceptable as learning tuition; ruinous if churned.
- **Knife check:** price below floor → verify no adverse disclosure/announcement BEFORE buying. Verify thesis, then accumulate — never mechanically.

### Daily loop (30 seconds per holding)
```
Trigger event occurred?
├─ NO  → do nothing. (This fires ~85 of 90 days. That IS the answer.)
└─ YES → re-run thesis
         ├─ broken  → SELL
         └─ intact  → price ≤ floor & tranche budget left → BUY (limit)
                      price ≥ ceiling                     → SELL
                      otherwise                           → nothing
```
The check is daily; the decisions are event-driven. A daily ritual must never create pressure to act daily.

### Sell rules — exactly four legitimate reasons
1. Thesis broken by a named trigger event.
2. Ceiling reached.
3. Demonstrably better opportunity requiring the capital.
4. Life requires the money.

*Price falling, by itself, appears nowhere on this list.*

### Journal
Log every decision (including "did nothing") with the rule that produced it, and name the failure mode it guards against:
- **Narrative buying** (JKH) — bought a story, not a valuation.
- **Social abandonment** (JXG exit) — dropped the system under a friend's influence.
- **Delegation without thesis** (SUN) — owned a position I couldn't defend.

---

## Standing warnings
- Cash at a limit order is a position. "No trade" is a valid output of the system.
- One number cannot be both a buy signal and a sell signal. Valuation floor ≠ stop-loss; if I ever want a stop-loss, it goes BELOW the last tranche level as thesis-failure insurance, and is written in advance.
- Two-day horizons are noise plus transaction costs. My edge, if any, is price–value gaps closing over quarters.
- If red makes me want to exit while the thesis is intact, that is mood, not information. The discomfort must argue with this document, not with me.
