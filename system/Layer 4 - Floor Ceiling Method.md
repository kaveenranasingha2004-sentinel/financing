# Layer 4 — The Floor/Ceiling Method
*Version 1.0 — 2026-07-15. The exact derivation behind every floor and ceiling in the research files. Written so any number can be recomputed from the primary reports.*

---

## 0. The primitive (why this works at all)

A share is a claim on a stream of future cash. Its value is what that stream is worth *to me*, given what I could earn risklessly instead. Everything below is machinery for answering one question:

> **At what price does this company's earning power pay me enough more than a government bond to compensate for every risk I can name?**

The floor is the price where the answer becomes "clearly yes." The ceiling is the price where the answer becomes "no longer."

## 1. Step one — the hurdle rate

**Hurdle = current long-dated T-bond yield.** (Now: ~12.6%, from the 13-Jul auction.)

Why the long bond, not the T-bill: equity is a long-duration claim; compare like with like. Why risk-free at all: it's the alternative that requires no analysis, no thesis, no monitoring. Any stock must beat it *after* risk, or the stock is charity.

Convert to a multiple: **max fair P/E for a zero-growth business = 1 ÷ hurdle** = 1/0.126 ≈ **8×**. A company earning flat forever at 8× merely ties the bond. This is the ceiling's outer wall before any adjustment.

## 2. Step two — sustainable EPS (the hard part; 80% of the work)

Reported EPS is a starting claim, not a fact. Rebuild it:

1. **Decompose the income statement.** Separate: core operating profit / market-linked items (fair-value gains, realised gains) / one-offs (asset sales, associate swings) / timing artifacts (actuarial transfer conventions).
2. **Keep what recurs, haircut what's weather.** Test for each line: *would this appear in an average year of the next five?*
3. **Check the accounting standard's lifespan.** An EPS measured under a dying standard (SLFRS 4 → 17) carries an asterisk that widens every margin below.
4. **Divide by the CURRENT share count** — verified against the latest filing, never an aggregator (the JINS 1:3 split lesson).

Worked examples:
- **UAL:** FY25 PAT 3,370 Mn ÷ 589.3 Mn shares = **5.72**. Smooth annual surplus transfers, little market-linked noise → used as-is.
- **JINS:** FY25 PAT 3,466 Mn (EPS 5.10 post-split) — but ~half is FV gains + FCH associate. Sustainable PAT ≈ 2.0–2.5 Bn → **EPS ≈ 3.0**.
- **AAIC:** FY25 group EPS **14.8** — real insurance earnings, but Q4-loaded via actuarial transfers and measured under the expiring standard → kept, with the risk pushed into step three's margin instead.

## 3. Step three — the floor

**Floor = sustainable EPS × floor multiple**, where the floor multiple starts at the neutral 8× and is *cut* for every named risk. This is the crucial discipline: **each risk in the red-flags register must be paid for in the multiple.** Risks are not adjectives; they are subtractions.

**Floor P/E ≈ (1 ÷ hurdle) × (1 − Σ risk haircuts)** — the haircuts are judgment, but they must be *listed*, so the judgment is auditable.

Worked examples:
- **AAIC: floor 70** = 14.8 × ~4.7×. Haircuts from 8×: SLFRS 17 restatement opacity (large), ≥4 Bn tax contingency vs 14 Bn equity, 87.8% concentrated ownership with a live related-party channel, 12% float. At 70 the earnings yield is 21% — even a one-third downward earnings restatement still clears the hurdle. *That's the test a floor must pass: wrong-but-still-fine.*
- **JINS: floor 18** = 3.0 × 6×. Haircuts: undisclosed persistency on a 70% first-year book, filing-error pattern, Diri Savi liquidity, equity book = 35% of shareholders' equity. E/y ~17%.
- **UAL: floor 55** = 5.72 × ~9.6× — *above* the neutral 8×, the one deliberate exception: earnings are understated by conservatism (the fund grew 20% while reported profit fell), the dividend is real (9.1% yield at 55), governance is clean. Quality can justify a modest premium to neutral — but only when named and argued, never assumed.

**Cross-check with a second anchor before accepting any floor:** dividend yield at the floor (is the cash return alone respectable vs the bond?); asset backing as sanity only (P/B means nothing without ROE context — a 39% ROE business at 1.8× book can be cheaper than a 5% ROE business at 0.5×).

## 4. Step four — the ceiling

**Ceiling = the price where sustainable earnings yield falls to ≈ the hurdle** — where the margin of safety is fully spent and holding the stock pays no better than the bond while carrying all the risk.

**Ceiling ≈ sustainable EPS ÷ hurdle**, stretched modestly (10–20%) only where growth is *mechanical* (contracted, arithmetic — an FX margin, a reinvestment gap), never where growth is narrative.

- JINS: 3.0 ÷ 0.126 ≈ 24, stretched to 24–27 for the (real) 42% GWP growth.
- AAIC: 100–105 ≈ 7× on 14.8 — e/y ~14%, margin thinned to noise given restatement risk.
- UAL: 78–80 — e/y toward 7%, indefensible against 12.6%; also respects observed distribution zone (Q1 high 83.20). Market structure may inform a ceiling; it may never create a floor.

## 5. Step five — mechanics
- **Second tranche = floor × 0.90.** One level, pre-written; prevents improvised averaging.
- **Round conservatively** (floors down, ceilings down).
- **Write the falsifiers** next to the numbers: the named events that would move them (e.g., JINS ceiling rises if the SLFRS 17 CSM is large or a persistency ladder appears). Numbers without falsifiers become dogma.
- Numbers change only when a **trigger event** fires — never because the price moved.

## 6. Method selection — the multiple follows the business
Earnings-yield is the default because it makes the fewest assumptions. But:
- **Depressed/recovery earnings** (JKH): earnings meaningless at the trough → asset anchor (P/B 0.85 vs recovery ROE) does the work.
- **Holdcos** (JXG): SOTP — value the parts, apply the double-count check and a holdco discount.
- **Insurers, properly:** the actuarially honest tool is embedded value / CSM — which is why the SLFRS 17 restatement is the standing trigger on all three insurance files. My earnings-yield floors are the conservative proxy until that disclosure exists.
- Commodity/cyclicals (upcoming: HAYL, DIPD): use *mid-cycle* earnings, never peak — same decomposition discipline, applied to the cycle instead of the accounting.

## 7. What these numbers are NOT
Not price predictions. The market may never visit the floor (fine — no trade) and may live above the ceiling for years (fine — not my money). Floor and ceiling are statements about **my required compensation**, derived from the bond market and the company's own filings. They move when facts move. The market's only role is to occasionally agree with me at a moment I've prepared for in advance.

---

*One-line version: strip the earnings to what recurs, demand the bond yield plus payment for every named risk at the floor, surrender the position when the margin is spent at the ceiling, and let the written falsifiers — not the price — reopen the question.*
