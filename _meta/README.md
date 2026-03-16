# _meta/ — Vault Infrastructure

Administrative and documentation files for the IbogaVault. Not clinical content.

## Active Files

| File                                         | Purpose                                                                                                               |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `ROADMAP.md`                                 | Development plan and active priorities                                                                                |
| `WORKLOG.md`                                 | Session-by-session progress log (template at top; newest first)                                                       |
| `conversion_manifest.md`                     | **Paper conversion reference** — YAML schema, tags, template                                                          |
| `transcript_manifest.md`                     | **Transcript conversion reference** — meeting/interview YAML schema, scope field, retrofit guide                      |
| `Tag_Taxonomy.md`                            | Canonical 62-tag taxonomy reference                                                                                   |
| `VAULT_ARCHITECTURE.md`                      | Structural overview of vault organisation                                                                             |
| `NLQ_ARCHITECTURE.md`                        | Natural language query system design                                                                                  |
| `schema_registry.yml`                        | **Single source of truth** — all schemas, enums, field definitions (derivatives derive from here)                     |
| `VAULT_PRINCIPLES.md`                        | 8 architectural axioms to prevent drift — prompt sweeps, single-source counts, archival provenance                    |
| `archive/reference_gap_analysis_COMPLETE.md` | Citation-mined gaps — 52 papers identified from 14 vault reviews (50 filled, 2 remaining). Archived after completion. |

## Tools

| File | Purpose |
|------|---------|
| `tools/validate_yaml.py` | YAML validation audit — checks all papers against `schema_registry.yml`. Run: `python3 validate_yaml.py [--summary \| --json \| --file path.md]` |

## Prompts

`prompts/` contains session prompts for Claude. Two types:

- **Templates** (prefixed `_template_`): Reusable — copy into new chats and fill placeholders. E.g., `_template_conversion_session.md`.
- **Date-stamped prompts**: Single-use session instructions for specific tasks. E.g., `2026-02-23_systemic_coherence_audit.md`.

## Other Vault Locations

| Directory | Purpose |
|-----------|---------|
| `Collaborator_Research/` | Research syntheses from collaborators (Sam Fraser Oliver et al.) — not vault papers, not _meta infrastructure |
| `Cowork_Outputs/` | Clinical work products from Cowork plugin sessions |
| `_builds/pangea-ibovault/` | Cowork plugin v2.3.0 (9 skills + 11 commands) |
| `_archive/_builds_v1/` | Archived v1.x plugin (`pangea-ibogavault` v1.3.0) — superseded by `pangea-ibovault/` v2.3.0 |
| `_archive/_skills_legacy/` | Archived training docs — superseded by `pangea-ibovault/` skills (v2.0.0) |
| `copilot/` | Obsidian Copilot Plus configuration |

## Archive

`archive/` contains completed audit reports, damage remediation records, historical logs, constellation graph exports, and archived enhancement proposals. Preserved for institutional memory.

## For Claude

- **Adding papers?** Read `conversion_manifest.md` + the PDF. That's the workflow.
- **Converting transcripts?** Read `transcript_manifest.md`. Different schema from papers — uses `participants`, `scope`, `key_decisions`.
- **Logging work?** Append to `WORKLOG.md` using the standard entry template at the top.
- **Checking priorities?** `ROADMAP.md` — scan in 60 seconds.
