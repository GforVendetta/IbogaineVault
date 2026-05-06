---
title: "Methodology"
tags:
  - meta
aliases: ["Methodology", "Conversion Methodology"]
---

# Methodology

> How the IbogaineVault transforms source publications into a structured, queryable research instrument. For the architecture that organises the result, see [Vault Architecture](VAULT_ARCHITECTURE.md). For the principles governing quality and classification, see [Vault Principles](VAULT_PRINCIPLES.md).

---

## Source Material and Scope

The vault contains over 300 publications spanning 1957–2026. Source material includes peer-reviewed journal articles, clinical guidelines, case reports, systematic reviews, book chapters, PhD theses, regulatory documents, conference proceedings, investigative journalism, and primary-source interviews.

Papers are identified through systematic literature searches, citation chaining from key reviews, clinical practice knowledge contributed by collaborators with direct ibogaine treatment experience, and contributions from researchers in the field. The vault does not apply formal inclusion/exclusion criteria in the manner of a systematic review (see [Limitations](#limitations-and-known-constraints)). Instead, it aims to be comprehensive within its scope: any publication that contributes evidence relevant to ibogaine science — from a 1962 Naranjo case series to a 2026 randomised controlled trial — belongs in the vault if it can be located and converted.

What the vault excludes is equally important: it does not contain unpublished clinical data, proprietary treatment protocols, or patient-level information. Every paper in the vault derives from a published or publicly accessible source. The `evidence_level` field (defined in `schema_registry.yml`) makes the methodological quality of each study explicit — from `rct` through `case-report` to `journalism` — so that readers can calibrate their confidence without the vault needing to exclude lower-quality evidence.

---

## Conversion Process

Converting a publication into a vault paper is analytical synthesis, not transcription. Each paper is read in full, understood as a contribution to ibogaine science, and re-expressed in a consistent analytical framework that does not exist in the source material.

### Structured Metadata

Every paper carries YAML frontmatter with 15 required fields populated directly from the publication — not inferred or assumed. These include bibliographic data (authors, year, journal, DOI), classification data (category, evidence level, clinical significance), and clinical safety fields (boolean flags for QTc data, hERG data, and electrolyte data; contraindications; dosing range and route where applicable). The authoritative field definitions live in `schema_registry.yml`. Conditional fields such as `mortality_count` and `mortality_scope` are required when a paper reports fatalities, ensuring that mortality data is both captured and contextualised.

### Analytical Body Format

Papers in the vault's analytical format are structured with Key Findings, Clinical Implications, and Limitations sections that synthesise the publication's contributions in the vault's own analytical voice. This format foregrounds clinical utility: a researcher or clinician reading a vault paper encounters the study's principal findings, their implications for treatment practice, and their methodological constraints — in that order.

A subset of papers retain their original academic structure (Introduction, Methods, Results, Discussion) — these are labelled `body_format: academic-retained` in the YAML metadata. The v1.1 programme extends analytical-format coverage across the vault; both formats coexist during this transition.

### Cross-Referencing

Each paper includes markdown links to related publications, connecting studies that build on, contradict, or extend each other. These links appear in the body text where the relationship is discussed and in a See Also section that maps the paper's position within the broader literature. The result is a navigable research graph rather than a flat collection of summaries.

---

## Copyright Compliance

The vault synthesises published research into a structured instrument. This section describes how that synthesis is conducted to ensure that vault papers are non-displacive — designed to make readers want to consult the source publication, not substitute for it.

### The Core Principle

Papers in the vault's analytical format are rewritten, not reproduced. The conversion process involves reading the source PDF, understanding its contribution, and re-expressing the findings, data, and clinical implications in the vault's own analytical voice. The source text is not quoted at length, paraphrased closely, or structurally mirrored. Each vault paper adds interpretive structure — Key Findings, Clinical Implications, cross-references to related work — that does not exist in the source material.

### Licence-Aware Posture

Every paper carries a `licence_type` field classifying its copyright terms. This classification determines the degree of textual transformation required during conversion:

- **Restrictive** (`all-rights-reserved`, `unknown`): Full analytical rewrite. The source text is read, understood, and the vault paper is written from comprehension rather than reference. Papers with unknown licence status are treated as restrictive — copyright caution is never relaxed without a confirmed licence.
- **Moderate** (`cc-by-nc-nd`, `cc-by-nd`): Analytical format preferred for clinical utility. The vault's operating interpretation is that analytical summaries for scholarly research constitute scholarly review, not adaptation under ND (no-derivatives) terms. This position is defensible and widely held but not universally settled. Every moderate-posture paper is written to survive a downgrade to restrictive without data loss.
- **Permissive** (`cc-by`, `cc-by-sa`, `cc-by-nc`, `cc-by-nc-sa`): Analytical format preferred. Reproduction is licence-permitted, but the vault uses its analytical voice for consistency and clinical utility.

A `licence_verified` boolean records whether the licence was confirmed from the paper's own licence statement (true) or inferred from publisher-level patterns (false). This two-field system makes the copyright posture both explicit and auditable.

### Numerical Fidelity

While text is rewritten, quantitative data must be preserved exactly. Sample sizes, p-values, dosing ranges, QTc intervals, IC₅₀ values, and mortality counts are never rounded, approximated, or paraphrased. A fidelity audit tool verifies numerical accuracy against source PDFs, checking that the vault paper's abstract matches the source abstract and that reported numbers are grounded in the original publication.

### N-gram Validation

Automated n-gram analysis measures textual overlap between vault papers and their source PDFs. The primary metric is 4-gram overlap — the proportion of four-word sequences in the vault paper that also appear in the source. Thresholds are posture-dependent: restrictive papers target scores below 0.20, moderate papers below 0.40, and permissive papers are measured but not gated. Papers exceeding their threshold are flagged for further rewriting. Scores above 0.35 trigger full reconversion regardless of posture.

This is a systematic, auditable process. Every converted paper can be scored against its source, and the results are reproducible.

### What the Vault Reproduces

Vault papers may contain standardised terminology, chemical nomenclature, study metadata (author lists, journal names, DOIs), and tables of extracted quantitative data (dosing ranges, fatality summaries, receptor binding affinities). These are factual elements that do not raise copyright concerns. Brief direct quotations, where they appear, are clearly attributed and used sparingly — particularly in phenomenology papers where participant language carries irreplaceable first-person data.

### Source Access

Each paper's YAML includes DOI, PMID, and/or PMCID fields linking to the original publication. The vault is a structured index that directs readers to sources, not a replacement for reading them.

### Methodology Development

The copyright compliance infrastructure described above — licence-aware posture classification, n-gram validation, fidelity auditing, and the reconversion pipeline — was formalised during 2025–2026 as the vault matured from a working collection into a citable research instrument. Earlier conversions predated these systems and were produced under less formal copyright discipline. A vault-wide copyright audit has identified papers requiring reconversion to meet current standards, and a systematic reconversion programme is applying these methods retroactively, prioritised by clinical urgency (cardiac safety first, then protocols, outcomes, mechanisms, phenomenology, and historical context). The `body_format` field in each paper's YAML tracks whether it has been converted to the vault's analytical format or retains its original academic structure.

---

## Quality Assurance

The vault maintains zero validation errors across its entire paper collection. This is achieved through layered automated checks, not manual review alone.

### Automated Validation

`validate_vault.py` runs against every paper, checking YAML schema compliance (field presence, type correctness, enum membership), tag taxonomy conformance (all tags must exist in the 66-tag canonical taxonomy), structural integrity (required sections present, no orphaned metadata), and cross-file consistency. The validator is the final gate — no paper enters the vault with a validation error.

### Reconversion Verification

Papers undergoing format conversion pass through an eight-check automated validator: structural integrity (no residual academic headings), YAML compliance (correct body format, boolean flags, licence metadata), tag audit (canonical taxonomy, count policy), wikilink preservation (no cross-references lost), proof-of-reading verification (confirming the source PDF was consulted), n-gram copyright analysis (textual overlap scoring), numerical fidelity audit (abstract and data verification against source), and full vault validation. Each check produces a PASS, WARN, or FAIL result with actionable detail.

### Cross-Model Verification

The automated validators described above confirm structural, schema, copyright, and numerical integrity — but they cannot detect a specific class of error that the vault-analytical reconversion process is structurally vulnerable to. Analytical generation errors occur when the vault body reads as plausible and internally consistent but silently omits, reframes, or distorts findings present in the source publication. Such text passes structural, schema, tag, and n-gram checks while being wrong. The cross-model verification programme addresses this gap and stands alongside automated validation, reconversion verification, and cross-paper consistency as a dedicated quality pillar.

The protocol pairs two uncorrelated AI model families. One model performs a blind extraction of the source PDF against a structured extraction prompt — no vault context, no vault markdown, no error taxonomy loaded into the extraction session. A fresh session of a different model family then compares the blind extraction against the vault entry, flagging discrepancies into three buckets: vault error (vault says X, paper says Y, extraction confirms Y), source inconsistency (paper itself is internally inconsistent, extraction flagged it, vault smoothed over it), and extraction artefact (extraction misread the PDF, vault is correct). All vault errors require source-PDF verification before correction.

This approach is designed to break a structural verification limitation: same-model verification has near-zero discriminative power for the most dangerous error types, because the verifier and the system under test share identical failure modes. A fabricated methodology term generated from one model's distributional priors sounds right to a verifying instance of the same model for exactly the same reason it was generated. This is not psychological confirmation bias; it is a property of verifiers sharing training distribution with the generator. A different model family has different training data, different distributional priors, different tokenisation, and different attention patterns — its extraction errors are uncorrelated with the first model's errors, so discrepancies become visible rather than systematically confirmed. The principle is the same as ensemble methods in machine learning: two models with uncorrelated error distributions provide stronger coverage than two passes from the same model.

Extraction and comparison prompts are branched by paper genre (cardiac safety and mortality papers, clinical protocol papers, mechanism papers — preclinical, in-vitro, review, observational) to reflect genre-specific error patterns, with retention checklists encoding the empirically validated omission categories for each genre. Categories are promoted from single-paper observation to confirmed pattern only when independently confirmed across structurally diverse papers. The programme runs in waves aligned with clinical priority and is progressively closing the verification perimeter across the clinical-decision-support subset of the vault.

### Cross-Paper Consistency

Mortality data illustrates the vault's approach to cross-paper integrity. Each paper reporting fatalities carries both a `mortality_count` and a `mortality_scope` field. The scope distinguishes cumulative reviews (which tally deaths across the literature) from discrete cases (individual incidents) and incidental mentions. This prevents the naïve-summation error — adding 38 deaths from a cumulative review to 3 deaths from a case report that the review already includes — which would overcount the evidence base.

### Continuous Integration

GitHub Actions validate pull requests against the schema before merge. This provides a pre-merge safety gate ensuring that no paper enters the public repository with structural errors, non-canonical tags, or missing required fields.

---

## AI-Assisted Methodology

The vault is built using AI-assisted knowledge architecture. Claude (Anthropic) serves as a conversion tool — reading PDFs, extracting metadata, drafting analytical summaries, identifying cross-references, and running automated validation — under human direction and verification.

This is analogous to computational biology pipelines that use automated tools for data processing while relying on domain expertise for interpretation. The sequencer produces reads; the biologist interprets the genome. Similarly, the AI drafts structured summaries from source PDFs; humans with clinical and research expertise make the classification decisions, verify clinical accuracy, and determine how papers relate to each other within the broader evidence landscape.

What the AI does not do is equally important. Category assignment, cardiac safety classification, clinical significance ratings, contraindication identification, and the interpretive connections drawn in Hubs and MOCs — these are human decisions informed by clinical expertise and deep familiarity with the literature. The AI proposes; humans decide.

Making this methodology explicit serves transparency. AI-assisted research tools are novel, and readers should be able to calibrate their trust appropriately. The vault's reliability is determined by its validation infrastructure, its copyright compliance methodology, and the clinical oversight governing its editorial decisions — not by the tools used to build it.

---

## Limitations and Known Constraints

The vault is evidence synthesis — not a systematic review, not medical advice, and not a substitute for reading primary sources. These limitations are structural, not temporary.

**Not a systematic review.** The vault does not follow PRISMA or equivalent protocols. There is no pre-registered search strategy, no formal risk-of-bias assessment per paper, and no meta-analytic pooling of outcomes. The vault's value lies in comprehensive organisation and clinical synthesis, not in the methodological guarantees that a systematic review provides. Researchers conducting formal reviews should use the vault as a discovery tool and citation resource, not as a replacement for their own systematic search.

**Single-contributor knowledge architecture.** The vault was built by a single knowledge architect in collaboration with clinical practitioners. This means that analytical summaries represent one informed reading of each paper. Other interpretations are valid, and the structured metadata enables readers to locate papers and form their own assessments. Expansion of the contributor base is planned.

**English-language constraint.** The vault covers English-language publications, with noted exceptions for historically significant non-English sources. Ibogaine research published in French, Spanish, Portuguese, and other languages is not systematically represented.

**Living document.** The vault is not a fixed publication. Papers may be updated as new evidence emerges, as errors are identified, or as format standards evolve. The version-controlled git history provides a complete audit trail of every change.

**Coverage gaps.** A small number of identified publications have not yet been converted. These are documented in the vault's gap analysis and are being addressed in the v1.1 development programme.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1 | 2026-03-26 | Initial methodology statement. Covers source scope, conversion process, copyright compliance (licence-aware posture, n-gram validation, numerical fidelity), quality assurance (8-check validator, CI), AI-assisted methodology, and limitations. |
| v2 | 2026-04-17 | Added Cross-Model Verification as a quality assurance pillar. Describes the two-uncorrelated-model-families protocol, the structural limitation it addresses (same-model verification shares failure modes with the system under test), genre-branched prompts by paper type, and the n=2 rule for promoting observed patterns to confirmed error categories. Parallel to Tier 2 v3; Tier 1 version omits internal tool paths and project-specific references for external audiences. |

---

**See also:** [Vault Architecture](VAULT_ARCHITECTURE.md) · [Vault Principles](VAULT_PRINCIPLES.md) · [Schema Registry](_meta/schema_registry.yml) · [Tag Taxonomy](Tag_Taxonomy.md)
