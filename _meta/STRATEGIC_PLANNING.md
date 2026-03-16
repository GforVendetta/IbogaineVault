---
title: "IbogaineVault — Strategic Planning"
tags:
  - meta/hub
document_type: administrative
created: 2026-02-26
---

# IbogaineVault — Strategic Planning

> Distribution strategy, academic positioning, collaboration tactics, and novel ideas. This is a thinking space — items graduate to [[_meta/ROADMAP|ROADMAP]] when they become concrete work items.
>
> Technical distribution architecture → [[_meta/DISTRIBUTION_ARCHITECTURE|Distribution Architecture]]

---

## Phase 1 — Immediate (No Web Development Required)

### 1.1 Direct Vault Sharing with Collaborators
**Status:** Not started
**Effort:** 1–2 hours
**Impact:** Highest ROI action available

Zip the Tier 1 directory and send to Geoff Noller and Martijn Arns with a brief getting-started guide for Obsidian. They get the full graph, wikilinks, search, hub navigation, and YAML metadata — everything the vault offers — without waiting for any web layer.

Obsidian is free. Install takes five minutes. This can happen *today*.

If collaborators have Copilot Plus subscriptions, they also get natural language querying out of the box.

**Deliverables:**
- [ ] Write a 1-page "Getting Started with IbogaineVault in Obsidian" guide
- [ ] Zip Tier 1 directory
- [ ] Send to Noller and Arns
- [ ] Establish update cadence (periodic updated zips, or shared folder)

### 1.2 ORCID Registration
**Status:** Not started
**Effort:** 10 minutes
**Impact:** Permanent academic infrastructure

Register at https://orcid.org/. This is a persistent digital identifier for academic work — needed for CITATION.cff, Zenodo DOI, and any future publications. Do this once, use it forever.

### 1.3 CSV Metadata Export for Quantitative Researchers
**Status:** Not started
**Effort:** 1–2 hours (script)
**Impact:** High for Arns collaboration specifically

The vault's YAML frontmatter already contains structured fields that meta-analysts need: `sample_size`, `evidence_level`, `dosing_range`, `route`, `mortality_count`, `qtc_data`, `herg_data`, `electrolyte_data`, etc. A script to extract all YAML metadata into a CSV/Excel file creates a ready-made dataset for quantitative meta-analysis.

Arns would likely find this immediately useful for the fatalities analysis paper. This dramatically increases the vault's utility for quantitative researchers with minimal effort.

---

## Phase 2 — Academic Positioning

### 2.1 Methodology Paper
**Status:** Not started
**Effort:** Weeks (writing), but high leverage
**Impact:** Establishes vault as a citable academic contribution

Write a paper about the vault itself as a methodological contribution. Working title:

> *"Systematic Knowledge Architecture for Clinical Decision Support: A Structured Literature Synthesis of Ibogaine Research (1957–2026)"*

Publishable in medical informatics, drug policy, or evidence synthesis journals. The 8-week construction timeline, YAML schema design, category system, hub architecture, and cross-reference methodology are novel work. Nobody has built a structured clinical decision-support system for ibogaine research at this scale.

This paper is also the natural vehicle for a Zenodo DOI — the vault becomes the dataset/supplement.

### 2.2 Vault as Preprint Companion
**Status:** Concept
**Impact:** Genuinely novel in evidence synthesis literature

When Noller or Arns publish with you, the vault becomes a *living supplement* to the paper. Most systematic reviews have static supplementary tables. Yours would be an interactive, queryable, cross-referenced knowledge base.

Frame explicitly: "Supplementary Material: IbogaineVault — an interactive clinical decision-support system available at [URL/DOI]."

### 2.3 Replicable Methodology Template
**Status:** Concept
**Impact:** Broader contribution beyond ibogaine

The conversion manifest, YAML schema, category system, and hub architecture are a *generalised methodology* for building clinical decision-support systems from research literature. Someone could take this approach and build a KetamineVault, PsilocybinVault, MDMAVault.

If the methodology paper (2.1) documents this well, you're sharing a template for how to structure any clinical research domain — a bigger contribution than any individual vault.

### 2.4 Zenodo DOI Integration
**Status:** Not started (depends on 1.2 ORCID)
**Effort:** 1–2 hours once ORCID exists
**Impact:** Makes the vault citable in academic papers

A DOI is the bridge between "impressive project" and "established research instrument." When collaborators reference the vault in publications, they need a DOI. Zenodo is free and integrates with GitHub repos, but can also accept direct uploads — does not require a public repo.

---

## Phase 3 — Public Distribution (Future)

> These items require the GitHub repo to go public. The repo (`IbogaineVault` on GitHub) is currently **private** and staying that way until the pre-publication checklist is complete and the timing is right. None of Phase 3 is urgent — Phase 1 and 2 actions deliver more value sooner.

### 3.1 Pre-Publication Checklist (Before Repo Goes Public)
- [ ] ORCID registration + CITATION.cff update
- [ ] METHODOLOGY.md (vault construction methodology at publication level)
- [ ] `_meta/` review for public appropriateness
- [ ] `scope: pangea` sweep (automated, already passing)
- [ ] Git history scrub (BFG/filter-repo — old commits may contain internal tooling)
- [ ] Google Drive PDF folder (source PDFs for contributors)
- [ ] Final README review (counts, links)
- [ ] Zenodo DOI integration

### 3.2 Quartz Static Site
**Effort:** 1–2 weekends once repo is public
**Impact:** Transforms vault from "GitHub markdown files" into a browsable, searchable website

Quartz (https://quartz.jzhao.xyz/) is a free, open-source static site generator built specifically for Obsidian vaults. It preserves wikilinks as clickable links, renders a graph view, has full-text search, and handles YAML frontmatter.

Deployment pipeline: Working vault → `sync_tier1.sh` → git push → GitHub Action triggers Quartz build → live site on GitHub Pages (free hosting). No second source of truth. No drift. Site rebuilds from the same markdown.

**Why Quartz over alternatives:**
- **Obsidian Publish** ($8/month): easier but less customisable, no YAML querying, ongoing cost
- **MkDocs Material**: excellent for technical docs, less native support for Obsidian wikilinks/graph
- **Hugo/Jekyll**: general-purpose, would require more configuration for Obsidian-native features
- Quartz is purpose-built for this exact use case

### 3.3 YAML-Driven Query Pages
**Effort:** Days of development (after Quartz is running)
**Impact:** Makes the vault's structured metadata queryable on the web

Add pre-rendered or interactive query pages — filter by category, evidence_level, qtc_data, herg_data, dosing_range, etc. This is where the vault's clinical utility metadata becomes genuinely transformative compared to a flat document collection.

### 3.4 Community Outreach
**Status:** Concept (timing matters — do this when there's something to point people to)

The ibogaine policy and research community is small. MAPS, ATAI Life Sciences, Drug Policy Alliance, GITA (Global Ibogaine Therapy Alliance) would likely be interested. A well-timed announcement — through Noller's network, relevant mailing lists, or a conference poster — could establish the vault as a reference instrument for the field.

---

## Phase 4 — Deferred / Evaluate Later

### 4.1 AI-Powered Web Querying
**Status:** Deferred
**Effort:** Significant engineering project
**Impact:** Potentially transformative, but premature

An embedded chat widget on a public site that queries the vault via the Anthropic API. A clinician could type "What QTc monitoring protocols have the strongest evidence?" and get a synthesised answer with vault citations.

Genuinely powerful, but complex: API key management, cost per query, prompt engineering, rate limiting, authentication. This is a Phase 4 project — and the Obsidian + Copilot Plus setup already provides this capability for anyone with the vault installed locally.

### 4.2 IDE / Development Environment Changes
**Status:** Not needed currently

The current workflow (Obsidian + Claude Desktop + terminal) is appropriate for vault content work. VS Code or Claude Code would help specifically for Quartz configuration and GitHub Actions setup (Phase 3), but adding tooling complexity before then would be premature.

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-26 | Created strategic planning doc | Separate thinking space from ROADMAP (which tracks vault development work) |
| 2026-02-26 | GitHub repo stays private for now | Phase 1–2 actions deliver more value sooner; no rush to go public |
| 2026-02-26 | Direct vault sharing prioritised over web distribution | Highest ROI: collaborators get full vault capability immediately via Obsidian |
