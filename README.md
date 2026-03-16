# IbogaineVault

**A structured evidence map for ibogaine science**

~300 documents · 1957–2026 · 6 categories · 4,400+ cross-references · Structured YAML metadata

---

## What is this?

The IbogaineVault is a structured evidence map of ibogaine research. Every paper has been converted from PDF to searchable markdown with standardised clinical metadata — enabling systematic queries across seven decades of research that previously existed only as scattered, disconnected publications.

This vault originated from clinical practice at [Pangea Biomedics](https://pangeabiomedics.com) and now serves the broader ibogaine research community. Accuracy is critical: miscategorised cardiac safety evidence can impact patient safety.

## Who is this for?

- **Researchers** investigating ibogaine pharmacology, safety, or clinical outcomes
- **Clinicians** reviewing the evidence base for ibogaine-assisted treatment
- **Collaborators** contributing to systematic reviews, meta-analyses, or fatality documentation
- **Students and journalists** seeking a navigable entry point into a fragmented literature

This is a structured evidence map, not medical advice. It does not make treatment recommendations. It synthesises and organises published evidence so that researchers and clinicians can find what they need efficiently. The vault is not a substitute for reading primary sources — it is a map to them.

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

## Structure

```
IbogaineVault/
├── 1957–2026/          # Papers organised by publication year
│   └── AuthorYear_Short_Title.md
├── Hubs/               # Category hubs + cross-cutting synthesis
├── MOCs/               # Researcher maps of content
├── Bases/              # Queryable databases (Obsidian Properties)
│   ├── All_Papers.base
│   ├── Cardiac_Safety.base
│   ├── Dosing_Protocols.base
│   └── ...
├── Clinical_Guidelines/ # Treatment guidelines and protocols
├── Primary_Sources/     # Interviews, transcripts, oral history
├── Industry_Documents/  # Organisational reports and analyses
├── Other/              # Experience reports, journalism, legal
├── _meta/              # Schema, taxonomy, architecture docs
│   ├── schema_registry.yml      # Single source of truth for all schemas
│   ├── Tag_Taxonomy.md          # 62 canonical tags
│   ├── VAULT_ARCHITECTURE.md    # Three-layer navigation design
│   ├── VAULT_PRINCIPLES.md      # Design philosophy and clinical principles
│   └── README.md                # _meta/ directory guide
├── HOME.md             # Dashboard and entry point
├── CONTRIBUTING.md     # How to add papers
├── CHANGELOG.md        # Version history
├── GETTING_STARTED.md  # Orientation guide
├── papers.json         # Machine-readable index (all papers, all metadata)
├── papers.csv          # Flat export (core fields for tabular queries)
├── validate_vault.py   # Integrity validator (YAML, wikilinks, DOIs)
├── generate_index.py   # Regenerates papers.json + papers.csv
└── AGENTS.md           # Instructions for AI coding agents
```

## Paper format

Every paper includes structured YAML frontmatter with clinical metadata:

```yaml
title: "Paper title"
authors: ["Author1", "Author2"]
year: 2024
doi: "10.xxxx/xxxxx"
category: RED          # Primary classification
secondary_categories: [GREEN, ORANGE]
tags: [topic/cardiac, topic/qtc, mechanism/herg-blockade]
evidence_level: rct    # rct | cohort | case-series | case-report | ...
sample_size: 30
qtc_data: true
herg_data: false
mortality_count: 0
contraindications: ["pre-existing cardiac conditions", "..."]
```

This metadata enables systematic queries: "Show all RED papers with hERG data published after 2015" or "List contraindications across all clinical trials with sample size > 20." The full schema is defined in `_meta/schema_registry.yml`.

## Navigation layers

The vault uses three complementary navigation layers:

- **Bases** — Queryable databases for systematic filtering (e.g., all papers with QTc data, all dosing protocols)
- **Hubs** — Curated category entry points with narrative synthesis and cross-paper analysis
- **MOCs** (Maps of Content) — Researcher-centred navigation following individual contributors across categories

## Using this vault


The markdown files are readable in any text editor or GitHub's web interface. For the full interactive experience, the vault is designed for [Obsidian](https://obsidian.md) (v1.4+), which renders wikilinks, YAML metadata, and queryable bases as a navigable research environment.

**In Obsidian:**
1. Clone this repository
2. Open the folder as an Obsidian vault
3. Start from [HOME.md](HOME.md) — bases use native Properties (no plugins needed)

**On GitHub:** Browse the repository directly. All markdown renders natively. Wikilinks appear as plain text but the content is fully readable.

## Citation

If you use the IbogaineVault in your research, please cite:

> Kagalovsky, P. (2026). *IbogaineVault: A Structured Evidence Map for Ibogaine Science* — approximately 290 publications and clinical documents (1957–2026) with standardised mortality and safety metadata (Kagalovsky, in preparation). GitHub. https://github.com/GforVendetta/IbogaineVault

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding papers, the YAML schema, tag taxonomy, and quality standards.

## Copyright and Licence

This vault contains **analytical summaries** of published research, not the original publications. Source PDFs are not included. Open access papers are summarised under their respective CC licences; non-OA papers from major publishers (Elsevier, Wiley, Springer Nature, Taylor & Francis, and others) have been converted to original analytical works — structured critical analyses written in the vault curator's own voice, with reconstructed data tables and cross-reference annotations. These are transformative scholarly works, not reproductions.

All original vault content (metadata schemas, cross-references, hub syntheses, analytical commentary) is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Individual papers retain their original copyright and are referenced via DOI. See [COPYRIGHT.md](COPYRIGHT.md) for full details and [LICENSE](LICENSE) for the vault licence.

## Acknowledgements

Built in collaboration with Clare Wilkins (Clinical Director, Pangea Biomedics — 800+ ibogaine treatment sessions) and Sarita Wilkins (Therapeutic Integration, Pangea Biomedics).
