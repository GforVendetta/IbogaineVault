#!/usr/bin/env bash
# sync_tier1.sh — Populate Tier 1 distribution directory from working vault
# 
# Usage: bash _meta/tools/sync_tier1.sh
# Run from anywhere — paths are absolute.
#
# This script is IDEMPOTENT — safe to run repeatedly. It uses rsync to mirror
# the working vault into the Tier 1 directory. Files removed from the working
# vault will be removed from Tier 1 on next run.
#
# The Tier 1 directory is the GitHub repo. The working vault is the primary
# clinical instrument. This script is the air gap between them.
#
# SECURITY MODEL:
#   _meta/  → ALLOWLIST (only explicitly listed files sync; new files excluded by default)
#   rest    → DENYLIST  (everything syncs unless explicitly excluded)
#
# The _meta/ allowlist is self-sealing: adding a new file to _meta/ in the
# working vault does NOT leak it to Tier 1. You must add it to the --include
# list in the rsync command AND to META_ALLOWED in the verification section.

set -euo pipefail

SOURCE="/Users/aretesofia/IbogaineVault/"
DEST="/Users/aretesofia/IbogaineVault-Tier1/"

# Colours for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No colour

echo "═══════════════════════════════════════════════════"
echo "  IbogaineVault Tier 1 Sync"
echo "  Source: ${SOURCE}"
echo "  Dest:   ${DEST}"
echo "═══════════════════════════════════════════════════"
echo ""

# --- Pre-flight checks ---
if [ ! -d "$SOURCE" ]; then
    echo -e "${RED}ERROR: Source directory does not exist: ${SOURCE}${NC}"
    exit 1
fi

if [ ! -d "$DEST" ]; then
    echo -e "${RED}ERROR: Destination directory does not exist: ${DEST}${NC}"
    echo "Create it first: mkdir -p ${DEST}"
    exit 1
fi

# --- Rsync (denylist for top-level; allowlist for _meta/) ---
echo "Syncing files..."
rsync -av --delete-excluded \
    --filter='P .git/' \
    --filter='P .gitignore' \
    --exclude='Pangea_Ops/' \
    --exclude='Clinical_Guidelines/Pangea/' \
    --exclude='Collaborator_Research/' \
    --exclude='Cowork_Outputs/' \
    --exclude='.obsidian/' \
    --exclude='.local/' \
    --exclude='.trash/' \
    --exclude='_builds/' \
    --exclude='_archive/' \
    --exclude='copilot/' \
    --exclude='Other/Strategic_Implementation_Benzodiazepines_CBD.md' \
    --exclude='Other/deLugo2025_Kush_Sierra_Leone_Synthetics.md' \
    --include='_meta/README.md' \
    --include='_meta/schema_registry.yml' \
    --include='_meta/Tag_Taxonomy.md' \
    --include='_meta/VAULT_PRINCIPLES.md' \
    --include='_meta/VAULT_ARCHITECTURE.md' \
    --exclude='_meta/*' \
    --exclude='CLAUDE.md' \
    --exclude='Untitled.*' \
    --exclude='*.pdf' \
    --exclude='*.zip' \
    --exclude='*.plugin' \
    --exclude='*.tar.gz' \
    --exclude='.DS_Store' \
    --exclude='.copilot-index/' \
    --exclude='.smart-env/' \
    "$SOURCE" "$DEST"

echo ""

# --- Post-sync: explicitly remove file-level exclusions ---
# macOS rsync --delete-excluded doesn't reliably remove individual excluded files
# that already exist in the destination. Belt-and-braces deletion.
EXCLUDED_FILES=(
    "Other/Strategic_Implementation_Benzodiazepines_CBD.md"
    "Other/deLugo2025_Kush_Sierra_Leone_Synthetics.md"
)
for exfile in "${EXCLUDED_FILES[@]}"; do
    if [ -f "${DEST}${exfile}" ]; then
        rm -f "${DEST}${exfile}"
        echo -e "${GREEN}✓ Removed excluded file: ${exfile}${NC}"
    fi
done

echo ""
echo "── Sync complete ──"
echo ""

# --- Post-sync: strip Pangea_Ops wikilinks from Tier 1 files ---
# Working vault hubs link to Pangea_Ops/ content (Ibogaine Stories transcripts,
# Noller Q&A, internal calls). These targets don't exist in Tier 1, so we strip
# the wikilinks to avoid broken references. Handles both piped and unpiped forms:
#   [[Pangea_Ops/path/to/file|Display Text]]  →  Display Text
#   [[Pangea_Ops/path/to/file]]               →  (removed entirely)
echo "Stripping Pangea_Ops wikilinks from Tier 1..."
STRIPPED=0
while IFS= read -r -d '' mdfile; do
    if grep -q '\[\[Pangea_Ops/' "$mdfile"; then
        # Piped form: [[Pangea_Ops/...|Display Text]] → Display Text
        sed -i '' 's/\[\[Pangea_Ops\/[^]|]*|\([^]]*\)\]\]/\1/g' "$mdfile"
        # Unpiped form: [[Pangea_Ops/...]] → (empty string)
        sed -i '' 's/\[\[Pangea_Ops\/[^]]*\]\]//g' "$mdfile"
        STRIPPED=$((STRIPPED + 1))
    fi
done < <(find "$DEST" -name "*.md" -print0)
if [ "$STRIPPED" -gt 0 ]; then
    echo -e "${GREEN}✓ Stripped Pangea_Ops wikilinks from ${STRIPPED} file(s)${NC}"
else
    echo -e "${GREEN}✓ No Pangea_Ops wikilinks found (clean)${NC}"
fi
echo ""
# Only flags files where scope: pangea appears in the YAML frontmatter (between --- delimiters),
# NOT in body text that merely documents or references the field.
echo "Running scope:pangea YAML frontmatter safety sweep..."
PANGEA_HITS=""
while IFS= read -r -d '' mdfile; do
    # Extract YAML frontmatter (between first --- and second ---) and check for scope: pangea
    if awk '/^---$/{n++; next} n==1{print} n>=2{exit}' "$mdfile" | grep -q "^scope: pangea"; then
        PANGEA_HITS="${PANGEA_HITS}${mdfile}\n"
    fi
done < <(find "$DEST" -name "*.md" -print0)

if [ -n "$PANGEA_HITS" ]; then
    echo -e "${RED}╔═══════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  SAFETY FAILURE: scope:pangea found in Tier 1 ║${NC}"
    echo -e "${RED}╠═══════════════════════════════════════════════╣${NC}"
    echo -e "$PANGEA_HITS" | while read -r f; do
        [ -n "$f" ] && echo -e "${RED}║  $f${NC}"
    done
    echo -e "${RED}╚═══════════════════════════════════════════════╝${NC}"
    echo ""
    echo "These files have scope:pangea in their YAML frontmatter — Tier 2 content."
    echo "Fix the source vault, then re-run this script."
    exit 1
fi
echo -e "${GREEN}✓ No scope:pangea in YAML frontmatter — Tier 1 clean${NC}"
echo ""

# --- Verification summary ---
echo "── Verification ──"

# Check excluded directories don't exist
FAIL=0
for dir in Pangea_Ops Clinical_Guidelines/Pangea Collaborator_Research Cowork_Outputs .obsidian .local .trash _builds _archive copilot; do
    if [ -d "${DEST}${dir}" ]; then
        echo -e "${RED}✗ EXCLUDED directory present: ${dir}/${NC}"
        FAIL=1
    fi
done

# Check top-level excluded files
if [ -f "${DEST}CLAUDE.md" ]; then
    echo -e "${RED}✗ EXCLUDED file present: CLAUDE.md${NC}"
    FAIL=1
fi

# Check _meta/ contains ONLY allowlisted files (self-sealing verification)
# UPDATE THIS LIST when adding new files to the rsync --include list above.
META_ALLOWED="README.md schema_registry.yml Tag_Taxonomy.md VAULT_ARCHITECTURE.md VAULT_PRINCIPLES.md"
if [ -d "${DEST}_meta" ]; then
    while IFS= read -r -d '' item; do
        fname=$(basename "$item")
        if ! echo "$META_ALLOWED" | grep -qw "$fname"; then
            echo -e "${RED}✗ UNLISTED file in _meta/: ${fname}${NC}"
            FAIL=1
        fi
    done < <(find "${DEST}_meta" -maxdepth 1 -not -type d -not -name '.DS_Store' -print0)
    while IFS= read -r -d '' subdir; do
        dname=$(basename "$subdir")
        echo -e "${RED}✗ UNLISTED directory in _meta/: ${dname}/${NC}"
        FAIL=1
    done < <(find "${DEST}_meta" -mindepth 1 -maxdepth 1 -type d -print0)
else
    echo -e "${YELLOW}⚠ _meta/ directory missing from Tier 1${NC}"
fi

# Check no PDFs leaked
PDF_COUNT=$(find "$DEST" -name "*.pdf" 2>/dev/null | wc -l | tr -d ' ')
if [ "$PDF_COUNT" -gt 0 ]; then
    echo -e "${RED}✗ ${PDF_COUNT} PDF file(s) found in Tier 1${NC}"
    FAIL=1
fi

# Check governance files present
for file in README.md LICENSE CITATION.cff CONTRIBUTING.md CHANGELOG.md GETTING_STARTED.md HOME.md _meta/README.md _meta/schema_registry.yml _meta/Tag_Taxonomy.md _meta/VAULT_PRINCIPLES.md _meta/VAULT_ARCHITECTURE.md; do
    if [ -f "${DEST}${file}" ]; then
        echo -e "${GREEN}✓ ${file}${NC}"
    else
        echo -e "${YELLOW}⚠ Missing governance file: ${file}${NC}"
    fi
done

if [ "$FAIL" -eq 0 ]; then
    echo ""

    # --- Post-sync: Generate machine-readable index against Tier 1 ---
    # CRITICAL: Index is generated against DEST (Tier 1), not SOURCE (working vault).
    # The index must reflect exactly what a Tier 1 consumer sees.
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    echo "Generating machine-readable index (papers.json + papers.csv)..."
    if python3 "$SCRIPT_DIR/generate_index.py" --vault "$DEST" --output "$DEST"; then
        echo -e "${GREEN}✓ Index generated successfully${NC}"
    else
        echo -e "${RED}✗ Index generation failed${NC}"
        exit 1
    fi
    echo ""

    # --- Post-sync: Copy validate_vault.py to Tier 1 root (stripped of Tier 2 dirs) ---
    echo "Copying validate_vault.py to Tier 1 (stripping Tier 2 references)..."
    cp "$SCRIPT_DIR/validate_vault.py" "${DEST}validate_vault.py"
    # Strip Tier 2 directory names from skip_dirs and docstring
    sed -i '' \
        -e 's/Excludes .obsidian\/, .copilot-index\/, .smart-env\/, _archive\/, _builds\/, copilot\/, .git\/\./Excludes .obsidian\/, .copilot-index\/, .smart-env\/, .git\/\./' \
        -e 's/skip_dirs = {".obsidian", ".copilot-index", ".smart-env", "_archive",/skip_dirs = {".obsidian", ".copilot-index", ".smart-env",/' \
        -e 's/                 "_builds", "copilot", ".git", ".local", "Cowork_Outputs",/                 ".git", ".local", "node_modules"}/' \
        -e 's/                 "Collaborator_Research", "Pangea_Ops", "node_modules"}//' \
        "${DEST}validate_vault.py"
    echo -e "${GREEN}✓ validate_vault.py copied and sanitised${NC}"

    # --- Post-sync: Copy generate_index.py to Tier 1 root (for agent use) ---
    echo "Copying generate_index.py to Tier 1..."
    cp "$SCRIPT_DIR/generate_index.py" "${DEST}generate_index.py"
    echo -e "${GREEN}✓ generate_index.py copied${NC}"
    echo ""

    # Verify generated files
    GEN_FAIL=0
    for file in validate_vault.py generate_index.py papers.json papers.csv; do
        if [ -f "${DEST}${file}" ]; then
            echo -e "${GREEN}✓ ${file}${NC}"
        else
            echo -e "${RED}✗ Missing generated file: ${file}${NC}"
            GEN_FAIL=1
        fi
    done
    echo ""

    if [ "$GEN_FAIL" -eq 1 ]; then
        echo -e "${RED}═══════════════════════════════════════════════════${NC}"
        echo -e "${RED}  Tier 1 sync FAILED — generated files missing${NC}"
        echo -e "${RED}═══════════════════════════════════════════════════${NC}"
        exit 1
    fi

    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Tier 1 sync PASSED — ready for git commit${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo ""
    echo "Next steps:"
    echo "  cd ${DEST}"
    echo "  git add ."
    echo "  git commit -m \"your message\""
    echo "  git push"
else
    echo ""
    echo -e "${RED}═══════════════════════════════════════════════════${NC}"
    echo -e "${RED}  Tier 1 sync FAILED — fix issues above${NC}"
    echo -e "${RED}═══════════════════════════════════════════════════${NC}"
    exit 1
fi
