#!/usr/bin/env python3
"""
lookup_identifiers.py — Missing Academic Identifier Lookup for IbogaineVault

Looks up DOIs, PMIDs, PMCIDs, and ISSNs via CrossRef and PubMed APIs,
then populates them in paper YAML frontmatter.

Usage:
    python3 lookup_identifiers.py --dry-run --verbose
    python3 lookup_identifiers.py --apply
    python3 lookup_identifiers.py --apply-all
"""

import json
import os
import re
import sys
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from difflib import SequenceMatcher
from datetime import datetime
import xml.etree.ElementTree as ET

VAULT_ROOT = "/Users/aretesofia/IbogaineVault"
PAPERS_JSON = os.path.join(VAULT_ROOT, "papers.json")
REPORT_PATH = os.path.join(VAULT_ROOT, "_meta", "tools", "identifier_lookup_report.json")
MAILTO = "philip@pangeabiomedics.com"

# ── Rate limiting ──────────────────────────────────────────────────────────
class RateLimiter:
    def __init__(self, requests_per_second):
        self.min_interval = 1.0 / requests_per_second
        self.last_request = 0
        self.total_calls = 0

    def wait(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request = time.time()
        self.total_calls += 1

crossref_limiter = RateLimiter(1)   # 1 req/s
ncbi_limiter = RateLimiter(3)       # 3 req/s

# ── Helpers ────────────────────────────────────────────────────────────────
def is_valid_doi(doi):
    """Check if a DOI string is well-formed."""
    if not doi or not isinstance(doi, str):
        return False
    doi = doi.strip()
    return doi.startswith("10.") and "/" in doi and len(doi) > 7

def title_similarity(a, b):
    """Case-insensitive title similarity ratio."""
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

def first_author_surname(authors):
    """Extract first author's surname from the authors list."""
    if not authors or not isinstance(authors, list) or len(authors) == 0:
        return ""
    first = authors[0]
    if isinstance(first, str):
        # Format: "Surname, Given" or just "Surname"
        return first.split(",")[0].strip()
    return ""

def safe_api_call(url, limiter, timeout=15):
    """Make a rate-limited API call with error handling."""
    limiter.wait()
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", f"IbogaineVault/1.0 (mailto:{MAILTO})")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            # Rate limited — wait and retry once
            time.sleep(5)
            limiter.wait()
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return resp.read().decode("utf-8")
            except Exception:
                return None
        return None
    except Exception:
        return None

# ── YAML Modification (targeted string ops, no re-serialisation) ──────────
def read_frontmatter_and_body(filepath):
    """Read a markdown file, return (frontmatter_str, body_str, full_text)."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.match(r'^---\n(.*?)\n---\n?(.*)', text, re.DOTALL)
    if not m:
        return None, None, text
    return m.group(1), m.group(2), text

def insert_yaml_field(fm_str, field_name, value, after_field=None):
    """Insert a YAML field into frontmatter string. Returns modified string."""
    line = f'{field_name}: "{value}"'
    lines = fm_str.split("\n")
    
    if after_field:
        for i, l in enumerate(lines):
            if l.startswith(f"{after_field}:"):
                lines.insert(i + 1, line)
                return "\n".join(lines)
    
    # Default: insert before the last line (or at end)
    lines.append(line)
    return "\n".join(lines)

def update_yaml_field(fm_str, field_name, old_val, new_val):
    """Replace a YAML field value. Returns modified string."""
    pattern = re.compile(
        rf'^({field_name}:\s*){re.escape(str(old_val))}(\s*)$',
        re.MULTILINE
    )
    return pattern.sub(rf'\g<1>{new_val}\2', fm_str, count=1)

def apply_field_to_file(filepath, field_name, value, verbose=False):
    """Apply a single field to a paper's YAML frontmatter."""
    full_path = os.path.join(VAULT_ROOT, filepath)
    fm_str, body, full_text = read_frontmatter_and_body(full_path)
    if fm_str is None:
        return False

    # Check if field already has a value
    pattern = re.compile(rf'^{field_name}:\s*"?(.+?)"?\s*$', re.MULTILINE)
    existing = pattern.search(fm_str)
    if existing and existing.group(1).strip() not in ("", "null", "~"):
        if verbose:
            print(f"  SKIP {field_name} for {filepath}: already has value")
        return False

    if existing:
        # Field exists but is empty/null — replace it
        new_fm = pattern.sub(f'{field_name}: "{value}"', fm_str, count=1)
    else:
        # Field doesn't exist — insert it in logical position
        # Preferred insertion points by field
        after_map = {
            "doi": "year",
            "pmid": "doi",
            "pmcid": "pmid",
            "issn": "journal",
        }
        after = after_map.get(field_name)
        new_fm = insert_yaml_field(fm_str, field_name, value, after_field=after)

    new_text = f"---\n{new_fm}\n---\n{body}"
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    return True

def apply_open_access_upgrade(filepath, verbose=False):
    """Upgrade open_access from false/unknown to true."""
    full_path = os.path.join(VAULT_ROOT, filepath)
    fm_str, body, full_text = read_frontmatter_and_body(full_path)
    if fm_str is None:
        return False
    
    # Match open_access: false or open_access: unknown
    pattern = re.compile(r'^(open_access:\s*)(false|unknown)\s*$', re.MULTILINE)
    if not pattern.search(fm_str):
        return False
    
    new_fm = pattern.sub(r'\g<1>true', fm_str, count=1)
    new_text = f"---\n{new_fm}\n---\n{body}"
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    if verbose:
        print(f"  UPGRADED open_access → true for {filepath}")
    return True

# ── Phase 1: NCBI ID Converter (DOI → PMID + PMCID) ──────────────────────
def phase1_ncbi_id_converter(papers, verbose=False):
    """For papers with valid DOI but missing PMID/PMCID, query NCBI ID Converter."""
    results = []
    candidates = [p for p in papers if is_valid_doi(p.get("doi"))
                  and (not p.get("pmid") or not p.get("pmcid"))]
    
    if verbose:
        print(f"\n═══ Phase 1: NCBI ID Converter ({len(candidates)} papers) ═══")

    for i, p in enumerate(candidates):
        doi = p["doi"].strip()
        url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={urllib.parse.quote(doi)}&format=json"
        raw = safe_api_call(url, ncbi_limiter)
        if not raw:
            continue
        
        try:
            data = json.loads(raw)
            records = data.get("records", [])
            if not records:
                continue
            rec = records[0]
            
            if rec.get("status") == "error":
                continue
            
            pmid = rec.get("pmid", "")
            pmcid = rec.get("pmcid", "")
            
            if pmid and not p.get("pmid"):
                results.append({
                    "filepath": p["filepath"],
                    "field": "pmid",
                    "value": pmid,
                    "source": "ncbi-idconv",
                    "confidence": 1.0,
                    "title_similarity": 1.0,
                    "year_match": True,
                    "status": "auto-applied"
                })

            if pmcid and not p.get("pmcid"):
                results.append({
                    "filepath": p["filepath"],
                    "field": "pmcid",
                    "value": pmcid,
                    "source": "ncbi-idconv",
                    "confidence": 1.0,
                    "title_similarity": 1.0,
                    "year_match": True,
                    "status": "auto-applied"
                })
            
            if verbose and (pmid or pmcid):
                found = []
                if pmid and not p.get("pmid"):
                    found.append(f"PMID={pmid}")
                if pmcid and not p.get("pmcid"):
                    found.append(f"PMCID={pmcid}")
                if found:
                    print(f"  [{i+1}/{len(candidates)}] {p['filepath'][:50]} → {', '.join(found)}")
        except (json.JSONDecodeError, KeyError, IndexError):
            continue
    
    if verbose:
        pmids = sum(1 for r in results if r["field"] == "pmid")
        pmcids = sum(1 for r in results if r["field"] == "pmcid")
        print(f"  Phase 1 complete: {pmids} PMIDs, {pmcids} PMCIDs found")
    
    return results

# ── Phase 2: CrossRef DOI lookup (for papers missing DOI) ─────────────────
def phase2_crossref(papers, verbose=False):
    """For papers without a valid DOI, search CrossRef by title + author."""
    results = []
    candidates = [p for p in papers if not is_valid_doi(p.get("doi"))]
    
    if verbose:
        print(f"\n═══ Phase 2: CrossRef DOI Lookup ({len(candidates)} papers) ═══")
    
    for i, p in enumerate(candidates):
        title = p.get("title", "")
        if not title or len(title) < 10:
            continue
        
        year = p.get("year")
        author = first_author_surname(p.get("authors", []))
        
        # Build query
        params = {
            "query.bibliographic": title,
            "rows": "3",
            "mailto": MAILTO,
        }
        if author:
            params["query.author"] = author
        
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
        raw = safe_api_call(url, crossref_limiter, timeout=20)
        if not raw:
            if verbose:
                print(f"  [{i+1}/{len(candidates)}] {p['filepath'][:50]} → API error/timeout")
            continue

        try:
            data = json.loads(raw)
            items = data.get("message", {}).get("items", [])
            if not items:
                continue
            
            best_match = None
            best_sim = 0
            
            for item in items[:3]:
                item_titles = item.get("title", [])
                if not item_titles:
                    continue
                item_title = item_titles[0]
                sim = title_similarity(title, item_title)
                
                # Year check
                year_ok = False
                for date_field in ["published-print", "published-online", "created"]:
                    date_parts = item.get(date_field, {}).get("date-parts", [[]])
                    if date_parts and date_parts[0] and date_parts[0][0]:
                        if str(date_parts[0][0]) == str(year):
                            year_ok = True
                            break
                
                if sim > best_sim and sim > 0.85 and year_ok:
                    best_sim = sim
                    best_match = item
                    best_match["_year_ok"] = year_ok
                    best_match["_sim"] = sim
        except (json.JSONDecodeError, KeyError):
            continue

        if not best_match:
            if verbose:
                print(f"  [{i+1}/{len(candidates)}] {p['filepath'][:50]} → no match above threshold")
            continue
        
        doi = best_match.get("DOI", "")
        if not is_valid_doi(doi):
            continue
        
        confidence = best_match["_sim"]
        status = "auto-applied" if confidence > 0.90 else "pending-review"
        
        results.append({
            "filepath": p["filepath"],
            "field": "doi",
            "value": doi,
            "source": "crossref",
            "confidence": round(confidence, 4),
            "title_similarity": round(best_match["_sim"], 4),
            "year_match": True,
            "status": status
        })
        
        # Capture ISSN (prefer electronic)
        issn_types = best_match.get("issn-type", [])
        issn = None
        for it in issn_types:
            if it.get("type") == "electronic":
                issn = it.get("value")
                break
        if not issn and issn_types:
            issn = issn_types[0].get("value")
        if not issn:
            issn_list = best_match.get("ISSN", [])
            if issn_list:
                issn = issn_list[-1]  # last is often electronic

        if issn and not p.get("issn"):
            results.append({
                "filepath": p["filepath"],
                "field": "issn",
                "value": issn,
                "source": "crossref",
                "confidence": round(confidence, 4),
                "title_similarity": round(best_match["_sim"], 4),
                "year_match": True,
                "status": status  # same confidence as DOI match
            })
        
        # Capture publisher if empty
        publisher = best_match.get("publisher", "")
        if publisher and not p.get("publisher"):
            results.append({
                "filepath": p["filepath"],
                "field": "publisher",
                "value": publisher,
                "source": "crossref",
                "confidence": round(confidence, 4),
                "title_similarity": round(best_match["_sim"], 4),
                "year_match": True,
                "status": status
            })
        
        if verbose:
            print(f"  [{i+1}/{len(candidates)}] {p['filepath'][:50]} → DOI={doi} (sim={confidence:.2f}, {status})")
    
    if verbose:
        dois = sum(1 for r in results if r["field"] == "doi")
        issns = sum(1 for r in results if r["field"] == "issn")
        print(f"  Phase 2 complete: {dois} DOIs, {issns} ISSNs found")
    
    return results

# ── Phase 2b: CrossRef ISSN lookup for papers WITH DOI but MISSING ISSN ───
def phase2b_crossref_issn(papers, verbose=False):
    """For papers with DOI but no ISSN, query CrossRef by DOI for ISSN."""
    results = []
    candidates = [p for p in papers if is_valid_doi(p.get("doi")) and not p.get("issn")]
    
    if verbose:
        print(f"\n═══ Phase 2b: CrossRef ISSN Lookup ({len(candidates)} papers with DOI, no ISSN) ═══")
    
    for i, p in enumerate(candidates):
        doi = p["doi"].strip()
        url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}?mailto={MAILTO}"
        raw = safe_api_call(url, crossref_limiter, timeout=15)
        if not raw:
            continue
        
        try:
            data = json.loads(raw)
            item = data.get("message", {})

            # Extract ISSN (prefer electronic)
            issn = None
            issn_types = item.get("issn-type", [])
            for it in issn_types:
                if it.get("type") == "electronic":
                    issn = it.get("value")
                    break
            if not issn and issn_types:
                issn = issn_types[0].get("value")
            if not issn:
                issn_list = item.get("ISSN", [])
                if issn_list:
                    issn = issn_list[-1]
            
            if issn:
                results.append({
                    "filepath": p["filepath"],
                    "field": "issn",
                    "value": issn,
                    "source": "crossref-doi",
                    "confidence": 1.0,
                    "title_similarity": 1.0,
                    "year_match": True,
                    "status": "auto-applied"
                })
                if verbose and (i + 1) % 20 == 0:
                    print(f"  [{i+1}/{len(candidates)}] progress...")
        except (json.JSONDecodeError, KeyError):
            continue

    if verbose:
        print(f"  Phase 2b complete: {len(results)} ISSNs found from DOI lookups")
    
    return results

# ── Phase 3: PubMed ESearch (for papers still missing PMID) ───────────────
def phase3_pubmed_esearch(papers, new_dois, verbose=False):
    """
    For papers still missing PMID after Phases 1-2:
    - If they gained a DOI from Phase 2, try NCBI ID Converter with new DOI
    - Otherwise, search PubMed by title
    """
    results = []
    
    # 3a: Papers that gained a DOI from Phase 2 — try NCBI ID Converter
    new_doi_fps = {m["filepath"]: m["value"] for m in new_dois}
    phase3a_candidates = [p for p in papers
                          if p["filepath"] in new_doi_fps and not p.get("pmid")]
    
    if verbose:
        print(f"\n═══ Phase 3a: NCBI ID Conv for new DOIs ({len(phase3a_candidates)} papers) ═══")

    for i, p in enumerate(phase3a_candidates):
        doi = new_doi_fps[p["filepath"]]
        url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={urllib.parse.quote(doi)}&format=json"
        raw = safe_api_call(url, ncbi_limiter)
        if not raw:
            continue
        try:
            data = json.loads(raw)
            records = data.get("records", [])
            if not records or records[0].get("status") == "error":
                continue
            rec = records[0]
            pmid = rec.get("pmid", "")
            pmcid = rec.get("pmcid", "")
            if pmid:
                results.append({
                    "filepath": p["filepath"], "field": "pmid", "value": pmid,
                    "source": "ncbi-idconv-phase3", "confidence": 1.0,
                    "title_similarity": 1.0, "year_match": True, "status": "auto-applied"
                })
            if pmcid:
                results.append({
                    "filepath": p["filepath"], "field": "pmcid", "value": pmcid,
                    "source": "ncbi-idconv-phase3", "confidence": 1.0,
                    "title_similarity": 1.0, "year_match": True, "status": "auto-applied"
                })
            if verbose and (pmid or pmcid):
                print(f"  [3a] {p['filepath'][:50]} → PMID={pmid} PMCID={pmcid}")
        except (json.JSONDecodeError, KeyError):
            continue

    # 3b: Papers without DOI and without PMID — search PubMed by title
    # Collect filepaths that already have PMID from earlier phases
    gained_pmid_fps = {r["filepath"] for r in results if r["field"] == "pmid"}
    phase3b_candidates = [p for p in papers
                          if not is_valid_doi(p.get("doi"))
                          and p["filepath"] not in new_doi_fps
                          and not p.get("pmid")
                          and p["filepath"] not in gained_pmid_fps]
    
    if verbose:
        print(f"\n═══ Phase 3b: PubMed ESearch by title ({len(phase3b_candidates)} papers) ═══")
    
    for i, p in enumerate(phase3b_candidates):
        title = p.get("title", "")
        if not title or len(title) < 10:
            continue
        
        # Clean title for search
        search_title = re.sub(r'[^\w\s]', ' ', title)
        author = first_author_surname(p.get("authors", []))
        
        term = f"{search_title}"
        if author:
            term += f" {author}"
        
        url = (f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
               f"db=pubmed&term={urllib.parse.quote(term)}&retmode=json&retmax=3")
        raw = safe_api_call(url, ncbi_limiter)
        if not raw:
            continue

        try:
            data = json.loads(raw)
            result = data.get("esearchresult", {})
            count = int(result.get("count", 0))
            idlist = result.get("idlist", [])
            
            if count == 0 or not idlist:
                continue
            
            # Only accept if unambiguous (count=1) for safety
            if count == 1:
                pmid = idlist[0]
                results.append({
                    "filepath": p["filepath"], "field": "pmid", "value": pmid,
                    "source": "pubmed-esearch", "confidence": 0.90,
                    "title_similarity": 0.90, "year_match": True,
                    "status": "auto-applied"
                })
                if verbose:
                    print(f"  [3b] {p['filepath'][:50]} → PMID={pmid} (unambiguous)")
            elif verbose:
                print(f"  [3b] {p['filepath'][:50]} → {count} results, skipped (ambiguous)")
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
    
    if verbose:
        pmids = sum(1 for r in results if r["field"] == "pmid")
        pmcids = sum(1 for r in results if r["field"] == "pmcid")
        print(f"  Phase 3 complete: {pmids} PMIDs, {pmcids} PMCIDs found")
    
    return results

# ── Phase 4: PubMed EFetch (PMID → DOI) ──────────────────────────────────
def phase4_pubmed_efetch(papers, new_pmids, verbose=False):
    """For papers with PMID but missing DOI, fetch DOI from PubMed record."""
    results = []
    
    # Build set of papers that have PMID (existing + newly gained) but no DOI
    new_pmid_map = {m["filepath"]: m["value"] for m in new_pmids}
    candidates = []
    for p in papers:
        pmid = p.get("pmid") or new_pmid_map.get(p["filepath"])
        if pmid and not is_valid_doi(p.get("doi")):
            candidates.append((p, pmid))
    
    if verbose:
        print(f"\n═══ Phase 4: PubMed EFetch PMID→DOI ({len(candidates)} papers) ═══")
    
    for i, (p, pmid) in enumerate(candidates):
        url = (f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
               f"db=pubmed&id={pmid}&retmode=xml")
        raw = safe_api_call(url, ncbi_limiter, timeout=15)
        if not raw:
            continue

        try:
            root = ET.fromstring(raw)
            # Find DOI in ArticleIdList
            for aid in root.iter("ArticleId"):
                if aid.get("IdType") == "doi":
                    doi = aid.text.strip() if aid.text else ""
                    if is_valid_doi(doi):
                        results.append({
                            "filepath": p["filepath"], "field": "doi",
                            "value": doi, "source": "pubmed-efetch",
                            "confidence": 1.0, "title_similarity": 1.0,
                            "year_match": True, "status": "auto-applied"
                        })
                        if verbose:
                            print(f"  [4] {p['filepath'][:50]} → DOI={doi}")
                        break
            
            # Also try to get PMCID from the same record
            if not p.get("pmcid"):
                for aid in root.iter("ArticleId"):
                    if aid.get("IdType") == "pmc":
                        pmcid = aid.text.strip() if aid.text else ""
                        if pmcid:
                            if not pmcid.startswith("PMC"):
                                pmcid = f"PMC{pmcid}"
                            results.append({
                                "filepath": p["filepath"], "field": "pmcid",
                                "value": pmcid, "source": "pubmed-efetch",
                                "confidence": 1.0, "title_similarity": 1.0,
                                "year_match": True, "status": "auto-applied"
                            })
                            break
        except ET.ParseError:
            continue

    if verbose:
        dois = sum(1 for r in results if r["field"] == "doi")
        pmcids = sum(1 for r in results if r["field"] == "pmcid")
        print(f"  Phase 4 complete: {dois} DOIs, {pmcids} PMCIDs found")
    
    return results

# ── Phase 5: Open Access Upgrade ─────────────────────────────────────────
def phase5_open_access_upgrades(papers, all_results, verbose=False):
    """For papers that gained a PMCID, upgrade open_access to true."""
    upgrades = []
    new_pmcids = {r["filepath"] for r in all_results if r["field"] == "pmcid"}
    
    if verbose:
        print(f"\n═══ Phase 5: Open Access Upgrades ({len(new_pmcids)} papers gained PMCID) ═══")
    
    for p in papers:
        if p["filepath"] in new_pmcids:
            oa = p.get("open_access")
            if oa in (False, "false", "unknown", None):
                upgrades.append({
                    "filepath": p["filepath"],
                    "field": "open_access",
                    "value": "true",
                    "source": "pmcid-derived",
                    "confidence": 1.0,
                    "title_similarity": 1.0,
                    "year_match": True,
                    "status": "auto-applied",
                    "previous_value": str(oa) if oa is not None else "null"
                })
                if verbose:
                    print(f"  {p['filepath'][:50]} → open_access: {oa} → true")
    
    if verbose:
        print(f"  Phase 5 complete: {len(upgrades)} open access upgrades")
    
    return upgrades

# ── Main Orchestrator ─────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="IbogaineVault identifier lookup")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Run lookups and generate report without modifying files (default)")
    parser.add_argument("--apply", action="store_true",
                        help="Apply high-confidence (>90%%) matches")
    parser.add_argument("--apply-all", action="store_true",
                        help="Apply all matches above 85%%")
    parser.add_argument("--skip-crossref", action="store_true",
                        help="Skip Phase 2 (CrossRef DOI lookups)")
    parser.add_argument("--skip-issn", action="store_true",
                        help="Skip Phase 2b (CrossRef ISSN lookups for papers with DOI)")
    parser.add_argument("--verbose", action="store_true",
                        help="Print each lookup as it happens")
    args = parser.parse_args()
    
    # --apply or --apply-all overrides --dry-run
    do_apply = args.apply or args.apply_all
    confidence_threshold = 0.85 if args.apply_all else 0.90
    
    start_time = time.time()
    
    # Load papers.json
    if not os.path.exists(PAPERS_JSON):
        print(f"ERROR: {PAPERS_JSON} not found. Run generate_index.py first.")
        sys.exit(1)

    with open(PAPERS_JSON) as f:
        papers_data = json.load(f)
    papers = papers_data["papers"]
    print(f"Loaded {len(papers)} papers from papers.json")
    
    # Detect malformed DOIs
    malformed_dois = []
    for p in papers:
        doi = p.get("doi", "")
        if doi and not is_valid_doi(doi):
            malformed_dois.append(p["filepath"])
            if args.verbose:
                print(f"  MALFORMED DOI: {p['filepath']} → '{doi[:60]}'")
    
    all_results = []
    
    # ── Phase 1 ──
    p1_results = phase1_ncbi_id_converter(papers, verbose=args.verbose)
    all_results.extend(p1_results)
    
    # ── Phase 2 ──
    if not args.skip_crossref:
        p2_results = phase2_crossref(papers, verbose=args.verbose)
        all_results.extend(p2_results)
    else:
        p2_results = []
        if args.verbose:
            print("\n═══ Phase 2: SKIPPED (--skip-crossref) ═══")

    # ── Phase 2b: ISSN from CrossRef for papers with DOI ──
    if not args.skip_issn and not args.skip_crossref:
        p2b_results = phase2b_crossref_issn(papers, verbose=args.verbose)
        all_results.extend(p2b_results)
    else:
        p2b_results = []
        if args.verbose:
            print("\n═══ Phase 2b: SKIPPED ═══")
    
    # ── Phase 3 ──
    new_dois = [r for r in all_results if r["field"] == "doi"]
    p3_results = phase3_pubmed_esearch(papers, new_dois, verbose=args.verbose)
    all_results.extend(p3_results)
    
    # ── Phase 4 ──
    new_pmids = [r for r in all_results if r["field"] == "pmid"]
    p4_results = phase4_pubmed_efetch(papers, new_pmids, verbose=args.verbose)
    all_results.extend(p4_results)
    
    # ── Phase 5: Open Access Upgrades ──
    p5_results = phase5_open_access_upgrades(papers, all_results, verbose=args.verbose)
    all_results.extend(p5_results)

    # ── Apply matches to files ──
    applied_count = 0
    skipped_count = 0
    
    if do_apply:
        print(f"\n{'='*60}")
        print(f"APPLYING matches (threshold: {confidence_threshold})")
        print(f"{'='*60}")
        
        for r in all_results:
            if r["confidence"] < confidence_threshold:
                r["status"] = "pending-review"
                skipped_count += 1
                continue
            
            if r["field"] == "open_access":
                success = apply_open_access_upgrade(r["filepath"], verbose=args.verbose)
            elif r["field"] == "publisher":
                # Publisher updates via targeted string replacement
                full_path = os.path.join(VAULT_ROOT, r["filepath"])
                fm_str, body, full_text = read_frontmatter_and_body(full_path)
                if fm_str and "publisher:" not in fm_str:
                    new_fm = insert_yaml_field(fm_str, "publisher", r["value"], after_field="journal")
                    new_text = f"---\n{new_fm}\n---\n{body}"
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(new_text)
                    success = True
                else:
                    success = False
            else:
                success = apply_field_to_file(r["filepath"], r["field"], r["value"],
                                              verbose=args.verbose)

            if success:
                r["status"] = "applied"
                applied_count += 1
            else:
                r["status"] = "apply-failed"
        
        print(f"\nApplied: {applied_count}, Skipped (below threshold): {skipped_count}")
    else:
        print("\n── DRY RUN — no files modified ──")
        for r in all_results:
            if r["confidence"] >= 0.90:
                r["status"] = "would-auto-apply"
            elif r["confidence"] >= 0.85:
                r["status"] = "pending-review"
            else:
                r["status"] = "below-threshold"
    
    # ── Build report ──
    elapsed = time.time() - start_time
    
    # Count by field
    dois_found = sum(1 for r in all_results if r["field"] == "doi")
    pmids_found = sum(1 for r in all_results if r["field"] == "pmid")
    pmcids_found = sum(1 for r in all_results if r["field"] == "pmcid")
    issns_found = sum(1 for r in all_results if r["field"] == "issn")
    publishers_updated = sum(1 for r in all_results if r["field"] == "publisher")
    oa_upgrades = sum(1 for r in all_results if r["field"] == "open_access")

    # Papers that still have no DOI after all lookups
    found_doi_fps = {r["filepath"] for r in all_results if r["field"] == "doi"}
    no_doi_papers = []
    for p in papers:
        if not is_valid_doi(p.get("doi")) and p["filepath"] not in found_doi_fps:
            # Guess reason
            title = (p.get("title") or "").lower()
            year = p.get("year", 9999)
            fp = p["filepath"].lower()
            if "thesis" in fp or "dissertation" in title:
                reason = "Thesis/dissertation — no DOI expected"
            elif "book" in title or "chapter" in title:
                reason = "Book/book chapter — may not have DOI"
            elif any(x in fp for x in ["journalism", "news", "blog", "editorial"]):
                reason = "Journalism/editorial — no DOI expected"
            elif year < 1990:
                reason = "Pre-DOI era publication (before 1990)"
            elif "guideline" in title or "protocol" in title:
                reason = "Clinical guideline/protocol — may lack DOI"
            else:
                reason = "No CrossRef match above threshold"
            no_doi_papers.append({
                "filepath": p["filepath"],
                "title": p.get("title", ""),
                "year": p.get("year"),
                "reason": reason
            })

    report = {
        "run_date": datetime.now().strftime("%Y-%m-%d"),
        "mode": "apply-all" if args.apply_all else ("apply" if args.apply else "dry-run"),
        "elapsed_seconds": round(elapsed, 1),
        "api_calls": {
            "crossref": crossref_limiter.total_calls,
            "ncbi": ncbi_limiter.total_calls,
            "total": crossref_limiter.total_calls + ncbi_limiter.total_calls
        },
        "summary": {
            "papers_processed": len(papers),
            "dois_found": dois_found,
            "pmids_found": pmids_found,
            "pmcids_found": pmcids_found,
            "issns_found": issns_found,
            "publishers_updated": publishers_updated,
            "open_access_upgrades": oa_upgrades,
            "malformed_dois_found": malformed_dois,
            "applied": applied_count if do_apply else 0,
            "pending_review": sum(1 for r in all_results if r["status"] == "pending-review"),
        },
        "matches": all_results,
        "no_doi_papers": no_doi_papers
    }
    
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"IDENTIFIER LOOKUP COMPLETE")
    print(f"{'='*60}")

    print(f"  DOIs found:            {dois_found}")
    print(f"  PMIDs found:           {pmids_found}")
    print(f"  PMCIDs found:          {pmcids_found}")
    print(f"  ISSNs found:           {issns_found}")
    print(f"  Publishers updated:    {publishers_updated}")
    print(f"  Open access upgrades:  {oa_upgrades}")
    print(f"  Malformed DOIs:        {len(malformed_dois)}")
    print(f"  No DOI (expected):     {len(no_doi_papers)}")
    print(f"  Pending review:        {report['summary']['pending_review']}")
    print(f"  API calls:             {report['api_calls']['total']} "
          f"(CrossRef: {report['api_calls']['crossref']}, "
          f"NCBI: {report['api_calls']['ncbi']})")
    print(f"  Elapsed time:          {elapsed:.0f}s ({elapsed/60:.1f}min)")
    print(f"\n  Report: {REPORT_PATH}")
    
    if do_apply:
        print(f"\n  Files modified: {applied_count}")
    else:
        print(f"\n  ⚠ DRY RUN — run with --apply to modify files")

if __name__ == "__main__":
    main()
