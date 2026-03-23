# Changelog

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
