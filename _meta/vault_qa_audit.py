#!/usr/bin/env python3
"""
IbogaineVault QA Audit Script
===========================
Validates all paper markdown files for:
  - YAML schema compliance (required fields, valid enums, type checks)
  - Structural integrity (body sections, truncation detection)
  - Content completeness heuristics (file length, empty sections)
  - PDF conversion artefact detection (OCR, encoding, table corruption)
  - Wikilink syntax validation
  - RED paper priority flagging

Produces a risk-ranked markdown report.

Usage:
    python3 vault_qa_audit.py [vault_path]
    Default vault_path: /Users/aretesofia/IbogaineVault
"""

import os
import sys
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ── Configuration ──────────────────────────────────────────────────────────

VAULT_PATH = sys.argv[1] if len(sys.argv) > 1 else "/Users/aretesofia/IbogaineVault"

# Paper directories (year-based + special locations)
PAPER_DIRS = []
for item in os.listdir(VAULT_PATH):
    full = os.path.join(VAULT_PATH, item)
    if os.path.isdir(full) and re.match(r'^\d{4}$', item):
        PAPER_DIRS.append(full)
for special in ['Clinical_Guidelines', 'Primary_Sources', 'Other', 'Industry_Documents']:
    sd = os.path.join(VAULT_PATH, special)
    if os.path.isdir(sd):
        PAPER_DIRS.append(sd)

# ── Valid Enums (from schema_registry.yml) ─────────────────────────────────

VALID_CATEGORIES = {'RED', 'GREEN', 'ORANGE', 'BLUE', 'PURPLE', 'WHITE'}

VALID_EVIDENCE_LEVELS = {
    'rct', 'cohort', 'case-series', 'case-report', 'in-vitro',
    'preclinical', 'review', 'systematic-review', 'guideline',
    'observational', 'qualitative', 'journalism'
}

VALID_DOCUMENT_TYPES = {
    'clinical-trial', 'review', 'systematic-review', 'case-report',
    'case-series', 'guideline', 'in-vitro', 'preclinical', 'observational',
    'qualitative', 'commentary', 'book', 'book-chapter', 'thesis',
    'primary-source', 'research-article', 'conference-talk', 'educational',
    'interview-transcript', 'journalism', 'policy-report',
    'brief-communication', 'industry-report'
}

VALID_ROUTES = {
    'oral', 'intravenous', 'subcutaneous', 'intramuscular',
    'intraperitoneal', 'topical', 'not-specified', 'not-applicable'
}

VALID_CLINICAL_SIGNIFICANCE = {'low', 'moderate', 'high', 'landmark'}

VALID_TAGS = {
    'topic/18-mc', 'topic/adverse-event', 'topic/alcohol', 'topic/analogues',
    'topic/assessment', 'topic/benzodiazepine', 'topic/cardiac', 'topic/cognition',
    'topic/combination', 'topic/cyp2d6', 'topic/dopamine', 'topic/efficacy',
    'topic/electrolytes', 'topic/gdnf', 'topic/harm-reduction', 'topic/history',
    'topic/mechanism', 'topic/motor', 'topic/multiple-sclerosis', 'topic/neuroimaging',
    'topic/neuroplasticity', 'topic/noribogaine', 'topic/opioid', 'topic/parkinsons',
    'topic/pharmacokinetics', 'topic/phenomenology', 'topic/policy', 'topic/protocol',
    'topic/psychiatric', 'topic/ptsd', 'topic/receptor', 'topic/serotonin',
    'topic/sleep', 'topic/stimulant', 'topic/tbi', 'topic/toxicity',
    'topic/traditional-use', 'topic/veterans', 'topic/withdrawal',
    'mechanism/dopamine-modulation', 'mechanism/energy-metabolism',
    'mechanism/herg-blockade', 'mechanism/ion-channel', 'mechanism/kappa-opioid',
    'mechanism/mu-opioid', 'mechanism/nicotinic-receptor', 'mechanism/nmda-antagonism',
    'mechanism/sert-inhibition', 'mechanism/sigma-receptor',
    'method/case-report', 'method/case-series', 'method/clinical-trial',
    'method/in-vitro', 'method/journalism', 'method/observational',
    'method/preclinical', 'method/proteomics', 'method/qualitative',
    'method/review', 'method/systematic-review',
    'meta/hub', 'meta/moc'
}

# Document types that count as "synthesis" for tag count policy
SYNTHESIS_TYPES = {
    'review', 'systematic-review', 'thesis', 'guideline', 'primary-source',
    'conference-talk', 'educational', 'interview-transcript', 'commentary',
    'book', 'book-chapter', 'policy-report'
}

# Named exceptions for encyclopedic tag counts
ENCYCLOPEDIC_EXCEPTIONS = {'Alper2001': 16, 'Kobr2024': 14, 'Alfonso2023': 11}


# ── PDF Conversion Artefact Patterns ──────────────────────────────────────

# OCR / encoding corruption patterns
OCR_PATTERNS = [
    (re.compile(r'ﬁ|ﬂ|ﬃ|ﬄ|ﬅ|ﬆ'), 'ligature_artefact'),
    (re.compile(r'Ã©|Ã¨|Ã¼|Ã¶|Ã¤|Ã±|â€™|â€œ|â€\x9d|â€"'), 'utf8_mojibake'),
    (re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]'), 'control_characters'),
    (re.compile(r'[^\x00-\x7F]{5,}'), 'unicode_garbage_run'),  # 5+ non-ASCII in a row
    (re.compile(r'\(\s*\)'), 'empty_parentheses'),  # Known PDF stripping pattern
    (re.compile(r'\(\s*;\s*\)'), 'stripped_semicolon_content'),
    (re.compile(r'lg/mL'), 'corrupted_micro_prefix'),  # µg/mL → lg/mL
]

# Patterns suggesting table corruption
TABLE_CORRUPTION_PATTERNS = [
    (re.compile(r'\|[|\s]*\|[|\s]*\|'), 'empty_table_cells'),  # Multiple empty cells
    (re.compile(r'\|\s*\n\s*[^|]'), 'broken_table_row'),  # Table row that doesn't continue
]

# Duplicate content detection (same paragraph repeated)
DUPLICATE_THRESHOLD = 80  # characters - paragraphs longer than this checked for duplication

# Suspiciously short file thresholds by document type
MIN_LINES_BY_TYPE = {
    'review': 100,
    'systematic-review': 100,
    'thesis': 150,
    'book': 150,
    'book-chapter': 80,
    'clinical-trial': 80,
    'guideline': 80,
    'case-report': 50,
    'case-series': 60,
    'default': 40
}

# ── Helper Functions ──────────────────────────────────────────────────────

def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file. Returns (yaml_dict, body_text, errors)."""
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None, '', [f"FILE_READ_ERROR: {e}"]

    # Check for YAML delimiters
    if not content.startswith('---'):
        return None, content, ['YAML_MISSING: No opening --- delimiter']

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content, ['YAML_MALFORMED: No closing --- delimiter']

    yaml_text = parts[1]
    body = parts[2]

    # Check for blank line after opening ---
    if yaml_text.startswith('\n\n'):
        errors.append('YAML_BLANK_LINE: Blank line after opening ---')

    try:
        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            return None, body, ['YAML_PARSE_ERROR: Frontmatter is not a dict']
    except yaml.YAMLError as e:
        return None, body, [f'YAML_PARSE_ERROR: {e}']

    return data, body, errors


def check_yaml_schema(data, filepath):
    """Validate YAML fields against the paper schema. Returns list of issues."""
    issues = []
    fname = os.path.basename(filepath)

    # ── Required fields ──
    required = ['title', 'authors', 'year', 'category', 'tags', 'key_findings',
                'document_type', 'clinical_significance', 'aliases', 'source_pdf',
                'qtc_data', 'electrolyte_data', 'herg_data', 'contraindications',
                'evidence_level']
    for field in required:
        if field not in data:
            issues.append(f'MISSING_REQUIRED: {field}')

    if not issues or 'category' in data:  # Continue even with some missing fields
        cat = data.get('category')
        if cat and cat not in VALID_CATEGORIES:
            issues.append(f'INVALID_ENUM: category "{cat}" not in {VALID_CATEGORIES}')

    # ── Type checks ──
    if 'year' in data and not isinstance(data['year'], int):
        issues.append(f'TYPE_ERROR: year should be int, got {type(data["year"]).__name__}')

    if 'authors' in data:
        if not isinstance(data['authors'], list):
            issues.append('TYPE_ERROR: authors should be list')
        elif isinstance(data['authors'][0], dict):
            # Sometimes YAML parses "Surname, Given" as a dict
            issues.append('TYPE_ERROR: authors parsed as dict — check quoting')

    if 'tags' in data:
        if not isinstance(data['tags'], list):
            issues.append('FORMAT_ERROR: tags should be list format, not inline')
        else:
            for tag in data['tags']:
                if isinstance(tag, str) and tag.startswith('#'):
                    issues.append(f'TAG_FORMAT: tag "{tag}" has # prefix — remove it')
                if isinstance(tag, str) and tag not in VALID_TAGS:
                    issues.append(f'INVALID_TAG: "{tag}" not in canonical 62-tag taxonomy')

    # ── Enum validation ──
    ev = data.get('evidence_level')
    if ev and str(ev) not in VALID_EVIDENCE_LEVELS:
        issues.append(f'INVALID_ENUM: evidence_level "{ev}" not valid')

    dt = data.get('document_type')
    if dt and str(dt) not in VALID_DOCUMENT_TYPES:
        issues.append(f'INVALID_ENUM: document_type "{dt}" not valid')

    cs = data.get('clinical_significance')
    if cs and str(cs) not in VALID_CLINICAL_SIGNIFICANCE:
        issues.append(f'INVALID_ENUM: clinical_significance "{cs}" not valid')

    route = data.get('route')
    if route and str(route) not in VALID_ROUTES:
        issues.append(f'INVALID_ENUM: route "{route}" not valid')

    sc = data.get('secondary_categories')
    if sc:
        if isinstance(sc, list):
            for s in sc:
                if str(s) not in VALID_CATEGORIES:
                    issues.append(f'INVALID_ENUM: secondary_category "{s}" not valid')
        # Check inline array format (common YAML gotcha)
        elif isinstance(sc, str):
            issues.append('FORMAT_ERROR: secondary_categories should be list, not string')

    # ── Boolean checks ──
    for bf in ['qtc_data', 'electrolyte_data', 'herg_data']:
        val = data.get(bf)
        if val is not None and not isinstance(val, bool):
            issues.append(f'TYPE_ERROR: {bf} should be boolean, got {type(val).__name__} "{val}"')

    # ── key_findings length ──
    kf = data.get('key_findings', '')
    if isinstance(kf, str) and len(kf) > 250:
        issues.append(f'LENGTH: key_findings is {len(kf)} chars (max 250)')

    # ── Contraindications: must be list (can be empty []) ──
    ci = data.get('contraindications')
    if ci is not None and not isinstance(ci, list):
        issues.append(f'TYPE_ERROR: contraindications should be list, got {type(ci).__name__}')

    # ── aliases: minimum 2 ──
    aliases = data.get('aliases')
    if aliases is not None:
        if not isinstance(aliases, list):
            issues.append('TYPE_ERROR: aliases should be list')
        elif len(aliases) < 2:
            issues.append(f'INSUFFICIENT: aliases has {len(aliases)} entries (min 2)')

    # ── Tag count policy ──
    tags = data.get('tags', [])
    if isinstance(tags, list) and dt:
        tag_count = len(tags)
        # Check named exceptions
        stem = os.path.splitext(fname)[0]
        is_exception = any(stem.startswith(exc) for exc in ENCYCLOPEDIC_EXCEPTIONS)
        if not is_exception:
            if str(dt) in SYNTHESIS_TYPES:
                if tag_count > 12:  # 10 + 2 tolerance
                    issues.append(f'TAG_COUNT: {tag_count} tags for synthesis doc (max ~10)')
            else:
                if tag_count > 7:  # 5 + 2 tolerance
                    issues.append(f'TAG_COUNT: {tag_count} tags for empirical doc (max ~5)')

    # ── Category-specific mandatory fields ──
    cat = data.get('category')
    if cat == 'RED':
        if 'dosing_range' not in data:
            issues.append('RED_MANDATORY: dosing_range missing (required even for unknowns)')
        if 'route' not in data:
            issues.append('RED_MANDATORY: route missing')
    if cat == 'GREEN':
        if 'dosing_range' not in data:
            issues.append('GREEN_MANDATORY: dosing_range missing')
        if 'route' not in data:
            issues.append('GREEN_MANDATORY: route missing')

    # ── Semantic field omission checks ──
    if data.get('mortality_count') == 0:
        issues.append('SEMANTIC: mortality_count is 0 — should be omitted if no deaths')
    if data.get('sample_size') == 0:
        issues.append('SEMANTIC: sample_size is 0 — should be omitted if not a human study')
    if data.get('doi') == '':
        issues.append('SEMANTIC: doi is empty string — should be omitted entirely')
    if data.get('journal') == '':
        issues.append('SEMANTIC: journal is empty string — should be omitted entirely')

    # ── research-article warning ──
    if dt == 'research-article':
        issues.append('NONSPECIFIC: document_type is "research-article" — should be disambiguated')

    return issues
