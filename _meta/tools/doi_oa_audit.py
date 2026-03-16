#!/usr/bin/env python3
"""
IbogaineVault — DOI Verification + Open Access Status Audit
=========================================================
Phase 0 script: Batch-verifies DOI resolution and checks OA status
via the Unpaywall API for all vault papers.

Produces a classified report:
  - GREEN:  OA paper — keep full text in Tier1
  - AMBER:  Non-OA, small/niche publisher — keep with fair use framing
  - RED:    Non-OA, aggressive publisher — truncate for Tier1
  - GREY:   No DOI / DOI missing — manual review needed
  - BROKEN: DOI does not resolve — fix required

Usage:
    python3 doi_oa_audit.py [--vault PATH] [--email EMAIL] [--output PATH]

Defaults:
    --vault   /Users/aretesofia/IbogaineVault
    --email   philip@pangeabiomedics.com  (for Unpaywall polite pool)
    --output  /Users/aretesofia/IbogaineVault/_meta/tools/doi_oa_report.md

Requirements:
    pip3 install requests pyyaml
"""

import os
import sys
import re
import time
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

try:
    import yaml
    import requests
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip3 install requests pyyaml")
    sys.exit(1)


# ── Aggressive publishers (known to issue DMCA takedowns) ──
AGGRESSIVE_PUBLISHERS = {
    # Normalised lowercase substrings to match against publisher/journal fields
    "elsevier", "springer", "nature publishing", "springer nature",
    "wiley", "john wiley", "taylor & francis", "taylor and francis",
    "informa", "sage publications", "oxford university press",
    "cambridge university press", "american chemical society",
    "ieee", "acs publications", "thieme", "karger",
    "wolters kluwer", "lippincott", "academic press",
}

# Known OA-friendly publishers/journals (likely safe even without Unpaywall confirmation)
OA_FRIENDLY = {
    "plos", "mdpi", "frontiers", "bmc", "biomed central",
    "hindawi", "cureus", "preprints.org", "f1000",
}


def extract_yaml_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, IOError):
        return None

    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None

    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def check_doi_resolution(doi):
    """Check if a DOI resolves. Returns (resolved: bool, redirect_url: str, status_code: int)."""
    if not doi:
        return False, None, None

    # Clean DOI
    doi = doi.strip()
    if doi.startswith("http"):
        # Extract DOI from URL
        doi = re.sub(r'^https?://doi\.org/', '', doi)

    url = f"https://doi.org/{doi}"
    try:
        resp = requests.head(url, allow_redirects=True, timeout=15)
        return resp.status_code == 200, resp.url, resp.status_code
    except requests.RequestException as e:
        return False, None, str(e)


def check_unpaywall(doi, email):
    """Query Unpaywall API for OA status. Returns dict with oa_status, publisher, licence, etc."""
    if not doi:
        return None

    doi = doi.strip()
    if doi.startswith("http"):
        doi = re.sub(r'^https?://doi\.org/', '', doi)

    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return {
                'is_oa': data.get('is_oa', False),
                'oa_status': data.get('oa_status', 'unknown'),  # gold, green, hybrid, bronze, closed
                'publisher': data.get('publisher', 'unknown'),
                'journal': data.get('journal_name', 'unknown'),
                'title': data.get('title', ''),
                'year': data.get('year', ''),
                'best_oa_location': data.get('best_oa_location', {}),
                'doi_url': data.get('doi_url', ''),
            }
        elif resp.status_code == 404:
            return {'is_oa': None, 'oa_status': 'not_found', 'publisher': 'unknown', 'journal': 'unknown'}
        else:
            return {'is_oa': None, 'oa_status': f'error_{resp.status_code}', 'publisher': 'unknown', 'journal': 'unknown'}
    except requests.RequestException:
        return {'is_oa': None, 'oa_status': 'error_network', 'publisher': 'unknown', 'journal': 'unknown'}


def classify_paper(doi_resolves, unpaywall_data, yaml_data):
    """
    Classify a paper into risk tiers:
      GREEN  — OA, keep full text
      AMBER  — Non-OA but small/niche publisher, keep with fair use framing
      RED    — Non-OA + aggressive publisher, truncate for Tier1
      GREY   — No DOI or Unpaywall can't find it, manual review
      BROKEN — DOI doesn't resolve, needs fixing
    """
    doi = yaml_data.get('doi', '')

    if not doi or doi.strip() == '':
        return 'GREY', 'No DOI in YAML'

    if not doi_resolves:
        return 'BROKEN', 'DOI does not resolve'

    if unpaywall_data is None:
        return 'GREY', 'Unpaywall lookup failed'

    if unpaywall_data.get('oa_status') == 'not_found':
        return 'GREY', 'DOI not in Unpaywall database'

    if unpaywall_data.get('is_oa'):
        licence = ''
        best_loc = unpaywall_data.get('best_oa_location') or {}
        if best_loc:
            licence = best_loc.get('license', '') or ''
        oa_type = unpaywall_data.get('oa_status', 'unknown')
        return 'GREEN', f'Open Access ({oa_type}), licence: {licence or "not specified"}'

    # Non-OA — check publisher
    publisher = (unpaywall_data.get('publisher') or '').lower()
    journal = (unpaywall_data.get('journal') or '').lower()
    combined = f"{publisher} {journal}"

    for aggressive in AGGRESSIVE_PUBLISHERS:
        if aggressive in combined:
            return 'RED', f'Non-OA, aggressive publisher: {unpaywall_data.get("publisher", "unknown")}'

    return 'AMBER', f'Non-OA, publisher: {unpaywall_data.get("publisher", "unknown")}'


def find_vault_papers(vault_path):
    """Find all paper markdown files in the vault (year folders + special dirs)."""
    papers = []
    vault = Path(vault_path)

    # Year folders (1957-2026)
    for year_dir in sorted(vault.iterdir()):
        if year_dir.is_dir() and re.match(r'^\d{4}$', year_dir.name):
            for md_file in sorted(year_dir.glob('*.md')):
                papers.append(md_file)

    # Special directories
    for special_dir in ['Clinical_Guidelines', 'Primary_Sources', 'Industry_Documents', 'Other']:
        sdir = vault / special_dir
        if sdir.is_dir():
            for md_file in sorted(sdir.rglob('*.md')):
                papers.append(md_file)

    return papers


def generate_report(results, output_path):
    """Generate a markdown report classified by risk tier."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    counts = defaultdict(int)
    for r in results:
        counts[r['tier']] += 1

    lines = [
        f"# IbogaineVault — DOI + Open Access Audit Report",
        f"",
        f"**Generated:** {now}",
        f"**Papers scanned:** {len(results)}",
        f"",
        f"## Summary",
        f"",
        f"| Tier | Count | Action |",
        f"|------|-------|--------|",
        f"| GREEN (OA) | {counts.get('GREEN', 0)} | Keep full text in Tier1 |",
        f"| AMBER (Non-OA, small publisher) | {counts.get('AMBER', 0)} | Keep with fair use framing |",
        f"| RED (Non-OA, aggressive publisher) | {counts.get('RED', 0)} | **Truncate for Tier1** |",
        f"| GREY (No DOI / not found) | {counts.get('GREY', 0)} | Manual review needed |",
        f"| BROKEN (DOI doesn't resolve) | {counts.get('BROKEN', 0)} | **Fix DOI** |",
        f"",
        f"---",
        f"",
    ]

    # RED papers first (action required)
    if counts.get('RED', 0) > 0:
        lines.append("## RED — Truncate for Tier1 (Non-OA, Aggressive Publisher)")
        lines.append("")
        lines.append("These papers are from publishers known to issue DMCA takedowns.")
        lines.append("Tier1 versions should contain: YAML + abstract + analytical summary + See Also only.")
        lines.append("")
        lines.append("| File | Year | Publisher | Journal | DOI |")
        lines.append("|------|------|-----------|---------|-----|")
        for r in sorted(results, key=lambda x: x.get('year', 0)):
            if r['tier'] == 'RED':
                lines.append(f"| {r['filename']} | {r.get('year', '')} | {r.get('publisher', '')} | {r.get('journal', '')} | {r.get('doi', '')} |")
        lines.append("")

    # BROKEN DOIs
    if counts.get('BROKEN', 0) > 0:
        lines.append("## BROKEN — DOI Does Not Resolve")
        lines.append("")
        lines.append("| File | Year | DOI | Error |")
        lines.append("|------|------|-----|-------|")
        for r in sorted(results, key=lambda x: x.get('year', 0)):
            if r['tier'] == 'BROKEN':
                lines.append(f"| {r['filename']} | {r.get('year', '')} | {r.get('doi', '')} | {r.get('reason', '')} |")
        lines.append("")

    # GREY (manual review)
    if counts.get('GREY', 0) > 0:
        lines.append("## GREY — Manual Review Needed")
        lines.append("")
        lines.append("| File | Year | Reason |")
        lines.append("|------|------|--------|")
        for r in sorted(results, key=lambda x: x.get('year', 0)):
            if r['tier'] == 'GREY':
                lines.append(f"| {r['filename']} | {r.get('year', '')} | {r.get('reason', '')} |")
        lines.append("")

    # GREEN (safe)
    if counts.get('GREEN', 0) > 0:
        lines.append("## GREEN — Open Access (Keep Full Text)")
        lines.append("")
        lines.append("| File | Year | OA Type | Publisher | Licence |")
        lines.append("|------|------|---------|-----------|---------|")
        for r in sorted(results, key=lambda x: x.get('year', 0)):
            if r['tier'] == 'GREEN':
                lines.append(f"| {r['filename']} | {r.get('year', '')} | {r.get('reason', '')} | {r.get('publisher', '')} | {r.get('licence', '')} |")
        lines.append("")

    # AMBER (keep with framing)
    if counts.get('AMBER', 0) > 0:
        lines.append("## AMBER — Non-OA, Small/Niche Publisher (Keep with Fair Use Framing)")
        lines.append("")
        lines.append("| File | Year | Publisher | Journal |")
        lines.append("|------|------|-----------|---------|")
        for r in sorted(results, key=lambda x: x.get('year', 0)):
            if r['tier'] == 'AMBER':
                lines.append(f"| {r['filename']} | {r.get('year', '')} | {r.get('publisher', '')} | {r.get('journal', '')} |")
        lines.append("")

    # Write report
    report_text = '\n'.join(lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    # Also write JSON for programmatic use
    json_path = str(output_path).replace('.md', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)

    return report_text


def main():
    parser = argparse.ArgumentParser(description='IbogaineVault DOI + OA Status Audit')
    parser.add_argument('--vault', default='/Users/aretesofia/IbogaineVault',
                        help='Path to the working vault')
    parser.add_argument('--email', default='philip@ibogaine.space',
                        help='Email for Unpaywall API polite pool')
    parser.add_argument('--output', default=None,
                        help='Output report path (default: vault/_meta/tools/doi_oa_report.md)')
    parser.add_argument('--skip-resolve', action='store_true',
                        help='Skip DOI resolution check (faster, Unpaywall only)')
    parser.add_argument('--delay', type=float, default=0.2,
                        help='Delay between API calls in seconds (be polite)')
    args = parser.parse_args()

    if args.output is None:
        args.output = os.path.join(args.vault, '_meta', 'tools', 'doi_oa_report.md')

    print("=" * 60)
    print("  IbogaineVault — DOI + Open Access Audit")
    print(f"  Vault: {args.vault}")
    print(f"  Email: {args.email}")
    print(f"  Output: {args.output}")
    print("=" * 60)
    print()

    # Find papers
    papers = find_vault_papers(args.vault)
    print(f"Found {len(papers)} paper files.")
    print()

    results = []
    for i, paper_path in enumerate(papers):
        filename = str(paper_path.relative_to(args.vault))
        yaml_data = extract_yaml_frontmatter(paper_path)

        if yaml_data is None:
            results.append({
                'filename': filename,
                'tier': 'GREY',
                'reason': 'Could not parse YAML frontmatter',
                'doi': '',
                'year': '',
            })
            print(f"  [{i+1}/{len(papers)}] {filename} — GREY (no YAML)")
            continue

        doi = yaml_data.get('doi', '')
        year = yaml_data.get('year', '')

        if not doi or str(doi).strip() in ('', 'N/A', 'n/a', 'none', 'None'):
            results.append({
                'filename': filename,
                'tier': 'GREY',
                'reason': 'No DOI in YAML',
                'doi': '',
                'year': year,
            })
            print(f"  [{i+1}/{len(papers)}] {filename} — GREY (no DOI)")
            continue

        # Clean DOI for display
        clean_doi = doi.strip()
        if clean_doi.startswith("http"):
            clean_doi = re.sub(r'^https?://doi\.org/', '', clean_doi)

        # Check DOI resolution
        doi_resolves = True
        if not args.skip_resolve:
            doi_resolves, redirect_url, status = check_doi_resolution(clean_doi)
            time.sleep(args.delay / 2)

        # Check Unpaywall
        unpaywall_data = check_unpaywall(clean_doi, args.email)
        time.sleep(args.delay)

        # Classify
        tier, reason = classify_paper(doi_resolves, unpaywall_data, yaml_data)

        result = {
            'filename': filename,
            'tier': tier,
            'reason': reason,
            'doi': clean_doi,
            'year': year,
            'publisher': (unpaywall_data or {}).get('publisher', ''),
            'journal': (unpaywall_data or {}).get('journal', ''),
            'licence': '',
        }

        # Extract licence for GREEN
        if tier == 'GREEN' and unpaywall_data:
            best_loc = unpaywall_data.get('best_oa_location') or {}
            result['licence'] = best_loc.get('license', '') or ''

        results.append(result)
        print(f"  [{i+1}/{len(papers)}] {filename} — {tier} ({reason[:60]})")

    print()
    print("Generating report...")
    report = generate_report(results, args.output)

    # Print summary
    counts = defaultdict(int)
    for r in results:
        counts[r['tier']] += 1

    print()
    print("=" * 60)
    print("  AUDIT COMPLETE")
    print("=" * 60)
    print(f"  GREEN (OA, keep full text):       {counts.get('GREEN', 0)}")
    print(f"  AMBER (Non-OA, small publisher):  {counts.get('AMBER', 0)}")
    print(f"  RED (Non-OA, aggressive pub):     {counts.get('RED', 0)}")
    print(f"  GREY (No DOI / not found):        {counts.get('GREY', 0)}")
    print(f"  BROKEN (DOI doesn't resolve):     {counts.get('BROKEN', 0)}")
    print(f"  TOTAL:                            {len(results)}")
    print()
    print(f"  Report: {args.output}")
    print(f"  JSON:   {args.output.replace('.md', '.json')}")
    print()

    # Exit code: 1 if any RED or BROKEN papers found
    if counts.get('RED', 0) > 0 or counts.get('BROKEN', 0) > 0:
        print("  ⚠️  Action required — see RED and BROKEN sections in report.")
        sys.exit(1)
    else:
        print("  ✅  No immediate action required.")
        sys.exit(0)


if __name__ == '__main__':
    main()
