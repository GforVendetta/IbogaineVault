---
title: "Vault Architecture Reference"
tags:
  - meta
aliases: ["Architecture", "Technical Reference"]
---

# Vault Architecture Reference

> Technical reference for the IbogaineVault's structure, navigation systems, and metadata schema. For the design philosophy underpinning these choices, see [[_meta/VAULT_PRINCIPLES|Vault Principles]]. For getting started as a researcher, see [[GETTING_STARTED]].

---

## The Six-Category System

Every paper in the vault is assigned a primary category based on its principal contribution to ibogaine science:

| Category | Colour | Domain | Typical Content |
|----------|--------|--------|-----------------|
| **RED** | Red | Cardiac safety, fatalities, adverse events | QTc studies, hERG data, case fatality analyses, toxicology |
| **GREEN** | Green | Clinical protocols, guidelines, screening | GITA guidelines, dosing protocols, pre-treatment screening |
| **ORANGE** | Orange | Pharmacology and mechanisms | Receptor binding, GDNF, noribogaine metabolism, 18-MC |
| **BLUE** | Blue | Clinical outcomes and efficacy | Trials, observational studies, veterans/TBI outcomes |
| **PURPLE** | Purple | Subjective experience, phenomenology | IES scale, qualitative accounts, therapeutic process |
| **WHITE** | Grey | Historical, traditional use, policy | Bwiti practice, Lotsof discovery, scheduling, regulation |

### Category Assignment Logic

A paper's primary category reflects its *principal contribution*, not every topic it mentions. When a paper spans multiple domains:

1. **What question does the paper primarily answer?** A paper measuring QTc intervals during ibogaine treatment is RED (cardiac safety), even if it also reports efficacy outcomes.
2. **Where would a clinician look for it?** If someone searching for cardiac safety evidence would miss this paper under a different category, it belongs in RED.
3. **Use `secondary_categories` for secondary contributions.** A mechanisms paper that incidentally reports a treatment-associated death should carry `secondary_categories: [RED]` so it surfaces in cardiac safety queries.
4. **When in doubt, classify towards safety.** See [[_meta/VAULT_PRINCIPLES#4. Conservative Classification|Principle 4: Conservative Classification]].

**Non-RED boundary examples:**

- **BLUE vs GREEN:** A study evaluating a screening protocol's effectiveness at predicting outcomes is GREEN (its contribution is the protocol validation), even though it reports efficacy data. An efficacy trial that incidentally describes its screening process is BLUE.
- **ORANGE vs BLUE:** A paper investigating receptor binding profiles that also reports behavioural outcomes in animal models is ORANGE (mechanisms are its principal contribution). A clinical trial that discusses pharmacological mechanisms to explain its results is BLUE with `secondary_categories: [ORANGE]`.
- **PURPLE vs BLUE:** A qualitative interview study analysing visionary content is PURPLE. A mixed-methods study reporting both psychometric outcomes and thematic experience analysis is BLUE if the outcomes data is primary, PURPLE if the experiential analysis is primary.
- **WHITE boundaries:** A paper becomes WHITE when its principal value is historical or policy context rather than active evidence. A 1960s case series still providing the only data on a particular dosing approach remains in its primary evidence category (BLUE or RED); the same paper's historical significance does not override its evidentiary function.

---

## YAML Metadata Schema

Every paper carries structured YAML frontmatter that enables systematic queries across the vault. The authoritative field definitions live in `schema_registry.yml`; this section provides an overview.

### Key Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `category` | Primary classification (RED/GREEN/ORANGE/BLUE/PURPLE/WHITE) | `RED` |
| `secondary_categories` | Additional categories when a paper spans domains | `[RED, ORANGE]` |
| `evidence_level` | Methodological rigour of the study | `rct`, `cohort`, `case-report`, `systematic-review` |
| `tags` | Topical and methodological tags from the 62-tag taxonomy | `[topic/cardiac, mechanism/herg-blockade]` |
| `clinical_significance` | Editorial assessment of clinical impact | `low`, `moderate`, `high`, `landmark` |
| `qtc_data` | Whether the paper reports QTc interval data | `true` / `false` |
| `herg_data` | Whether the paper reports hERG channel findings | `true` / `false` |
| `electrolyte_data` | Whether the paper reports electrolyte data | `true` / `false` |
| `contraindications` | Contraindications identified in the paper | `["methadone", "QTc > 450ms"]` |
| `dosing_range` | Dosing information (required for RED and GREEN papers) | `"12–20 mg/kg oral"` |

### Boolean Safety Flags

The three boolean fields (`qtc_data`, `herg_data`, `electrolyte_data`) enable rapid filtering for cardiac safety evidence. A query for all papers with `qtc_data: true` returns every paper in the vault that reports QTc interval measurements, regardless of its primary category.

### Evidence Levels

The `evidence_level` field uses a controlled vocabulary defined in the schema registry. Valid values span from `rct` (randomised controlled trial) through `case-report` to `journalism` and `primary-source`. See [Schema Registry](_meta/schema_registry.yml) for the full list of valid values.

---

## Navigation Architecture

The vault uses a three-layer navigation system. Each layer serves a different mode of inquiry.

### Bases — Queryable Databases

Location: `Bases/`

Bases are Obsidian's structured database views, filtering papers by YAML metadata. They answer *specific clinical questions* — "show me all RED papers with QTc data" or "list GREEN papers by dosing range."

| Base | Filter Logic | Purpose |
|------|--------------|---------|
| `Cardiac_Safety.base` | `category == "RED"` | Life-safety evidence lookup |
| `All_Papers.base` | `category != null` | Master vault database |
| `Researchers.base` | `authors != null` | Find papers by researcher name |
| `Veterans_TBI.base` | `tags` includes veterans/tbi | MISTIC protocol evidence |
| `Analogue_Safety.base` | `tags` includes analogues/18-mc | Safer analogue research |
| `Dosing_Protocols.base` | `category == "GREEN"` | Clinical protocol comparison |
| `Contraindications.base` | `tags` includes adverse-event/toxicity/cardiac | Exclusion criteria lookup |

Bases require the **Obsidian Bases** community plugin. Without the plugin, the `.base` files are still human-readable YAML filter definitions, and the same queries are achievable through Dataview queries against the YAML frontmatter.

### Hubs — Curated Domain Entry Points

Location: `Hubs/`

Hubs are long-form, editorially curated documents that synthesise the evidence within a domain. Each of the six categories has a primary hub, plus cross-cutting hubs for specific research themes.

| Hub | Domain |
|-----|--------|
| [[RED_Cardiac_Safety_Hub]] | Cardiac safety, fatalities, hERG, magnesium co-administration |
| [[GREEN_Clinical_Protocols_Hub]] | GITA guidelines, screening protocols, dosing |
| [[ORANGE_Mechanisms_Hub]] | Receptor pharmacology, GDNF, noribogaine, 18-MC |
| [[BLUE_Outcomes_Hub]] | Clinical trials, veterans/TBI outcomes, effect sizes |
| [[PURPLE_Phenomenology_Hub]] | Subjective experience, the Ibogaine Experience Scale |
| [[WHITE_Historical_Hub]] | Bwiti tradition, Lotsof discovery narrative, drug policy |
| [[Hub_PK-PD_Synthesis]] | Pharmacokinetics, noribogaine, CYP2D6, dose-safety relationships |
| [[Key_Researchers_Hub]] | Cross-category profiles of major contributors to ibogaine science |

Hubs differ from Bases in that they provide *narrative context* — explaining why papers matter relative to each other, identifying patterns across the literature, and highlighting gaps. A Base answers "what exists"; a Hub answers "what it means."

### MOCs — Researcher-Centred Navigation

Location: `MOCs/`

Maps of Content (MOCs) organise the vault around individual researchers whose work spans multiple categories. A researcher MOC collects their papers, identifies their intellectual trajectory, and cross-references their contributions.

| MOC | Focus |
|-----|-------|
| [[Kenneth_Alper_MOC\|Kenneth Alper]] | Safety science, hERG pharmacology, fatality documentation |
| [[Clare_Wilkins_MOC\|Clare Wilkins]] | Clinical practice, 800+ ibogaine treatment sessions |
| [[Howard_Lotsof_MOC\|Howard Lotsof]] | Discovery, early development, patent history, advocacy |

### How the Three Layers Complement Each Other

A researcher investigating cardiac safety might follow this path: start at the **Cardiac Safety Base** to see all RED papers in a sortable table → read the **RED Cardiac Safety Hub** for narrative synthesis and the paradigm shift from risk management to risk elimination → visit **Kenneth Alper's MOC** to trace the evolution of fatality documentation from his earliest case series to the comprehensive reviews.

---

## Graph View Colour Coding

Obsidian's graph view colours nodes by category using YAML property queries:

- `["category":RED]` → Red (safety)
- `["category":GREEN]` → Green (protocols)
- `["category":ORANGE]` → Orange (mechanisms)
- `["category":BLUE]` → Blue (outcomes)
- `["category":PURPLE]` → Purple (phenomenology)
- `["category":WHITE]` → Grey (historical)

---

## Wikilink Conventions

The vault uses Obsidian-style `[[wikilinks]]` to create a navigable research graph. Conventions:

- **Paper-to-paper links** connect studies that directly build on, contradict, or extend each other. The link should appear in the body text where the relationship is discussed, not in a standalone "Related Papers" section.
- **Paper-to-hub backlinks** ensure every paper is reachable from its domain hub. Papers include a backlink to their primary hub (e.g., `Categorised in [[RED_Cardiac_Safety_Hub]]`).
- **Hub cross-references** link between hubs when evidence in one domain has implications for another (e.g., the RED hub references GREEN protocol papers that address cardiac screening).
- **Display text** uses the pipe syntax for readability: `[[Alper2001_Ibogaine_Review|Alper 2001]]`.

---

## Folder Structure

```
IbogaineVault/
├── README.md                    # Repository overview
├── HOME.md                      # Dashboard and primary navigation
├── GETTING_STARTED.md           # Onboarding guide
├── CONTRIBUTING.md              # How to contribute
├── CHANGELOG.md                 # Version history and milestones
├── CITATION.cff                 # Academic citation metadata
├── LICENSE                      # Licence
│
├── 1957/ ... 2026/              # Papers organised by publication year
├── Bases/                       # Queryable databases (Obsidian Bases plugin)
├── Hubs/                        # Domain entry points by category
│   ├── RED_Cardiac_Safety_Hub.md
│   ├── GREEN_Clinical_Protocols_Hub.md
│   ├── ORANGE_Mechanisms_Hub.md
│   ├── BLUE_Outcomes_Hub.md
│   ├── PURPLE_Phenomenology_Hub.md
│   ├── WHITE_Historical_Hub.md
│   ├── Key_Researchers_Hub.md
│   └── Hub_PK-PD_Synthesis.md
├── MOCs/                        # Researcher-centred navigation
│   ├── Kenneth_Alper_MOC.md
│   ├── Clare_Wilkins_MOC.md
│   └── Howard_Lotsof_MOC.md
├── Clinical_Guidelines/         # Published guidelines (GITA, IACT, Aotearoa)
├── Primary_Sources/             # Interview transcripts, oral histories
├── Industry_Documents/          # Beond, ICEERS reports
├── Other/                       # Miscellaneous
│
└── _meta/                       # Administrative and reference documents
    ├── schema_registry.yml      # Single source of truth for all schemas
    ├── Tag_Taxonomy.md          # 62 canonical tags across 6 categories
    ├── VAULT_PRINCIPLES.md      # Design philosophy and quality principles
    ├── VAULT_ARCHITECTURE.md    # This file
    └── README.md                # _meta/ directory guide
```

---

## Distribution

This is the public research vault. The IbogaineVault also exists as an internal clinical workstation with additional operational content (team protocols, session transcripts, clinical work products) that is maintained separately and not included in this distribution. All research content — papers, hubs, MOCs, clinical guidelines, and metadata — is identical across both versions.

---

## Version Control

The vault is version-controlled with git. Every paper conversion, hub update, and metadata correction is recorded as a commit with a description and full diff, providing disaster recovery and a forensic audit trail. The repository is hosted on GitHub at `GforVendetta/IbogaineVault`.

For information about proposing corrections or contributing papers, see [[CONTRIBUTING]].

---

**See also:** [[GETTING_STARTED]] · [[HOME]] · [[_meta/VAULT_PRINCIPLES|Vault Principles]] · [[_meta/Tag_Taxonomy|Tag Taxonomy]]
