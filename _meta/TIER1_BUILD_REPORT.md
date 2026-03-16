# IbogaineVault-Tier1: Build Report & Session Brief

**Generated:** 2026-03-06
**Purpose:** Comprehensive audit findings + action plan for building the publicly available IbogaineVault-Tier1 research support tool. This document is designed to be used as a session prompt for a new Claude Opus 4.6 conversation in the IbogaineVault project.
**Author:** Philip Kagalovsky (with Claude Opus 4.6 audit)

---

## How to Use This Document

Paste this entire document into a new chat in the IbogaineVault Claude Project. Then say: "I want to work through this report systematically, starting with Category 1 fixes. Let's begin."

---

## Architecture Overview

There are **two vaults**. Never confuse them.

| Vault | Path | Purpose |
|-------|------|---------|
| **Working vault** (internal) | `/Users/aretesofia/IbogaineVault/` | Primary clinical instrument. Contains ALL content — Tier 1 public research + Tier 2 internal Pangea operations, Copilot, Cowork plugin, operational logs, prompts, tools. This is where all editing happens. |
| **Tier1 vault** (public) | `/Users/aretesofia/IbogaineVault-Tier1/` | GitHub repo (`GforVendetta/IbogaineVault`). Contains ONLY distributable research content. Populated by `sync_tier1.sh` from the working vault. This is what the world sees. |

**The air gap:** The sync script at `/Users/aretesofia/IbogaineVault/_meta/tools/sync_tier1.sh` uses rsync with exclusions to mirror the working vault into Tier1. Excluded: `Pangea_Ops/`, `Collaborator_Research/`, `Cowork_Outputs/`, `.obsidian/`, `_builds/`, `_archive/`, `copilot/`, `_meta/archive/`, `_meta/prompts/`, `_meta/tools/`, `WORKLOG.md`, `ROADMAP.md`, `CLAUDE.md`, all PDFs, all binaries.

**The product vision:** Tier1 should be accessible as a web-based research tool (via Quartz static site at GitHub Pages), a cloneable GitHub repo, and eventually queryable by researchers who don't use Obsidian. It currently contains ~256 year-folder papers, 4 clinical guidelines, 14 primary sources, 8 other documents, 4 industry documents, 8 hubs, 3 MOCs, and 7 Bases (.base files). All papers have structured YAML frontmatter with 62 canonical tags, 6 colour-coded categories, boolean safety flags, and clinical metadata.

**Source PDFs** live at `/Users/aretesofia/IbogaineVault/.local/pdfs/` in a mirror structure (year folders + Clinical_Guidelines, Industry_Documents, Other, Primary_Sources). They are NOT in the Tier1 repo and should NOT be added to git. Decision: keep PDFs in Google Drive (shared folder), document `source_pdf` field as a provenance reference in README.

**Source of truth hierarchy:**
1. `schema_registry.yml` — authoritative for all enums, field definitions, type constraints
2. `conversion_manifest.md` — derivative; displays schema data with examples and decision tables
3. `Tag_Taxonomy.md` — derivative; displays canonical tags
4. Paper YAML — authoritative for all numerical claims about individual papers
5. Hub documents — synthesise and cite papers; never introduce values absent from paper YAML

---

## Audit Findings

### Category 1: Will Embarrass You If the Repo Goes Public

These must be fixed BEFORE the repo visibility changes from private to public.

**1.1 — Pangea internal document in Tier1**
- File: `Clinical_Guidelines/Pangea/Pangea_Emergency_Equipment.md`
- Issues: `status: incomplete`, `source: "Internal Pangea Biomedics documentation"`, `related_papers` with commented-out reference to `Pangea_Ops/Pangea_4Phase_Treatment`
- Cause: `sync_tier1.sh` excludes `Pangea_Ops/` but NOT `Clinical_Guidelines/Pangea/`
- Fix: Either (a) exclude `Clinical_Guidelines/Pangea/` from sync, or (b) strip internal markers and complete the document for public consumption, or (c) add explicit Tier1 exclusion for incomplete/internal documents
- Risk: HIGH — publishing an incomplete internal document undermines credibility

**1.2 — Broken wikilinks to excluded content (10+ files)**
- Files affected: `HOME.md`, `GETTING_STARTED.md`, `CONTRIBUTING.md`, `GREEN_Clinical_Protocols_Hub.md`, `WHITE_Historical_Hub.md`
- References to: `Pangea_Ops`, `_archive`, `WORKLOG`, `ROADMAP`, `CLAUDE.md`
- Consequence: Dead links in public vault. Worse: the *names* of excluded content are visible, revealing the existence of a hidden internal layer
- Fix: Systematic sweep — either remove Tier2 references or add "[internal]" annotations. Must be done in the WORKING vault first, then re-sync
- Note: The search found these in Tier1, meaning they survive the sync

**1.3 — Empty ORCID in CITATION.cff**
- File: `CITATION.cff` line 8: `orcid: ""`
- Consequence: CFF parsers and Zenodo DOI integration will reject this
- Fix: Register ORCID at orcid.org OR remove the field entirely

**1.4 — `_meta/phase2_prompt.md` in Tier1**
- This is an internal Claude operational prompt referencing worklog entries
- Has no business in the public repo
- Fix: Add to sync_tier1.sh exclusions

**1.5 — Filename typos baked into the repo**
- `Naranjo1969_Psychotherapeutic_Possibilities_Fantasy-Enhancing_Drugs.md` ("Possibilities")
- `Rodriguez-Cano2022_Underground_Ibogaine_Use_for_SUD_Tx_Qualitative_Analysis_Subjective_Experiences.md` ("Qualitative")
- Must be renamed BEFORE publication because renaming after leaves evidence in git history
- Requires updating all wikilinks that reference these files
- Fix: Rename in working vault, update all references, re-sync, force-push clean history

---

### Category 2: Schema Inconsistencies Codex Will Flag

These need resolution to enable automated validation.

**2.1 — `related_papers` field used but not in schema (~12 files)**
- All Primary_Sources files + Pangea Emergency Equipment use `related_papers:`
- `schema_registry.yml` doesn't list it. `validate_yaml.py` will flag as `unknown_field`
- Fix: Either add `related_papers` to the schema as optional on paper and transcript_published, OR remove from files and rely on body "See Also" wikilinks

**2.2 — `secondary_categories` inline arrays (~55 files)**
- Most files use `secondary_categories: ["RED", "GREEN"]` inline format
- Manifest says "Tags in list format (never inline array)" but that rule technically applies to `tags`, not `secondary_categories`
- Both parse identically in YAML
- Decision needed: Are inline arrays acceptable for `secondary_categories`? If yes, document it. If no, convert all 55 files to list format

**2.3 — `publication_date` type inconsistency**
- At least `Koenig2012` and `Glick1991` have `publication_date: 1991` (bare integer)
- Schema says `type: date`. YAML parses bare integers as integers, not dates
- Fix: Either convert to proper date strings or remove (the `year` field covers it — the manifest says "omit if only year is known")

**2.4 — `source` and `status` fields in Primary_Sources and Clinical_Guidelines**
- Several files have `source:` and `status:` fields not in the paper schema
- `Noller2025_Ibogaine_QA.md` has `source: "Internal transcript..."`
- `Pangea_Emergency_Equipment.md` has `status: incomplete`
- Fix: Add to schema as optional fields, or remove from files

---

### Category 3: Architectural Gaps

These affect the vault's utility as a public research tool.

**3.1 — `.base` files are Obsidian-only**
- `Bases/` directory has 7 `.base` files (All_Papers, Cardiac_Safety, Contraindications, etc.)
- These are opaque outside Obsidian — GitHub renders them as empty, Quartz can't display them, Codex can't interpret them
- Options: (a) Generate static markdown equivalents with Dataview query results, (b) Add a README in `Bases/` explaining what they are and how to use them with Obsidian, (c) Exclude from Tier1
- Recommendation: Option (b) minimum, option (a) ideal

**3.2 — No validation script in Tier1**
- `validate_yaml.py` (the good one, 719 lines) lives at `_meta/tools/validate_yaml.py` — excluded by sync
- `vault_qa_audit.py` IS in Tier1 but is half-built (OCR detection patterns defined but never wired up, body structure checks not implemented)
- Both hardcode `/Users/aretesofia/IbogaineVault` as vault root
- Fix: Create a unified `_meta/validate_vault.py` that auto-detects vault root, merges both validators, and is included in Tier1 sync

**3.3 — No wikilink integrity check exists (~3,900 wikilinks)**
- Nobody has ever systematically verified that wikilinks resolve to actual files
- Some use `[[Hubs/filename]]` with paths, others use `[[filename]]` without (relying on Obsidian fuzzy resolution)
- Outside Obsidian, only path-based links resolve correctly
- Fix: Add wikilink resolution checking to the validation suite

**3.4 — `source_pdf` is a phantom reference**
- Every paper says `source_pdf: "2024/filename.pdf"` but no PDF exists in the repo
- No documentation explains what this field means to someone cloning the repo
- Fix: Add explanation to README.md: "The `source_pdf` field indicates the file's location within the source PDF collection, available at [Google Drive link]"

**3.5 — No hub coverage regression detection**
- All 6 hubs are at 100% coverage (manually verified)
- But no automated test checks whether a new paper is referenced by its category hub
- Fix: Add to validation suite — for each paper, check that at least one hub in its category references its filename

**3.6 — No machine-readable index**
- No single file lists all papers with metadata in a consumable format
- Anyone wanting to build on the vault (import to Zotero, systematic review, meta-analysis, AI processing) must parse 250+ individual markdown files
- Fix: Generate `papers.json` and/or `papers.csv` in repo root. Can be auto-generated by a script

**3.7 — No CI/CD pipeline for pull requests**
- External collaborators will submit PRs with markdown files
- No GitHub Actions workflow validates schema compliance on PRs
- Fix: Create `.github/workflows/validate.yml` that runs the validation suite on every PR

**3.8 — No query mechanism outside Obsidian**
- Someone cloning the repo gets markdown files they can `grep` and nothing more
- Fix: A generated index (3.6) plus a simple Python query script would make the vault 10x more useful

---

### Category 4: Strategic Opportunities

**4.1 — DOI backlink verification** — dead DOIs undermine credibility; automate checking
**4.2 — Copyright statement** — need clear README statement about academic research fair use
**4.3 — Quartz web publishing** — already in progress (v4.5.2, first build successful); this IS the web access layer
**4.4 — Codex automated QA** — scheduled validation runs on the GitHub repo

---

## Recommended Action Sequence

### Phase 1: Hygiene (do first, before anything else)

1. Fix Pangea document leak (1.1) — decide exclude or complete
2. Fix broken wikilinks to excluded content (1.2) — systematic sweep in working vault
3. Fix ORCID in CITATION.cff (1.3)
4. Exclude `_meta/phase2_prompt.md` from sync (1.4)
5. Fix filename typos (1.5) — rename files, update all wikilinks, force-push clean history
6. Decide on `related_papers` field (2.1)
7. Decide on `secondary_categories` format (2.2)
8. Fix `publication_date` integers (2.3)
9. Decide on `source`/`status` fields (2.4)
10. Re-run sync_tier1.sh after all working vault fixes
11. Force-push clean git history

### Phase 2: Validation Infrastructure

12. Build unified `validate_vault.py` — YAML validation, wikilink resolution, OCR artefact detection, hub coverage, cross-reference minimums, duplicate DOI detection
13. Add `Bases/README.md` explaining .base files
14. Document `source_pdf` field in README.md
15. Generate `papers.json` / `papers.csv` index
16. Add validation script to Tier1 sync inclusions

### Phase 3: Codex & CI/CD

17. Create `AGENTS.md` for Tier1 repo
18. Create `.agents/skills/` with validation skills
19. Create `setup.sh` for Codex cloud environment
20. Create `.github/workflows/validate.yml` for PR validation
21. Set up Codex Automation for scheduled integrity reports

### Phase 4: Web Access

22. Complete Quartz light config
23. Quartz metadata cleanup
24. Quartz custom components (filtered pages, graph colouring, master table)
25. Deploy to GitHub Pages

---

## Key Files Reference

| File | Location | Purpose |
|------|----------|---------|
| Schema Registry | `/Users/aretesofia/IbogaineVault/_meta/schema_registry.yml` | Single source of truth |
| Conversion Manifest | both vaults `_meta/conversion_manifest.md` | YAML schema with examples (484 lines) |
| validate_yaml.py | `/Users/aretesofia/IbogaineVault/_meta/tools/validate_yaml.py` | Best validator (719 lines) — NOT in Tier1 |
| vault_qa_audit.py | both vaults `_meta/vault_qa_audit.py` | Half-built validator (307 lines) |
| sync_tier1.sh | `/Users/aretesofia/IbogaineVault/_meta/tools/sync_tier1.sh` | Air gap script (170 lines) |
| ROADMAP | `/Users/aretesofia/IbogaineVault/_meta/ROADMAP.md` | Current priorities (NOT in Tier1) |
| WORKLOG | `/Users/aretesofia/IbogaineVault/_meta/WORKLOG.md` | Session log (NOT in Tier1) |
| Source PDFs | `/Users/aretesofia/IbogaineVault/.local/pdfs/` | Mirror structure of year folders |
| Quartz | `/Users/aretesofia/IbogaineVault-Quartz/` | Static site generator (Mac Studio) |

---

## Vault Statistics (as of 2026-03-06)

- ~301 total documents (256 year-folder papers + guidelines + primary sources + other + hubs/MOCs)
- ~3,900 wikilinks
- 62 canonical tags (39 topic, 10 mechanism, 11 method, 2 meta)
- 6 co-equal categories: RED (cardiac safety), GREEN (protocols), ORANGE (mechanisms), BLUE (outcomes), PURPLE (phenomenology), WHITE (history/policy)
- All 6 category hubs at 100% coverage
- 3 boolean safety flags required on ALL papers: `qtc_data`, `electrolyte_data`, `herg_data`
- Gap analysis: 72/73 papers converted (4 remaining)

---

## Critical Principles

1. **Field omission is semantic.** `mortality_count: 0` ≠ omission. Presence signals data; absence signals no data.
2. **All six categories are co-equal.** Never deprioritise PURPLE or WHITE.
3. **Paper YAML is authoritative.** Hubs synthesise and cite — never introduce values absent from paper YAML.
4. **Schema registry wins.** If a downstream doc disagrees with `schema_registry.yml`, the registry is correct.
5. **Accuracy is critical for patient safety.** Miscategorised cardiac safety evidence could contribute to preventable deaths.

---

## Notes for Next Session

- Start with Category 1 fixes — these are blocking publication
- For each fix, work in the WORKING vault (`/Users/aretesofia/IbogaineVault/`), then re-sync to Tier1
- After Category 1, decide the open questions in Category 2 (they're design decisions, not bugs)
- The validation script (Phase 2) should be built to run on BOTH vaults with auto-detection
- Codex integration (Phase 3) depends on Phase 2 being complete
- Quartz deployment (Phase 4) can proceed in parallel with Phases 2-3
