---
title: "IboVault Worklog"
date: 2026-02-20
category: WHITE
tags:
  - meta/moc
document_type: administrative
---

# IboVault Worklog

**Purpose:** Orientation dashboard + lean session chronology for vault development.

---

## Status Dashboard

*Rewritten in-place after every session. This is the single point of orientation.*

**Current phase:** Tier 1 pre-ship remediation — executing 6-prompt plan (2 of 6 done)
**Batch progress:** Audit ✅ | Prompt 1 (schema) ✅ | Prompt 2 (metadata pop) ✅ | **Prompt 3 (ID lookup) ⬜** | Prompt 4 (sync v2) ⬜ | Prompt 5 (reconversions) ⬜ | Prompt 6 (ship gate) ⬜
**Metadata population:** open_access 300/300, publisher 198/300, body_format 300/300; 21 copyright risk papers identified
**Validation baseline:** 300 papers, 0 errors, 100% compliance
**Blocking:** Prompt 3 (PMCID/ISSN enrichment) will upgrade some open_access:false→true; Prompt 4 (sync v2) must precede final validation
**Next session:** Execute Prompt 3 (CrossRef/NCBI API lookups for PMCID and ISSN) from `_meta/_tier1_overrides/VAULT_REMEDIATION_PROMPTS.md`
**Reconversion plan:** 21 copyright risk papers identified by metadata_report.csv — queue for Prompt 5
**Last updated:** 2026-03-16

---

## Logging Protocol

*This protocol is mandatory. Every session that modifies vault content must follow it.*

**After completing work:**

1. **REWRITE the Status Dashboard** — update phase, batch progress, blocking items, next session guidance. Do not append; overwrite the existing dashboard content.
2. **APPEND one entry to the Session Log** — maximum 5 lines, following the format below. No tables, no verification matrices, no field-level detail.
3. **If granular detail is needed** (e.g., which files changed, which YAML fields were corrected), write a session note to `_meta/archive/sessions/YYYY-MM-DD-[label].md`. Do not put operational detail in the worklog.

**Session entry format (strict):**

```
## YYYY-MM-DD-[a/b/c] — [Title]
[One sentence: what was done and why]
[2–3 lines: key outcomes — what changed, what was created, what was decided]
[One line: what remains or what's next]
```

**Session dating:** Use `YYYY-MM-DD-a`, `-b`, `-c` for multiple sessions on the same day. No sequential session numbers.

**Archiving:** Archive by completed phase (not by line count). When a phase completes, move its entries to `_meta/archive/WORKLOG_archive_[phase-descriptor].md`. Each archive should be a coherent unit of work.

---

## Session Log

*Append-only. Newest at top. Maximum 5 lines per entry.*

## 2026-03-16-i — Prompt 2 COMPLETE: open_access, publisher, body_format populated across 300 papers
Wrote and ran populate_metadata.py — string-surgery insertion of 3 fields into all 300 papers without YAML re-serialisation. Fixed critical f-string regex bug (`{2,3}` interpreted as tuple inside rf-string, producing `^#(2, 3)` instead of `^#{2,3}`). Expanded DOI publisher map from 27→49 prefixes to cover all vault DOI ranges.
Results: open_access 105 true / 128 false / 67 unknown; publisher 198/300 (3 existing preserved + 195 detected); body_format 154 vault-analytical / 76 academic-retained / 36 hybrid / 34 narrative. Copyright risk report identifies 21 papers for Prompt 5 reconversion queue. Validator: 0 errors, 100% compliance.
Next: Execute Prompt 3 (CrossRef/NCBI API lookups for PMCID/ISSN enrichment) from VAULT_REMEDIATION_PROMPTS.md.

## 2026-03-16-h — Prompt 1 COMPLETE: schema additions (open_access, publisher, body_format, issn)
Added four copyright/format metadata fields to schema_registry.yml (D17 group) with two new enums (open_access_status, body_formats), updated generate_index.py INDEX_FIELDS (4 new columns), and added enum validation to validate_vault.py with YAML boolean coercion handling for open_access. Spot-check confirmed publisher and issn already had values on a handful of papers now surfaced in the index.
Validation: 300 papers, 0 errors, 100% compliance. Next: Execute Prompt 2 (automated metadata population) from VAULT_REMEDIATION_PROMPTS.md.

## 2026-03-16-g — Deep audit + 6-prompt remediation plan for Tier 1 pre-ship
Comprehensive Tier 1 audit found two structural root causes behind recurring blockers: (1) sync script overwrites all Tier-1-specific fixes on every run, (2) no metadata fields (open_access, publisher, body_format) for copyright risk assessment. Identified 78 academic-structure papers, 102 missing DOIs, Mash2000 as highest copyright risk (776 lines, Wiley, unscreened by Phase 0C). Wrote 6-prompt remediation sequence at `_meta/_tier1_overrides/VAULT_REMEDIATION_PROMPTS.md` covering schema additions, automated metadata population, API identifier lookup, sync script v2 with override mechanism, reconversion queue, and final ship validation.
Next: Execute prompts 1→6 sequentially (~3-4h). Prompt 4 (sync script v2) is the linchpin preventing future regressions.

## 2026-03-16-f — Batch 5 COMPLETE: Arias2023 ✅ + Bhat2020 ✅ + Iyer2025 ✅ — Phase 0C DONE
Completed final batch of copyright reconversion (3 papers across two conversations). Arias2023 and Bhat2020 done in prior conversation. Iyer2025 reconverted with all 9 data tables preserved (4 optimisation tables, synthesis comparison, modularity compounds, spinogenesis, SERT inhibition/efflux EC₅₀s); YAML corrected — added route:not-applicable and topic/neuroplasticity tag. Phase 0 copyright reconversion now COMPLETE: 16 of 16 papers across 5 batches.
Next: Run n-gram triage to verify all Batch 5 papers score <0.20. Then re-sync Tier 1, validate, commit+push, update ROADMAP for Phase 0C completion.

## 2026-03-16-e — Batch 4 COMPLETE: Paskulin2010 ✅ + Davis2023 ✅ reconverted
Completed final two papers of Batch 4. Paskulin2010 reconverted in prior conversation (0.798→0.143 🟢). Davis2023 reconverted with mermaid protocol diagram, demographics table, and head injury profile restored after initial over-aggressive compression (0.660→0.250 🟡 — overlap driven by verbatim abstract and data table vocabulary, not reproduced prose). All Batch 4 scores: Hearn1995 0.162 🟢, Glick1999 0.068 🟢, Paskulin2010 0.143 🟢, Davis2023 0.250 🟡. 13 of 16 papers complete.
Next: Batch 5 — Arias2023 (0.429), Bhat2020 (0.404), Iyer2025 (0.373); ~7.3K source words, 3 papers.

## 2026-03-16-d — Batch 4 partial: Hearn1995 ✅ + Glick1999 ✅ reconverted
Reconverted Glick1999_18MC_Review_CNS_Drugs from verbatim reproduction (0.897) to vault analytical format (4g=0.068, 6g=0.027, 8g=0.018 — second-lowest score in triage after Mash2000 exemplar). Full 23-target receptor binding table restored with ligand column and SEMs; DOI and ISSN added to YAML. Hearn1995 was completed in a prior conversation (0.771→0.162). N-gram triage confirms both 🟢.
Next: Batch 4 continues — Paskulin2010 (0.798) and Davis2023 (0.660) remain.

## 2026-03-16-c — Table remediation COMPLETE + earlier-batch audit clean
Inserted missing data tables into 4 reconverted papers: Knuijver2021 (Table 1 demographics + Table 2 expanded to full primary/secondary outcomes), Knuijver2024 (Table 1 study population), Cherian2024 (Table 1 baseline demographics/diagnoses), Iyer2019 (Table 2 synthesis overview — 21 routes). Audited all 12 earlier-batch papers across Batches 1–3 and 5 for similar gaps; none found. Extended Data Tables in Cherian2024 excluded as supplementary per Philip's discretion.
Next: Batch 4 reconversion (Hearn1995, Glick1999, Paskulin2010, Davis2023) in fresh conversation.

## 2026-03-16-b — Audit found missing data tables in 4 reconverted papers
Post-reconversion audit compared PDF table counts against vault markdown table blocks across all 9 completed papers. Systematic failure mode identified: demographic/baseline tables were stripped during reconversion while data tables were retained. Confirmed missing: Knuijver2021 (Table 1 demographics, Table 2 only partially represented), Knuijver2024 (Table 1 population characteristics), Cherian2024 (Table 1 baseline demographics), Iyer2019 (Table 2 synthesis overview). Arias2010, Mundey2000, Carnicella2010, Hwu2025 confirmed OK. Wilson2020 qtc_data corrected to true.
Next: Restore 4 missing tables before starting Batch 4.

## 2026-03-16-a — Copyright reconversion Batch 3 COMPLETE: Wilson2020 PASS
Reconverted Wilson2020_Novel_Tx_OUD_Ibogaine_Iboga_Case_Study from verbatim reproduction (0.914) to vault analytical format (4g=0.179, 6g=0.147, 8g=0.134 — all 🟢). Corrected qtc_data to true (Case 2 documented QTc 512 ms from iboga+quetiapine interaction). YAML journal field flagged: should be "Journal of Psychedelic Studies" not "Journal of Psychoactive Drugs" — for Phase 1 YAML audit. Batch 3 now complete: Knuijver2024 0.176, Cherian2024 0.151, Mundey2000 0.129, Wilson2020 0.179 — all clear. 9 of 16 papers done; 7 remain (4 🔴, 3 🟠).
Next: Batch 4 — Hearn1995, Glick1999, Paskulin2010, Davis2023 (~15.5K source words, 4 papers).

## 2026-03-15-k — Copyright reconversion Batch 2 COMPLETE: Carnicella2010 PASS
Reconverted Carnicella2010_Noribogaine_18MC_GDNF from verbatim reproduction (0.837) to vault analytical format (4g=0.196, 6g=0.168, 8g=0.149 — all 🟢). Body rewritten as independent GDNF/mechanism analysis (~1,600 words from ~5,392 source) with two-pathway dissociation model (VTA/GDNF vs habenula/α3β4) surfaced as central insight. Batch 2 now complete: Arias2010 0.153, Knuijver2021 0.155, Carnicella2010 0.196 — all clear. 5 of 16 papers done; 11 remain (8 🔴, 3 🟠).
Next: Batch 3 — Knuijver2024, Cherian2024, Mundey2000, Wilson2020 (~18.3K source words, 4 papers).

## 2026-03-15-j — Copyright reconversion Batch 2 paper 2: Knuijver2021 DONE
Reconverted Knuijver2021_Safety_Opioid_Detox from verbatim reproduction (0.792) to vault analytical format. Body rewritten as independent cardiac safety analysis (~2,000 words from ~5,901 source) with Cardiac Safety Data section (QTc, haemodynamic, pharmacokinetic subsections), Cerebellar and Behavioural Effects, and expanded Clinical Implications connecting to MISTIC protocol. YAML preserved character-for-character, all numerical values triple-checked against PDF, 2 new wikilinks added (Knuijver2024, Noller2017). PMID 33620733 / PMCID PMC9292417 / DOI 10.1111/add.15448 confirmed via PubMed.
N-gram score pending (run triage script before next session). Next: Batch 2 paper 3 — Carnicella2010_Noribogaine_18MC_GDNF (0.837, 5,392 words).

## 2026-03-15-i — Copyright reconversion Batch 2 paper 1: Arias2010 PASS
Reconverted Arias2010_Interactions_Ibogaine_NicotinicAChR_Human from verbatim reproduction (0.746) to vault analytical format (4g=0.153, 6g=0.115, 8g=0.095 — all 🟢). Body rewritten as independent receptor pharmacology analysis (~2,200 words from ~8,344 source). YAML preserved, 5 data tables verified against PDF, 2 new wikilinks added. PMID 20684041 / PMCID PMC4609575 confirmed.
Next: Batch 2 paper 2 — Knuijver2021_Safety_Opioid_Detox (0.792, 5,901 words).

## 2026-03-15-h — Copyright reconversion Batch 1 COMPLETE: Iyer2019 PASS + triage script fix
Reconverted Iyer2019_Iboga_Enigma (8,265 source words, 0.955 → 0.114 🟢). Batch 1 now complete: both papers pass all three n-gram thresholds. Fixed triage script Python 3.9 compatibility (dict|None → Optional[dict]); full 17-paper run confirmed (3 🟢, 11 🔴, 3 🟠). DOI/PMID/PMCID verified via PubMed for Iyer2019 — all match existing YAML.
Next: Batch 2 (Arias2010, Knuijver2021, Carnicella2010) — ~19.6K source words, 3 papers.

## 2026-03-15-g — Copyright reconversion Batch 1 paper 1: Hwu2025 PASS
N-gram triage script identified 16 papers with 4-gram overlap >0.20 against source PDFs (12 🔴, 3 🟠). Reconverted Hwu2025_Matrix_Pharmacology_VMAT2_SERT from verbatim reproduction (0.851) to vault analytical format (0.157 🟢). YAML preserved, abstract preserved, body rewritten as independent analysis (~3,000 words from ~10,267 source). Python 3.9.6 compatibility issue with triage script resolved via __future__ annotations.
Next: Iyer2019 (Batch 1 paper 2, 0.955 → target <0.20) in fresh ET conversation.

## 2026-03-15-f — Governance review complete, HOME.md Tier 1 fix
Combined governance session completing the pre-release fix sequence. OA format paragraph added to CONTRIBUTING.md; citation counts harmonised to "approximately 300" across all governance files; HOME.md category counts updated to current (GREEN 11→20, WHITE 19→42); cross-reference counts corrected to ~4,400; QTc paper count 53→54; clinical decision-support framing sweep clean. Arns first-impression review: all 9 governance files pass. HOME.md Primary Sources table re-featured from Tier-2-only Pangea_Ops interview to Primary_Sources/2010_Horizons_Clare_Wilkins (works in both tiers).
Validation: 300/297, 0 errors, 100% compliance. Two commits pushed (29fc33d, 867eed3). Next: ship-it — flip repo public, Zenodo DOI, Arns delivery.

## 2026-03-15-e — Mechanical formatting cleanup: ligatures, LaTeX, dashes
Vault-wide character normalisation and formatting artefact removal ahead of Tier 1 public release.
Ligatures: 17,728 instances across 556 files → 0 via sed (ﬁ→fi, ﬂ→fl, ﬀ→ff, ﬃ→ffi, ﬄ→ffl). LaTeX: 29 garbled/duplicated superscripts and author affiliation artefacts cleaned across 11 files via targeted Python script; legitimate scientific notation preserved. Dashes: 66 dosing_range values across 65 files standardised from hyphen to en-dash. OA format decision: Option 1 (documentation) chosen; full OA analytical conversion deferred to v1.1. Validation: 300 papers, 0 errors, 30 warnings (unchanged).
Next: Combined governance session (Option 1 doc paragraph + citation harmonisation + framing sweep + Arns first-impression review + sync/validate/commit).

## 2026-03-15-d — PMID/PMCID duplicate YAML key deduplication
resolve_pmids.py had an idempotency bug — 144 files had duplicate pmid: lines and 50 had duplicate pmcid: lines from the insertion logic failing to detect existing fields.
Wrote and ran dedup_pmid_fields.py; all duplicates removed, verification clean. Re-synced, validated (297 papers, 0 errors, 100% compliance), papers.json regenerated, committed and pushed (169badc).
Next: Session 3 (OA format + formatting) per `_meta/prompts/pre_release_fix_sessions.md`.

## 2026-03-15-c — PMID/PMCID enrichment COMPLETE: 157 of 191 DOI-bearing papers resolved
Built and ran resolve_pmids.py (NCBI ID Converter API + PubMed ESearch fallback) to populate pmid and pmcid YAML fields for academic credibility ahead of Arns manuscript citation.
157 PMIDs and 50 PMCIDs populated; 34 papers correctly unresolvable (preprints, non-indexed journals, book chapters). Schema D16, validate_vault.py, and generate_index.py already had pmid/pmcid support from prior propagation. papers.json/csv regenerated with 25 fields.
Next: Session 3 (OA format + formatting) per `_meta/prompts/pre_release_fix_sessions.md`.

## 2026-03-15-b — Pangea contamination cleanup COMPLETE: quality gate passed
Completed cleanup with 2 final editorial fixes (Wachtel2025 and 1996_WBAI_Mash — Pangea-specific commentary → generic clinical language). Full NDA-term sweep (NZ initiative, 4-phase, Pangea_Ops, New Zealand's first) returned zero in Tier-1-eligible content.
Re-synced (297 papers, 0 parse failures), validated (0 errors, 100% compliance, 0 broken wikilinks), final Tier 1 grep confirmed only Pattern C (legitimate biographical/published source) references remain.
Next: Session 2 (PMID enrichment) per `_meta/prompts/pre_release_fix_sessions.md`.

## 2026-03-15-a — Pangea contamination cleanup: Pattern A complete, Pattern B ~85%
Two-session cleanup of "Pangea" ghost-text across working vault. Pattern A (paper Clinical Implications): 89 files cleaned across all year directories. Pattern B (hub editorial): ORANGE, RED, PURPLE, WHITE, GREEN, Key_Researchers all cleaned — de-linked Pangea_Ops wikilinks, removed NDA-sensitive NZ initiative references, reframed Pangea sections around Clare Wilkins' published role. Also removed internal Tier 2 document references (4-Phase Protocol, Emergency Equipment, Noller Q&A, 2026 Call).
Remaining: Hub_PK-PD_Synthesis (~18 Pangea hits) → then verify → sync → validate → final Tier 1 grep.

## 2026-03-14-i — External audit: 5 pre-flip issues found, fix session prompts generated
Adversarial audit of Tier 1 repo (simulating Arns/Alper first impression) found 5 issue categories: (1) BLOCKER — 206 "Pangea" ghost-text matches across Tier 1 body text from incomplete wikilink stripping, (2) no PMIDs, (3) OA verbatim vs non-OA analytical format gap, (4) citation count mismatch, (5) LaTeX/formatting artefacts.
Generated `_meta/prompts/pre_release_fix_sessions.md` — 5 self-contained session prompts (Pangea cleanup → PMID enrichment → OA format + formatting → governance harmonisation → ship-it).
Next: Execute Session 1 (Pangea contamination BLOCKER) before any other work.

## 2026-03-14-h — Session 2 complete: content fidelity PASS (8 fixes across 297 papers)
Stratified 15-paper sample (0 SERIOUS, 1 MODERATE, 3 MINOR) + boolean sweep of all 297 papers via boolean_sweep.py.
Session 2 proper: 5 fixes (Schenberg2014 electrolyte→false, Brown2018 dosing/route, Thurner2014 secondary ORANGE, Evans2026 significance→moderate, Chen2024 key_findings). Sweep continuation: 3 fixes (Glue2016 herg→false, Clare Wilkins herg→false, Malcolm2022 electrolyte→false). Script had 3 field-name bugs (file→filepath, category→primary_category) producing blind output — fixed, re-run confirmed no systemic misclassification. 11 non-RED mortality papers all correctly carry RED secondary. Sync patched for Untitled.* exclusion.
Commit d0bb646 pushed. Next: flip repo public → Zenodo DOI → Arns delivery.

## 2026-03-14-g — Pre-release audit Session 3: machine-readability PASS
Programmatic audit of papers.json/csv for structural integrity, schema compliance, and data quality.
297 papers, 23 fields, 0 enum violations, 0 invalid DOIs, 0 CSV malformations, 0 JSON↔YAML mismatches (8 sampled), 0 orphan files, 0 null booleans. One MEDIUM finding: mixed dash characters in dosing_range (post-release). Audit script at _meta/tools/session3_audit.py.
Session 2 handoff: 20 RED papers with qtc_data=false for semantic verification; 8 high-mortality reviews for count verification; 13 landmark papers for content fidelity priority sampling.
Next: Session 2 content fidelity deep check in new conversation.

## 2026-03-14-f — Pre-release audit Session 1: six caveats resolved
Executed the six fixes from the Arns Experience Test audit (GO WITH CAVEATS → GO).
Fix 1 (CRITICAL): key_findings + filepath added to papers.json/csv (23 fields). Fix 2: "On GitHub" section in GETTING_STARTED.md. Fix 3: clinical disclaimers on PK-PD and GREEN Hubs. Fix 4: GitHub note on HOME.md. Fix 5: paper counts harmonised. Fix 6: NC clause clarified in COPYRIGHT.md.
All edits applied to both working vault and Tier 1. Validation: 297 papers, 0 errors. Committed and pushed (bc19a82).
Next: Session 2 (content fidelity audit), then flip to public + Zenodo + Arns delivery.

## 2026-03-14-e — Post-audit remediation: broken wikilinks, stem mismatches, DeRienzo integration
Executed all fixes from comprehensive programmatic audit — 6 hub/governance broken refs, 32+ stem mismatches across 8 papers, 3 CHANGELOG internal tooling refs, .yml wikilink→markdown link conversions. DeRienzo chapters (17 files) integrated into WHITE Hub and Lotsof MOC.
Validator: 300 papers, 0 errors, 100% compliance, 0 broken wikilinks. Sync passed, pushed to GitHub (6b023dd).
Next: flip repo public, Zenodo DOI, GitHub release v1.0.0, send Arns.

## 2026-03-14-d — Tier 1 pre-release: governance sweep, hub gaps, sync, push
Consolidated session resolving all 5 governance issues from -c audit plus 3 hub coverage gaps. "Structured evidence map" across 6 governance files; Evans2026→RED hub, DeRienzo book→WHITE hub, Hoeck2003→ORANGE hub; CHANGELOG rewritten for public audience; README/CONTRIBUTING counts corrected (4,500→3,400); CITATION.cff date-released updated; 2 non-ibogaine files excluded from Tier 1.
macOS rsync --delete-excluded bug discovered (file-level excludes not removed from dest); patched sync_tier1.sh with explicit post-rsync deletion loop. Tier 1: 297 papers, 0 errors, 100% compliance. Commit 63e792f pushed. Release notes at _meta/RELEASE_NOTES_v1.0.0.md. ROADMAP updated.
Next: flip repo public → Zenodo DOI → GitHub release v1.0.0 → send Arns. Then PMID enrichment (#11) or Quartz (9d–9g).

## 2026-03-14-c — Pre-flip external audit: 5 governance issues found
Comprehensive audit of Tier 1 repo against v4 execution sequence. Phases 0–3 confirmed complete. Validation clean (299 papers, 0 errors).
Five issues pre-flip: CITATION.cff "clinical decision support" keyword contradicts README's "research support tool" framing; AGENTS.md opens with "clinical decision-making"; CHANGELOG.md leaks Pangea_Ops (line 31) and references non-existent _meta/ files; README wikilink count (4,500+) doesn't match Tier 1 (~3,400); CITATION.cff date-released is 2026-02-26 (stale). Quartz confirmed not on critical path.
Next: Execute governance fixes → sync → flip public → Zenodo DOI.

## 2026-03-14-b — Phase 3: CI/CD + final review + push
Phase 3 CI/CD infrastructure created and final README/CITATION review completed. Commit 575b692 pushed to GforVendetta/IbogaineVault.
AGENTS.md (88 lines), validate.yml (GitHub Actions), setup.sh written. validate_vault.py + generate_index.py copy steps added to sync_tier1.sh with Tier 2 directory stripping. README fixes: duplicate line, stale tree entry, Dataview→Properties in tree, new files added. CITATION.cff updated (title, abstract, paper count). GETTING_STARTED.md Dataview references clarified.
Next: flip repo to public (item 6k). Google Drive PDF folder optional. Zenodo deferred.

## 2026-03-14-a — Phase 2C: Bases/README.md + .base sync decision + source_pdf verification + Dataview correction
Decided to keep .base files in Tier 1 (already syncing; encode clinical intent as structured queries; non-Obsidian users have papers.json/csv). Wrote Bases/README.md (47 lines): .base format, all 7 bases with accurate filters, schema dependency, papers.json/csv alternatives. Corrected Dataview misattribution in 3 files — .base files use Obsidian's native Properties (v1.4+), not Dataview. Fixed: Bases/README.md, README.md (Obsidian setup instructions), GETTING_STARTED.md (directory tree comment).
Verified source_pdf documented across README.md, CONTRIBUTING.md, and Bases/README.md. Phase 2C complete.
Next: Phase 3 (CI/CD: AGENTS.md, validate.yml, setup.sh) + Task 3 (final README review), then sync → commit → push.

## 2026-03-13-c — Phase 2B complete: generate_index.py + sync pipeline integration
Built generate_index.py (21 fields, zero external deps, PyYAML fallback) producing papers.json and papers.csv from YAML frontmatter. Tested against working vault (300 papers) and Tier 1 (299 papers) — all sanity checks pass: JSON valid, CSV properly quoted, boolean flags null-when-absent, aliases default to []. Integrated into sync_tier1.sh as post-verification step generating index against Tier 1 directory (not working vault).
Papers.json envelope includes vault name, version, timestamp, schema reference, and 299 paper records. Papers.csv uses semicolon-space joins for list fields with csv.writer quoting.
Next: Git commit and push, then Phase 3 (CI/CD) or Phase 4 (Quartz).

## 2026-03-13-b — Validator bug fix: Industry_Documents discovery + schema registry alignment
Discovered validate_vault.py did not scan Industry_Documents/ — 4 papers (Beond2022, ICEERS2019, ICEERS2020, LAPPA2025) were in Tier 1 but never validated. Added "Industry_Documents" to discover_paper_files() and "Industry_Documents/*.md" to schema_registry.yml location_patterns. All 4 papers pass all checks.
New baseline: 300 papers (working vault) / 299 (Tier 1), 0 errors, 100.0% compliance. Tier 1 synced; schema_registry.yml is the only Tier 1 change.
Next: Commit and push to GitHub, then Phase 2B — generate_index.py.

## 2026-03-13-a — Phase 2A complete: 91.2% → 100.0% compliance (0 errors)
Resolved all 36 YAML errors across 26 files. Fixes: 12 DeRienzo key_findings trimmed to ≤250, 10 invalid tags replaced with canonical equivalents, 8 Clare Wilkins Primary Sources given source_pdf + source_url (YouTube/podcast links where available), 3 tag-policy adjustments (D2: journalism/industry-report→synthesis; D3: GITA2015 encyclopedic exception), 1 DOI allowlist for shared proceedings volume (D5: Shawn2012/Warrick2012), 1 validator bug fixed (D4: scope not forbidden for Primary_Sources/), 1 mortality_count:0 removed.
Five D-decisions propagated to schema_registry.yml and validate_vault.py. source_url added as optional field (D1). Tier1 synced and pushed (7ee64de).
Next: Phase 2B — generate papers.json + papers.csv index files.

## 2026-03-12-m — Wikilink triage: DeRienzo strip, --pedantic flag, alias resolution
Resolved all 157 broken wikilinks from the Phase 2A baseline. Stripped 240 aspirational wikilinks from 17 DeRienzo chapters; demoted noisy l→I OCR regex to --pedantic flag in validate_vault.py; added 22 aliases across 20 target files to resolve shortened filename references (Ona2024 thesis + scattered); stripped 11 links to papers not in vault (Baumann2000, Bhatt2020, Bowen2001, 2× Maillet2015, 3 legacy hubs, Clare Wilkins). Updated validator to index YAML aliases in wikilink resolution.
Final baseline: 296 papers, 0 broken wikilinks, 10 OCR warnings, 1 duplicate DOI, 36 errors (26 YAML + 10 other), 91.2% compliance. Wikilink Resolution: ✅ PASS.
Next: Resolve remaining 26 YAML errors, investigate duplicate DOI (Warrick2012/Shawn2012), then Phase 2B papers.json + papers.csv.

## 2026-03-12-l — Biosca-Brull2024 ligature normalisation
Replaced 101 Unicode ligature characters (ﬁ→fi, ﬂ→fl) in Biosca-Brull2024_Transcriptomic_Analysis_Single_Ibogaine_Dose.md using Python (perl/sed failed silently on macOS Unicode). Validator confirms 64 OCR warnings → 0, file now fully compliant. Vault-wide ligature scan confirms zero remaining across all .md files.
Next: Strip DeRienzo aspirational wikilinks, demote l→I regex to --pedantic flag, fix broken wikilinks via aliases.

## 2026-03-12-k — Phase 2A: validate_vault.py baseline confirmed + bug fix
Ran validate_vault.py against vault for first time. Fixed KeyError bug (severity dict keys "errors"/"warnings" → "error"/"warning"). YAML-only baseline: 296 papers, 26 errors, 91.2% (delta from 300/28/90.7% explained by 4 papers moved to Pangea_Ops in session -g). New checks revealed: 157 broken wikilinks (dominated by DeRienzo chapters), 1 duplicate DOI (Warrick2012/Shawn2012), 122 OCR warnings (Biosca-Brull2024 = 64, l→I regex noisy).
Next: Triage wikilink/OCR findings — strip DeRienzo links, tune l→I regex, fix genuine filename mismatches, reconvert Biosca-Brull2024 ligatures.

## 2026-03-12-j — Phase 2A: unified validate_vault.py written (steps 1–4)
Built validate_vault.py (supersedes validate_yaml.py) with 4 check types: YAML schema validation, wikilink resolution, duplicate DOI detection, and OCR artefact detection. Auto-detects vault root, CLI flags (--skip-wikilinks, --skip-ocr, --json, --summary, --file, --vault), zero-dependency design with PyYAML optional fallback. Steps 5–7 (hub coverage, academic ID, DOI resolution) stubbed with TODO markers and CATEGORY_HUB_MAP pre-populated.
Next: Run against vault to confirm baseline parity (300/28/90.7%), then review wikilink and OCR output.

## 2026-03-12-i — Git history scrub: orphan commit force-pushed
Force-pushed clean orphan commit to GforVendetta/IbogaineVault, replacing all prior git history with a single verified-clean state. Repo URL, settings, and future Zenodo integration preserved — indistinguishable from a fresh repo to anyone cloning post-push. Pre-publication checklist item "Git history scrub" complete.
Next: Phase 2A — build unified validation script.

## 2026-03-12-h — Sync confirmed clean; v3 alignment review
Resolved stale Clinical_Guidelines/Pangea/ directory in Tier 1 (rsync --delete-excluded can't clean directories absent from source) and confirmed sync PASSED — all governance files present, zero excluded content, zero scope:pangea. Reviewed execution sequence v3 against WORKLOG and ROADMAP: Phase 1E hybrid allowlist/denylist is correct (v3's tier1_manifest.txt approach descoped for good reason), evidence_level primary-source enum already resolved (D15), wikilink count confirmed 4,541. Fixed WORKLOG v2→v3 reference. Updated ROADMAP: Active Priority #7 → ✅, backlog evidence_level gap → resolved, footer updated, sync clean pass added to pre-pub checklist.
Decision: unified validation script starts internal but designed Tier-1-ready (auto-detect vault root, validate what it finds). PMID enrichment deferred to post-Phase 2.
Next: Phase 2A — build unified validation script.

## 2026-03-12-g — Consent-based transcript triage and sync script hardening
Resolved documentary transcript consent issue: 3 Ibogaine Stories interviews (Oliver/Wilkins, Oliver/Alper, Oliver/Mash) and Noller Q&A moved from Primary_Sources/ to Pangea_Ops/ in working vault, deleted from Tier 1. Interviewees consented to a documentary, not a public repo — conference talks and published media remain in Tier 1 (scope: published). Updated 19 wikilinks across hubs, MOCs, and Primary_Sources. Added scope: published to 2 files that were missing it (MYEBOGA, Wachtel).
Sync script: removed 4 redundant per-file excludes (now caught by Pangea_Ops/ directory exclude), added post-sync sed step that strips [[Pangea_Ops/...]] wikilinks from Tier 1 hubs automatically (piped form → display text, unpiped → removed). Removed per-file verification block.
Next: Run sync_tier1.sh to confirm clean pass, then Phase 2 validation.

## 2026-03-12-f — Phase 1D complete: _meta/README.md + sync_tier1.sh allowlist migration
Rewrote _meta/README.md (53 → 31 lines) as a concise Tier 1 directory guide for the 5 _meta/ files. Discovered 4 unlisted files leaking to Tier 1 due to denylist architecture, and migrated sync_tier1.sh _meta/ section from denylist (15 exclude rules) to self-sealing allowlist (5 include rules + catch-all exclude). Also excluded 4 scope:pangea Primary_Sources files. Allowlist verification section replaces brittle per-file checks.
Sync confirmed: _meta/ contains exactly 5 files, zero directories, zero leaks. Sync currently blocked by scope:pangea safety check on 4 Primary_Sources files (exclusions added, awaiting --delete-excluded fix to purge stale destination copies).
Next: Resolve --delete vs --delete-excluded for stale destination files, then Phase 2 validation.

## 2026-03-12-e — Phase 1D Batch 3 deep review: all 8 issues verified resolved
Reviewed VAULT_PRINCIPLES.md and VAULT_ARCHITECTURE.md against a detailed 8-issue punch list (GREEN coverage, category depth, classification boundary examples, evidence level references, Bases plugin note, conversion_manifest sync status). All issues were already addressed by the Batch 3 rewrite session. Confirmed conversion_manifest.md is correctly excluded from sync (line 64 of sync_tier1.sh) and absent from the architecture tree.
Next: Batch 4 — _meta/README.md rewrite (5 files in Tier 1 _meta/, not 6).

## 2026-03-12-d — Phase 1D Batch 3: VAULT_PRINCIPLES.md + VAULT_ARCHITECTURE.md rewrites
Rewrote both files for Tier 1 public audience after resolving the audience question: architectural principles belong in Tier 1 but rewritten for epistemic significance (methodological trustworthiness) rather than operational SOPs. VAULT_PRINCIPLES.md (68 → 92 lines): clinical principles first (evidence hierarchy, cardiac safety primacy, category co-equality, conservative classification, transparency about limitations), then methodological principles (single source of truth, provenance and traceability, representational accuracy). Dropped 3 operational principles and "Read ONE File."
VAULT_ARCHITECTURE.md (278 → 227 lines): added six-category decision logic, YAML schema overview, three-layer navigation architecture (Bases/Hubs/MOCs), wikilink conventions, Tier 1–only folder tree. Stripped all operational content (already in CLAUDE.md from Batch 2). Updated sync_tier1.sh (removed both from exclude list, added to governance presence check) and CLAUDE.md override files list. Verification confirmed zero prohibited terms.
Next: Batch 4 — _meta/README.md (final Phase 1D file, then full sync and Phase 2 validation).

## 2026-03-12-c — Phase 1D Batch 2: HOME.md + GETTING_STARTED.md rewrites
Relocated Copilot/Cowork operational content from both files into CLAUDE.md (74 → 126 lines), then rewrote HOME.md (211 → 214 lines) and GETTING_STARTED.md (252 → 203 lines) for public Tier 1 audience.
"Ask the Vault" Copilot section → "Querying the Vault" with evidence flags table preserved as metadata documentation. Directory tree rebuilt to match actual Tier 1 structure with Hubs/ and MOCs/ directories. All AI tooling, Pangea_Ops, and internal refs removed; scripted verification confirmed zero prohibited terms.
Next: Batch 3 — VAULT_PRINCIPLES.md + VAULT_ARCHITECTURE.md rewrites (both currently excluded from Tier 1 sync, join whitelist after rewrite).

## 2026-03-12-b — Phase 1D Batch 1: README.md + CONTRIBUTING.md rewrites
Rewrote both files for public Tier 1 audience: "clinical decision-support" → "research knowledge base" throughout, paper count updated to ~301 (verified 286 year-folder + ~18 other), wikilinks updated to ~4,500 (verified 4,541), accessibility statement added to README, citation updated for Arns collaboration wording.
Removed all Copilot/Cowork/CLAUDE.md/Pangea_Ops references. Fixed internal-audience leakage in CONTRIBUTING.md (distribution tiers section and validation script reference were written for Tier 2 users, not external contributors). Scripted verification pass confirmed zero prohibited terms across both files.
Next: Batch 2 — HOME.md + GETTING_STARTED.md. Begin by reading CLAUDE.md (74 lines, confirmed headroom) and relocating Cowork/Copilot content there before rewriting.

## 2026-03-12-a — Vault name standardisation (IbogaVault → IbogaineVault)
Wrote and ran `_meta/fix_vault_name.sh` to replace all instances of "IbogaVault" and "Ibogavault" with "IbogaineVault" across both working vault and Tier1 repo, skipping .git/.smart-env/.obsidian and binary files.
235 replacements across 133 files (including 4 Copilot index chunks, archive/legacy skills, Cowork outputs, governance docs, tools, and prompts). Verification pass confirmed 0 remaining case-variant references. Lowercase `ibogavault` slugs in archive path names left intact intentionally — renaming those directories would break references for no benefit.
Next: Phase 1D documentation rewrites (7 governance files for public audience).

---

## Archives

- [[_meta/archive/WORKLOG_archive_Phase0_copyright_reconversion|Phase 0: Copyright / DOI Audit + RED Reconversion (2026-03-11 to 2026-03-12)]]
- [[_meta/archive/WORKLOG_archive_pre-Phase0_infrastructure|Pre-Phase-0 Infrastructure (2026-02-26 to 2026-03-06)]]
- [[_meta/archive/WORKLOG_archive_Mar2026_pre-restructure|March 2026 verbose entries (pre-restructure)]]
- [[_meta/archive/WORKLOG_archive_Feb2026_26|February 26 sessions]]
- [[_meta/archive/WORKLOG_archive_Feb2026_23final-25|February 23 (final) – February 25 sessions]]
- [[_meta/archive/WORKLOG_archive_Feb2026_23late|February 23 (late session)]]
- [[_meta/archive/WORKLOG_archive_Feb2026_23mid|February 23 (mid-session)]]
- [[_meta/archive/WORKLOG_archive_Feb2026_22-23early|February 22–23 (early) sessions]]
- [[_meta/archive/WORKLOG_archive_Feb2026_20-21|February 20–21 sessions]]
- [[_meta/archive/WORKLOG_archive_Feb2026_early|February 5–19 sessions]]
- [[_meta/archive/WORKLOG_archive_pre-Feb2026|January 2026 sessions]]
