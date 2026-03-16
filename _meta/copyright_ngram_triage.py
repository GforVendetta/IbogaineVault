#!/usr/bin/env python3
"""
IbogaineVault Copyright N-gram Triage
=====================================
Compares vault markdown files against source PDFs using n-gram overlap
to detect verbatim or near-verbatim text that must be reconverted before
Tier 1 public release.

Usage:
    python3 _meta/copyright_ngram_triage.py

Output:
    - Console summary with colour-coded verdicts
    - Saves full audit to _meta/copyright_ngram_analysis_2026-03-15.md

Requires: pymupdf (pip install pymupdf --break-system-packages)
"""

import fitz  # pymupdf
import re
import sys
from pathlib import Path
from datetime import date
from typing import Optional

# --- Paths ---
VAULT = Path('/Users/aretesofia/IbogaineVault')
PDF_BASE = Path('/Users/aretesofia/Library/Mobile Documents/com~apple~CloudDocs/IbogaineVault_PDFs')

# --- The 17 papers to analyse ---
PAPERS = [
    ("2000/Mash2000_Ibogaine_Pharmacokinetics_Safety", "Wiley", "Ann NYAS", 740),
    ("2025/Hwu2025_Matrix_Pharmacology_VMAT2_SERT", "ACS", "ACS Chem Neurosci", 552),
    ("2019/Iyer2019_Iboga_Enigma_Chemistry_Neuropharmacology_Alkaloids_Analogs", "RSC", "Nat Prod Rep", 474),
    ("2023/Arias2023_Catharanthine_18-MC", "Elsevier", "Eur J Pharmacol", 454),
    ("2024/Cherian2024_Magnesium_Ibogaine_TBI", "Springer Nature", "Nature Medicine", 452),
    ("2025/Iyer2025_Modular_Synthesis_Nature_Chemistry", "Springer Nature", "Nature Chem", 395),
    ("2000/Mundey2000_Ibogaine_18MC_Smooth_Muscle", "Wiley", "Br J Pharmacol", 384),
    ("2021/Knuijver2021_Safety_Opioid_Detox", "Wiley", "Addiction", 378),
    ("2010/Arias2010_Interactions_Ibogaine_NicotinicAChR_Human", "Elsevier", "Int J Biochem CB", 335),
    ("2024/Knuijver2024_Pharmacokinetics_Pharmacodynamics_Ibogaine_OUD_Patients", "SAGE", "J Psychopharmacol", 318),
    ("2020/Bhat2020_Tropane_Ibo_Analog_SERT_DAT", "ACS", "ACS Pharmacol Transl", 304),
    ("2023/Davis2023_Ibogaine_5MeO-DMT_for_SEALS", "T&F", "Am J Drug Alcohol", 294),
    ("2010/Carnicella2010_Noribogaine_18MC_GDNF", "Wiley", "Addict Biol", 266),
    ("1995/Hearn1995_Noribogaine_Metabolite", "Oxford", "J Anal Toxicol", 266),
    ("2010/Paskulin2010_Yeast_Enzymes_Ibogaine_Adaptation_ATP", "Elsevier", "Eur J Pharmacol", 258),
    ("2020/Wilson2020_Novel_Tx_OUD_Ibogaine_Iboga_Case_Study", "T&F", "J Psychoactive Drugs", 208),
    ("1999/Glick1999_18MC_Review_CNS_Drugs", "Wiley", "CNS Drug Rev", 206),
]


# ============================================================
# TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_path: Path) -> str:
    """Extract all text from PDF via pymupdf."""
    doc = fitz.open(str(pdf_path))
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def extract_md_body(md_path: Path) -> str:
    """Extract body text from vault markdown, stripping frontmatter and formatting."""
    content = md_path.read_text(errors='replace')
    # Strip YAML frontmatter
    body = re.sub(r'^---\n.+?\n---\n?', '', content, flags=re.DOTALL)
    # Strip markdown formatting but keep text
    body = re.sub(r'^#{1,6}\s+', '', body, flags=re.MULTILINE)
    body = re.sub(r'\[\[([^\]|]+?)(?:\|([^\]]*?))?\]\]', lambda m: m.group(2) or m.group(1), body)
    body = re.sub(r'\[([^\]]+?)\]\([^)]+?\)', r'\1', body)
    body = re.sub(r'[*_`~]', '', body)
    body = re.sub(r'^\s*[-|].*$', '', body, flags=re.MULTILINE)  # table rows
    body = re.sub(r'```.*?```', '', body, flags=re.DOTALL)  # code blocks
    return body


def strip_references(text: str) -> str:
    """Remove reference/bibliography sections — identical by definition, inflate overlap."""
    # Match common section headers for references
    patterns = [
        r'(?i)\n\s*references?\s*\n.*$',
        r'(?i)\n\s*bibliography\s*\n.*$',
        r'(?i)\n\s*works?\s+cited\s*\n.*$',
        r'(?i)\n\s*literature\s+cited\s*\n.*$',
    ]
    for pat in patterns:
        text = re.sub(pat, '', text, flags=re.DOTALL)
    return text


def normalise(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def make_ngrams(text: str, n: int = 4) -> set:
    """Generate n-grams (set of tuples) from normalised text."""
    words = text.split()
    if len(words) < n:
        return set()
    return set(tuple(words[i:i+n]) for i in range(len(words) - n + 1))


def compute_overlap(md_ng: set, pdf_ng: set) -> tuple:
    """Returns (overlap_ratio, overlap_count, md_count)."""
    if not md_ng:
        return (0.0, 0, 0)
    shared = md_ng & pdf_ng
    return (len(shared) / len(md_ng), len(shared), len(md_ng))


def verdict_emoji(ratio: float) -> tuple:
    """Returns (emoji, label) for a given overlap ratio."""
    if ratio > 0.50:
        return ("🔴", "VERBATIM")
    elif ratio > 0.35:
        return ("🟠", "CONCERNING")
    elif ratio > 0.20:
        return ("🟡", "MODERATE")
    else:
        return ("🟢", "REWRITTEN")


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyse_paper(stem: str, publisher: str, journal: str, lines: int) -> Optional[dict]:
    """Run multi-n-gram analysis on a single paper. Returns result dict or None."""
    md_path = VAULT / f"{stem}.md"
    pdf_path = PDF_BASE / f"{stem}.pdf"

    if not md_path.exists():
        print(f"  ⚠ SKIP (no MD): {stem}")
        return None
    if not pdf_path.exists():
        print(f"  ⚠ SKIP (no PDF): {stem}")
        return None

    # Extract and clean
    pdf_raw = extract_pdf_text(pdf_path)
    md_raw = extract_md_body(md_path)

    # Strip references from both before normalising
    pdf_clean = strip_references(pdf_raw)
    md_clean = strip_references(md_raw)

    pdf_norm = normalise(pdf_clean)
    md_norm = normalise(md_clean)

    md_words = len(md_norm.split())
    pdf_words = len(pdf_norm.split())

    # Multi-n-gram analysis (4, 6, 8)
    result = {
        'stem': stem,
        'file': stem.split('/')[-1],
        'publisher': publisher,
        'journal': journal,
        'body_lines': lines,
        'md_words': md_words,
        'pdf_words': pdf_words,
    }

    for n in (4, 6, 8):
        md_ng = make_ngrams(md_norm, n)
        pdf_ng = make_ngrams(pdf_norm, n)
        ratio, shared, total = compute_overlap(md_ng, pdf_ng)
        result[f'{n}g_ratio'] = ratio
        result[f'{n}g_shared'] = shared
        result[f'{n}g_total'] = total

    # Estimate "verbatim word equivalent" from 4-gram overlap
    # Each shared 4-gram ≈ 1 word of truly shared text (sliding window),
    # so shared_4grams ≈ words of verbatim-equivalent content
    result['verbatim_word_equiv'] = result['4g_shared']

    return result


# ============================================================
# OUTPUT FORMATTING
# ============================================================

def print_header():
    w = 110
    print("=" * w)
    print("IbogaineVault — Copyright N-gram Triage")
    print(f"Date: {date.today().isoformat()}")
    print(f"Papers: {len(PAPERS)} | Method: 4/6/8-gram overlap | Refs stripped: yes")
    print("=" * w)
    print()

def print_result_line(r: dict):
    emoji, label = verdict_emoji(r['4g_ratio'])
    print(f"  {emoji} {r['4g_ratio']:.3f}  "
          f"6g={r['6g_ratio']:.3f}  8g={r['8g_ratio']:.3f}  "
          f"| {r['md_words']:5d} wds  "
          f"| ~{r['verbatim_word_equiv']:4d} verbatim-equiv  "
          f"| {r['publisher']:15s} | {r['file']}")


def print_summary(results: list):
    results_sorted = sorted(results, key=lambda x: -x['4g_ratio'])

    print()
    print("=" * 110)
    print("RANKED SUMMARY (by 4-gram overlap, refs stripped)")
    print("=" * 110)
    print()
    print(f"  {'':4s} {'4g':>6s}  {'6g':>6s}  {'8g':>6s}  "
          f"| {'Words':>6s}  | {'~Verb':>5s}  | {'Publisher':15s} | File")
    print(f"  {'':4s} {'─'*6}  {'─'*6}  {'─'*6}  "
          f"| {'─'*6}  | {'─'*5}  | {'─'*15} | {'─'*40}")

    for r in results_sorted:
        print_result_line(r)

    # Tier counts
    reds = [r for r in results_sorted if r['4g_ratio'] > 0.50]
    oranges = [r for r in results_sorted if 0.35 < r['4g_ratio'] <= 0.50]
    yellows = [r for r in results_sorted if 0.20 < r['4g_ratio'] <= 0.35]
    greens = [r for r in results_sorted if r['4g_ratio'] <= 0.20]

    print()
    print(f"  🔴 Likely verbatim  (>0.50):  {len(reds):2d} papers — NEED RECONVERSION")
    print(f"  🟠 Concerning    (0.35–0.50):  {len(oranges):2d} papers — manual review")
    print(f"  🟡 Moderate      (0.20–0.35):  {len(yellows):2d} papers — likely OK")
    print(f"  🟢 Rewritten       (<0.20):    {len(greens):2d} papers — clear")

    total_verbatim = sum(r['verbatim_word_equiv'] for r in reds + oranges)
    print()
    print(f"  Total verbatim-equivalent words in 🔴+🟠 papers: ~{total_verbatim:,d}")
    print()

    # N-gram signature insight
    print("  N-GRAM SIGNATURE CHECK (verbatim text stays high across all n; rewritten drops)")
    print(f"  {'':4s} {'File':45s} {'4g':>6s} → {'6g':>6s} → {'8g':>6s}  {'Drop':>6s}")
    for r in results_sorted[:10]:  # top 10 only
        drop = r['4g_ratio'] - r['8g_ratio']
        print(f"  {'':4s} {r['file']:45s} {r['4g_ratio']:.3f} → {r['6g_ratio']:.3f} → {r['8g_ratio']:.3f}  {drop:+.3f}")

    return results_sorted


def save_audit(results: list):
    """Save full audit to markdown file."""
    out_path = VAULT / '_meta' / f'copyright_ngram_analysis_{date.today().isoformat()}.md'

    lines = [
        '---',
        f'title: "Copyright N-gram Triage — {date.today().isoformat()}"',
        f'created: {date.today().isoformat()}',
        'type: audit',
        '---',
        '',
        '# IbogaineVault Copyright N-gram Triage',
        '',
        f'**Date:** {date.today().isoformat()}',
        f'**Papers analysed:** {len(results)}',
        '**Method:** 4/6/8-gram overlap (references stripped, tables stripped)',
        '',
        '## Thresholds',
        '',
        '| 4-gram overlap | Interpretation | Action |',
        '|----------------|----------------|--------|',
        '| < 0.20 | 🟢 Genuinely rewritten | Clear |',
        '| 0.20 – 0.35 | 🟡 Moderate similarity | Likely OK |',
        '| 0.35 – 0.50 | 🟠 Concerning | Manual review needed |',
        '| > 0.50 | 🔴 Likely verbatim | Needs reconversion |',
        '',
        '## Results (ranked by 4-gram overlap)',
        '',
    ]
    # Markdown table
    lines.append('| Status | 4g | 6g | 8g | Words | ~Verbatim | Publisher | File |')
    lines.append('|--------|-----|-----|-----|-------|-----------|-----------|------|')

    for r in results:
        emoji, label = verdict_emoji(r['4g_ratio'])
        lines.append(
            f"| {emoji} {label} | {r['4g_ratio']:.3f} | {r['6g_ratio']:.3f} | {r['8g_ratio']:.3f} "
            f"| {r['md_words']:,d} | ~{r['verbatim_word_equiv']:,d} | {r['publisher']} | {r['file']} |"
        )

    # Tier summary
    reds = [r for r in results if r['4g_ratio'] > 0.50]
    oranges = [r for r in results if 0.35 < r['4g_ratio'] <= 0.50]
    yellows = [r for r in results if 0.20 < r['4g_ratio'] <= 0.35]
    greens = [r for r in results if r['4g_ratio'] <= 0.20]

    lines.append('')
    lines.append('## Summary')
    lines.append('')
    lines.append(f'- 🔴 **Likely verbatim (>0.50):** {len(reds)} papers — NEED RECONVERSION')
    lines.append(f'- 🟠 **Concerning (0.35–0.50):** {len(oranges)} papers — manual review')
    lines.append(f'- 🟡 **Moderate (0.20–0.35):** {len(yellows)} papers — likely OK')
    lines.append(f'- 🟢 **Rewritten (<0.20):** {len(greens)} papers — clear')

    total_v = sum(r['verbatim_word_equiv'] for r in reds + oranges)
    lines.append(f'- **Total verbatim-equivalent words in 🔴+🟠:** ~{total_v:,d}')
    lines.append('')
    out_path.write_text('\n'.join(lines))
    print(f"\n  Audit saved → {out_path}")


# ============================================================
# MAIN
# ============================================================

def main():
    print_header()

    # Check pymupdf
    try:
        fitz.version
    except Exception:
        print("ERROR: pymupdf not installed. Run: pip install pymupdf --break-system-packages")
        sys.exit(1)

    # Check paths
    if not VAULT.exists():
        print(f"ERROR: Vault not found at {VAULT}")
        sys.exit(1)
    if not PDF_BASE.exists():
        print(f"ERROR: PDF base not found at {PDF_BASE}")
        sys.exit(1)

    results = []
    skipped = []

    print(f"Processing {len(PAPERS)} papers...\n")

    for i, (stem, publisher, journal, lines) in enumerate(PAPERS, 1):
        print(f"[{i:2d}/{len(PAPERS)}] {stem.split('/')[-1]}")
        result = analyse_paper(stem, publisher, journal, lines)
        if result:
            emoji, label = verdict_emoji(result['4g_ratio'])
            print(f"        → {emoji} {result['4g_ratio']:.3f} "
                  f"(~{result['verbatim_word_equiv']} verbatim-equiv words)\n")
            results.append(result)
        else:
            skipped.append(stem)
            print()

    if not results:
        print("No papers analysed — check file paths.")
        sys.exit(1)

    # Print summary
    sorted_results = print_summary(results)

    # Save audit
    save_audit(sorted_results)

    if skipped:
        print(f"\n  Skipped {len(skipped)} papers (missing files):")
        for s in skipped:
            print(f"    - {s}")

    print("\nDone.")


if __name__ == '__main__':
    main()
