---
title: "NLQ Architecture — Natural Language Query System"
date: 2026-02-05
category: WHITE
tags:
  - meta/moc
document_type: administrative
---

# NLQ Architecture — Natural Language Query System

**Purpose:** Design documentation for natural language query capability over the IbogaineVault  
**Status:** Planning — Phases 1-3 in development  
**Last updated:** 2026-02-05

---

## Section 1: Why NLQ Matters for Pangea

### The Gap Between Infrastructure and Consultation

The IbogaineVault exists. It contains 236 papers with structured YAML metadata, six colour-coded domain Hubs with curated research narratives, seven queryable Bases, and 552+ wikilinks forming evidence chains between papers. By any measure of research infrastructure, the vault is complete.

Yet Clare and Sarita don't currently consult it during clinical work. The gap isn't *content*—it's *access*. In the midst of an intake assessment, there's no time to construct a Bases query. During a pre-treatment screening, the cognitive load of navigating from Hub to paper to cross-reference exceeds what clinical workflow allows. The evidence is there; the interface isn't.

This is the gap NLQ addresses. Natural language query transforms the vault from a *research archive* into a *clinical copilot*—one that answers questions in the language clinicians think in, with citation-locked responses that trace every claim to its source.

### Clinical Workflow Integration Points

NLQ must serve four distinct clinical moments, each with different urgency, evidence requirements, and output formats:

| Clinical Moment | Example Question | Response Requirements |
|-----------------|------------------|----------------------|
| **Intake Assessment** | "Is this patient eligible given their cardiac history and methadone use?" | Fast, contraindication-focused, binary eligibility signal + reasoning |
| **Pre-Treatment Screening** | "What cardiac monitoring is required for this patient profile?" | Protocol-specific, draws on GREEN guidelines with RED evidence backing |
| **During Session** | "QTc is prolonging beyond baseline—what does the evidence say?" | Urgent synthesis, prioritises actionable clinical guidance over comprehensive review |
| **Post-Session Analysis** | "Patient reported ancestor contact and ego dissolution—what does the literature suggest for integration?" | Longer-form, draws on PURPLE phenomenology, supports therapeutic reflection |

The same underlying infrastructure serves all four, but the *output format* and *evidence weighting* differ by context.

---

## Section 2: Architecture Overview

### System Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         NATURAL LANGUAGE QUERY                          │
│                                                                         │
│   "What cardiac contraindications exist for a patient on methadone?"    │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        IR PARSING (Phase 3)                             │
│                                                                         │
│   Intent: CONTRAINDICATIONS                                             │
│   Hard constraints: category == "RED" OR contraindications contains     │
│                     "methadone"                                         │
│   Soft constraints: evidence_level in [guideline, systematic-review,    │
│                     rct] preferred                                      │
│   Output format: CONTRAINDICATION_MATRIX                                │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        METADATA FILTER (The Key)                        │
│                                                                         │
│   Vault's structured YAML enables precise pre-filtering:                │
│   - category: RED, GREEN, ORANGE, BLUE, PURPLE, WHITE                   │
│   - evidence_level: rct, guideline, systematic-review, etc.             │
│   - qtc_data: boolean (has any QTc findings)                            │
│   - contraindications: array of strings                                 │
│   - mortality_count: integer (presence = ≥1 death)                      │
│                                                                         │
│   This pre-filtering is the vault's superpower vs. generic RAG.         │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        SEMANTIC RANKING                                 │
│                                                                         │
│   Within filtered set, rank by semantic relevance to query.             │
│   Embeddings over paper abstracts and key_findings fields.              │
│   Wikilink graph expansion: include 1-hop connected papers.             │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        SOURCE REVIEW (Human-in-Loop)                    │
│                                                                         │
│   Present 5-8 candidate sources to clinician BEFORE synthesis.          │
│   Clinician can exclude/add sources.                                    │
│   Required for all safety-critical intents.                             │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        CITATION-LOCKED SYNTHESIS                        │
│                                                                         │
│   Every claim traces to a source paper.                                 │
│   Evidence weights displayed: [RCT], [Guideline], [Case Report]         │
│   Synthesis reflects MISTIC paradigm shift where applicable.            │
│   Format matches intent: brief for CONTRAINDICATIONS, longer for        │
│   EVIDENCE_SYNTHESIS.                                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Why Metadata-First Filtering Is the Key Differentiator

Generic RAG systems retrieve by semantic similarity alone. This creates two failure modes:

1. **False positives:** Papers mentioning "cardiac" in passing rank alongside papers that *study* cardiac effects
2. **False negatives:** Case reports with rare adverse events get buried beneath higher-ranked review articles

The vault's structured YAML enables *metadata-first filtering*. Before semantic ranking even begins, the system can:

- Filter to RED category papers only (cardiac safety)
- Require `qtc_data: true` (papers with actual QTc findings)
- Exclude papers without `evidence_level` (unvetted content)
- Surface papers where `contraindications` array contains specific terms

This isn't semantic search with metadata as a tiebreaker—it's *constraint satisfaction* that guarantees relevant papers enter the ranking stage.

### Evidence Weighting Prevents Dangerous Confidence

The dangerous failure mode for clinical decision-support isn't irrelevant results—it's *confident synthesis that misses a crucial exception*. 

A single case report documenting fatal arrhythmia in a patient with undiagnosed channelopathy might be the most clinically important paper for a given query, even if 15 cohort studies report no adverse events. Generic RAG systems, optimising for average relevance, would bury that case report.

Evidence weighting addresses this by:

1. **Elevating guidelines and systematic reviews** for protocol questions (highest quality evidence shapes recommendations)
2. **Never excluding case reports** for safety-critical intents (rare events matter)
3. **Flagging evidence level in synthesis** so clinicians see the epistemic status of each claim

For CONTRAINDICATION intents specifically, case reports receive *elevated* not depressed ranking—the one patient who died matters more than the hundred who didn't.

---

## Section 3: Phase 1 — Copilot Configuration (Immediate)

### Objective

Configure an AI copilot (likely Obsidian Copilot or similar plugin) to use the vault as its knowledge base, with clinical-appropriate prompting that enforces citation and evidence awareness.

### Indexing Boundaries

**Include:**
- All papers in year folders (`/1969/` through `/2026/`)
- Clinical Guidelines (`/Clinical_Guidelines/` including `/Pangea/`)
- Primary Sources (`/Primary_Sources/`)
- Industry Documents (`/Industry_Documents/`)
- All Hub and MOC files
- Tag Taxonomy and GETTING_STARTED.md

**Exclude:**
- `/Pangea_Ops/` — Internal operational notes (not clinical evidence)
- `/_meta/` — Administrative files (ROADMAP, WORKLOG, etc.)
- `/.local/` — Local PDF integration (already excluded from Publish)
- `/.obsidian/` — Obsidian configuration

### Clinical System Prompt Template

```markdown
You are a clinical research assistant for Pangea Biomedics, New Zealand's first legal ibogaine treatment facility. You have access to a curated vault of 236 ibogaine research papers (1969-2026) with structured metadata.

**Response Requirements:**

1. **Every claim must cite its source.** Use the format: "QTc prolongation risk increases with dose [Alper2016]" — never make uncited clinical claims.

2. **Flag evidence level for each citation:**
   - [RCT], [Systematic Review], [Guideline] = highest confidence
   - [Cohort], [Observational] = moderate confidence
   - [Case Report], [Case Series] = important for safety, lower generalisability

3. **For cardiac safety questions:** Always check for and mention any case reports with adverse outcomes, even if larger studies show favourable results. One death matters.

4. **Paradigm awareness:** The MISTIC protocol (Cherian 2024) demonstrated that magnesium co-administration eliminates QTc prolongation. Frame cardiac safety evidence through this lens—not "these are the risks" but "this is how we know the protocol is safe when followed correctly."

5. **When uncertain:** Say so. "The vault contains no papers addressing X directly" is better than fabricated synthesis.

6. **Clinical context categories:**
   - RED = Cardiac safety, fatalities, contraindications
   - GREEN = Clinical protocols, screening, guidelines
   - ORANGE = Pharmacology, mechanisms
   - BLUE = Clinical outcomes, efficacy
   - PURPLE = Phenomenology, subjective experience
   - WHITE = Historical, cultural context

**The vault's key_findings field in each paper's YAML contains a one-line clinical summary. Prioritise these for rapid orientation before diving into full paper content.**
```

### Recommended Plugin: Obsidian Copilot

- Indexes vault content including YAML frontmatter
- Supports custom system prompts
- Can be configured to prefer local embeddings over cloud

**Alternative:** Smart Connections plugin (more mature embedding system, less flexible prompting)

---

## Section 4: Phase 2 — Clinical Question Test Suite (This Week)

### Purpose

A validated set of 20-30 real clinical questions that test the NLQ system's retrieval accuracy and synthesis quality. These questions should come from Clare and Sarita based on actual queries they encounter in clinical practice.

### Intent Categories

The following categories scaffold the test suite. Each placeholder question illustrates the intent type—**Clare and Sarita should replace these with actual questions they've had or anticipate having.**

#### 4.1 CONTRAINDICATIONS

Questions about patient eligibility and exclusion criteria.

| # | Placeholder Question | Expected Constraints | Output Format |
|---|---------------------|---------------------|---------------|
| 1 | REPLACE: "Can a patient with Long QT Syndrome receive ibogaine?" | category: RED OR contraindications contains "long qt" | CONTRAINDICATION_MATRIX |
| 2 | REPLACE: "What cardiac conditions absolutely exclude treatment?" | category: RED, evidence_level: guideline preferred | CONTRAINDICATION_MATRIX |
| 3 | REPLACE: "Is methadone maintenance a contraindication?" | tags contains topic/methadone OR contraindications contains "methadone" | CLINICAL_BRIEF |

#### 4.2 CARDIAC_RISK

Questions specifically about cardiac safety evidence.

| # | Placeholder Question | Expected Constraints | Output Format |
|---|---------------------|---------------------|---------------|
| 4 | REPLACE: "What causes QTc prolongation with ibogaine?" | category: RED, qtc_data: true, tags contains mechanism/herg-blockade | EVIDENCE_SYNTHESIS |
| 5 | REPLACE: "How does magnesium prevent cardiac events?" | tags contains topic/electrolytes, evidence_level: rct OR cohort preferred | EVIDENCE_SYNTHESIS |
| 6 | REPLACE: "Have there been cardiac deaths in controlled clinical settings?" | mortality_count exists, category: RED | CASE_SUMMARY |

#### 4.3 DRUG_INTERACTIONS

Questions about medication interactions and washout requirements.

| # | Placeholder Question | Expected Constraints | Output Format |
|---|---------------------|---------------------|---------------|
| 7 | REPLACE: "What is the required washout period for SSRIs?" | tags contains topic/drug-interaction OR contraindications contains "ssri" | CLINICAL_BRIEF |
| 8 | REPLACE: "Is buprenorphine safer than methadone for transition?" | tags contains topic/methadone OR topic/buprenorphine | EVIDENCE_SYNTHESIS |
| 9 | REPLACE: "What medications interact with ibogaine's hERG blockade?" | category: RED, tags contains mechanism/herg-blockade | DRUG_INTERACTION_TABLE |

#### 4.4 DOSING_PROTOCOLS

Questions about dosing strategies and administration.

| # | Placeholder Question | Expected Constraints | Output Format |
|---|---------------------|---------------------|---------------|
| 10 | REPLACE: "What is the typical dose range for opioid dependence?" | category: GREEN, dosing_range exists | CLINICAL_BRIEF |
| 11 | REPLACE: "How does GITA recommend titrating based on weight?" | category: GREEN, evidence_level: guideline | PROTOCOL_SUMMARY |
| 12 | REPLACE: "What's the evidence for flood vs. incremental dosing?" | category: GREEN, tags contains topic/dosing | EVIDENCE_SYNTHESIS |

#### 4.5 CLINICAL_OUTCOMES

Questions about treatment efficacy and outcomes.

| # | Placeholder Question | Expected Constraints | Output Format |
|---|---------------------|---------------------|---------------|
| 13 | REPLACE: "What are the PTSD remission rates in veterans studies?" | category: BLUE, tags contains topic/veterans AND topic/ptsd | OUTCOMES_SUMMARY |
| 14 | REPLACE: "How long do anti-craving effects typically last?" | category: BLUE, evidence_level: rct OR cohort | EVIDENCE_SYNTHESIS |
| 15 | REPLACE: "What predicts positive treatment outcomes?" | category: BLUE, tags contains method/clinical-trial | EVIDENCE_SYNTHESIS |

#### 4.6 PHENOMENOLOGY

Questions about subjective experience and integration.

| # | Placeholder Question | Expected Constraints | Output Format |
|---|---------------------|---------------------|---------------|
| 16 | REPLACE: "What visual phenomena are commonly reported?" | category: PURPLE | QUALITATIVE_SUMMARY |
| 17 | REPLACE: "How should ancestor contact experiences be integrated?" | category: PURPLE, evidence_level: qualitative | CLINICAL_BRIEF |
| 18 | REPLACE: "Does phenomenology predict therapeutic outcome?" | category: PURPLE OR BLUE, tags contains topic/phenomenology | EVIDENCE_SYNTHESIS |

#### 4.7 MECHANISMS

Questions about pharmacology and neuroscience.

| # | Placeholder Question | Expected Constraints | Output Format |
|---|---------------------|---------------------|---------------|
| 19 | REPLACE: "How does ibogaine's GDNF upregulation work?" | category: ORANGE, tags contains mechanism/gdnf | MECHANISM_SUMMARY |
| 20 | REPLACE: "What's the clinical relevance of kappa-opioid agonism?" | category: ORANGE, tags contains mechanism/kappa-opioid | EVIDENCE_SYNTHESIS |

### Validation Protocol

For each test question:

1. Run query through NLQ system
2. Record retrieved papers (compare to expected set)
3. Record synthesis output
4. Clare/Sarita rate: 
   - Retrieval accuracy (did it find the right papers?)
   - Synthesis quality (is the answer clinically useful?)
   - Safety (did it miss any critical contraindications or caveats?)
5. Document failures for IR schema refinement

---

## Section 5: Phase 3 — Query Plan IR Schema (Near-term)

### Purpose

An intermediate representation that maps natural language queries to structured constraints before retrieval. This prevents the model from inventing filters or misinterpreting vault structure.

### Schema Structure

```yaml
query_plan:
  raw_query: "What cardiac contraindications exist for methadone patients?"
  
  intent:
    primary: CONTRAINDICATIONS
    secondary: CARDIAC_RISK
  
  constraints:
    hard:
      # Must-pass filters — papers not matching are excluded
      - or:
          - category: RED
          - contraindications_contains: ["methadone", "cardiac", "qtc"]
    soft:
      # Ranking preferences — matching papers scored higher
      - evidence_level_in: [guideline, systematic-review, rct]
      - qtc_data: true
  
  graph_expansion:
    enabled: true
    hops: 1
    # Include papers linked via wikilinks from matched set
  
  output:
    format: CONTRAINDICATION_MATRIX
    max_sources: 8
    evidence_display: true  # Show [RCT], [Guideline] etc.
    hub_context: RED_Cardiac_Safety_Hub  # Inform synthesis with Hub narrative
```

### Intent Catalogue

| Intent | Hard Constraints | Soft Constraints | Output Format | Case Report Handling |
|--------|------------------|------------------|---------------|---------------------|
| CONTRAINDICATIONS | category: RED OR contraindications exists | evidence_level: guideline preferred | CONTRAINDICATION_MATRIX | **Elevated** — rare events crucial |
| CARDIAC_RISK | category: RED | qtc_data: true, herg_data: true | EVIDENCE_SYNTHESIS | **Elevated** |
| DRUG_INTERACTIONS | tags contains topic/drug-interaction | evidence_level: guideline, systematic-review | DRUG_INTERACTION_TABLE | **Elevated** |
| DOSING_PROTOCOLS | category: GREEN | evidence_level: guideline | PROTOCOL_SUMMARY | Normal |
| CLINICAL_OUTCOMES | category: BLUE | evidence_level: rct, cohort | OUTCOMES_SUMMARY | Normal |
| EFFICACY_COMPARISON | category: BLUE | evidence_level: rct, systematic-review | COMPARISON_TABLE | Normal |
| PHENOMENOLOGY | category: PURPLE | evidence_level: qualitative | QUALITATIVE_SUMMARY | N/A |
| MECHANISM | category: ORANGE | evidence_level: preclinical, in-vitro | MECHANISM_SUMMARY | N/A |
| HISTORICAL | category: WHITE | (none) | NARRATIVE | N/A |
| PATIENT_ELIGIBILITY | (multi-category) | category: RED + GREEN | ELIGIBILITY_CHECKLIST | **Elevated** |

### Phrase → Intent Mapping

The IR parser should recognise these trigger phrases and map to intents:

```yaml
phrase_intent_mapping:
  # CONTRAINDICATIONS triggers
  - phrases: ["contraindicated", "can they receive", "eligible", "exclude", "rule out"]
    intent: CONTRAINDICATIONS
  
  # CARDIAC_RISK triggers
  - phrases: ["cardiac", "QTc", "heart", "arrhythmia", "hERG", "torsades"]
    intent: CARDIAC_RISK
    constraint_additions:
      - qtc_data: true
  
  # DRUG_INTERACTIONS triggers
  - phrases: ["interact", "combination", "washout", "clearance", "with methadone", "with SSRIs"]
    intent: DRUG_INTERACTIONS
  
  # DOSING_PROTOCOLS triggers
  - phrases: ["dose", "dosing", "mg/kg", "titrate", "flood", "incremental"]
    intent: DOSING_PROTOCOLS
  
  # CLINICAL_OUTCOMES triggers
  - phrases: ["outcome", "efficacy", "remission", "success rate", "effect size"]
    intent: CLINICAL_OUTCOMES
  
  # PHENOMENOLOGY triggers
  - phrases: ["experience", "vision", "ancestor", "entity", "dissolution", "integration"]
    intent: PHENOMENOLOGY
```

### Phrase → Category Priors

When specific categories are mentioned, bias filtering accordingly:

```yaml
phrase_category_mapping:
  - phrases: ["safety", "death", "fatality", "adverse", "risk", "cardiac"]
    category_prior: RED
    weight: 0.8
  
  - phrases: ["protocol", "guideline", "screening", "monitoring", "procedure"]
    category_prior: GREEN
    weight: 0.7
  
  - phrases: ["mechanism", "receptor", "GDNF", "pharmacology", "binding"]
    category_prior: ORANGE
    weight: 0.7
  
  - phrases: ["trial", "study", "outcome", "remission", "veterans", "PTSD"]
    category_prior: BLUE
    weight: 0.6
  
  - phrases: ["experience", "vision", "journey", "integration", "subjective"]
    category_prior: PURPLE
    weight: 0.7
  
  - phrases: ["history", "Bwiti", "Lotsof", "traditional", "policy"]
    category_prior: WHITE
    weight: 0.5
```

### Evidence Weighting Defaults

```yaml
evidence_weights:
  # Base weights (0-1) applied during ranking
  rct: 1.0
  systematic-review: 0.95
  guideline: 0.95
  cohort: 0.75
  observational: 0.65
  case-series: 0.5
  case-report: 0.4
  qualitative: 0.5
  preclinical: 0.4
  in-vitro: 0.35
  review: 0.6
  
  # Override for safety-critical intents
  safety_critical_override:
    intents: [CONTRAINDICATIONS, CARDIAC_RISK, DRUG_INTERACTIONS, PATIENT_ELIGIBILITY]
    case_report_weight: 0.85  # Elevated from 0.4
    mortality_boost: 0.3       # Additional weight for papers with mortality_count
```

### YAML Field Reference

> **Derived from** `_meta/schema_registry.yml` (authoritative where they disagree).  
> Last verified against registry: 2026-02-23

These are the queryable fields the IR schema can constrain:

**Structural:**
- `category` — RED, GREEN, ORANGE, BLUE, PURPLE, WHITE
- `tags` — 62 canonical tags in topic/, mechanism/, method/, meta/ namespaces (39 topic + 10 mechanism + 11 method + 2 meta)
- `document_type` — 22 paper types, 3 transcript types, 1 meta type. See `_meta/schema_registry.yml` for the full enum; common queryable values include: clinical-trial, review, systematic-review, case-report, case-series, guideline, in-vitro, preclinical, observational, qualitative, commentary, meeting-transcript, interview-transcript, conference-talk
- `scope` — `pangea` | `published`. Distinguishes internal operational content from publicly available material. Present on transcript schemas (transcript_meeting, transcript_published) only — papers don't carry scope.

**Evidence:**
- `evidence_level` — rct, systematic-review, cohort, case-series, case-report, observational, qualitative, preclinical, in-vitro, review, guideline, journalism

**Clinical:**
- `qtc_data` — boolean (any QTc finding, numeric OR qualitative)
- `herg_data` — boolean (hERG channel studies)
- `electrolyte_data` — boolean (magnesium/potassium protocols)
- `contraindications` — array of strings
- `sample_size` — integer
- `mortality_count` — integer (field presence = ≥1 death)
- `dosing_range` — string
- `route` — oral, intravenous, subcutaneous, intramuscular, intraperitoneal, topical, not-specified. NLQ query interfaces may accept abbreviations (iv, im, etc.) but the vault stores full names.

---

## Section 6: Graph and Hub Integration

### Wikilink Graph Exploitation

The vault contains 552+ wikilinks representing *intellectual relationships* discovered through close reading. These aren't algorithmic similarity scores—they're assertions that "this paper builds on that paper" or "this finding contradicts that finding."

**Graph expansion logic:**

1. Metadata filtering produces initial paper set (e.g., 12 papers)
2. For each paper in set, retrieve papers it links to via `[[wikilink]]` (1-hop expansion)
3. For each linked paper, check if it passes soft constraints
4. Add qualifying linked papers to candidate set with slightly lower ranking score
5. Present expanded set (e.g., 15-18 papers) for semantic ranking

**Rationale:** A paper that closely links to a query-matched paper likely contains relevant context, even if its YAML metadata wouldn't have matched the query directly.

### Hub-Aware Synthesis

The six domain Hubs aren't just navigation aids—they contain *curated synthesis*. Each Hub includes:

- "How We Got Here" research arc narratives
- Key papers organised by significance
- Cross-references showing how evidence evolved

**When to use Hub content:**

| Query Type | Hub Integration |
|------------|-----------------|
| CONTRAINDICATIONS | Surface RED_Cardiac_Safety_Hub's contraindications synthesis |
| CARDIAC_RISK | Use Hub's "MISTIC Paradigm Shift" framing |
| DOSING_PROTOCOLS | Draw on GREEN_Clinical_Protocols_Hub's protocol comparisons |
| PHENOMENOLOGY | Reference PURPLE_Phenomenology_Hub's experience taxonomy |

**Implementation:** When query matches a Hub's domain, include Hub's relevant sections in context alongside raw paper retrieval. This grounds synthesis in pre-validated narrative structure.

### Hub Priority Matrix

| Intent | Primary Hub | Secondary Hub |
|--------|-------------|---------------|
| CONTRAINDICATIONS | RED_Cardiac_Safety_Hub | GREEN_Clinical_Protocols_Hub |
| CARDIAC_RISK | RED_Cardiac_Safety_Hub | — |
| DRUG_INTERACTIONS | RED_Cardiac_Safety_Hub | GREEN_Clinical_Protocols_Hub |
| DOSING_PROTOCOLS | GREEN_Clinical_Protocols_Hub | — |
| CLINICAL_OUTCOMES | BLUE_Outcomes_Hub | — |
| PHENOMENOLOGY | PURPLE_Phenomenology_Hub | — |
| MECHANISM | ORANGE_Mechanisms_Hub | — |
| HISTORICAL | WHITE_Historical_Hub | — |

---

## Section 7: Human-in-the-Loop Protocol

### Why Human Review Is Non-Negotiable

This system supports clinical decision-making. The consequences of acting on incorrect synthesis range from suboptimal treatment to patient death. Human review isn't a "nice to have"—it's a safety requirement.

### Source Review Protocol

**For all safety-critical intents (CONTRAINDICATIONS, CARDIAC_RISK, DRUG_INTERACTIONS, PATIENT_ELIGIBILITY):**

1. **Source display before synthesis:** Present 5-8 candidate sources with:
   - Paper title and year
   - Evidence level badge: [RCT], [Guideline], [Case Report], etc.
   - One-line key_findings summary
   - Relevance score (why this paper matched)

2. **Clinician actions:**
   - ✓ Confirm sources and proceed to synthesis
   - ✗ Exclude specific source (with optional reason)
   - + Add source by name (search and include)
   - ⚠ Flag source for later review

3. **Only after confirmation:** Generate synthesis from approved source set

**For non-safety intents (CLINICAL_OUTCOMES, PHENOMENOLOGY, MECHANISM, HISTORICAL):**

- Source review is *offered* but not *required*
- Clinician can request "show me the sources" before synthesis
- Default behaviour: proceed to synthesis with sources cited

### Source Count Guidelines

| Intent Type | Minimum Sources | Typical Range | Maximum |
|-------------|-----------------|---------------|---------|
| Safety-critical | 3 | 5-8 | 12 |
| Clinical outcomes | 2 | 4-6 | 10 |
| Phenomenology | 2 | 3-5 | 8 |
| Mechanism | 2 | 4-6 | 10 |
| Historical | 1 | 2-4 | 6 |

### Handling Source Disagreement

When retrieved sources contain conflicting findings:

1. **Flag the conflict** explicitly: "Sources disagree on X"
2. **Present both positions** with respective evidence levels
3. **Recommend the higher-evidence position** while noting the caveat
4. **For safety conflicts:** Always err toward caution; if one case report shows adverse outcome and ten cohort studies don't, mention the case report prominently

---

## Section 8: Future Phases (Deferred — Notes Only)

> **⚠️ NOT IN SCOPE FOR CURRENT DEVELOPMENT**
> 
> The following sections document future possibilities for reference only. Do not implement until Phases 1-3 are complete and validated.

### Phase 4: Plugin Implementation

**Potential approach:** Custom Obsidian plugin combining:

- Smart Connections (embedding and retrieval)
- Custom metadata pre-filter layer
- IR schema parser
- Human-in-the-loop UI components

**Technical considerations:**
- Embedding model selection (local vs. cloud)
- Query plan persistence for audit trail
- Integration with existing Bases infrastructure

### Phase 5: Static Evidence Packs for Publish

**Concept:** Pre-computed synthesis documents for common queries, published alongside the vault. Clinicians get instant answers for frequent questions without waiting for LLM synthesis.

**Example evidence packs:**
- "Cardiac Contraindications Summary" — pre-synthesised from RED papers
- "MISTIC Protocol Evidence Brief" — BLUE outcomes + RED safety
- "Drug Interaction Quick Reference" — GREEN protocols + RED contraindications

**Benefits:**
- No LLM latency for common queries
- Reviewed and approved synthesis (higher trust)
- Available offline/on Publish site

### Phase 6: Continuous Learning

**Concept:** Track clinician corrections to synthesis and use to refine:
- Intent classification
- Evidence weighting
- Phrase→constraint mappings

**Requirements:** Structured feedback capture, privacy-compliant logging, periodic schema updates.

---

## Related Documents

- [[_meta/VAULT_ARCHITECTURE]] — Bases syntax, graph view, PDF integration, folder structure
- [[_meta/ROADMAP]] — Project development status
- [[_meta/WORKLOG]] — Session-by-session progress
- [[_meta/Tag_Taxonomy]] — Complete 61-tag reference
- [[RED_Cardiac_Safety_Hub]] — Cardiac safety evidence synthesis
- [[GREEN_Clinical_Protocols_Hub]] — Clinical protocol guidance

---

*Last updated: 2026-02-05*
