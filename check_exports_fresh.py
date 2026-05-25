#!/usr/bin/env python3
"""check_exports_fresh.py — fail if committed papers.json/papers.csv are stale.

Defect D10: green CI did not mean the committed exports were current (a metadata
change could land without regenerating papers.json/papers.csv). This regenerates
the index to a temp dir and compares it against the committed exports:

  * papers.csv  — must be byte-identical
  * papers.json — must match except for `generated_at` (its timestamp changes
                  on every run, so it is excluded from the comparison)

Exit 1 on any drift. Self-contained (no vault_config import) so it runs both in
Tier 2 (_meta/tools/) and in the Tier-1 projection (copied to repo root).

Usage:
  python3 check_exports_fresh.py [--vault .]
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENERATE = HERE / "generate_index.py"


def main():
    parser = argparse.ArgumentParser(description="Verify committed exports are fresh")
    parser.add_argument("--vault", default=".",
                        help="Vault root holding the committed papers.json/papers.csv (default: .)")
    args = parser.parse_args()

    vault = Path(args.vault).resolve()
    committed_json = vault / "papers.json"
    committed_csv = vault / "papers.csv"
    for f in (committed_json, committed_csv):
        if not f.exists():
            sys.exit(f"check_exports_fresh: missing committed export {f}")

    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [sys.executable, str(GENERATE), "--vault", str(vault), "--output", tmp],
            capture_output=True, text=True)
        if result.returncode != 0:
            sys.exit("check_exports_fresh: regeneration failed:\n"
                     + (result.stderr or result.stdout))
        fresh_json = Path(tmp) / "papers.json"
        fresh_csv = Path(tmp) / "papers.csv"

        if committed_csv.read_bytes() != fresh_csv.read_bytes():
            sys.exit("check_exports_fresh: papers.csv is STALE — regenerate and commit "
                     "(python3 _meta/tools/generate_index.py --vault .).")

        committed = json.loads(committed_json.read_text(encoding="utf-8"))
        fresh = json.loads(fresh_json.read_text(encoding="utf-8"))
        committed.pop("generated_at", None)
        fresh.pop("generated_at", None)
        if committed != fresh:
            sys.exit("check_exports_fresh: papers.json is STALE — regenerate and commit "
                     "(python3 _meta/tools/generate_index.py --vault .).")

    print("check_exports_fresh: PASS — papers.json/papers.csv are current.")


if __name__ == "__main__":
    main()
