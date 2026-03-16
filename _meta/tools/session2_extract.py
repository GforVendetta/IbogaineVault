#!/usr/bin/env python3
"""
IbogaineVault Session 2: Content Fidelity — Preparatory Extraction
Run: python3 /Users/aretesofia/IbogaineVault/_meta/tools/session2_extract.py
Output: stdout (paste into Claude conversation)

Extracts stratified sample of 15 papers with YAML + body preview
for manual content fidelity evaluation.
"""

import json, re, random
from pathlib import Path

TIER1 = Path('/Users/aretesofia/IbogaineVault-Tier1')
JSON_PATH = TIER1 / 'papers.json'

random.seed(42)

with open(JSON_PATH) as f:
    data = json.load(f)
papers = data['papers']

# Build lookup
by_filepath = {p['filepath']: p for p in papers}

# ── STRATUM 1: High-mortality papers (3) ──
mortality_targets = [
    '2024/Chen2024_RIVM_Iboga_Risk_Assessment.md',
    '2018/Corkery2018_Ibogaine_Benefits_Dangers_Fatalities.md',
    '2012/Alper2012_Ibogaine_Fatalities.md',
]
stratum1 = [by_filepath[fp] for fp in mortality_targets if fp in by_filepath]

# ── STRATUM 2: RED papers with qtc_data=false (3) ──
# Priority: hERG in-vitro + one fatality case report
red_qtc_targets = [
    '2012/Koenig2012_Ibogaine_hERG_Cardiac_Arrhythmia_Risk.md',
    '2014/Thurner2014_hERG_Channel_Block_Ibogaine.md',
    '2002/Marker2002_Ibogaine_Related_Fatality.md',
]
stratum2 = [by_filepath[fp] for fp in red_qtc_targets if fp in by_filepath]

# ── STRATUM 3: Landmark papers (3) ──
landmark_targets = [
    '2024/Cherian2024_Magnesium_Ibogaine_TBI.md',
    '2014/Schenberg2014_Treating_Drug_Dependence_Retrospective_Study.md',
    '2018/Brown2018_OUD_Detoxification_Outcomes.md',
]
stratum3 = [by_filepath[fp] for fp in landmark_targets if fp in by_filepath]

# ── STRATUM 4: One random paper from each category (6) ──
used_fps = set(mortality_targets + red_qtc_targets + landmark_targets)
stratum4 = []
for cat in ['RED', 'GREEN', 'ORANGE', 'BLUE', 'PURPLE', 'WHITE']:
    pool = [p for p in papers
            if p['primary_category'] == cat and p['filepath'] not in used_fps]
    if pool:
        stratum4.append(random.choice(pool))

all_samples = (
    [(p, "Stratum 1: Mortality") for p in stratum1] +
    [(p, "Stratum 2: RED/qtc_false") for p in stratum2] +
    [(p, "Stratum 3: Landmark") for p in stratum3] +
    [(p, "Stratum 4: Category coverage") for p in stratum4]
)

print("=" * 70)
print(f"SESSION 2 EXTRACTION — {len(all_samples)} papers")
print("=" * 70)

for i, (paper, stratum) in enumerate(all_samples, 1):
    fp = paper['filepath']
    md_path = TIER1 / fp
    
    print(f"\n{'━' * 70}")
    print(f"PAPER {i}/{len(all_samples)} — [{stratum}]")
    print(f"File: {fp}")
    print(f"{'━' * 70}")
    
    # Print key JSON fields
    print(f"\n── JSON METADATA ──")
    for field in ['title', 'primary_category', 'secondary_categories',
                  'evidence_level', 'clinical_significance', 'key_findings',
                  'mortality_count', 'sample_size', 'qtc_data', 'herg_data',
                  'electrolyte_data', 'dosing_range', 'route', 'tags']:
        val = paper.get(field)
        print(f"  {field}: {val}")
    
    # Read and extract from markdown file
    if md_path.exists():
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split YAML frontmatter from body
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if match:
            yaml_text = match.group(1)
            body = match.group(2)
            
            print(f"\n── YAML FRONTMATTER ──")
            print(yaml_text)
            
            print(f"\n── BODY PREVIEW (first ~2500 chars) ──")
            preview = body[:2500]
            if len(body) > 2500:
                preview += f"\n\n[... TRUNCATED — {len(body)} total chars ...]"
            print(preview)
            
            # Extract wikilinks for spot-checking
            wikilinks = re.findall(r'\[\[([^\]]+)\]\]', body)
            if wikilinks:
                sample_links = wikilinks[:5]
                print(f"\n── WIKILINKS (first 5 of {len(wikilinks)}) ──")
                for wl in sample_links:
                    print(f"  [[{wl}]]")
        else:
            print(f"\n  ⚠️ Could not parse frontmatter/body split")
    else:
        print(f"\n  ❌ File not found: {md_path}")

print(f"\n{'=' * 70}")
print(f"EXTRACTION COMPLETE")
print(f"{'=' * 70}")
print(f"Total papers extracted: {len(all_samples)}")
print(f"  Stratum 1 (Mortality): {len(stratum1)}")
print(f"  Stratum 2 (RED/qtc_false): {len(stratum2)}")
print(f"  Stratum 3 (Landmark): {len(stratum3)}")
print(f"  Stratum 4 (Category coverage): {len(stratum4)}")
cats = [p['primary_category'] for p, _ in all_samples]
print(f"  Categories represented: {sorted(set(cats))}")
print(f"\nPaste this entire output into the Session 2 conversation.")
print(f"The model will evaluate each paper against the checklist in the prompt.")
