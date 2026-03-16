---
title: "Contributing to the IbogaineVault"
aliases: ["Contributing", "Contributor Guide"]
---

# Contributing to the IbogaineVault

Welcome — and thank you for contributing to ibogaine research infrastructure. This vault is a structured evidence map: accuracy directly impacts the quality of evidence synthesis available to researchers and clinicians. Please read this guide before adding or modifying content.

---

## Quick Orientation

The vault contains over 300 papers (1957–2026) converted to searchable markdown with structured YAML metadata. Everything is organised around six co-equal categories:

| Category | Hub | Focus |
|----------|-----|-------|
| 🔴 RED | [[RED_Cardiac_Safety_Hub]] | Cardiac safety, fatalities, hERG, adverse events |
| 🟢 GREEN | [[GREEN_Clinical_Protocols_Hub]] | Clinical protocols, guidelines, screening, dosing |
| 🟠 ORANGE | [[ORANGE_Mechanisms_Hub]] | Pharmacology, receptors, GDNF, analogues |
| 🔵 BLUE | [[BLUE_Outcomes_Hub]] | Clinical outcomes, trials, efficacy |
| 🟣 PURPLE | [[PURPLE_Phenomenology_Hub]] | Subjective experience, phenomenology |
| ⚪ WHITE | [[WHITE_Historical_Hub]] | Bwiti, Lotsof, policy, historical |

All six categories are equally important. RED is not "more important" than PURPLE — they serve different functions within the same research instrument.

---

## Adding Papers

### The Workflow

1. Read `_meta/schema_registry.yml` for field definitions and valid enums, and `_meta/Tag_Taxonomy.md` for the 62 canonical tags
2. Review the category assignment logic in [[_meta/VAULT_ARCHITECTURE|Vault Architecture]]
3. Read the source PDF
4. Convert following the YAML schema and body structure described below
5. Place the file in the appropriate year folder: `YYYY/AuthorYear_Short_Title.md`

### Critical Rules

- **YAML accuracy is paramount.** Every field in the frontmatter drives downstream queries. A miscategorised RED paper could mean cardiac safety evidence is missed during screening.
- **Use canonical tags only.** The 62-tag taxonomy is at `_meta/Tag_Taxonomy.md`. Do not invent new tags — if a concept isn't covered, discuss adding it.
- **Category assignment follows the decision logic** in [[_meta/VAULT_ARCHITECTURE|Vault Architecture]]. When in doubt, ask: "What clinical question does this paper primarily answer?"
- **`see_also` links should include a `**Parent hub:**` back-link** as the first item, mapping to the paper's primary category hub.

### YAML Essentials

The single source of truth for all field definitions is `_meta/schema_registry.yml`. Key fields:

| Field | Purpose | Example |
|-------|---------|---------|
| `category` | Primary colour category (RED/GREEN/ORANGE/BLUE/PURPLE/WHITE) | `RED` |
| `tags` | Canonical tags from taxonomy | `[topic/cardiac, mechanism/herg-blockade]` |
| `evidence_level` | Study methodology type | `rct`, `case-report`, `systematic-review` |
| `document_type` | What kind of document this is | `research-article`, `review`, `guideline` |
| `key_findings` | One-line clinical significance | `"First human PK study of ibogaine..."` |
| `qtc_data` / `herg_data` / `electrolyte_data` | Boolean flags for cardiac safety queries | `true` / `false` |

---

## Format: Open Access vs Non-OA Papers

The vault contains two paper formats — this is a deliberate design decision, not an oversight. Open access papers may include more extensive source material (original abstracts, detailed results, full data tables) consistent with the terms of their CC licences. Non-OA papers from major publishers are presented as original analytical works: structured Key Findings and Clinical Implications written in the vault curator's voice, with reconstructed data tables and cross-reference annotations. Both formats carry identical structured YAML metadata and are equally queryable. Extending the vault's analytical format to all papers (including OA) is planned for v1.1 — see [COPYRIGHT.md](COPYRIGHT.md) for full details on how each paper type is represented.

---

## Wikilink Integrity

All wikilinks in contributed papers should point to files that exist in this repository. If you're unsure whether a file is included, check the directory structure or ask.

---

## Modifying Existing Content

- **Do not change YAML frontmatter** without understanding the downstream impact — Bases, Dataview queries, and validation tooling all depend on it
- **Preserve wikilinks** — the vault has ~4,400 cross-references; broken links degrade the knowledge network
- Contributions will be validated against the schema registry before merging

---

## Key References

| Document | Location | Purpose |
|----------|----------|---------|
| Tag taxonomy | `_meta/Tag_Taxonomy.md` | 62 canonical tags — the only permitted tags |
| Schema registry | `_meta/schema_registry.yml` | Single source of truth for all schemas |
| Architecture | `_meta/VAULT_ARCHITECTURE.md` | Folder structure, Bases, navigation layers |
| Vault Principles | `_meta/VAULT_PRINCIPLES.md` | Design philosophy and clinical integrity principles |

---

## Source PDFs

The vault's markdown files are the knowledge layer — structured metadata, cross-references, and clinical annotations. The original source PDFs are stored separately in a shared Google Drive folder, not in this repository. Git is not designed for large binary files and would bloat the repository permanently.

**Accessing source papers:**

1. **By DOI** — Every paper's YAML frontmatter includes a `doi` field. Most recent papers are open-access or available through institutional access.
2. **Shared Google Drive** — For paywalled, pre-print, or hard-to-find papers, the complete PDF collection is available at: [Google Drive link — request access from Philip]
3. **By request** — Contact Philip if you need a specific PDF not available via the above routes.

**Adding new papers:** When converting a new paper, add the source PDF to the shared Google Drive folder using the naming convention `AuthorYear_Short_Title.pdf` (matching the vault filename). The PDF should never be committed to the git repository.

---

## Questions?

Contact Philip Kagalovsky (vault architect) before making structural changes. For paper conversions, the schema registry and architecture reference provide the complete specification.
