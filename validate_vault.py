#!/usr/bin/env python3
"""
IbogaineVault Unified Validation Script
========================================
Comprehensive integrity checking for the IbogaineVault research knowledge base.
Auto-detects vault root. Works from working vault or Tier 1 clone.

CHECK TYPES:
  [x] 1. YAML schema validation    — fields, enums, types, tag policy
  [x] 2. Wikilink resolution       — all [[links]] resolve to existing files
  [x] 3. Duplicate DOI detection    — no two papers share a DOI
  [x] 4. OCR artefact detection     — broken ligatures, misread chars, orphaned unicode

OUTPUT: Summary to stdout + optional JSON (--json). Exit code 0 if pass, 1 if failures.

USAGE:
  python3 validate_vault.py                     # Full report (fast checks only)
  python3 validate_vault.py --summary           # Summary only
  python3 validate_vault.py --json              # Machine-readable JSON
  python3 validate_vault.py --file path.md      # Single file
  python3 validate_vault.py --vault /path/to/vault  # Explicit vault root
  python3 validate_vault.py --pedantic          # Include noisy OCR checks (l→I)

Created: 2026-03-12 (Phase 2A — supersedes validate_yaml.py)
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# ══════════════════════════════════════════
# VAULT DETECTION
# ══════════════════════════════════════════

VAULT_MARKERS = ["_meta/schema_registry.yml", "HOME.md", "Hubs"]

def detect_vault_root(explicit_path=None):
    """Auto-detect vault root by walking up from CWD or script location.
    Looks for schema_registry.yml, HOME.md, or Hubs/ as markers.
    Returns Path or exits with error."""
    if explicit_path:
        p = Path(explicit_path)
        if p.exists() and any((p / m).exists() for m in VAULT_MARKERS):
            return p
        print(f"ERROR: {explicit_path} does not look like a vault root.", file=sys.stderr)
        sys.exit(1)

    # Try CWD, then parent dirs, then script location
    candidates = [Path.cwd()]
    candidates += list(Path.cwd().parents)
    candidates.append(Path(__file__).resolve().parent.parent.parent)  # _meta/tools/ -> vault

    for candidate in candidates:
        if any((candidate / m).exists() for m in VAULT_MARKERS):
            return candidate

    print("ERROR: Cannot detect vault root. Use --vault /path/to/vault.", file=sys.stderr)
    sys.exit(1)


# ══════════════════════════════════════════
# CANONICAL ENUMS (from schema_registry.yml)
# ══════════════════════════════════════════
# These are hardcoded for zero-dependency operation.
# If schema_registry.yml changes, update these sets.

VALID_CATEGORIES = {"RED", "GREEN", "ORANGE", "BLUE", "PURPLE", "WHITE"}

VALID_CLINICAL_SIGNIFICANCE = {"low", "moderate", "high", "landmark"}

VALID_EVIDENCE_LEVELS = {
    "rct", "cohort", "case-series", "case-report", "in-vitro",
    "preclinical", "review", "systematic-review", "guideline",
    "observational", "qualitative", "journalism", "primary-source",
}

VALID_ROUTES = {
    "oral", "intravenous", "subcutaneous", "intramuscular",
    "intraperitoneal", "topical", "not-specified", "not-applicable",
}

VALID_DOCUMENT_TYPES_PAPER = {
    "clinical-trial", "review", "systematic-review", "case-report",
    "case-series", "guideline", "in-vitro", "preclinical",
    "observational", "qualitative", "commentary", "book",
    "book-chapter", "thesis", "primary-source", "research-article",
    "conference-talk", "educational", "interview-transcript", "journalism",
    "policy-report", "brief-communication", "industry-report",
}

VALID_SCOPES = {"published"}

VALID_OPEN_ACCESS = {"true", "false", "unknown"}

VALID_BODY_FORMATS = {"vault-analytical", "academic-retained", "hybrid", "narrative"}

VALID_LICENCE_TYPES = {
    "all-rights-reserved", "unknown",
    "cc-by-nc-nd", "cc-by-nd", "cc-by-nc-sa", "cc-by-nc",
    "cc-by-sa", "cc-by",
}

VALID_MORTALITY_SCOPES = {"cumulative-review", "discrete-cases", "incidental"}

# ── Canonical tags (62 total) ──
VALID_TAGS = {
    # topic/ (39)
    "topic/18-mc", "topic/adverse-event", "topic/alcohol", "topic/analogues",
    "topic/assessment", "topic/benzodiazepine", "topic/cardiac", "topic/cognition",
    "topic/combination", "topic/cyp2d6", "topic/dopamine", "topic/efficacy",
    "topic/electrolytes", "topic/gdnf", "topic/harm-reduction", "topic/history",
    "topic/mechanism", "topic/motor", "topic/multiple-sclerosis", "topic/neuroimaging",
    "topic/neuroplasticity", "topic/noribogaine", "topic/opioid", "topic/parkinsons",
    "topic/pharmacokinetics", "topic/phenomenology", "topic/policy", "topic/protocol",
    "topic/psychiatric", "topic/ptsd", "topic/receptor", "topic/serotonin",
    "topic/sleep", "topic/stimulant", "topic/tbi", "topic/toxicity",
    "topic/traditional-use", "topic/veterans", "topic/withdrawal",
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
    # meta/ (2)
    "meta/hub", "meta/moc",
}

META_ONLY_TAGS = {"meta/hub", "meta/moc"}

# ── Field definitions ──
REQUIRED_FIELDS = [
    "title", "authors", "year", "category", "tags", "key_findings",
    "document_type", "clinical_significance", "aliases", "source_pdf",
    "qtc_data", "electrolyte_data", "herg_data", "contraindications",
    "evidence_level",
]

FORBIDDEN_PAPER_FIELDS = {"scope", "participants", "key_decisions", "action_items"}

ALL_VALID_PAPER_FIELDS = {
    "title", "authors", "year", "category", "tags", "key_findings",
    "document_type", "clinical_significance", "aliases", "source_pdf",
    "qtc_data", "electrolyte_data", "herg_data", "contraindications",
    "evidence_level", "dosing_range", "route", "sample_size",
    "mortality_count", "doi", "journal", "publication_date",
    "secondary_categories", "organisation", "scope",
    "source_event", "peer_reviewed", "volume", "pages",
    "supervisor", "institution", "publisher", "source_url", "language",
    "original_title", "notes", "conference", "source_url",
    "conference_location", "book_title", "book_editors", "issn",
    "pmid", "pmcid", "isbn",
    "open_access", "body_format",
    "licence_type", "licence_verified",
    "mortality_scope",
    "references_stripped",
}

BOOLEAN_FIELDS = {"qtc_data", "electrolyte_data", "herg_data"}

SYNTHESIS_DOC_TYPES = {
    "review", "systematic-review", "thesis", "guideline", "primary-source",
    "conference-talk", "educational", "interview-transcript", "commentary",
    "book", "book-chapter", "policy-report", "journalism", "industry-report",
}
STANDARD_TAG_MAX = 5
SYNTHESIS_TAG_MAX = 10

ENCYCLOPEDIC_EXCEPTIONS = {
    "Alper2001": 16, "Kobr2024": 14, "Alfonso2023": 11, "GITA2015": 13,
}

# ── OCR artefact patterns (Check 4) ──
OCR_PATTERNS = [
    # Broken ligatures
    (r'(?<![a-zA-Z])ﬁ(?![a-zA-Z])', "broken ligature: ﬁ (should be fi)"),
    (r'(?<![a-zA-Z])ﬂ(?![a-zA-Z])', "broken ligature: ﬂ (should be fl)"),
    (r'(?<![a-zA-Z])ﬀ(?![a-zA-Z])', "broken ligature: ﬀ (should be ff)"),
    (r'(?<![a-zA-Z])ﬃ(?![a-zA-Z])', "broken ligature: ﬃ (should be ffi)"),
    (r'(?<![a-zA-Z])ﬄ(?![a-zA-Z])', "broken ligature: ﬄ (should be ffl)"),
    # Also catch them mid-word (more common in OCR text)
    (r'\w+ﬁ\w*|\w*ﬁ\w+', "broken ligature ﬁ in word"),
    (r'\w+ﬂ\w*|\w*ﬂ\w+', "broken ligature ﬂ in word"),
    (r'\w+ﬀ\w*|\w*ﬀ\w+', "broken ligature ﬀ in word"),
    # Orphaned Unicode
    (r'[\ufb00-\ufb06]', "Unicode ligature character (FB00-FB06 range)"),
    (r'[\x00-\x08\x0b\x0c\x0e-\x1f]', "control character in text"),
    # Repeated word fragments (OCR stutter)
    (r'\b(\w{3,})\s+\1\b', "repeated word (possible OCR stutter)"),
]

# Pedantic-only patterns (high false-positive rate in scientific text; run with --pedantic)
PEDANTIC_OCR_PATTERNS = [
    (r'(?<=[a-z])l(?=[A-Z])', "suspicious l→I transition (possible OCR: lowercase-L for uppercase-I)"),
]

# Compile for performance
OCR_COMPILED = [(re.compile(pat), desc) for pat, desc in OCR_PATTERNS]
PEDANTIC_OCR_COMPILED = [(re.compile(pat), desc) for pat, desc in PEDANTIC_OCR_PATTERNS]

# ── Category-to-hub mapping (for future Check 5) ──
CATEGORY_HUB_MAP = {
    "RED": "Hubs/RED_Cardiac_Safety_Hub.md",
    "GREEN": "Hubs/GREEN_Clinical_Protocols_Hub.md",
    "ORANGE": "Hubs/ORANGE_Mechanisms_Hub.md",
    "BLUE": "Hubs/BLUE_Outcomes_Hub.md",
    "PURPLE": "Hubs/PURPLE_Phenomenology_Hub.md",
    "WHITE": "Hubs/WHITE_Historical_Hub.md",
}

# ── Known shared DOIs (proceedings volumes with multiple abstracts) ──
# These are legitimate duplicates: distinct abstracts sharing a proceedings-volume DOI.
SHARED_DOI_ALLOWLIST = {
    "10.3109/15563650.2012.700015",  # NACCT 2012 proceedings: Shawn2012 (#180) + Warrick2012 (#184)
}


# ══════════════════════════════════════════
# VIOLATION FRAMEWORK
# ══════════════════════════════════════════

class Violation:
    """Single validation violation with check-type provenance."""
    def __init__(self, field, vtype, message, severity="error", check="yaml"):
        self.field = field
        self.vtype = vtype
        self.message = message
        self.severity = severity  # "error" or "warning"
        self.check = check        # "yaml", "wikilink", "doi", "ocr"

    def __repr__(self):
        icon = "❌" if self.severity == "error" else "⚠️"
        return f"  {icon} [{self.check}:{self.vtype}] {self.field}: {self.message}"

    def to_dict(self):
        return {
            "field": self.field, "type": self.vtype,
            "message": self.message, "severity": self.severity,
            "check": self.check,
        }


# ══════════════════════════════════════════
# YAML PARSING
# ══════════════════════════════════════════

def extract_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file.
    Returns (dict, raw_yaml_text, body_text, list_of_parse_errors).
    body_text is everything after the closing ---."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return None, "", "", [f"Cannot read file: {e}"]

    if not content.startswith("---"):
        return None, "", content, ["No YAML frontmatter (file doesn't start with ---)"]

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        end_match = re.search(r'\n---\s*$', content[3:])
        if not end_match:
            return None, "", content, ["No closing --- delimiter"]

    yaml_text = content[3:3 + end_match.start()]
    body_text = content[3 + end_match.end():]

    # Try PyYAML first, fall back to manual
    try:
        import yaml
        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            return None, yaml_text, body_text, ["YAML doesn't parse as dict"]
        return data, yaml_text, body_text, []
    except ImportError:
        pass
    except Exception as e:
        return None, yaml_text, body_text, [f"YAML parse error: {e}"]

    data, errors = _parse_yaml_manual(yaml_text)
    return data, yaml_text, body_text, errors

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
# FILE DISCOVERY
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


def discover_all_md_files(vault_root):
    """Find ALL .md files in the vault (for wikilink index).
    Excludes .obsidian/, .copilot-index/, .smart-env/, .git/."""
    vault = Path(vault_root)
    skip_dirs = {".obsidian", ".copilot-index", ".smart-env",
                 ".git", ".local", "node_modules"}

    all_files = []
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if f.endswith(".md"):
                all_files.append(Path(root) / f)
    return all_files


# ══════════════════════════════════════════
# CHECK 1: YAML SCHEMA VALIDATION
# ══════════════════════════════════════════

def get_paper_id(filepath):
    """Extract paper identifier from filename (e.g., 'Cherian2024')."""
    stem = Path(filepath).stem
    match = re.match(r'^([A-Za-z]+\d{4})', stem)
    return match.group(1) if match else stem


def validate_paper(filepath, data):
    """Check 1: Validate a single paper's YAML against the schema.
    Returns list of Violations."""
    violations = []
    paper_id = get_paper_id(filepath)

    # ── 1. Required fields ──
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] is None:
            violations.append(Violation(field, "missing_required",
                "Required field missing"))

    # ── 2. Forbidden fields ──
    doc_type = data.get("document_type", "")
    is_transcript_published = doc_type in ("conference-talk", "interview-transcript")
    # Detect transcript_published schema: Primary_Sources/ files use scope
    is_primary_source = "Primary_Sources/" in str(filepath) or "/Primary_Sources/" in str(filepath)
    for field in FORBIDDEN_PAPER_FIELDS:
        if field in data:
            if field == "scope" and (is_transcript_published or is_primary_source):
                continue
            violations.append(Violation(field, "forbidden_field",
                f"Field '{field}' is forbidden on papers"))

    # ── 3. Unknown/misspelled fields ──
    for field in data:
        if field not in ALL_VALID_PAPER_FIELDS:
            violations.append(Violation(field, "unknown_field",
                "Unrecognised field — possible typo or deprecated name",
                severity="warning"))

    # ── 4. Enum validation ──
    cat = data.get("category")
    if cat and cat not in VALID_CATEGORIES:
        violations.append(Violation("category", "invalid_enum",
            f"'{cat}' not in {sorted(VALID_CATEGORIES)}"))

    cs = data.get("clinical_significance")
    if cs is not None:
        cs_str = str(cs).lower().strip('"').strip("'")
        if cs_str not in VALID_CLINICAL_SIGNIFICANCE:
            violations.append(Violation("clinical_significance", "invalid_enum",
                f"'{cs}' not in {sorted(VALID_CLINICAL_SIGNIFICANCE)}"))

    el = data.get("evidence_level")
    if el and str(el) not in VALID_EVIDENCE_LEVELS:
        violations.append(Violation("evidence_level", "invalid_enum",
            f"'{el}' not in {sorted(VALID_EVIDENCE_LEVELS)}"))

    dt = data.get("document_type")
    if dt and str(dt) not in VALID_DOCUMENT_TYPES_PAPER:
        violations.append(Violation("document_type", "invalid_enum",
            f"'{dt}' not in valid document types"))

    route = data.get("route")
    if route and str(route) not in VALID_ROUTES:
        violations.append(Violation("route", "invalid_enum",
            f"'{route}' not in {sorted(VALID_ROUTES)}"))

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

    scope = data.get("scope")
    if scope and str(scope) not in VALID_SCOPES:
        violations.append(Violation("scope", "invalid_enum",
            f"'{scope}' not in {sorted(VALID_SCOPES)}"))

    # open_access: YAML boolean coercion — true/false parsed as Python bool
    oa = data.get("open_access")
    if oa is not None:
        oa_str = str(oa).lower()
        if oa_str not in VALID_OPEN_ACCESS:
            violations.append(Violation("open_access", "invalid_enum",
                f"'{oa}' not in {sorted(VALID_OPEN_ACCESS)}"))

    bf = data.get("body_format")
    if bf is not None and str(bf) not in VALID_BODY_FORMATS:
        violations.append(Violation("body_format", "invalid_enum",
            f"'{bf}' not in {sorted(VALID_BODY_FORMATS)}"))

    # licence_type: enum check + missing warning (D18)
    lt = data.get("licence_type")
    if lt is not None and str(lt) not in VALID_LICENCE_TYPES:
        violations.append(Violation("licence_type", "invalid_enum",
            f"'{lt}' not in {sorted(VALID_LICENCE_TYPES)}"))
    if lt is None:
        violations.append(Violation("licence_type", "missing_licence",
            "licence_type not set — run licence workflow (D18)",
            severity="warning"))

    # licence_verified: type check + missing warning (D18)
    lv = data.get("licence_verified")
    if lv is not None and not isinstance(lv, bool):
        violations.append(Violation("licence_verified", "type_error",
            f"Must be boolean (true/false), got: {type(lv).__name__} '{lv}'"))
    if lt is not None and lv is None:
        violations.append(Violation("licence_verified", "missing_licence_verified",
            "licence_type is set but licence_verified is missing",
            severity="warning"))

    # references_stripped: optional boolean check (D19)
    rs = data.get("references_stripped")
    if rs is not None and not isinstance(rs, bool):
        violations.append(Violation("references_stripped", "type_error",
            f"Must be boolean (true/false), got: {type(rs).__name__} '{rs}'"))

    # mortality_scope: enum check (Track 0b)
    ms = data.get("mortality_scope")
    if ms is not None and str(ms) not in VALID_MORTALITY_SCOPES:
        violations.append(Violation("mortality_scope", "invalid_enum",
            f"'{ms}' not in {sorted(VALID_MORTALITY_SCOPES)}"))

    # mortality_scope ↔ mortality_count cross-field checks
    mc = data.get("mortality_count")
    if mc is not None and isinstance(mc, int) and mc > 0 and ms is None:
        violations.append(Violation("mortality_scope", "missing_mortality_scope",
            "mortality_count > 0 but mortality_scope not set — classify as cumulative-review, discrete-cases, or incidental",
            severity="warning"))
    if ms is not None and (mc is None or (isinstance(mc, int) and mc == 0)):
        violations.append(Violation("mortality_scope", "orphan_mortality_scope",
            "mortality_scope set but mortality_count is null/0 — field should only exist when deaths are reported"))

    # ── 5. Tag validation ──
    tags = data.get("tags", [])
    if isinstance(tags, list):
        for tag in tags:
            tag_str = str(tag).strip()
            if tag_str.startswith("#"):
                violations.append(Violation("tags", "tag_format",
                    f"Tag '{tag_str}' has # prefix — should be bare"))
                tag_str = tag_str[1:]
            if tag_str not in VALID_TAGS:
                violations.append(Violation("tags", "invalid_tag",
                    f"'{tag_str}' not in canonical 62-tag set"))
            if tag_str in META_ONLY_TAGS:
                violations.append(Violation("tags", "meta_tag_on_paper",
                    f"'{tag_str}' is meta-only — shouldn't appear on research papers",
                    severity="warning"))

        tag_count = len(tags)
        if tag_count < 2:
            violations.append(Violation("tags", "too_few_tags",
                f"Minimum 2 tags required, found {tag_count}"))

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
                    f"{policy} policy max is {max_tags}, found {tag_count}"))
            elif tag_count > max_tags:
                violations.append(Violation("tags", "tag_count_at_limit",
                    f"{policy} policy max is {max_tags}, found {tag_count}",
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
    year = data.get("year")
    if year is not None and not isinstance(year, int):
        violations.append(Violation("year", "type_error",
            f"Must be integer, got: {type(year).__name__} '{year}'"))

    authors = data.get("authors")
    if authors is not None and not isinstance(authors, list):
        violations.append(Violation("authors", "type_error", "Must be a list of strings"))

    aliases = data.get("aliases")
    if aliases is not None:
        if not isinstance(aliases, list):
            violations.append(Violation("aliases", "type_error", "Must be a list"))
        elif len(aliases) < 2:
            violations.append(Violation("aliases", "too_few_aliases",
                f"Minimum 2 aliases required, found {len(aliases)}"))

    ci = data.get("contraindications")
    if ci is not None and not isinstance(ci, list):
        violations.append(Violation("contraindications", "type_error",
            "Must be a list (use [] for empty)"))

    ss = data.get("sample_size")
    if ss is not None:
        if not isinstance(ss, int):
            violations.append(Violation("sample_size", "type_error",
                f"Must be integer, got: {type(ss).__name__}"))
        elif ss == 0:
            violations.append(Violation("sample_size", "semantic_error",
                "sample_size: 0 should be omitted (0 implies 'studied 0 participants')"))

    mc = data.get("mortality_count")
    if mc is not None:
        if not isinstance(mc, int):
            violations.append(Violation("mortality_count", "type_error",
                f"Must be integer, got: {type(mc).__name__}"))
        elif mc == 0:
            violations.append(Violation("mortality_count", "semantic_error",
                "mortality_count: 0 should be omitted (0 implies 'analysed fatalities, found none')"))

    # ── 8. Empty string checks ──
    omit_if_unavailable = ["doi", "journal", "publication_date", "dosing_range",
                           "route", "organisation"]
    for field in omit_if_unavailable:
        val = data.get(field)
        if isinstance(val, str) and val.strip() == "":
            violations.append(Violation(field, "empty_string",
                "Should be omitted when unavailable, not set to empty string"))

    # ── 9. Category-specific mandatory fields ──
    if cat == "RED":
        if "dosing_range" not in data:
            violations.append(Violation("dosing_range", "category_required",
                "RED papers require dosing_range"))
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
            "'research-article' is non-specific — should be disambiguated",
            severity="warning"))

    return violations


# ══════════════════════════════════════════
# CHECK 2: WIKILINK RESOLUTION
# ══════════════════════════════════════════

def build_wikilink_index(vault_root):
    """Build a set of all resolvable wikilink targets (stem names + YAML aliases).
    In Obsidian, [[Target]] resolves to any file named Target.md OR any file
    with Target in its aliases: frontmatter field."""
    all_files = discover_all_md_files(vault_root)
    index = {}
    for f in all_files:
        stem = f.stem
        if stem in index:
            index[stem].append(f)
        else:
            index[stem] = [f]

        # Also index YAML aliases so [[AliasName]] resolves
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                head = fh.read(4096)  # aliases are always near the top
            if head.startswith('---'):
                # Inline array: aliases: ["a", "b"]
                m = re.search(r'^aliases:\s*\[(.+?)\]', head, re.MULTILINE)
                if m:
                    aliases = [a.strip().strip('"').strip("'")
                               for a in m.group(1).split(',')]
                else:
                    # Block array: aliases:\n  - "a"\n  - "b"
                    m = re.search(r'^aliases:\s*\n((?:\s+-\s+.+\n)*)', head, re.MULTILINE)
                    if m:
                        aliases = re.findall(r'-\s+"?(.+?)"?\s*$', m.group(1), re.MULTILINE)
                    else:
                        aliases = []
                for alias in aliases:
                    alias = alias.strip()
                    if alias and alias != stem:
                        if alias in index:
                            index[alias].append(f)
                        else:
                            index[alias] = [f]
        except Exception:
            pass  # skip files that can't be read

    return index


WIKILINK_RE = re.compile(r'\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|[^\]]+?)?\]\]')

def check_wikilinks(filepath, body_text, wikilink_index, vault_root):
    """Check 2: Find all [[wikilinks]] in body text and verify targets exist.
    Handles [[Target]], [[Target|Alias]], [[Target#Heading]], [[Path/Target]].
    Returns list of Violations."""
    violations = []
    lines = body_text.split('\n')

    for line_num, line in enumerate(lines, start=1):
        # Skip code blocks
        if line.strip().startswith('```'):
            continue

        for match in WIKILINK_RE.finditer(line):
            target = match.group(1).strip()
            if not target:
                continue

            # Handle path-style links: [[Folder/File]] -> resolve "File"
            if '/' in target:
                # Check if the full relative path resolves
                rel_path = Path(vault_root) / (target + ".md")
                if rel_path.exists():
                    continue
                # Fall back to stem-only resolution
                target = target.split('/')[-1]

            # Resolve against index (stem-based, case-sensitive)
            if target not in wikilink_index:
                violations.append(Violation(
                    "wikilink", "broken_link",
                    f"Line {line_num}: [[{target}]] — target not found",
                    severity="error", check="wikilink"))

    return violations


# ══════════════════════════════════════════
# CHECK 3: DUPLICATE DOI DETECTION
# ══════════════════════════════════════════

def check_duplicate_dois(all_paper_data):
    """Check 3: Scan all papers for DOI collisions.
    all_paper_data is dict of {filepath: {"data": dict, ...}}.
    Returns list of Violations attached to the second (and subsequent) occurrences."""
    doi_map = {}  # doi -> first filepath
    violations = []

    for filepath, result in all_paper_data.items():
        data = result.get("data")
        if not data:
            continue
        doi = data.get("doi")
        if not doi or not isinstance(doi, str):
            continue
        doi_clean = doi.strip().lower()
        if not doi_clean:
            continue

        if doi_clean in doi_map:
            if doi_clean in SHARED_DOI_ALLOWLIST:
                pass  # Known shared proceedings-volume DOI — not a true duplicate
            else:
                violations.append(Violation(
                    "doi", "duplicate_doi",
                    f"DOI '{doi}' also in {Path(doi_map[doi_clean]).name}",
                    severity="error", check="doi"))
                # Attach to this filepath
                result.setdefault("extra_violations", []).append(violations[-1])
        else:
            doi_map[doi_clean] = filepath

    return violations


# ══════════════════════════════════════════
# CHECK 4: OCR ARTEFACT DETECTION
# ══════════════════════════════════════════

def check_ocr_artefacts(filepath, yaml_text, body_text, pedantic=False):
    """Check 4: Scan YAML and body text for common OCR artefacts.
    Returns list of Violations."""
    violations = []
    full_text = yaml_text + "\n" + body_text
    lines = full_text.split('\n')

    for line_num, line in enumerate(lines, start=1):
        for pattern, description in OCR_COMPILED:
            matches = pattern.findall(line)
            if matches:
                # Deduplicate: report once per pattern per line
                sample = matches[0] if isinstance(matches[0], str) else str(matches[0])
                violations.append(Violation(
                    "text", "ocr_artefact",
                    f"Line {line_num}: {description} (found: '{sample[:30]}')",
                    severity="warning", check="ocr"))

    if pedantic:
        for line_num, line in enumerate(full_text.split('\n'), start=1):
            for pattern, description in PEDANTIC_OCR_COMPILED:
                matches = pattern.findall(line)
                if matches:
                    sample = matches[0] if isinstance(matches[0], str) else str(matches[0])
                    violations.append(Violation(
                        "text", "ocr_artefact_pedantic",
                        f"Line {line_num}: {description} (found: '{sample[:30]}')",
                        severity="warning", check="ocr"))

    return violations


# ══════════════════════════════════════════
# REPORT GENERATION
# ══════════════════════════════════════════

def generate_report(results, wikilink_stats, doi_dupes, vault_root, verbose=True):
    """Generate the unified validation report."""
    lines = []
    lines.append("=" * 70)
    lines.append("  IbogaineVault Unified Validation Report")
    lines.append(f"  Vault root: {vault_root}")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)
    lines.append("")

    total = len(results)
    # Merge extra_violations (from DOI dupes) into each result's violations
    for filepath, result in results.items():
        result["violations"].extend(result.get("extra_violations", []))

    compliant = sum(1 for r in results.values()
                    if not any(v.severity == "error" for v in r["violations"]))
    warnings_only = sum(1 for r in results.values()
                        if r["violations"]
                        and not any(v.severity == "error" for v in r["violations"]))
    errors_count = total - compliant
    parse_failures = sum(1 for r in results.values() if r["parse_error"])

    total_violations = sum(len(r["violations"]) for r in results.values())
    total_errors = sum(1 for r in results.values()
                       for v in r["violations"] if v.severity == "error")
    total_warnings = sum(1 for r in results.values()
                         for v in r["violations"] if v.severity == "warning")

    # ── Summary ──
    lines.append("── SUMMARY ──────────────────────────────────")
    lines.append(f"  Total papers scanned:     {total}")
    lines.append(f"  ✅ Fully compliant:       {compliant}")
    lines.append(f"  ⚠️  Warnings only:         {warnings_only}")
    lines.append(f"  ❌ With errors:           {errors_count}")
    lines.append(f"  💀 Parse failures:        {parse_failures}")
    lines.append(f"  Total violations:         {total_violations} ({total_errors} errors, {total_warnings} warnings)")
    if total:
        lines.append(f"  Compliance rate:          {compliant/total*100:.1f}%")
    lines.append("")

    # ── Check-specific summaries ──
    lines.append("── CHECK RESULTS ───────────────────────────")
    # Count by check type
    check_counts = defaultdict(lambda: {"error": 0, "warning": 0})
    for r in results.values():
        for v in r["violations"]:
            check_counts[v.check][v.severity] += 1

    for check_name in ["yaml", "wikilink", "doi", "ocr"]:
        c = check_counts.get(check_name, {"error": 0, "warning": 0})
        e, w = c.get("error", 0), c.get("warning", 0)
        status = "✅ PASS" if e == 0 else f"❌ {e} errors"
        if w > 0:
            status += f", {w} warnings"
        label = {"yaml": "YAML Schema", "wikilink": "Wikilink Resolution",
                 "doi": "Duplicate DOI", "ocr": "OCR Artefacts"}.get(check_name, check_name)
        lines.append(f"  {label}: {status}")

    # Wikilink stats
    if wikilink_stats:
        lines.append(f"\n  Wikilink index: {wikilink_stats['total_files']} files indexed, "
                     f"{wikilink_stats['total_links']} links scanned, "
                     f"{wikilink_stats['broken']} broken")

    if doi_dupes:
        lines.append(f"  Duplicate DOIs found: {len(doi_dupes)}")
    else:
        lines.append("  Duplicate DOIs: 0 (clean)")
    lines.append("")

    # ── Violations grouped by type ──
    by_type = defaultdict(list)
    for filepath, result in results.items():
        for v in result["violations"]:
            by_type[v.vtype].append((filepath, v))

    if by_type and verbose:
        lines.append("── VIOLATIONS BY TYPE ───────────────────────")
        for vtype in sorted(by_type, key=lambda t: (-len(by_type[t]), t)):
            items = by_type[vtype]
            sev_counts = defaultdict(int)
            for _, v in items:
                sev_counts[v.severity] += 1
            sev_str = ", ".join(f"{cnt} {sev}" for sev, cnt in sev_counts.items())
            lines.append(f"\n  {vtype} ({len(items)} — {sev_str})")
            for filepath, v in items[:15]:
                rel = Path(filepath).relative_to(vault_root)
                lines.append(f"    {rel}: {v.message}")
            if len(items) > 15:
                lines.append(f"    ... and {len(items) - 15} more")
        lines.append("")

    # ── Worst offenders ──
    worst = sorted(results.items(), key=lambda x: len(x[1]["violations"]), reverse=True)
    worst = [(f, r) for f, r in worst if r["violations"]]

    if worst and verbose:
        lines.append("── WORST OFFENDERS ─────────────────────────")
        for filepath, result in worst[:15]:
            rel = Path(filepath).relative_to(vault_root)
            err_count = sum(1 for v in result["violations"] if v.severity == "error")
            warn_count = sum(1 for v in result["violations"] if v.severity == "warning")
            lines.append(f"  {rel}: {err_count} errors, {warn_count} warnings")
            if verbose:
                for v in result["violations"]:
                    lines.append(f"  {v}")
        lines.append("")

    # ── Parse failures ──
    parse_fails = [(f, r) for f, r in results.items() if r["parse_error"]]
    if parse_fails:
        lines.append("── PARSE FAILURES ──────────────────────────")
        for filepath, result in parse_fails:
            rel = Path(filepath).relative_to(vault_root)
            lines.append(f"  {rel}: {result['parse_error']}")
        lines.append("")

    return "\n".join(lines)


# ══════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="IbogaineVault Unified Validation Script")
    parser.add_argument("--summary", action="store_true", help="Summary only")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--file", type=str, help="Validate single file")
    parser.add_argument("--vault", type=str, help="Explicit vault root path")
    parser.add_argument("--skip-wikilinks", action="store_true",
                        help="Skip wikilink resolution (faster)")
    parser.add_argument("--skip-ocr", action="store_true",
                        help="Skip OCR artefact detection")
    parser.add_argument("--pedantic", action="store_true",
                        help="Include high-false-positive checks (e.g. l→I OCR pattern)")
    args = parser.parse_args()

    vault_root = detect_vault_root(args.vault)
    print(f"Vault root: {vault_root}\n")

    # ── Discover papers ──
    if args.file:
        paper_files = [Path(args.file)]
    else:
        paper_files = discover_paper_files(vault_root)

    if not paper_files:
        print("No paper files found.")
        sys.exit(1)

    print(f"Scanning {len(paper_files)} papers...\n")

    # ── Check 1: YAML validation (per-file) ──
    results = {}
    for filepath in paper_files:
        data, yaml_text, body_text, parse_errors = extract_frontmatter(filepath)
        result = {
            "parse_error": parse_errors[0] if parse_errors else None,
            "violations": [],
            "data": data,
            "yaml_text": yaml_text,
            "body_text": body_text,
        }

        if data:
            result["violations"] = validate_paper(str(filepath), data)

            # ── Check 4: OCR artefacts (per-file) ──
            if not args.skip_ocr:
                result["violations"].extend(
                    check_ocr_artefacts(str(filepath), yaml_text, body_text, pedantic=args.pedantic))

        results[str(filepath)] = result

    # ── Check 2: Wikilink resolution (whole-vault) ──
    wikilink_stats = None
    if not args.skip_wikilinks and not args.file:
        print("Building wikilink index...")
        wl_index = build_wikilink_index(vault_root)
        wikilink_stats = {
            "total_files": sum(len(v) for v in wl_index.values()),
            "total_links": 0,
            "broken": 0,
        }

        for filepath, result in results.items():
            body = result.get("body_text", "")
            if body:
                wl_violations = check_wikilinks(filepath, body, wl_index, vault_root)
                result["violations"].extend(wl_violations)
                wikilink_stats["total_links"] += len(WIKILINK_RE.findall(body))
                wikilink_stats["broken"] += len(wl_violations)

        print(f"  {wikilink_stats['total_files']} files indexed, "
              f"{wikilink_stats['total_links']} links, "
              f"{wikilink_stats['broken']} broken\n")

    # ── Check 3: Duplicate DOI detection (whole-vault) ──
    doi_dupes = check_duplicate_dois(results)
    if doi_dupes:
        print(f"  ⚠ {len(doi_dupes)} duplicate DOI(s) found\n")
    else:
        print("  DOI uniqueness: clean\n")

    # ── Output ──
    if args.json:
        json_output = {}
        for filepath, result in results.items():
            rel = str(Path(filepath).relative_to(vault_root))
            json_output[rel] = {
                "parse_error": result["parse_error"],
                "violations": [v.to_dict() for v in result["violations"]],
                "data_preview": {
                    "category": result["data"].get("category") if result["data"] else None,
                    "document_type": result["data"].get("document_type") if result["data"] else None,
                    "year": result["data"].get("year") if result["data"] else None,
                },
            }
        print(json.dumps(json_output, indent=2))
    else:
        report = generate_report(results, wikilink_stats, doi_dupes,
                                 vault_root, verbose=not args.summary)
        print(report)

    # ── Exit code ──
    has_errors = any(
        any(v.severity == "error" for v in r["violations"])
        for r in results.values()
    )
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
