---
title: "Distribution Architecture — Working Vault & Tier 1"
tags:
  - meta/hub
document_type: administrative
created: 2026-02-26
---

# Distribution Architecture

> How the IbogaineVault exists as two separate directories, how they relate to each other, and how changes flow from development to public distribution.

---

## The Two-Directory Model

The IbogaineVault uses a **physical air gap** between the working clinical instrument and the public GitHub repository. There is no shared `.git/` — they are two completely independent directories connected only by an export script.

### Working Vault

**Path:** `/Users/aretesofia/IbogaineVault/`

This is the primary clinical instrument. It contains everything: research papers, clinical protocols, Pangea operational documents, internal tooling, development roadmaps, prompt libraries, Obsidian configuration, Copilot indices, and all metadata.

Key characteristics:
- **No `.git/` directory** — not a git repository. Changes are tracked via `_meta/WORKLOG.md` and `_meta/CHANGELOG.md`
- **Obsidian is the interface** — this is where Copilot queries, graph view, Bases, and all clinical workflows operate
- **Contains Tier 2 content** — Pangea-specific protocols, internal meeting transcripts, operational documents, collaborator research, development infrastructure
- **Single source of truth** for all vault content. Every paper, hub, MOC, and base file originates here

### Tier 1 Distribution (GitHub)

**Path:** `/Users/aretesofia/IbogaineVault-Tier1/`
**Remote:** `https://github.com/GforVendetta/IbogaineVault.git`

This is a filtered mirror of the working vault — everything a researcher, collaborator, or the public needs, with nothing internal. The repo name is `IbogaineVault` (not `IbogaineVault-Tier1`) because the public identity shouldn't expose internal architecture.

Key characteristics:
- **Is a git repository** — has `.git/`, tracks changes via commits, pushes to GitHub
- **Contains only Tier 1 content** — no Pangea operations, no internal tooling, no development infrastructure, no PDFs, no Obsidian configuration
- **Never edited directly** (with three exceptions — see Override Files below). Content flows one way: working vault → sync script → Tier 1

---

## How Content Flows

```
Working Vault                    Sync Script                     Tier 1 Repo
/IbogaineVault/     ──────►    sync_tier1.sh    ──────►    /IbogaineVault-Tier1/
                                                                    │
  (edit here)              (rsync + exclusions)                     │
                                                               git add .
                                                               git commit
                                                               git push
                                                                    │
                                                                    ▼
                                                            GitHub (public)
```

### The Sync Script

**Location:** `_meta/tools/sync_tier1.sh`

The script uses `rsync` with `--delete` to create an idempotent mirror. Running it repeatedly always produces the same result — it copies new/changed files from the working vault and deletes files from Tier 1 that no longer exist in the working vault (unless excluded).

**To run:**
```bash
bash /Users/aretesofia/IbogaineVault/_meta/tools/sync_tier1.sh
```

The script:
1. Runs rsync with all exclusion rules
2. Performs a YAML frontmatter safety sweep — checks every `.md` file in Tier 1 for `scope: pangea` between YAML `---` delimiters (not in body text)
3. Verifies excluded directories/files are absent
4. Confirms all governance files are present
5. Reports pass/fail

### After Syncing

```bash
cd /Users/aretesofia/IbogaineVault-Tier1
git add .
git commit -m "descriptive message"
git push
```

---

## What Gets Excluded

The sync script excludes three categories of content:

### Directories (entire trees excluded)

| Directory | Reason |
|-----------|--------|
| `Pangea_Ops/` | Internal clinical operations — Tier 2 |
| `Collaborator_Research/` | Private research shared by collaborators |
| `Cowork_Outputs/` | Automated tool outputs |
| `.obsidian/` | Obsidian configuration (themes, plugins, workspace state) |
| `.local/` | Local Obsidian data |
| `.trash/` | Obsidian trash |
| `_builds/` | Build artefacts (tag extractions, tool outputs) |
| `_archive/` | Archived vault content |
| `copilot/` | Copilot Plus index files |
| `_meta/archive/` | Worklog archives and historical meta files |
| `_meta/prompts/` | Claude prompt library |
| `_meta/tools/` | Development scripts (including sync_tier1.sh itself) |
| `.copilot-index/` | Copilot search index |
| `.smart-env/` | Smart Connections plugin data |

### Individual files excluded

| File | Reason |
|------|--------|
| `CLAUDE.md` | Claude Desktop project instructions |
| `_meta/WORKLOG.md` | Session-by-session development log |
| `_meta/ROADMAP.md` | Internal development roadmap |
| `_meta/NLQ_ARCHITECTURE.md` | Pangea clinical copilot architecture |
| `_meta/STRATEGIC_PLANNING.md` | Internal distribution strategy and academic planning |
| `_meta/transcript_manifest.md` | Internal transcript conversion workflow |

### File patterns excluded

| Pattern | Reason |
|---------|--------|
| `*.pdf` | Source PDFs (copyright — vault contains markdown conversions only) |
| `*.zip`, `*.tar.gz` | Archive bundles |
| `*.plugin` | Obsidian plugin files |
| `.DS_Store` | macOS filesystem metadata |

---

## Override Files

Three files in `_meta/` have **different content** in the working vault vs Tier 1. These are the only files that break the "one source of truth" pattern, and they do so for good reason: the internal versions reference Pangea operations, development tooling, and operational checklists that don't belong in a public repository.

| File | Working Vault Version | Tier 1 Version |
|------|----------------------|----------------|
| `_meta/README.md` | References WORKLOG, archive/, tools/, prompts/, full internal file listing | Contributor-focused directory guide, schema architecture |
| `_meta/VAULT_ARCHITECTURE.md` | Shows Tier 2 directories, local PDF paths, old git workflow, Pangea references | Public structural reference — navigation layers, folder tree, category system, YAML |
| `_meta/VAULT_PRINCIPLES.md` | 8 principles including prompt lifecycle, ROADMAP migration, session-end checklist | 7 principles — replaces internal ones with "Accuracy Over Speed", "Categories Are Co-Equal" |

### How overrides work mechanically

The sync script **excludes** these three filenames. This means:
- rsync will **not copy** the working vault version to Tier 1 (so the Tier 1 version is preserved)
- rsync's `--delete` will **not remove** the Tier 1 version (excluded files are invisible to rsync in both directions)
- The Tier 1 versions were written directly into `/Users/aretesofia/IbogaineVault-Tier1/_meta/` and are maintained there independently

**Consequence:** if you edit `_meta/VAULT_ARCHITECTURE.md` in the working vault, the Tier 1 version will NOT update. You must edit the Tier 1 version separately if the change is relevant to both audiences. This is intentional — the two versions serve different readers with different needs.

### The root README.md is NOT an override

The root `README.md` is a normal synced file. It uses markdown relative links (not wikilinks) because it's primarily rendered by GitHub. Edit it in the working vault, sync, and it propagates. It's somewhat redundant inside Obsidian (where `HOME.md` serves as the dashboard), but keeping one source of truth is worth the vestigial copy.

---

## Synced vs Override: Decision Framework

When adding a new `_meta/` file, ask:

1. **Does the internal version contain Pangea-specific, operational, or development-only content?** → Override file (exclude from sync, maintain Tier 1 version independently)
2. **Is the content identical for both audiences?** → Synced file (edit in working vault, sync propagates)
3. **Is the content entirely internal with no public equivalent?** → Exclude from sync entirely (no Tier 1 version exists)

Current classification:

| File | Type |
|------|------|
| `schema_registry.yml` | Synced — identical for all audiences |
| `conversion_manifest.md` | Synced — useful for contributors |
| `Tag_Taxonomy.md` | Synced — reference document |
| `README.md` | Override — different audiences |
| `VAULT_ARCHITECTURE.md` | Override — internal refs removed |
| `VAULT_PRINCIPLES.md` | Override — internal principles replaced |
| `ROADMAP.md` | Excluded — entirely internal |
| `NLQ_ARCHITECTURE.md` | Excluded — entirely internal |
| `transcript_manifest.md` | Excluded — entirely internal |
| `WORKLOG.md` | Excluded — entirely internal |
| `DISTRIBUTION_ARCHITECTURE.md` | Excluded — internal operational reference |
| `STRATEGIC_PLANNING.md` | Excluded — internal strategy and academic planning |

---

## Safety Mechanisms

### scope: pangea sweep

The sync script includes a YAML frontmatter-aware safety sweep. It checks every `.md` file in Tier 1 for `scope: pangea` appearing between the YAML `---` delimiters (not in body text that merely documents the field). If found, the sync fails with a clear error listing the offending files.

This catches the case where a Tier 2 paper (e.g., a Pangea-specific clinical protocol) accidentally makes it through the exclusion rules.

### Verification checks

After syncing, the script verifies:
- All excluded directories are absent from Tier 1
- All excluded files are absent
- No PDFs leaked through
- All governance files (README, LICENSE, CITATION.cff, CONTRIBUTING, CHANGELOG, GETTING_STARTED, HOME) are present

### Clean git history

The Tier 1 repo was initialised with a force-push of a single root commit, erasing previous history that contained internal tooling. The public git history begins clean.

---

## Common Operations

### Adding a new paper
1. Convert in working vault (follow `conversion_manifest.md`)
2. Run sync script
3. `cd /Users/aretesofia/IbogaineVault-Tier1 && git add . && git commit -m "Add Author2026_Topic" && git push`

### Updating a hub
1. Edit in working vault
2. Run sync script (hub propagates automatically)
3. Commit and push from Tier 1

### Updating an override file
1. Edit the Tier 1 version directly in `/Users/aretesofia/IbogaineVault-Tier1/_meta/`
2. Do NOT run sync (it won't touch override files, but no need to risk confusion)
3. Commit and push from Tier 1
4. If the working vault version also needs updating, edit it separately

### Adding a new exclusion
1. Add `--exclude='pattern'` to the rsync command in `sync_tier1.sh`
2. Add a verification check in the script's verification section
3. Manually remove any already-present files from Tier 1 (rsync `--exclude` prevents future transfer but doesn't delete existing files)
4. Run sync to confirm clean pass

---

*Created: 2026-02-26. This document lives in the working vault only — explicitly excluded from Tier 1 sync.*
