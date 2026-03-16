---
title: "A New Approach Methodology (NAM) for the Prediction of (Nor)Ibogaine-Induced Cardiotoxicity in Humans"
authors:
  - "Shi, Miaoying"
  - "Wesseling, Sebastiaan"
  - "Bouwmeester, Hans"
  - "Rietjens, Ivonne M. C. M."
year: 2021
category: RED
tags:
  - topic/cardiac
  - topic/cyp2d6
  - topic/noribogaine
  - topic/pharmacokinetics
  - topic/toxicity
  - method/in-vitro
secondary_categories: [ORANGE]
key_findings: "PBK model predicts ibogaine QTc BMDL₁₀ of 97mg/70kg; noribogaine dominates in vivo cardiotoxicity due to high plasma levels and lower protein binding"
source_pdf: "2021/Shi2021_NAM_Ibogaine_Cardiotoxicity.pdf"
doi: "10.14573/altex.2103311"
pmid: "34271588"
journal: "ALTEX - Alternatives to Animal Experimentation"
publication_date: "2021-07-16"
document_type: in-vitro
clinical_significance: high
aliases:
  - "Shi 2021"
  - "NAM Ibogaine Cardiotoxicity Prediction"
  - "PBK Reverse Dosimetry Ibogaine"
evidence_level: in-vitro
qtc_data: true
electrolyte_data: false
herg_data: false
contraindications:
  - "Doses above BMDL₁₀ of ~97 mg ibogaine (70 kg body weight) predicted to cause significant QTc prolongation"
  - "CYP2D6 poor metaboliser status (up to 43-fold higher ibogaine concentrations)"
  - "Concurrent CYP2D6 inhibitor use (26-fold higher ibogaine Cmax reported)"
  - "Clinical doses (420–2100 mg) are 4–21-fold above predicted BMDL₁₀ for QTc prolongation"
dosing_range: "BMDL₁₀: 97 mg ibogaine / 70 kg (QTc onset); clinical range discussed: 420–2100 mg (6–30 mg/kg)"
route: oral
open_access: unknown
publisher: "Bentham Open"
body_format: vault-analytical
---

# A New Approach Methodology (NAM) for the Prediction of (Nor)Ibogaine-Induced Cardiotoxicity in Humans

**Citation:** Shi, M., Wesseling, S., Bouwmeester, H. and Rietjens, I. M. C. M. (2021). A New Approach Methodology (NAM) for the Prediction of (Nor)Ibogaine-Induced Cardiotoxicity in Humans. *ALTEX - Alternatives to Animal Experimentation*, 38(4), 636–652. doi:10.14573/altex.2103311

## Abstract

The development of non-animal-based new approach methodologies (NAMs) for chemical risk assessment and safety evaluation is urgently needed. The aim of the present study was to investigate the applicability of an in vitro–in silico approach to predict human cardiotoxicity of the herbal alkaloid ibogaine and its metabolite noribogaine, which are promising anti-addiction drugs. Physiologically based kinetic (PBK) models were developed using in silico-derived parameters and biokinetic data obtained from in vitro liver microsomal incubations and Caco-2 transport studies. Human induced pluripotent stem cell-derived cardiomyocytes (hiPSC-CMs) combined with a multi-electrode array (MEA) assay were used to determine in vitro concentration-dependent cardiotoxicity reflected by prolongation of field potential duration, which was subsequently translated to in vivo dose-dependent prolongation of the QTc (heart rate corrected duration from ventricular depolarization to repolarization) using PBK modeling-based reverse dosimetry. Results showed that the predictions matched well with in vivo kinetic data and QTc data for ibogaine and noribogaine available in the literature, indicating a good performance of the NAM. Benchmark dose analysis of the predicted dose response curves adequately predicted the onset of in vivo cardiotoxicity detected by QTc prolongation upon oral exposure to ibogaine and noribogaine. The present study provides an additional proof-of-principle of using PBK modeling-based reverse dosimetry as a NAM to predict human cardiotoxicity.

## Key Findings

- **FPDc prolongation:** Ibogaine and noribogaine induce significant concentration-dependent prolongation of FPDc in hiPSC-CMs, with BMCL₁₀ values of 0.11 μM (ibogaine) and 0.15 μM (noribogaine). Arrhythmia-type waveforms observed at 1 μM ibogaine and 3 μM noribogaine.
- **Toxic equivalency:** Ibogaine TEF = 1.00; noribogaine TEF = 0.65 (ibogaine is 1.4-fold more potent than noribogaine in the hiPSC-CM MEA assay).
- **PBK model validation:** Predicted blood Cmax and AUC within 2-fold of reported clinical values for both ibogaine and noribogaine (adequate performance threshold).
- **Noribogaine dominates in vivo cardiotoxicity:** Despite lower intrinsic potency, noribogaine contributes substantially more to in vivo cardiotoxic equivalents than ibogaine itself due to: (i) efficient CYP2D6-mediated O-demethylation of ibogaine to noribogaine (catalytic efficiency 2,248-fold higher than noribogaine glucuronidation), (ii) high plasma protein binding of ibogaine (fu = 0.04 vs 0.26 for noribogaine), (iii) slow noribogaine clearance via glucuronidation.
- **BMDL₁₀ predictions:** Ibogaine-induced QTc prolongation BMDL₁₀ = 96.9 mg/70 kg (~1.4 mg/kg); noribogaine BMDL₁₀ = 94.2 mg/70 kg. Clinical doses (420–2100 mg) are 4–21-fold above this threshold.
- **Validation against clinical data:** Predicted noribogaine dose-response curve BMDL₁₀ within 1.5-fold of clinically derived BMDL₁₀ (110 mg predicted vs 163 mg observed for 81.9 kg subjects). Ibogaine predictions best match clinical data when internet-purchased ibogaine purity of 15% is assumed.

## Methodology

**Study design:** In vitro–in silico NAM combining hiPSC-CM MEA cardiotoxicity data with PBK modeling-based reverse dosimetry (QIVIVE approach).

**In vitro cardiotoxicity assessment:**
- hiPSC-CMs (Pluricyte® cardiomyocytes, Ncardia) on MEA platform (60-6well MEA200/30iR-Ti-tcr, MCS GmbH)
- Cumulative concentration exposure protocol: ibogaine 0.03–1 μM; noribogaine 0.03–3 μM
- Endpoint: FPDc (field potential duration corrected for beat rate via Fridericia formula)
- Reference compounds: dofetilide (positive hERG control) and isoproterenol
- Three independent experiments, six well replicates each; ANOVA with Dunnett's test, significance at p < 0.05

**Biokinetic parameters:**
- Intestinal absorption: Caco-2 transport studies (Papp values)
- Metabolism: Human liver microsomal incubations (pooled from 150 donors) — Michaelis-Menten kinetics for ibogaine→noribogaine (CYP2D6-mediated O-demethylation) and noribogaine→noribogaine glucuronide (UGT-mediated)
- Protein binding: Rapid equilibrium dialysis (RED) in human plasma and in vitro medium

**PBK model:**
- Multi-compartment model for ibogaine with submodel for noribogaine
- Solved with Berkeley Madonna (v8.3.18), Rosenbrock's algorithms
- Evaluated against clinical PK data from Glue et al. (2015a,b, 2016)
- TEQ approach combining ibogaine + noribogaine cardiotoxicity for oral ibogaine dosing

**BMD analysis:** EFSA web-tool based on R-package PROAST v69; BMDL₁₀ as point of departure.

## Cardiac Safety Data

### In Vitro Cardiotoxicity (hiPSC-CM MEA)

| Compound | BMCL₁₀ (μM) | TEF | Arrhythmia threshold |
|----------|-------------|-----|---------------------|
| Ibogaine | 0.11 | 1.00 | 1 μM |
| Noribogaine | 0.15 | 0.65 | 3 μM |

Note: BMCL₁₀ corrected for unbound fraction in medium → noribogaine unbound effective concentration = 0.12 μM. This falls within the unbound blood concentration range at clinical doses (0.08–0.47 μM for noribogaine).

### Predicted In Vivo Dose-Response (QTc Prolongation)

| Parameter | Ibogaine | Noribogaine |
|-----------|----------|-------------|
| Predicted BMDL₁₀ (70 kg) | 96.9 mg (~1.4 mg/kg) | 94.2 mg (~1.3 mg/kg) |
| Predicted BMDL₁₀ (81.9 kg) | 108 mg | 110 mg |
| Clinical BMDL₁₀ (81.9 kg) | N/A (case reports only) | 163 mg (Glue et al., 2016) |
| Predicted/clinical ratio | — | 0.67 (1.5-fold difference) |

### Pharmacokinetic Parameters

| Parameter | Ibogaine | Noribogaine |
|-----------|----------|-------------|
| Papp (10⁻⁶ cm/s) | 27.9 ± 4.6 | 42.4 ± 3.6 |
| ka (/h) | 0.79 | 1.23 |
| Vmax (nmol/min/mg) | 0.17 ± 0.033 (→noribogaine) | 0.036 ± 0.0008 (→glucuronide) |
| Km (μM) | 0.63 ± 0.005 | 305 ± 15.8 |
| Catalytic efficiency (μL/min/mg) | 269.8 | 0.12 |
| fu (in vitro medium) | 0.71 ± 0.01 | 0.80 ± 0.03 |
| fu (human plasma) | 0.04 ± 0.017 | 0.26 ± 0.05 |

The 2,248-fold difference in catalytic efficiency (ibogaine→noribogaine vs noribogaine→glucuronide) explains why noribogaine plasma levels substantially exceed ibogaine levels after oral ibogaine dosing, and why noribogaine dominates the in vivo cardiotoxic profile.

### PBK Model Validation (vs Glue et al. clinical data)

| Study | Dose | Predicted/Reported Cmax ratio | Predicted/Reported AUC ratio |
|-------|------|------------------------------|------------------------------|
| Ibogaine (Glue 2015b) | 20 mg | 1.7 | 2.1 |
| Noribogaine (formed from 20 mg ibogaine) | — | 1.2 | 1.5 |
| Noribogaine (Glue 2015a) | 3 mg | 0.77 | 0.89 |
| Noribogaine (Glue 2015a) | 10 mg | 0.92 | 0.87 |
| Noribogaine (Glue 2015a) | 30 mg | 0.72 | 0.95 |
| Noribogaine (Glue 2015a) | 60 mg | 0.69 | 0.68 |
| Noribogaine (Glue 2016) | 60 mg | 0.94 | 0.76 |
| Noribogaine (Glue 2016) | 120 mg | 0.89 | 0.96 |
| Noribogaine (Glue 2016) | 180 mg | 0.86 | 0.68 |

All ratios within 2-fold (adequate predictive performance threshold).

### CYP2D6 Vulnerability

- CYP2D6 poor metabolisers: up to 43-fold higher ibogaine internal concentrations (Mash et al., 2001; Glue et al., 2015b)
- CYP2D6 inhibitor co-administration: 26-fold higher ibogaine Cmax in extensive metabolisers (Glue et al., 2015b)
- α1-acid glycoprotein levels (up to 10-fold interindividual variation) may further influence ibogaine protein binding

## Clinical Implications

This study provides quantitative risk thresholds highly relevant to clinical ibogaine practice:

1. **BMDL₁₀ as safety reference:** The predicted BMDL₁₀ of ~97 mg ibogaine/70 kg (≈1.4 mg/kg) represents the dose at which QTc prolongation onset is predicted to be negligible. All therapeutic doses (6–30 mg/kg) substantially exceed this threshold, confirming that QTc monitoring is essential for any ibogaine treatment.

2. **Noribogaine as primary cardiotoxic driver:** Despite ibogaine having higher intrinsic potency in vitro, noribogaine dominates in vivo cardiotoxicity. This has direct clinical relevance: (i) QTc prolongation may persist long after ibogaine clearance due to noribogaine's long half-life; (ii) monitoring should extend well beyond the acute ibogaine phase; (iii) noribogaine as a standalone therapeutic candidate would have comparable QTc risk at equivalent doses but eliminates the psychoactive ibogaine phase.

3. **CYP2D6 genotyping implications:** The dramatic (up to 43-fold) difference in ibogaine exposure between CYP2D6 metaboliser phenotypes underscores the importance of pharmacogenomic screening in pre-treatment protocols.

4. **Internet-purchased ibogaine purity:** The model predictions best match clinical case report data when assuming 15% purity of internet-purchased ibogaine, consistent with known quality control issues in unregulated supply chains.

## Limitations

- PBK model only includes glucuronidation for noribogaine clearance; other pathways (e.g., sulphation) may also contribute but data were insufficient to model
- hiPSC-CM MEA assay measures FPDc as a surrogate for QTc — while validated, it does not capture all proarrhythmic mechanisms
- Case report data used for ibogaine validation had unknown purity and poorly documented demographics/risk factors, introducing uncertainty in dose-response comparisons
- Model assumes additive cardiotoxicity of ibogaine and noribogaine; potential synergistic or antagonistic interactions not assessed
- Interindividual variability in CYP2D6 activity, plasma protein binding, and demographics not modelled (single representative 70 kg individual)
- The study authors note the biphasic kinetics reported by Obach et al. (1998) for ibogaine metabolism were not observed in their incubations

---

## See Also
- [[2016/Alper2016_hERG_Blockade]] — hERG blockade by iboga alkaloids; provides the patch-clamp hERG data this study contextualises
- [[2017/Rubi2017_hERG_iPSC_Cardiomyocytes]] — hiPSC-CM action potential prolongation by ibogaine/noribogaine; single-concentration comparison
- [[2015/Glue2015_Noribogaine_Ascending_Doses]] — Clinical PK data (noribogaine 3–60 mg) used for PBK model validation
- [[2015/Glue2015_Ibogaine_CYP2D6_Activity]] — Clinical PK data (20 mg ibogaine, CYP2D6 influence) used for PBK model validation
- [[2016/Glue2016_Noribogaine_Opioid_Patients_Safety]] — Clinical QTc dose-response data (noribogaine 60–180 mg) used for BMDL₁₀ validation
- [[2016/Schep2016_Ibogaine_Safe_Dose]] — Safe dose review; this study provides quantitative BMDL₁₀ estimates to complement Schep's clinical review
- [[RED_Cardiac_Safety_Hub]]
