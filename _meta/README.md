# _meta/ — Vault Infrastructure

Schema definitions, taxonomy, and architectural documentation for the IbogaineVault.

## Files

| File | Purpose |
|------|---------|
| `schema_registry.yml` | **Single source of truth** — all YAML schemas, enums, field definitions, and validation rules. Every paper's frontmatter conforms to this schema. |
| `Tag_Taxonomy.md` | Canonical 62-tag taxonomy. All tags used in paper frontmatter are drawn from this controlled vocabulary. |
| `VAULT_ARCHITECTURE.md` | Three-layer navigation design: Bases (queryable databases), Hubs (curated entry points), MOCs (researcher maps of content). |
| `VAULT_PRINCIPLES.md` | Design philosophy — 8 architectural axioms governing vault organisation, clinical accuracy standards, and co-equal category treatment. |
| `README.md` | This file. |

## For Programmatic Users

The schema in `schema_registry.yml` defines every YAML field, its type, permitted values, and which fields are required vs optional. If you are writing scripts against `papers.json` or `papers.csv`, the schema registry is the authoritative reference for field semantics.

## For Contributors

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full paper conversion workflow, including YAML schema requirements, tag selection, and quality standards.
