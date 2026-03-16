---
title: "Tier 1 Pre-Release Audit — 15 March 2026"
type: audit-report
created: 2026-03-15
scope: IbogaineVault-Tier1
---

# IbogaineVault-Tier1 Pre-Publication Audit

**Date:** 15 March 2026
**Scope:** Everything in `/Users/aretesofia/IbogaineVault-Tier1/` — what ships to the public.
**Auditor approach:** Martijn Arns (academic reviewer) × Ken Alper (forensic, analytical)

---

## Vault Stats at Audit Time

| Metric | Value |
|--------|-------|
| Total markdown files | 320 |
| Year-dir papers | 257 |
| Other/ | 22 |
| Primary_Sources/ | 10 |
| Clinical_Guidelines/ | 4 |
| Industry_Documents/ | 4 |
| **Total content files** | **297** |
| Total wikilinks | 3,366 |
| papers.json entries | 297 |
| papers.csv rows | 297 |
| YAML parse errors | 0 |
| Non-canonical tags | 0 |
| Year/YAML mismatches | 0 |

### Category Distribution (all content files)

| Category | Count | HOME.md claim |
|----------|-------|---------------|
| ORANGE | 120 | ~120 ✓ |
| BLUE | 50 | ~50 ✓ |
| RED | 47 | ~47 ✓ |
| WHITE | 41 | ~42 ✓ |
| PURPLE | 21 | ~21 ✓ |
| GREEN | 18 | ~20 ✓ |

---

## SEVERITY KEY

- 🔴 **BLOCKER** — Cannot ship. Destroys credibility or leaks internal content.
- 🟡 **SIGNIFICANT** — Should fix before flip. An academic reviewer would notice.
- 🟢 **MINOR** — Fix if time permits. Won't block release but worth cleaning.

---

## 🔴 BLOCKER 1: `_meta/README.md` is the Tier 2 operational document

The sync script copies `_meta/README.md` from the working vault **without sanitisation**. It contains:

- References to `WORKLOG.md`, `ROADMAP.md`, `conversion_manifest.md`, `transcript_manifest.md`, `NLQ_ARCHITECTURE.md` — **none of which exist in Tier 1**
- References to `Cowork_Outputs/`, `_builds/pangea-ibovault/` (Cowork plugin v2.3.0), `_archive/`, `copilot/` — all internal tooling
- Uses the wrong name: **"IbogaVault"** instead of "IbogaineVault"
- The "For Claude" section with operational instructions

**Fix:** Write a new Tier 1-specific `_meta/README.md` describing only the 5 files that exist in Tier 1's `_meta/`.

---

## 🔴 BLOCKER 2: Wikilink count overclaim — 4,400 vs 3,366 (31% inflation)

| Document | Claim | Actual |
|----------|-------|--------|
| README.md L5 | "4,400+ cross-references" | 3,366 |
| CONTRIBUTING.md L76 | "~4,400 cross-references" | 3,366 |
| CHANGELOG.md stats table | "~4,400" | 3,366 |

**Fix:** Replace all instances with `~3,400 cross-references`.

---

## 🔴 BLOCKER 3: `schema_registry.yml` references `Pangea_Ops/`

Line 78: `- "Pangea_Ops/Pangea_Internal_Calls/*.md"` in the `transcript_meeting` schema block.

**Fix:** Strip `transcript_meeting` block from Tier 1 version. See downstream analysis note — no Tier 1 content uses this schema.

---

## 🟡 SIGNIFICANT 4: 5 broken wikilinks remain

| Source | Broken Target | Correct Target |
|--------|--------------|----------------|
| `2015/Glue2015_Ibogaine_CYP2D6_Activity.md` | `2015/Glue2015_Ascending_Dose_Noribogaine_Safety` | `2015/Glue2015_Noribogaine_Ascending_Doses` |
| `2015/Glue2015_Ibogaine_CYP2D6_Activity.md` | `2024/Knuijver2024_CYP2D6_Ibogaine_Cardiac_Risk` | `2024/Knuijver2024_Pharmacokinetics_Pharmacodynamics_Ibogaine_OUD_Patients` (verify) |
| `2023/Boukandou2023_...Iboga_Alkaloids.md` | `2016/Alper2016_hERG_Blockade_Iboga_Alkaloids` | `2016/Alper2016_hERG_Blockade` |
| `GETTING_STARTED.md` | `[[wikilinks]]` | Convert to inline code |
| `_meta/VAULT_ARCHITECTURE.md` | `[[wikilinks]]` | Convert to inline code |

---

## 🟡 SIGNIFICANT 5: HOME.md heading anchor broken

`[[GETTING_STARTED#How to Find Things]]` (×2) targets non-existent heading.
Actual heading: `## How to Find Things (Obsidian)`.

**Fix:** Align heading or link.

---

## 🟡 SIGNIFICANT 6: `validate_vault.py` leaks

- L100: `VALID_SCOPES = {"pangea", "published"}` — "pangea" should be stripped
- L13-15: TODO comments for unimplemented features
- L360-362: References to `.copilot-index/` in docstring (cosmetic)

---

## 🟡 SIGNIFICANT 7: CHANGELOG.md stats table wrong counts

Cross-references claim: ~4,400 (should be ~3,400)
Total documents: 300 (acceptable — actual is 297)

---

## 🟡 SIGNIFICANT 8: 58 email addresses in paper bodies

Mostly corresponding author emails from published papers. Low risk but creates scraping target.

---

## 🟢 MINOR 9: CITATION.cff date-released 2026-03-14

Update to actual release date.

---

## 🟢 MINOR 10: .DS_Store in repo root

Gitignored, untracked. No action needed.

---

## 🟢 MINOR 11: setup.sh bare pip install

`pip install pyyaml` may fail on Python 3.12+. Use `python3 -m pip install pyyaml`.

---

## 🟢 MINOR 12: ICEERS report 1,502 lines

Longest document. Verify copyright status supports full inclusion.

---

## 🟢 MINOR 13: Shawn2012/Warrick2012 duplicate DOI

Known allowlisted case. No action.

---

## CLEAN (passed checks)

- YAML integrity: 0 parse errors, all required fields present
- Category counts match HOME.md claims (with tilde)
- Tag canonicality: all 59 in-use tags from canonical 62
- papers.json: 297 entries, all filepaths resolve
- papers.csv: 297 rows, correct header
- No absolute path leaks
- No Pangea_Ops directory
- No CLAUDE.md
- No scope:pangea in any YAML frontmatter
- Pangea_Ops wikilink stripping working
- No stub/empty papers
- Year/YAML year consistency: zero mismatches
- DeRienzo chapters: 17 present, referenced from hubs and MOCs
- GitHub URLs consistent

---

## TODO: Additional audits needed

- [ ] GitHub rendering quality check — how do hubs/papers actually look?
- [ ] Copyright deep dive — verbatim content, OA vs non-OA compliance
- [ ] Quartz assessment — is GitHub rendering sufficient or is web publishing needed?
- [ ] Downstream analysis of BLOCKER 3 (Pangea_Ops in schema_registry.yml)

---

## APPENDIX A: Pangea_Ops Downstream Analysis

**Question:** Does stripping `transcript_meeting` schema from Tier 1's schema_registry.yml break anything?

**Answer: No. Zero downstream consequences.**

- All 10 Primary_Sources files use `scope: published` (none use `scope: pangea`)
- No Tier 1 file uses document types from transcript_meeting (`meeting-transcript`, `internal-call`, `planning-session`)
- The `transcript_meeting` schema's location pattern is `Pangea_Ops/Pangea_Internal_Calls/*.md` — directory doesn't exist in Tier 1
- `validate_vault.py` doesn't specifically reference `transcript_meeting`
- Safe to strip entire block.

---

## APPENDIX B: GitHub Rendering Assessment

### What works
- **README.md** uses only markdown links (0 wikilinks) — renders perfectly on GitHub. This is the entry point and it's clean.
- **Category table** in README links to all 6 hub files via markdown links — all resolve.
- **YAML frontmatter** renders as GitHub's metadata table — verbose but functional.
- **Mermaid diagrams** (25 papers) render natively on GitHub.
- **LaTeX math** (~955 expressions) renders on GitHub (basic support).
- **HOME.md** has a note redirecting GitHub users to README.

### What degrades
- **3,366 wikilinks** across 296 files show as raw `[[text]]` on GitHub — not clickable.
- **35 escaped-pipe wikilinks** (`[[file\|alias]]`) render as ugly `[[file\|alias]]` in tables — worst case scenario for display.
- **Obsidian callouts** (13 across 10 files) render as plain blockquotes — content preserved but formatting lost.
- **7 .base files** (Obsidian Properties databases) don't render at all on GitHub.
- **Hub navigation** relies entirely on wikilinks — the narrative synthesis text is readable but navigation is broken.

### Assessment: Is GitHub sufficient for Martijn Arns?

**YES — with caveats.** The README→Hubs→Papers path works because README uses markdown links to hubs. Once inside a hub, the wikilinks to papers appear as `[[2024/Cherian2024_Magnesium_Ibogaine_TBI]]` — not clickable but the path is visible, and a reader can manually navigate to `2024/Cherian2024_Magnesium_Ibogaine_TBI.md`. The content is fully readable. The YAML metadata tables render. The paper bodies render.

**Quartz would be nice-to-have but is NOT blocking.** The vault's primary value proposition to Martijn is:
1. The structured metadata (queryable via papers.json)
2. The cross-reference network (visible even as plain text wikilinks)
3. The cardiac safety evidence synthesis (readable in hubs)

None of these require Quartz. A researcher looking at `papers.json` programmatically gets full value. A researcher reading hubs on GitHub gets 80% of the value. Quartz adds the clickable navigation layer — nice, but not essential for a first release.

---

## APPENDIX C: Copyright Deep Dive

### The Problem: `open_access` field not populated

**Zero** of 297 papers have the `open_access` field in their YAML. The COPYRIGHT.md claims precise numbers (~97 OA, ~87 non-OA from major publishers) that cannot be programmatically verified. This is a metadata gap.

### Publisher × Format Cross-Tabulation

The vault contains papers in two body formats:
1. **Vault analytical** — Key Findings + Clinical Implications (original work)
2. **Academic structure** — Introduction / Methods / Results / Discussion (follows original paper structure)

| Publisher category | Vault analytical | Academic structure | Total |
|--------------------|------------------|--------------------|-------|
| Known OA journals | — | 12 | (low risk — OA licence) |
| Major non-OA publishers | 73 | 31 | ~104 |
| Unknown/grey/no-DOI | — | — | ~143 |

### The 17 papers at highest copyright risk

These are non-OA papers from major publishers that:
- Have >200 lines of body text
- Use the original paper's section structure (not vault analytical format)
- May contain verbatim or near-verbatim text

| Lines | Publisher | Journal | File |
|-------|-----------|---------|------|
| 740 | Wiley | Annals of the NYAS | Mash2000 |
| 552 | ACS | ACS Chem Neurosci | Hwu2025 |
| 474 | RSC | Nat Prod Reports | Iyer2019 |
| 454 | Elsevier | Eur J Pharmacology | Arias2023 |
| 452 | Springer Nature | Nature Medicine | Cherian2024 |
| 395 | Springer Nature | Nature Chemistry | Iyer2025 |
| 384 | Wiley | Br J Pharmacology | Mundey2000 |
| 378 | Wiley | Addiction | Knuijver2021 |
| 335 | Elsevier | Int J Biochem CB | Arias2010 |
| 318 | SAGE | J Psychopharmacology | Knuijver2024 |
| 304 | ACS | ACS Pharmacol Transl | Bhat2020 |
| 294 | T&F | Am J Drug Alcohol | Davis2023 |
| 266 | Wiley | Addiction Biology | Carnicella2010 |
| 266 | Oxford | J Anal Toxicology | Hearn1995 |
| 258 | Elsevier | Eur J Pharmacology | Paskulin2010 |
| 208 | T&F | J Psychoactive Drugs | Wilson2020 |
| 206 | Wiley | CNS Drug Reviews | Glick1999 |

**Total lines at risk: ~6,300 across 17 papers**

### Important caveats

1. **Cherian2024 (Nature Medicine)** — may actually be OA under NIH open access policy (Stanford/DoD funded). Check the DOI.
2. **Structure ≠ verbatim.** Having Introduction/Methods/Results sections doesn't mean the TEXT is copied. It could be analytical summary following the same outline. This requires spot-checking against source PDFs.
3. **COPYRIGHT.md's framing is strong.** The language about "transformative scholarly works — structured critical analyses, not reproductions" is well-crafted IF it matches reality.

### Recommendation

Before shipping, spot-check 3-5 of the longest against their PDFs:
- Mash2000 (740 lines, Wiley)
- Hwu2025 (552 lines, ACS)
- Iyer2019 (474 lines, RSC)
- Cherian2024 (452 lines, Nature Medicine — may be OA)
- Mundey2000 (384 lines, Wiley)

If the text is >50% verbatim, these need reconversion to vault analytical format (Key Findings + Clinical Implications). If the text is genuinely rewritten analytical summary that happens to follow the same outline, they're defensible.

---

## APPENDIX D: Summary — What Actually Blocks Release

### Must fix (30 min–1 hr)
1. Rewrite `_meta/README.md` for Tier 1
2. Fix wikilink count: 4,400 → ~3,400 (in README, CONTRIBUTING, CHANGELOG)
3. Strip `transcript_meeting` block from schema_registry.yml
4. Fix 5 broken wikilinks
5. Fix HOME.md heading anchor

### Should fix (15 min)
6. Strip "pangea" from validate_vault.py VALID_SCOPES
7. Fix CHANGELOG stats table

### Must assess before release
8. Copyright spot-check: 3-5 highest-risk papers against source PDFs
