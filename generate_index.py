#!/usr/bin/env python3
"""
IbogaineVault Machine-Readable Index Generator
===============================================
Produces papers.json and papers.csv from YAML frontmatter across the vault.

Zero external dependencies (PyYAML used when available, manual parser fallback).
Reuses discovery and parsing patterns from validate_vault.py.

USAGE:
  python3 generate_index.py --vault /path/to/vault
  python3 generate_index.py --vault /path/to/vault --output /path/to/output

Created: 2026-03-13 (Phase 2B)
"""

import os
import sys
import re
import json
import csv
import argparse
from pathlib import Path
from datetime import datetime, timezone


# ══════════════════════════════════════════
# VAULT DETECTION (mirrored from validate_vault.py)
# ══════════════════════════════════════════

VAULT_MARKERS = ["_meta/schema_registry.yml", "HOME.md", "Hubs"]


def detect_vault_root(explicit_path):
    """Validate an explicit vault root path.
    Returns Path or exits with error."""
    p = Path(explicit_path)
    if p.exists() and any((p / m).exists() for m in VAULT_MARKERS):
        return p
    print(f"ERROR: {explicit_path} does not look like a vault root.", file=sys.stderr)
    sys.exit(1)


# ══════════════════════════════════════════
# YAML PARSING (mirrored from validate_vault.py)
# ══════════════════════════════════════════

def extract_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file.
    Returns (dict, list_of_parse_errors).
    Uses PyYAML when available, falls back to manual parser."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return None, [f"Cannot read file: {e}"]

    if not content.startswith("---"):
        return None, ["No YAML frontmatter"]

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        end_match = re.search(r'\n---\s*$', content[3:])
        if not end_match:
            return None, ["No closing --- delimiter"]

    yaml_text = content[3:3 + end_match.start()]

    # Try PyYAML first
    try:
        import yaml
        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            return None, ["YAML doesn't parse as dict"]
        return data, []
    except ImportError:
        pass
    except Exception as e:
        return None, [f"YAML parse error: {e}"]

    # Manual fallback
    data, errors = _parse_yaml_manual(yaml_text)
    return data, errors


def _parse_yaml_manual(text):
    """Simple manual YAML parser for frontmatter. Handles the vault's patterns."""
    data = {}
    errors = []
    current_key = None
    current_list = None
    lines = text.split('\n')

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        if stripped.startswith('- ') and current_key:
            val = stripped[2:].strip().strip('"').strip("'")
            if current_list is None:
                current_list = []
            current_list.append(val)
            data[current_key] = current_list
            continue

        match = re.match(r'^([a-z_]+)\s*:\s*(.*)', line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            current_key = key
            current_list = None

            if not value:
                data[key] = None
                continue
            if value.startswith('[') and value.endswith(']'):
                items = [v.strip().strip('"').strip("'") for v in value[1:-1].split(',')]
                data[key] = [x for x in items if x]
                current_list = data[key]
                continue
            if value.lower() in ('true', 'false'):
                data[key] = value.lower() == 'true'
                continue
            try:
                data[key] = int(value)
                continue
            except ValueError:
                pass
            data[key] = value.strip('"').strip("'")

    return data, errors


# ══════════════════════════════════════════
# FILE DISCOVERY (mirrored from validate_vault.py)
# ══════════════════════════════════════════

def discover_paper_files(vault_root):
    """Find all .md files in paper locations. Works for both working vault and Tier 1."""
    paper_files = []
    vault = Path(vault_root)

    # Year folders (1957-2026)
    for entry in sorted(vault.iterdir()):
        if entry.is_dir() and re.match(r'^\d{4}$', entry.name):
            for md in sorted(entry.glob("*.md")):
                paper_files.append(md)

    # Special paper folders
    for folder_name in ["Clinical_Guidelines", "Primary_Sources", "Other", "Industry_Documents"]:
        folder = vault / folder_name
        if folder.exists():
            for md in sorted(folder.glob("*.md")):
                paper_files.append(md)
            for subdir in sorted(folder.iterdir()):
                if subdir.is_dir() and subdir.name not in (".DS_Store",):
                    for md in sorted(subdir.glob("*.md")):
                        paper_files.append(md)

    return paper_files


# ══════════════════════════════════════════
# FIELD EXTRACTION
# ══════════════════════════════════════════

# The 23 fields to extract, with their YAML source key and absent-value handling.
# Most fields map 1:1 from YAML. "primary_category" is renamed from "category".
INDEX_FIELDS = [
    # (output_key, yaml_key, absent_default)
    ("title",                "title",                None),
    ("authors",              "authors",              None),
    ("year",                 "year",                 None),
    ("doi",                  "doi",                  None),
    ("primary_category",     "category",             None),
    ("secondary_categories", "secondary_categories", None),
    ("evidence_level",       "evidence_level",       None),
    ("tags",                 "tags",                 None),
    ("clinical_significance","clinical_significance", None),
    ("key_findings",         "key_findings",         None),
    ("sample_size",          "sample_size",          None),
    ("mortality_count",      "mortality_count",      None),
    ("mortality_scope",      "mortality_scope",       None),
    ("qtc_data",             "qtc_data",             None),   # Missing → null, NOT false
    ("herg_data",            "herg_data",            None),   # Missing → null, NOT false
    ("electrolyte_data",     "electrolyte_data",     None),   # Missing → null, NOT false
    ("contraindications",    "contraindications",    None),
    ("dosing_range",         "dosing_range",         None),
    ("route",                "route",                None),
    ("source_pdf",           "source_pdf",           None),
    ("journal",              "journal",              None),
    ("aliases",              "aliases",              []),      # Missing → [], NOT null
    ("source_url",           "source_url",           None),
    ("pmid",                 "pmid",                 None),
    ("pmcid",                "pmcid",                None),
    ("open_access",          "open_access",          None),
    ("publisher",            "publisher",             None),
    ("body_format",          "body_format",           None),
    ("issn",                 "issn",                  None),
    ("licence_type",         "licence_type",          None),
    ("licence_verified",     "licence_verified",      None),
]


def extract_paper_record(yaml_dict):
    """Extract the 21 index fields from a parsed YAML frontmatter dict.
    Returns a dict suitable for JSON serialisation."""
    record = {}
    for output_key, yaml_key, absent_default in INDEX_FIELDS:
        value = yaml_dict.get(yaml_key)
        if value is None:
            # Field absent or explicitly null in YAML
            # Use the specified absent default (None for most, [] for aliases)
            if absent_default is not None:
                record[output_key] = list(absent_default)  # copy to avoid mutation
            else:
                record[output_key] = None
        else:
            record[output_key] = value
    return record


# ══════════════════════════════════════════
# OUTPUT GENERATION
# ══════════════════════════════════════════

def generate_json(papers, output_path):
    """Write papers.json to the specified directory."""
    envelope = {
        "vault": "IbogaineVault",
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "paper_count": len(papers),
        "schema_reference": "_meta/schema_registry.yml",
        "papers": papers,
    }
    filepath = Path(output_path) / "papers.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2, ensure_ascii=False)
    return filepath


def _flatten_for_csv(value):
    """Convert a value for CSV output.
    Lists → semicolon-space joined. None → empty string. Booleans → lowercase."""
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(v) for v in value)
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def generate_csv(papers, output_path):
    """Write papers.csv to the specified directory."""
    if not papers:
        return None

    # Column order matches INDEX_FIELDS
    columns = [output_key for output_key, _, _ in INDEX_FIELDS] + ["filepath"]

    filepath = Path(output_path) / "papers.csv"
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for paper in papers:
            row = [_flatten_for_csv(paper.get(col)) for col in columns]
            writer.writerow(row)
    return filepath


# ══════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="IbogaineVault Machine-Readable Index Generator")
    parser.add_argument("--vault", type=str, required=True,
                        help="Path to vault root directory")
    parser.add_argument("--output", type=str, default=None,
                        help="Output directory (defaults to vault root)")
    args = parser.parse_args()

    vault_root = detect_vault_root(args.vault)
    output_dir = Path(args.output) if args.output else vault_root

    if not output_dir.exists():
        print(f"ERROR: Output directory does not exist: {output_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Vault root: {vault_root}")
    print(f"Output:     {output_dir}")
    print()

    # Discover papers
    paper_files = discover_paper_files(vault_root)
    if not paper_files:
        print("No paper files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Discovered {len(paper_files)} papers")


    # Extract records
    papers = []
    parse_failures = []
    for filepath in paper_files:
        data, errors = extract_frontmatter(filepath)
        if data:
            record = extract_paper_record(data)
            # Add computed filepath (relative to vault root)
            rel_path = str(filepath.relative_to(vault_root))
            record['filepath'] = rel_path
            papers.append(record)
        else:
            parse_failures.append((filepath, errors))

    if parse_failures:
        print(f"\n⚠ {len(parse_failures)} parse failure(s):")
        for fp, errs in parse_failures[:10]:
            print(f"  {Path(fp).name}: {errs[0] if errs else 'unknown'}")
        if len(parse_failures) > 10:
            print(f"  ... and {len(parse_failures) - 10} more")
        print()

    # Generate outputs
    json_path = generate_json(papers, output_dir)
    csv_path = generate_csv(papers, output_dir)

    print(f"\n── Results ──")
    print(f"  Papers indexed:  {len(papers)}")
    print(f"  Parse failures:  {len(parse_failures)}")
    print(f"  papers.json:     {json_path}")
    print(f"  papers.csv:      {csv_path}")

    # Quick sanity checks
    print(f"\n── Sanity checks ──")

    # Check: JSON paper_count matches
    with open(json_path, "r", encoding="utf-8") as f:
        j = json.load(f)
    if j["paper_count"] == len(papers):
        print(f"  ✓ JSON paper_count matches ({j['paper_count']})")
    else:
        print(f"  ✗ JSON paper_count mismatch: header={j['paper_count']}, actual={len(papers)}")

    # Check: boolean flags are null when absent, not false
    bool_fields = ["qtc_data", "herg_data", "electrolyte_data"]
    null_bools = sum(1 for p in papers for bf in bool_fields if p.get(bf) is None)
    false_bools = sum(1 for p in papers for bf in bool_fields if p.get(bf) is False)
    true_bools = sum(1 for p in papers for bf in bool_fields if p.get(bf) is True)
    print(f"  Boolean flags: {true_bools} true, {false_bools} false, {null_bools} null")

    # Check: aliases are [] when absent, not null
    null_aliases = sum(1 for p in papers if p.get("aliases") is None)
    empty_aliases = sum(1 for p in papers if p.get("aliases") == [])
    populated_aliases = sum(1 for p in papers if isinstance(p.get("aliases"), list) and len(p.get("aliases", [])) > 0)
    print(f"  Aliases: {populated_aliases} populated, {empty_aliases} empty [], {null_aliases} null (should be 0)")

    # Check: at least one source_url populated
    source_urls = sum(1 for p in papers if p.get("source_url"))
    print(f"  source_url populated: {source_urls}")

    # Check: CSV row count
    with open(csv_path, "r", encoding="utf-8") as f:
        csv_lines = sum(1 for _ in f) - 1  # subtract header
    if csv_lines == len(papers):
        print(f"  ✓ CSV row count matches ({csv_lines})")
    else:
        print(f"  ✗ CSV row count mismatch: {csv_lines} vs {len(papers)}")

    print()


if __name__ == "__main__":
    main()
