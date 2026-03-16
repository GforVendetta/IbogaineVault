---
title: "Quartz Web Publishing — Implementation Plan"
date: 2026-02-27
category: WHITE
tags:
  - meta/architecture
  - meta/planning
document_type: administrative
---

# Quartz Web Publishing — Implementation Plan

**Created:** 2026-02-27
**Status:** Phase 1 complete, Phase 2 pending
**Location:** Mac Studio only — `/Users/aretesofia/IbogaineVault-Quartz/`
**Quartz version:** v4.5.2

---

## Architecture Overview

### Device Topology

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MACBOOK PRO                                  │
│                                                                     │
│  IbogaineVault/          ◄──── Obsidian Sync ────►  (Mac Studio)   │
│  (working vault)                                                    │
│                                                                     │
│  IbogaineVault-Tier1/    ◄──── sync_tier1.sh (local)               │
│  (distribution copy)            NOT synced between machines         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         MAC STUDIO                                  │
│                                                                     │
│  IbogaineVault/          ◄──── Obsidian Sync ────►  (MacBook Pro)  │
│  (working vault)                                                    │
│                                                                     │
│  IbogaineVault-Tier1/    ◄──── git clone from GitHub                │
│  (cloned from repo)            NOT synced via Obsidian              │
│                                                                     │
│  IbogaineVault-Quartz/   ◄──── Mac Studio ONLY                     │
│  (Quartz site generator)                                            │
│    └── content/           ◄──── copy of Tier 1 content              │
│                                 (.git included from clone)          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow (Current)

```
Working Vault (either machine)
    │
    ▼  sync_tier1.sh
IbogaineVault-Tier1/ (Mac Studio)
    │
    ▼  git push
GitHub repo (GforVendetta/IbogaineVault)
    │
    ▼  manual copy / future automation
IbogaineVault-Quartz/content/
    │
    ▼  npx quartz build
public/ → localhost:8888 (dev) or GitHub Pages (production)
```

### Key Decision: Copy over Symlink

Symlink from `content/` → `IbogaineVault-Tier1/` was attempted but abandoned.
The Quartz dev server's `serve-handler` library had issues following symlinks
(EISDIR errors). Content is now a direct copy. This means `sync_tier1.sh`
needs a post-sync step to update `IbogaineVault-Quartz/content/` — see
Phase 2 automation below.

---

## Sequencing Philosophy

**Set up Quartz now. Don't wait for perfect metadata.**

Think of it like fluorescence microscopy: you don't prepare all your slides
perfectly then turn on the fluorescent labels. You apply the stain first,
because the staining is what reveals the problems you can't see with the
naked eye.

Quartz running locally with `npx quartz build --serve` becomes a **diagnostic
instrument** for metadata cleanup:

- Broken wikilinks → visible dead links (greyed out, no popover preview)
- Malformed YAML → build errors with file names and line numbers
- Missing `description`/`key_findings` → blank previews in link cards
- Tag inconsistencies → separate tag pages for `topic/cardiac` vs `topic/Cardiac`
- Orphaned papers → visible in graph view as disconnected nodes

The `sync_tier1.sh` → Tier 1 → Quartz pipeline means every fix flows through
automatically. Fix a paper's YAML, run sync, refresh browser, see the fix.
Tight feedback loop rather than two sequential projects.

---

## Phase Breakdown

### Phase 1: Setup ✅ COMPLETE (2026-02-26/27)

**What was done:**
- Cloned Quartz v4.5.2 to `/Users/aretesofia/IbogaineVault-Quartz/`
- Installed Node v22.22.0 via nvm (Mac Studio)
- `npm i` (486 packages)
- `npx quartz create` — empty content, shortest-path link resolution
- Cloned GitHub repo to `IbogaineVault-Tier1/` on Mac Studio
- Copied Tier 1 content into `content/`
- Created `content/index.md` from `HOME.md`

**Issues resolved:**
- `npm audit fix --force` downgraded `serve-handler` from v6 to v1.0.0 → EISDIR crash. Fixed by reinstalling v6.1.6.
- `HOME.md` alias `"Index"` caused Quartz to generate `index.html` as a redirect stub → infinite loop. Fixed by removing `"Index"` from aliases and `cssclass: dashboard` (not a Quartz property).
- Symlink approach abandoned due to serve-handler incompatibility.

**Result:** 310 markdown files parsed, 1530 files emitted, site live at localhost:8888.

---

### Phase 2: Light Configuration (~1–2 hours)

#### 2a. HOME.md → index.md Automation

Currently manual. Add to `sync_tier1.sh` (or a post-sync hook):

```bash
cp "$DEST/HOME.md" "$DEST/index.md"
# Strip "Index" alias and cssclass from the copy
sed -i '' '/^aliases:/,/^[^-]/{/- "Index"/d;}' "$DEST/index.md"
sed -i '' '/^cssclass:/d' "$DEST/index.md"
```

Or create a dedicated `sync_quartz.sh` that:
1. `rsync` from `IbogaineVault-Tier1/` to `IbogaineVault-Quartz/content/`
2. Copies and patches `index.md`
3. Optionally triggers `npx quartz build`

#### 2b. Explorer Custom Sort

Priority folders first, then year folders (numeric sort), then files.
~15 lines in `quartz.layout.ts`:

```typescript
Component.Explorer({
  sortFn: (a, b) => {
    const priority = ['Hubs', 'Bases', 'MOCs', 'Clinical_Guidelines'];
    const aIdx = priority.indexOf(a.displayName);
    const bIdx = priority.indexOf(b.displayName);
    if (aIdx !== -1 && bIdx !== -1) return aIdx - bIdx;
    if (aIdx !== -1) return -1;
    if (bIdx !== -1) return 1;
    if (a.isFolder && !b.isFolder) return -1;
    if (!a.isFolder && b.isFolder) return 1;
    return a.displayName.localeCompare(b.displayName, undefined, {
      numeric: true, sensitivity: "base"
    });
  }
})
```

#### 2c. KeyFindingsToDescription Transformer Plugin

The Description plugin (`quartz/plugins/transformers/description.ts`) checks
`frontmatter.description` first. If absent, it auto-generates from content.
Our papers have `key_findings` instead. Rather than duplicating data in the
YAML, create a transformer that runs *before* `Plugin.Description()`:

```typescript
// quartz/plugins/transformers/keyFindings.ts
import { QuartzTransformerPlugin } from "../types"

export const KeyFindingsToDescription: QuartzTransformerPlugin = () => ({
  name: "KeyFindingsToDescription",
  markdownPlugins() {
    return [
      () => (_tree, file) => {
        const fm = file.data.frontmatter
        if (fm && !fm.description && fm.key_findings) {
          fm.description = fm.key_findings
        }
      },
    ]
  },
})
```

Register in `quartz/plugins/transformers/index.ts`, add to `quartz.config.ts`
before `Plugin.Description()`. Working vault YAML stays untouched. ~15 lines.

**Why this approach over alternatives:**
- Modifying Description plugin directly → merge conflicts on Quartz updates
- Adding `description` to every YAML block → data duplication, drift risk
- Custom transformer → clean separation, survives updates

#### 2d. Category Colour CSS (Page Elements Only)

CSS for page titles, sidebar entries, and tag labels. NOT the graph
(that's Phase 4). About 12 lines in `quartz/styles/custom.scss`:

```scss
// Category colour accents for page elements
[data-category="RED"]    { --category-color: #e74c3c; }
[data-category="GREEN"]  { --category-color: #2ecc71; }
[data-category="ORANGE"] { --category-color: #f39c12; }
[data-category="BLUE"]   { --category-color: #3498db; }
[data-category="PURPLE"] { --category-color: #9b59b6; }
[data-category="WHITE"]  { --category-color: #95a5a6; }
```

Requires a small component modification to emit `data-category` attributes
from frontmatter onto page elements. Light work but depends on understanding
which Quartz component renders the page wrapper.

#### 2e. quartz.config.ts Basic Settings

```typescript
configuration: {
  pageTitle: "IbogaineVault",
  enableSPA: true,
  enablePopovers: true,
  locale: "en-GB",
  baseUrl: "gforvendetta.github.io/IbogaineVault",
  ignorePatterns: ["_meta", ".git", "*.pdf", "Pangea_Ops"],
  // ...
}
```

Key: `ignorePatterns` must exclude `_meta/` (internal), `.git/` (from Tier 1
clone), PDFs, and `Pangea_Ops/` (Tier 2 only, should never be in Tier 1 but
belt-and-braces).

---

### Phase 3: Metadata Cleanup with Quartz Preview

Run Quartz locally as a diagnostic while continuing metadata work:

- Fix broken wikilinks (visible as dead links in rendered pages)
- Identify orphaned papers via graph view
- Catch YAML inconsistencies via tag pages
- Verify `key_findings` → description pipeline works across all papers
- Check that year-folder structure renders cleanly in explorer

This phase runs **in parallel** with Phases 2 and 4. It's not a gate —
it's an ongoing activity that Quartz makes faster.

---

### Phase 4: Custom Components (Moderate Work)

#### 4a. Filtered Clinical Pages

Three custom pages that filter `allFiles` by YAML frontmatter:

**Cardiac Safety Dashboard** (`category: RED`)
- Filter: `category === "RED"` or `secondary_categories includes "RED"`
- Display: Paper title, year, evidence_level, key_findings, qtc_data/herg_data flags
- Sort: By evidence_level (RCT → systematic review → ... → case report)

**Clinical Protocols Page** (`category: GREEN`)
- Filter: `category === "GREEN"`
- Display: Guideline name, year, dosing_range, contraindications, route

**Fatalities Register**
- Filter: `mortality_count > 0`
- Display: Paper, year, mortality_count, cause if documented
- **Critical caveat:** Same fatality may appear across multiple papers
  (e.g., Maas & Strubelt 2006 reporting same case as Alper 2012 retrospective).
  Needs deduplication logic or at minimum a displayed caveat.
  Data modelling question: does YAML currently have a unique fatality identifier
  linking duplicate reports to the same underlying case? If not, consider adding one.

Each is a custom emitter plugin or custom page component. ~50–100 lines each.

#### 4b. Category-Coloured Graph Nodes

This is **not CSS** — the graph renders via D3.js force simulation onto an
HTML Canvas element (`quartz/components/scripts/graph.inline.ts`). Canvas
doesn't respond to CSS selectors.

**Required changes:**
1. `quartz/plugins/emitters/contentIndex.ts` — include `category` in output
   data (currently emits: title, links, tags, content, date)
2. `quartz/components/scripts/graph.inline.ts` — modify node rendering to
   read category from content index and map to fill colours

```typescript
// Colour mapping for graph nodes
const categoryColors: Record<string, string> = {
  RED:    "#e74c3c",
  GREEN:  "#2ecc71",
  ORANGE: "#f39c12",
  BLUE:   "#3498db",
  PURPLE: "#9b59b6",
  WHITE:  "#95a5a6",
};
```

~30–50 lines of TypeScript across two files. Moderate work.

#### 4c. Filterable Master Table

The most complex component. A client-side sortable/filterable table replacing
Dataview TABLE for the web. Built as a custom Quartz component with React
state management.

- Data source: `allFiles` frontmatter
- Columns: title, year, category, evidence_level, tags, key_findings
- Features: column sorting, text filter, category filter checkboxes
- Think of it as the Dataview TABLE replacement that works on the web

~150–200 lines. Could use Claude Code for iterative development with live
preview feedback.

---

### Phase 5: GitHub Pages Deployment

**Prerequisites:** Phases 2 and 4 substantially complete.

**Steps:**
1. Set `baseUrl` in `quartz.config.ts` to deployment URL
2. Create `.github/workflows/deploy.yml` in the Quartz repo
3. Push to GitHub — site builds and deploys automatically
4. Configure custom domain if desired

**Quartz generates `file.html`** not `file/index.html`, so trailing-slash
links may break. If migrating from Obsidian Publish with existing links,
Cloudflare Pages handles redirects better than GitHub Pages.

---

## Known Issues & Caveats

### Dev Server Vulnerabilities (Safe to Ignore)

`npm audit` reports vulnerabilities in `minimatch`, `path-to-regexp`, and
`serve-handler`. These affect **only** the local dev server (`--serve` flag)
and do not impact production builds or deployed sites.

**Do not run `npm audit fix --force`** — it downgrades `serve-handler` from
v6 to v1.0.0, breaking the dev server entirely.

### Symlink Incompatibility

Quartz's dev server (`serve-handler`) cannot follow symlinks reliably.
Content must be a real directory copy, not a symlink. The `sync_quartz.sh`
script (Phase 2a) handles this.

### Alias Conflicts

Quartz processes `aliases` in frontmatter by generating redirect HTML files.
An alias of `"Index"` on any file will override the homepage `index.html`
with a redirect stub → infinite loop. Never use `"Index"` as an alias.

### .git Directory in Content

The GitHub clone of `IbogaineVault-Tier1/` includes `.git/`. When copied
to `content/`, this gets picked up by Quartz. Add `.git` to `ignorePatterns`
in `quartz.config.ts`.

---

## Tool Recommendations

| Task | Best Tool |
|------|-----------|
| Config changes (explorer sort, transformer, CSS) | Claude Desktop + Desktop Commander |
| Custom JSX components (filtered pages, master table) | Claude Code (can run `npx quartz build` to test) |
| Metadata cleanup | Claude Desktop (existing workflow) |
| Graph node colouring | Claude Code (needs visual verification) |
| Deployment setup | Either — straightforward YAML config |

---

## Reference

- Quartz docs: https://quartz.jzhao.xyz/
- Quartz repo: https://github.com/jackyzha0/quartz
- IbogaineVault Tier 1 repo: https://github.com/GforVendetta/IbogaineVault
- Quartz local path: `/Users/aretesofia/IbogaineVault-Quartz/` (Mac Studio)
- Dev server: `npx quartz build --serve --port 8888`
