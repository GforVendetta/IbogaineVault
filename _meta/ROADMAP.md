---
title: "IboVault Growth Roadmap"
date: 2026-02-19
category: WHITE
tags:
  - meta/moc
document_type: administrative
---

# IboVault Growth Roadmap

**Purpose:** Prioritised development plan for the Ibogaine Research Vault
**Published:** https://publish.obsidian.md/pangea-ibo-vault-v1

> Session detail → [[_meta/WORKLOG]]. Paper conversion workflow → `_meta/conversion_manifest.md`. Architectural principles → [[_meta/VAULT_PRINCIPLES|Vault Principles]]. Distribution strategy → [[_meta/STRATEGIC_PLANNING|Strategic Planning]].

### Vault Principle: Co-Equal Categories

The vault serves multiple tiers simultaneously: clinical decision-support, academic research synthesis, phenomenological archive, and historical record. **All six categories are co-equal knowledge domains, not ranked.** RED cardiac safety is not "more important" than PURPLE phenomenology or WHITE history — they serve different functions within the same research instrument. Deprioritising any category impoverishes the vault. The precision demanded for cardiac safety evidence applies equally to experiential data, mechanistic pharmacology, and historical context.

---

## Current State (2026-03-16)

**300 documents** (257 year-folder papers + clinical guidelines, industry docs, primary sources, hubs/MOCs) | **~4,900 wikilinks** (working) / **~3,400** (Tier 1) | **62 canonical tags** | **6 category hubs at 100% coverage** | Copilot Plus operational (Claude Opus 4.6) | Cowork plugin v2.3.0 (9 skills, 11 commands) | Schema registry as single source of truth | Gap analysis 72/73 (99%) | **Phase 0C copyright reconversion COMPLETE (16/16 papers)** | **Tier 1 pre-ship audit found structural blockers — 6-prompt remediation plan in progress** | **Validation: 300 papers (working) / 297 (Tier 1), 0 errors, 100% compliance** | CI/CD: GitHub Actions, AGENTS.md, validate_vault.py + generate_index.py in Tier 1

### Completed Programmes

| Programme | Scope | Status |
|-----------|-------|--------|
| Comprehensive Audit (Tiers 1A–1C) | 305 issues across 161 papers | ✅ Complete |
| ORANGE Tier 2+ Data Restoration | 24 papers, ~870 restorations | ✅ Complete |
| Damage Pilot Audit | 8 papers, 5 damage classes identified | ✅ Complete |
| Class 1 Operator Corruption | ± → 6, μ → m, = → 5 | ✅ Complete |
| Class 2 Table Cell Dropout | AI dropped numeric cell contents | ✅ Complete |
| Class 3+4 Table Omission + OCR | 12 papers, S33–S42 | ✅ Complete |
| Class 5 Parenthetical Stripping | Phase 2 grep-based fixes | ✅ Complete |
| Transcript Schema Retrofit | 5 internal calls + 12 Primary Sources | ✅ Complete |
| Tier 1D: `research-article` disambiguation | All papers disambiguated; enum prohibited for new conversions | ✅ Complete |
| Cowork ingestion commands | `/convert-paper` + `/convert-transcript`; plugin v1.4.0 | ✅ Complete |
| Gap analysis Batch 1 | 9 Tier 1 papers; audited | ✅ Complete |
| Gap analysis Batch 2 | 12 Tier 2/3 papers; cardiac cases + clinical | ✅ Complete |
| Gap analysis Batch 3 | 18 Tier 1/2 papers; pharmacology + safety lineage | ✅ Complete |
| DOI verification audit | 8 corrections (6 fixed, 2 added) | ✅ Complete |
| Hub_PK-PD_Synthesis.md | 54-paper cross-cutting synthesis; 7 sections; 291 lines; QA verified | ✅ Complete |
| Hub_PK-PD_Synthesis Tier 1+2 revision | 12 papers integrated (4 Tier 1 + 8 Tier 2); 3 misattributions fixed; §5.7 necrosis pathway + §8 cross-paper synthesis (5 entries) added; 338 lines, 38 wikilinks, all verified | ✅ Complete |
| RED Cardiac Safety Hub rebuild | 32%→100% coverage (44/44 primary + cross-refs); 7-act timeline; 71 wikilinks | ✅ Complete |
| GREEN Clinical Protocols Hub audit | Lotsof2003 added; Tier 1 enforcement (4 internal items removed); 100% Tier 1 coverage | ✅ Complete |
| BLUE Outcomes Hub rebuild | 59%→100% coverage (46/46 BLUE papers); 5 new sections; Prior2014 RCT integrated; Effect Size table expanded | ✅ Complete |
| PURPLE Phenomenology Hub rebuild | 71%→100% coverage (17/17 PURPLE papers + 3 cross-refs); null ASC–outcome editorial thread | ✅ Complete |
| WHITE Historical Hub completion | 69%→100% coverage (16/16 WHITE papers); Popik1995 wikilink fix; timeline expanded | ✅ Complete |
| Conversion session template overhaul | schema_registry.yml integration; filename/PDF-rename workflow; specialist skills | ✅ Complete |
| _meta/ redundancy audit & cleanup | Prompt dirs merged; Sam_Research relocated; validate_yaml.py updated (73→0 false positives) | ✅ Complete |
| Schema registry + downstream alignment | `schema_registry.yml` created; 4 derivative docs updated with derivation notices | ✅ Complete |
| Key Researchers Hub | 15 researchers added (2 sessions); navigation table 20 domain rows; 222→464 lines | ✅ Complete |
| Kenneth Alper MOC gap fill | 4 papers added; 3 brief attribution errors corrected; reading path 8→14 entries; broken wikilink fixed | ✅ Complete |
| Howard Lotsof MOC gap fill | 3 co-authored papers added; 4 Related Papers added; 2 attribution errors corrected; reading path 5→8; research arc 10→12 entries | ✅ Complete |
| Clare Wilkins MOC verification | Verified complete (0 gaps); Kohek2020 attribution error corrected; Brown2018 annotation verified | ✅ Complete |
| ORANGE Mechanisms Hub rebuild | 48%→103.6% coverage (116/112 primary + 14 secondary cross-refs); 9-batch programme; 6 Research Arcs; 130 verified wikilinks | ✅ Complete |
| Navigation refinement (Key Researchers + MOCs) | Key Researchers Hub (15 researchers, 20 domain rows) + Alper + Lotsof + Wilkins MOCs; Tier 3 programme complete | ✅ Complete |
| Hub_PK-PD_Synthesis Tier 3 final revision (Parts A+B+C) | 4 paper integrations + §8.6 analogue hERG hierarchy + 10 novel cross-paper synthesis entries; 394 lines, 141 wikilinks, 16 §8 entries; 4 PUBLISHABLE, 4 CLINICAL FLAG, 2 INTERNAL TENSION, 3 RESEARCH GAP | ✅ Complete |
| Cowork Plugin v2.x rebuild (3-stage) + audit remediation | Rename + restructure (v2.0.0); knowledge layer (v2.1.0); commands audit + new commands + docs split (v2.2.0); validation gates, tier filtering, collision handling, manifest files (v2.3.0) | ✅ Complete |
| Paper conversions batch 8 | Rodger2011, Lavaud2017, Luciano2000, Pablo1998 | ✅ Complete |
| Cowork audit: Tier 2 filtering on output commands | Default-to-Tier-1 on all output commands; `vault-audit` exempt. Plugin v2.3.0 | ✅ Complete |
| Cowork audit: Output collision handling | HHMM timestamp added to all 9 output commands. Plugin v2.3.0 | ✅ Complete |
| Systemic Coherence Audit (C1–C7) | 7 cross-file issues: stale pointers, schema drift, old plugin archival, navigation overlap, prompt accumulation, loose scripts, Copilot conversations. All resolved 2026-02-26. Detail in WORKLOG | ✅ Complete |
| Architectural Coherence Audit (E1–E6) | 6 structural issues: hub back-links (131 papers), prompt sweep, misplaced file, CONTRIBUTING.md, tier boundary audit, CHANGELOG. All resolved 2026-02-26. Detail in WORKLOG | ✅ Complete |
| Phase 2 Conversion Quality Audit (4 categories) | Cat 1: repeated content (15 files inspected); Cat 2: table formatting (45 files sampled); Cat 3: unclosed bold (16 files); Cat 4: sparse wikilinks (11 files, +355 wikilinks from 0 baseline). Glick1996 bracket mismatch confirmed false positive (reference notation, not broken wikilinks). Detail in WORKLOG | ✅ Complete |

**The vault's quantitative integrity is now systematically verified across all five identified damage classes.**

---

## Active Priorities

| #   | Task                                               | Status       | Blocked By                      |
| --- | -------------------------------------------------- | ------------ | ------------------------------- |
| 0   | **Tier 1 pre-ship remediation (6-prompt sequence)** | 🔄 Active   | Execute prompts 1→6 from `_meta/_tier1_overrides/VAULT_REMEDIATION_PROMPTS.md`. Adds open_access/publisher/body_format schema fields, populates metadata, fixes sync script architecture, reconverts remaining copyright-risk papers, final validation. |
| 1   | Complete Pangea 4-Phase Protocol (III/IV)          | ⏸️ Blocked   | Clare/Sarita input              |
| 2   | Finalise Pangea Emergency Equipment                | ⏸️ Blocked   | Clare/Sarita input              |
| 3   | NLQ Phase 2: Clinical test suite + custom commands | ⏳ Planned    | Clare/Sarita for test questions |
| 4   | **Gap analysis: missing papers acquisition**       | 🔄 Active    | 72/73 converted; 4 remain (Dzoljic1988, O'Hearn1997, Fernandez1982, Authier2016) |
| 5   | **Cowork audit: Dry-run test conversion**           | ⏳ Planned   | Run gated `/convert-paper` against a known-good manual conversion. Validates gate architecture in practice. Do AFTER installing updated plugin. |
| 6   | **GitHub repository & version control**            | 🔄 Active    | See sub-steps below              |
| 7   | **Schema: `evidence_level` enum gap for primary sources** | ✅ Complete | `primary-source` added to evidence_levels enum (D15, Phase 1C). Schema registry, validator, and manifest all updated. |
| 8   | **Publication plans: Two-Hit Cardiotoxicity Model + CYP2D6 Dosing Nomogram** | ⏳ Planned | Comprehensive plans at `Collaborator_Research/Philip_Kagalovsky/`. Two publishable frameworks derived from PK-PD Synthesis Hub Section 8 cross-paper synthesis. Requires co-author identification and data extraction from source PDFs. |
| 11  | **Academic identifier enrichment (pmid, pmcid)** | ✅ Complete | D16: pmid + pmcid added to schema_registry.yml. resolve_pmids.py built (NCBI ID Converter + ESearch fallback). 157 PMIDs + 50 PMCIDs populated across 191 DOI-bearing papers. Duplicate-key bug from script idempotency failure fixed (dedup_pmid_fields.py, 144 files). papers.json/csv include both fields (25 total). isbn/issn deferred — low ROI for Tier 1 release. |
| 10  | **D-decision propagation infrastructure**  | ✅ Complete   | Propagation checklist template created (`_meta/prompts/schema_decision_propagation_checklist.md`). Schema Decision Log added to manifest. Session templates verified (delegate correctly, no enum duplication). Cowork plugin audit deferred — will inherit correct enums when rebuilt. See WORKLOG 2026-03-11 |
| 9   | **Quartz web publishing layer**                    | 🔄 Active    | See sub-steps below              |

> **Completed programme detail** (C1–C7, E1–E6, Cowork v2.x stages, Hub/MOC coverage batches) preserved in WORKLOG archives for forensic reference.

### #6 — GitHub Repository & Version Control

**Why:** The vault is a clinical instrument with no off-machine backup. One disk failure loses ~8 weeks of structured knowledge architecture that cannot be reconstructed from source PDFs alone. GitHub provides: disaster recovery, collaboration infrastructure (Geoff Noller, Martijn Arns), academic citability (Zenodo DOI), and the Tier 1 public distribution mechanism.

**Architecture decision: two-directory model (revised 2026-02-26).**
> Broader distribution strategy, academic positioning, and collaboration planning → [[_meta/STRATEGIC_PLANNING|Strategic Planning]]
- The working vault at `/Users/aretesofia/IbogaineVault/` is the primary clinical instrument. It contains all Tier 1 and Tier 2 content, Obsidian configuration, Copilot, operational logs, and internal tooling. It may use git locally for version control but does **not** push to GitHub.
- A separate directory at `/Users/aretesofia/IbogaineVault-Tier1/` is the GitHub repo (`GforVendetta/IbogaineVault`). It contains only Tier 1 distributable research content, populated by an export script that mirrors the working vault minus all exclusions.
- This replaces the earlier single-repo approach where `.gitignore` acted as the tier boundary. The two-directory model provides a physical air gap — no accidental push of internal content is possible because the internal content never exists in the repo directory.
- The export script (`sync_tier1.sh`) lives in the working vault at `_meta/tools/` and handles all exclusions. Workflow: edit in working vault → run script → review diff → commit → push.

**Sub-steps:**

| Step | Action | Status |
|------|--------|--------|
| 6a | Initialise git locally (`git init` + first commit) | ✅ 2026-02-26 |
| 6b | Create private GitHub repo (`GforVendetta/IbogaineVault`) | ✅ 2026-02-26 |
| 6c | Push initial commit to remote | ✅ 2026-02-26 |
| 6d | Verify `.gitignore` exclusions (confirm no Tier 2 content in repo) | ✅ 2026-02-26 |
| 6e | Tier 1 repo hygiene: untrack binaries, add README/LICENSE/CITATION | ✅ 2026-02-26 |
| 6f | Tier 1 cleanup: untrack internal tooling (`_archive/`, `copilot/`, `CLAUDE.md`) | ✅ 2026-02-26 |
| 6g | Document git workflow in VAULT_ARCHITECTURE.md | ✅ 2026-02-26 |
| 6g2 | **Migrate to two-directory model** | ✅ 2026-02-26 — Tier 1 at `/Users/aretesofia/IbogaineVault-Tier1/`; export script at `_meta/tools/sync_tier1.sh`; force-pushed clean history; `.git/` removed from working vault |
| 6h | Pre-publication checklist (see below) | ⏳ |
| 6i | Invite collaborators (Geoff Noller — read access) | ⏳ Needs Geoff's GitHub username |
| 6j | Zenodo DOI integration | ⏳ Deferred until first publication |
| 6k | Flip to public / Tier 1 distribution | ⏳ Deferred |

### #6h — Pre-Publication Checklist (before flipping to public)

All items must be completed before the repo visibility changes from private to public. Comprehensive audit conducted 2026-03-11 — see `IbogaineVault_Tier1_Audit_Report.pdf` for full findings. Execution sequence PDF available as printable checklist.

| Item | Action | Status |
|------|--------|--------|
| **COPYRIGHT / DOI AUDIT** | DOI audit complete (304 papers). Definitive OA classification: 97 GREEN, 87 RED, 6 AMBER, 114 GREY, 0 BROKEN. All 10 broken DOIs corrected. 29 publisher-mirror RED papers reconverted to vault analytical format (5 batches). `COPYRIGHT.md` written + condensed statement in README.md. 8 stale files purged from Tier1/_meta/. **Phase 0C n-gram reconversion:** 16 papers flagged by 4-gram overlap analysis (0.373–0.955) reconverted across 5 batches. Final triage: 15 🟢, 2 🟡 (data-table vocabulary, not reproduced prose). Commit 34abb62. | ✅ 2026-03-16 |
| **VALIDATION GATE (post-0C)** | Phase 2A COMPLETE. `validate_vault.py`: 300 papers (working) / 297 (Tier 1), 0 errors, 100.0% compliance. 5 D-decisions propagated (source_url field, journalism/industry-report in synthesis policy, GITA2015 encyclopedic exception, transcript_published scope handling, shared-DOI allowlist). | ✅ 2026-03-14 |
| ORCID | Registered: https://orcid.org/0009-0008-3558-3097. Already in CITATION.cff | ✅ 2026-03-11 |
| Tier1 documentation rewrites | Rewrite 7 files for public audience: HOME.md, GETTING_STARTED.md, CONTRIBUTING.md, VAULT_PRINCIPLES.md, VAULT_ARCHITECTURE.md, _meta/README.md, README.md. Strip all Copilot/Cowork/Pangea_Ops/CLAUDE.md references, absolute paths, internal tooling refs. Detail in audit report §8 | ✅ 2026-03-12 |
| `_meta/` whitelist | Switch from exclude-list to whitelist approach: only schema_registry.yml, Tag_Taxonomy.md, VAULT_PRINCIPLES.md (rewritten), VAULT_ARCHITECTURE.md (rewritten), README.md (rewritten) pass through to Tier1. Self-sealing: new _meta/ files excluded by default. | ✅ 2026-03-12 |
| Sync script evolution | Allowlist architecture for _meta/. --delete-excluded + .git protect filter. Post-sync sed strips [[Pangea_Ops/...]] wikilinks. 4 redundant per-file excludes removed (files relocated to Pangea_Ops/). | ✅ 2026-03-12 |
| .gitignore in Tier1 | Created in Tier1 repo. Covers .DS_Store, editor files, *.pdf, .obsidian/, .copilot-index/, .smart-env/ | ✅ 2026-03-11 |
| Filename typos | Renamed Naranjo1969 (Possibilities, 23 wikilinks) and Rodriguez-Cano2022 (Qualitative, 14 wikilinks) | ✅ 2026-03-11 |
| Accessibility statement | Add to README: who vault is for, what it is not (not medical advice), limitations of evidence synthesis | ✅ 2026-03-12 |
| Schema decisions | D11: related_papers removed (14 files); D12: secondary_categories normalised to inline (117 files); D13: publication_date cleaned (75 removed, 79 quoted); D14: source/status removed (34 files); D15: primary-source enum added + 11 files updated. **Propagation audit 2026-03-11:** D12, D13, D15 were not propagated to conversion_manifest.md and/or validate_yaml.py — all fixed. Checklist items added to manifest. | ✅ 2026-03-11 |
| `scope: pangea` sweep | 3 Oliver documentary interviews + Noller Q&A relocated from Primary_Sources/ to Pangea_Ops/ (consent-based triage). Deleted from Tier 1. 19 wikilinks updated. scope:pangea YAML sweep passes clean. Conference talks + published media remain (scope: published). | ✅ 2026-03-12 |
| Sync clean pass | `sync_tier1.sh` PASSED: all governance files present, zero excluded content, zero scope:pangea, Pangea_Ops wikilinks stripped from 16 files. Stale `Clinical_Guidelines/Pangea/` manually removed (rsync edge case). | ✅ 2026-03-12 |
| Git history scrub | Force-pushed orphan commit to GforVendetta/IbogaineVault — all prior history replaced with single verified-clean state. Repo URL preserved. | ✅ 2026-03-12 |
| Google Drive PDF folder | Create shared folder, upload source PDFs, update placeholder link in `CONTRIBUTING.md` | ⏳ |
| Final README review | Paper count ("over 300"), wikilink count ("4,500+" verified at 4,742), governance links verified, duplicate line fixed, stale tree entry removed, Dataview→Properties correction, CITATION.cff updated (title/abstract/count), GETTING_STARTED.md clarified | ✅ 2026-03-14 |
| CI/CD infrastructure | AGENTS.md (88 lines, Codex agent instructions), `.github/workflows/validate.yml` (push + PR + weekly cron), `setup.sh`. validate_vault.py + generate_index.py copied to Tier 1 root via sync_tier1.sh (Tier 2 directory names stripped from validator). Commit 575b692. | ✅ 2026-03-14 |
| Governance sweep + hub coverage | "Structured evidence map" terminology across 6 governance files. 2 non-ibogaine files excluded (Strategic_Implementation, deLugo). 3 hub gaps fixed (Evans2026→RED, DeRienzo book→WHITE, Hoeck2003→ORANGE). CHANGELOG rewritten for public audience. README/CONTRIBUTING counts corrected. sync_tier1.sh patched for macOS rsync file-deletion bug. 297 papers, 0 errors, 100% compliance. Commit 63e792f. | ✅ 2026-03-14 |
| Post-audit remediation | 6 hub/governance broken refs fixed, 32+ stem mismatches across 8 papers, .yml wikilink→markdown link conversions, DeRienzo chapters (17 files) integrated into WHITE Hub + Lotsof MOC. README wikilink count corrected (3,300+). 300 papers, 0 errors, 100% compliance, 0 broken wikilinks. Commit 6b023dd. | ✅ 2026-03-14 |
| **Content fidelity audit (Session 2)** | 15-paper stratified sample + boolean sweep (297 papers). 8 fixes: 5 metadata corrections (Schenberg, Brown, Thurner, Evans, Chen) + 3 boolean corrections from sweep (Glue2016, Clare Wilkins, Malcolm2022). boolean_sweep.py field-name bugs fixed. 11 non-RED mortality papers verified (all carry RED secondary). Commit d0bb646. | ✅ 2026-03-14 |
| **Pre-release Session 1: Pangea contamination** | 206 "Pangea" ghost-text matches across Tier 1 from incomplete wikilink stripping. 89 paper Clinical Implications cleaned + 8 hubs rewritten (de-linked Pangea_Ops wikilinks, removed NDA-sensitive refs). NDA-term sweep clean. Quality gate passed. | ✅ 2026-03-15 |
| **Pre-release Session 2: PMID/PMCID enrichment** | resolve_pmids.py (NCBI ID Converter + ESearch fallback): 157 PMIDs + 50 PMCIDs populated across 191 DOI-bearing papers. Duplicate-key idempotency bug found and fixed (dedup_pmid_fields.py, 144 files). papers.json/csv include both fields (25 total). Commit 169badc. | ✅ 2026-03-15 |
| **Pre-release Session 3: Formatting cleanup** | 17,728 ligatures normalised across 556 files, 29 LaTeX artefacts removed across 11 files, 66 dosing_range values standardised to en-dash across 65 files. OA format decision: documentation only (v1.1 for full analytical conversion). | ✅ 2026-03-15 |
| **Pre-release Session 4: Governance review** | OA format paragraph added to CONTRIBUTING.md. Citation counts harmonised ("approximately 300"). Category counts updated in HOME.md. Cross-reference counts corrected (~4,400). Clinical decision-support framing sweep clean. Arns first-impression review: all 9 governance files pass. HOME.md re-featured Tier-2-only link to Tier-1-available Primary Source. Commits 29fc33d + 867eed3. | ✅ 2026-03-15 |
| Zenodo integration | Connect repo to Zenodo for automatic DOI assignment on release | ⏳ |

### #9 — Quartz Web Publishing Layer

**Why:** Transforms the Tier 1 vault from a static Obsidian Publish site into a navigable research website with category-coloured graph, filtered clinical pages, and interactive tables. Quartz v4.5.2 (Option B — local clone) enables custom plugins and components impossible with black-box deployment. Also serves as a diagnostic instrument for metadata cleanup: broken wikilinks, malformed YAML, and missing fields become immediately visible.

**Architecture:** `sync_tier1.sh` → `IbogaineVault-Tier1/` → copy to `IbogaineVault-Quartz/content/`. Symlink abandoned (serve-handler incompatibility). Future: `sync_quartz.sh` automates the copy + index.md patch.

**Environment:** Mac Studio. Quartz at `/Users/aretesofia/IbogaineVault-Quartz/`. Node v22.22.0 via nvm.

| Step | Action | Status |
|------|--------|--------|
| 9a | Clone Quartz, install deps, initialise empty content | ✅ 2026-02-26 |
| 9b | Clone GitHub repo to Mac Studio as `IbogaineVault-Tier1/`; copy content to Quartz | ✅ 2026-02-26 |
| 9c | First build: `npx quartz build --serve` — verify 310 docs render at localhost:8888 | ✅ 2026-02-27 |
| 9d | Light config: explorer sort, `KeyFindingsToDescription` transformer, HOME→index.md, category colour CSS | ⏳ |
| 9e | Metadata cleanup with Quartz preview as diagnostic | ⏳ |
| 9f | Custom components: filtered pages (cardiac, protocols, fatalities), graph colouring, master table | ⏳ |
| 9g | GitHub Pages deployment | ⏳ |

---

## Gap Analysis — Missing Papers

**72/73 converted (99%).** 4 remaining — convert as PDFs become available. Obach1998 converted 2026-02-24; Geoly2026, Malcolm2022, Terasaki2026 converted 2026-02-23; batch 8 (Rodger2011, Lavaud2017, Luciano2000, Pablo1998) converted 2026-02-25.

**Method:** Phase 1 (Deep Research literature sweep) + Phase 2 (citation mining of 14 vault reviews), cross-referenced and deduplicated. Full methodology: `_meta/archive/reference_gap_analysis_COMPLETE.md`. Batch conversion history: `_meta/archive/`.

### Remaining Gaps (4 papers)

| Paper | Category | Why It Matters |
|-------|----------|----------------|
| Dzoljic 1988 — First preclinical anti-withdrawal | ORANGE | First published evidence ibogaine blocks withdrawal; cited 5/14 reviews; old journal, likely needs interlibrary loan |
| O'Hearn 1997 — Olivocerebellar mechanism | ORANGE | Extends O'Hearn 1993 neurotoxicity; trans-synaptic excitotoxicity |
| Fernandez 1982 — *Bwiti* monograph | WHITE | Canonical Bwiti ethnography (Princeton UP book); vault has 2001 chapter only |
| Authier 2016 — Noribogaine EEG safety | GREEN | NOAEL 320 mg/kg in primates; no seizure activity |

### Deprioritised (convert if clinically needed)

Noller 2018 verification — resolved via duplicate merge (Noller2016/2017 consolidated 2026-02-22).

### Completed Batch History

Batches 1–3 converted 39 papers across three sessions (2026-02-19 to 2026-02-21). Additional papers converted during individual sessions. Batch-by-batch detail preserved in `_meta/archive/gap_batch_history.md`.

---

## Backlog

### ~~Schema: `evidence_level` gap for non-research primary sources~~ — RESOLVED

**Resolution:** Option 1 implemented during D15 (Phase 1C). `primary-source` added to `evidence_levels` enum in schema_registry.yml, propagated to validate_yaml.py and conversion_manifest.md. Active Priority #7 marked complete.

**De Rienzo & Beal 1995 — remaining chapter conversions (Ch1–11).** Chapters 12–18 ✅ complete (in `Other/`). Three chapters have meaningful vault content; remainder are biographical/counterculture history with minimal clinical value. Convert in priority order:

| Chapter | Title | Category | Vault Value | Why |
|---------|-------|----------|-------------|-----|
| Ch7 | Stanley Glick | ORANGE | ~~**High**~~ | ✅ Converted 2026-03-06. `Other/DeRienzo1995_Ibogaine_Story_Ch7.md` |
| Ch5 | The Staten Island Project | WHITE/BLUE | ~~Moderate~~ | ✅ Converted 2026-03-06. `Other/DeRienzo1995_Ibogaine_Story_Ch5.md` |
| Ch6 | Bob Sisko | WHITE/PURPLE | ~~Moderate~~ | ✅ Converted 2026-03-06. `Other/DeRienzo1995_Ibogaine_Story_Ch6.md` |
| Ch8 | Nico Adriaans | WHITE/PURPLE | ~~Low–Moderate~~ | ✅ Converted 2026-03-06. `Other/DeRienzo1995_Ibogaine_Story_Ch8.md` |
| Ch10 | Carlo Contoreggi | WHITE/GREEN | ~~Low–Moderate~~ | ✅ Converted 2026-03-06. `Other/DeRienzo1995_Ibogaine_Story_Ch10.md` |
| Ch11 | Geerte F. | PURPLE | ~~Low–Moderate~~ | ✅ Converted 2026-03-06. `Other/DeRienzo1995_Ibogaine_Story_Ch11.md` |
| Ch1 | The War With the Junkies | WHITE | Low | Counterculture/drug war origins; Forcade suicide |
| Ch2 | Howard Lotsof | WHITE | Low | Lotsof biography; 1962 self-experiment (already captured in Ch5/12–18) |
| Ch3 | Dhoruba Moore | WHITE | Low | Black Panther/COINTELPRO history; racial politics context |
| Ch4 | Dana Beal | WHITE | Low | Beal biography; Yippie movement; cannabis activism |
| Ch9 | Jon Parker | WHITE | Low | Needle exchange; harm reduction activism |

Source: `/Users/aretesofia/Library/Mobile Documents/com~apple~CloudDocs/IbogaineVault_PDFs/Other/The Ibogaine Story Report On The Staten Island Project by Dana Beal and Paul De Rienzo.txt` (3,136 lines)

**Remaining conversions (pre-gap-analysis):** Knuijver2022 (QTc, if PDF located), ICEERS2012 (if PDF located). Convert if requested. Sijic2025 ✅ converted. Kontrimavičiūtė 2006a ✅ converted (LC-MS plasma method).

**Research threads (optional):** MISTIC evidence arc completion, GDNF/neuroplasticity thread, Protocol Comparison Matrix.

**NLQ Phases 3–5:** Query Plan IR refinement, plugin implementation, static evidence packs. Deferred until Phase 2 validates clinical utility.

**Schema enhancement proposals (archived):** Three proposals for structured YAML fields — `pk_pd_profile`, `contradictory_evidence`, `intervention_context`. Archived to `_meta/archive/enhancement_proposals.md`. Proposal 1 partially superseded by Hub_PK-PD_Synthesis.md. Revisit when programmatic queries (Copilot Plus / Noller collaboration) justify the maintenance cost.

---

## Infrastructure

| Component | Location | Purpose |
|-----------|----------|---------|
| Distribution Tiers | [[_meta/VAULT_ARCHITECTURE]] | Tier 1 (public, excl. Pangea_Ops/) vs Tier 2 (internal) |
| Distribution Architecture | [[_meta/DISTRIBUTION_ARCHITECTURE]] | Two-directory model, sync script, exclusions |
| Strategic Planning | [[_meta/STRATEGIC_PLANNING]] | Distribution strategy, academic positioning, collaboration tactics |
| Cowork Plugin (current) | `_builds/pangea-ibovault/` | 9 skills + 11 commands (v2.3.0) |
| Cowork Plugin (legacy) | `_archive/_builds_v1/pangea-ibogavault/` | Archived v1.3.0 (2026-02-26) |
| Cowork Outputs | `Cowork_Outputs/` | Clinical work products |
| Skills Archive | `_archive/_skills_legacy/` | Former `_skills/` — superseded by Cowork plugin v2.0.0 |
| Primary Sources Archive | `_archive/primary-sources/` | Non-research primary sources (legal filings, regulatory correspondence) — in vault graph but separated from research papers |
| Copilot | `copilot/` | Obsidian Copilot Plus (Claude Opus 4.6) |
| Quartz | `/Users/aretesofia/IbogaineVault-Quartz/` (Mac Studio) | Static site generator v4.5.2; `content/` is copy of Tier 1 (symlink abandoned). Dev server: port 8888 |
| NLQ Architecture | [[_meta/NLQ_ARCHITECTURE]] | Natural language query design |
| Tag Taxonomy | [[_meta/Tag_Taxonomy]] | 62 canonical tags |
| Schema Registry | `_meta/schema_registry.yml` | Single source of truth for all schemas, enums, field defs |
| Conversion Manifest | `_meta/conversion_manifest.md` | YAML schema, tags, template (derives from registry) |
| Propagation Checklist | `_meta/prompts/schema_decision_propagation_checklist.md` | Required workflow for all future schema decisions |
| Conversion Template | `_meta/prompts/_template_conversion_session.md` | Reusable session prompt for paper conversions |
| Transcript Manifest | `_meta/transcript_manifest.md` | Transcript YAML schema, scope field (derives from registry) |

---

*Last updated: 2026-03-16 — 300 documents (257 year-folder papers + guidelines, primary sources, hubs/MOCs). Gap analysis: 72/73 converted (4 remaining). All 6 category hubs at 100% coverage. ~4,400 wikilinks. 62 canonical tags. Schema registry as single source of truth. Phase 0 COMPLETE: DOI audit (97 GREEN, 87 RED, 6 AMBER, 114 GREY), 29 RED paper reconversions, validation gate passed. Phase 0C COMPLETE: 16 papers reconverted via n-gram copyright triage (15 🟢, 2 🟡), commit 34abb62. Phase 1D COMPLETE: 7 doc rewrites, _meta/ allowlist, sync script hardened, scope:pangea sweep clean. Phase 2A COMPLETE: unified validate_vault.py, 36 errors resolved, 100.0% compliance (0 errors, 24 warnings), 5 D-decisions propagated. Phase 2B COMPLETE: generate_index.py producing papers.json + papers.csv (297 Tier 1 records), integrated into sync_tier1.sh. Phase 2C COMPLETE: Bases/README.md, source_pdf verification, Dataview→Properties correction. Phase 3 COMPLETE: AGENTS.md, validate.yml, setup.sh, validate_vault.py + generate_index.py in Tier 1 root. Phase 4 COMPLETE: governance terminology, hub coverage gaps, CHANGELOG rewritten, sync script macOS fix, CITATION.cff date-released. Content fidelity audit COMPLETE: 8 fixes, boolean sweep clean. **Pre-release fix sequence COMPLETE:** (1) Pangea contamination cleaned (89 papers + 8 hubs), (2) PMID enrichment (157 PMIDs + 50 PMCIDs), (3) formatting cleanup (17,728 ligatures, 29 LaTeX artefacts, 66 dosing_range dashes), (4) governance review (OA documentation, citation harmonisation, framing sweep, Arns first-impression test, HOME.md Tier 1 fix). Tier 1: 297 papers, 0 errors, 100% compliance. **Ready for ship-it: flip repo public → Zenodo DOI → Arns delivery.***
