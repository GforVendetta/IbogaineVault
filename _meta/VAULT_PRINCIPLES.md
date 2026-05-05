---
title: "Vault Principles"
tags:
  - meta
aliases: ["Principles", "Design Philosophy"]
---

# Vault Principles

> The IbogaineVault exists because ibogaine research is scattered across decades, disciplines, and continents. These principles ensure that when evidence is organised, nothing safety-critical is lost, obscured, or misrepresented.

**Purpose:** The principles governing quality, consistency, and clinical integrity across the IbogaineVault. These are not aspirational — they describe what the vault already does, made explicit so that contributors and collaborators maintain the standard.

---

## Clinical Principles

### 1. Evidence Hierarchy

The vault represents all evidence levels — from randomised controlled trials to individual case reports to preclinical studies — and labels each one explicitly via the `evidence_level` YAML field. Higher-quality evidence (RCTs, systematic reviews) carries more weight in clinical synthesis, but lower-quality evidence is never excluded.

Case reports are critical for adverse event documentation where controlled trials do not exist. Preclinical data provides mechanistic context that informs clinical reasoning. The hierarchy is descriptive, not exclusionary.

**Why this matters:** Ibogaine research spans seven decades with very few RCTs. Discarding case reports would eliminate most of the safety evidence base. The vault makes the evidence level visible so that readers can calibrate their confidence appropriately.

### 2. Cardiac Safety Primacy

RED-category papers (cardiac safety, fatalities, adverse events) receive the most rigorous classification and metadata treatment. This is not a hierarchy of importance between categories — it reflects the consequence of error.

A miscategorised cardiac safety paper can mean that a clinician performing a pre-treatment literature search fails to find critical safety evidence. In ibogaine treatment, that failure mode can be fatal. Every paper reporting cardiac outcomes, QTc prolongation, hERG channel data, or treatment-associated deaths must be accurately classified as RED primary or flagged with `secondary_categories: [RED]`.

**Why this matters:** The vault originated from a commitment to ensure that no one dies from ibogaine treatment due to inaccessible or disorganised safety evidence.

### 3. Category Co-equality

All six categories (RED, GREEN, ORANGE, BLUE, PURPLE, WHITE) serve different functions within the same research instrument. None is subordinate. Each answers a clinical or research question the others cannot:

- **RED** documents how ibogaine can kill — cardiac risk, fatality patterns, adverse events. It answers: *what can go wrong, and how do we prevent it?*
- **GREEN** captures the protocols, guidelines, and screening procedures that translate research into clinical practice. It answers: *how should ibogaine be administered safely?* A GITA guideline or a dosing protocol is not a research paper — it is the bridge between evidence and practice, and the vault treats it as such.
- **ORANGE** maps the pharmacological mechanisms — receptor binding, GDNF expression, noribogaine metabolism, 18-MC analogues. It answers: *why does ibogaine work, and how might it be improved?*
- **BLUE** records clinical outcomes and efficacy data — trials, observational studies, veterans and TBI cohorts. It answers: *does ibogaine treatment produce measurable benefit?*
- **PURPLE** documents the subjective experiences that distinguish ibogaine from other anti-addiction interventions — visionary states, therapeutic process, the Ibogaine Experience Scale. It answers: *what happens to the person during treatment, and how does that relate to outcomes?*
- **WHITE** preserves the historical, traditional, and policy context without which the field cannot be understood — Bwiti practice, the Lotsof discovery narrative, scheduling decisions. It answers: *how did we get here, and what institutional forces shape the field?*

A vault that deprioritises phenomenology or history is a lesser research tool, not a more focused one.

**Why this matters:** Ibogaine sits at the intersection of pharmacology, clinical medicine, lived experience, traditional use, and drug policy. No single disciplinary lens captures the full picture.

### 4. Conservative Classification

When a paper's category assignment is ambiguous, the vault classifies towards safety. This applies across all category boundaries, not only RED:

- **Safety direction:** A mechanisms paper that incidentally reports a death should carry `secondary_categories: [RED]`. A cardiac safety paper miscategorised as mechanisms is a missed warning; a mechanisms paper flagged RED is a minor redundancy.
- **Protocol direction:** A dosing study that primarily establishes a treatment protocol belongs in GREEN, even if it reports efficacy outcomes that would fit BLUE. The protocol is what clinicians will search for.
- **Outcomes vs phenomenology:** A qualitative study reporting treatment outcomes alongside experiential accounts is BLUE if the outcomes data is its principal contribution, PURPLE if the experiential analysis is primary. When genuinely balanced, classify as BLUE with `secondary_categories: [PURPLE]` — outcomes data has more direct clinical utility.

The cost of false negatives in safety and protocol classification is measured in lives. The cost of false positives is measured in an extra row in a database query. The vault's classification practice reflects this asymmetry.

### 5. Transparency About Limitations

The vault is evidence synthesis — not medical advice and not a substitute for reading primary sources. Limitations of individual studies are noted in each paper's structured summary. Gaps in the evidence base are documented, not hidden. Where the vault draws interpretive connections between papers (in Hubs and MOCs), those connections are clearly distinguished from the primary evidence.

The vault does not make treatment recommendations. It organises and surfaces the evidence from which treatment decisions can be informed.

### 6. Temporal Evidence and the Evolution of Understanding

The vault spans 1957–2026. A 1962 Naranjo case report and a 2025 Cherian RCT coexist within the same structure. The vault preserves the *evolution* of understanding rather than presenting only the current consensus.

Superseded findings are not removed or annotated as incorrect — they remain in the vault with their original evidence level and classification. A 2001 review estimating fatality rates from limited data is not wrong; it was the best available synthesis at the time. A 2024 analysis with a larger dataset does not invalidate the earlier work — it extends it. Both are present, both are labelled, and the Hubs provide narrative context explaining how the field moved from one understanding to the next.

This is particularly important for ibogaine's paradigm shift from cardiac risk *management* (monitoring and screening to reduce harm) to cardiac risk *elimination* (magnesium co-administration protocols that may abolish QTc prolongation). The vault represents both paradigms without retroactively delegitimising the earlier approach that kept patients alive for two decades.

**Why this matters:** A research instrument that only presents current knowledge is a textbook. The vault is a history of evidence — it shows not just what we know, but how we came to know it. For a field as young and contested as ibogaine science, that trajectory is itself evidence.

---

## Methodological Principles

### 7. Single Source of Truth

Every classification, field definition, and evidence label used in this vault derives from a single authoritative schema (`schema_registry.yml`). When multiple documents reference the same concept — an evidence level, a category definition, a tag meaning — they all derive from the same source.

This prevents the silent drift that occurs when parallel definitions evolve independently. In a safety-critical context, that drift could mean that "systematic-review" carries different implications on different papers, or that a category boundary shifts without anyone noticing. One schema governs the entire vault.

**Why this matters:** Before the schema registry existed, four files defined enums independently and drifted apart. The single-source pattern eliminated an entire class of errors.

### 8. Provenance and Traceability

Archived artefacts include enough context to be understood without archaeology. When papers are reclassified, when metadata is corrected, when a category assignment changes — the audit trail preserves both the change and its rationale. Filenames are descriptive. Archived content carries context about what it was and why it was superseded.

**Why this matters:** A research instrument that cannot account for its own editorial history cannot be trusted. Provenance ensures that any claim about how many papers the vault contains, or how they are categorised, can be verified against the historical record.

### 9. Representational Accuracy

The vault does not create false impressions of evidence that does not exist. Empty categories are not padded. If a year folder contains three papers, it contains three papers — not a placeholder suggesting more. Stale data files are either updated or clearly marked as superseded. Paper counts use approximate language ("over 300 papers") rather than brittle exact numbers, unless the context demands precision.

**Why this matters:** A researcher browsing the vault forms expectations based on its structure. An empty folder implies missing content; a stale count implies more or fewer papers than exist. Representational accuracy is a prerequisite for the vault to function as a trustworthy research instrument.

### 10. Meta-Tooling Deprecation Discipline

Research papers in this vault are bounded by a clear scope test: is this study about ibogaine? Tools in `_meta/tools/` are bounded by use: if no workflow runs a script, it is archived. Meta-documentation — progress trackers, session logs, amendment catalogues, process registers, self-describing sub-programmes — has no equivalent natural constraint. It does not fall out of scope because its own existence creates its scope. It does not fall out of use because it is the thing tracking use. Unpruned, it grows indefinitely.

The vault therefore treats its meta-layer as requiring explicit deprecation discipline that content and code do not need. At the close of every phase and at each v1.x release, meta-documents are evaluated for retirement. If a tracker has produced an insight worth keeping, the insight is extracted into a permanent document — a change-log note, a principle, a schema comment — and the tracker is archived. If no such insight exists, the tracker is archived with a note explaining why it did not earn a permanent place. The default state of meta-tooling is deprecation; survival is the exception that requires justification.

A meta-document whose existence is justified by problems the meta-layer itself generated is itself a deprecation signal. When a tracker produces a sub-tracker, or a register begins to track its own state, the correct response is to archive the subtree and return to the original work it was meant to support.

**Why this matters:** Locally rational additions to meta-infrastructure compound into globally irrational ceremony. A process register, an amendment catalogue, a progress tracker, a session log — each addition defensible in isolation; collectively they become paralysing. Without deliberate deprecation, the scaffold outgrows the building. For a vault whose legitimacy depends on producing accurate evidence synthesis at clinical pace, ceremony is not free — it displaces the work it is meant to organise.

### 11. Transparent Flagging of Editorial Judgement

The vault makes editorial decisions that cannot be fully mechanised: whether a borderline paper belongs in the corpus, whether a category boundary is crossed, whether a secondary category is warranted, whether an interpretation in a hub is supported by the underlying papers. These are assessments, not verdicts — and they are flagged as such.

The vault prefers the language of *assessment* over *judgement*: an assessment is provisional, evidenced, and open to revision; a judgement claims authority the vault does not possess. Where an editorial decision is non-obvious — a paper at the margin of inclusion, a category assignment that could plausibly go two ways, an interpretive claim in a hub that extends beyond any single source — the vault presents the evidence that informed the decision, the reasoning applied, and the remaining uncertainty explicitly. The reader is left to agree, disagree, or refine.

This principle forbids two failure modes. The first is hidden adjudication: quietly including or excluding papers without flagging the borderline status, so that the vault appears more settled than it is. The second is false certainty: presenting an interpretive synthesis as if it were derivable from the primary evidence when it depends on editorial inference.

**Why this matters:** A vault that hides its own editorial reasoning cannot be audited. A collaborator — now or in five years — must be able to see which decisions were difficult, what evidence was weighed, and where the editor was uncertain. Transparent flagging makes the vault's epistemic state legible, and legibility is a prerequisite for trust in any research instrument maintained by a single curator.

---

## Applying These Principles

Contributors and collaborators working with the vault should verify:

- **Evidence integrity:** Do cardiac safety papers have correct RED classification? Are `secondary_categories` applied where a paper spans domains?
- **Evidence levels:** Does the `evidence_level` field match the source methodology? A non-randomised open-label study is a cohort study, not an RCT.
- **Schema compliance:** Do YAML fields and values match `schema_registry.yml`? Undefined fields and non-canonical enum values break downstream queries.
- **Structural honesty:** Are there empty directories, unreferenced files, or placeholder content that implies evidence not yet present?
- **Link integrity:** Do cross-references point to papers and hubs that exist? Dead links in a research instrument signal unreliable organisation.

---

**See also:** [Vault Architecture](VAULT_ARCHITECTURE.md) · [Methodology](METHODOLOGY.md) · [Tag Taxonomy](Tag_Taxonomy.md) · [Schema Registry](_meta/schema_registry.yml)
