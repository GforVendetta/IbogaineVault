# Tag Taxonomy

**62 canonical tags** organised by namespace. Use these when filtering in Bases or understanding paper classifications.

> Canonical source: `_meta/schema_registry.yml` | Verified: 2026-02-23

---

## Topic Tags (39)

| Tag | Meaning |
|-----|---------|
| `topic/18-mc` | 18-methoxycoronaridine analogue research |
| `topic/adverse-event` | Side effects, complications, negative outcomes |
| `topic/alcohol` | Alcohol use disorder, alcohol dependence |
| `topic/analogues` | Ibogaine derivatives, synthetic analogues |
| `topic/assessment` | Screening tools, questionnaires, scales |
| `topic/benzodiazepine` | Benzodiazepine use as adjunct, GABAergic safety, withdrawal seizure management |
| `topic/cardiac` | Heart-related effects, cardiovascular |
| `topic/cognition` | Cognitive effects, memory, attention |
| `topic/combination` | Multi-substance protocols, drug combinations |
| `topic/cyp2d6` | CYP2D6 metabolism, pharmacogenomics |
| `topic/dopamine` | Dopamine system, reward pathways |
| `topic/efficacy` | Treatment effectiveness, success rates |
| `topic/electrolytes` | Magnesium, potassium, electrolyte management |
| `topic/gdnf` | Glial cell line-derived neurotrophic factor |
| `topic/harm-reduction` | Risk mitigation, safer use practices |
| `topic/history` | Historical context, timeline, origins |
| `topic/mechanism` | General mechanism discussions |
| `topic/motor` | Motor effects, tremor, ataxia |
| `topic/multiple-sclerosis` | MS-related research |
| `topic/neuroimaging` | fMRI, PET, brain imaging studies |
| `topic/neuroplasticity` | Neuroplasticity, synaptic remodelling, structural brain changes |
| `topic/noribogaine` | Noribogaine metabolite research |
| `topic/opioid` | Opioid use disorder, opioid withdrawal |
| `topic/parkinsons` | Parkinson's disease research |
| `topic/pharmacokinetics` | Absorption, distribution, metabolism, excretion |
| `topic/phenomenology` | Subjective experience, visions, consciousness |
| `topic/policy` | Legal status, regulation, drug policy |
| `topic/protocol` | Treatment protocols, clinical procedures |
| `topic/psychiatric` | Mental health applications beyond addiction |
| `topic/ptsd` | Post-traumatic stress disorder |
| `topic/receptor` | Receptor binding, receptor pharmacology |
| `topic/serotonin` | Serotonin system, 5-HT receptors |
| `topic/sleep` | Sleep effects, REM, circadian |
| `topic/stimulant` | Cocaine, amphetamine, stimulant addiction |
| `topic/tbi` | Traumatic brain injury |
| `topic/toxicity` | Toxic effects, poisoning, overdose |
| `topic/traditional-use` | Bwiti, ceremonial, indigenous practices |
| `topic/veterans` | Military veterans, veteran populations |
| `topic/withdrawal` | Withdrawal symptoms, withdrawal management |

---

## Mechanism Tags (10)

| Tag | Meaning |
|-----|---------|
| `mechanism/dopamine-modulation` | Dopamine transporter effects, DAT |
| `mechanism/energy-metabolism` | Mitochondrial effects, ATP, metabolic |
| `mechanism/herg-blockade` | hERG potassium channel blockade, QT prolongation mechanism |
| `mechanism/ion-channel` | General ion channel effects (not hERG-specific) |
| `mechanism/kappa-opioid` | Kappa opioid receptor agonism |
| `mechanism/mu-opioid` | Mu-opioid receptor interactions, MOR binding/antagonism |
| `mechanism/nicotinic-receptor` | Nicotinic acetylcholine receptor effects |
| `mechanism/nmda-antagonism` | NMDA receptor antagonism |
| `mechanism/sert-inhibition` | Serotonin transporter inhibition |
| `mechanism/sigma-receptor` | Sigma receptor binding |

---

## Method Tags (11)

| Tag | Meaning |
|-----|---------|
| `method/case-report` | Single case descriptions |
| `method/case-series` | Multiple patients reported together (n≥2), same methodology |
| `method/clinical-trial` | Controlled trials (RCT or non-randomised) |
| `method/in-vitro` | Cell culture, receptor binding assays |
| `method/journalism` | Investigative journalism, news features, non-peer-reviewed reporting |
| `method/observational` | Retrospective, cross-sectional, registry studies |
| `method/preclinical` | Animal studies |
| `method/proteomics` | Proteomic analysis, protein expression profiling |
| `method/qualitative` | Interviews, thematic analysis, phenomenological |
| `method/review` | Narrative reviews, non-systematic |
| `method/systematic-review` | Systematic reviews, meta-analyses |

---

## Meta Tags (2)

| Tag | Meaning |
|-----|---------|
| `meta/hub` | Hub navigation documents (not research papers) |
| `meta/moc` | Maps of Content (not research papers) |

*Meta tags identify structural documents, not research papers.*

---

## Tag Count Policy

Three-tier limits based on document function:

- **Standard (≤5):** Empirical papers — clinical-trial, case-report, case-series, in-vitro, preclinical, observational, qualitative, research-article, brief-communication.
- **Synthesis (≤10):** Reviews, systematic-reviews, theses, guidelines, primary-sources, conference-talks, educational, interview-transcripts, commentaries, books, book-chapters, policy-reports.
- **Encyclopedic (named exceptions):** Alper2001 (16), Kobr2024 (14), Alfonso2023 (11). Comprehensive field reviews spanning ≥4 distinct domains. Adding new exceptions requires review.

The limit is a target, not a ceiling. Papers at limit+1 are acceptable when each tag maps to a distinct section of the paper. Limit+2 or more requires review.

---

## Using Tags in Bases

Filter by tag in any Base using:
```
tags.contains("topic/cardiac")
```

Combine with OR logic:
```yaml
or:
  - 'tags.contains("topic/veterans")'
  - 'tags.contains("topic/tbi")'
```
