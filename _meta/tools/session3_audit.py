#!/usr/bin/env python3
"""
IbogaineVault Session 3: Machine-Readability and Metadata Validation
Run: python3 /Users/aretesofia/IbogaineVault/_meta/tools/session3_audit.py
Output: stdout (paste back into Claude chat)
"""

import json, csv, re, os, glob, random, sys
from collections import Counter
from pathlib import Path

TIER1 = Path('/Users/aretesofia/IbogaineVault-Tier1')
VAULT = Path('/Users/aretesofia/IbogaineVault')
JSON_PATH = TIER1 / 'papers.json'
CSV_PATH = TIER1 / 'papers.csv'
SCHEMA_PATH = VAULT / '_meta/schema_registry.yml'
GENINDEX_PATH = VAULT / '_meta/tools/generate_index.py'

random.seed(42)  # reproducible sampling

with open(JSON_PATH) as f:
    data = json.load(f)
papers = data['papers']

print("=" * 70)
print("SESSION 3 AUDIT — Machine-Readability and Metadata Validation")
print("=" * 70)

# ── STEP 1: Field Completeness ──
print(f"\n{'─'*70}")
print(f"STEP 1: FIELD COMPLETENESS")
print(f"{'─'*70}")
print(f"Total papers: {len(papers)}")
fields = set()
for p in papers:
    fields.update(p.keys())
print(f"Total fields: {len(fields)}\n")

for field in sorted(fields):
    populated = sum(1 for p in papers if p.get(field) not in [None, '', [], 0, False])
    pct = 100 * populated / len(papers)
    flag = " ⚠️  LOW" if pct < 50 else ""
    print(f'  {field}: {populated}/{len(papers)} ({pct:.0f}%){flag}')

# ── STEP 2: Enumerated Field Values ──
print(f"\n{'─'*70}")
print(f"STEP 2: ENUMERATED FIELD VALUES")
print(f"{'─'*70}")

# Schema enum values (hardcoded from schema_registry.yml to avoid YAML dep)
SCHEMA_ENUMS = {
    'evidence_level': ['rct','cohort','case-series','case-report','in-vitro',
        'preclinical','review','systematic-review','guideline','observational',
        'qualitative','journalism','primary-source'],
    'clinical_significance': ['low','moderate','high','landmark'],
    'primary_category': ['RED','GREEN','ORANGE','BLUE','PURPLE','WHITE'],
    'route': ['oral','intravenous','subcutaneous','intramuscular',
        'intraperitoneal','topical','not-specified','not-applicable'],
}

for field_name, valid_values in SCHEMA_ENUMS.items():
    values = [p.get(field_name) for p in papers if p.get(field_name)]
    counts = Counter(values)
    rogue = [v for v in counts if v not in valid_values]
    print(f"\n  === {field_name} (valid: {len(valid_values)}) ===")
    for val, count in counts.most_common():
        marker = " ❌ ROGUE" if val in rogue else ""
        print(f"    {val}: {count}{marker}")
    if rogue:
        print(f"  ⚠️  ROGUE VALUES: {rogue}")
    else:
        print(f"  ✅ All values match schema")

# Also check secondary_categories values
sec_vals = []
for p in papers:
    sc = p.get('secondary_categories')
    if sc and isinstance(sc, list):
        sec_vals.extend(sc)
sec_counts = Counter(sec_vals)
rogue_sec = [v for v in sec_counts if v not in SCHEMA_ENUMS['primary_category']]
print(f"\n  === secondary_categories (flattened) ===")
for val, count in sec_counts.most_common():
    marker = " ❌ ROGUE" if val in rogue_sec else ""
    print(f"    {val}: {count}{marker}")
if rogue_sec:
    print(f"  ⚠️  ROGUE VALUES: {rogue_sec}")
else:
    print(f"  ✅ All values match schema")

# ── STEP 3: Dosing Range Format ──
print(f"\n{'─'*70}")
print(f"STEP 3: DOSING RANGE FORMAT CONSISTENCY")
print(f"{'─'*70}")
dosing = [p.get('dosing_range') for p in papers if p.get('dosing_range')]
print(f"Populated: {len(dosing)}/{len(papers)}")
print(f"Unique values: {len(set(dosing))}")
# Check for common format inconsistencies
dash_types = Counter()
for d in dosing:
    if '–' in d: dash_types['en-dash (–)'] += 1
    if '-' in d and '–' not in d: dash_types['hyphen (-)'] += 1
    if '—' in d: dash_types['em-dash (—)'] += 1
print(f"Dash usage: {dict(dash_types)}")
# Check mg/kg formatting
mgkg = [d for d in dosing if 'mg/kg' in d]
mgkg_space = [d for d in dosing if 'mg /kg' in d or 'mg/ kg' in d]
print(f"Contains 'mg/kg': {len(mgkg)}")
print(f"Inconsistent spacing around mg/kg: {len(mgkg_space)}")
print(f"NOTE: dosing_range is free-text by schema design — heterogeneity expected")

# ── STEP 4: DOI Validation ──
print(f"\n{'─'*70}")
print(f"STEP 4: DOI VALIDATION")
print(f"{'─'*70}")
doi_pattern = re.compile(r'^10\.\d{4,}/.+$')
dois = [(p.get('filepath', 'unknown'), p.get('doi')) for p in papers]
invalid = []
for fname, doi in dois:
    if doi and not doi_pattern.match(str(doi)):
        invalid.append((fname, doi))
missing = sum(1 for _, doi in dois if not doi)
url_prefix = [(f, d) for f, d in dois if d and ('http' in str(d) or 'doi.org' in str(d))]
print(f"DOIs present: {len(dois) - missing}/{len(papers)}")
print(f"DOIs missing: {missing}")
print(f"Invalid DOI format: {len(invalid)}")
for fname, doi in invalid:
    print(f"  ❌ {fname}: {doi}")
print(f"DOIs with URL prefix (should be bare): {len(url_prefix)}")
for fname, doi in url_prefix:
    print(f"  ❌ {fname}: {doi}")
if not invalid and not url_prefix:
    print(f"  ✅ All DOIs are valid bare identifiers")

# ── STEP 5: CSV Integrity ──
print(f"\n{'─'*70}")
print(f"STEP 5: CSV INTEGRITY")
print(f"{'─'*70}")
try:
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for BOM
    has_bom = content.startswith('\ufeff')
    print(f"BOM detected: {has_bom}")
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(f"CSV columns: {len(header)}")
        print(f"Headers: {header}")
        errors = []
        row_count = 0
        for i, row in enumerate(reader, start=2):
            row_count += 1
            if len(row) != len(header):
                errors.append(f"Row {i}: {len(row)} cols (expected {len(header)})")
        print(f"Data rows: {row_count}")
        print(f"JSON papers: {len(papers)}")
        print(f"Row count match: {'✅' if row_count == len(papers) else '❌ MISMATCH'}")
        print(f"Column count errors: {len(errors)}")
        for e in errors[:10]:
            print(f"  ❌ {e}")
        if not errors:
            print(f"  ✅ All rows have correct column count")
except Exception as e:
    print(f"  ❌ CSV read error: {e}")

# ── STEP 6: JSON ↔ YAML Consistency ──
print(f"\n{'─'*70}")
print(f"STEP 6: JSON ↔ YAML CONSISTENCY (sampled)")
print(f"{'─'*70}")

# Get mortality papers for priority sampling
mortality_papers = [p for p in papers if p.get('mortality_count') and p['mortality_count'] > 0]
other_papers = [p for p in papers if not p.get('mortality_count') or p['mortality_count'] == 0]

# Sample: 3 mortality + 5 random others
sample_mort = random.sample(mortality_papers, min(3, len(mortality_papers)))
sample_other = random.sample(other_papers, min(5, len(other_papers)))
sample = sample_mort + sample_other

import re as re_mod

def extract_yaml_frontmatter(md_path):
    """Extract YAML frontmatter from a markdown file."""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Match YAML frontmatter between --- markers
        match = re_mod.match(r'^---\s*\n(.*?)\n---', content, re_mod.DOTALL)
        if not match:
            return None
        yaml_text = match.group(1)
        # Simple YAML parsing for key fields (avoid yaml dependency)
        result = {}
        for line in yaml_text.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('-') and not line.startswith('#'):
                key, _, val = line.partition(':')
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if val.lower() == 'true': val = True
                elif val.lower() == 'false': val = False
                elif val.lower() == 'null' or val == '': val = None
                else:
                    try: val = int(val)
                    except: pass
                result[key] = val
        return result
    except Exception as e:
        return {'_error': str(e)}

CHECK_FIELDS = ['primary_category', 'evidence_level', 'mortality_count',
                'sample_size', 'qtc_data', 'herg_data', 'electrolyte_data',
                'clinical_significance']

mismatches = []
for p in sample:
    fp = p.get('filepath', '')
    # Try Tier1 first, then working vault
    md_path = TIER1 / fp
    if not md_path.exists():
        md_path = VAULT / fp
    
    is_mort = "MORTALITY" if p.get('mortality_count') and p['mortality_count'] > 0 else ""
    print(f"\n  --- {fp} {is_mort} ---")
    
    yaml_data = extract_yaml_frontmatter(md_path)
    if yaml_data is None:
        print(f"    ❌ Could not parse YAML frontmatter")
        mismatches.append(fp)
        continue
    if '_error' in yaml_data:
        print(f"    ❌ Error reading file: {yaml_data['_error']}")
        mismatches.append(fp)
        continue
    
    # Map YAML 'category' to JSON 'primary_category'
    yaml_field_map = {'primary_category': 'category'}
    
    paper_ok = True
    for field in CHECK_FIELDS:
        json_val = p.get(field)
        yaml_key = yaml_field_map.get(field, field)
        yaml_val = yaml_data.get(yaml_key)
        match = (json_val == yaml_val)
        # Handle None vs absent
        if json_val is None and yaml_val is None:
            match = True
        status = "✅" if match else "❌ MISMATCH"
        if not match:
            paper_ok = False
            print(f"    {status} {field}: JSON={json_val} YAML={yaml_val}")
    if paper_ok:
        print(f"    ✅ All checked fields match")
    else:
        mismatches.append(fp)

print(f"\n  Total sampled: {len(sample)} (mortality: {len(sample_mort)}, other: {len(sample_other)})")
print(f"  Mismatches found: {len(mismatches)}")

# ── STEP 7: Negative Space — Files vs Index ──
print(f"\n{'─'*70}")
print(f"STEP 7: NEGATIVE SPACE — FILES vs INDEX")
print(f"{'─'*70}")

# Find all .md files in paper directories
paper_dirs = ['1957','1958','1960','1962','1963','1965','1966','1967','1968','1969',
    '1970','1971','1972','1973','1974','1975','1976','1977','1978','1979',
    '1980','1981','1982','1983','1984','1985','1986','1987','1988','1989',
    '1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
    '2000','2001','2002','2003','2004','2005','2006','2007','2008','2009',
    '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019',
    '2020','2021','2022','2023','2024','2025','2026',
    'Clinical_Guidelines','Industry_Documents','Primary_Sources','Other']

fs_files = set()
for d in paper_dirs:
    dirpath = TIER1 / d
    if dirpath.exists():
        for md in dirpath.glob('*.md'):
            rel = str(md.relative_to(TIER1))
            fs_files.add(rel)

json_files = set(p.get('filepath', '') for p in papers)

in_fs_not_json = fs_files - json_files
in_json_not_fs = json_files - fs_files

print(f"Markdown files on filesystem: {len(fs_files)}")
print(f"Papers in JSON index: {len(json_files)}")
if in_fs_not_json:
    print(f"⚠️  In filesystem but NOT in JSON ({len(in_fs_not_json)}):")
    for f in sorted(in_fs_not_json):
        print(f"  {f}")
else:
    print(f"✅ No orphan files on filesystem")

if in_json_not_fs:
    print(f"❌ In JSON but NOT on filesystem ({len(in_json_not_fs)}):")
    for f in sorted(in_json_not_fs):
        print(f"  {f}")
else:
    print(f"✅ No phantom entries in JSON")

# ── STEP 8: Boolean Field Sanity ──
print(f"\n{'─'*70}")
print(f"STEP 8: BOOLEAN FIELD SANITY")
print(f"{'─'*70}")

for flag in ['qtc_data', 'herg_data', 'electrolyte_data']:
    true_count = sum(1 for p in papers if p.get(flag) is True)
    false_count = sum(1 for p in papers if p.get(flag) is False)
    null_count = sum(1 for p in papers if p.get(flag) is None)
    total = true_count + false_count + null_count
    print(f"  {flag}: true={true_count}, false={false_count}, null={null_count}, sum={total}")

# Cross-check: RED papers should not have null boolean flags
print(f"\n  RED papers with null boolean flags:")
red_papers = [p for p in papers if p.get('primary_category') == 'RED']
red_null_issues = []
for p in red_papers:
    nulls = [f for f in ['qtc_data','herg_data','electrolyte_data'] if p.get(f) is None]
    if nulls:
        red_null_issues.append((p.get('filepath','?'), nulls))
        print(f"    ⚠️  {p.get('filepath','?')}: null on {nulls}")
if not red_null_issues:
    print(f"    ✅ All RED papers have explicit boolean values")

# ── STEP 9: generate_index.py Field Count ──
print(f"\n{'─'*70}")
print(f"STEP 9: generate_index.py FIELD CROSS-CHECK")
print(f"{'─'*70}")

# Read generate_index.py and look for field definitions
try:
    with open(GENINDEX_PATH, 'r') as f:
        genindex_src = f.read()
    # Look for the fields being extracted — typically in a dict comprehension or explicit list
    # Print lines containing field names for manual verification
    print(f"  Source: {GENINDEX_PATH}")
    print(f"  JSON actual fields ({len(fields)}): {sorted(fields)}")
    print(f"\n  Key lines from generate_index.py referencing fields:")
    for i, line in enumerate(genindex_src.split('\n'), 1):
        # Show lines that assign to paper dict or mention field names
        if any(f'"{f}"' in line or f"'{f}'" in line for f in ['key_findings','filepath','mortality_count','sample_size']):
            print(f"    L{i}: {line.rstrip()}")
    # Check that key_findings and filepath (Session 1 additions) are present
    has_key_findings = 'key_findings' in genindex_src
    has_filepath = 'filepath' in genindex_src
    print(f"\n  Session 1 additions present in generator:")
    print(f"    key_findings: {'✅' if has_key_findings else '❌ MISSING'}")
    print(f"    filepath: {'✅' if has_filepath else '❌ MISSING'}")
    # Verify all 23 fields are populated in actual JSON
    print(f"\n  All 23 fields present in papers.json: {'✅' if len(fields) == 23 else '❌ Got ' + str(len(fields))}")
except Exception as e:
    print(f"  ❌ Error reading generate_index.py: {e}")

# ── BONUS: Anomalous Values for Session 2 Handoff ──
print(f"\n{'─'*70}")
print(f"SESSION 2 HANDOFF — Priority Targets")
print(f"{'─'*70}")

# High mortality counts
print(f"\n  Papers with mortality_count > 10 (verify in Session 2):")
high_mort = [(p.get('filepath','?'), p.get('mortality_count'), p.get('evidence_level'))
             for p in papers if p.get('mortality_count') and p['mortality_count'] > 10]
for fp, mc, el in sorted(high_mort, key=lambda x: -x[1]):
    print(f"    {fp}: mortality_count={mc}, evidence_level={el}")

# Dosing ranges that look anomalous (>50 mg/kg for human oral)
print(f"\n  Papers with 'landmark' clinical_significance (verify in Session 2):")
landmarks = [(p.get('filepath','?'), p.get('title','?')[:60]) for p in papers
             if p.get('clinical_significance') == 'landmark']
for fp, title in landmarks:
    print(f"    {fp}: {title}")

# RED papers with qtc_data=false (potential misconfiguration)
print(f"\n  RED cardiac papers with qtc_data=false (verify in Session 2):")
red_no_qtc = [(p.get('filepath','?'), p.get('title','?')[:60])
              for p in papers
              if p.get('primary_category') == 'RED' and p.get('qtc_data') is False]
for fp, title in red_no_qtc:
    print(f"    {fp}: {title}")
print(f"  Count: {len(red_no_qtc)}")

# JSON↔YAML mismatches from Step 6
if mismatches:
    print(f"\n  JSON↔YAML mismatches from Step 6 sampling:")
    for m in mismatches:
        print(f"    {m}")

# ── SUMMARY ──
print(f"\n{'='*70}")
print(f"SUMMARY")
print(f"{'='*70}")
print(f"Papers: {len(papers)}")
print(f"Fields: {len(fields)}")
print(f"100% populated: {sum(1 for f in fields if all(p.get(f) not in [None,'',[], 0, False] for p in papers))}")
print(f"Enum violations: {sum(1 for f,v in SCHEMA_ENUMS.items() for p in papers if p.get(f) and p.get(f) not in v)}")
print(f"Invalid DOIs: {len(invalid)}")
print(f"CSV row errors: {len(errors) if 'errors' in dir() else 'N/A'}")
print(f"JSON↔YAML mismatches (sampled): {len(mismatches)}/{len(sample)}")
print(f"Orphan files: {len(in_fs_not_json)}")
print(f"Phantom JSON entries: {len(in_json_not_fs)}")
print(f"RED papers with null booleans: {len(red_null_issues)}")
print(f"\n{'='*70}")
print(f"END OF SESSION 3 AUDIT")
print(f"{'='*70}")
