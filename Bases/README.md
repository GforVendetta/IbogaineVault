---
title: "Bases — Queryable Databases"
aliases: ["Bases", "Queryable Databases"]
---

# Bases — Queryable Databases

Bases are structured query views that filter and display papers by clinical function. Each `.base` file defines a filter (which papers to include), a set of columns (which metadata fields to show), and a table layout. They are the vault's equivalent of saved database queries — pre-built lenses for common research questions.

## How they work

Each `.base` file uses Obsidian's native [Properties](https://help.obsidian.md/Editing+and+formatting/Properties) database format (introduced in v1.4): a YAML-like syntax that specifies filters against YAML frontmatter fields, which properties to display as columns, and how to sort and size the resulting table. When opened in Obsidian (v1.4+), they render as interactive, sortable, filterable tables drawn from every paper in the vault — no plugins required.

The files are small (20–25 lines each) and human-readable. Even without Obsidian, they document exactly which queries the vault is designed to answer.

## Available bases

| Base | Filter | What it answers |
|------|--------|-----------------|
| `All_Papers.base` | All papers with a category | Master index — every paper in the vault, sortable by year, category, significance |
| `Cardiac_Safety.base` | `category == "RED"` | Which papers contain cardiac safety evidence? QTc, hERG, fatalities, adverse events |
| `Dosing_Protocols.base` | `category == "GREEN"` | Which papers describe clinical protocols, screening procedures, dosing guidelines? |
| `Analogue_Safety.base` | Tags: `topic/analogues` or `topic/18-mc` | Safety and efficacy data for ibogaine analogues (noribogaine, 18-MC, tabernanthalog) |
| `Contraindications.base` | Tags: `topic/adverse-event`, `topic/toxicity`, or `topic/cardiac` | Which papers document adverse events, toxicity, or cardiac risks? |
| `Researchers.base` | All papers with authors | Papers organised by author — useful for tracing individual research programmes (two views: by researcher, by year) |
| `Veterans_TBI.base` | Tags: `topic/veterans` or `topic/tbi` | Evidence base for ibogaine in traumatic brain injury and veteran populations (MISTIC and related) |

## Requirements

Bases render as interactive tables in [Obsidian](https://obsidian.md) v1.4 or later — they use the native Properties system and do not require any plugins. Without Obsidian, the `.base` files are still readable as plain text — they just won't render interactively.

**Not using Obsidian?** The vault provides two machine-readable alternatives at the repository root:

- **`papers.json`** — Structured JSON with full metadata for every paper (title, authors, year, DOI, category, tags, evidence level, boolean flags, clinical significance, sample size, mortality count). Suitable for programmatic queries, scripts, or import into any data tool.
- **`papers.csv`** — Flat table version of the same data for spreadsheet users. Opens directly in Excel, Google Sheets, or any CSV reader.

Both files are regenerated automatically on every sync and reflect the current state of the vault.

## Schema dependency

All base queries filter on YAML frontmatter fields defined in `_meta/schema_registry.yml` — the single source of truth for the vault's metadata schema. If you are building custom queries or extending a base, consult the schema registry for valid field names, types, and enum values.

## The `source_pdf` field

Every paper's YAML frontmatter includes a `source_pdf` field (e.g., `source_pdf: "2024/Cherian2024_Ibogaine_Primer_Clinicians.pdf"`). This is a reference to the original publication filename — the source PDFs themselves are **not included** in this repository. Git is not designed for large binary files, and distributing copyrighted PDFs would violate publisher agreements.

To access source papers: use the `doi` field in each paper's YAML to retrieve from the publisher, or see the shared Google Drive folder referenced in [CONTRIBUTING.md](../CONTRIBUTING.md).
