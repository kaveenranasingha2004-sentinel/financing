# _tools — CSE Vault Tooling

Three read-only Python scripts that audit the vault and build derived outputs.
All scripts read research files; none modify them. New files are written only to `_generated/`.

---

## Requirements

```bash
pip3 install pyyaml matplotlib
```

---

## Commands

### 1. `validate_vault.py` — vault health check

```bash
python3 _tools/validate_vault.py [vault_root]
# vault_root defaults to the parent of _tools/ (i.e. the vault root)
```

Runs six checks against every `.md` file in `research/` and prints a pass/fail report.

| Check | FAIL | WARN | NOTE |
|-------|------|------|------|
| YAML parse | exception from `yaml.safe_load` | – | – |
| Required YAML fields | – | ticker/floor/ceiling/last-review missing | – |
| Numeric coerce | – | unparseable floor or ceiling | quoted string (still parseable) |
| Second-tranche arithmetic | – | \|stated − floor×0.90\| > Rs 0.25 | \|Δ\| ≤ Rs 0.25 |
| Hurdle rate | – | not found; or stale vs 12.17% | rate found, source noted |
| Required sections | – | core section absent | optional section absent |

Exit code 0 = no FAILs; exit code 1 = at least one FAIL.

**Hurdle rate sources (priority order):**
1. `hurdle:` YAML field (only CTC has this)
2. Verified fallback map (hardcoded in the script from manual vault inspection — prevents false positives from historical rates embedded in file body text)
3. Body-text regex (only used for tickers not in the map)

To update the fallback map when a hurdle rate changes, edit `KNOWN_HURDLE_FALLBACK` near the top of `validate_vault.py` and update `CURRENT_HURDLE` / `CURRENT_HURDLE_LABEL`.

---

### 2. `portfolio.py` — position analytics

```bash
python3 _tools/portfolio.py [vault_root] [--holdings path] [--prices path]
# vault_root defaults to the parent of _tools/
# holdings defaults to <vault_root>/holdings.csv
# prices   defaults to <vault_root>/prices.csv
```

**Input CSV formats:**

`holdings.csv`:
```
ticker,shares,avg_cost
JXG.N0000,800,9.04
```

`prices.csv`:
```
ticker,price
JXG.N0000,12.10
```

**What it computes per position:**
- Cost basis, market value, unrealised P&L %
- % of portfolio by market value
- Distance to floor and ceiling (signed %)
- Flags positions trading below their written floor

**Concentration checks (from Tracker v1.2/v1.3):**
- Single-name cap: 50% of total invested capital → BREACH flagged
- Cluster cap: same 50% ceiling applied to correlated groups
  - Default cluster: JKH + KHL (Tourism/Hormuz)
  - Add custom clusters via `_tools/clusters.json`:
    ```json
    {
      "my_cluster": {
        "label": "My Cluster Label",
        "tickers": ["A.N0000", "B.N0000"]
      }
    }
    ```

**Outputs:**
- `_generated/portfolio_allocation.png` — pie chart of position sizes
- `_generated/portfolio_vs_levels.png` — horizontal bar chart showing floor/price/ceiling per ticker

Exit code 1 if any concentration breach detected; 0 otherwise.

---

### 3. `build_dashboard.py` — Obsidian dashboard

```bash
python3 _tools/build_dashboard.py [vault_root]
```

Reads all 16 research files and writes `_generated/Dashboard.md`.

**Dashboard sections:**
1. **Positions & Watchlist** — ticker, price (from `prices.csv` if present), floor, ceiling midpoint, % vs floor, hurdle rate used, last-review date, status
2. **Portfolio Charts** — embeds `![[portfolio_allocation.png]]` and `![[portfolio_vs_levels.png]]`
3. **Stale Hurdle Rates** — lists all tickers not yet re-derived to the current benchmark (12.17%)
4. **Open Homework** — aggregates all bullet-list items from every file's Homework/Open-items section, grouped by category (Interims, Hurdle/re-derivation, Insurance KPIs, Corporate events, Earnings quality)

Completed homework items (strikethrough `~~...~~`, checkmark `☑`, or `[x]`) are automatically excluded.

**Note:** `Dashboard.md` is a generated file. Do not edit it directly — re-run `build_dashboard.py`.

---

## Known Limitations

1. **Hurdle rate extraction** — body-text regex can pick up historical rates embedded in file narratives (files contain their full re-derivation history). The fallback map in both `validate_vault.py` and `build_dashboard.py` is the reliable source. When you re-derive a file to a new hurdle rate, update `KNOWN_HURDLE_FALLBACK` in both scripts.

2. **Sustainable EPS extraction** — only finds EPS when the phrase "Sustainable EPS:" or "Normalised EPS:" immediately precedes the number. Files that embed EPS in prose or tables without that exact label will show "EPS not found." Arithmetic notes are informational only; multipliers involve qualitative risk haircuts that cannot be reproduced automatically.

3. **UAL / JKH / KHL ceiling** — these files use quality-premium or NAV-anchored ceilings rather than pure `EPS ÷ hurdle`. The validator reports the implied multiple but cannot verify whether it's correct (it requires the judgment call in the file).

4. **CTC second-tranche** — the file states Rs. 860; floor × 0.90 = 864. The Rs. 4 gap is flagged as WARN by the validator. Per the hard rules, the file is not changed.

5. **AAIC second-tranche** — not in YAML (implied 63 = 70 × 0.90). Validator warns; field should be added to the YAML on next file touch.

6. **Section detection** — the validator looks for keywords in heading text. Files that use non-standard heading names (e.g. "Decision Journal" instead of "Thesis Log") will show false WARNs for missing sections.

7. **Homework categorisation** — keyword-based; imperfect. An item may land in the wrong category if it contains a matching word incidentally. The categorisation is for convenience only and does not affect data integrity.

8. **Prices column** — the dashboard and portfolio analytics show "–" for tickers not in `prices.csv`. Update `prices.csv` with current quotes before each run.

---

## Updating for a new hurdle rate

When the long-bond yield changes:
1. Open `_tools/validate_vault.py` and update `CURRENT_HURDLE`, `CURRENT_HURDLE_LABEL`, and the relevant ticker entry in `KNOWN_HURDLE_FALLBACK`.
2. Open `_tools/build_dashboard.py` and make the same changes to `CURRENT_HURDLE`, `CURRENT_HURDLE_LABEL`, and `KNOWN_HURDLE_FALLBACK`.
3. Re-run `validate_vault.py` to see which files are now stale.
4. Re-derive the affected research files (your job, per hard rules) and update `KNOWN_HURDLE_FALLBACK` when done.
