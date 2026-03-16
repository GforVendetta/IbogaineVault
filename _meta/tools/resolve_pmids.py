#!/usr/bin/env python3
"""
IbogaineVault PMID/PMCID Resolution Script
============================================
Resolves DOIs to PMIDs and PMCIDs via the NCBI ID Converter API,
then writes the results into paper YAML frontmatter.

Uses line-by-line YAML insertion (NOT full round-tripping) to preserve
existing field order and formatting exactly.

USAGE:
  python3 resolve_pmids.py --vault /path/to/vault
  python3 resolve_pmids.py --vault /path/to/vault --dry-run
  python3 resolve_pmids.py --vault /path/to/vault --report-only

Created: 2026-03-15 (Session 2 — PMID Enrichment)
"""

import os
import sys
import re
import json
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from collections import defaultdict


# ══════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════

NCBI_API_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
TOOL_NAME = "ibogainevault"
CONTACT_EMAIL = "philip@ibogaine.space"
BATCH_SIZE = 200        # NCBI max per request
REQUEST_DELAY = 0.35    # seconds between batches (3 req/s limit)


# ══════════════════════════════════════════
# VAULT DETECTION (mirrored from validate_vault.py)
# ══════════════════════════════════════════

VAULT_MARKERS = ["_meta/schema_registry.yml", "HOME.md", "Hubs"]


def detect_vault_root(explicit_path):
    p = Path(explicit_path)
    if p.exists() and any((p / m).exists() for m in VAULT_MARKERS):
        return p
    print(f"ERROR: {explicit_path} does not look like a vault root.", file=sys.stderr)
    sys.exit(1)


# ══════════════════════════════════════════
# FILE DISCOVERY (mirrored from validate_vault.py)
# ══════════════════════════════════════════

def discover_paper_files(vault_root):
    """Find all .md files in paper locations."""
    paper_files = []
    vault = Path(vault_root)
    for entry in sorted(vault.iterdir()):
        if entry.is_dir() and re.match(r'^\d{4}$', entry.name):
            for md in sorted(entry.glob("*.md")):
                paper_files.append(md)
    for folder_name in ["Clinical_Guidelines", "Primary_Sources",
                        "Other", "Industry_Documents"]:
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
# FRONTMATTER ANALYSIS
# ══════════════════════════════════════════

def analyse_frontmatter(filepath):
    """Parse frontmatter line-by-line. Returns dict with:
      doi, pmid, pmcid          — string values or None
      has_pmid_field             — bool (field line exists, even if empty)
      has_pmcid_field            — bool
      doi_line_num               — 0-indexed line number of doi: line, or None
      pmid_line_num              — 0-indexed line number of pmid: line, or None
      pmcid_line_num             — 0-indexed line number of pmcid: line, or None
      closing_delimiter_line     — 0-indexed line number of closing ---
      has_frontmatter            — bool
    """
    info = {
        "doi": None, "pmid": None, "pmcid": None,
        "has_pmid_field": False, "has_pmcid_field": False,
        "doi_line_num": None, "pmid_line_num": None, "pmcid_line_num": None,
        "closing_delimiter_line": None, "has_frontmatter": False,
    }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return info

    if not lines or lines[0].strip() != "---":
        return info
    info["has_frontmatter"] = True

    for i, line in enumerate(lines[1:], start=1):
        stripped = line.strip()
        if stripped == "---":
            info["closing_delimiter_line"] = i
            break

        def _extract_val(text):
            v = text.strip().strip('"').strip("'")
            return v if v else None

        if re.match(r'^doi:\s', stripped) or stripped == "doi:":
            info["doi_line_num"] = i
            val = stripped.split(":", 1)[1] if ":" in stripped else ""
            info["doi"] = _extract_val(val)
        elif re.match(r'^pmid:\s', stripped) or stripped == "pmid:":
            info["has_pmid_field"] = True
            info["pmid_line_num"] = i
            val = stripped.split(":", 1)[1] if ":" in stripped else ""
            info["pmid"] = _extract_val(val)
        elif re.match(r'^pmcid:\s', stripped) or stripped == "pmcid:":
            info["has_pmcid_field"] = True
            info["pmcid_line_num"] = i
            val = stripped.split(":", 1)[1] if ":" in stripped else ""
            info["pmcid"] = _extract_val(val)

    return info


# ══════════════════════════════════════════
# NCBI ID CONVERTER API
# ══════════════════════════════════════════

def resolve_dois_batch(dois):
    """Call NCBI ID Converter API with a list of DOIs.
    Returns dict: {doi_lower: {"pmid": str|None, "pmcid": str|None, "error": str|None}}"""
    results = {}
    if not dois:
        return results

    ids_param = ",".join(dois)
    url = (f"{NCBI_API_URL}?tool={TOOL_NAME}&email={CONTACT_EMAIL}"
           f"&ids={ids_param}&format=json")

    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", f"{TOOL_NAME}/1.0 ({CONTACT_EMAIL})")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"  ✗ HTTP error {e.code}: {e.reason}", file=sys.stderr)
        for d in dois:
            results[d.lower()] = {"pmid": None, "pmcid": None, "error": f"HTTP {e.code}"}
        return results
    except (urllib.error.URLError, Exception) as e:
        print(f"  ✗ Request error: {e}", file=sys.stderr)
        for d in dois:
            results[d.lower()] = {"pmid": None, "pmcid": None, "error": str(e)}
        return results

    records = data.get("records", [])
    for rec in records:
        doi = rec.get("doi", "").lower()
        if not doi:
            continue
        if rec.get("status") == "error" or rec.get("errmsg"):
            results[doi] = {"pmid": None, "pmcid": None,
                            "error": rec.get("errmsg", "unknown")}
        else:
            results[doi] = {
                "pmid": rec.get("pmid"),
                "pmcid": rec.get("pmcid"),
                "error": None,
            }

    # Mark any DOIs sent but not in response
    for d in dois:
        if d.lower() not in results:
            results[d.lower()] = {"pmid": None, "pmcid": None,
                                  "error": "not in NCBI response"}

    return results


def resolve_doi_via_esearch(doi):
    """Fallback: search PubMed directly for a DOI using ESearch.
    Returns PMID string or None. Only gets PMID (no PMCID)."""
    import urllib.parse
    term = urllib.parse.quote(f"{doi}[doi]")
    url = (f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
           f"?db=pubmed&term={term}&retmode=json"
           f"&tool={TOOL_NAME}&email={CONTACT_EMAIL}")

    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", f"{TOOL_NAME}/1.0 ({CONTACT_EMAIL})")
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

    id_list = data.get("esearchresult", {}).get("idlist", [])
    if id_list and len(id_list) == 1:
        return id_list[0]
    return None


# ══════════════════════════════════════════
# FRONTMATTER INSERTION (line-by-line, preserves formatting)
# ══════════════════════════════════════════

def update_frontmatter(filepath, pmid_val, pmcid_val, info):
    """Insert or update pmid/pmcid in YAML frontmatter.
    
    Rules:
    - Field exists with value → SKIP (never overwrite existing data)
    - Field exists but empty   → FILL with resolved value
    - Field absent             → INSERT after doi: line
    
    Returns: (modified: bool, actions: list[str])
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    actions = []
    new_lines = list(lines)  # work on a copy

    # ── Handle PMID ──
    if pmid_val:
        if info["has_pmid_field"] and info["pmid"]:
            pass  # already populated, skip
        elif info["has_pmid_field"] and not info["pmid"]:
            # Empty pmid: field → fill it
            ln = info["pmid_line_num"]
            new_lines[ln] = f'pmid: "{pmid_val}"\n'
            actions.append(f"filled empty pmid → {pmid_val}")
        elif not info["has_pmid_field"] and info["doi_line_num"] is not None:
            # No pmid field → insert after doi line
            ln = info["doi_line_num"]
            new_lines.insert(ln + 1, f'pmid: "{pmid_val}"\n')
            actions.append(f"inserted pmid → {pmid_val}")
            # Track the offset caused by insertion
            # (subsequent line numbers in info are now stale by +1)

    # Calculate offset from pmid insertion
    offset = 0
    if pmid_val and not info["has_pmid_field"] and info["doi_line_num"] is not None:
        if not (info["has_pmid_field"] and info["pmid"]):
            offset = 1

    # ── Handle PMCID ──
    if pmcid_val:
        if info["has_pmcid_field"] and info["pmcid"]:
            pass  # already populated, skip
        elif info["has_pmcid_field"] and not info["pmcid"]:
            # Empty pmcid: field → fill it
            ln = info["pmcid_line_num"] + offset
            new_lines[ln] = f'pmcid: "{pmcid_val}"\n'
            actions.append(f"filled empty pmcid → {pmcid_val}")
        elif not info["has_pmcid_field"]:
            # Insert after pmid line (if just inserted) or after doi line
            if pmid_val and not info["has_pmid_field"] and info["doi_line_num"] is not None:
                # pmid was just inserted at doi_line_num + 1, so pmcid goes at +2
                insert_at = info["doi_line_num"] + 2
            elif info["has_pmid_field"]:
                insert_at = info["pmid_line_num"] + 1 + offset
            elif info["doi_line_num"] is not None:
                insert_at = info["doi_line_num"] + 1 + offset
            else:
                insert_at = None
            if insert_at is not None:
                new_lines.insert(insert_at, f'pmcid: "{pmcid_val}"\n')
                actions.append(f"inserted pmcid → {pmcid_val}")

    if not actions:
        return False, actions

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    return True, actions


# ══════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Resolve DOIs to PMIDs/PMCIDs via NCBI and populate vault frontmatter")
    parser.add_argument("--vault", type=str, required=True,
                        help="Path to vault root directory")
    parser.add_argument("--dry-run", action="store_true",
                        help="Resolve IDs but don't write to files")
    parser.add_argument("--report-only", action="store_true",
                        help="Scan vault and report status without calling NCBI")
    args = parser.parse_args()

    vault_root = detect_vault_root(args.vault)
    print(f"Vault root: {vault_root}")
    print()

    # ── Step 1: Discover and analyse all papers ──
    paper_files = discover_paper_files(vault_root)
    print(f"Discovered {len(paper_files)} papers")

    # Categorise papers
    has_doi = []         # (filepath, doi, info)
    no_doi = []          # filepath
    already_resolved = [] # (filepath, doi, pmid)
    needs_resolution = [] # (filepath, doi, info)

    for fp in paper_files:
        info = analyse_frontmatter(fp)
        if not info["has_frontmatter"]:
            continue
        if not info["doi"]:
            no_doi.append(fp)
            continue
        has_doi.append((fp, info["doi"], info))
        if info["pmid"]:
            already_resolved.append((fp, info["doi"], info["pmid"]))
        else:
            needs_resolution.append((fp, info["doi"], info))

    print(f"  With DOI:          {len(has_doi)}")
    print(f"  Without DOI:       {len(no_doi)} (books, theses, primary sources — skipped)")
    print(f"  Already have PMID: {len(already_resolved)}")
    print(f"  Need resolution:   {len(needs_resolution)}")
    print()

    if args.report_only:
        print("── Report only mode — no NCBI calls, no file writes ──")
        if already_resolved:
            print(f"\nAlready resolved ({len(already_resolved)}):")
            for fp, doi, pmid in already_resolved:
                print(f"  {Path(fp).name}: PMID {pmid}")
        if needs_resolution:
            print(f"\nNeed resolution ({len(needs_resolution)}):")
            for fp, doi, info in needs_resolution:
                print(f"  {Path(fp).name}: {doi}")
        return

    if not needs_resolution:
        print("Nothing to resolve — all papers with DOIs already have PMIDs.")
        return

    # ── Step 2: Batch resolve via NCBI ──
    dois_to_resolve = [doi for _, doi, _ in needs_resolution]
    # Build a lookup: doi_lower → list of (filepath, info)
    doi_to_papers = defaultdict(list)
    for fp, doi, info in needs_resolution:
        doi_to_papers[doi.lower()].append((fp, info))

    # NOTE: PMCID backfill for already-resolved papers is NOT done here.
    # The ID Converter batch already returns PMCIDs when available.
    # Papers whose DOIs aren't in PMC will never have PMCIDs regardless
    # of how many times we query. Backfill would just waste API calls.

    # Deduplicate DOIs
    unique_dois = list(dict.fromkeys(d.lower() for d in dois_to_resolve))

    print(f"Resolving {len(unique_dois)} unique DOIs via NCBI ID Converter...")
    all_results = {}
    batches = [unique_dois[i:i+BATCH_SIZE]
               for i in range(0, len(unique_dois), BATCH_SIZE)]

    for batch_num, batch in enumerate(batches, 1):
        print(f"  Batch {batch_num}/{len(batches)}: {len(batch)} DOIs...", end=" ")
        results = resolve_dois_batch(batch)
        resolved_count = sum(1 for r in results.values()
                             if r["pmid"] is not None)
        print(f"→ {resolved_count} resolved")
        all_results.update(results)
        if batch_num < len(batches):
            time.sleep(REQUEST_DELAY)

    # ── Step 2b: Fallback — ESearch for DOIs not found via ID Converter ──
    failed_dois = [doi for doi, r in all_results.items()
                   if r["error"] and "not found" in r["error"].lower()]
    if failed_dois:
        print(f"\nFallback: searching PubMed ESearch for {len(failed_dois)} "
              f"DOIs not in PMC...")
        esearch_found = 0
        for i, doi in enumerate(failed_dois):
            pmid = resolve_doi_via_esearch(doi)
            if pmid:
                all_results[doi] = {"pmid": pmid, "pmcid": None, "error": None}
                esearch_found += 1
            else:
                # Keep as not-found (clear the error for cleaner reporting)
                all_results[doi] = {"pmid": None, "pmcid": None, "error": None}
            # Rate limit: 3 requests/sec without API key
            if (i + 1) % 3 == 0:
                time.sleep(1.0)
            if (i + 1) % 30 == 0:
                print(f"  ...{i+1}/{len(failed_dois)} checked, "
                      f"{esearch_found} found so far")
        print(f"  ESearch resolved {esearch_found} additional PMIDs")

    # ── Step 3: Write results to files ──
    stats = {
        "resolved_pmid": 0,
        "resolved_pmcid": 0,
        "not_found": 0,
        "errors": 0,
        "already_had_pmid": len(already_resolved),
        "no_doi": len(no_doi),
        "files_modified": 0,
        "skipped_existing": 0,
    }
    error_details = []
    not_found_details = []
    resolved_details = []

    for doi_lower, result in all_results.items():
        if doi_lower not in doi_to_papers:
            continue

        pmid_val = result["pmid"]
        pmcid_val = result["pmcid"]
        error = result["error"]

        if error:
            stats["errors"] += 1
            for fp, info in doi_to_papers[doi_lower]:
                error_details.append((Path(fp).name, doi_lower, error))
            continue

        if not pmid_val and not pmcid_val:
            stats["not_found"] += 1
            for fp, info in doi_to_papers[doi_lower]:
                not_found_details.append((Path(fp).name, doi_lower))
            continue

        if pmid_val:
            stats["resolved_pmid"] += 1
        if pmcid_val:
            stats["resolved_pmcid"] += 1

        for fp, info in doi_to_papers[doi_lower]:
            # Skip if both already populated
            if info["pmid"] and info["pmcid"]:
                stats["skipped_existing"] += 1
                continue

            if args.dry_run:
                actions_desc = []
                if pmid_val and not info["pmid"]:
                    actions_desc.append(f"pmid={pmid_val}")
                if pmcid_val and not info["pmcid"]:
                    actions_desc.append(f"pmcid={pmcid_val}")
                if actions_desc:
                    resolved_details.append(
                        (Path(fp).name, doi_lower,
                         ", ".join(actions_desc)))
                continue

            modified, actions = update_frontmatter(
                fp, pmid_val, pmcid_val, info)
            if modified:
                stats["files_modified"] += 1
                resolved_details.append(
                    (Path(fp).name, doi_lower,
                     "; ".join(actions)))

    # ── Summary Report ──
    print()
    print("═" * 60)
    print("PMID/PMCID RESOLUTION REPORT")
    print("═" * 60)
    print(f"  Total papers discovered:  {len(paper_files)}")
    print(f"  Papers with DOI:          {len(has_doi)}")
    print(f"  Papers without DOI:       {len(no_doi)}")
    print(f"  Already had PMID:         {stats['already_had_pmid']}")
    print(f"  Unique DOIs resolved:     {len(unique_dois)}")
    print()
    print(f"  PMIDs found:              {stats['resolved_pmid']}")
    print(f"  PMCIDs found:             {stats['resolved_pmcid']}")
    print(f"  Not in PubMed:            {stats['not_found']}")
    print(f"  API errors:               {stats['errors']}")
    print()
    if args.dry_run:
        print(f"  DRY RUN — no files modified")
        print(f"  Would modify:             {len(resolved_details)}")
    else:
        print(f"  Files modified:           {stats['files_modified']}")
        print(f"  Skipped (existing data):  {stats['skipped_existing']}")
    print("═" * 60)

    if resolved_details:
        print(f"\n── Resolved ({len(resolved_details)}) ──")
        for name, doi, desc in sorted(resolved_details):
            print(f"  {name}: {desc}")

    if not_found_details:
        print(f"\n── Not in PubMed ({len(not_found_details)}) ──")
        for name, doi in sorted(not_found_details):
            print(f"  {name}: {doi}")

    if error_details:
        print(f"\n── Errors ({len(error_details)}) ──")
        for name, doi, err in sorted(error_details):
            print(f"  {name}: {doi} — {err}")

    print()


if __name__ == "__main__":
    main()
