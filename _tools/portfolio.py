#!/usr/bin/env python3
"""
portfolio.py — portfolio analytics against vault floor/ceiling levels.

Usage:
    python3 portfolio.py [--holdings holdings.csv] [--prices prices.csv] [vault_root]

    vault_root defaults to the parent of the directory containing this script.

CSV formats:
    holdings.csv  — ticker,shares,avg_cost
    prices.csv    — ticker,price

Output:
    Prints a summary table to stdout.
    Writes PNGs to <vault_root>/_generated/:
        portfolio_allocation.png
        portfolio_vs_levels.png

Concentration rules (from system/Portfolio - Concentration and Correlation Tracker.md):
    - Single name cap:   50% of total invested capital
    - Cluster cap:       50% of total invested capital (same rule, per Tracker v1.2)
"""

import csv
import os
import re
import sys
import json
import yaml

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("WARNING: matplotlib not installed — charts will be skipped. Run: pip3 install matplotlib", file=sys.stderr)

VAULT_RESEARCH_DIR = "research"
GENERATED_DIR = "_generated"
CLUSTERS_FILE = "clusters.json"   # optional sidecar in _tools/

# Default cluster map — expandable via clusters.json sidecar
DEFAULT_CLUSTERS = {
    "tourism_hormuz": {
        "label": "Tourism/Hormuz (JKH+KHL)",
        "tickers": ["JKH.N0000", "KHL.N0000"],
    }
}

SINGLE_NAME_CAP = 0.50
CLUSTER_CAP = 0.50

COLORS = {
    "floor":    "#4a90d9",   # blue
    "tranche":  "#7fb3e0",   # light blue
    "ceiling":  "#e67e22",   # orange
    "price":    "#27ae60",   # green
    "below":    "#e74c3c",   # red (price below floor)
}


# ── helpers ────────────────────────────────────────────────────────────────

def parse_range_value(raw):
    """Same as validate_vault.py — parse float or range, return midpoint. Strips parentheticals."""
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


def load_csv(path, required_cols):
    """Load a CSV into a list of dicts; raise if required columns missing."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for col in required_cols:
            if col not in (reader.fieldnames or []):
                raise ValueError(f"{path}: missing column {col!r}. Found: {reader.fieldnames}")
        for row in reader:
            rows.append(row)
    return rows


def load_vault_levels(vault_root):
    """
    Read every .md file in research/ and extract YAML floor/second-tranche/ceiling.
    Returns dict: ticker -> {floor, tranche, ceiling, last_review, status, hurdle, ticker_short}
    """
    research_dir = os.path.join(vault_root, VAULT_RESEARCH_DIR)
    levels = {}
    if not os.path.isdir(research_dir):
        return levels
    for fname in os.listdir(research_dir):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(research_dir, fname)
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        try:
            fm = yaml.safe_load(text[3:end]) or {}
        except yaml.YAMLError:
            continue
        ticker = fm.get("ticker")
        if not ticker:
            continue
        levels[ticker] = {
            "floor":        parse_range_value(fm.get("floor")),
            "tranche":      parse_range_value(fm.get("second-tranche")),
            "ceiling":      parse_range_value(fm.get("ceiling")),
            "last_review":  fm.get("last-review", ""),
            "status":       str(fm.get("status", fm.get("verdict", ""))).split("—")[0].strip(),
            "hurdle":       fm.get("hurdle", ""),
            "ticker_short": (ticker.split(".")[0] if "." in ticker else ticker),
        }
    return levels


def load_clusters(tools_dir):
    clusters_path = os.path.join(tools_dir, CLUSTERS_FILE)
    if os.path.exists(clusters_path):
        with open(clusters_path, encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CLUSTERS


# ── charts ─────────────────────────────────────────────────────────────────

def chart_allocation(positions, out_path):
    """Pie chart of portfolio allocation by market value."""
    labels = [p["ticker_short"] for p in positions]
    sizes  = [p["market_value"] for p in positions]
    total  = sum(sizes)

    fig, ax = plt.subplots(figsize=(7, 5))
    wedge_colors = plt.cm.tab10.colors[:len(labels)]
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%",
        colors=wedge_colors, startangle=140,
        pctdistance=0.82, labeldistance=1.08,
    )
    for t in autotexts:
        t.set_fontsize(9)
    ax.set_title(f"Portfolio Allocation (Total MV: Rs {total:,.0f})", fontsize=12, pad=14)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Chart saved: {out_path}")


def chart_vs_levels(positions, out_path):
    """
    Horizontal bar chart: for each position, show a band from floor to ceiling
    with a marker for current price and a marker for avg cost.
    """
    tickers = [p["ticker_short"] for p in positions]
    n = len(tickers)
    fig, ax = plt.subplots(figsize=(10, max(3, n * 0.9 + 1.5)))

    y_pos = list(range(n))

    for i, p in enumerate(positions):
        floor   = p.get("floor")
        tranche = p.get("tranche")
        ceiling = p.get("ceiling")
        price   = p["price"]
        cost    = p["avg_cost"]

        if floor is not None and ceiling is not None:
            # Floor → ceiling band
            ax.barh(i, ceiling - floor, left=floor, height=0.45,
                    color=COLORS["floor"], alpha=0.25, label="_nolegend_")
            # Floor → tranche sub-band
            if tranche is not None:
                ax.barh(i, tranche - floor, left=floor, height=0.45,
                        color=COLORS["tranche"], alpha=0.35, label="_nolegend_")

        price_color = COLORS["below"] if (floor is not None and price < floor) else COLORS["price"]
        ax.plot(price, i, "D", color=price_color, markersize=9, zorder=5)
        ax.plot(cost,  i, "s", color="#8e44ad", markersize=7, zorder=4, alpha=0.8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(tickers, fontsize=10)
    ax.set_xlabel("Price (Rs)", fontsize=10)
    ax.set_title("Positions vs Vault Levels (Floor / Tranche / Ceiling)", fontsize=11, pad=10)

    # Legend
    legend_items = [
        mpatches.Patch(color=COLORS["floor"],   alpha=0.25, label="Floor–Ceiling band"),
        mpatches.Patch(color=COLORS["tranche"], alpha=0.55, label="Floor–2nd Tranche"),
        plt.Line2D([0], [0], marker="D", color="w", markerfacecolor=COLORS["price"],  markersize=9, label="Current price (above floor)"),
        plt.Line2D([0], [0], marker="D", color="w", markerfacecolor=COLORS["below"],  markersize=9, label="Current price (below floor)"),
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#8e44ad", markersize=7, label="Avg cost"),
    ]
    ax.legend(handles=legend_items, loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Chart saved: {out_path}")


# ── main ───────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Portfolio analytics vs vault floor/ceiling levels")
    parser.add_argument("vault_root", nargs="?",
                        default=os.path.join(os.path.dirname(__file__), ".."),
                        help="Path to vault root (default: parent of _tools/)")
    parser.add_argument("--holdings", default=None,
                        help="Path to holdings.csv (default: <vault_root>/holdings.csv)")
    parser.add_argument("--prices",   default=None,
                        help="Path to prices.csv (default: <vault_root>/prices.csv)")
    args = parser.parse_args()

    vault_root   = os.path.realpath(args.vault_root)
    holdings_csv = args.holdings or os.path.join(vault_root, "holdings.csv")
    prices_csv   = args.prices   or os.path.join(vault_root, "prices.csv")
    generated_dir = os.path.join(vault_root, GENERATED_DIR)
    tools_dir     = os.path.dirname(os.path.realpath(__file__))

    os.makedirs(generated_dir, exist_ok=True)

    # ── Load data ──────────────────────────────────────────────────────────
    if not os.path.exists(holdings_csv):
        print(f"ERROR: holdings.csv not found at {holdings_csv}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(prices_csv):
        print(f"ERROR: prices.csv not found at {prices_csv}", file=sys.stderr)
        sys.exit(1)

    holdings_rows = load_csv(holdings_csv, ["ticker", "shares", "avg_cost"])
    prices_rows   = load_csv(prices_csv,   ["ticker", "price"])

    prices_map = {r["ticker"]: float(r["price"]) for r in prices_rows}
    vault_levels = load_vault_levels(vault_root)
    clusters = load_clusters(tools_dir)

    # ── Build positions ────────────────────────────────────────────────────
    positions = []
    total_cost = 0.0
    total_mv   = 0.0

    for row in holdings_rows:
        ticker   = row["ticker"].strip()
        shares   = float(row["shares"])
        avg_cost = float(row["avg_cost"])
        price    = prices_map.get(ticker)
        if price is None:
            print(f"  WARNING: No price for {ticker} — skipping", file=sys.stderr)
            continue

        cost_basis   = shares * avg_cost
        market_value = shares * price
        total_cost  += cost_basis
        total_mv    += market_value

        lvl = vault_levels.get(ticker, {})
        pos = {
            "ticker":       ticker,
            "ticker_short": lvl.get("ticker_short", ticker.split(".")[0]),
            "shares":       shares,
            "avg_cost":     avg_cost,
            "price":        price,
            "cost_basis":   cost_basis,
            "market_value": market_value,
            "floor":        lvl.get("floor"),
            "tranche":      lvl.get("tranche"),
            "ceiling":      lvl.get("ceiling"),
            "last_review":  lvl.get("last_review", ""),
            "status":       lvl.get("status", ""),
            "hurdle":       lvl.get("hurdle", ""),
        }
        positions.append(pos)

    # Second pass — portfolio ratios and distance metrics
    for p in positions:
        p["pct_mv"]           = p["market_value"] / total_mv if total_mv else 0
        p["pct_cost"]         = p["cost_basis"]   / total_cost if total_cost else 0
        p["unrealised_pct"]   = (p["price"] - p["avg_cost"]) / p["avg_cost"]
        fl = p.get("floor")
        ce = p.get("ceiling")
        p["dist_floor"]   = (p["price"] - fl)  / fl  if fl else None
        p["dist_ceiling"] = (ce - p["price"])   / ce  if ce else None

    # ── Concentration checks ───────────────────────────────────────────────
    print(f"\n{'='*72}")
    print(f"  PORTFOLIO ANALYTICS  —  {len(positions)} positions")
    print(f"  Total invested: Rs {total_cost:,.2f}  |  Market value: Rs {total_mv:,.2f}")
    print(f"{'='*72}\n")

    # Print table
    header = f"{'Ticker':<10} {'Shares':>6} {'AvgCost':>8} {'Price':>8} {'Unreal%':>8} " \
             f"{'%MV':>6} {'Floor':>8} {'Ceiling':>8} {'ToFloor%':>9} {'ToCeil%':>9}  Status"
    print(header)
    print("-" * len(header))
    for p in positions:
        df = f"{p['dist_floor']*100:+.1f}%" if p["dist_floor"] is not None else "   n/a"
        dc = f"{p['dist_ceiling']*100:+.1f}%" if p["dist_ceiling"] is not None else "   n/a"
        fl_s = f"{p['floor']:.2f}" if p["floor"] is not None else "  n/a"
        ce_s = f"{p['ceiling']:.2f}" if p["ceiling"] is not None else "  n/a"
        flag = ""
        if p["floor"] is not None and p["price"] < p["floor"]:
            flag = " ◄ BELOW FLOOR"
        print(f"{p['ticker_short']:<10} {p['shares']:>6.0f} {p['avg_cost']:>8.2f} {p['price']:>8.2f} "
              f"{p['unrealised_pct']*100:>+7.1f}% {p['pct_mv']*100:>5.1f}% "
              f"{fl_s:>8} {ce_s:>8} {df:>9} {dc:>9}  {p['status'][:30]}{flag}")

    print(f"\n  Portfolio total  —  cost: Rs {total_cost:,.2f} | MV: Rs {total_mv:,.2f} | "
          f"total return: {(total_mv-total_cost)/total_cost*100:+.1f}%\n")

    # Single-name caps
    print("  CONCENTRATION CHECKS:")
    breaches = []
    for p in positions:
        pct = p["cost_basis"] / total_cost
        flag = " *** BREACH (>50%)" if pct > SINGLE_NAME_CAP else ""
        warn = " !   APPROACHING (>40%)" if (pct > 0.40 and not flag) else ""
        print(f"    {p['ticker_short']:<8}  {pct*100:.1f}% of invested capital{flag}{warn}")
        if flag:
            breaches.append(p["ticker_short"])

    # Cluster caps
    print()
    for cluster_id, cluster in clusters.items():
        cluster_tickers = cluster["tickers"]
        cluster_cost = sum(p["cost_basis"] for p in positions if p["ticker"] in cluster_tickers)
        pct = cluster_cost / total_cost if total_cost else 0
        flag = " *** BREACH (>50%)" if pct > CLUSTER_CAP else ""
        warn = " !   APPROACHING (>40%)" if (pct > 0.40 and not flag) else ""
        names = ", ".join(t.split(".")[0] for t in cluster_tickers)
        print(f"    Cluster [{cluster['label']}]:  {pct*100:.1f}%{flag}{warn}")

    if breaches:
        print(f"\n  *** {len(breaches)} BREACH(ES): {', '.join(breaches)}")

    # ── Charts ─────────────────────────────────────────────────────────────
    if HAS_MATPLOTLIB and positions:
        print(f"\n  Generating charts → {generated_dir}")
        chart_allocation(positions, os.path.join(generated_dir, "portfolio_allocation.png"))
        chart_vs_levels(positions,  os.path.join(generated_dir, "portfolio_vs_levels.png"))
    elif not HAS_MATPLOTLIB:
        print("\n  Charts skipped (matplotlib not available).")
    else:
        print("\n  No positions to chart.")

    print()
    return 1 if breaches else 0


if __name__ == "__main__":
    sys.exit(main())
