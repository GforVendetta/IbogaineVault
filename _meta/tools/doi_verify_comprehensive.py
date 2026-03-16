#!/usr/bin/env python3
"""
IbogaineVault — Comprehensive DOI Verification
=============================================
Verifies every vault DOI against CrossRef/PubMed registered metadata.
Catches SILENT MISMATCHES: DOIs that resolve but point to the wrong paper.

Strategy:
  1. CrossRef /works/{doi} — returns registered title/authors/year (primary)
  2. PubMed esearch+esummary — fallback for biomedical papers not in CrossRef
  3. Fuzzy title comparison (SequenceMatcher) to detect mismatches

Output classifications:
  VERIFIED       — CrossRef title matches vault title (ratio >= 0.75)
  MISMATCH       — DOI points to a different paper (ratio < 0.50)
  UNCERTAIN      — Partial match (0.50 <= ratio < 0.75), needs manual check
  CR_NOT_FOUND   — DOI not in CrossRef (try PubMed fallback)
  PUBMED_VERIFIED — Not in CrossRef but PubMed confirms match
  NO_DOI         — Paper has no DOI in YAML
  ERROR          — API error during verification

Usage:
    python3 doi_verify_comprehensive.py [--vault PATH] [--output PATH] [--delay SECONDS]

Requirements:
    pip3 install requests pyyaml
"""

import os
import sys
import re
import json
import time
import unicodedata
import argparse
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from collections import defaultdict, Counter
from urllib.parse import quote

try:
    import yaml
    import requests
except ImportError:
    print("ERROR: pip3 install requests pyyaml")
    sys.exit(1)

# ── Configuration ──
CROSSREF_BASE = "https://api.crossref.org/works"
PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

HEADERS = {
    "User-Agent": "IbogaineVault/1.0 (https://github.com/ibogavault; mailto:philip@pangeabiomedics.com)",
}

# Thresholds for fuzzy title matching
MATCH_VERIFIED = 0.75   # >= this = verified match
MATCH_UNCERTAIN = 0.50  # >= this but < VERIFIED = uncertain, needs manual check
                        # < UNCERTAIN = mismatch


def normalise_title(title):
    """Normalise a title for comparison: lowercase, strip accents, remove punctuation."""
    if not title:
        return ""
    # Unicode normalise (decompose accents)
    title = unicodedata.normalize('NFKD', str(title))
    title = ''.join(c for c in title if not unicodedata.combining(c))
    # Lowercase
    title = title.lower()
    # Remove common prefixes/suffixes publishers add
    title = re.sub(r'\s*\[.*?\]\s*', ' ', title)  # [PubMed] [Retracted] etc
    title = re.sub(r'\s*\(.*?erratum.*?\)\s*', ' ', title, flags=re.IGNORECASE)
    # Remove punctuation except spaces
    title = re.sub(r'[^\w\s]', ' ', title)
    # Collapse whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    return title


def title_similarity(title_a, title_b):
    """Compare two titles after normalisation. Returns ratio 0.0-1.0."""
    a = normalise_title(title_a)
    b = normalise_title(title_b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


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


def extract_first_author(yaml_data):
    """Extract first author surname from YAML authors field."""
    authors = yaml_data.get('authors', [])
    if not authors:
        return ""
    first = authors[0] if isinstance(authors, list) else str(authors)
    if isinstance(first, dict):
        return first.get('family', first.get('name', ''))
    # String: "Surname, Given" or "Given Surname"
    first = str(first).strip()
    if ',' in first:
        return first.split(',')[0].strip()
    parts = first.split()
    return parts[-1] if parts else ""


def clean_doi(doi):
    """Clean a DOI string to its canonical form."""
    if not doi:
        return ""
    doi = str(doi).strip()
    doi = re.sub(r'^https?://doi\.org/', '', doi)
    doi = re.sub(r'^doi:\s*', '', doi, flags=re.IGNORECASE)
    return doi.strip()


def query_crossref(doi, session):
    """
    Query CrossRef for DOI metadata.
    Returns dict with title, authors, year, container, or None on failure.
    """
    url = f"{CROSSREF_BASE}/{quote(doi, safe='/:')}"
    try:
        resp = session.get(url, headers=HEADERS, timeout=20)
        if resp.status_code == 200:
            msg = resp.json().get('message', {})
            # Extract title
            titles = msg.get('title', [])
            title = titles[0] if titles else ""
            # Extract authors
            authors = []
            for a in msg.get('author', []):
                authors.append({
                    'family': a.get('family', ''),
                    'given': a.get('given', ''),
                })
            # Extract year (try multiple date fields)
            year = None
            for date_field in ['published-print', 'published-online', 'issued', 'created']:
                dp = msg.get(date_field, {}).get('date-parts', [[]])
                if dp and dp[0] and dp[0][0]:
                    year = dp[0][0]
                    break
            # Container title (journal)
            containers = msg.get('container-title', [])
            container = containers[0] if containers else ""
            
            return {
                'found': True,
                'title': title,
                'authors': authors,
                'year': year,
                'container': container,
                'type': msg.get('type', ''),
                'publisher': msg.get('publisher', ''),
            }
        elif resp.status_code == 404:
            return {'found': False, 'error': 'not_in_crossref'}
        else:
            return {'found': False, 'error': f'http_{resp.status_code}'}
    except requests.exceptions.Timeout:
        return {'found': False, 'error': 'timeout'}
    except requests.exceptions.RequestException as e:
        return {'found': False, 'error': f'request_error: {str(e)[:80]}'}
    except (json.JSONDecodeError, KeyError) as e:
        return {'found': False, 'error': f'parse_error: {str(e)[:80]}'}


def query_pubmed(title, first_author, year, session):
    """
    Search PubMed by title + author + year. Returns DOI and title if found.
    """
    # Build search term
    terms = []
    if title:
        # Use first 100 chars of title for search
        clean_title = re.sub(r'[^\w\s]', ' ', title)[:100].strip()
        terms.append(f"{clean_title}[Title]")
    if first_author:
        terms.append(f"{first_author}[Author]")
    if year:
        terms.append(f"{year}[Date - Publication]")
    
    if not terms:
        return None
    
    query = " AND ".join(terms)
    
    try:
        # Step 1: esearch
        params = {
            'db': 'pubmed',
            'term': query,
            'retmode': 'json',
            'retmax': 3,
        }
        resp = session.get(PUBMED_ESEARCH, params=params, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return None
        
        data = resp.json()
        id_list = data.get('esearchresult', {}).get('idlist', [])
        if not id_list:
            return None
        
        # Step 2: esummary for first result
        params2 = {
            'db': 'pubmed',
            'id': ','.join(id_list[:3]),
            'retmode': 'json',
        }
        resp2 = session.get(PUBMED_ESUMMARY, params=params2, headers=HEADERS, timeout=15)
        if resp2.status_code != 200:
            return None
        
        data2 = resp2.json()
        results = []
        for pmid in id_list[:3]:
            doc = data2.get('result', {}).get(pmid, {})
            if doc:
                # Extract DOI from articleids
                pm_doi = ""
                for aid in doc.get('articleids', []):
                    if aid.get('idtype') == 'doi':
                        pm_doi = aid.get('value', '')
                        break
                results.append({
                    'pmid': pmid,
                    'title': doc.get('title', ''),
                    'doi': pm_doi,
                    'source': doc.get('source', ''),  # journal
                    'pubdate': doc.get('pubdate', ''),
                })
        
        return results if results else None
    
    except Exception:
        return None


def find_vault_papers(vault_path):
    """Find all paper markdown files in the vault."""
    papers = []
    vault = Path(vault_path)
    # Year folders
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


def verify_paper(vault_doi, vault_title, vault_authors, vault_year, session, delay=0.3):
    """
    Verify a single paper's DOI against CrossRef and PubMed.
    Returns classification dict.
    """
    result = {
        'vault_doi': vault_doi,
        'vault_title': vault_title,
        'classification': 'ERROR',
        'title_similarity': 0.0,
        'crossref_title': '',
        'crossref_year': None,
        'crossref_container': '',
        'suggested_doi': '',
        'notes': '',
    }
    
    # Query CrossRef
    cr = query_crossref(vault_doi, session)
    time.sleep(delay)
    
    if cr and cr.get('found'):
        cr_title = cr.get('title', '')
        result['crossref_title'] = cr_title
        result['crossref_year'] = cr.get('year')
        result['crossref_container'] = cr.get('container', '')
        result['crossref_publisher'] = cr.get('publisher', '')
        result['crossref_type'] = cr.get('type', '')
        
        sim = title_similarity(vault_title, cr_title)
        result['title_similarity'] = round(sim, 3)
        
        if sim >= MATCH_VERIFIED:
            result['classification'] = 'VERIFIED'
            # Also check year mismatch as a warning
            if cr.get('year') and vault_year:
                try:
                    if abs(int(vault_year) - int(cr['year'])) > 1:
                        result['notes'] = f"Year mismatch: vault={vault_year}, CrossRef={cr['year']}"
                except (ValueError, TypeError):
                    pass
        elif sim >= MATCH_UNCERTAIN:
            result['classification'] = 'UNCERTAIN'
            result['notes'] = f"Partial title match — vault: '{vault_title[:60]}' vs CR: '{cr_title[:60]}'"
        else:
            result['classification'] = 'MISMATCH'
            result['notes'] = f"DOI points to: '{cr_title[:80]}'"
    
    elif cr and cr.get('error') == 'not_in_crossref':
        result['classification'] = 'CR_NOT_FOUND'
        
        # Fallback: try PubMed
        first_author = ""
        if vault_authors:
            if isinstance(vault_authors, list) and vault_authors:
                a = vault_authors[0]
                if isinstance(a, dict):
                    first_author = a.get('family', a.get('name', ''))
                else:
                    first_author = str(a).split(',')[0].strip() if ',' in str(a) else str(a).split()[-1]
            else:
                first_author = str(vault_authors).split(',')[0].strip()
        
        pm_results = query_pubmed(vault_title, first_author, vault_year, session)
        time.sleep(delay)
        
        if pm_results:
            # Check each PubMed result for title match
            best_sim = 0.0
            best_match = None
            for pm in pm_results:
                sim = title_similarity(vault_title, pm.get('title', ''))
                if sim > best_sim:
                    best_sim = sim
                    best_match = pm
            
            if best_match and best_sim >= MATCH_VERIFIED:
                pm_doi = best_match.get('doi', '')
                if pm_doi and clean_doi(pm_doi) == clean_doi(vault_doi):
                    result['classification'] = 'PUBMED_VERIFIED'
                    result['notes'] = f"PubMed confirms DOI (PMID: {best_match['pmid']})"
                elif pm_doi:
                    result['classification'] = 'PUBMED_DOI_DIFFERS'
                    result['suggested_doi'] = pm_doi
                    result['notes'] = f"PubMed DOI: {pm_doi} (PMID: {best_match['pmid']})"
                else:
                    result['classification'] = 'PUBMED_VERIFIED_NO_DOI'
                    result['notes'] = f"PubMed title matches but no DOI in PubMed (PMID: {best_match['pmid']})"
                result['title_similarity'] = round(best_sim, 3)
            else:
                result['notes'] = "Not in CrossRef; PubMed search inconclusive"
    else:
        result['classification'] = 'ERROR'
        result['notes'] = cr.get('error', 'unknown error') if cr else 'no response'
    
    return result


def generate_report(results, output_path, vault_path):
    """Generate verification report."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    counts = Counter(r['classification'] for r in results)
    total_with_doi = sum(1 for r in results if r.get('vault_doi'))
    total_no_doi = sum(1 for r in results if not r.get('vault_doi'))
    
    lines = [
        "# IbogaineVault — Comprehensive DOI Verification Report\n",
        f"**Generated:** {now}",
        f"**Vault:** {vault_path}",
        f"**Papers with DOIs verified:** {total_with_doi}",
        f"**Papers without DOIs (skipped):** {total_no_doi}",
        "",
        "## Verification Summary\n",
        "| Classification | Count | Description |",
        "|----------------|-------|-------------|",
    ]
    
    class_desc = {
        'VERIFIED': 'CrossRef title matches vault (similarity >= 0.75)',
        'UNCERTAIN': 'Partial match (0.50-0.75) — manual review needed',
        'MISMATCH': 'DOI points to a DIFFERENT paper — FIX REQUIRED',
        'CR_NOT_FOUND': 'DOI not in CrossRef, PubMed inconclusive',
        'PUBMED_VERIFIED': 'Not in CrossRef but PubMed confirms match',
        'PUBMED_DOI_DIFFERS': 'PubMed found paper but with a different DOI',
        'PUBMED_VERIFIED_NO_DOI': 'PubMed title match, no DOI in PubMed',
        'NO_DOI': 'No DOI in vault YAML',
        'ERROR': 'API error during verification',
    }
    
    for cls in ['VERIFIED', 'PUBMED_VERIFIED', 'UNCERTAIN', 'MISMATCH', 
                'PUBMED_DOI_DIFFERS', 'CR_NOT_FOUND', 'PUBMED_VERIFIED_NO_DOI',
                'NO_DOI', 'ERROR']:
        c = counts.get(cls, 0)
        if c > 0:
            lines.append(f"| **{cls}** | {c} | {class_desc.get(cls, '')} |")
    
    lines.append("")
    
    # ── MISMATCH section (critical — action required) ──
    mismatches = [r for r in results if r['classification'] == 'MISMATCH']
    if mismatches:
        lines.append("## ⚠️ MISMATCH — DOI Points to Wrong Paper (FIX REQUIRED)\n")
        lines.append("These DOIs resolve but point to a DIFFERENT paper than what's in the vault.\n")
        for r in sorted(mismatches, key=lambda x: x.get('filename', '')):
            lines.append(f"### {r['filename']}")
            lines.append(f"- **Vault title:** {r['vault_title'][:100]}")
            lines.append(f"- **CrossRef title:** {r['crossref_title'][:100]}")
            lines.append(f"- **Stored DOI:** `{r['vault_doi']}`")
            lines.append(f"- **Title similarity:** {r['title_similarity']}")
            if r.get('suggested_doi'):
                lines.append(f"- **Suggested correct DOI:** `{r['suggested_doi']}`")
            lines.append("")
    
    # ── PUBMED_DOI_DIFFERS section ──
    pm_differs = [r for r in results if r['classification'] == 'PUBMED_DOI_DIFFERS']
    if pm_differs:
        lines.append("## ⚠️ PUBMED_DOI_DIFFERS — PubMed Has Different DOI\n")
        lines.append("Vault DOI not in CrossRef, but PubMed found the paper with a different DOI.\n")
        for r in sorted(pm_differs, key=lambda x: x.get('filename', '')):
            lines.append(f"### {r['filename']}")
            lines.append(f"- **Vault DOI:** `{r['vault_doi']}`")
            lines.append(f"- **PubMed DOI:** `{r['suggested_doi']}`")
            lines.append(f"- **Notes:** {r.get('notes', '')}")
            lines.append("")
    
    # ── UNCERTAIN section ──
    uncertains = [r for r in results if r['classification'] == 'UNCERTAIN']
    if uncertains:
        lines.append("## ⚡ UNCERTAIN — Partial Title Match (Manual Check)\n")
        lines.append("| File | Similarity | Vault Title | CrossRef Title |")
        lines.append("|------|-----------|-------------|----------------|")
        for r in sorted(uncertains, key=lambda x: x['title_similarity']):
            lines.append(f"| {r['filename']} | {r['title_similarity']} | {r['vault_title'][:50]} | {r['crossref_title'][:50]} |")
        lines.append("")
    
    # ── CR_NOT_FOUND section ──
    not_found = [r for r in results if r['classification'] == 'CR_NOT_FOUND']
    if not_found:
        lines.append("## CR_NOT_FOUND — Not in CrossRef, PubMed Inconclusive\n")
        lines.append("| File | DOI | Notes |")
        lines.append("|------|-----|-------|")
        for r in sorted(not_found, key=lambda x: x.get('filename', '')):
            lines.append(f"| {r['filename']} | `{r['vault_doi']}` | {r.get('notes', '')} |")
        lines.append("")
    
    # ── ERROR section ──
    errors = [r for r in results if r['classification'] == 'ERROR']
    if errors:
        lines.append("## ERROR — API Failures\n")
        lines.append("| File | DOI | Error |")
        lines.append("|------|-----|-------|")
        for r in sorted(errors, key=lambda x: x.get('filename', '')):
            lines.append(f"| {r['filename']} | `{r['vault_doi']}` | {r.get('notes', '')} |")
        lines.append("")
    
    # ── VERIFIED with year warnings ──
    year_warnings = [r for r in results if r['classification'] == 'VERIFIED' and r.get('notes')]
    if year_warnings:
        lines.append("## Verified with Year Discrepancy Warnings\n")
        lines.append("| File | DOI | Warning |")
        lines.append("|------|-----|---------|")
        for r in sorted(year_warnings, key=lambda x: x.get('filename', '')):
            lines.append(f"| {r['filename']} | `{r['vault_doi']}` | {r['notes']} |")
        lines.append("")
    
    # ── NO_DOI summary ──
    no_dois = [r for r in results if r['classification'] == 'NO_DOI']
    if no_dois:
        lines.append(f"## NO_DOI — {len(no_dois)} Papers Without DOIs\n")
        lines.append("| File | Year |")
        lines.append("|------|------|")
        for r in sorted(no_dois, key=lambda x: x.get('filename', '')):
            lines.append(f"| {r['filename']} | {r.get('vault_year', '')} |")
        lines.append("")
    
    report_text = "\n".join(lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    json_path = output_path.replace('.md', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    return report_text


def main():
    parser = argparse.ArgumentParser(description='IbogaineVault Comprehensive DOI Verification')
    parser.add_argument('--vault', default='/Users/aretesofia/IbogaineVault')
    parser.add_argument('--output', default=None)
    parser.add_argument('--delay', type=float, default=0.35,
                        help='Delay between API calls (CrossRef polite pool)')
    parser.add_argument('--limit', type=int, default=0,
                        help='Limit number of papers to verify (0 = all)')
    parser.add_argument('--start-from', type=str, default='',
                        help='Start from this filename (for resuming)')
    args = parser.parse_args()
    
    if args.output is None:
        args.output = os.path.join(args.vault, '_meta', 'tools', 'doi_verify_report.md')
    
    print("=" * 65)
    print("  IbogaineVault — Comprehensive DOI Verification")
    print(f"  Vault: {args.vault}")
    print(f"  Delay: {args.delay}s between CrossRef calls")
    print("=" * 65)
    print()
    
    papers = find_vault_papers(args.vault)
    print(f"Found {len(papers)} paper files.\n")
    
    session = requests.Session()
    results = []
    started = not bool(args.start_from)
    verified_count = 0
    
    for i, paper_path in enumerate(papers):
        filename = str(paper_path.relative_to(args.vault))
        
        # Resume support
        if not started:
            if args.start_from in filename:
                started = True
            else:
                continue
        
        yaml_data = extract_yaml_frontmatter(paper_path)
        if yaml_data is None:
            results.append({
                'filename': filename,
                'classification': 'ERROR',
                'vault_doi': '',
                'vault_title': '',
                'vault_year': '',
                'notes': 'Could not parse YAML',
            })
            print(f"  [{i+1}/{len(papers)}] {filename} — ERROR (no YAML)")
            continue
        
        doi = clean_doi(yaml_data.get('doi', ''))
        title = yaml_data.get('title', '')
        year = yaml_data.get('year', '')
        authors = yaml_data.get('authors', [])
        
        if not doi or doi.lower() in ('n/a', 'none', ''):
            results.append({
                'filename': filename,
                'classification': 'NO_DOI',
                'vault_doi': '',
                'vault_title': title,
                'vault_year': year,
            })
            print(f"  [{i+1}/{len(papers)}] {filename} — NO_DOI")
            continue
        
        # Verify this DOI
        result = verify_paper(doi, title, authors, year, session, delay=args.delay)
        result['filename'] = filename
        result['vault_year'] = year
        result['vault_authors'] = str(authors)[:100] if authors else ''
        results.append(result)
        
        verified_count += 1
        cls = result['classification']
        sim = result.get('title_similarity', 0)
        
        # Colour-coded output
        if cls == 'MISMATCH':
            marker = '❌'
        elif cls in ('UNCERTAIN', 'PUBMED_DOI_DIFFERS'):
            marker = '⚠️'
        elif cls in ('VERIFIED', 'PUBMED_VERIFIED'):
            marker = '✅'
        elif cls == 'ERROR':
            marker = '💥'
        else:
            marker = '🔍'
        
        print(f"  [{i+1}/{len(papers)}] {filename} — {marker} {cls} (sim={sim:.2f})")
        
        if args.limit and verified_count >= args.limit:
            print(f"\n  Reached limit ({args.limit}). Stopping.")
            # Add remaining as unverified
            break
    
    print(f"\n{'='*65}")
    print("Generating report...")
    generate_report(results, args.output, args.vault)
    
    # Summary
    counts = Counter(r['classification'] for r in results)
    print(f"\n{'='*65}")
    print("  VERIFICATION COMPLETE")
    print(f"{'='*65}")
    for cls in ['VERIFIED', 'PUBMED_VERIFIED', 'UNCERTAIN', 'MISMATCH',
                'PUBMED_DOI_DIFFERS', 'CR_NOT_FOUND', 'PUBMED_VERIFIED_NO_DOI',
                'NO_DOI', 'ERROR']:
        c = counts.get(cls, 0)
        if c > 0:
            print(f"  {cls:25s}: {c}")
    print(f"  {'TOTAL':25s}: {len(results)}")
    print(f"\n  Report: {args.output}")
    print(f"  JSON:   {args.output.replace('.md', '.json')}")
    
    # Exit code
    critical = counts.get('MISMATCH', 0) + counts.get('PUBMED_DOI_DIFFERS', 0)
    if critical > 0:
        print(f"\n  ⚠️  {critical} DOIs need correction!")
        sys.exit(1)
    else:
        print(f"\n  ✅  No critical mismatches found.")
        sys.exit(0)


if __name__ == '__main__':
    main()
