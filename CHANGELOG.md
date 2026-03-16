---
title: "Changelog"
aliases: ["Version History", "What's New"]
---

# IbogaineVault Changelog

Version history for the IbogaineVault structured evidence map. Major additions, structural changes, and infrastructure milestones.

---

## 2026-02-26

### Structural
- **Hub back-links added to all papers** — every paper's See Also section now links back to its parent category hub, enabling bidirectional navigation
- **CONTRIBUTING.md created** — collaborator onboarding guide covering YAML schema, conversion workflow, tag taxonomy, and tier boundary rules
- **Tier boundary audit** — confirmed zero cross-tier broken links in public vault
- **Systemic coherence audit complete (C1–C7, E1–E6)** — _meta/ reconciliation, schema drift fixes, prompt archival, build tooling refresh, root directory cleanup

### Papers Added
- Rodger 2011 — Ibogaine: cultural traditions and contemporary use (WHITE)
- Lavaud 2017 — Iboga alkaloid extraction and biogenesis (ORANGE)
- Luciano 2000 — Withdrawal hyperalgesia ibogaine reversal (BLUE/RED)
- Pablo 1998 — Noribogaine NMDA receptor interactions (ORANGE)

### Infrastructure
- Validation infrastructure — YAML gates, tier-aware filtering, collision handling
- `_meta/tools/inject_hub_backlinks.py` — automated hub back-link injection
- `_meta/tools/validate_yaml.py` — schema validation against `schema_registry.yml`
- Build tooling refreshed — tag data regenerated (184→283 papers, 58→60 tags)
- **Git + GitHub initialised** — local git repository on `main` branch; private GitHub repo at `GforVendetta/IbogaineVault`. Provides version control, collaboration infrastructure, and path to Zenodo DOI citability. VAULT_ARCHITECTURE.md updated with Version Control section and git workflow documentation.

---

## 2026-02-23

### Structural
- **All 6 category hubs rebuilt to 100% coverage** — RED, GREEN, BLUE, PURPLE, WHITE, ORANGE
- **Hub_PK-PD_Synthesis Tier 3 final revision** — 394 lines, 141 wikilinks, 16 cross-paper synthesis entries (4 publishable, 4 clinical flag), first-ever assembled analogue hERG safety hierarchy
- **ORANGE Mechanisms Hub rebuild** — 9-batch programme, 116 primary + 14 secondary papers, 6 Research Arcs, 130 verified wikilinks
- **Schema registry created** — `_meta/schema_registry.yml` as single source of truth for all YAML schemas, enums, and field definitions
- **Key Researchers Hub + MOCs** — 15 researchers, Kenneth Alper MOC (14-entry reading path), Howard Lotsof MOC (8-entry reading path), Clare Wilkins MOC verified complete

### Papers Added (Batches 1–7, gap analysis)
- 72 papers converted from citation-mined gap analysis (52 papers identified from 14 vault reviews)
- Notable additions: Chen 2024 RIVM risk assessment (first national-level, 76pp, 34 deaths tabulated), Alper 2001 Review reconverted (475 lines from source), Alper 2001 Contemporary History reconverted (331 lines)

### Infrastructure
- DOI verification audit — 8 corrections applied
- Document_type/evidence_level mismatch audit — 3 corrections
- Industry document schema extended — `organisation` field + `industry-report` document_type
- Transcript schema retrofit — 19 transcripts validated

---

## 2026-02-19

### Structural
- **Phase 2 RED Audit complete** — all 19 cardiac safety papers verified against source PDFs (10.5% correction rate)
- **Natural language query capability deployed** — citation-locked queries with evidence-level filtering
- **Comprehensive audit complete (Tiers 1A–1C)** — 305 issues across 161 papers resolved
- **All 5 damage classes remediated** — operator corruption, table cell dropout, table omission, OCR errors, parenthetical stripping

### Infrastructure
- Paper ingestion pipeline — structured conversion workflow with 3-gate validation
- NLQ Architecture documented — `_meta/NLQ_ARCHITECTURE.md`

---

## 2026-01 (January)

### Foundation
- Vault created — initial paper conversions began
- YAML schema established with 6-category colour-coding system
- Tag taxonomy developed (62 canonical tags across topic/, mechanism/, method/ namespaces)
- Clinical Guidelines directory structured (GITA, IACT, Aotearoa)
- Primary Sources collection initiated (Clare Wilkins interviews, oral histories)

---

## Vault Statistics

| Metric | Value |
|--------|-------|
| Total documents | 300 |
| Date range | 1957–2026 |
| Cross-references | ~4,400 |
| Canonical tags | 62 |
| Category hubs | 6 (all at 100% coverage) |
| Researcher MOCs | 3 (Alper, Wilkins, Lotsof) |
| Clinical databases (Bases) | 7 |

---

*For vault architecture and design principles, see `_meta/VAULT_PRINCIPLES.md` and `_meta/VAULT_ARCHITECTURE.md`.*
