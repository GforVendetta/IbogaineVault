#!/usr/bin/env python3
"""
IbogaineVault Metadata Population Script
=========================================
Auto-populates open_access, publisher, body_format across all vault papers.
Generates a copyright risk report.

USAGE:
  python3 populate_metadata.py                          # dry-run (default)
  python3 populate_metadata.py --report                 # generate CSV report
  python3 populate_metadata.py --apply                  # modify files
  python3 populate_metadata.py --report --apply         # both

Created: 2026-03-16 (Phase 0-2)
"""

import os
import sys
import re
import csv
import argparse
from pathlib import Path

# ══════════════════════════════════════════
# VAULT DETECTION (from generate_index.py)
# ══════════════════════════════════════════

VAULT_MARKERS = ["_meta/schema_registry.yml", "HOME.md", "Hubs"]


def detect_vault_root(explicit_path):
    p = Path(explicit_path)
    if p.exists() and any((p / m).exists() for m in VAULT_MARKERS):
        return p
    print(f"ERROR: {explicit_path} does not look like a vault root.", file=sys.stderr)
    sys.exit(1)


def discover_paper_files(vault_root):
    paper_files = []
    vault = Path(vault_root)
    for entry in sorted(vault.iterdir()):
        if entry.is_dir() and re.match(r'^\d{4}$', entry.name):
            for md in sorted(entry.glob("*.md")):
                paper_files.append(md)
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
# FRONTMATTER EXTRACTION (string-based)
# ══════════════════════════════════════════

def read_file_parts(filepath):
    """Returns (yaml_text, body_text, raw_content) or (None, None, None)."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return None, None, None
    if not content.startswith("---"):
        return None, None, None
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        end_match = re.search(r'\n---\s*$', content[3:])
        if not end_match:
            return None, None, None
    yaml_text = content[3:3 + end_match.start()]
    body_start = 3 + end_match.end()
    body_text = content[body_start:]
    return yaml_text, body_text, content


def parse_yaml_value(yaml_text, key):
    """Extract a single top-level value from YAML text. Returns value or None."""
    pattern = rf'^{re.escape(key)}\s*:\s*(.*)$'
    match = re.search(pattern, yaml_text, re.MULTILINE)
    if not match:
        return None
    val = match.group(1).strip()
    if not val:
        return None
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        val = val[1:-1]
    if val.lower() == 'true':
        return True
    if val.lower() == 'false':
        return False
    return val


def yaml_has_field(yaml_text, key):
    """Check if a top-level YAML field exists."""
    pattern = rf'^{re.escape(key)}\s*:'
    return bool(re.search(pattern, yaml_text, re.MULTILINE))


# ══════════════════════════════════════════
# BODY FORMAT DETECTION
# ══════════════════════════════════════════

def has_heading(body, text):
    """Check if text appears as an h2 or h3 heading anywhere in the body."""
    pattern = rf'^#{{2,3}}\s+.*{re.escape(text)}'
    return bool(re.search(pattern, body, re.MULTILINE | re.IGNORECASE))


def has_numbered_sections(body):
    """Check for numbered academic section headings like ## 1. or ## 1.1"""
    pattern = r'^#{2,3}\s+\d+[\.\d]*\s+'
    return bool(re.search(pattern, body, re.MULTILINE))


def count_headings(body):
    """Count total h2/h3 headings in body."""
    return len(re.findall(r'^#{2,3}\s+', body, re.MULTILINE))


def detect_body_format(body):
    """Detect body format. Returns (format_string, ambiguity_flag)."""
    vault_markers = ["Key Findings", "Clinical Implications"]
    academic_markers = ["Introduction", "Methods", "Results", "Discussion"]
    has_vault = any(has_heading(body, m) for m in vault_markers)
    has_academic = any(has_heading(body, m) for m in academic_markers)
    has_numbered = has_numbered_sections(body)

    if has_vault and has_academic:
        return "hybrid", None
    if has_vault:
        return "vault-analytical", None
    if has_academic or has_numbered:
        return "academic-retained", None
    heading_count = count_headings(body)
    if heading_count > 5:
        return "narrative", "narrative-review"
    return "narrative", None


# ══════════════════════════════════════════
# PUBLISHER DETECTION
# ══════════════════════════════════════════

DOI_PUBLISHER_MAP = {
    "10.21203": "Research Square",
    "10.31665": "Food Science Publisher",
    "10.20944": "Preprints.org",
    "10.46919": "Psilocybin Technology",
    "10.47626": "Brazilian Journal Publisher",
    "10.14573": "Bentham Open",
    "10.1016": "Elsevier",
    "10.1002": "Wiley",
    "10.1111": "Wiley",
    "10.1007": "Springer Nature",
    "10.1038": "Springer Nature",
    "10.1017": "Cambridge University Press",
    "10.1021": "American Chemical Society",
    "10.1039": "Royal Society of Chemistry",
    "10.1051": "EDP Sciences",
    "10.1056": "NEJM Group",
    "10.1057": "Palgrave Macmillan",
    "10.1096": "FASEB",
    "10.1108": "Emerald Publishing",
    "10.1163": "Brill",
    "10.1590": "SciELO",
    "10.3109": "Informa Healthcare",
    "10.3389": "Frontiers",
    "10.3390": "MDPI",

    "10.1371": "PLoS",
    "10.1080": "Taylor & Francis",
    "10.1177": "SAGE",
    "10.1101": "Cold Spring Harbor",
    "10.1093": "Oxford University Press",
    "10.1155": "Hindawi",
    "10.2174": "Bentham Science",
    "10.1556": "Akadémiai Kiadó",
    "10.1186": "BioMed Central",
    "10.1124": "ASPET",
    "10.1097": "Lippincott Williams & Wilkins",
    "10.1073": "PNAS",
    "10.1523": "Society for Neuroscience",
    "10.1126": "AAAS",
    "10.4103": "Wolters Kluwer",
    "10.5334": "Ubiquity Press",
    "10.2147": "Dove Medical Press",
    "10.1089": "Mary Ann Liebert",
    "10.1146": "Annual Reviews",
    "10.7759": "Cureus",
    "10.21945": "RIVM",
}

DOI_PREFIXES_SORTED = sorted(DOI_PUBLISHER_MAP.keys(), key=len, reverse=True)

JOURNAL_PUBLISHER_MAP = {
    "frontiers in": "Frontiers",
    "plos ": "PLoS",
    "bmc ": "BioMed Central",
    "mdpi": "MDPI",
    "biorxiv": "Cold Spring Harbor",
}


def detect_publisher(doi, journal):
    """Detect publisher from DOI prefix or journal name. Returns string or None."""
    if doi:
        for prefix in DOI_PREFIXES_SORTED:
            if doi.startswith(prefix):
                return DOI_PUBLISHER_MAP[prefix]
    if journal:
        jl = journal.lower()
        for pattern, publisher in JOURNAL_PUBLISHER_MAP.items():
            if pattern in jl:
                return publisher
    return None


# ══════════════════════════════════════════
# OPEN ACCESS DETECTION
# ══════════════════════════════════════════

OA_PUBLISHERS = {
    "Frontiers", "MDPI", "PLoS", "BioMed Central", "Hindawi",
    "Ubiquity Press", "Dove Medical Press", "Cureus", "SciELO",
    "Preprints.org",
}

PAYWALLED_PUBLISHERS = {
    "Elsevier", "Wiley", "Springer Nature", "Taylor & Francis",
    "SAGE", "Bentham Science", "Akadémiai Kiadó",
    "Oxford University Press", "Lippincott Williams & Wilkins",
    "Mary Ann Liebert", "Annual Reviews", "ASPET", "AAAS",
    "Society for Neuroscience", "Cambridge University Press",
    "American Chemical Society", "Royal Society of Chemistry",
    "Informa Healthcare", "Palgrave Macmillan", "Brill",
    "EDP Sciences", "FASEB", "Emerald Publishing", "NEJM Group",
}


GREY_LIT_TYPES = {"journalism", "primary-source", "book-chapter", "thesis"}


def determine_open_access(doi, pmcid, publisher, journal, document_type):
    """Multi-signal OA detection. Returns True, False, or 'unknown'."""
    if pmcid:
        return True
    if publisher in OA_PUBLISHERS:
        return True
    if journal and any(x in journal.lower() for x in ["biorxiv", "preprint", "research square"]):
        return True
    if document_type in GREY_LIT_TYPES:
        return True
    if publisher in PAYWALLED_PUBLISHERS:
        return False
    return "unknown"


# ══════════════════════════════════════════
# YAML INSERTION (string surgery)
# ══════════════════════════════════════════

def build_insertion_block(open_access, publisher, body_format):
    """Build YAML lines to insert. Returns string (may be empty)."""
    lines = []
    if open_access is not None:
        if open_access is True:
            lines.append("open_access: true")
        elif open_access is False:
            lines.append("open_access: false")
        else:
            lines.append(f"open_access: {open_access}")
    if publisher is not None:
        lines.append(f'publisher: "{publisher}"')
    if body_format is not None:
        lines.append(f"body_format: {body_format}")
    return "\n".join(lines)


def apply_metadata(filepath, yaml_text, raw_content,
                   open_access, publisher, body_format):
    """Insert new metadata fields into file. Returns True if modified."""
    oa_val = open_access if not yaml_has_field(yaml_text, "open_access") else None
    pub_val = publisher if not yaml_has_field(yaml_text, "publisher") else None
    bf_val = body_format if not yaml_has_field(yaml_text, "body_format") else None

    block = build_insertion_block(oa_val, pub_val, bf_val)
    if not block:
        return False

    first_newline = raw_content.index('\n', 0)
    search_start = first_newline + 1
    end_match = re.search(r'\n---\s*\n', raw_content[search_start:])
    if not end_match:
        end_match = re.search(r'\n---\s*$', raw_content[search_start:])
    if not end_match:
        return False

    insert_pos = search_start + end_match.start()
    new_content = raw_content[:insert_pos] + "\n" + block + raw_content[insert_pos:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


# ══════════════════════════════════════════
# MAIN PROCESSING
# ══════════════════════════════════════════

def process_paper(filepath, apply=False):
    """Process a single paper. Returns a result dict."""
    yaml_text, body_text, raw_content = read_file_parts(filepath)
    if yaml_text is None:
        return {"filepath": str(filepath), "error": "Cannot parse frontmatter"}

    doi = parse_yaml_value(yaml_text, "doi")
    pmcid = parse_yaml_value(yaml_text, "pmcid")
    journal = parse_yaml_value(yaml_text, "journal")
    document_type = parse_yaml_value(yaml_text, "document_type")
    existing_publisher = parse_yaml_value(yaml_text, "publisher")

    body_format, ambiguity_flag = detect_body_format(body_text)

    if existing_publisher:
        publisher = existing_publisher
        publisher_source = "existing"
    else:
        publisher = detect_publisher(doi, journal)
        publisher_source = "detected" if publisher else "none"

    if yaml_has_field(yaml_text, "open_access"):
        open_access = parse_yaml_value(yaml_text, "open_access")
        oa_source = "existing"
    else:
        open_access = determine_open_access(doi, pmcid, publisher, journal, document_type)
        oa_source = "detected"

    line_count = len(body_text.splitlines()) if body_text else 0

    modified = False
    if apply:
        modified = apply_metadata(filepath, yaml_text, raw_content,
                                  open_access, publisher, body_format)

    return {
        "filepath": str(filepath),
        "open_access": open_access,
        "oa_source": oa_source,
        "publisher": publisher,
        "publisher_source": publisher_source,
        "body_format": body_format,
        "line_count": line_count,
        "doi": doi,
        "pmcid": pmcid,
        "document_type": document_type,
        "ambiguity_flag": ambiguity_flag,
        "modified": modified,
        "error": None,
    }


def write_report(results, output_path):
    """Write CSV report."""
    columns = ["filepath", "open_access", "publisher", "body_format",
               "line_count", "doi", "pmcid", "document_type", "ambiguity_flag"]
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for r in results:
            if r.get("error"):
                continue
            row = []
            for col in columns:
                val = r.get(col)
                if val is None:
                    row.append("")
                elif isinstance(val, bool):
                    row.append(str(val).lower())
                else:
                    row.append(str(val))
            writer.writerow(row)
    return output_path


def print_summary(results):
    """Print population summary and risk lists."""
    valid = [r for r in results if not r.get("error")]
    errors = [r for r in results if r.get("error")]
    oa_true = sum(1 for r in valid if r["open_access"] is True)
    oa_false = sum(1 for r in valid if r["open_access"] is False)
    oa_unknown = sum(1 for r in valid if r["open_access"] == "unknown")
    pub_populated = sum(1 for r in valid if r["publisher"])
    pub_existing = sum(1 for r in valid if r["publisher_source"] == "existing")
    pub_detected = sum(1 for r in valid if r["publisher_source"] == "detected")
    bf = {}
    for r in valid:
        bf[r["body_format"]] = bf.get(r["body_format"], 0) + 1
    modified = sum(1 for r in valid if r["modified"])

    print(f"\n{'='*60}")
    print(f"  METADATA POPULATION SUMMARY")
    print(f"{'='*60}")
    print(f"  Papers processed:  {len(valid)}")
    print(f"  Parse errors:      {len(errors)}")
    print(f"  Files modified:    {modified}")
    print(f"\n  open_access:")
    print(f"    true:    {oa_true}")
    print(f"    false:   {oa_false}")
    print(f"    unknown: {oa_unknown}")
    print(f"\n  publisher:")
    print(f"    populated:   {pub_populated} ({pub_existing} existing + {pub_detected} detected)")
    pub_gap = sum(1 for r in valid if r["doi"] and not r["publisher"])
    print(f"    DOI w/o pub: {pub_gap}")

    print(f"\n  body_format:")
    for fmt in ["vault-analytical", "academic-retained", "hybrid", "narrative"]:
        print(f"    {fmt}: {bf.get(fmt, 0)}")

    # Copyright risk
    copyright_risk = [r for r in valid
                      if r["open_access"] in (False, "unknown")
                      and r["body_format"] == "academic-retained"
                      and r["line_count"] > 200]
    if copyright_risk:
        print(f"\n{'='*60}")
        print(f"  COPYRIGHT RISK ({len(copyright_risk)} papers)")
        print(f"  (OA=false/unknown + academic-retained + >200 lines)")
        print(f"{'='*60}")
        for r in copyright_risk:
            print(f"  [{str(r['open_access']).lower()}] {Path(r['filepath']).name}  ({r['line_count']} lines)")

    # Ambiguity
    ambiguous = [r for r in valid if r["ambiguity_flag"]]
    if ambiguous:
        print(f"\n{'='*60}")
        print(f"  AMBIGUOUS FORMAT ({len(ambiguous)} papers)")
        print(f"  (narrative with 5+ headings - needs manual review)")
        print(f"{'='*60}")
        for r in ambiguous:
            print(f"  {Path(r['filepath']).name}  (flag: {r['ambiguity_flag']})")


    # Publisher gaps
    pub_gaps = [r for r in valid if r["doi"] and not r["publisher"]]
    if pub_gaps:
        print(f"\n{'='*60}")
        print(f"  PUBLISHER GAPS ({len(pub_gaps)} papers)")
        print(f"  (have DOI but no publisher match)")
        print(f"{'='*60}")
        for r in pub_gaps:
            doi_prefix = r["doi"].split("/")[0] if r["doi"] else "?"
            print(f"  {Path(r['filepath']).name}  (DOI prefix: {doi_prefix})")

    if errors:
        print(f"\n{'='*60}")
        print(f"  PARSE ERRORS ({len(errors)})")
        print(f"{'='*60}")
        for r in errors:
            print(f"  {r['filepath']}: {r['error']}")

    print()


# ══════════════════════════════════════════
# CLI ENTRYPOINT
# ══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="IbogaineVault Metadata Population Script")
    parser.add_argument("--vault", type=str,
                        default="/Users/aretesofia/IbogaineVault",
                        help="Path to vault root")
    parser.add_argument("--apply", action="store_true",
                        help="Actually modify files (default: dry-run)")
    parser.add_argument("--report", action="store_true",
                        help="Generate CSV report")
    args = parser.parse_args()

    vault_root = detect_vault_root(args.vault)
    if not args.apply:
        print("DRY RUN - no files will be modified. Use --apply to write changes.\n")

    paper_files = discover_paper_files(vault_root)
    print(f"Discovered {len(paper_files)} papers\n")

    results = []
    for filepath in paper_files:
        results.append(process_paper(filepath, apply=args.apply))

    print_summary(results)

    if args.report:
        report_path = vault_root / "_meta" / "tools" / "metadata_report.csv"
        write_report(results, report_path)
        print(f"Report written to: {report_path}\n")


if __name__ == "__main__":
    main()
