#!/usr/bin/env python3
"""
truncate_red_papers.py — Phase 0C: RED Paper Truncation for IbogaineVault Tier 1

Reads the definitive RED list from doi_oa_report_v2.json, classifies each as
either "publisher-mirror" (full paper text) or "vault-template" (already an
analytical summary), and truncates only the publisher-mirror papers.

CLASSIFICATION SIGNALS (publisher-mirror):
  - Has a ## or ### References section
  - High density of numbered (1,2,3) or author-date citations
  - Publisher-style section headers (Introduction, Methods, Results, Discussion)
  - Zero vault-signature sections (Clinical Implications, Limitations, Key Findings)

RETAINED in truncated version:
  - Complete YAML frontmatter (unchanged)
  - Title + citation line
  - Copyright notice callout
  - Abstract section
  - Factual data tables (markdown tables found in body)
  - key_findings from YAML (as Vault Commentary seed)
  - See Also / wikilinks section

STRIPPED:
  - Introduction, Methods, Results, Discussion, Conclusion
  - References section
  - Author affiliations and article history
  - Figure descriptions without data

Legal basis:
  - Abstracts: standard scholarly indexing practice (PubMed/Scholar precedent)
  - Data tables: Feist v. Rural (1991) — factual data not copyrightable;
    tables reconstructed in vault's own format
  - key_findings: original vault analytical commentary (17 U.S.C. §107)
  - See Also: vault's own navigational infrastructure

Usage:
  python3 truncate_red_papers.py --preview          # Write to preview directory
  python3 truncate_red_papers.py --apply             # Overwrite vault files
  python3 truncate_red_papers.py --stats             # Classification stats only
  python3 truncate_red_papers.py --preview --sample 5  # Preview first 5 only
"""

import json, os, sys, re, argparse, textwrap
from pathlib import Path
from datetime import datetime

# ── Configuration ────────────────────────────────────────────────────────────

VAULT_ROOT = Path('/Users/aretesofia/IbogaineVault')
OA_REPORT = VAULT_ROOT / '_meta/tools/doi_oa_report_v2.json'
PREVIEW_DIR = VAULT_ROOT / '_meta/tools/truncated_preview'

# Publisher display names (normalise CrossRef variations)
PUBLISHER_MAP = {
    'Elsevier BV': 'Elsevier',
    'Wiley': 'Wiley',
    'Springer Science and Business Media LLC': 'Springer Nature',
    'Springer Nature': 'Springer Nature',
    'Informa UK Limited': 'Taylor & Francis',
    'SAGE Publications': 'SAGE Publications',
    'American Chemical Society (ACS)': 'American Chemical Society',
    'Ovid Technologies (Wolters Kluwer Health)': 'Wolters Kluwer',
    'Oxford University Press (OUP)': 'Oxford University Press',
}

# Vault-signature section names (Philip's analytical framework)
VAULT_SECTIONS = {
    'clinical implications', 'limitations', 'key findings',
    'vault commentary', 'cardiac safety data', 'mechanistic discussion',
    'receptor binding data', 'toxicological data', 'pharmacokinetic significance',
    'animal toxicity data', 'fatality data', 'dopamine modulation',
    'cerebellar toxicity dissociation', 'pharmacological context',
    'psychiatric adverse event data', 'mechanism of block', 'toxicity implications',
    'herg blockade data', 'circumstances of death', 'autopsy and histopathology',
    'cardiac safety context', 'detailed fatality analysis', 'pharmacokinetic highlights',
    'contraindications identified', 'policy context', 'case report',
}


# ── Parsing helpers ──────────────────────────────────────────────────────────

def parse_yaml_frontmatter(content: str) -> tuple[str, str]:
    """Split file into YAML frontmatter and body. Returns (yaml_block, body)."""
    if not content.startswith('---'):
        return '', content
    end = content.find('\n---', 3)
    if end == -1:
        return '', content
    # Include both --- delimiters
    yaml_block = content[:end + 4]  # up to and including closing ---
    body = content[end + 4:].lstrip('\n')
    return yaml_block, body


def extract_yaml_field(yaml_block: str, field: str) -> str:
    """Extract a simple scalar field from YAML frontmatter."""
    m = re.search(rf'^{field}:\s*"?(.+?)"?\s*$', yaml_block, re.M)
    return m.group(1).strip('"').strip("'") if m else ''


def extract_yaml_key_findings(yaml_block: str) -> str:
    """Extract key_findings field, handling multi-line quoted strings."""
    m = re.search(r'^key_findings:\s*"(.+?)"', yaml_block, re.M | re.S)
    if m:
        return m.group(1).strip()
    m = re.search(r"^key_findings:\s*'(.+?)'", yaml_block, re.M | re.S)
    if m:
        return m.group(1).strip()
    m = re.search(r'^key_findings:\s*(.+)$', yaml_block, re.M)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return ''


def find_sections(body: str) -> list[dict]:
    """Find all H2 and H3 sections with their line positions and content."""
    lines = body.split('\n')
    sections = []
    for i, line in enumerate(lines):
        m = re.match(r'^(#{2,3})\s+(.+)', line)
        if m:
            sections.append({
                'level': len(m.group(1)),
                'title': m.group(2).strip(),
                'title_lower': m.group(2).strip().lower(),
                'line_idx': i,
            })
    # Add end positions
    for j, sec in enumerate(sections):
        if j + 1 < len(sections):
            sec['end_idx'] = sections[j + 1]['line_idx']
        else:
            sec['end_idx'] = len(lines)
    return sections


def extract_section_content(body: str, sections: list[dict], title_lower: str) -> str:
    """Extract the full content of a section by its lowercased title."""
    lines = body.split('\n')
    for sec in sections:
        if sec['title_lower'] == title_lower:
            return '\n'.join(lines[sec['line_idx']:sec['end_idx']]).strip()
    # Try partial match
    for sec in sections:
        if title_lower in sec['title_lower']:
            return '\n'.join(lines[sec['line_idx']:sec['end_idx']]).strip()
    return ''


def extract_markdown_tables(body: str) -> list[str]:
    """Extract all markdown tables from body text.
    
    A table is a block of lines where each line starts with |.
    Also captures the line immediately before the table block if it looks
    like a table caption/header.
    """
    lines = body.split('\n')
    tables = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('|'):
            # Found start of a table — collect all contiguous | lines
            start = i
            while i < len(lines) and lines[i].strip().startswith('|'):
                i += 1
            table_lines = lines[start:i]
            
            # Check if line before table is a caption
            caption = ''
            if start > 0:
                prev = lines[start - 1].strip()
                if prev and not prev.startswith('#') and not prev.startswith('|'):
                    # Could be a table caption like "**Table 1: ...**"
                    if prev.startswith('**') or prev.startswith('*') or 'table' in prev.lower():
                        caption = prev
            
            table_text = '\n'.join(table_lines)
            if caption:
                table_text = caption + '\n' + table_text
            
            # Only keep tables with at least 2 data rows (header + separator + 1+ data)
            data_rows = [l for l in table_lines if l.strip().startswith('|') 
                         and not re.match(r'^\|[\s\-:]+\|', l.strip())]
            if len(data_rows) >= 2:
                tables.append(table_text)
        else:
            i += 1
    return tables


# ── Classification ───────────────────────────────────────────────────────────

def classify_paper(content: str) -> str:
    """Classify a RED paper as 'publisher-mirror' or 'vault-template'.
    
    Returns: 'publisher-mirror' | 'vault-template'
    """
    # Signal 1: References section (strongest signal — no vault-template has one)
    has_refs = bool(re.search(r'^#{2,3}\s+References', content, re.M | re.I))
    
    # Signal 2: Numbered citations like (1), (1,2), (1-3), (1–3)
    num_cites = len(re.findall(r'\(\d+(?:[,–\-]\d+)*\)', content))
    
    # Signal 3: Author-date citations like (Alper 2001)
    auth_cites = len(re.findall(
        r'\([A-Z][a-z]+(?:\s+et\s+al\.?)?,?\s+\d{4}\)', content))
    
    # Signal 4: Publisher-style section headers
    pub_headers = 0
    for pat in ['Introduction', 'Methods', 'Results', 'Discussion',
                'Conclusion', 'Acknowledgment', 'Funding', 'Disclosure']:
        if re.search(r'^#{2,3}\s+(?:\d+\.?\s+)?' + pat, content, re.M | re.I):
            pub_headers += 1
    
    # Signal 5: Vault-signature sections
    vault_sigs = 0
    body_lower = content.lower()
    for vs in VAULT_SECTIONS:
        if re.search(r'^#{2,3}\s+' + re.escape(vs), body_lower, re.M):
            vault_sigs += 1
    
    # Decision logic — conservative: only truncate when confident
    publisher_score = (
        (3 if has_refs else 0) +          # References section is strongest signal
        (2 if num_cites > 10 else 0) +
        (1 if auth_cites > 5 else 0) +
        (1 if pub_headers >= 3 else 0)
    )
    vault_score = (
        (3 if vault_sigs >= 2 else 0) +
        (1 if num_cites < 5 else 0)
    )
    
    if publisher_score >= 3 and vault_score < 3:
        return 'publisher-mirror'
    else:
        return 'vault-template'


# ── Truncation ───────────────────────────────────────────────────────────────

def build_truncated_version(content: str, paper_info: dict) -> str:
    """Build a truncated version of a publisher-mirror paper.
    
    Retains: YAML, title, abstract, data tables, key_findings, See Also.
    Strips: Introduction, Methods, Results, Discussion, References, etc.
    """
    yaml_block, body = parse_yaml_frontmatter(content)
    
    # Extract fields from YAML
    title = extract_yaml_field(yaml_block, 'title')
    doi = extract_yaml_field(yaml_block, 'doi')
    key_findings = extract_yaml_key_findings(yaml_block)
    publisher_raw = paper_info.get('publisher', 'the original publisher')
    publisher = PUBLISHER_MAP.get(publisher_raw, publisher_raw)
    
    # Find sections in body
    sections = find_sections(body)
    
    # Extract abstract — conservative: stop at horizontal rules, citation lines,
    # keywords, or next heading. Prevents introduction text bleed-through.
    abstract = ''
    for sec in sections:
        if 'abstract' in sec['title_lower']:
            lines = body.split('\n')
            abstract_lines = []
            for j in range(sec['line_idx'] + 1, sec['end_idx']):
                line = lines[j]
                stripped = line.strip()
                # Stop conditions — these mark the end of the abstract
                if stripped == '---':
                    break
                if stripped.lower().startswith('**citation'):
                    break
                if re.match(r'^\*\*key\s*words?', stripped, re.I):
                    break
                if re.match(r'^key\s*words?:', stripped, re.I):
                    break
                # Stop at lines that look like author affiliations
                if re.match(r'^\*?\*?\s*\(?[a-z]\)?\s*[A-Z].*(?:University|Institute|Department|Hospital)', stripped):
                    break
                abstract_lines.append(line)
            abstract = '\n'.join(abstract_lines).strip()
            # Final cleanup: strip trailing keywords if any slipped through
            abstract = re.sub(
                r'\n\*\*Keywords?:\*\*.*$', '', abstract, flags=re.I | re.S
            ).strip()
            break
    
    if not abstract:
        # Fallback: find abstract as first paragraph after title
        lines = body.split('\n')
        for i, line in enumerate(lines):
            if line.strip().lower().startswith('abstract'):
                abstract_lines = []
                for j in range(i + 1, min(i + 30, len(lines))):
                    if re.match(r'^#{2,3}\s', lines[j]) or lines[j].strip() == '---':
                        break
                    abstract_lines.append(lines[j])
                abstract = '\n'.join(abstract_lines).strip()
                break
    
    # Extract See Also section
    see_also = ''
    for sec in sections:
        if 'see also' in sec['title_lower']:
            lines = body.split('\n')
            see_also_lines = lines[sec['line_idx']:sec['end_idx']]
            see_also = '\n'.join(see_also_lines).strip()
            break
    
    # Extract all data tables from the full body
    tables = extract_markdown_tables(body)
    
    # Build truncated version
    parts = [yaml_block, '']
    
    # Title
    parts.append(f'# {title}')
    parts.append('')
    
    # Copyright callout
    doi_link = f'https://doi.org/{doi}' if doi else '[DOI not available]'
    callout = textwrap.dedent(f"""\
        > [!info] Copyright Notice
        > This paper is published by {publisher} and is not available under an open access licence. The full text is retained in the working vault for clinical reference but is excluded from the public Tier 1 distribution. This entry contains: bibliographic metadata, the original abstract, analytical commentary, reconstructed factual data tables, and cross-references.
        >
        > Full publication: [{doi}]({doi_link})""")
    parts.append(callout)
    parts.append('')
    # Abstract
    if abstract:
        parts.append('## Abstract')
        parts.append('')
        parts.append(abstract)
        parts.append('')
    
    # Data tables
    if tables:
        parts.append('## Key Data')
        parts.append('')
        parts.append('*Factual data reconstructed in the vault\'s standardised format. Per* Feist v. Rural Telephone Co. *(1991), factual data compilations are not copyrightable; only creative arrangement is protected.*')
        parts.append('')
        for table in tables:
            parts.append(table)
            parts.append('')
    
    # Vault commentary from key_findings
    if key_findings:
        parts.append('## Vault Commentary')
        parts.append('')
        parts.append(key_findings)
        parts.append('')
    
    # See Also
    if see_also:
        parts.append('')
        parts.append(see_also)
    
    return '\n'.join(parts).rstrip() + '\n'


# ── Main ─────────────────────────────────────────────────────────────────────

def load_red_papers() -> list[dict]:
    """Load RED paper list from OA report JSON."""
    with open(OA_REPORT) as f:
        data = json.load(f)
    return [p for p in data if p['tier'] == 'RED']


def main():
    parser = argparse.ArgumentParser(
        description='Truncate RED publisher-mirror papers for Tier 1 distribution')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--preview', action='store_true',
                       help='Write truncated versions to preview directory')
    group.add_argument('--apply', action='store_true',
                       help='Overwrite vault files with truncated versions')
    group.add_argument('--stats', action='store_true',
                       help='Show classification statistics only')
    parser.add_argument('--sample', type=int, default=0,
                        help='Process only first N publisher-mirror papers')
    parser.add_argument('--verbose', action='store_true',
                        help='Show detailed classification reasoning')
    args = parser.parse_args()
    
    red_papers = load_red_papers()
    print(f"Loaded {len(red_papers)} RED papers from OA report\n")
    
    # Classify all papers
    classifications = {
        'publisher-mirror': [],
        'vault-template': [],
        'missing': [],
    }
    
    for paper in red_papers:
        fpath = VAULT_ROOT / paper['filename']
        if not fpath.exists():
            classifications['missing'].append(paper)
            continue
        
        content = fpath.read_text()
        cls = classify_paper(content)
        paper['_classification'] = cls
        paper['_total_lines'] = len(content.split('\n'))
        classifications[cls].append(paper)
    
    # Report classification
    print("=" * 70)
    print("CLASSIFICATION RESULTS")
    print("=" * 70)
    pm = classifications['publisher-mirror']
    vt = classifications['vault-template']
    ms = classifications['missing']
    print(f"  Publisher-mirror (need truncation):    {len(pm)}")
    print(f"  Vault-template (already compliant):    {len(vt)}")
    if ms:
        print(f"  Missing files:                         {len(ms)}")
    print()
    if args.verbose or args.stats:
        print("Publisher-mirror papers (will truncate):")
        for p in sorted(pm, key=lambda x: -x['_total_lines']):
            pub = PUBLISHER_MAP.get(p.get('publisher',''), p.get('publisher',''))
            print(f"  {p['_total_lines']:>4} lines | {pub:<25} | {p['filename']}")
        
        print(f"\nVault-template papers (skip — already compliant):")
        for p in sorted(vt, key=lambda x: -x['_total_lines']):
            print(f"  {p['_total_lines']:>4} lines | {p['filename']}")
    
    if args.stats:
        return
    
    # Process publisher-mirror papers
    to_process = pm
    if args.sample > 0:
        to_process = pm[:args.sample]
        print(f"Processing sample of {args.sample} papers\n")
    
    if args.preview:
        PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    
    results = {
        'truncated': [],
        'errors': [],
        'tables_found': [],
    }
    
    for paper in to_process:
        fpath = VAULT_ROOT / paper['filename']
        content = fpath.read_text()
        original_lines = len(content.split('\n'))
        
        try:
            truncated = build_truncated_version(content, paper)
            new_lines = len(truncated.split('\n'))
            
            # Count tables extracted
            tables = extract_markdown_tables(content)
            
            if args.preview:
                # Write to preview dir, preserving year subdirectory
                out_path = PREVIEW_DIR / paper['filename']
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(truncated)
                action = f"preview → {out_path.relative_to(VAULT_ROOT)}"
            elif args.apply:
                fpath.write_text(truncated)
                action = "APPLIED"
            
            reduction = ((original_lines - new_lines) / original_lines * 100)
            print(f"  ✓ {paper['filename']}")
            print(f"    {original_lines} → {new_lines} lines "
                  f"({reduction:.0f}% reduction) | "
                  f"{len(tables)} tables | {action}")
            
            results['truncated'].append({
                'filename': paper['filename'],
                'original_lines': original_lines,
                'new_lines': new_lines,
                'tables_extracted': len(tables),
                'publisher': paper.get('publisher', ''),
            })
            if tables:
                results['tables_found'].append(paper['filename'])
        except Exception as e:
            print(f"  ✗ ERROR: {paper['filename']}: {e}")
            results['errors'].append({
                'filename': paper['filename'],
                'error': str(e),
            })
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"  Total RED papers:              {len(red_papers)}")
    print(f"  Publisher-mirror (truncated):   {len(results['truncated'])}")
    print(f"  Vault-template (skipped):       {len(vt)}")
    print(f"  Errors:                         {len(results['errors'])}")
    if results['tables_found']:
        print(f"  Papers with data tables:        {len(results['tables_found'])}")
        for f in results['tables_found']:
            print(f"    → {f}")
    
    if results['truncated']:
        total_orig = sum(r['original_lines'] for r in results['truncated'])
        total_new = sum(r['new_lines'] for r in results['truncated'])
        print(f"\n  Total lines: {total_orig} → {total_new} "
              f"({(total_orig-total_new)/total_orig*100:.0f}% reduction)")
    
    # Write report
    if args.preview or args.apply:
        report_path = VAULT_ROOT / '_meta/tools/truncation_report.md'
        mode_str = 'PREVIEW' if args.preview else 'APPLIED'
        with open(report_path, 'w') as f:
            f.write(f"# RED Paper Truncation Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"**Mode:** {mode_str}\n")
            f.write(f"**Total RED papers:** {len(red_papers)}\n\n")
            f.write(f"## Classification\n\n")
            f.write(f"| Category | Count |\n|----------|-------|\n")
            f.write(f"| Publisher-mirror (truncated) | {len(pm)} |\n")
            f.write(f"| Vault-template (already compliant) | {len(vt)} |\n")
            f.write(f"| Missing | {len(ms)} |\n\n")
            
            f.write(f"## Truncated Papers\n\n")
            f.write(f"| File | Original | Truncated | Reduction | Tables |\n")
            f.write(f"|------|----------|-----------|-----------|--------|\n")
            for r in results['truncated']:
                red_pct = (r['original_lines']-r['new_lines'])/r['original_lines']*100
                f.write(f"| {r['filename']} | {r['original_lines']} | "
                        f"{r['new_lines']} | {red_pct:.0f}% | "
                        f"{r['tables_extracted']} |\n")
            
            f.write(f"\n## Vault-Template Papers (Skipped)\n\n")
            f.write("These papers are already analytical summaries with ")
            f.write("vault-signature sections. No truncation needed.\n\n")
            for p in sorted(vt, key=lambda x: x['filename']):
                f.write(f"- {p['filename']} ({p['_total_lines']} lines)\n")
            
            if results['errors']:
                f.write(f"\n## Errors\n\n")
                for e in results['errors']:
                    f.write(f"- {e['filename']}: {e['error']}\n")
        
        print(f"\n  Report: {report_path.relative_to(VAULT_ROOT)}")
    
    if args.preview:
        print(f"\n  Preview files written to: {PREVIEW_DIR.relative_to(VAULT_ROOT)}/")
        print(f"  Review these before running with --apply")


if __name__ == '__main__':
    main()
