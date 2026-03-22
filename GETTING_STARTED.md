---
title: "Getting Started with This Vault"
tags:
  - meta
  - guide
aliases: ["Getting Started", "Quick Start"]
---

# Getting Started with This Vault

Welcome to your ibogaine research library — over 300 academic papers, clinical documents, and primary sources (1957–2026), converted to searchable markdown with structured metadata.

---

## Viewing This Vault

### On GitHub (or any markdown viewer)

All content is readable as standard markdown. For programmatic access to the full dataset:

- **[papers.json](papers.json)** — Machine-readable index of all ~300 papers with structured metadata (category, evidence level, mortality count, QTc data, key findings, DOI, and more). Load in Python, R, or any JSON-capable tool to filter and query systematically.
- **[papers.csv](papers.csv)** — Flat CSV export of the same data. Opens directly in Excel, Google Sheets, or R.

To find mortality data: filter `papers.json` for `mortality_count > 0` (31 papers). To find cardiac safety evidence: filter for `primary_category: "RED"` (47 papers). To find papers with QTc data: filter for `qtc_data: true` (54 papers).

All cross-references between papers are standard markdown links — clickable on GitHub and in any markdown viewer. For the full interactive experience with graph view, backlinks, and queryable databases, open the vault in [Obsidian](https://obsidian.md) (free, v1.4+).

### In Obsidian (full interactive experience)

1. Clone this repository
2. Open the folder as an Obsidian vault
3. Start from HOME.md — the dashboard with links to all Hubs
4. Bases use native Obsidian Properties (no community plugins needed)

Links use standard markdown format for broad compatibility. A setup script (`setup_obsidian.sh`) to convert to Obsidian's native double-bracket link format for enhanced graph and backlink features is planned for v1.1.

---

## How Papers Are Organised

### By Folder (Year)
Papers live in year folders: `1991/`, `2016/`, `2024/`, etc. The filename convention is `AuthorYear_Short_Title.md` — for example, `Alper2016_hERG_Blockade.md`.

### By Category (YAML Field)
Every paper has a `category` field in its frontmatter:

| Category | Meaning |
|----------|---------|
| 🔴 RED | Cardiac safety, fatalities, adverse events |
| 🟢 GREEN | Clinical protocols, guidelines, screening |
| 🟠 ORANGE | Pharmacology, mechanisms, receptors |
| 🔵 BLUE | Clinical outcomes, trials, efficacy |
| 🟣 PURPLE | Subjective experience, phenomenology |
| ⚪ WHITE | Historical, Bwiti, policy |

*Use `All_Papers.base` or graph view to see current counts per category.*

### By Topic (Tags)
Papers have hierarchical tags describing their content:

| Namespace | Examples |
|-----------|----------|
| `topic/` | `topic/cardiac`, `topic/noribogaine`, `topic/veterans`, `topic/gdnf` |
| `mechanism/` | `mechanism/herg-blockade`, `mechanism/sert-inhibition`, `mechanism/kappa-opioid` |
| `method/` | `method/clinical-trial`, `method/preclinical`, `method/systematic-review` |

See [Tag Taxonomy](_meta/Tag_Taxonomy.md) for the complete 62-tag list.

---

## Understanding Evidence Levels

The vault assigns an evidence level to every paper based on study methodology. This metadata is stored in the `evidence_level` YAML field and enables filtering by strength of evidence.

| Evidence Level | Meaning | Weight |
|----------------|---------|--------|
| `RCT` | Randomised controlled trial | Highest |
| `systematic-review` | Meta-analysis or systematic review | Highest |
| `clinical-guideline` | Clinical practice guideline (GITA, IACT) | Highest |
| `cohort-study` | Prospective cohort study | Moderate |
| `case-report` | Single case | Lower generalisation, but crucial for adverse events |
| `preclinical` | Animal or in-vitro study | Mechanistic context only |

Evidence levels follow the hierarchy used in clinical research: RCTs and systematic reviews carry the most weight for treatment decisions, but case reports are critical for documenting adverse events where controlled trials would be unethical. Preclinical studies provide mechanistic context that informs — but does not replace — clinical evidence.

For safety-critical queries (cardiac risk, contraindications, drug interactions), always review the source papers directly rather than relying on any synthesis.

---

## How to Find Things (Obsidian)

### Method 1: Quick Switcher — Fastest
Press `Cmd + O` and start typing:
- Author name: `alper`, `mash`, `williams`, `cherian`
- Year: `2024`, `2016`
- Topic: `herg`, `gdnf`, `cardiac`, `magnesium`

### Method 2: Search
Press `Cmd + Shift + F` for full-text search across all papers.

### Method 3: Graph View
Press `Cmd + G` to see papers as a colour-coded network. Categories are automatically coloured:
- 🔴 Red nodes = cardiac safety
- 🟢 Green nodes = clinical protocols
- 🟠 Orange nodes = mechanisms
- 🔵 Blue nodes = outcomes
- 🟣 Purple nodes = phenomenology
- ⚪ Grey nodes = historical

### Method 4: Hub Navigation
Start from [HOME](HOME.md) and follow links to domain-specific hubs:
- [RED_Cardiac_Safety_Hub](Hubs/RED_Cardiac_Safety_Hub.md) — Start here for safety-critical evidence
- [GREEN_Clinical_Protocols_Hub](Hubs/GREEN_Clinical_Protocols_Hub.md) — GITA guidelines, screening protocols
- [ORANGE_Mechanisms_Hub](Hubs/ORANGE_Mechanisms_Hub.md) — Receptor pharmacology, GDNF, 18-MC
- [Key_Researchers_Hub](Hubs/Key_Researchers_Hub.md) — Navigate by researcher (Alper, Mash, Noller, etc.)
- [Clare_Wilkins_MOC](MOCs/Clare_Wilkins_MOC.md) — Clare Wilkins's complete materials (primary sources + publications)

### Method 5: Dataview Queries (Optional Plugin)
With the [Dataview](https://github.com/blacksmithgu/obsidian-dataview) community plugin, you can query the vault programmatically. For example, to list all RED papers with QTc data:

```dataview
TABLE evidence_level, key_findings
FROM ""
WHERE category = "RED" AND qtc_data = true
SORT year DESC
```

See [Technical Reference](_meta/VAULT_ARCHITECTURE.md) for the Bases system and more query patterns.

---

## Reading a Paper

Each paper contains:

1. **YAML Frontmatter** — structured metadata for queries
2. **Title & Citation** — original publication details
3. **Key Findings** — one-line clinical significance summary
4. **Full Content** — converted markdown text with tables/figures
5. **See Also** — cross-references to related papers

### Understanding Paper Metadata

Every paper has structured metadata (YAML frontmatter) at the top that enables filtering and querying. You can see it when you open any paper — fields like `category`, `tags`, `evidence_level`, `key_findings`, and `doi`. You do not need to understand or edit this metadata to use the vault. The structured fields power the Bases (via native Obsidian Properties) and enable advanced Dataview queries.

---

## Essential Keyboard Shortcuts

| Action | Mac | What it does |
|--------|-----|--------------|
| Quick switcher | `Cmd + O` | Jump to any paper by name |
| Search all files | `Cmd + Shift + F` | Full-text search |
| Graph view | `Cmd + G` | Visual network of papers |
| Back | `Cmd + Alt + ←` | Previous note |
| Forward | `Cmd + Alt + →` | Next note |
| Toggle sidebar | `Cmd + \` | Hide/show file list |
| Command palette | `Cmd + P` | All available commands |

---

## Recommended First Steps

1. **Open [HOME](HOME.md)** — Dashboard with links to all Hubs and safety essentials
2. **Read RED papers first** — Cardiac safety is paramount
3. **Explore the Hubs** — Each hub includes "How We Got Here" research arcs tracing how understanding evolved
4. **Explore the graph** — `Cmd + G` to visualise connections
5. **Query the Bases** — Filter by category, evidence level, or tags (no plugins needed)

---

## Vault Structure

```
IbogaineVault/
├── HOME.md                      # Dashboard — start here
├── GETTING_STARTED.md           # This onboarding guide
├── CONTRIBUTING.md              # How to contribute
├── README.md                    # Repository overview
├── CHANGELOG.md                 # Version history
├── COPYRIGHT.md                 # Copyright and licensing details
├── CITATION.cff                 # Machine-readable citation metadata
├── LICENSE                      # Licence file
│
├── Hubs/                        # Domain hubs by category
│   ├── RED_Cardiac_Safety_Hub.md
│   ├── GREEN_Clinical_Protocols_Hub.md
│   ├── BLUE_Outcomes_Hub.md
│   ├── ORANGE_Mechanisms_Hub.md
│   ├── PURPLE_Phenomenology_Hub.md
│   ├── WHITE_Historical_Hub.md
│   ├── Hub_PK-PD_Synthesis.md
│   └── Key_Researchers_Hub.md
│
├── MOCs/                        # Researcher Maps of Content
│   ├── Kenneth_Alper_MOC.md
│   ├── Clare_Wilkins_MOC.md
│   └── Howard_Lotsof_MOC.md
│
├── 1957/ ... 2026/              # Papers organised by publication year
├── Bases/                       # Queryable databases (native Properties)
├── Clinical_Guidelines/         # GITA, IACT, Aotearoa protocols
├── Primary_Sources/             # Interview transcripts, oral histories
├── Industry_Documents/          # Beond, ICEERS reports
├── Other/                       # Miscellaneous
│
├── _meta/                       # Administrative documents
│   ├── schema_registry.yml      # Single source of truth for YAML schemas
│   ├── Tag_Taxonomy.md          # 62 canonical tags
│   └── README.md                # Directory guide
└── .gitignore
```

### Source PDFs

The original research PDFs are not stored in this repository — they live in a shared Google Drive folder. Each paper's YAML frontmatter includes a `doi` field for independent access. If you need PDFs that are not available via DOI, request access to the shared collection from Philip.

---

## Questions?

This vault was created by converting PDFs to searchable markdown with structured metadata.

- **[Technical Reference](_meta/VAULT_ARCHITECTURE.md)** — Bases syntax, folder structure, YAML schema overview
- **[Tag Taxonomy](_meta/Tag_Taxonomy.md)** — Complete list of 62 canonical tags
- **[Design Principles](_meta/VAULT_PRINCIPLES.md)** — Quality standards and clinical integrity principles
- **[CONTRIBUTING](CONTRIBUTING.md)** — How to contribute papers, corrections, or improvements
