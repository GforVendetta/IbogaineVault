#!/usr/bin/env python3
"""
Boolean Sweep — IbogaineVault Session 2 follow-up
Run: python3 /Users/aretesofia/IbogaineVault/_meta/tools/boolean_sweep.py
Paste output back into the conversation.

v2 — fixed field-name bugs: file→filepath, category→primary_category
"""
import json

with open('/Users/aretesofia/IbogaineVault-Tier1/papers.json', 'r') as f:
    data = json.load(f)
papers = data.get('papers', data) if isinstance(data, dict) else data
if isinstance(papers, dict) and 'papers' in papers:
    papers = papers['papers']

def stem(p):
    """Extract readable stem from filepath."""
    fp = p.get('filepath', '?')
    return fp.split('/')[-1].replace('.md', '')[:55]

print("=" * 70)
print("BOOLEAN SWEEP v2 — IbogaineVault")
print("=" * 70)

# --- electrolyte_data: true ---
elec = [p for p in papers if p.get('electrolyte_data') is True]
print(f"\n### electrolyte_data: true ({len(elec)} papers)\n")
for p in sorted(elec, key=lambda x: x.get('year', 0)):
    print(f"  {p.get('year','')} | {stem(p):55s} | {p.get('primary_category','?'):5s} | ev:{p.get('evidence_level','?')}")

# --- qtc_data: true ---
qtc = [p for p in papers if p.get('qtc_data') is True]
print(f"\n### qtc_data: true ({len(qtc)} papers)\n")
for p in sorted(qtc, key=lambda x: x.get('year', 0)):
    print(f"  {p.get('year','')} | {stem(p):55s} | {p.get('primary_category','?'):5s} | ev:{p.get('evidence_level','?')}")

# --- herg_data: true ---
herg = [p for p in papers if p.get('herg_data') is True]
print(f"\n### herg_data: true ({len(herg)} papers)\n")
for p in sorted(herg, key=lambda x: x.get('year', 0)):
    print(f"  {p.get('year','')} | {stem(p):55s} | {p.get('primary_category','?'):5s} | ev:{p.get('evidence_level','?')}")

# --- SUSPICIOUS PATTERNS ---
print("\n" + "=" * 70)
print("SUSPICIOUS PATTERNS")
print("=" * 70)

# 1. electrolyte_data true on reviews/preclinical/in-vitro
review_types = {'review', 'systematic-review', 'in-vitro', 'preclinical', 'journalism', 'commentary'}
suspect = [p for p in elec if p.get('evidence_level', '') in review_types]
print(f"\n⚠ electrolyte_data: true on review/preclinical ({len(suspect)}):")
for p in suspect:
    print(f"    {stem(p):55s} | ev:{p.get('evidence_level','?')}")

# 2. Both herg + qtc true (rare — bench AND clinical in one paper)
both = [p for p in papers if p.get('herg_data') is True and p.get('qtc_data') is True]
print(f"\n⚠ Both herg_data AND qtc_data true ({len(both)}):")
for p in both:
    print(f"    {stem(p):55s} | ev:{p.get('evidence_level','?')}")

# 3. RED papers with ALL booleans false
red_false = [p for p in papers if p.get('primary_category') == 'RED'
             and p.get('qtc_data') is False
             and p.get('herg_data') is False
             and p.get('electrolyte_data') is False]
print(f"\n⚠ RED papers with ALL booleans false ({len(red_false)}):")
for p in sorted(red_false, key=lambda x: x.get('year', 0)):
    kf = (p.get('key_findings') or '')[:80]
    print(f"    {p.get('year','')} | {stem(p):55s} | mort:{str(p.get('mortality_count','—')):4s} | {kf}")

# 4. Non-RED papers with mortality_count > 0
non_red_mort = [p for p in papers if p.get('primary_category') != 'RED'
                and p.get('mortality_count') is not None
                and p.get('mortality_count', 0) > 0]
print(f"\n⚠ Non-RED papers with mortality_count > 0 ({len(non_red_mort)}):")
for p in sorted(non_red_mort, key=lambda x: (-x.get('mortality_count', 0), x.get('year', 0))):
    cat = p.get('primary_category', '?')
    sc = p.get('secondary_categories') or []
    red_sec = '✓' if 'RED' in sc else '✗'
    print(f"    {stem(p):55s} | cat:{cat:6s} | mort:{p.get('mortality_count'):3d} | RED_sec:{red_sec}")

print("\n" + "=" * 70)
print("SWEEP COMPLETE")
print("=" * 70)
