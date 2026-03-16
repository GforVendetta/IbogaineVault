#!/usr/bin/env python3
"""
Deduplicate pmid: and pmcid: lines in YAML frontmatter.

The resolve_pmids.py script inserted pmid/pmcid lines but didn't detect
that some files already had these fields (from a prior run or schema
propagation), resulting in duplicate YAML keys.

This script:
1. Scans all .md files in paper directories
2. For each file, checks if pmid: or pmcid: appears more than once
   within the YAML frontmatter block
3. Removes the SECOND (and any subsequent) occurrence, keeping the first
4. Reports what it fixed

Safe: only operates within the --- ... --- frontmatter block.
"""

import os
import re
from pathlib import Path

VAULT_ROOT = "/Users/aretesofia/IbogaineVault"

PAPER_DIRS = [
    "1957", "1969", "1971", "1991", "1992", "1993", "1994", "1995",
    "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003",
    "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011",
    "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019",
    "2020", "2021", "2022", "2023", "2024", "2025", "2026",
    "Clinical_Guidelines", "Industry_Documents", "Other", "Primary_Sources",
]

def find_paper_files():
    files = []
    for d in PAPER_DIRS:
        dirpath = os.path.join(VAULT_ROOT, d)
        if not os.path.isdir(dirpath):
            continue
        for fn in os.listdir(dirpath):
            if fn.endswith(".md"):
                files.append(os.path.join(dirpath, fn))
    return sorted(files)

def dedup_frontmatter_field(lines, field_name):
    """Remove duplicate field_name: lines from frontmatter.
    Returns (new_lines, removed_count)."""
    # Find frontmatter boundaries
    fm_start = None
    fm_end = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if fm_start is None:
                fm_start = i
            else:
                fm_end = i
                break

    if fm_start is None or fm_end is None:
        return lines, 0

    # Find all occurrences of field_name: within frontmatter
    pattern = re.compile(rf"^{re.escape(field_name)}:\s")
    occurrences = []
    for i in range(fm_start + 1, fm_end):
        if pattern.match(lines[i]):
            occurrences.append(i)

    if len(occurrences) <= 1:
        return lines, 0

    # Keep the first, remove all subsequent
    to_remove = set(occurrences[1:])
    new_lines = [line for i, line in enumerate(lines) if i not in to_remove]
    return new_lines, len(to_remove)

def main():
    files = find_paper_files()
    print(f"Scanning {len(files)} paper files...")

    pmid_fixed = 0
    pmcid_fixed = 0
    files_modified = 0

    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            lines = f.readlines()

        lines, pmid_removed = dedup_frontmatter_field(lines, "pmid")
        lines, pmcid_removed = dedup_frontmatter_field(lines, "pmcid")

        if pmid_removed or pmcid_removed:
            with open(fp, "w", encoding="utf-8") as f:
                f.writelines(lines)
            files_modified += 1
            pmid_fixed += pmid_removed
            pmcid_fixed += pmcid_removed
            fname = os.path.basename(fp)
            parts = []
            if pmid_removed:
                parts.append(f"pmid x{pmid_removed}")
            if pmcid_removed:
                parts.append(f"pmcid x{pmcid_removed}")
            print(f"  FIXED: {fname} — removed {', '.join(parts)}")

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"  Files scanned:  {len(files)}")
    print(f"  Files modified: {files_modified}")
    print(f"  pmid dupes removed:  {pmid_fixed}")
    print(f"  pmcid dupes removed: {pmcid_fixed}")

    # Verification pass
    print(f"\nVERIFICATION: re-scanning for any remaining duplicates...")
    remaining = 0
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        for field in ["pmid", "pmcid"]:
            count = len(re.findall(rf"^{field}:", content, re.MULTILINE))
            if count > 1:
                print(f"  STILL DUPLICATE: {os.path.basename(fp)} has {count}x {field}")
                remaining += 1
    if remaining == 0:
        print("  ✅ CLEAN — zero duplicate pmid/pmcid fields remain")
    else:
        print(f"  ❌ {remaining} duplicates still remain!")

if __name__ == "__main__":
    main()
