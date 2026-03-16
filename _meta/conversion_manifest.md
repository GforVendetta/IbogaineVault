# Conversion Manifest
# Single source of truth for all paper conversions.
# Read this + the PDF. That's it.
#
# Schema changes: Follow the propagation checklist at
# _meta/prompts/schema_decision_propagation_checklist.md

---

## YAML Schema

```yaml
---
title: "Full Academic Title"          # Quoted if contains colons
authors:                               # List format, ALL authors, surname first
  - "Surname, Given Name"
year: 2024                             # Integer, publication year
category: RED                          # Exactly one: RED | GREEN | ORANGE | BLUE | PURPLE | WHITE
tags:                                  # 2–10 depending on document type — see Tag Count Policy below, list format
  - topic/cardiac
  - method/review
key_findings: "≤250 chars"            # What matters most about THIS paper in its own domain
source_pdf: "2024/filename.pdf"        # Relative path
doi: "10.xxxx/xxxxx"                   # If available — omit field entirely if not
journal: "Journal Name"               # If available — omit field entirely if not
publication_date: "2024-03-15"         # Quoted string per D13 — omit if only year known (year field covers it)
document_type: review                  # See valid types below
secondary_categories: [BLUE]           # Inline format per D12 — never multi-line YAML list
clinical_significance: high            # high | moderate | low | landmark
aliases:                               # For Obsidian search
  - "Author Year"
  - "Short Description"
evidence_level: review                 # See valid levels below
sample_size: 50                        # Human studies only — see Field Rules below
mortality_count: 3                     # Fatality data only — see Field Rules below
qtc_data: false                        # REQUIRED ALL PAPERS — see Boolean Flag Rules
electrolyte_data: false                # REQUIRED ALL PAPERS — see Boolean Flag Rules
herg_data: false                       # REQUIRED ALL PAPERS — see Boolean Flag Rules
contraindications:                     # Populated list OR [] — never omit field
  - "Pre-existing cardiac conditions"
dosing_range: "10–20 mg/kg oral"       # GREEN mandatory; populate for RED/BLUE when available
route: oral                            # GREEN mandatory; populate for RED/BLUE when available
organisation: "Org Name"               # Non-academic documents only (industry, NGO, journalism)
pmid: "12345678"                       # PubMed ID — omit if not indexed. Never fabricate
pmcid: "PMC1234567"                    # PubMed Central ID — omit if no PMC deposit
isbn: "978-0-691-02713-0"             # Books, book-chapters, theses — omit if not applicable
issn: "1234-5678"                      # Journal ISSN — especially useful for journals without DOIs
---
```

### YAML Rules
- No blank lines between opening `---` and first field
- Tags in list format (never inline array)
- No `#` prefix on tags
- contraindications: populated list OR `[]` — never empty field, never omit

### Field Omission Rules

**Omit entirely when unavailable** (never use empty strings, fabricated dates, or zero):
- `doi` — omit if no DOI exists. Never `doi: ""`
- `journal` — omit if not applicable (e.g., book, primary source)
- `publication_date` — omit if only year is known. The `year` field covers it. Never fabricate month/day. When present, always quote: `"2024-03-15"` (D13)
- `sample_size` — omit for non-human studies, reviews, in-vitro. Never use 0
- `mortality_count` — omit if no deaths reported. Never use 0. See Field Rules below
- `dosing_range` — omit for ORANGE/PURPLE/WHITE if genuinely no dosing data
- `route` — omit for ORANGE/PURPLE/WHITE if genuinely no route data
- `organisation` — omit for academic papers
- `pmid` — omit if paper not indexed in PubMed. Never fabricate. Resolvable from DOI via NCBI ID Converter
- `pmcid` — omit if no PubMed Central deposit. Subset of PMID papers
- `isbn` — omit unless book, book-chapter, or thesis with ISBN
- `issn` — omit unless journal has no DOI or is obscure enough that name alone may not resolve
- `secondary_categories` — omit if only one category applies

**Principle:** The PRESENCE of a field is a semantic signal. `mortality_count: 0` falsely says "this paper analysed fatalities and found zero." Omission says "this paper doesn't contain fatality data." These mean different things to a clinician querying the vault.

---

## Field Rules

### sample_size
- **Human studies only.** Integer count of human participants from Methods section
- Reviews: omit (don't use total of reviewed studies)
- Animal studies: omit (preclinical animal counts are not sample_size)
- In-vitro: omit

### mortality_count
```
Does the paper report ≥1 death (directly studied, case report, or tabulated in review)?
  YES → mortality_count: [exact integer]
  NO  → OMIT the field entirely
```
- For review papers that tabulate or systematically analyse deaths from the literature, count them (e.g., Koenig2015: 22, Litjens2016: 27, Esperanca2026: 19)
- Fatality case reports: mortality_count: 1
- Paper discusses death risk without reporting specific deaths: omit

### evidence_level Clarifications
- **in-vitro ≠ preclinical.** `in-vitro` = cell/tissue/channel assays (hERG patch-clamp, receptor binding, hepatocyte studies). `preclinical` = whole animal models (rat self-administration, mouse locomotor, primate studies). Don't conflate.
- **Thesis/book:** Use actual methodology, not document format. Thesis doing a review → `evidence_level: review`. Book synthesising ethnographic material → `evidence_level: qualitative`.
- **Brief-communication:** Same principle. Publication format ≠ evidence type.
- **Journalism:** The one exception to the "publication format ≠ evidence type" rule. Use `evidence_level: journalism` for all `document_type: journalism` papers. Journalism uses interview-based, document-analysis methods without systematic design, peer review, or reproducible protocols. Forcing journalism into `qualitative`, `observational`, or `case-report` overstates rigour and contaminates evidence-filtered queries (e.g., a clinician querying "all observational evidence" should not find a Substack article). The `document_type: journalism` field identifies *what* it is; `evidence_level: journalism` tells a querying clinician *how much to trust it*.

---

## Boolean Flag Decision Table

All three flags are REQUIRED on ALL papers, no exceptions. These drive Bases queries — incorrect flags mean safety-critical data won't surface when queried.

| Flag | Set `true` when | Set `false` when | Common false negatives |
|------|----------------|------------------|----------------------|
| `qtc_data` | Paper contains ANY QTc interval data, QTc prolongation discussion with measurements, or ECG monitoring protocols with QTc thresholds | Paper mentions "cardiac" without QTc specifics | QTc screening thresholds in exclusion criteria (e.g., ">450ms") **count as true**. ECG monitoring protocols that specify QTc cutoffs = true |
| `electrolyte_data` | Paper contains ANY electrolyte guidance — K⁺, Mg²⁺, Ca²⁺ levels, magnesium co-administration protocols, hypokalaemia warnings, electrolyte screening, TdP treatment with Mg²⁺ | Paper doesn't mention electrolytes or mentions them only by name without data/guidance | **Most frequently miscategorised flag.** Mg²⁺ infusion protocols = true. K⁺ in exclusion criteria = true. Clinical electrolyte guidance counts even without an explicit "electrolyte monitoring" section header. Pre-dosing MgSO₄ listed as supportive care in treatment procedures paragraphs = true (e.g., Barsuglia2018) |
| `herg_data` | Paper contains original hERG channel assay data, hERG IC₅₀ values, or hERG blockade discussion with specific experimental data | Paper cites hERG studies without original data. Review papers discussing hERG findings from other papers | Only original hERG assay data = true. Citing or discussing others' hERG results = false |

---

## Category-Specific Mandatory Fields

Beyond the fields required for ALL papers (category, tags, three booleans, contraindications, key_findings, aliases), each category has additional mandatory fields:

| Field | RED | GREEN | ORANGE | BLUE | PURPLE | WHITE |
|-------|-----|-------|--------|------|--------|-------|
| `mortality_count` | If ≥1 death | — | — | — | — | — |
| `dosing_range` | **Yes**¹ | **Yes** | — | If available | — | — |
| `route` | **Yes**¹ | **Yes** | — | If available | — | — |
| `sample_size` | If human | — | — | If human | If human | — |
| `contraindications` | Comprehensive | Comprehensive | `[]` typical | Extract from exclusion criteria | `[]` typical | `[]` typical |

¹ RED papers: populate even for fatality cases with unknown doses. Describe what IS known: `"unknown (root bark, ~18 spoonfuls over ~10 hours, blood levels 5–20× therapeutic)"`. Route is usually determinable even from fatality reports.

---

## Contraindications Extraction Strategy

This field was the most systematically underpopulated across ALL categories. Patterson2014 went from 7→19 items when properly extracted. The data IS in the papers — search these locations:

1. **Exclusion criteria / Screening criteria** — Richest source. Every exclusion criterion IS a contraindication
2. **Emergency response protocols** — Contraindicated medications that interact with emergency drugs
3. **Medication interaction lists** — CYP2D6 inhibitors, QT-prolonging drugs, serotonergic medications, opioid agonists
4. **Substance abstinence requirements** — Pre-treatment taper timelines (methadone, benzodiazepines, stimulants)
5. **CYP2D6 guidance** — Poor metaboliser status, genotyping recommendations, dose adjustments
6. **Medical history red flags** — Cardiac history, hepatic/renal impairment, seizure history, pregnancy
7. **Age/demographic restrictions** — Minimum/maximum age, BMI restrictions
8. **Monitoring thresholds that imply contraindication** — "QTc >450ms excludes participation" → contraindication

**Format:** Each item as a separate string. Be specific:
```yaml
# BAD:
contraindications:
  - "Heart problems"

# GOOD:
contraindications:
  - "Pre-existing cardiac disease (cardiomyopathy, valvular disease, CAD)"
  - "Baseline QTc >450ms (males) or >460ms (females)"
  - "CYP2D6 poor metaboliser status"
  - "Concurrent methadone use (minimum 7-day taper required)"
```

If the paper genuinely contains NO contraindication data: `contraindications: []`

---

## Dosing Data Extraction

Even when the paper's primary purpose isn't dosing, capture what's present:

- **Therapeutic doses:** "10-20 mg/kg", "15 mg/kg HCl", "200mg test dose"
- **Fatality case doses:** Even if unknown, describe context — see RED exemplar below
- **Safety threshold doses:** "NOAEL 25 mg/kg in rats", "safe dose ~0.87 mg/kg"
- **Test dose protocols:** "100-200mg initial test dose, followed by full dose 2h later"
- **Animal study doses:** Include route and vehicle: "40 and 80 mg/kg IP (ibogaine in water, 10 mg/ml)"
- **Reviews discussing multiple ranges:** Summarise the range discussed

---

## Conventions
- **Thesis/book/book-chapter:** `document_type: thesis` (or `book`, `book-chapter`) pairs with the actual methodology as `evidence_level` (e.g., thesis doing a review → `evidence_level: review`; book synthesising qualitative and ethnographic material → `evidence_level: qualitative`). Not a mismatch.
- **Brief-communication:** `document_type: brief-communication` pairs with the actual methodology as `evidence_level` (e.g., brief communication reporting in-vitro data → `evidence_level: in-vitro`). Publication format ≠ evidence type.
- **Educational vs conference-talk:** `educational` = lectures, online courses, webinars, slide decks created with pedagogical intent (e.g., Malcolm's Psychedelic Pharmacology course). `conference-talk` = presentations delivered at named conferences or symposia (e.g., MAPS Psychedelic Science, Breaking Convention). The distinction is venue: a conference has a named event; educational content is course material. Both use the actual methodology as `evidence_level`.
- **Tag count (three-tier):**
  - **Standard (≤5):** Empirical papers — clinical-trial, case-report, case-series, in-vitro, preclinical, observational, qualitative, research-article, brief-communication.
  - **Synthesis (≤10):** Reviews, systematic-reviews, theses, guidelines, primary-sources, conference-talks, educational, interview-transcripts, commentaries, books, book-chapters, policy-reports. Cross-topic coverage is clinically valuable for these document types.
  - **Encyclopedic (named exceptions):** Alper2001 (16), Kobr2024 (14), Alfonso2023 (11). Comprehensive field reviews spanning ≥4 distinct domains. Adding new exceptions requires review.
  - The limit is a target, not a ceiling. Papers at limit+1 are acceptable when each tag maps to a distinct section of the paper. Limit+2 or more requires review.
- **Single source of truth:** Paper YAML is authoritative for all numerical claims (effect sizes, IC₅₀/Ki values, sample sizes, mortality counts). Hub documents synthesise and cite — they never introduce values absent from paper YAML. When the same value appears in both locations, the paper YAML governs. Effect sizes must specify timepoint and metric (e.g., `d=2.54 [1mo, PCL-5]`; `η²=0.414 [PCL-5]`). If a Hub value diverges from its source paper YAML, the Hub is wrong.

### Valid Enums

> Canonical source for all enums: `_meta/schema_registry.yml` | Verified: 2026-02-23

**evidence_level:** rct | cohort | case-series | case-report | in-vitro | preclinical | review | systematic-review | guideline | observational | qualitative | journalism | primary-source

**document_type:** clinical-trial | review | systematic-review | case-report | case-series | guideline | in-vitro | preclinical | observational | qualitative | commentary | book | book-chapter | thesis | primary-source | research-article | conference-talk | educational | interview-transcript | journalism | policy-report | brief-communication | industry-report

> ⚠️ **`research-article` is valid but non-specific.** It validates correctly but tells a clinician nothing about methodology. As of 2026-02-19, all papers have been disambiguated to specific types (Tier 1D complete). New conversions should always use the precise type — never default to `research-article`.

**route:** oral | intravenous | subcutaneous | intramuscular | intraperitoneal | topical | not-specified | not-applicable

---

## Category Decision

| If primary focus is... | Category |
|------------------------|----------|
| QTc, hERG, fatalities, cardiac AE, contraindications | RED |
| Screening, dosing, guidelines, clinical procedures | GREEN |
| Receptors, pharmacology, GDNF, noribogaine, 18-MC | ORANGE |
| Efficacy trials, outcomes, follow-up data | BLUE |
| Subjective experience, visions, integration | PURPLE |
| Bwiti, Lotsof, policy, traditional use, history | WHITE |

**Cardiac mention ≠ RED.** RED = paper's primary PURPOSE is cardiac safety evidence.
Paper mentions QTc incidentally? → Use primary category + `secondary_categories: [RED]`

---

## Canonical Tag Taxonomy (62 tags)

### topic/ (39)
topic/18-mc · topic/adverse-event · topic/alcohol · topic/analogues · topic/assessment · topic/benzodiazepine · topic/cardiac · topic/cognition · topic/combination · topic/cyp2d6 · topic/dopamine · topic/efficacy · topic/electrolytes · topic/gdnf · topic/harm-reduction · topic/history · topic/mechanism · topic/motor · topic/multiple-sclerosis · topic/neuroimaging · topic/neuroplasticity · topic/noribogaine · topic/opioid · topic/parkinsons · topic/pharmacokinetics · topic/phenomenology · topic/policy · topic/protocol · topic/psychiatric · topic/ptsd · topic/receptor · topic/serotonin · topic/sleep · topic/stimulant · topic/tbi · topic/toxicity · topic/traditional-use · topic/veterans · topic/withdrawal

### mechanism/ (10)
mechanism/dopamine-modulation · mechanism/energy-metabolism · mechanism/herg-blockade · mechanism/ion-channel · mechanism/kappa-opioid · mechanism/mu-opioid · mechanism/nicotinic-receptor · mechanism/nmda-antagonism · mechanism/sert-inhibition · mechanism/sigma-receptor

### method/ (11)
method/case-report · method/case-series · method/clinical-trial · method/in-vitro · method/journalism · method/observational · method/preclinical · method/proteomics · method/qualitative · method/review · method/systematic-review

### meta/ (2) — vault structure only, never research papers
meta/hub · meta/moc

---

## Exemplar YAML by Category

### RED — Fatality Case Report
```yaml
category: RED
tags:
  - topic/adverse-event
  - topic/pharmacokinetics
  - topic/noribogaine
  - method/case-report
evidence_level: case-report
sample_size: 1
mortality_count: 1
qtc_data: false
electrolyte_data: false
herg_data: false
contraindications:
  - "Unsupervised root bark ingestion"
  - "Concomitant drug abuse history"
  - "Absence of medical monitoring"
dosing_range: "unknown (root bark, ~18 spoonfuls over ~10 hours, blood levels 5–20× therapeutic)"
route: oral
clinical_significance: high
```

### GREEN — Clinical Guideline
```yaml
category: GREEN
tags:
  - topic/protocol
  - topic/cardiac
  - topic/electrolytes
  - topic/harm-reduction
  - method/review
evidence_level: guideline
qtc_data: true
electrolyte_data: true
herg_data: false
contraindications:
  - "Active cardiac disease or QTc prolongation"
  - "Concurrent use of QT-prolonging medications"
  - "Hepatic impairment"
  - "Active psychosis or severe psychiatric instability"
  - "Pregnancy or breastfeeding"
  - "Concurrent opioid agonist use without adequate taper"
  - "Epilepsy or seizure disorders"
  - "Cerebellar dysfunction"
  - "Concurrent use of CYP2D6 inhibitors"
dosing_range: "10–25 mg/kg oral (HCl equivalent); test dose protocol recommended"
route: oral
clinical_significance: landmark
```

### BLUE — Cohort Study
```yaml
category: BLUE
tags:
  - topic/tbi
  - topic/ptsd
  - topic/efficacy
  - topic/cardiac
  - method/clinical-trial
secondary_categories: [RED, GREEN]
evidence_level: cohort
sample_size: 30
qtc_data: true
electrolyte_data: true
herg_data: false
contraindications:
  - "Cardiac abnormalities on screening ECG"
  - "Concurrent psychiatric medications without taper"
  - "Active substance use disorder"
dosing_range: "12 mg/kg oral (ibogaine HCl) + magnesium co-administration"
route: oral
clinical_significance: landmark
```

### ORANGE — In-vitro Receptor Study
```yaml
category: ORANGE
tags:
  - topic/receptor
  - topic/cardiac
  - mechanism/herg-blockade
  - method/in-vitro
evidence_level: in-vitro
qtc_data: false
electrolyte_data: false
herg_data: true
contraindications: []
clinical_significance: high
```

### PURPLE — Qualitative Experience Study
```yaml
category: PURPLE
tags:
  - topic/phenomenology
  - topic/opioid
  - method/qualitative
evidence_level: qualitative
sample_size: 12
qtc_data: false
electrolyte_data: false
herg_data: false
contraindications: []
clinical_significance: moderate
```

### WHITE — Historical/Policy
```yaml
category: WHITE
tags:
  - topic/history
  - topic/policy
  - topic/harm-reduction
  - method/review
evidence_level: review
document_type: policy-report
qtc_data: false
electrolyte_data: false
herg_data: false
contraindications: []
clinical_significance: moderate
```

---

## Document Body Template

```markdown
# [Paper Title]

**Citation:** Authors (Year). Title. *Journal*, Volume(Issue), Pages. DOI

## Abstract
[Full abstract — not summarised. Preserve all numerical values.]

## Key Findings
[Main findings with clinical relevance. Include specific numbers, effect sizes, CIs.]

## Methodology
[Study design, sample characteristics, measurement tools, statistical approach]

## [Topic-Specific Sections]
[Adapt to paper content:]
[- "Cardiac Safety Data" for RED]
[- "Dosing Protocol" for GREEN]
[- "Receptor Binding Data" for ORANGE]
[- "Treatment Outcomes" for BLUE]
[- "Experience Reports" for PURPLE]
[- "Historical Context" for WHITE]
[Reproduce data tables accurately from PDF]

## Clinical Implications
[RED/GREEN/BLUE: Connect to Pangea screening, monitoring, dosing, discharge decisions]
[ORANGE: Mechanistic significance for treatment development]
[PURPLE: Integration practice implications]
[WHITE: Historical/policy context for the field]

## Limitations
[As noted by authors — don't invent additional ones]

---

## See Also
- [[Year/Related_Paper]] — minimum 2, aim for 3-5
- [[Relevant_Hub]]
```

---

## File Placement

| Type | Location |
|------|----------|
| Academic paper | `YYYY/` (from vault root) |
| Primary source | `Primary_Sources/` |
| Non-research primary source | `_archive/primary-sources/` |
| Guideline | `Clinical_Guidelines/` |
| Other | `Other/` |

**Filename:** `AuthorYear_Brief_Topic.md` (e.g., `Cherian2024_Magnesium_Ibogaine_TBI.md`)

---

## Known PDF-to-Markdown Damage Patterns

Reference for auditing or restoring papers converted before 2024. See `archive/audit_phase2_progress_COMPLETE.md` for full detail.

### Damage Types

| Type | Example | Grep-Visible? |
|------|---------|---------------|
| Empty `()` brackets | `nAChRs ()` → `nAChRs (α3β4, α4β2, α7)` | ✅ |
| Stripped IC₅₀/EC₅₀/Kᵢ labels | `, hSERT = 280 nM` → `IC₅₀, hSERT = 280 nM` | ❌ |
| Stripped superscripts | `[H]` → `[³H]` | ❌ |
| Missing units | `14.6` → `14.6 μM` | ❌ |
| Missing Greek/symbols | `Cmax` → `C_max`; `FosB` → `ΔFosB` | ❌ |
| Missing receptor names | `opioid receptors` → `κ opioid receptors` | ❌ |
| Empty table cells | Entire data columns blank | Partially |
| Stripped `(; )` content | `(; )` → `(log ε 4.28; 3.78)` | ❌ |
| Corrupted µ encoding | `lg/mL` or `mg/mL` when should be `µg/mL` | ❌ |

### Multiplier Heuristic (grep `()` hits → actual restorations)

| Paper Type | Expected Multiplier |
|------------|-------------------|
| Behavioural/in vivo | 1× |
| Experimental receptor pharmacology | 2–3× |
| Dense IC₅₀/Kᵢ papers | 5× |
| Comprehensive receptor reviews | 10×+ |
| Phytochemistry with data tables | 20× |

### Limitations

- **Grep catches `()` but not silent deletions.** Entire parenthetical expressions can vanish without leaving bracket traces. A PDF-vs-markdown comparison is the only definitive check.
- **Post-2024 AI-summarised conversions are immune** — 0% stripping rate. Issue is exclusively in early verbatim PDF-to-text extraction.

### Spot-Check Backlog

4 early-restored papers may have residual non-`()` damage (restored before multiplier patterns were discovered): Gonzalez2018, Bhat2020, Cachat2013, Glick2000. Papers with receptor binding data or isotope labels are highest risk.

---

## Pre-Completion Checklist

### Structural
- [ ] YAML parses (no blank line after opening `---`)
- [ ] Tags in list format (never inline array), no `#` prefix
- [ ] `secondary_categories` in INLINE format `[RED, BLUE]` — never multi-line list (D12)
- [ ] `publication_date` quoted when present — `"2024-03-15"` not bare date (D13)
- [ ] Category is exactly one of the six
- [ ] All tags from canonical 62-tag list
- [ ] key_findings ≤250 characters
- [ ] File in correct folder
- [ ] `document_type` is precise — never `research-article` for new conversions

### Boolean & Clinical Fields
- [ ] `qtc_data`: set true/false — checked for QTc thresholds in exclusion criteria?
- [ ] `electrolyte_data`: set true/false — checked for Mg²⁺/K⁺ protocols, not just explicit headers?
- [ ] `herg_data`: set true/false — original assay data only, not cited results?
- [ ] `contraindications`: populated list OR `[]` — searched all 8 extraction locations?
- [ ] `evidence_level`: matches actual methodology (in-vitro ≠ preclinical)
- [ ] Optional fields omitted correctly (no empty strings, no fabricated dates, no zeros)

### Category-Specific
- [ ] **RED?** → `mortality_count` set if ≥1 death. `dosing_range` populated (even "unknown — [context]"). `route` populated
- [ ] **GREEN?** → `dosing_range` populated (MANDATORY). `route` populated (MANDATORY). Contraindications comprehensive
- [ ] **Human study?** → `sample_size` populated as integer
- [ ] **Non-human study?** → `sample_size` omitted
- [ ] **Review tabulating fatalities?** → `mortality_count` with accurate tally
- [ ] **Fatality case?** → All circumstantial data captured (substances, monitoring status, medical history)

### Cross-References & Data Integrity
- [ ] ≥2 See Also wikilinks (aim for 3-5)
- [ ] Relevant Hub linked (verified filename exists in vault)
- [ ] Related papers by same author group linked where they exist
- [ ] Numerical values cross-checked against PDF (concentrations, p-values, effect sizes)
- [ ] Tables reproduced accurately (no empty cells, no swapped columns)
- [ ] Species names in italics, chemical nomenclature correct
- [ ] PDF damage patterns checked (see Damage Types table above)

---

## Schema Decision Log

Decisions applied to vault schema. Each decision has been propagated to all downstream consumers per the [propagation checklist](_meta/prompts/schema_decision_propagation_checklist.md).

| ID | Date | Decision | Propagated To |
|----|------|----------|---------------|
| D11 | 2026-03-11 | `related_papers` field removed from schema | Papers (14 files) |
| D12 | 2026-03-11 | `secondary_categories` normalised to inline format `[RED, GREEN]` | Papers (117 files), manifest schema example + exemplars, pre-completion checklist |
| D13 | 2026-03-11 | `publication_date` quoted as `"YYYY-MM-DD"` | Papers (79 files), manifest schema + field omission rules, registry format note, pre-completion checklist |
| D14 | 2026-03-11 | `source`/`status` fields removed from schema | Papers (34 files) |
| D15 | 2026-03-11 | `primary-source` added to `evidence_level` enum | Registry, manifest enum list, validate_yaml.py `VALID_EVIDENCE_LEVELS`, papers (11 files) |
| D16 | 2026-03-11 | `pmid`, `pmcid`, `isbn`, `issn` added as optional academic identifier fields | Registry (optional fields), manifest (schema example + field omission rules), validate_yaml.py `ALL_VALID_PAPER_FIELDS`. Data population deferred — schema definition is immediate |

> **Adding new decisions:** Use the [Schema Decision Propagation Checklist](/Users/aretesofia/IbogaineVault/_meta/prompts/schema_decision_propagation_checklist.md) to ensure all downstream consumers are updated atomically.
