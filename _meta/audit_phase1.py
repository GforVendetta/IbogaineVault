#!/usr/bin/env python3
"""
IbogaineVault — Phase 1 Automated Structural Audit
Scans all paper markdown files and flags potential conversion quality issues.
Outputs a ranked report: most problematic files first.
"""

import os
import re
import sys
import json
import yaml
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

VAULT_ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/Users/aretesofia/IbogaineVault")

# ── Directories containing papers ──
PAPER_DIRS = [
    # Year directories
    *[VAULT_ROOT / str(y) for y in range(1950, 2030)],
    VAULT_ROOT / "Clinical_Guidelines",
    VAULT_ROOT / "Primary_Sources",
    VAULT_ROOT / "Other",
    VAULT_ROOT / "Industry_Documents",
]

# ── Valid enums from schema_registry.yml ──
VALID_CATEGORIES = {"RED", "GREEN", "ORANGE", "BLUE", "PURPLE", "WHITE"}

VALID_EVIDENCE_LEVELS = {
    "rct", "cohort", "case-series", "case-report", "in-vitro", "preclinical",
    "review", "systematic-review", "guideline", "observational", "qualitative", "journalism"
}

VALID_DOCUMENT_TYPES = {
    "clinical-trial", "review", "systematic-review", "case-report", "case-series",
    "guideline", "in-vitro", "preclinical", "observational", "qualitative",
    "commentary", "book", "book-chapter", "thesis", "primary-source",
    "research-article", "conference-talk", "educational", "interview-transcript",
    "journalism", "policy-report", "brief-communication", "industry-report"
}

VALID_ROUTES = {
    "oral", "intravenous", "subcutaneous", "intramuscular", "intraperitoneal",
    "topical", "not-specified", "not-applicable"
}

VALID_CLINICAL_SIGNIFICANCE = {"low", "moderate", "high", "landmark"}

VALID_TAGS = {
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
    "mechanism/dopamine-modulation", "mechanism/energy-metabolism",
    "mechanism/herg-blockade", "mechanism/ion-channel", "mechanism/kappa-opioid",
    "mechanism/mu-opioid", "mechanism/nicotinic-receptor", "mechanism/nmda-antagonism",
    "mechanism/sert-inhibition", "mechanism/sigma-receptor",
    "method/case-report", "method/case-series", "method/clinical-trial",
    "method/in-vitro", "method/journalism", "method/observational",
    "method/preclinical", "method/proteomics", "method/qualitative",
    "method/review", "method/systematic-review",
}

# Synthesis types that allow up to 10 tags
SYNTHESIS_DOC_TYPES = {
    "review", "systematic-review", "thesis", "guideline", "primary-source",
    "conference-talk", "educational", "interview-transcript", "commentary",
    "book", "book-chapter", "policy-report"
}

# Encyclopedic exceptions
ENCYCLOPEDIC_EXCEPTIONS = {"Alper2001": 16, "Kobr2024": 14, "Alfonso2023": 11}


# ── Issue severity levels ──
CRITICAL = "CRITICAL"  # Likely broken / needs reconversion
HIGH = "HIGH"          # Significant quality issue
MEDIUM = "MEDIUM"      # Moderate concern
LOW = "LOW"            # Minor / cosmetic

class Issue:
    def __init__(self, severity, category, detail):
        self.severity = severity
        self.category = category
        self.detail = detail
    
    def __repr__(self):
        return f"[{self.severity}] {self.category}: {self.detail}"
    
    @property
    def score(self):
        return {CRITICAL: 100, HIGH: 50, MEDIUM: 20, LOW: 5}[self.severity]


def find_paper_files():
    """Find all .md files in paper directories."""
    files = []
    for d in PAPER_DIRS:
        if d.exists():
            for f in d.glob("*.md"):
                # Skip obvious non-paper files
                name = f.name.lower()
                if name.startswith(".") or name in ("readme.md",):
                    continue
                files.append(f)
    return sorted(files)


def split_yaml_body(content):
    """Split a markdown file into YAML frontmatter and body text."""
    if not content.startswith("---"):
        return None, content
    
    # Find closing ---
    end = content.find("\n---", 3)
    if end == -1:
        return None, content
    
    yaml_str = content[3:end].strip()
    body = content[end + 4:].strip()
    return yaml_str, body


def parse_yaml_safe(yaml_str):
    """Parse YAML frontmatter, returning dict or None on error."""
    try:
        return yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        return None



def check_yaml_schema(yaml_data, filename, issues):
    """Validate YAML frontmatter against the paper schema."""
    if yaml_data is None:
        issues.append(Issue(CRITICAL, "YAML", "Failed to parse YAML frontmatter"))
        return
    
    if not isinstance(yaml_data, dict):
        issues.append(Issue(CRITICAL, "YAML", f"YAML parsed as {type(yaml_data).__name__}, not dict"))
        return

    # ── Required fields ──
    required_fields = [
        "title", "authors", "year", "category", "tags", "key_findings",
        "document_type", "clinical_significance", "aliases", "source_pdf",
        "qtc_data", "electrolyte_data", "herg_data", "contraindications",
        "evidence_level"
    ]
    for field in required_fields:
        if field not in yaml_data:
            issues.append(Issue(HIGH, "YAML-missing", f"Required field missing: {field}"))
        elif yaml_data[field] is None:
            issues.append(Issue(HIGH, "YAML-null", f"Required field is null: {field}"))

    # ── Enum validations ──
    cat = yaml_data.get("category")
    if cat and cat not in VALID_CATEGORIES:
        issues.append(Issue(CRITICAL, "YAML-enum", f"Invalid category: '{cat}'"))
    
    ev = yaml_data.get("evidence_level")
    if ev and ev not in VALID_EVIDENCE_LEVELS:
        issues.append(Issue(HIGH, "YAML-enum", f"Invalid evidence_level: '{ev}'"))
    
    dt = yaml_data.get("document_type")
    if dt and dt not in VALID_DOCUMENT_TYPES:
        issues.append(Issue(HIGH, "YAML-enum", f"Invalid document_type: '{dt}'"))
    
    cs = yaml_data.get("clinical_significance")
    if cs and cs not in VALID_CLINICAL_SIGNIFICANCE:
        issues.append(Issue(HIGH, "YAML-enum", f"Invalid clinical_significance: '{cs}'"))
    
    route = yaml_data.get("route")
    if route and route not in VALID_ROUTES:
        issues.append(Issue(HIGH, "YAML-enum", f"Invalid route: '{route}'"))
    
    sec_cats = yaml_data.get("secondary_categories", [])
    if sec_cats:
        for sc in sec_cats:
            if sc not in VALID_CATEGORIES:
                issues.append(Issue(HIGH, "YAML-enum", f"Invalid secondary_category: '{sc}'"))

    # ── Tag validation ──
    tags = yaml_data.get("tags", [])
    if isinstance(tags, list):
        for tag in tags:
            if not isinstance(tag, str):
                issues.append(Issue(MEDIUM, "YAML-tags", f"Non-string tag: {tag}"))
            elif tag.startswith("#"):
                issues.append(Issue(MEDIUM, "YAML-tags", f"Tag has # prefix: '{tag}'"))
            elif tag not in VALID_TAGS:
                issues.append(Issue(MEDIUM, "YAML-tags", f"Non-canonical tag: '{tag}'"))
        
        # Tag count policy
        stem = Path(filename).stem
        doc_type = yaml_data.get("document_type", "")
        max_allowed = 5  # Standard
        if doc_type in SYNTHESIS_DOC_TYPES:
            max_allowed = 10
        for exc, limit in ENCYCLOPEDIC_EXCEPTIONS.items():
            if exc in stem:
                max_allowed = limit + 2  # Allow some buffer
        
        if len(tags) > max_allowed + 1:  # +1 grace
            issues.append(Issue(LOW, "YAML-tags", f"Tag count ({len(tags)}) exceeds policy max ({max_allowed}) for {doc_type}"))
        
        if len(tags) < 2:
            issues.append(Issue(MEDIUM, "YAML-tags", f"Fewer than 2 tags ({len(tags)})"))
    else:
        issues.append(Issue(HIGH, "YAML-tags", f"Tags not a list (type: {type(tags).__name__})"))

    # ── Boolean flags must be actual booleans ──
    for bf in ["qtc_data", "electrolyte_data", "herg_data"]:
        val = yaml_data.get(bf)
        if val is not None and not isinstance(val, bool):
            issues.append(Issue(HIGH, "YAML-bool", f"{bf} is {type(val).__name__} ('{val}'), expected boolean"))

    # ── key_findings length ──
    kf = yaml_data.get("key_findings", "")
    if isinstance(kf, str) and len(kf) > 250:
        issues.append(Issue(LOW, "YAML-length", f"key_findings exceeds 250 chars ({len(kf)} chars)"))

    # ── Aliases check ──
    aliases = yaml_data.get("aliases", [])
    if isinstance(aliases, list) and len(aliases) < 2:
        issues.append(Issue(LOW, "YAML-aliases", f"Fewer than 2 aliases ({len(aliases)})"))

    # ── Authors check ──
    authors = yaml_data.get("authors", [])
    if isinstance(authors, list) and len(authors) == 0:
        issues.append(Issue(HIGH, "YAML-authors", "Empty authors list"))

    # ── Category-specific mandatory fields ──
    if cat in ("RED", "GREEN"):
        if "dosing_range" not in yaml_data or not yaml_data.get("dosing_range"):
            issues.append(Issue(MEDIUM, "YAML-category", f"{cat} paper missing dosing_range (mandatory for {cat})"))
        if "route" not in yaml_data or not yaml_data.get("route"):
            issues.append(Issue(MEDIUM, "YAML-category", f"{cat} paper missing route (mandatory for {cat})"))

    # ── Contraindications type check ──
    contras = yaml_data.get("contraindications")
    if contras is not None and not isinstance(contras, list):
        issues.append(Issue(HIGH, "YAML-contras", f"contraindications is {type(contras).__name__}, expected list"))

    # ── Forbidden empty string fields ──
    for field in ["doi", "journal", "publication_date"]:
        if field in yaml_data and yaml_data[field] == "":
            issues.append(Issue(MEDIUM, "YAML-empty", f"'{field}' is empty string — should be omitted if unavailable"))
    
    # ── sample_size / mortality_count zero check ──
    if yaml_data.get("sample_size") == 0:
        issues.append(Issue(MEDIUM, "YAML-zero", "sample_size is 0 — should be omitted if not a human study"))
    if yaml_data.get("mortality_count") == 0:
        issues.append(Issue(MEDIUM, "YAML-zero", "mortality_count is 0 — should be omitted if no deaths reported"))

    # ── Year sanity ──
    year = yaml_data.get("year")
    if isinstance(year, int) and (year < 1900 or year > 2030):
        issues.append(Issue(HIGH, "YAML-year", f"Suspicious year: {year}"))

    # ── Deprecated research-article warning ──
    if dt == "research-article":
        issues.append(Issue(LOW, "YAML-deprecated", "document_type is 'research-article' — should be disambiguated"))


def check_body_content(body, filename, issues):
    """Check body text for truncation, corruption, and structural issues."""
    
    if not body or len(body.strip()) == 0:
        issues.append(Issue(CRITICAL, "BODY-empty", "No body content after YAML frontmatter"))
        return
    
    body_bytes = len(body.encode("utf-8"))
    
    # ── Suspiciously short ──
    if body_bytes < 500:
        issues.append(Issue(CRITICAL, "BODY-short", f"Body content only {body_bytes} bytes (likely truncated/stub)"))
    elif body_bytes < 1000:
        issues.append(Issue(HIGH, "BODY-short", f"Body content only {body_bytes} bytes (possibly incomplete)"))

    # ── Truncation detection ──
    stripped = body.rstrip()
    if stripped:
        last_char = stripped[-1]
        last_50 = stripped[-50:]
        
        # Ends mid-word (no terminal punctuation, no heading marker, no link)
        if last_char.isalpha() and not stripped.endswith("md") and not stripped.endswith("]]"):
            # Check if it looks like an incomplete sentence
            last_line = stripped.split("\n")[-1].strip()
            if (last_line and not last_line.startswith("#") 
                and not last_line.startswith("-") 
                and not last_line.startswith("*")
                and not last_line.endswith("]]")
                and not last_line.endswith(")")
                and not last_line.endswith(">")
                and not last_line.endswith("|")
                and last_char not in ".!?:;\"')]}>"
                and len(last_line) > 10):
                issues.append(Issue(HIGH, "BODY-truncated", f"File may end mid-sentence: '...{last_line[-60:]}'"))
        
        # Ends with unclosed markdown constructs
        if stripped.count("```") % 2 == 1:
            issues.append(Issue(HIGH, "BODY-truncated", "Unclosed code block (odd number of ``` delimiters)"))

    # ── Missing expected sections ──
    body_lower = body.lower()
    headings = re.findall(r'^#{1,4}\s+(.+)$', body, re.MULTILINE)
    heading_texts = [h.lower().strip() for h in headings]
    
    has_abstract = any("abstract" in h for h in heading_texts)
    has_key_findings = any("key finding" in h for h in heading_texts)
    has_see_also = any("see also" in h for h in heading_texts)
    has_any_heading = len(headings) > 0
    
    if not has_any_heading:
        issues.append(Issue(HIGH, "BODY-structure", "No markdown headings found in body"))
    
    if not has_abstract and "abstract" not in body_lower:
        issues.append(Issue(MEDIUM, "BODY-structure", "No Abstract section found"))
    
    if not has_see_also and "see also" not in body_lower:
        issues.append(Issue(LOW, "BODY-structure", "No 'See Also' section found"))
    
    # ── Wikilinks check ──
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', body)
    if len(wikilinks) < 2:
        issues.append(Issue(LOW, "BODY-links", f"Fewer than 2 wikilinks ({len(wikilinks)})"))
    
    # Check for broken wikilinks (orphaned brackets)
    orphan_open = len(re.findall(r'\[\[(?![^\]]*\]\])', body))
    orphan_close = len(re.findall(r'(?<!\[\[)\]\]', body))  # rough check
    bracket_pairs = body.count("[[")
    closing_pairs = body.count("]]")
    if bracket_pairs != closing_pairs:
        issues.append(Issue(MEDIUM, "BODY-links", f"Mismatched wikilink brackets: {bracket_pairs} [[ vs {closing_pairs} ]]"))


def check_corruption(content, filename, issues):
    """Check for garbled text, PDF extraction artefacts, and encoding issues."""
    
    # ── Common PDF extraction artefacts ──
    # Broken ligatures: ﬁ ﬂ ﬀ ﬃ ﬄ are fine Unicode, but garbled versions aren't
    garbled_patterns = [
        (r'[^\x00-\x7F\u00A0-\u024F\u0370-\u03FF\u2000-\u206F\u2190-\u21FF\u2200-\u22FF\u2300-\u23FF\u2500-\u257F\u25A0-\u25FF\u2600-\u26FF\u2700-\u27BF\u2B00-\u2BFF\uFE00-\uFE0F\u0300-\u036F\u1E00-\u1EFF\u2010-\u2027\u2030-\u205E\u00B0-\u00FF]{3,}', 
         "Possible garbled Unicode cluster"),
        (r'(?:\x00)', "Null bytes in content"),
        (r'\uFFFD', "Unicode replacement character (U+FFFD) — encoding error"),
        (r'(?<!\w)\(\s*\)', "Empty parentheses () — possible PDF stripping artefact"),
        (r'(?<!\w)\(\s*;\s*\)', "Empty (;) — possible PDF stripping artefact"),
    ]
    
    for pattern, desc in garbled_patterns:
        matches = re.findall(pattern, content)
        if matches:
            count = len(matches)
            if desc.startswith("Empty parentheses"):
                if count >= 3:
                    issues.append(Issue(HIGH, "CORRUPT-pdf", f"{desc}: {count} instances (known PDF damage pattern)"))
                elif count >= 1:
                    issues.append(Issue(MEDIUM, "CORRUPT-pdf", f"{desc}: {count} instance(s)"))
            elif desc.startswith("Empty (;)"):
                if count >= 1:
                    issues.append(Issue(HIGH, "CORRUPT-pdf", f"{desc}: {count} instance(s) (known PDF damage pattern)"))
            elif desc == "Null bytes in content":
                issues.append(Issue(CRITICAL, "CORRUPT-null", f"Null bytes found in file"))
            elif desc.startswith("Unicode replacement"):
                issues.append(Issue(HIGH, "CORRUPT-encoding", f"Replacement characters found: {count} instance(s)"))
            else:
                if count > 5:
                    issues.append(Issue(MEDIUM, "CORRUPT-unicode", f"{desc}: {count} instance(s)"))

    # ── Corrupted µ encoding ──
    # lg/mL when should be µg/mL
    if re.search(r'\blg/m[Ll]\b', content):
        issues.append(Issue(HIGH, "CORRUPT-mu", "Possible corrupted µ: 'lg/mL' found (should be µg/mL?)"))
    
    # ── Missing Greek letters (heuristic) ──
    if re.search(r'(?<![a-zA-Z])FosB(?!.*Δ)', content) and "ΔFosB" not in content and "delta" not in content.lower():
        issues.append(Issue(LOW, "CORRUPT-greek", "FosB without Δ prefix — possible missing Greek letter"))

    # ── Broken table detection ──
    table_lines = [l for l in content.split("\n") if l.strip().startswith("|")]
    if table_lines:
        for i, line in enumerate(table_lines):
            pipe_count = line.count("|")
            if i > 0 and abs(pipe_count - table_lines[0].count("|")) > 2:
                issues.append(Issue(MEDIUM, "BODY-table", f"Table row {i+1} has inconsistent column count ({pipe_count} vs {table_lines[0].count('|')} pipes)"))
                break  # Report once per file


def check_repetition(body, filename, issues):
    """Check for repeated paragraphs or sentences (PDF extraction bug)."""
    
    # Split into paragraphs
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip() and len(p.strip()) > 50]
    
    if len(paragraphs) < 2:
        return
    
    # Check for exact duplicate paragraphs
    para_counts = Counter(paragraphs)
    for para, count in para_counts.items():
        if count > 1:
            preview = para[:80].replace("\n", " ")
            issues.append(Issue(HIGH, "BODY-repeat", f"Paragraph repeated {count}x: '{preview}...'"))
    
    # Check for duplicate sentences (more granular)
    all_sentences = []
    for para in paragraphs:
        sentences = re.split(r'(?<=[.!?])\s+', para)
        all_sentences.extend([s.strip() for s in sentences if len(s.strip()) > 40])
    
    sent_counts = Counter(all_sentences)
    repeated_sents = {s: c for s, c in sent_counts.items() if c > 2}  # threshold: 3+
    if repeated_sents:
        for sent, count in list(repeated_sents.items())[:3]:  # Report max 3
            preview = sent[:70]
            issues.append(Issue(MEDIUM, "BODY-repeat", f"Sentence repeated {count}x: '{preview}...'"))


def check_formatting(body, filename, issues):
    """Check for broken markdown formatting."""
    
    lines = body.split("\n")
    
    # ── Unclosed code blocks ──
    in_code = False
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_code = not in_code
    if in_code:
        issues.append(Issue(HIGH, "FORMAT-code", "Unclosed code block at end of file"))
    
    # ── Malformed headings ──
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#") and not stripped.startswith("# ") and len(stripped) > 1:
            if stripped.startswith("##") and not stripped.startswith("## "):
                if stripped.startswith("###") and not stripped.startswith("### "):
                    pass  # deeper heading
                elif not stripped.startswith("###"):
                    issues.append(Issue(LOW, "FORMAT-heading", f"Line {i+1}: Heading missing space after #: '{stripped[:40]}'"))
    
    # ── Empty markdown links ──
    empty_links = re.findall(r'\[([^\]]*)\]\(\s*\)', body)
    if empty_links:
        issues.append(Issue(MEDIUM, "FORMAT-links", f"Empty markdown link targets: {len(empty_links)} instances"))
    
    # ── Broken bold/italic ──
    # Count unmatched ** or * (very rough heuristic)
    bold_count = body.count("**")
    if bold_count % 2 == 1:
        issues.append(Issue(LOW, "FORMAT-bold", "Odd number of ** delimiters (possible unclosed bold)"))


def audit_file(filepath):
    """Run all checks on a single file, return list of issues."""
    issues = []
    
    try:
        content = filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        issues.append(Issue(CRITICAL, "ENCODING", "File cannot be read as UTF-8"))
        return issues
    except Exception as e:
        issues.append(Issue(CRITICAL, "READ-ERROR", f"Cannot read file: {e}"))
        return issues
    
    if len(content.strip()) == 0:
        issues.append(Issue(CRITICAL, "EMPTY", "File is completely empty"))
        return issues
    
    # Split into YAML and body
    yaml_str, body = split_yaml_body(content)
    
    if yaml_str is None:
        issues.append(Issue(CRITICAL, "YAML", "No YAML frontmatter found (missing opening ---)"))
    else:
        yaml_data = parse_yaml_safe(yaml_str)
        if yaml_data is None:
            issues.append(Issue(CRITICAL, "YAML", "YAML frontmatter failed to parse"))
        else:
            check_yaml_schema(yaml_data, filepath.name, issues)
    
    # Body checks
    check_body_content(body, filepath.name, issues)
    check_corruption(content, filepath.name, issues)
    check_repetition(body, filepath.name, issues)
    check_formatting(body, filepath.name, issues)
    
    return issues



def generate_report(results):
    """Generate ranked report from audit results."""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    lines = []
    lines.append("=" * 78)
    lines.append(f"  IbogaineVault — Phase 1 Automated Structural Audit Report")
    lines.append(f"  Generated: {timestamp}")
    lines.append("=" * 78)
    lines.append("")
    
    # ── Summary statistics ──
    total_files = len(results)
    files_with_issues = sum(1 for _, issues in results if issues)
    clean_files = total_files - files_with_issues
    
    all_issues = []
    for _, issues in results:
        all_issues.extend(issues)
    
    severity_counts = Counter(i.severity for i in all_issues)
    category_counts = Counter(i.category for i in all_issues)
    
    lines.append(f"  SUMMARY")
    lines.append(f"  ─────────────────────────────────────────")
    lines.append(f"  Total paper files scanned:  {total_files}")
    lines.append(f"  Files with issues:          {files_with_issues}")
    lines.append(f"  Clean files:                {clean_files}")
    lines.append(f"  Total issues found:         {len(all_issues)}")
    lines.append(f"")
    lines.append(f"  By severity:")
    for sev in [CRITICAL, HIGH, MEDIUM, LOW]:
        count = severity_counts.get(sev, 0)
        if count:
            lines.append(f"    {sev:10s}  {count}")
    lines.append(f"")
    lines.append(f"  Top issue categories:")
    for cat, count in category_counts.most_common(10):
        lines.append(f"    {cat:25s}  {count}")
    lines.append("")
    
    # ── Ranked file list ──
    scored_results = []
    for filepath, issues in results:
        if issues:
            total_score = sum(i.score for i in issues)
            scored_results.append((filepath, issues, total_score))
    
    scored_results.sort(key=lambda x: -x[2])
    
    lines.append("=" * 78)
    lines.append("  RANKED FILE REPORT (most problematic first)")
    lines.append("=" * 78)
    lines.append("")
    
    for rank, (filepath, issues, score) in enumerate(scored_results, 1):
        rel_path = filepath.relative_to(VAULT_ROOT)
        severity_summary = Counter(i.severity for i in issues)
        sev_str = ", ".join(f"{c}×{s}" for s, c in sorted(severity_summary.items(), 
                           key=lambda x: [CRITICAL, HIGH, MEDIUM, LOW].index(x[0])))
        
        lines.append(f"  #{rank:3d}  [Score: {score:4d}]  {rel_path}")
        lines.append(f"       Issues: {len(issues)} ({sev_str})")
        
        # Group issues by severity
        for sev in [CRITICAL, HIGH, MEDIUM, LOW]:
            sev_issues = [i for i in issues if i.severity == sev]
            for issue in sev_issues:
                lines.append(f"         [{sev}] {issue.category}: {issue.detail}")
        
        lines.append("")
    
    # ── Clean files list ──
    clean = [(f, i) for f, i in results if not i]
    if clean:
        lines.append("=" * 78)
        lines.append(f"  CLEAN FILES ({len(clean)} files — no issues detected)")
        lines.append("=" * 78)
        for filepath, _ in clean:
            rel_path = filepath.relative_to(VAULT_ROOT)
            lines.append(f"    ✓ {rel_path}")
        lines.append("")
    
    return "\n".join(lines)


def main():
    print("IbogaineVault Phase 1 Audit — scanning paper files...\n")
    
    files = find_paper_files()
    print(f"Found {len(files)} paper markdown files to audit.\n")
    
    results = []
    for i, filepath in enumerate(files):
        if (i + 1) % 25 == 0:
            print(f"  Scanning... {i+1}/{len(files)}")
        issues = audit_file(filepath)
        results.append((filepath, issues))
    
    report = generate_report(results)
    
    # Write report
    report_path = VAULT_ROOT / "_meta" / "audit_phase1_report.txt"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {report_path}")
    print(f"\n{report}")


if __name__ == "__main__":
    main()
