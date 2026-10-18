#!/usr/bin/env python3
"""
build_dashboard.py — generate _generated/Dashboard.md from vault research files.

Usage:
    python3 build_dashboard.py [vault_root]

    vault_root defaults to the parent of the directory containing this script.

Output:
    _generated/Dashboard.md — Obsidian-compatible markdown with:
        1. Positions table (ticker, price, floor, ceiling, premium/discount, hurdle, last-review, status)
        2. Embedded portfolio charts (allocation + vs-levels)
        3. Aggregated homework list grouped by category
        4. Stale-hurdle summary

Requires prices.csv in vault_root (optional; falls back to "–" if missing).
"""

import csv
import os
import re
import sys
import yaml
from datetime import date

VAULT_RESEARCH_DIR = "research"
GENERATED_DIR = "_generated"
CURRENT_HURDLE = 12.17
CURRENT_HURDLE_LABEL = "12.17%"

# Manually verified hurdle rates per ticker (same as validate_vault.py)
KNOWN_HURDLE_FALLBACK = {
    "AAIC.N0000": 12.6,
    "JKH.N0000":  12.6,
    "MGT.N0000":  12.6,
    "SERV.N0000": 12.6,
    "SINS.N0000": 12.6,
    "ALUM.N0000": 12.6,
    "SUN.N0000":  12.6,
    "HAYC.N0000": 11.96,
    "LIOC.N0000": 11.96,
    "CTC.N0000":  12.17,
    "DIPD.N0000": 12.17,
    "HAYL.N0000": 12.17,
    "JINS.N0000": 12.17,
    "UAL.N0000":  12.17,
    "KHL.N0000":  12.17,
    "JXG.N0000":  12.17,
}

# ── Homework extraction patterns ───────────────────────────────────────────
# Each tuple: (category_label, list_of_regex_patterns)
HOMEWORK_CATEGORIES = [
    ("Interims & results due", [
        re.compile(r"(Q[1-4]\s*(FY|interim|result|update|cash\s*flow))", re.IGNORECASE),
        re.compile(r"(interim|results?\s+due|quarterly\s+report)", re.IGNORECASE),
    ]),
    ("Hurdle rate / re-derivation", [
        re.compile(r"(hurdle|long.?bond|primary\s+auction|re.?deriv)", re.IGNORECASE),
    ]),
    ("Insurance KPIs (CAR / SLFRS 17)", [
        re.compile(r"(\bCAR\b|capital\s+adequacy|SLFRS\s*17|persistency|solvency)", re.IGNORECASE),
    ]),
    ("Corporate events & acquisitions", [
        re.compile(r"(acqui|merger|CEO|dividend|rights|capex|plant|expansion)", re.IGNORECASE),
    ]),
    ("Earnings quality & reconciliation", [
        re.compile(r"(NPL|reconcil|OCF|cash\s*flow\s*vs|finance\s*cost|funding\s*cost|EPS\s+series)", re.IGNORECASE),
    ]),
    ("Other", []),    # catch-all
]


def parse_range_value(raw):
    if raw is None:
        return None
    s = str(raw).strip().replace("–", "-").replace("—", "-").strip('"').strip("'")
    paren = s.find("(")
    if paren != -1:
        s = s[:paren].strip()
    if "-" in s:
        parts = s.split("-", 1)
        try:
            return (float(parts[0].strip()) + float(parts[1].strip())) / 2
        except ValueError:
            return None
    try:
        return float(s)
    except ValueError:
        return None


def extract_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end].strip(), text[end + 4:]
    return None, text


def extract_hurdle_from_yaml_or_body(fm, body):
    """
    Return hurdle as float%.
    Priority: YAML field > verified fallback map > body regex.
    Fallback map wins over body regex to avoid picking up historical rates.
    """
    ticker = fm.get("ticker", "")
    h = fm.get("hurdle")
    if h:
        m = re.search(r"([\d\.]+)", str(h))
        if m:
            return float(m.group(1))
    if ticker in KNOWN_HURDLE_FALLBACK:
        return KNOWN_HURDLE_FALLBACK[ticker]
    # Body regex as last resort
    patterns = [
        r"hurdle\s+rate[^0-9]{0,20}(\d{1,2}\.\d+)\s*%",
        r"hurdle[:\s=]+(\d{1,2}\.\d+)\s*%",
        r"(\d{1,2}\.\d+)\s*%.*?long.?bond",
        r"long.?bond.*?(\d{1,2}\.\d+)\s*%",
    ]
    for pat in patterns:
        m = re.search(pat, body, re.IGNORECASE)
        if m:
            v = float(m.group(1))
            if 8.0 < v < 18.0:
                return v
    return None


def extract_homework_items(body):
    """
    Find lines inside homework/open-items sections.
    Returns list of item text strings.
    """
    # Match any markdown heading (## 10. Homework, ## Open homework, etc.)
    hw_section_re = re.compile(
        r"^#{1,4}[^#\n]*(homework|open\s+item|on\s+the\s+horizon|to\s+investigate|pending|action\s+item)",
        re.IGNORECASE
    )
    items = []
    in_hw = False
    for line in body.splitlines():
        if hw_section_re.search(line):
            in_hw = True
            continue
        if in_hw:
            # Stop at next heading
            if re.match(r"^#{1,4}\s", line) and not hw_section_re.search(line):
                in_hw = False
                continue
            # Collect bullet/numbered lines
            stripped = line.strip()
            if stripped.startswith(("-", "*", "•")) or re.match(r"^\d+\.", stripped):
                text = re.sub(r"^[-*•\d\.]+\s*", "", stripped).strip()
                # Skip completed items: strikethrough (~~), checkmark (☑), or [x]
                if text and not text.startswith(("~~", "☑", "[x]", "[X]")):
                    items.append(text)
    return items


def categorise_item(item_text):
    for label, patterns in HOMEWORK_CATEGORIES[:-1]:
        for pat in patterns:
            if pat.search(item_text):
                return label
    return "Other"


def load_prices(vault_root):
    path = os.path.join(vault_root, "prices.csv")
    if not os.path.exists(path):
        return {}
    prices = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker = row.get("ticker", "").strip()
            price_str = row.get("price", "").strip()
            try:
                prices[ticker] = float(price_str)
            except ValueError:
                pass
    return prices


# ── main ───────────────────────────────────────────────────────────────────

def main():
    vault_root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
    vault_root = os.path.realpath(vault_root)
    research_dir = os.path.join(vault_root, VAULT_RESEARCH_DIR)
    generated_dir = os.path.join(vault_root, GENERATED_DIR)
    os.makedirs(generated_dir, exist_ok=True)

    prices_map = load_prices(vault_root)

    if not os.path.isdir(research_dir):
        print(f"ERROR: research directory not found: {research_dir}", file=sys.stderr)
        sys.exit(1)

    md_files = sorted(f for f in os.listdir(research_dir) if f.endswith(".md"))

    rows = []
    stale_hurdle = []
    all_homework = {}   # ticker_short -> [(category, item_text)]

    for fname in md_files:
        path = os.path.join(research_dir, fname)
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue

        raw_yaml, body = extract_frontmatter(text)
        if raw_yaml is None:
            continue
        try:
            fm = yaml.safe_load(raw_yaml) or {}
        except yaml.YAMLError:
            continue

        ticker = fm.get("ticker", "")
        ticker_short = ticker.split(".")[0] if "." in ticker else ticker
        status_raw = str(fm.get("status", fm.get("verdict", ""))).strip()
        status = status_raw.split("—")[0].strip()
        last_review = str(fm.get("last-review", "–"))

        floor_val   = parse_range_value(fm.get("floor"))
        ceiling_val = parse_range_value(fm.get("ceiling"))
        hurdle_val  = extract_hurdle_from_yaml_or_body(fm, body)
        hurdle_label = f"{hurdle_val}%" if hurdle_val else "–"

        price = prices_map.get(ticker)
        price_str = f"{price:.2f}" if price is not None else "–"

        # Premium/discount to floor
        if price is not None and floor_val is not None:
            pct = (price - floor_val) / floor_val * 100
            if pct >= 0:
                vs_floor = f"+{pct:.0f}% above"
            else:
                vs_floor = f"{pct:.0f}% BELOW"
        else:
            vs_floor = "–"

        # Stale hurdle
        if hurdle_val is not None and abs(hurdle_val - CURRENT_HURDLE) > 0.02:
            stale_hurdle.append((ticker_short, hurdle_val, CURRENT_HURDLE - hurdle_val))

        floor_str   = f"{floor_val:.2f}"   if floor_val   is not None else "–"
        ceiling_str = f"{ceiling_val:.2f}" if ceiling_val is not None else "–"

        rows.append({
            "ticker_short": ticker_short,
            "price":        price_str,
            "floor":        floor_str,
            "ceiling":      ceiling_str,
            "vs_floor":     vs_floor,
            "hurdle":       hurdle_label,
            "last_review":  last_review,
            "status":       status[:40],
        })

        # Homework
        hw_items = extract_homework_items(body)
        if hw_items:
            all_homework[ticker_short] = [
                (categorise_item(item), item) for item in hw_items
            ]

    # ── Build markdown ─────────────────────────────────────────────────────
    today = date.today().isoformat()
    lines = [
        f"# Vault Dashboard",
        f"",
        f"*Generated {today} · hurdle benchmark: {CURRENT_HURDLE_LABEL} · {len(rows)} files*",
        f"",
        f"---",
        f"",
        f"## Positions & Watchlist",
        f"",
        f"| Ticker | Price | Floor | Ceiling | vs Floor | Hurdle | Last Review | Status |",
        f"|--------|------:|------:|--------:|----------|--------|-------------|--------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['ticker_short']} | {r['price']} | {r['floor']} | {r['ceiling']} "
            f"| {r['vs_floor']} | {r['hurdle']} | {r['last_review']} | {r['status']} |"
        )

    lines += [
        f"",
        f"---",
        f"",
        f"## Portfolio Charts",
        f"",
        f"![[portfolio_allocation.png]]",
        f"",
        f"![[portfolio_vs_levels.png]]",
        f"",
        f"*(Run `portfolio.py` to regenerate charts from holdings.csv and prices.csv)*",
        f"",
        f"---",
        f"",
        f"## Stale Hurdle Rates",
        f"",
    ]

    if stale_hurdle:
        lines.append(f"Files not yet re-derived to current {CURRENT_HURDLE_LABEL}:\n")
        lines.append(f"| Ticker | Current Rate | Gap (pp) |")
        lines.append(f"|--------|-------------|---------|")
        for ts, rate, gap in sorted(stale_hurdle, key=lambda x: -abs(x[2])):
            lines.append(f"| {ts} | {rate}% | {gap:+.2f}pp |")
    else:
        lines.append(f"*All files are up to date with {CURRENT_HURDLE_LABEL}.*")

    lines += [
        f"",
        f"---",
        f"",
        f"## Open Homework",
        f"",
    ]

    # Group homework by category across all tickers
    from collections import defaultdict
    by_category = defaultdict(list)
    for ticker_short, items in sorted(all_homework.items()):
        for cat, item_text in items:
            by_category[cat].append((ticker_short, item_text))

    # Preserve defined category order
    cat_order = [label for label, _ in HOMEWORK_CATEGORIES]
    for cat in cat_order:
        items_in_cat = by_category.get(cat, [])
        if not items_in_cat:
            continue
        lines.append(f"### {cat}")
        lines.append(f"")
        for ticker_short, item_text in items_in_cat:
            lines.append(f"- **{ticker_short}** — {item_text}")
        lines.append(f"")

    lines += [
        f"---",
        f"",
        f"*Dashboard built by `_tools/build_dashboard.py`. Do not edit this file directly — re-run the script.*",
    ]

    output_path = os.path.join(generated_dir, "Dashboard.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Dashboard written to: {output_path}")
    print(f"  {len(rows)} tickers | {len(stale_hurdle)} stale hurdle | "
          f"{sum(len(v) for v in all_homework.values())} homework items")


if __name__ == "__main__":
    main()
