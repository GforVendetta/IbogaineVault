#!/usr/bin/env python3
"""
IbogaineVault — DOI Re-verification (BROKEN tier triage)
======================================================
Re-checks DOIs classified as BROKEN by doi_oa_audit.py using GET requests
instead of HEAD requests (many publishers block HEAD).

Produces a triage report separating:
  - FALSE_POSITIVE: DOI resolves via GET (publisher blocked HEAD)
  - GENUINELY_BROKEN: DOI does not resolve via GET either
  - REDIRECT_MISMATCH: DOI resolves but to an unexpected page (e.g. 404 page with 200 status)

Usage:
    python3 doi_reverify.py [--json PATH] [--output PATH] [--delay SECONDS]
"""

import json
import sys
import time
import argparse
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: pip3 install requests")
    sys.exit(1)


# ── User-Agent to avoid bot blocking ──
HEADERS = {
    "User-Agent": "IbogaineVault-DOI-Audit/1.0 (academic research; contact: philip@pangeabiomedics.com)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Known error page patterns (publishers that return 200 for broken pages)
ERROR_PATTERNS = [
    "page not found", "404", "no document found", "the page you requested",
    "this doi cannot be found", "resource not found", "article not found",
]


def reverify_doi(doi, timeout=20):
    """
    Check DOI resolution using GET request with proper User-Agent.
    Returns dict with resolution status and details.
    """
    url = f"https://doi.org/{doi}"
    result = {
        "doi": doi,
        "url": url,
        "resolved": False,
        "final_url": None,
        "status_code": None,
        "error": None,
        "classification": "GENUINELY_BROKEN",
    }

    try:
        resp = requests.get(
            url,
            headers=HEADERS,
            allow_redirects=True,
            timeout=timeout,
            stream=True,  # Don't download full body
        )
        result["status_code"] = resp.status_code
        result["final_url"] = resp.url

        if resp.status_code == 200:
            # Read just the first 2KB to check for error pages
            chunk = resp.raw.read(2048).decode("utf-8", errors="ignore").lower()
            resp.close()

            if any(pat in chunk for pat in ERROR_PATTERNS):
                result["classification"] = "SOFT_404"
                result["error"] = "200 status but error page content"
            else:
                result["resolved"] = True
                result["classification"] = "FALSE_POSITIVE"

        elif resp.status_code in (301, 302, 303, 307, 308):
            # Redirect not followed (shouldn't happen with allow_redirects=True)
            result["classification"] = "REDIRECT_ISSUE"
            result["error"] = f"Redirect {resp.status_code} to {resp.headers.get('Location', 'unknown')}"
            resp.close()

        elif resp.status_code == 404:
            result["classification"] = "GENUINELY_BROKEN"
            result["error"] = "404 Not Found"
            resp.close()

        elif resp.status_code == 403:
            # Some publishers block automated access but DOI is valid
            result["classification"] = "ACCESS_BLOCKED"
            result["error"] = "403 Forbidden (DOI may be valid but access blocked)"
            resp.close()

        elif resp.status_code == 503:
            result["classification"] = "TEMP_UNAVAILABLE"
            result["error"] = "503 Service Unavailable (retry later)"
            resp.close()

        else:
            result["classification"] = "OTHER_ERROR"
            result["error"] = f"HTTP {resp.status_code}"
            resp.close()

    except requests.exceptions.Timeout:
        result["error"] = "Timeout (20s)"
        result["classification"] = "TIMEOUT"
    except requests.exceptions.ConnectionError as e:
        result["error"] = f"Connection error: {str(e)[:100]}"
        result["classification"] = "CONNECTION_ERROR"
    except requests.exceptions.RequestException as e:
        result["error"] = f"Request error: {str(e)[:100]}"

    return result


def main():
    parser = argparse.ArgumentParser(description="Re-verify BROKEN DOIs from IbogaineVault audit")
    parser.add_argument("--json", default="/Users/aretesofia/IbogaineVault/_meta/tools/doi_oa_report.json",
                        help="Path to JSON report from doi_oa_audit.py")
    parser.add_argument("--output", default="/Users/aretesofia/IbogaineVault/_meta/tools/doi_reverify_report.md",
                        help="Output path for triage report")
    parser.add_argument("--delay", type=float, default=1.5,
                        help="Delay between requests in seconds (be polite)")
    args = parser.parse_args()

    # Load report
    with open(args.json, "r") as f:
        all_papers = json.load(f)

    broken = [p for p in all_papers if p.get("tier") == "BROKEN"]
    print(f"Found {len(broken)} BROKEN DOIs to re-verify")
    print(f"Using GET requests with {args.delay}s delay between requests")
    print(f"Estimated time: ~{len(broken) * args.delay / 60:.1f} minutes\n")

    results = []
    for i, paper in enumerate(broken, 1):
        doi = paper["doi"]
        filename = paper["filename"]
        print(f"[{i}/{len(broken)}] {filename} — {doi} ... ", end="", flush=True)

        result = reverify_doi(doi)
        result["filename"] = filename
        result["year"] = paper.get("year", "")
        results.append(result)

        print(f"{result['classification']}" +
              (f" → {result['final_url'][:80]}" if result["resolved"] else
               f" ({result.get('error', '')})" if result.get("error") else ""))

        if i < len(broken):
            time.sleep(args.delay)

    # ── Classify results ──
    buckets = {}
    for r in results:
        cls = r["classification"]
        buckets.setdefault(cls, []).append(r)

    # ── Generate report ──
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# IbogaineVault — DOI Re-verification Triage Report\n",
        f"**Generated:** {now}",
        f"**Method:** GET requests (replacing HEAD from initial audit)",
        f"**DOIs checked:** {len(results)}\n",
        "## Summary\n",
        "| Classification | Count | Action |",
        "|----------------|-------|--------|",
    ]

    class_info = {
        "FALSE_POSITIVE": ("DOI resolves (publisher blocked HEAD)", "No action — mark as resolved"),
        "GENUINELY_BROKEN": ("DOI does not resolve via GET", "Find correct DOI or mark as no-DOI"),
        "SOFT_404": ("200 status but error page content", "Likely broken — manual check"),
        "ACCESS_BLOCKED": ("403 — publisher blocks automation", "Probably valid — manual browser check"),
        "TIMEOUT": ("Request timed out", "Retry later"),
        "TEMP_UNAVAILABLE": ("503 — temporary issue", "Retry later"),
        "CONNECTION_ERROR": ("Connection failed", "Retry later"),
        "REDIRECT_ISSUE": ("Redirect problem", "Manual check"),
        "OTHER_ERROR": ("Other HTTP error", "Manual check"),
    }

    for cls, info in class_info.items():
        count = len(buckets.get(cls, []))
        if count > 0:
            lines.append(f"| {cls} | {count} | {info[1]} |")

    lines.append("")

    # ── Detail sections ──
    for cls, (desc, action) in class_info.items():
        items = buckets.get(cls, [])
        if not items:
            continue
        lines.append(f"## {cls} — {desc} ({len(items)})\n")
        lines.append(f"**Action:** {action}\n")
        lines.append("| File | Year | DOI | Final URL / Error |")
        lines.append("|------|------|-----|-------------------|")
        for r in sorted(items, key=lambda x: x.get("year", "")):
            final = r.get("final_url", r.get("error", "—"))
            if final and len(final) > 80:
                final = final[:77] + "..."
            lines.append(f"| {r['filename']} | {r.get('year', '')} | {r['doi']} | {final} |")
        lines.append("")

    # ── Write report ──
    report_text = "\n".join(lines)
    with open(args.output, "w") as f:
        f.write(report_text)
    print(f"\n{'='*60}")
    print(f"Report written to: {args.output}")

    # ── Also write JSON for programmatic use ──
    json_path = args.output.replace(".md", ".json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"JSON written to:   {json_path}")

    # ── Summary ──
    print(f"\n{'='*60}")
    print("SUMMARY:")
    for cls in class_info:
        count = len(buckets.get(cls, []))
        if count > 0:
            print(f"  {cls:20s}: {count}")
    fp = len(buckets.get("FALSE_POSITIVE", []))
    genuinely = len(results) - fp
    print(f"\n  False positive rate: {fp}/{len(results)} ({fp/len(results)*100:.0f}%)")
    print(f"  Genuinely need attention: {genuinely}")


if __name__ == "__main__":
    main()
