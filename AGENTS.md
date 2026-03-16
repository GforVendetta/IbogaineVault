# AGENTS.md — Codex Agent Instructions

## What This Vault Is

The IbogaineVault is a structured evidence map containing ~300 academic papers on
ibogaine (1957–2026) converted to markdown with structured YAML frontmatter.
Papers live in year folders (`1991/`, `2016/`, etc.) and are categorised into
six colour-coded domains: RED (cardiac safety), GREEN (clinical protocols),
ORANGE (pharmacology), BLUE (outcomes), PURPLE (phenomenology), WHITE (history/policy).

This vault supports evidence-based research. Accuracy is critical —
miscategorised evidence can impact patient safety protocols.

## Repository Structure

```
├── 1957–2026/           # Paper markdown files by year
├── Clinical_Guidelines/ # Clinical protocol documents
├── Primary_Sources/     # Published interviews, transcripts
├── Industry_Documents/  # Industry submissions and reports
├── Other/               # Materials outside standard categories
├── Hubs/                # Curated entry points by category
├── MOCs/                # Researcher-centred navigation maps
├── Bases/               # Queryable database views (via Obsidian Properties)
├── _meta/               # Governance: schema registry, tag taxonomy, architecture
├── papers.json          # Machine-readable index (all papers, all fields)
├── papers.csv           # Flat export (core fields only)
├── validate_vault.py    # Integrity validator (YAML, wikilinks, DOIs, OCR)
├── generate_index.py    # Regenerates papers.json + papers.csv
└── GETTING_STARTED.md   # Human-readable orientation
```

## Schema Authority

`_meta/schema_registry.yml` is the single source of truth for all YAML fields,
enums, types, and validation rules. Every paper has required fields including:
`title`, `authors`, `year`, `category`, `tags`, `key_findings`, `document_type`,
`clinical_significance`, `evidence_level`, `qtc_data`, `electrolyte_data`,
`herg_data`, `contraindications`, `aliases`, `source_pdf`.

Tags are drawn from a 62-tag canonical taxonomy defined in `_meta/Tag_Taxonomy.md`.

## What Agents CAN Do

1. **Run validation:**
   ```bash
   python3 validate_vault.py              # Full report
   python3 validate_vault.py --summary    # Summary only
   python3 validate_vault.py --json       # Machine-readable output
   python3 validate_vault.py --file path  # Single file
   ```
   Exit code 0 = pass, 1 = failures detected.

2. **Regenerate the index:**
   ```bash
   python3 generate_index.py --vault . --output .
   ```
   This rebuilds `papers.json` and `papers.csv` from current vault state.

3. **Read and analyse** any markdown file, YAML frontmatter, or governance doc.

4. **Report issues** found by validation — broken wikilinks, schema violations,
   duplicate DOIs, OCR artefacts.

## What Agents MUST NOT Do

- **Modify YAML frontmatter** — field values are clinically validated by humans.
- **Modify hub content** (`Hubs/`), MOCs (`MOCs/`), or governance docs (`_meta/`).
- **Add, remove, or rename paper files** — the corpus is curated.
- **Modify schema files** — `schema_registry.yml` and `Tag_Taxonomy.md` are authoritative.
- **Modify `CITATION.cff`**, `LICENSE`, or `CONTRIBUTING.md`.

## papers.json

Each entry contains the full YAML frontmatter of a paper plus a `_vault_path`
field. The file is a JSON array, one object per paper. `papers.csv` contains
core fields (title, authors, year, category, document_type, evidence_level, doi)
for tabular queries.

## Setup

```bash
bash setup.sh          # Installs PyYAML
python3 validate_vault.py --summary   # Verify integrity
```

Requires Python 3.8+ and PyYAML. The validator includes a built-in YAML fallback
parser but PyYAML is preferred for full compliance.
