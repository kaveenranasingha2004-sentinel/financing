#!/usr/bin/env python3
"""
validate_vault.py — read-only audit of the CSE equity research vault.

Usage:
    python3 validate_vault.py [vault_root]

    vault_root defaults to the parent of the directory containing this script.

Exit codes:
    0 — no FAILs (WARNs and NOTEs are acceptable)
    1 — at least one FAIL

Severity levels:
    FAIL — YAML parse error or required field entirely absent
    WARN — arithmetic deviation > Rs 0.25, missing core section, stale hurdle
    NOTE — rounding deviation ≤ Rs 0.25, optional section absent, informational
"""

import os
import re
import sys
import yaml

VAULT_RESEARCH_DIR = "research"
CURRENT_HURDLE = 12.17          # % — latest provisional rate (25-Sep-2026)
CURRENT_HURDLE_LABEL = "12.17%"
SECOND_TRANCHE_FACTOR = 0.90
SECOND_TRANCHE_WARN_DELTA = 0.25   # Rs — threshold for WARN vs NOTE
SECOND_TRANCHE_NOTE_DELTA = 0.05   # Rs — threshold for NOTE vs silent pass

REQUIRED_YAML_FIELDS = ["ticker", "floor", "ceiling", "last-review"]

# Core sections every file should have (regex patterns against heading lines)
CORE_SECTIONS = {
    "Thesis Log": re.compile(r"thesis", re.IGNORECASE),
    "Valuation/Layer 4": re.compile(r"(valuation|layer\s*4)", re.IGNORECASE),
}
RECOMMENDED_SECTIONS = {
    "Risks": re.compile(r"\brisks?\b", re.IGNORECASE),
    "Triggers/Catalysts": re.compile(r"(trigger|catalyst)", re.IGNORECASE),
}
OPTIONAL_SECTIONS = {
    "Layer 3a (OCF/Moat)": re.compile(r"(layer\s*3a|ocf|moat|competitive)", re.IGNORECASE),
    "Layer 6 (Forward Dev)": re.compile(r"(layer\s*6|forward\s+dev)", re.IGNORECASE),
}

# NAV-anchored files — skip EPS arithmetic for these
NAV_ANCHORED = {"JKH.N0000", "KHL.N0000", "JXG.N0000"}

# Files without second-tranche expected (structural anchors)
NO_SECOND_TRANCHE_EXPECTED = {"JXG.N0000"}

# Known hurdle rates by ticker (from body-text extraction context)
# Used only when body regex finds nothing
KNOWN_HURDLE_FALLBACK = {
    "AAIC.N0000": 12.6,
    "JKH.N0000": 12.6,
    "MGT.N0000": 12.6,
    "SERV.N0000": 12.6,
    "SINS.N0000": 12.6,
    "HAYC.N0000": 11.96,
    "LIOC.N0000": 11.96,
    "CTC.N0000": 12.17,
    "DIPD.N0000": 12.17,
    "HAYL.N0000": 12.17,
    "JINS.N0000": 12.17,
    "UAL.N0000": 12.17,
    "ALUM.N0000": 12.6,
    "KHL.N0000": 12.17,
    "JXG.N0000": 12.17,
    "SUN.N0000": 12.6,
}


# ── helpers ────────────────────────────────────────────────────────────────

def parse_range_value(raw):
    """
    Parse a YAML value that may be a float, int, or range string.
    Handles both ASCII hyphen (47.50-47.75) and en-dash (47.50–47.75).
    Strips parenthetical annotations like '70.00 (DRAFT — ...)'.
    Returns (low, high, midpoint) for ranges; (val, val, val) for scalars.
    Returns None on failure.
    """
    if raw is None:
        return None
    s = str(raw).strip().replace("–", "-").replace("—", "-")
    # Remove any enclosing quotes
    s = s.strip('"').strip("'")
    # Strip parenthetical annotations: everything from '(' onward
    paren = s.find("(")
    if paren != -1:
        s = s[:paren].strip()
    if "-" in s:
        parts = s.split("-", 1)
        try:
            lo = float(parts[0].strip())
            hi = float(parts[1].strip())
            return (lo, hi, (lo + hi) / 2)
        except ValueError:
            return None
    else:
        try:
            v = float(s)
            return (v, v, v)
        except ValueError:
            return None


def extract_frontmatter(text):
    """Return (raw_yaml_string, body_text) or (None, full_text)."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end].strip(), text[end + 4:]
    return None, text


def extract_hurdle_from_body(body):
    """
    Scan body text for a hurdle rate percentage in a clearly labelled context.
    Requires the rate to appear near 'hurdle', 'long bond', 'T-bond', or 'CBSL'.
    Returns float (e.g. 12.17) or None.
    """
    # Require explicit label context to avoid picking up earnings yields, ROE %, etc.
    patterns = [
        r"hurdle\s+rate[^0-9]{0,20}(\d{1,2}\.\d+)\s*%",
        r"hurdle[:\s=]+(\d{1,2}\.\d+)\s*%",
        r"(\d{1,2}\.\d+)\s*%\s+\(?hurdle",
        r"(\d{1,2}\.\d+)\s*%.*?long.?bond",
        r"long.?bond.*?(\d{1,2}\.\d+)\s*%",
        r"(\d{1,2}\.\d+)\s*%.*?CBSL",
        r"CBSL.*?(\d{1,2}\.\d+)\s*%",
        r"(\d{1,2}\.\d+)\s*%.*?T.?bond",
    ]
    found = []
    for pat in patterns:
        for m in re.finditer(pat, body, re.IGNORECASE):
            try:
                # group(1) is the number in all patterns
                v = float(m.group(1))
                if 8.0 < v < 18.0:   # sane hurdle rate range
                    found.append(v)
            except (ValueError, IndexError):
                pass
    if not found:
        return None
    from collections import Counter
    c = Counter(found)
    return c.most_common(1)[0][0]


def extract_eps_from_body(body):
    """
    Extract the sustainable/normalised EPS from body text.
    Only matches when a clear 'Sustainable EPS' or 'Normalised EPS' label is present.
    Returns float or None.
    """
    # Require explicit label; avoid loose "EPS:" which catches random per-share data
    patterns = [
        r"[Ss]ustainable\s+EPS[:\s=]+Rs\.?\s*([\d]+\.[\d]+)",
        r"[Ss]ustainable\s+EPS[:\s=]+Rs\.?\s*(\d+)",
        r"[Nn]ormali[sz]ed?\s+EPS[:\s=]+Rs\.?\s*([\d]+\.[\d]+)",
        r"[Nn]ormali[sz]ed?\s+EPS[:\s=]+Rs\.?\s*(\d+)",
        # Pattern for "EPS: Rs 5.43" or "EPS = Rs 5.43" at start of key-value line
        r"^\s*[-*]?\s*Sustainable\s+EPS[^\n]*?Rs\.?\s*([\d]+\.[\d]+)",
        r"^\s*[-*]?\s*Sustainable\s+EPS[^\n]*?=\s*([\d]+\.[\d]+)",
    ]
    for pat in patterns:
        m = re.search(pat, body, re.MULTILINE)
        if m:
            try:
                v = float(m.group(1))
                # Sanity: EPS should be plausible for CSE (< 1000, > 0.01)
                if 0.01 < v < 1000:
                    return v
            except ValueError:
                pass
    return None


def check_sections(body):
    """
    Returns dict: section_name -> bool (found or not).
    Checks headings (## lines) for each category.
    """
    headings = re.findall(r"^#{1,4}\s+(.+)$", body, re.MULTILINE)
    heading_blob = "\n".join(headings)

    results = {}
    for name, pat in {**CORE_SECTIONS, **RECOMMENDED_SECTIONS, **OPTIONAL_SECTIONS}.items():
        results[name] = bool(pat.search(heading_blob))
    return results


# ── per-file audit ─────────────────────────────────────────────────────────

def audit_file(path):
    """
    Run all checks on one file.
    Returns list of (severity, check_name, message) tuples.
    """
    issues = []

    def add(severity, check, msg):
        issues.append((severity, check, msg))

    filename = os.path.basename(path)

    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        add("FAIL", "file-read", str(e))
        return issues

    # ── 1. YAML parse ──────────────────────────────────────────────────────
    raw_yaml, body = extract_frontmatter(text)
    if raw_yaml is None:
        add("FAIL", "yaml-missing", "No YAML frontmatter block found")
        return issues

    try:
        fm = yaml.safe_load(raw_yaml) or {}
    except yaml.YAMLError as e:
        add("FAIL", "yaml-parse", f"yaml.safe_load error: {e}")
        return issues

    # ── 2. Required YAML fields ────────────────────────────────────────────
    ticker = fm.get("ticker", "UNKNOWN")
    for field in REQUIRED_YAML_FIELDS:
        if field not in fm:
            add("WARN", "yaml-fields", f"Missing required field: {field!r}")

    # ── 3. Numeric coercion ────────────────────────────────────────────────
    floor_raw = fm.get("floor")
    ceiling_raw = fm.get("ceiling")
    tranche_raw = fm.get("second-tranche")

    floor_parsed = parse_range_value(floor_raw)
    ceiling_parsed = parse_range_value(ceiling_raw)
    tranche_parsed = parse_range_value(tranche_raw) if tranche_raw is not None else None

    if floor_raw is not None and floor_parsed is None:
        add("WARN", "numeric-coerce", f"Cannot parse floor value: {floor_raw!r}")
    if ceiling_raw is not None and ceiling_parsed is None:
        add("WARN", "numeric-coerce", f"Cannot parse ceiling value: {ceiling_raw!r}")

    # Flag string floor (e.g. ALUM "3.8")
    if isinstance(floor_raw, str) and floor_parsed is not None:
        add("NOTE", "yaml-type", f"floor is a quoted string {floor_raw!r}; will be treated as {floor_parsed[2]}")

    # ── 4. Second-tranche arithmetic ───────────────────────────────────────
    if ticker in NO_SECOND_TRANCHE_EXPECTED:
        if tranche_raw is None:
            add("NOTE", "second-tranche", "No second-tranche in YAML (expected for this anchor type)")
    elif tranche_raw is None:
        add("WARN", "second-tranche", "second-tranche field missing from YAML (implied = floor × 0.90)")
    elif floor_parsed is not None and tranche_parsed is not None:
        floor_val = floor_parsed[2]
        tranche_val = tranche_parsed[2]
        expected = round(floor_val * SECOND_TRANCHE_FACTOR, 2)
        delta = abs(tranche_val - expected)
        if delta > SECOND_TRANCHE_WARN_DELTA:
            add("WARN", "second-tranche-arithmetic",
                f"second-tranche {tranche_val} ≠ floor×0.90 = {expected:.2f} (Δ = {delta:.2f})")
        elif delta > SECOND_TRANCHE_NOTE_DELTA:
            add("NOTE", "second-tranche-arithmetic",
                f"second-tranche {tranche_val} vs floor×0.90 = {expected:.2f} (Δ = {delta:.2f}, within rounding)")

    # ── 5. Hurdle rate ─────────────────────────────────────────────────────
    # Priority: YAML field > fallback map (manually verified) > body regex
    hurdle_yaml = fm.get("hurdle")
    hurdle_val = None

    if hurdle_yaml is not None:
        m = re.search(r"([\d\.]+)", str(hurdle_yaml))
        if m:
            hurdle_val = float(m.group(1))
        add("NOTE", "hurdle-source", f"Hurdle from YAML field: {hurdle_yaml}")
    elif ticker in KNOWN_HURDLE_FALLBACK:
        hurdle_val = KNOWN_HURDLE_FALLBACK[ticker]
        add("NOTE", "hurdle-source",
            f"Hurdle from verified map: {hurdle_val}% (no YAML field; body regex skipped to avoid historical-rate noise)")
    else:
        hurdle_val = extract_hurdle_from_body(body)
        if hurdle_val is not None:
            add("NOTE", "hurdle-source", f"Hurdle from body text: {hurdle_val}% (no YAML field)")
        else:
            add("WARN", "hurdle-missing", "Hurdle rate not found in YAML, map, or body text")

    if hurdle_val is not None and abs(hurdle_val - CURRENT_HURDLE) > 0.02:
        add("WARN", "hurdle-stale",
            f"Hurdle {hurdle_val}% ≠ current {CURRENT_HURDLE_LABEL} "
            f"(Δ = {abs(hurdle_val - CURRENT_HURDLE):.2f}pp) — floor/ceiling may need re-derivation")

    # ── 6. EPS → floor multiple (informational only) ───────────────────────
    if ticker in NAV_ANCHORED:
        add("NOTE", "eps-arithmetic", "NAV-anchored file — EPS multiple arithmetic skipped")
    else:
        eps = extract_eps_from_body(body)
        if eps is not None and floor_parsed is not None and ceiling_parsed is not None:
            floor_val = floor_parsed[2]
            ceil_val = ceiling_parsed[2]
            floor_mult = floor_val / eps
            ceil_ey = eps / ceil_val * 100
            add("NOTE", "eps-arithmetic",
                f"EPS {eps:.2f} → implied floor multiple {floor_mult:.2f}× "
                f"| ceiling E/Y {ceil_ey:.1f}%"
                + (f" (vs hurdle {hurdle_val}%)" if hurdle_val else ""))
        elif eps is None:
            add("NOTE", "eps-arithmetic", "Sustainable EPS not found in body text")

    # ── 7. Required sections ───────────────────────────────────────────────
    section_results = check_sections(body)
    is_closed = ("CLOSED" in str(fm.get("status", "")) or
                 "CLOSED" in str(fm.get("verdict", "")))

    for name in CORE_SECTIONS:
        if not section_results.get(name, True):
            if is_closed:
                add("NOTE", "missing-section", f"Core section not found (file CLOSED): {name!r}")
            else:
                add("WARN", "missing-section", f"Core section not found: {name!r}")
    for name in RECOMMENDED_SECTIONS:
        if not section_results.get(name, True):
            if is_closed:
                add("NOTE", "missing-section", f"Recommended section absent (file CLOSED): {name!r}")
            else:
                add("WARN", "missing-section", f"Recommended section not found: {name!r}")
    for name in OPTIONAL_SECTIONS:
        if not section_results.get(name, False):
            add("NOTE", "missing-section", f"Optional section absent: {name!r}")

    # ── 8. Wikilinks ───────────────────────────────────────────────────────
    wikilinks = re.findall(r"\[\[([^\]]+)\]\]", text)
    if wikilinks:
        add("NOTE", "wikilinks", f"Found {len(wikilinks)} [[wikilink]](s): {wikilinks[:5]}")

    return issues


# ── main ───────────────────────────────────────────────────────────────────

def main():
    vault_root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
    vault_root = os.path.realpath(vault_root)
    research_dir = os.path.join(vault_root, VAULT_RESEARCH_DIR)

    if not os.path.isdir(research_dir):
        print(f"FAIL: research directory not found: {research_dir}", file=sys.stderr)
        sys.exit(1)

    md_files = sorted(
        f for f in os.listdir(research_dir)
        if f.endswith(".md")
    )

    total_fails = 0
    total_warns = 0
    total_notes = 0
    file_summaries = []

    print(f"\n{'='*70}")
    print(f"  CSE VAULT VALIDATOR  — {len(md_files)} files in {research_dir}")
    print(f"  Current hurdle: {CURRENT_HURDLE_LABEL}  |  Second-tranche factor: {SECOND_TRANCHE_FACTOR}")
    print(f"{'='*70}\n")

    for fname in md_files:
        path = os.path.join(research_dir, fname)
        issues = audit_file(path)

        file_fails = sum(1 for s, _, _ in issues if s == "FAIL")
        file_warns = sum(1 for s, _, _ in issues if s == "WARN")
        file_notes = sum(1 for s, _, _ in issues if s == "NOTE")
        total_fails += file_fails
        total_warns += file_warns
        total_notes += file_notes

        status = "FAIL" if file_fails else ("WARN" if file_warns else "PASS")
        print(f"  [{status:4s}]  {fname}")
        for severity, check, msg in issues:
            indent = "          "
            print(f"{indent}{severity:4s}  [{check}]  {msg}")
        if not issues:
            print(f"          (no issues)")
        print()

        file_summaries.append((fname, status, file_fails, file_warns, file_notes))

    print(f"{'='*70}")
    print(f"  SUMMARY: {total_fails} FAIL | {total_warns} WARN | {total_notes} NOTE")
    print(f"{'='*70}\n")

    if total_fails:
        print(f"  FILES WITH FAIL:")
        for fname, status, ff, fw, fn in file_summaries:
            if ff:
                print(f"    {fname}  ({ff} fail)")
    if total_warns:
        print(f"  FILES WITH WARN:")
        for fname, status, ff, fw, fn in file_summaries:
            if fw:
                print(f"    {fname}  ({fw} warn)")
    print()

    sys.exit(1 if total_fails else 0)


if __name__ == "__main__":
    main()
