#!/usr/bin/env python3
"""
IbogaineVault Phase 2 Audit — Category 2 Table Triage
Classifies table inconsistencies as likely-false-positive or likely-real.
"""

import re
import os
import sys
from collections import Counter

VAULT = sys.argv[1] if len(sys.argv) > 1 else "/Users/aretesofia/IbogaineVault"

TABLE_FILES = [
    "2025/Swieczkowski2025_Clinical_Trials_Landscape.md",
    "2019/Coleman2019_SERT-Ibogaine_Complexes_Illuminate_Inhibition_Transport_Mechanisms.md",
    "2000/Glick2000_18-MC.md",
    "2024/Uzelac2024_Cardiotoxic_Necrosis_Redox.md",
    "2001/Mash2001_Ibogaine_Heroin_Withdrawal.md",
    "2004/Bastiaans2004_Life_After_Ibogaine.md",
    "2019/Bouso2019_Product_Quality.md",
    "Clinical_Guidelines/Lotsof2003_Ibogaine_Therapy_Manual.md",
    "Clinical_Guidelines/Patterson2014_IACT_Aotearoa_NZ_Guidelines_Integrated_Therapy.md",
    "2025/Brown2025_Mystical_Experience_PTSD_Veterans.md",
    "2025/Chen2025_Multiple_Sclerosis_Neuroimaging.md",
    "2010/Ray2010_Psychedelics_Human_Receptorome.md",
    "2020/Canessa2020_Ibogaine_Noribogaine_in_Tx_Review_Safety_Efficacy.md",
    "2023/Davis2023_Ibogaine_5MeO-DMT_for_SEALS.md",
    "1992/Glick1992_Ibogaine_Morphine_Withdrawal_Rats.md",
    "1994/Sheppard1994_Preliminary_Investigation_Ibogaine.md",
    "1996/Benwell1996_Ibogaine_Nicotine_Dopamine_Behaviour.md",
    "1996/Layer1996_IbogaineAnalogs_NMDA.md",
    "1998/Obach1998_CYP2D6_Ibogaine_Metabolism.md",
    "2001/Glick2001_Mechanisms_Action_Ibogaine_18MC.md",
    "2006/He2006_Ibogaine_and_GDNF.md",
    "2008/Cheze2008_Ibogaine_Noribogaine_LC-MSMS_Drowning_Death.md",
    "2012/Alper2012_Ibogaine_Fatalities.md",
    "2012/Paskulin2012_Metabolic_Plasticity_Ibogaine_Economising_Energy.md",
    "2014/Prior2014_Ibogaine_Cocaine_Pilot_RCT.md",
    "2014/Schenberg2014_Treating_Drug_Dependence_Retrospective_Study.md",
    "2015/Glue2015_Noribogaine_Ascending_Doses.md",
    "2015/Marta2015_Ibogaine_Mania_Case_Reports.md",
    "2016/Alper2016_hERG_Blockade.md",
    "2016/Belgers2016_Ibogaine_Addiction_Animal_Model_Review_Meta-analysis.md",
    "2016/Litjens2016_How_Toxic_Is_Ibogaine.md",
    "2018/Mash2018_Ibogaine_Detox_Opioid_Cocaine_Clinical_Observations_Tx_Outcomes.md",
    "2020/Davis2020_SpecialOps_Veterans_Trauma.md",
    "2020/Wilson2020_Novel_Tx_OUD_Ibogaine_Iboga_Case_Study.md",
    "2022/Kock2022_Systemic_Review_Clinical_Trials_Therapeutic_Applications_Ibogaine.md",
    "2022/Rodriguez-Cano2022_Underground_Ibogaine_Use_for_SUD_Tx_Qualitiative_Analysis_Subjective_Experiences.md",
    "2023/Alfonso2023_Ibogaine_Atypical_Psychedelic_Review_ES.md",
    "2023/Cherian2023_Ibogaine_Cognitive_Functioning.md",
    "2023/Rocha2023_Setting_Factors_Associated_With_Improved_Ibogaine_Safety.md",
    "2024/Chen2024_RIVM_Iboga_Risk_Assessment.md",
    "2024/Cherian2024_Magnesium_Ibogaine_TBI.md",
    "2025/Espejito2025_Ibogaine_Experience_Scale_Psychometrics_Subjective.md",
    "2025/Hwu2025_Matrix_Pharmacology_VMAT2_SERT.md",
    "2025/Iyer2025_Modular_Synthesis_Nature_Chemistry.md",
    "2026/Geoly2026_Cortical_Thickness_Brain_Age_MISTIC.md",
]

FOOTNOTE_PATTERNS = [
    r'^\s*\|?\s*\*+',
    r'^\s*\|?\s*[†‡§¶#]',
    r'^\s*\|?\s*(?:Note|Source|Abbreviation|Legend|Values|Data|SD|SEM|CI|NS|NA)\s*[:;]',
    r'^\s*\|?\s*(?:p\s*[<>=]|P\s*[<>=])',
    r'^\s*\|?\s*(?:Significance|Statistical)',
    r'<br>',
    r'^\s*\|?\s*$',
    r'^\s*\|[-:|\s]+\|?\s*$',
]

def count_pipes(line):
    return line.count('|')

def is_footnote_row(line):
    for pat in FOOTNOTE_PATTERNS:
        if re.search(pat, line, re.IGNORECASE):
            return True
    return False

def is_separator_row(line):
    cleaned = line.strip().replace(' ', '')
    return bool(re.match(r'^\|?[-:|]+\|?$', cleaned))

def get_category(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith('---'):
            end = content.index('---', 3)
            lines = content[3:end].split('\n')
            cat = 'UNKNOWN'
            sec = []
            in_sec = False
            for line in lines:
                if line.startswith('category:'):
                    cat = line.split(':',1)[1].strip().strip('"')
                if line.startswith('secondary_categories:'):
                    in_sec = True
                    continue
                if in_sec:
                    if line.strip().startswith('- '):
                        sec.append(line.strip()[2:].strip().strip('"'))
                    else:
                        in_sec = False
            return cat, sec
    except:
        pass
    return 'UNKNOWN', []

def analyze_tables(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    results = []
    in_table = False
    table_start = -1
    table_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        has_pipe = '|' in stripped
        
        if has_pipe and not in_table:
            in_table = True
            table_start = i + 1
            table_lines = [(i+1, stripped)]
        elif has_pipe and in_table:
            table_lines.append((i+1, stripped))
        elif not has_pipe and in_table:
            if len(table_lines) >= 2:
                issues = analyze_single_table(table_lines)
                if issues:
                    results.append({
                        'table_start': table_start,
                        'table_rows': len(table_lines),
                        'issues': issues
                    })
            in_table = False
            table_lines = []
    
    if in_table and len(table_lines) >= 2:
        issues = analyze_single_table(table_lines)
        if issues:
            results.append({
                'table_start': table_start,
                'table_rows': len(table_lines),
                'issues': issues
            })
    
    return results

def analyze_single_table(table_lines):
    issues = []
    pipe_counts = [count_pipes(line) for _, line in table_lines]
    count_freq = Counter(pipe_counts)
    expected_pipes = count_freq.most_common(1)[0][0]
    
    for line_num, line in table_lines:
        pipes = count_pipes(line)
        if pipes != expected_pipes:
            if is_separator_row(line):
                cls = "FALSE_POS:separator"
            elif is_footnote_row(line):
                cls = "FALSE_POS:footnote"
            elif pipes <= 2 and expected_pipes > 3:
                cls = "FALSE_POS:caption_or_note"
            elif pipes == 1 and expected_pipes > 2:
                cls = "FALSE_POS:section_header"
            else:
                diff = abs(pipes - expected_pipes)
                if diff == 1:
                    cls = "SUSPECT:off_by_one"
                else:
                    cls = f"LIKELY_REAL:off_by_{diff}"
            
            issues.append({
                'line': line_num,
                'expected_pipes': expected_pipes,
                'actual_pipes': pipes,
                'classification': cls,
                'text_preview': line[:100].strip()
            })
    
    return issues

def main():
    print("=" * 90)
    print("  IbogaineVault Phase 2 — Category 2 TABLE FORMATTING Automated Triage")
    print("=" * 90)
    print()
    
    likely_real = []
    suspect = []
    false_pos = []
    errors = []
    
    for relpath in TABLE_FILES:
        filepath = os.path.join(VAULT, relpath)
        if not os.path.exists(filepath):
            errors.append(relpath)
            continue
        
        cat, sec_cats = get_category(filepath)
        table_issues = analyze_tables(filepath)
        
        file_has_real = False
        file_has_suspect = False
        file_classifications = []
        
        for table in table_issues:
            for issue in table['issues']:
                cls = issue['classification']
                file_classifications.append({
                    'file': relpath,
                    'category': cat,
                    'secondary': sec_cats,
                    'table_start': table['table_start'],
                    **issue,
                })
                if cls.startswith("LIKELY_REAL"):
                    file_has_real = True
                elif cls.startswith("SUSPECT"):
                    file_has_suspect = True
        
        if file_has_real:
            likely_real.append((relpath, cat, sec_cats, file_classifications))
        elif file_has_suspect:
            suspect.append((relpath, cat, sec_cats, file_classifications))
        elif file_classifications:
            false_pos.append((relpath, cat, sec_cats, file_classifications))
        else:
            false_pos.append((relpath, cat, sec_cats, []))
    
    print(f"  SUMMARY")
    print(f"  {'─' * 50}")
    print(f"  Files analysed:        {len(TABLE_FILES) - len(errors)}")
    print(f"  LIKELY REAL issues:    {len(likely_real)} files")
    print(f"  SUSPECT (off-by-one):  {len(suspect)} files")
    print(f"  FALSE POSITIVE:        {len(false_pos)} files")
    if errors:
        print(f"  File not found:        {len(errors)} files")
    print()
    
    if likely_real:
        print("=" * 90)
        print("  LIKELY REAL TABLE ISSUES — Require Manual Inspection")
        print("=" * 90)
        
        def sort_key(item):
            _, cat, sec_cats, classifications = item
            is_red = 1 if cat == 'RED' or 'RED' in sec_cats else 0
            is_green = 1 if cat == 'GREEN' or 'GREEN' in sec_cats else 0
            return (-is_red, -is_green, -len([c for c in classifications if c['classification'].startswith('LIKELY_REAL')]))
        
        likely_real.sort(key=sort_key)
        
        for relpath, cat, sec_cats, classifications in likely_real:
            sec_str = f" + {','.join(sec_cats)}" if sec_cats else ""
            real_issues = [c for c in classifications if c['classification'].startswith('LIKELY_REAL')]
            suspect_issues = [c for c in classifications if c['classification'].startswith('SUSPECT')]
            print(f"\n  [{cat}{sec_str}] {relpath}")
            print(f"    Real: {len(real_issues)}, Suspect: {len(suspect_issues)}")
            for c in real_issues[:5]:
                print(f"    L{c['line']}: {c['actual_pipes']}p vs {c['expected_pipes']}p expected ({c['classification']})")
                print(f"      → {c['text_preview']}")
    
    if suspect:
        print()
        print("=" * 90)
        print("  SUSPECT (OFF-BY-ONE) — Lower Priority")
        print("=" * 90)
        for relpath, cat, sec_cats, classifications in suspect:
            sec_str = f" + {','.join(sec_cats)}" if sec_cats else ""
            sus = [c for c in classifications if c['classification'].startswith('SUSPECT')]
            print(f"\n  [{cat}{sec_str}] {relpath}")
            for c in sus[:3]:
                print(f"    L{c['line']}: {c['actual_pipes']}p vs {c['expected_pipes']}p ({c['classification']})")
                print(f"      → {c['text_preview']}")
    
    if false_pos:
        print()
        print("=" * 90)
        print(f"  FALSE POSITIVES — No Action ({len(false_pos)} files)")
        print("=" * 90)
        for relpath, cat, _, classifications in false_pos:
            fp_types = set(c['classification'].split(':')[1] for c in classifications if ':' in c['classification']) if classifications else {'clean'}
            print(f"    ✓ [{cat}] {relpath}  ({', '.join(fp_types)})")
    
    if errors:
        print(f"\n  NOT FOUND ({len(errors)}):")
        for e in errors:
            print(f"    ✗ {e}")
    
    print()
    print("=" * 90)

if __name__ == '__main__':
    main()
