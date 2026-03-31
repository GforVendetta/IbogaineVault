[![DOI](https://zenodo.org/badge/1167860310.svg)](https://doi.org/10.5281/zenodo.19159665)

# IbogaineVault

**A structured evidence map for ibogaine science**

Over 300 documents · 1957–2026 · 6 categories · 3,400+ cross-references · Structured YAML metadata

![Version](https://img.shields.io/badge/version-1.0.2-blue)
![Status](https://img.shields.io/badge/status-active_development-green)
![Papers](https://img.shields.io/badge/papers-304-brightgreen)
![License](https://img.shields.io/badge/license-CC_BY--NC--SA_4.0-lightgrey)
![CI](https://github.com/GforVendetta/IbogaineVault/actions/workflows/validate.yml/badge.svg)

v1.1 in active development — analytical format expansion, web publishing, enhanced tooling. See [CHANGELOG](CHANGELOG.md) for the roadmap.

---

## What is this?

The IbogaineVault is a structured evidence map of ibogaine research. Every paper has been converted from PDF to searchable markdown with standardised clinical metadata — enabling systematic queries across seven decades of research that previously existed only as scattered, disconnected publications.

This vault originated from clinical practice at [Pangea Biomedics](https://pangeabiomedics.com) and now serves the broader ibogaine research community. Accuracy is critical: miscategorised cardiac safety evidence can impact patient safety.

## Who is this for?

- **Researchers** investigating ibogaine pharmacology, safety, or clinical outcomes
- **Clinicians** reviewing the evidence base for ibogaine-assisted treatment
- **Collaborators** contributing to systematic reviews, meta-analyses, or fatality documentation
- **Students and journalists** seeking a navigable entry point into a fragmented literature

This is a structured evidence map, not medical advice. It does not make treatment recommendations. It synthesises and organises published evidence so that researchers and clinicians can find what they need efficiently.

## Quick start

**Browse on GitHub** — all markdown renders natively. Start from [HOME.md](HOME.md) or jump to any [category hub](#categories).

**Programmatic access** — download [`papers.json`](papers.json) (all 304 papers, all metadata fields) or [`papers.csv`](papers.csv) (flat export for R, Excel, or pandas). Load into any analysis environment in seconds:

```python
import json
papers = json.load(open("papers.json"))["papers"]

# All papers with QTc data published after 2015
qtc_recent = [p for p in papers if p.get("qtc_data") and p["year"] > 2015]

# Fatality papers — deduplicated by mortality_scope (see below)
discrete_deaths = [p for p in papers if p.get("mortality_scope") == "discrete-cases"]

# Every RED cardiac safety paper with sample size > 20
cardiac_trials = [p for p in papers if p["primary_category"] == "RED" and (p.get("sample_size") or 0) > 20]
```

**Full interactive experience** — clone the repository and open in [Obsidian](https://obsidian.md) (v1.4+) for graph view, backlinks, and queryable databases. A setup script (`setup_obsidian.sh`) to convert links to Obsidian's native format is coming in v1.1.

<details>
<summary>Obsidian setup instructions</summary>

1. Clone this repository
2. Open the folder as an Obsidian vault
3. Start from [HOME.md](HOME.md) — bases use native Properties (no plugins needed)

Links use standard markdown format for broad GitHub compatibility. In Obsidian, all links work natively; `setup_obsidian.sh` (v1.1) will additionally enable backlinks and graph traversal across cross-references.

</details>

## Categories

The vault organises research into six co-equal categories. All are equally important — they serve different functions within the same research instrument.

| Category | Hub | Focus |
|----------|-----|-------|
| 🔴 RED | [Cardiac Safety](Hubs/RED_Cardiac_Safety_Hub.md) | Cardiac safety, fatalities, hERG blockade, QTc, adverse events |
| 🟢 GREEN | [Clinical Protocols](Hubs/GREEN_Clinical_Protocols_Hub.md) | Screening, dosing, monitoring, clinical guidelines |
| 🟠 ORANGE | [Mechanisms](Hubs/ORANGE_Mechanisms_Hub.md) | Pharmacology, receptors, GDNF, analogues, PK/PD |
| 🔵 BLUE | [Outcomes](Hubs/BLUE_Outcomes_Hub.md) | Clinical trials, observational studies, efficacy data |
| 🟣 PURPLE | [Phenomenology](Hubs/PURPLE_Phenomenology_Hub.md) | Subjective experience, altered states, therapeutic process |
| ⚪ WHITE | [Historical](Hubs/WHITE_Historical_Hub.md) | Bwiti tradition, Howard Lotsof, policy, legal history |

## Paper format

Every paper includes structured YAML frontmatter with clinical and bibliographic metadata:

```yaml
title: "Paper title"
authors: ["Author1", "Author2"]
year: 2024
doi: "10.xxxx/xxxxx"
pmid: "12345678"
pmcid: "PMC12345678"
issn: "0000-0000"
category: RED                       # Primary classification
secondary_categories: [GREEN, ORANGE]
tags: [topic/cardiac, topic/qtc, mechanism/herg-blockade]
evidence_level: rct                 # rct | cohort | case-series | case-report | ...
sample_size: 30
route: oral                         # oral | intravenous | intramuscular | ...
dosing_range: "8–12 mg/kg"
qtc_data: true
herg_data: false
electrolyte_data: true
mortality_count: 0
mortality_scope: cumulative-review  # cumulative-review | discrete-cases | incidental
contraindications: ["pre-existing cardiac conditions", "..."]
```

This metadata enables systematic queries: "Show all RED papers with hERG data published after 2015" or "List contraindications across all clinical trials with sample size > 20." The full schema — including all enums, field definitions, and validation rules — is defined in [`_meta/schema_registry.yml`](_meta/schema_registry.yml).

> [!IMPORTANT]
> **Mortality scope — why this matters for accurate fatality counts**
>
> Papers that report deaths carry a `mortality_scope` field that classifies *how* the paper reports mortality: `cumulative-review` (a systematic tally drawing on the broader literature), `discrete-cases` (original case reports of individual deaths), or `incidental` (deaths mentioned but not the paper's primary contribution). This distinction is critical for accurate mortality analysis — naïvely summing `mortality_count` across papers without filtering by scope will produce inflated totals, because cumulative reviews already include deaths reported in discrete case papers. Any systematic count must deduplicate by scope.
>
> For a complete navigable index of all ibogaine fatality literature — including cumulative reviews, discrete case reports, and baseline reference papers — see the [Fatalities Hub](Hubs/RED_Fatalities_Hub.md).

## Navigation layers

The vault uses three complementary navigation layers:

- **Hubs** — Curated category entry points with narrative synthesis and cross-paper analysis
- **MOCs** (Maps of Content) — Researcher-centred navigation following individual contributors across categories
- **Bases** — Queryable databases for structured filtering (e.g., all papers with QTc data, all dosing protocols). Base files (`.base`) use Obsidian's native Properties view; for programmatic access to the same data, use [`papers.json`](papers.json) or [`papers.csv`](papers.csv)

## Structure

```
IbogaineVault/
├── 1957–2026/           # Papers organised by publication year
│   └── AuthorYear_Short_Title.md
├── Hubs/                # Category hubs with cross-paper synthesis
├── MOCs/                # Researcher maps of content
├── Bases/               # Queryable databases (Obsidian Properties view;
│   ├── All_Papers.base  #   see papers.json for programmatic equivalent)
│   ├── Cardiac_Safety.base
│   ├── Dosing_Protocols.base
│   └── ...
├── Clinical_Guidelines/ # Treatment guidelines and protocols
├── Primary_Sources/     # Interviews, transcripts, oral history, memoirs
├── Industry_Documents/  # Organisational reports and analyses
├── Other/               # Experience reports, journalism, legal, books
├── _meta/               # Schema, taxonomy, architecture docs
│   ├── schema_registry.yml      # Single source of truth for all schemas
│   ├── Tag_Taxonomy.md          # 62 canonical tags
│   ├── VAULT_ARCHITECTURE.md    # Three-layer navigation design
│   ├── VAULT_PRINCIPLES.md      # Design philosophy and clinical principles
│   ├── METHODOLOGY.md           # Conversion methodology and copyright compliance
│   └── README.md                # _meta/ directory guide
├── HOME.md              # Dashboard and entry point
├── GETTING_STARTED.md   # Orientation guide
├── CONTRIBUTING.md      # How to add papers
├── CHANGELOG.md         # Version history and v1.1 roadmap
├── COPYRIGHT.md         # Copyright and licensing details
├── CITATION.cff         # Machine-readable citation metadata
├── LICENSE              # CC BY-NC-SA 4.0
├── papers.json          # Machine-readable index (all papers, all metadata)
├── papers.csv           # Flat export (core fields for tabular queries)
├── validate_vault.py    # Integrity validator (YAML schema, cross-references)
└── generate_index.py    # Regenerates papers.json + papers.csv
```

## What's coming in v1.1

- **Analytical format expansion** — extending structured Key Findings, Clinical Implications, and Methodology sections across all open-access papers for richer programmatic access
- **Quartz web layer** — a navigable research website with category-coloured graph visualisation and filtered clinical pages, no installation required
- **`oa_class` copyright classification** — per-paper open-access status field for transparent copyright and reuse information
- **Enhanced validation** — expanded schema consistency audits, link verification, and new metadata fields
- **Obsidian setup script** — `setup_obsidian.sh` to convert links to native wikilink format for full graph and backlink features

See [CHANGELOG.md](CHANGELOG.md) for the complete version history and roadmap.

## Citation

If you use the IbogaineVault in your research, please cite:

> Kagalovsky, P. (2026). *IbogaineVault: A Structured Evidence Map for Ibogaine Science* (v1.0.2) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.19159665

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding papers, the YAML schema, tag taxonomy, and quality standards. If you identify errors or have suggestions, please [open an issue](https://github.com/GforVendetta/IbogaineVault/issues).

## Copyright and licence

This vault contains **analytical summaries** of published research, not the original publications. Source PDFs are not included. Papers from major publishers have been converted to original analytical works — structured critical analyses written in the vault curator's own voice, with reconstructed data tables and cross-reference annotations. All entries include complete YAML metadata and cross-references. For detailed methodology including copyright compliance, licence-aware conversion posture, and n-gram validation, see [METHODOLOGY](_meta/METHODOLOGY.md).

All original vault content (metadata schemas, cross-references, hub syntheses, analytical commentary) is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Individual papers retain their original copyright and are referenced via DOI. See [COPYRIGHT.md](COPYRIGHT.md) for full details and [LICENSE](LICENSE) for the vault licence.

## Acknowledgements

The clinical framework underlying this vault was informed by the practice of Clare Wilkins (Clinical Director, Pangea Biomedics — 800+ ibogaine treatment sessions) and Sarita Wilkins (Therapeutic Integration, Pangea Biomedics).
