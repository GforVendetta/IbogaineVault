# Changelog

## v1.0.2 — 2026-03-31

Analytical reconversions, methodology documentation, cross-verification infrastructure.

### Content

- **28 papers reconverted** from academic-retained to vault-analytical format across RED cardiac safety (10), GREEN protocols (5), and BLUE outcomes (13) — the three most clinically important categories. Each passed 8-check validation including n-gram copyright scoring and numerical fidelity audit against source PDFs
- Net effect: ~8,100 lines of source-proximate text replaced by ~4,800 lines of original analytical work

### Methodology & quality

- **`_meta/METHODOLOGY.md`** — First public documentation of conversion process, licence-aware copyright compliance, n-gram validation, numerical fidelity auditing, quality assurance, and AI-assisted methodology disclosure
- **Cross-model verification pilot** published at `_meta/quality/`: 5 papers blind-extracted by GPT-5.4 Pro, 46 genuine findings (91.3% silent omission, 0% fabrication), 1,008-line report with error taxonomy
- `generate_index.py` expanded to 34 indexed fields; `freely-distributed` licence type added to schema and validator

### Structural

- **Fatalities Hub** expanded: 6 baseline discrete case reports (Marker2002–Meisner2016) with provenance chains; Warrick2012/Jalal2013 confirmed same fatality via matching postmortem concentrations
- **`GETTING_STARTED.md`** expanded with mortality deduplication guidance (`mortality_scope` field explanation and worked algorithm)
- **File renames:** `Williams2025` → `Lissemore2025` (journal first-author correction); `QuinnWilliams2025` → `Williams2025`
- **Licence audit:** ~20 papers corrected for `licence_type`, `licence_verified`, `open_access`
- `schema_registry.yml`: `sample_size` convention documented (total enrollment vs active-arm)
- CI badge added to README; `Bouso2019` ghost file removed (duplicate DOI with `Bouso2020`)

## v1.0.1 — 2026-03-23

Documentation and repository polish.

- Added `mortality_scope` field documentation to README (deduplication methodology for fatality counts)
- Standardised hub naming: `Hub_PK-PD_Synthesis.md` → `ORANGE_PK-PD_Hub.md`
- Expanded CHANGELOG with v1.1 roadmap details
- README rewrite: Quick Start section, Python query examples, programmatic access guidance, roadmap preview
- Updated CITATION.cff to v1.0.1 with Zenodo version-specific DOI
- Added `vault_grep.sh` search tooling with exclusion list for maintenance queries
- Sync pipeline fixes for edge cases in `_meta/` allowlist handling

## v1.0.0 — 2026-03-22

Initial public release of the IbogaineVault Tier 1 research support repository.

### Contents

- **303 papers** (1957–2026) with standardised YAML frontmatter and 62-tag canonical taxonomy
- **9 curated research hubs** spanning cardiac safety, clinical protocols, pharmacology, outcomes, phenomenology, and history/policy
- **7 queryable bases** for structured metadata access
- **3 researcher MOCs** (Maps of Content) for Clare Wilkins, Ken Alper, and Howard Lotsof
- **~3,400 cross-references** linking papers to hubs, bases, and related research
- Machine-readable index: `papers.json` and `papers.csv`
- Validation tooling: `validate_vault.py`

---

## Planned — v1.1

- **OA format consistency:** Extending vault analytical format (Key Findings, Clinical Implications, Methodology, Data Tables, Limitations) to all open-access papers — the centrepiece of v1.1
- **`oa_class` copyright classification:** Per-paper open-access classification field (`open-access`, `subscription`, `grey-literature`, `small-publisher`) for transparent copyright status
- **`mortality_scope` documentation:** Full methodological documentation of the `mortality_scope` enum that prevents naïve-sum errors when aggregating mortality counts across papers
- **Hub naming standardisation:** All hubs now follow `{CATEGORY}_{Topic}_Hub.md` convention (completed: `Hub_PK-PD_Synthesis.md` → `ORANGE_PK-PD_Hub.md`)
- **Quartz web layer:** Navigable research website with category-coloured graph and filtered clinical pages
- **Enhanced validation and schema consistency:** Expanded `validate_vault.py` rules covering new fields, enum consistency audits, and link verification tooling
- **Obsidian setup script:** `setup_obsidian.sh` to convert markdown links to Obsidian's native wikilink format for users who prefer the full Obsidian experience
- **`references_stripped` metadata field:** Boolean flag indicating whether a paper's reference list was removed during conversion, enabling future systematic restoration
- **Resolver exclusion list:** Identifier resolution tooling now skips papers with known cross-match conflicts to prevent incorrect auto-assignment