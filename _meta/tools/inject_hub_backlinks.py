#!/usr/bin/env python3
"""
E1 Hub Back-Link Injector
Adds parent hub link to papers' See Also sections where missing.

Maps category → hub:
  RED → RED_Cardiac_Safety_Hub
  GREEN → GREEN_Clinical_Protocols_Hub
  ORANGE → ORANGE_Mechanisms_Hub
  BLUE → BLUE_Outcomes_Hub
  PURPLE → PURPLE_Phenomenology_Hub
  WHITE → WHITE_Historical_Hub

Logic:
  1. Find all papers with ## See Also
  2. Check if they already have a _Hub link in See Also
  3. If not, read category from YAML frontmatter
  4. Insert "**Parent hub:** [[X_Hub]]" as first line after ## See Also
"""

import os
import re
import sys

VAULT = "/Users/aretesofia/IbogaineVault"
PAPER_DIRS = [
    "1957","1969","1971","1991","1992","1993","1994","1995","1996","1997",
    "1998","1999","2000","2001","2002","2003","2004","2005","2006","2007",
    "2008","2009","2010","2011","2012","2013","2014","2015","2016","2017",
    "2018","2019","2020","2021","2022","2023","2024","2025","2026",
    "Clinical_Guidelines","Primary_Sources","Industry_Documents","Other"
]

CATEGORY_HUB = {
    "RED": "RED_Cardiac_Safety_Hub",
    "GREEN": "GREEN_Clinical_Protocols_Hub",
    "ORANGE": "ORANGE_Mechanisms_Hub",
    "BLUE": "BLUE_Outcomes_Hub",
    "PURPLE": "PURPLE_Phenomenology_Hub",
    "WHITE": "WHITE_Historical_Hub",
}

def get_category(content):
    """Extract category from YAML frontmatter."""
    m = re.search(r'^category:\s*(\w+)', content, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None

def has_hub_in_see_also(content):
    """Check if See Also section already contains a hub link."""
    see_also_match = re.search(r'## See Also.*', content, re.DOTALL)
    if not see_also_match:
        return True  # no see also = skip
    see_also_text = see_also_match.group(0)
    return '_Hub' in see_also_text

def inject_hub_link(content, hub_name):
    """Insert hub back-link after ## See Also heading."""
    # Pattern 1: ## See Also\n\n- (blank line before list)
    pattern = r'(## See Also\n)\n'
    replacement = f'\\1\n**Parent hub:** [[{hub_name}]]\n\n'
    new_content = re.sub(pattern, replacement, content, count=1)
    if new_content != content:
        return new_content
    
    # Pattern 2: ## See Also\n- (no blank line before list)
    pattern2 = r'(## See Also\n)(-)'
    replacement2 = f'\\1\n**Parent hub:** [[{hub_name}]]\n\n\\2'
    new_content = re.sub(pattern2, replacement2, content, count=1)
    return new_content

def main():
    dry_run = '--dry-run' in sys.argv
    
    modified = 0
    skipped_no_category = 0
    skipped_has_hub = 0
    skipped_no_see_also = 0
    errors = []
    
    for d in PAPER_DIRS:
        dirpath = os.path.join(VAULT, d)
        if not os.path.isdir(dirpath):
            continue
        for root, dirs, files in os.walk(dirpath):
            for f in files:
                if not f.endswith('.md'):
                    continue
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                except Exception as e:
                    errors.append(f"{filepath}: {e}")
                    continue
                
                if '## See Also' not in content:
                    skipped_no_see_also += 1
                    continue
                
                if has_hub_in_see_also(content):
                    skipped_has_hub += 1
                    continue
                
                category = get_category(content)
                if not category or category not in CATEGORY_HUB:
                    skipped_no_category += 1
                    if category:
                        errors.append(f"{filepath}: unknown category '{category}'")
                    else:
                        errors.append(f"{filepath}: no category field")
                    continue
                
                hub_name = CATEGORY_HUB[category]
                new_content = inject_hub_link(content, hub_name)
                
                if new_content != content:
                    if dry_run:
                        print(f"WOULD MODIFY: {filepath} → [[{hub_name}]]")
                    else:
                        with open(filepath, 'w', encoding='utf-8') as fh:
                            fh.write(new_content)
                        print(f"MODIFIED: {filepath} → [[{hub_name}]]")
                    modified += 1
                else:
                    errors.append(f"{filepath}: injection pattern didn't match")
    
    print(f"\n--- Summary ---")
    print(f"{'Would modify' if dry_run else 'Modified'}: {modified}")
    print(f"Skipped (already has hub): {skipped_has_hub}")
    print(f"Skipped (no See Also): {skipped_no_see_also}")
    print(f"Skipped (no/unknown category): {skipped_no_category}")
    if errors:
        print(f"\nIssues ({len(errors)}):")
        for e in errors:
            print(f"  {e}")

if __name__ == '__main__':
    main()
