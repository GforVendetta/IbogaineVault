#!/usr/bin/env python3
"""
IbogaineVault YAML Validation Audit
=================================
Validates all paper .md files against the schema_registry.yml.

Checks:
  - Required fields present
  - Enum fields use valid values
  - Tags from canonical 62-tag set
  - No deprecated/misspelled field names
  - Boolean flags are actual booleans
  - Field omission rules (no empty strings, no zero for mortality/sample)
  - Tag count policy compliance
  - Conditional field requirements (category-specific)

Usage:
  python3 validate_yaml.py                    # Full report
  python3 validate_yaml.py --summary          # Summary only
  python3 validate_yaml.py --json             # JSON output
  python3 validate_yaml.py --file path.md     # Single file

Created: 2026-02-23
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# ──────────────────────────────────────────
# VAULT ROOT
# ──────────────────────────────────────────
VAULT_ROOT = Path("/Users/aretesofia/IbogaineVault")

# ──────────────────────────────────────────
# CANONICAL ENUMS (from schema_registry.yml)
# ──────────────────────────────────────────
VALID_CATEGORIES = {"RED", "GREEN", "ORANGE", "BLUE", "PURPLE", "WHITE"}

VALID_CLINICAL_SIGNIFICANCE = {"low", "moderate", "high", "landmark"}

VALID_EVIDENCE_LEVELS = {
    "rct", "cohort", "case-series", "case-report", "in-vitro",
    "preclinical", "review", "systematic-review", "guideline",
    "observational", "qualitative", "journalism", "primary-source"
}

VALID_ROUTES = {
    "oral", "intravenous", "subcutaneous", "intramuscular",
    "intraperitoneal", "topical", "not-specified", "not-applicable"
}

VALID_DOCUMENT_TYPES_PAPER = {
    "clinical-trial", "review", "systematic-review", "case-report",
    "case-series", "guideline", "in-vitro", "preclinical",
    "observational", "qualitative", "commentary", "book",
    "book-chapter", "thesis", "primary-source", "research-article",
    "conference-talk", "educational", "interview-transcript", "journalism",
    "policy-report", "brief-communication", "industry-report"
}

VALID_SCOPES = {"pangea", "published"}


# ──────────────────────────────────────────
# CANONICAL TAGS (62 total — from schema_registry.yml)
# ──────────────────────────────────────────
VALID_TAGS = {
    # topic/ (39)
    "topic/18-mc", "topic/adverse-event", "topic/alcohol", "topic/analogues",
    "topic/assessment", "topic/benzodiazepine", "topic/cardiac", "topic/cognition",
    "topic/combination",
    "topic/cyp2d6", "topic/dopamine", "topic/efficacy", "topic/electrolytes",
    "topic/gdnf", "topic/harm-reduction", "topic/history", "topic/mechanism",
    "topic/motor", "topic/multiple-sclerosis", "topic/neuroimaging",
    "topic/neuroplasticity", "topic/noribogaine", "topic/opioid",
    "topic/parkinsons", "topic/pharmacokinetics", "topic/phenomenology",
    "topic/policy", "topic/protocol", "topic/psychiatric", "topic/ptsd",
    "topic/receptor", "topic/serotonin", "topic/sleep", "topic/stimulant",
    "topic/tbi", "topic/toxicity", "topic/traditional-use", "topic/veterans",
    "topic/withdrawal",
    # mechanism/ (10)
    "mechanism/dopamine-modulation", "mechanism/energy-metabolism",
    "mechanism/herg-blockade", "mechanism/ion-channel", "mechanism/kappa-opioid",
    "mechanism/mu-opioid", "mechanism/nicotinic-receptor", "mechanism/nmda-antagonism",
    "mechanism/sert-inhibition", "mechanism/sigma-receptor",
    # method/ (11)
    "method/case-report", "method/case-series", "method/clinical-trial",
    "method/in-vitro", "method/journalism", "method/observational", "method/preclinical",
    "method/proteomics", "method/qualitative", "method/review",
    "method/systematic-review",
    # meta/ (2) — normally only on meta docs, flagged as warning on papers
    "meta/hub", "meta/moc",
}

VALID_TAGS_META = {"meta/hub", "meta/moc"}

# Tags that suggest a paper has been miscategorised if found on a research paper
META_ONLY_TAGS = {"meta/hub", "meta/moc"}


# ──────────────────────────────────────────
# REQUIRED FIELDS (all papers)
# ──────────────────────────────────────────
REQUIRED_FIELDS = [
    "title", "authors", "year", "category", "tags", "key_findings",
    "document_type", "clinical_significance", "aliases", "source_pdf",
    "qtc_data", "electrolyte_data", "herg_data", "contraindications",
    "evidence_level"
]

# Fields forbidden on papers
FORBIDDEN_PAPER_FIELDS = {"scope", "participants", "key_decisions", "action_items"}

# All valid paper fields (for detecting misspelled/deprecated fields)
ALL_VALID_PAPER_FIELDS = {
    "title", "authors", "year", "category", "tags", "key_findings",
    "document_type", "clinical_significance", "aliases", "source_pdf",
    "qtc_data", "electrolyte_data", "herg_data", "contraindications",
    "evidence_level", "dosing_range", "route", "sample_size",
    "mortality_count", "doi", "journal", "publication_date",
    "secondary_categories", "organisation",
    # transcript_published additions
    "scope",
    # Extended bibliographic fields (used on specific document types)
    "source_event", "peer_reviewed", "volume", "pages",
    "supervisor", "institution", "publisher", "source_url", "language",
    "original_title", "notes", "conference",
    "conference_location", "book_title", "book_editors", "issn",
    "pmid", "pmcid", "isbn",
}

# Boolean fields that must be actual booleans (true/false)
BOOLEAN_FIELDS = {"qtc_data", "electrolyte_data", "herg_data"}

# Tag count policy — document types that get higher limits
SYNTHESIS_DOC_TYPES = {
    "review", "systematic-review", "thesis", "guideline", "primary-source",
    "conference-talk", "educational", "interview-transcript", "commentary", "book",
    "book-chapter", "policy-report"
}
STANDARD_TAG_MAX = 5
SYNTHESIS_TAG_MAX = 10

# Named encyclopedic exceptions (paper -> allowed count)
ENCYCLOPEDIC_EXCEPTIONS = {
    "Alper2001": 16,
    "Kobr2024": 14,
    "Alfonso2023": 11,
}


# ──────────────────────────────────────────
# YAML PARSER (simple, no PyYAML dependency)
# ──────────────────────────────────────────
def extract_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file.
    Returns (dict, list_of_parse_errors) or (None, errors) if no frontmatter."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return None, [f"Cannot read file: {e}"]

    # Find frontmatter delimiters
    if not content.startswith("---"):
        return None, ["No YAML frontmatter found (file doesn't start with ---)"]

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        # Try end of file
        end_match = re.search(r'\n---\s*$', content[3:])
        if not end_match:
            return None, ["No closing --- delimiter for YAML frontmatter"]

    yaml_text = content[3:3 + end_match.start()]

    # Try PyYAML if available, otherwise fall back to manual parsing
    try:
        import yaml
        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            return None, ["YAML frontmatter doesn't parse as a dictionary"]
        return data, []
    except ImportError:
        pass
    except Exception as e:
        return None, [f"YAML parse error: {e}"]

    # Manual fallback parser (handles most common cases)
    return _parse_yaml_manual(yaml_text)


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

        # List item under current key
        if stripped.startswith('- ') and current_key:
            val = stripped[2:].strip().strip('"').strip("'")
            if current_list is None:
                current_list = []
            current_list.append(val)
            data[current_key] = current_list
            continue

        # Key-value pair
        match = re.match(r'^([a-z_]+)\s*:\s*(.*)', line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()

            # Save previous list
            current_key = key
            current_list = None

            if not value:
                # Empty value — might be followed by list items
                data[key] = None
                continue

            # Inline list: [item1, item2]
            if value.startswith('[') and value.endswith(']'):
                items = [v.strip().strip('"').strip("'") for v in value[1:-1].split(',')]
                data[key] = [x for x in items if x]
                current_list = data[key]
                continue

            # Boolean
            if value.lower() in ('true', 'false'):
                data[key] = value.lower() == 'true'
                continue

            # Integer
            try:
                data[key] = int(value)
                continue
            except ValueError:
                pass

            # String (strip quotes)
            data[key] = value.strip('"').strip("'")
        else:
            # Continuation or unknown line
            pass

    return data, errors


# ──────────────────────────────────────────
# VALIDATION LOGIC
# ──────────────────────────────────────────

class Violation:
    """Single validation violation."""
    def __init__(self, field, vtype, message, severity="error"):
        self.field = field
        self.vtype = vtype          # e.g. "missing_required", "invalid_enum", "invalid_tag"
        self.message = message
        self.severity = severity    # "error" or "warning"

    def __repr__(self):
        icon = "❌" if self.severity == "error" else "⚠️"
        return f"  {icon} [{self.vtype}] {self.field}: {self.message}"


def get_paper_id(filepath):
    """Extract paper identifier from filename (e.g., 'Cherian2024')."""
    stem = Path(filepath).stem
    # Match Author + Year pattern
    match = re.match(r'^([A-Za-z]+\d{4})', stem)
    return match.group(1) if match else stem


def validate_paper(filepath, data):
    """Validate a single paper's YAML against the schema. Returns list of Violations."""
    violations = []
    paper_id = get_paper_id(filepath)

    # ── 1. Required fields ──
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] is None:
            violations.append(Violation(field, "missing_required",
                f"Required field missing"))

    # ── 2. Forbidden fields ──
    # Check for forbidden fields (except scope, which is valid for transcript_published)
    doc_type = data.get("document_type", "")
    is_transcript_published = doc_type in ("conference-talk", "interview-transcript")

    for field in FORBIDDEN_PAPER_FIELDS:
        if field in data:
            if field == "scope" and is_transcript_published:
                continue  # scope is valid for published transcripts
            violations.append(Violation(field, "forbidden_field",
                f"Field '{field}' is forbidden on papers (schema says: paper-only forbidden)"))

    # ── 3. Unknown/misspelled fields ──
    valid_fields_for_this = ALL_VALID_PAPER_FIELDS.copy()
    for field in data:
        if field not in valid_fields_for_this:
            violations.append(Violation(field, "unknown_field",
                f"Unrecognised field — possible typo or deprecated name",
                severity="warning"))

    # ── 4. Enum validation ──
    # category
    cat = data.get("category")
    if cat and cat not in VALID_CATEGORIES:
        violations.append(Violation("category", "invalid_enum",
            f"'{cat}' not in {sorted(VALID_CATEGORIES)}"))

    # clinical_significance
    cs = data.get("clinical_significance")
    if cs is not None:
        cs_str = str(cs).lower().strip('"').strip("'")
        if cs_str not in VALID_CLINICAL_SIGNIFICANCE:
            violations.append(Violation("clinical_significance", "invalid_enum",
                f"'{cs}' not in {sorted(VALID_CLINICAL_SIGNIFICANCE)}"))

    # evidence_level
    el = data.get("evidence_level")
    if el and str(el) not in VALID_EVIDENCE_LEVELS:
        violations.append(Violation("evidence_level", "invalid_enum",
            f"'{el}' not in {sorted(VALID_EVIDENCE_LEVELS)}"))

    # document_type
    dt = data.get("document_type")
    if dt and str(dt) not in VALID_DOCUMENT_TYPES_PAPER:
        violations.append(Violation("document_type", "invalid_enum",
            f"'{dt}' not in valid document types"))

    # route
    route = data.get("route")
    if route and str(route) not in VALID_ROUTES:
        violations.append(Violation("route", "invalid_enum",
            f"'{route}' not in {sorted(VALID_ROUTES)}"))

    # secondary_categories
    sc = data.get("secondary_categories")
    if sc:
        if not isinstance(sc, list):
            violations.append(Violation("secondary_categories", "type_error",
                "Must be a list"))
        else:
            for v in sc:
                if v not in VALID_CATEGORIES:
                    violations.append(Violation("secondary_categories", "invalid_enum",
                        f"'{v}' not in {sorted(VALID_CATEGORIES)}"))

    # scope (if present on transcript_published)
    scope = data.get("scope")
    if scope and str(scope) not in VALID_SCOPES:
        violations.append(Violation("scope", "invalid_enum",
            f"'{scope}' not in {sorted(VALID_SCOPES)}"))

    # ── 5. Tag validation ──
    tags = data.get("tags", [])
    if isinstance(tags, list):
        for tag in tags:
            tag_str = str(tag).strip()
            # Strip accidental # prefix
            if tag_str.startswith("#"):
                violations.append(Violation("tags", "tag_format",
                    f"Tag '{tag_str}' has # prefix — should be bare (e.g., topic/cardiac)"))
                tag_str = tag_str[1:]
            if tag_str not in VALID_TAGS:
                violations.append(Violation("tags", "invalid_tag",
                    f"'{tag_str}' not in canonical 62-tag set"))
            if tag_str in META_ONLY_TAGS:
                violations.append(Violation("tags", "meta_tag_on_paper",
                    f"'{tag_str}' is meta-only — shouldn't appear on research papers",
                    severity="warning"))

        # Tag count policy
        tag_count = len(tags)
        if tag_count < 2:
            violations.append(Violation("tags", "too_few_tags",
                f"Minimum 2 tags required, found {tag_count}"))

        # Determine max allowed
        is_encyclopedic = False
        for exc_id, exc_max in ENCYCLOPEDIC_EXCEPTIONS.items():
            if exc_id in paper_id:
                is_encyclopedic = True
                if tag_count > exc_max:
                    violations.append(Violation("tags", "tag_count_exceeded",
                        f"Encyclopedic exception allows {exc_max}, found {tag_count}",
                        severity="warning"))
                break

        if not is_encyclopedic:
            if dt in SYNTHESIS_DOC_TYPES:
                max_tags = SYNTHESIS_TAG_MAX
                policy = "synthesis"
            else:
                max_tags = STANDARD_TAG_MAX
                policy = "standard"

            if tag_count > max_tags + 1:
                violations.append(Violation("tags", "tag_count_exceeded",
                    f"{policy} policy max is {max_tags}, found {tag_count} (exceeds limit+1 → needs review)"))
            elif tag_count > max_tags:
                violations.append(Violation("tags", "tag_count_at_limit",
                    f"{policy} policy max is {max_tags}, found {tag_count} (at limit+1 — acceptable if justified)",
                    severity="warning"))
    elif tags is not None:
        violations.append(Violation("tags", "type_error",
            "Tags must be a list, not a scalar"))

    # ── 6. Boolean field validation ──
    for bf in BOOLEAN_FIELDS:
        val = data.get(bf)
        if val is not None and not isinstance(val, bool):
            violations.append(Violation(bf, "type_error",
                f"Must be boolean (true/false), got: {type(val).__name__} '{val}'"))

    # ── 7. Type checks ──
    # year must be integer
    year = data.get("year")
    if year is not None and not isinstance(year, int):
        violations.append(Violation("year", "type_error",
            f"Must be integer, got: {type(year).__name__} '{year}'"))

    # authors must be list
    authors = data.get("authors")
    if authors is not None and not isinstance(authors, list):
        violations.append(Violation("authors", "type_error",
            "Must be a list of strings"))

    # aliases must be list with ≥2 items
    aliases = data.get("aliases")
    if aliases is not None:
        if not isinstance(aliases, list):
            violations.append(Violation("aliases", "type_error",
                "Must be a list of strings"))
        elif len(aliases) < 2:
            violations.append(Violation("aliases", "too_few_aliases",
                f"Minimum 2 aliases required, found {len(aliases)}"))

    # contraindications must be list (can be empty [])
    ci = data.get("contraindications")
    if ci is not None and not isinstance(ci, list):
        violations.append(Violation("contraindications", "type_error",
            "Must be a list (use [] for empty)"))

    # sample_size must be integer if present, not zero
    ss = data.get("sample_size")
    if ss is not None:
        if not isinstance(ss, int):
            violations.append(Violation("sample_size", "type_error",
                f"Must be integer, got: {type(ss).__name__}"))
        elif ss == 0:
            violations.append(Violation("sample_size", "semantic_error",
                "sample_size: 0 should be omitted — 0 implies 'studied 0 participants', omission means 'not a human study'"))

    # mortality_count must be integer if present, not zero
    mc = data.get("mortality_count")
    if mc is not None:
        if not isinstance(mc, int):
            violations.append(Violation("mortality_count", "type_error",
                f"Must be integer, got: {type(mc).__name__}"))
        elif mc == 0:
            violations.append(Violation("mortality_count", "semantic_error",
                "mortality_count: 0 should be omitted — 0 implies 'analysed fatalities, found none', omission means 'no fatality data'"))

    # ── 8. Empty string checks (fields that should be omitted, not empty) ──
    omit_if_unavailable = ["doi", "journal", "publication_date", "dosing_range", "route", "organisation"]
    for field in omit_if_unavailable:
        val = data.get(field)
        if isinstance(val, str) and val.strip() == "":
            violations.append(Violation(field, "empty_string",
                "Should be omitted entirely when unavailable, not set to empty string"))

    # ── 9. Category-specific mandatory fields ──
    if cat == "RED":
        if "dosing_range" not in data:
            violations.append(Violation("dosing_range", "category_required",
                "RED papers require dosing_range (even 'unknown — [context]')"))
        if "route" not in data:
            violations.append(Violation("route", "category_required",
                "RED papers require route"))
    elif cat == "GREEN":
        if "dosing_range" not in data:
            violations.append(Violation("dosing_range", "category_required",
                "GREEN papers require dosing_range (MANDATORY)"))
        if "route" not in data:
            violations.append(Violation("route", "category_required",
                "GREEN papers require route (MANDATORY)"))

    # ── 10. key_findings length check ──
    kf = data.get("key_findings")
    if isinstance(kf, str) and len(kf) > 250:
        violations.append(Violation("key_findings", "too_long",
            f"key_findings is {len(kf)} chars, max is 250"))

    # ── 11. research-article warning ──
    if dt == "research-article":
        violations.append(Violation("document_type", "non_specific_type",
            "'research-article' is valid but non-specific — should be disambiguated to a precise type",
            severity="warning"))

    return violations


# ──────────────────────────────────────────
# FILE DISCOVERY
# ──────────────────────────────────────────

def discover_paper_files(vault_root):
    """Find all .md files in paper locations (year-folders + special folders).
    Excludes meta docs, hubs, MOCs, Pangea_Ops."""
    paper_files = []
    vault = Path(vault_root)

    # Year folders (1957-2026)
    for entry in sorted(vault.iterdir()):
        if entry.is_dir() and re.match(r'^\d{4}$', entry.name):
            for md in sorted(entry.glob("*.md")):
                paper_files.append(md)

    # Special folders
    for folder_name in ["Clinical_Guidelines", "Primary_Sources", "Other"]:
        folder = vault / folder_name
        if folder.exists():
            for md in sorted(folder.glob("*.md")):
                paper_files.append(md)
            # Check one level deep (e.g., Clinical_Guidelines/Pangea/)
            for subdir in sorted(folder.iterdir()):
                if subdir.is_dir() and subdir.name != ".DS_Store":
                    for md in sorted(subdir.glob("*.md")):
                        paper_files.append(md)

    return paper_files


# ──────────────────────────────────────────
# REPORT GENERATION
# ──────────────────────────────────────────

def generate_report(results, verbose=True):
    """Generate the validation report."""
    lines = []
    lines.append("=" * 70)
    lines.append("  IbogaineVault YAML Validation Report")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)
    lines.append("")

    total = len(results)
    compliant = sum(1 for r in results.values()
                    if not any(v.severity == "error" for v in r["violations"]))
    warnings_only = sum(1 for r in results.values()
                        if r["violations"]
                        and not any(v.severity == "error" for v in r["violations"]))
    errors = total - compliant
    parse_failures = sum(1 for r in results.values() if r["parse_error"])

    total_violations = sum(len(r["violations"]) for r in results.values())
    total_errors = sum(1 for r in results.values()
                       for v in r["violations"] if v.severity == "error")
    total_warnings = sum(1 for r in results.values()
                         for v in r["violations"] if v.severity == "warning")

    # Summary
    lines.append("── SUMMARY ──────────────────────────────────")
    lines.append(f"  Total papers scanned:     {total}")
    lines.append(f"  ✅ Fully compliant:       {compliant}")
    lines.append(f"  ⚠️  Warnings only:         {warnings_only}")
    lines.append(f"  ❌ With errors:           {errors}")
    lines.append(f"  💀 Parse failures:        {parse_failures}")
    lines.append(f"  Total violations:         {total_violations} ({total_errors} errors, {total_warnings} warnings)")
    lines.append(f"  Compliance rate:          {compliant/total*100:.1f}%" if total else "  No papers found")
    lines.append("")

    # Violations grouped by type
    by_type = defaultdict(list)
    for filepath, result in results.items():
        for v in result["violations"]:
            by_type[v.vtype].append((filepath, v))

    if by_type:
        lines.append("── VIOLATIONS BY TYPE ───────────────────────")
        for vtype in sorted(by_type, key=lambda t: (-len(by_type[t]), t)):
            items = by_type[vtype]
            severity_counts = defaultdict(int)
            for _, v in items:
                severity_counts[v.severity] += 1
            sev_str = ", ".join(f"{cnt} {sev}" for sev, cnt in severity_counts.items())
            lines.append(f"\n  {vtype} ({len(items)} occurrences — {sev_str})")
            if verbose:
                for filepath, v in items[:15]:  # Cap at 15 examples per type
                    rel = Path(filepath).relative_to(VAULT_ROOT)
                    lines.append(f"    {rel}: {v.message}")
                if len(items) > 15:
                    lines.append(f"    ... and {len(items) - 15} more")
        lines.append("")

    # Worst offenders (papers with most violations)
    worst = sorted(results.items(), key=lambda x: len(x[1]["violations"]), reverse=True)
    worst = [(f, r) for f, r in worst if r["violations"]]

    if worst:
        lines.append("── WORST OFFENDERS ─────────────────────────")
        for filepath, result in worst[:15]:
            rel = Path(filepath).relative_to(VAULT_ROOT)
            err_count = sum(1 for v in result["violations"] if v.severity == "error")
            warn_count = sum(1 for v in result["violations"] if v.severity == "warning")
            lines.append(f"  {rel}: {err_count} errors, {warn_count} warnings")
            if verbose:
                for v in result["violations"]:
                    lines.append(f"  {v}")
        lines.append("")

    # Parse failures
    parse_fails = [(f, r) for f, r in results.items() if r["parse_error"]]
    if parse_fails:
        lines.append("── PARSE FAILURES ──────────────────────────")
        for filepath, result in parse_fails:
            rel = Path(filepath).relative_to(VAULT_ROOT)
            lines.append(f"  {rel}: {result['parse_error']}")
        lines.append("")

    # Compliant papers
    if verbose:
        compliant_list = [f for f, r in results.items()
                         if not any(v.severity == "error" for v in r["violations"])]
        if compliant_list:
            lines.append("── COMPLIANT PAPERS ────────────────────────")
            for filepath in compliant_list:
                rel = Path(filepath).relative_to(VAULT_ROOT)
                warn_count = sum(1 for v in results[filepath]["violations"]
                                if v.severity == "warning")
                suffix = f" ({warn_count} warnings)" if warn_count else ""
                lines.append(f"  ✅ {rel}{suffix}")
            lines.append("")

    return "\n".join(lines)


# ──────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="IbogaineVault YAML Validation Audit")
    parser.add_argument("--summary", action="store_true", help="Summary only (no per-paper details)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--file", type=str, help="Validate a single file")
    parser.add_argument("--vault", type=str, default=str(VAULT_ROOT), help="Vault root path")
    args = parser.parse_args()

    vault_root = Path(args.vault)

    if args.file:
        files = [Path(args.file)]
    else:
        files = discover_paper_files(vault_root)

    if not files:
        print("No paper files found.")
        sys.exit(1)

    print(f"Scanning {len(files)} files...\n")

    results = {}
    for filepath in files:
        data, parse_errors = extract_frontmatter(filepath)
        result = {
            "parse_error": parse_errors[0] if parse_errors else None,
            "violations": [],
            "data_preview": {}
        }

        if data:
            result["violations"] = validate_paper(str(filepath), data)
            result["data_preview"] = {
                "category": data.get("category"),
                "document_type": data.get("document_type"),
                "year": data.get("year"),
            }

        results[str(filepath)] = result

    if args.json:
        json_output = {}
        for filepath, result in results.items():
            rel = str(Path(filepath).relative_to(vault_root))
            json_output[rel] = {
                "parse_error": result["parse_error"],
                "violations": [
                    {"field": v.field, "type": v.vtype,
                     "message": v.message, "severity": v.severity}
                    for v in result["violations"]
                ],
                "data_preview": result["data_preview"]
            }
        print(json.dumps(json_output, indent=2))
    else:
        report = generate_report(results, verbose=not args.summary)
        print(report)


if __name__ == "__main__":
    main()
