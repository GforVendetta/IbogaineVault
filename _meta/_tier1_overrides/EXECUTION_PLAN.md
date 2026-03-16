# IbogaineVault-Tier1 Ship Execution Plan

**Date:** 2026-03-16
**Goal:** Fix all blockers, ship Tier 1 public, get Zenodo DOI to Martijn Arns

---

## Architecture: The Override System

The sync script currently does a naive rsync that overwrites all Tier-1-specific
fixes on every run. This is the root cause of every "fixed but unfixed" issue.

**Solution:** Two mechanisms added to `sync_tier1.sh`:

1. **Override files** in `_meta/_tier1_overrides/` — completely different
   documents that replace the working vault version after rsync. For files
   where Tier 1 needs a fundamentally different document (e.g. _meta/README.md).

2. **Post-sync transforms** — targeted sed/awk operations in the sync script
   for surgical line-level edits (wikilink counts, Pangea references, scope
   enums). These are idempotent and auditable.

The overrides directory is excluded from rsync (never appears in Tier 1).

---

## Session 1: Sync Script v2 + Contamination Cleanup (45 min)

### 1a. Create override file: _meta/README.md
Already done — `_meta/_tier1_overrides/_meta_README.md`

### 1b. Upgrade sync_tier1.sh

Add after the existing Pangea wikilink stripping block:

```bash
# --- Post-sync: Apply Tier 1 overrides ---
echo "Applying Tier 1 overrides..."
OVERRIDES="${SOURCE}_meta/_tier1_overrides"

# Override: _meta/README.md (completely different document for Tier 1)
if [ -f "${OVERRIDES}/_meta_README.md" ]; then
    cp "${OVERRIDES}/_meta_README.md" "${DEST}_meta/README.md"
    echo -e "${GREEN}✓ Override: _meta/README.md${NC}"
fi

# --- Post-sync: Tier 1 content transforms ---
echo "Running Tier 1 content transforms..."

# T1: Cross-reference count (working vault ~4,900 → Tier 1 ~3,400)
for gfile in README.md CONTRIBUTING.md CHANGELOG.md; do
    if [ -f "${DEST}${gfile}" ]; then
        sed -i '' 's/4,400+ cross-references/3,400+ cross-references/g' "${DEST}${gfile}"
        sed -i '' 's/~4,400 cross-references/~3,400 cross-references/g' "${DEST}${gfile}"
        sed -i '' 's/| Cross-references | ~4,400 |/| Cross-references | ~3,400 |/g' "${DEST}${gfile}"
    fi
done
echo -e "${GREEN}✓ T1: Cross-reference counts corrected${NC}"

# T2: schema_registry.yml — strip transcript_meeting block + pangea scope
if [ -f "${DEST}_meta/schema_registry.yml" ]; then
    # Remove transcript_meeting block (from "  transcript_meeting:" to next top-level key or blank line before next block)
    python3 -c "
import re
with open('${DEST}_meta/schema_registry.yml') as f:
    content = f.read()
# Strip transcript_meeting block
content = re.sub(r'\n  transcript_meeting:.*?(?=\n  \w|\n[a-z]|\Z)', '', content, flags=re.DOTALL)
# Strip pangea from scopes
content = content.replace('    - pangea     # Internal/operational\n', '')
with open('${DEST}_meta/schema_registry.yml', 'w') as f:
    f.write(content)
"
    echo -e "${GREEN}✓ T2: schema_registry.yml sanitised${NC}"
fi

# T3: validate_vault.py — strip pangea scope + TODO comments
if [ -f "${DEST}validate_vault.py" ]; then
    sed -i '' 's/VALID_SCOPES = {"pangea", "published"}/VALID_SCOPES = {"published"}/' "${DEST}validate_vault.py"
    sed -i '' '/^\s*\[ \].*TODO/d' "${DEST}validate_vault.py"
fi
echo -e "${GREEN}✓ T3: validate_vault.py sanitised${NC}"

# T4: Clare Wilkins MOC — strip "Internal Documents" section
if [ -f "${DEST}MOCs/Clare_Wilkins_MOC.md" ]; then
    sed -i '' '/^### Internal Documents$/,/^### /{/^### [^I]/!d;}' "${DEST}MOCs/Clare_Wilkins_MOC.md"
    # Also clean the "Pangea consultation model" row in the trajectory table
    sed -i '' '/Pangea consultation model/d' "${DEST}MOCs/Clare_Wilkins_MOC.md"
fi
echo -e "${GREEN}✓ T4: Clare Wilkins MOC cleaned${NC}"

# T5: Howard Lotsof MOC — clean "Pangea philosophy" line
if [ -f "${DEST}MOCs/Howard_Lotsof_MOC.md" ]; then
    sed -i '' 's/| Harm reduction orientation | ICEERS, GITA, Pangea philosophy |/| Harm reduction orientation | ICEERS, GITA philosophy |/' "${DEST}MOCs/Howard_Lotsof_MOC.md"
fi
echo -e "${GREEN}✓ T5: Howard Lotsof MOC cleaned${NC}"

# T6: Nardou2023 — strip parenthetical Pangea Biomedics commentary
NARDOU=$(find "${DEST}" -name "Nardou2023*" -type f)
if [ -n "$NARDOU" ]; then
    sed -i '' 's/ (an entity associated with Pangea Biomedics)//' "$NARDOU"
fi
echo -e "${GREEN}✓ T6: Nardou2023 cleaned${NC}"

echo ""
```

### 1c. Run upgraded sync + verify

```bash
cd /Users/aretesofia/IbogaineVault
bash _meta/tools/sync_tier1.sh
cd /Users/aretesofia/IbogaineVault-Tier1
# Verify fixes stuck:
grep "4,400" README.md CONTRIBUTING.md CHANGELOG.md  # should return nothing
grep "Pangea" _meta/schema_registry.yml               # should return nothing
grep "transcript_meeting" _meta/schema_registry.yml    # should return nothing
grep "pangea" validate_vault.py                        # should return nothing
grep "Internal Documents" MOCs/Clare_Wilkins_MOC.md    # should return nothing
cat _meta/README.md | head -5                          # should be Tier 1 version
```

---

## Session 2: Copyright Format Audit + Reconversions (1-2 hours)

### 2a. Identify all non-OA papers in academic format

The format audit already identified 15 "ACADEMIC ONLY" papers (no Key Findings /
Clinical Implications sections). Of these, the copyright risks are:

| Paper | Lines | Publisher | Risk |
|-------|-------|-----------|------|
| Mash2000 | 776 | Wiley (NYAS) | 🔴 HIGH — no DOI, full numbered sections |
| Underwood2021 | 838 | J Psychedelic Studies | 🟡 Check OA status |
| Bastiaans2004 | 537 | Unknown (PURPLE) | 🟡 Check if thesis/grey lit |
| Kock2022 | 459 | Elsevier (JSAT) | 🟡 Has PMID, no PMCID |
| Alper2007 | 346 | Unknown | 🟡 Check publisher |
| Ona2024 | 643 | PhD Thesis | 🟢 Theses freely available |
| Uzelac2024 | 339 | MDPI (OA) | 🟢 OA journal |
| Faerman2025 | 291 | Preprint | 🟢 Preprint |

### 2b. Reconvert high-risk papers to vault analytical format

At minimum: **Mash2000** (776 lines, Wiley, non-OA, no DOI).
Probably: **Kock2022** (459 lines, Elsevier) and **Alper2007** if non-OA.
Each reconversion takes ~20 min using the copyright reconversion workflow.

### 2c. Run n-gram triage on remaining ACADEMIC ONLY papers

If the source PDF exists, run the triage script to verify the body text isn't
near-verbatim. This catches papers the previous Phase 0C may have missed.

---

## Session 3: Final Validation + Ship (30 min)

### 3a. PK-PD Hub clinical recommendation

The Aotearoa paragraph in Hub_PK-PD_Synthesis.md is excellent clinical reasoning
but contains imperative treatment recommendations ("should receive... as an
absolute standard") in a vault that says "this is not medical advice."

OPTIONS:
- A: Move the whole paragraph to Tier 2 only (add to sync excludes as sed deletion)
- B: Soften the language ("this analysis suggests..." rather than "should receive")
- C: Keep as-is with explicit caveat ("The following represents the curator's
  analysis, not clinical guidance")

Recommend Option A — it's the safest. The paragraph is Pangea-contextual and
clinical in nature. It belongs in Tier 2.

### 3b. GREEN Hub Pangea framing

Soften "Clare Wilkins (Pangea Biomedics) developed..." to
"Clare Wilkins developed... ([[Wilkins2017|Wilkins et al. 2017]])"
via sed in sync script.

### 3c. CITATION.cff date-released

Update to actual ship date.

### 3d. Final validation run

```bash
cd /Users/aretesofia/IbogaineVault-Tier1
python3 validate_vault.py --summary
# Verify: 0 errors, 297 papers
grep -rl "Pangea_Ops" --include="*.md" .  # should return 0
grep -rn "4,400" --include="*.md" .        # should return 0
grep -rn "Not yet transcribed" .           # should return 0
```

### 3e. Git commit + push + flip public

```bash
git add .
git commit -m "Pre-release: sync v2, copyright reconversions, contamination cleanup"
git push
# Then: GitHub → Settings → Change visibility → Public
# Then: Zenodo integration → DOI
# Then: Email Martijn
```

---

## Priority Order (if time is limited)

1. **Session 1 (sync script v2)** — MUST DO. Prevents all future regressions.
2. **Mash2000 reconversion** — MUST DO. Highest copyright risk in the vault.
3. **Run sync + verify** — MUST DO. Confirms everything works.
4. **Other reconversions** — SHOULD DO (Kock2022, Alper2007 if non-OA).
5. **PK-PD Hub paragraph** — SHOULD DO. Clinical language in "not medical advice" vault.
6. **GREEN Hub framing** — NICE TO HAVE.
7. **CITATION.cff date** — Do on ship day.
