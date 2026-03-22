---
title: "🔴 Cardiac Safety Hub"
category: RED
tags:
  - meta/moc
  - meta/hub
  - topic/cardiac
  - topic/toxicity
aliases: ["Safety Hub", "Cardiac Risk", "RED Papers"]
contraindications: []
qtc_data: false
electrolyte_data: false
herg_data: false
---

# 🔴 Cardiac Safety Hub

> **This is life-or-death territory.** Every fatality in the ibogaine literature traces back to cardiac mechanisms—specifically hERG channel blockade causing QTc prolongation. These papers document the problem AND the emerging solutions.

---

## The Core Problem: hERG Blockade

Ibogaine and its metabolite noribogaine block the hERG potassium channel (IKr), which delays cardiac repolarisation. This manifests as QTc prolongation on ECG—and when QTc exceeds ~500ms, the risk of fatal *torsades de pointes* (polymorphic ventricular tachycardia) becomes significant.

**Key insight**: Noribogaine has a longer half-life (24-36+ hours) than ibogaine (~4-7 hours), meaning cardiac risk persists LONG after subjective effects resolve.

---

## Foundational Toxicology

### [Dhahir 1971: Ibogaine Toxicology — The Foundation Stone](../1971/Dhahir1971_Ibogaine_Serotonin_Toxicity.md)
The earliest systematic toxicological characterisation of ibogaine. This PhD thesis established the LD₅₀ values still cited half a century later: **rat IP 145 mg/kg, mouse IP 175 mg/kg, rat oral 327 mg/kg, mouse oral 263 mg/kg**. Dhahir identified vagal cardiovascular mechanisms, predicted O-demethylation to an active metabolite (later confirmed as noribogaine), and documented dose-dependent respiratory depression and convulsions. Every subsequent dose-safety calculation — Schep 2016's NOAEL derivation, Shi 2021's PBK modelling — traces back to Dhahir's foundational data. Pre-dates clinical use entirely; purely pharmacological characterisation of a compound that wouldn't enter human therapeutics for another two decades.

---

## Authoritative Reviews

### [Corkery 2018: Benefits, Dangers and Fatalities — The Definitive Fatality Compilation](../2018/Corkery2018_Ibogaine_Benefits_Dangers_Fatalities.md)
**MOST COMPREHENSIVE FATALITY REVIEW**: 33 ibogaine-associated deaths (1990–2015) in *Progress in Brain Research*. Extends Alper 2012's 19-case series with 14 additional deaths including 5 UK coroner records. Key contributions:
- **Death-to-treatment ratio: 1:427** (based on Alper 2008 denominator of 3,414 treatments)
- **Risk triad**: cardiac disease (≥6 deaths), co-intoxicants (≥12 deaths), medical comorbidities (≥18 deaths)
- **CYP2D6 vulnerability**: 5–10% Caucasian poor metabolisers at elevated risk (78% of fatalities were opioid detox patients, predominantly Caucasian)
- **Post-mortem ibogaine range**: 0.24–9.3 mg/L (mean 2.11, N=16) — no clean dose-death threshold
- **Most comprehensive contraindication list** in the literature (10 items including pulmonary embolism risk — often overlooked)
- Pulmonary thromboembolism documented in 3 deaths — a non-cardiac fatality mechanism
- Pharmacokinetic data: oral 10–25 mg/kg, peak ~11 μg/mL at ~2h, noribogaine half-life 28–49h
- **18-MC** flagged as safer congener lacking tremor, bradycardia, and Purkinje cell damage

**Critical clinical implication**: Every fatality had at least one identifiable, screenable risk factor. These were preventable deaths. This paper is the evidential foundation for pre-treatment screening checklists.

### [Albert/MyEboga 2018: Community-Compiled Fatalities Record (1990–2010)](../Other/MyEboga2018_Fatalities_1990-2010.md)
**Community source, not peer-reviewed.** Lee Albert (MyEboga.com) compiled 12 ibogaine/iboga-associated fatalities from public domain sources — the most granular case-by-case documentation for the 1990–2010 period, with editorial commentary from a community researcher rather than a clinician. `mortality_scope: cumulative-review` — all 12 cases are subsumed within [Corkery 2018](../2018/Corkery2018_Ibogaine_Benefits_Dangers_Fatalities.md)'s 33-death series and [Köck 2022](../2022/Kock2022_Systemic_Review_Clinical_Trials_Therapeutic_Applications_Ibogaine.md)'s 38-death tally; these are NOT additional deaths. Key pattern across the series: every fatality had at least one identifiable, screenable risk factor (pre-existing cardiac disease in ≥5, polysubstance involvement in ≥4, absent medical screening in nearly all). Both [Corkery 2018](../2018/Corkery2018_Ibogaine_Benefits_Dangers_Fatalities.md) and [Chen 2024](../2024/Chen2024_RIVM_Iboga_Risk_Assessment.md) cite this compilation as a source, making it a historically significant upstream document in the fatality evidence chain despite its non-academic provenance.

### [Brunt 2026: Rare but Relevant — Cardiovascular Complications](../2026/Brunt2026_Cardiovascular_Complications_Review.md)
**CURRENT SYNTHESIS**: Clinical review in *Addiction* synthesising the state of cardiac safety evidence. Key contributions:
- **EC₅₀ for QTc prolongation: 0.195 µM** (Knuijver data)
- Peak plasma at therapeutic dose (10 mg/kg) is **>10× the EC₅₀**
- **Safe dose estimate: ~0.87 mg/kg** (10× lower than treatment doses)
- Recommends **CYP2D6 genotyping** before treatment (poor metabolisers at higher risk)
- Documents that cardiac events occur **without pre-existing cardiac conditions**
- References MISTIC magnesium protocol as mitigation strategy
- Reviews safer analogues (18-MC, oxa-iboga)

### [Schep et al. 2016: The Dose Paradox — Why "Safe" and "Therapeutic" Don't Overlap](../2016/Schep2016_Ibogaine_Safe_Dose.md)
**LANDMARK DOSE-SAFETY ANALYSIS**: The paper that quantified ibogaine's fundamental therapeutic paradox. Applying standard pharmaceutical safety factors to animal toxicity data (Dhahir 1971 LD₅₀ values) yields a theoretical safe dose of **0.87 mg/kg** — calculated via NOAEL with ÷10 intra-species, ÷10 inter-species, and ÷3 susceptible-population safety factors. Clinical doses for addiction treatment are **6–30 mg/kg**, an order of magnitude above this threshold. The hERG IC₅₀ sits squarely within therapeutic plasma concentrations. Schep placed ibogaine's risk profile in the language regulators understand, and the message was stark: there is no dose that is simultaneously safe and therapeutic by conventional pharmaceutical standards. This paper's methodology directly informed the RIVM's subsequent conclusion that no health-based guidance value can be derived ([Chen 2024](../2024/Chen2024_RIVM_Iboga_Risk_Assessment.md)).

### [Litjens & Brunt 2016: How Toxic Is Ibogaine?](../2016/Litjens2016_How_Toxic_Is_Ibogaine.md)
The most comprehensive toxicology review at time of publication in *Clinical Toxicology*. Analysed 14 detailed case reports, synthesised pharmacokinetic and pharmacodynamic data, and identified the critical triad driving ibogaine cardiotoxicity: **CYP2D6 metabolic variability** (poor metabolisers accumulate noribogaine), **noribogaine persistence** (half-life extending days beyond ibogaine clearance), and **hERG channel blockade** (therapeutic concentrations overlapping IC₅₀). Tabulated 27 deaths at time of writing. Foundation text for clinical risk assessment that anticipated many of the conclusions later formalised by regulatory bodies.

### [Chen et al. 2024: RIVM Risk Assessment — The Regulatory Verdict](../2024/Chen2024_RIVM_Iboga_Risk_Assessment.md)
**LANDMARK REGULATORY ASSESSMENT**: The most authoritative governmental risk assessment of ibogaine to date, conducted by the Netherlands' National Institute for Public Health and the Environment (RIVM). **34 deaths tabulated** — the most comprehensive official mortality count. 58 case reports analysed total. Core conclusion: **no health-based guidance value (HBGV) can be derived**, and RIVM **advises against consumer use**. QTc prolongation documented from doses as low as 4.5 mg/kg. CYP2D6 poor metabolisers face dramatically elevated exposure: **AUC 11,471 vs 3,936 ng·hr/mL** — a nearly 3-fold difference. This represents the regulatory endpoint of the evidence trajectory running from Dhahir 1971 through Schep 2016: five decades of accumulating evidence distilled into the bureaucratic language of "no safe dose derivable."

### [Esperança et al. 2026: Scoping Review — Translational Perspectives](../2026/Esperanca2026_Cardiac_Safety_Translational_Perspectives_Scoping_Review.md)
The most current comprehensive safety review, published in *Molecules* in February 2026. PRISMA-ScR methodology across PubMed/MEDLINE, SciELO, and Cochrane (1901–2025). 22 studies met inclusion criteria. Synthesises QTc prolongation data (values exceeding 600 ms in multiple reports, up to 714 ms), malignant ventricular arrhythmias, and **19+ fatalities**. The review positions ibogaine not as a viable therapeutic endpoint but as a **lead compound** informing rational design of next-generation anti-addictive therapeutics — a framing that acknowledges both the substance's extraordinary pharmacology and its intractable cardiac safety profile. Documents prolonged risk windows of 7–12 days post-exposure, consistent with noribogaine-driven delayed cardiotoxicity.

### [Evans 2026: Learning from Ibogaine Fatalities, Rather Than Covering Them Up](../Other/Evans2026_Ibogaine_Fatalities_Cover_Ups.md)
**CONTEMPORARY FATALITY DOCUMENTATION**: Investigative journalism documenting **5 ibogaine-associated deaths (2024–2026)** across underground and semi-regulated settings: Ambio (Mexico, fentanyl detection failure), SoulCentro (Costa Rica, cardiac arrest), Awaken Your Soul/Holos (Costa Rica, drowning), IbogaQuest (Mexico, undetectable physiological vulnerability), and Andy Haman (Colorado, underground treatment leading to criminal conviction). Cites the **1-in-427 fatality estimate** (from [Alper 2012](../2012/Alper2012_Ibogaine_Fatalities.md)/[Corkery 2018](../2018/Corkery2018_Ibogaine_Benefits_Dangers_Fatalities.md)) and references the forthcoming Barsuglia/Arns updated estimate. Includes GITA statement on **nitazene and xylazine detection failures** — lipophilic synthetic opioids may persist 7–14 days undetected by standard toxicology, risking opioid potentiation upon premature ibogaine administration. Arrives at a pivotal moment: unprecedented US political support ($50M Texas, $5M Arizona), major media coverage, and commercial investment increasing scrutiny of safety records. The piece argues that transparency and accountability — not concealment — are essential for field survival. Published on *Ecstatic Integration* (Substack). Read alongside [Corkery 2018](../2018/Corkery2018_Ibogaine_Benefits_Dangers_Fatalities.md) (systematic fatality compilation) and [Brunt 2026](../2026/Brunt2026_Cardiovascular_Complications_Review.md) (clinical review of cardiac complications).

---

## Foundational Electrophysiology

### [Luciano 2000: Early Continuous EKG Monitoring — A Negative Finding in Context](../2000/Luciano2000_Neurologic_EEG_Medical_Observations.md)
Among the earliest systematic cardiac monitoring during ibogaine treatment: **12h continuous EKG** in **n=5** opioid-dependent subjects receiving **~25 mg/kg** oral ibogaine HCl (St. Kitts). No abnormalities detected. At a dose now considered aggressive, normal EKG findings are notable — though the sample is far too small to be reassuring, and the monitoring predates systematic QTc reporting entirely. This paper reflects a period before hERG/QTc awareness entered the ibogaine literature; the absence of QTc data reflects the era, not the investigators' rigour. Read alongside the hERG characterisation that followed ([Koenig 2012](../2012/Koenig2012_Ibogaine_hERG_Cardiac_Arrhythmia_Risk.md), [Alper 2016](../2016/Alper2016_hERG_Blockade.md)) and the later hospital-based monitoring showing 50% QTc >500 ms at 10 mg/kg ([Knuijver 2021](../2021/Knuijver2021_Safety_Opioid_Detox.md)), this early negative finding likely reflects the insensitivity of pre-digital EKG interpretation to QTc changes rather than an absence of effect. Primary clinical outcomes reported in [BLUE_Outcomes_Hub](BLUE_Outcomes_Hub.md).

### [Alper et al. 2012: Fatalities Temporally Associated with Ibogaine](../2012/Alper2012_Ibogaine_Fatalities.md)
The definitive systematic review of ibogaine-associated deaths. Documented 19 fatalities (1990-2008). Critical finding: **100% of fatalities with documented electrolytes showed hypokalemia** (low potassium). This is THE paper that established the electrolyte-cardiac connection. Mortality rate 1 in 427 (based on Alper 2008 treatment denominator). Most deaths occurred 1.5–76 hours post-ingestion — a temporal window that presaged the later understanding of noribogaine's prolonged cardiac effects. Pre-existing cardiac pathology and opioid co-exposure identified as major risk factors. Transformed scattered case reports into actionable epidemiology.

### [König & Hilber 2015: Ibogaine and the Heart](../2015/Koenig2015_Cardiac_Mechanisms.md)
Comprehensive cardiac mechanisms review. Synthesises electrophysiology literature, establishes clinical significance of hERG blockade, reviews case reports. Essential reading for understanding WHY cardiac screening matters.

### [Alper et al. 2016: hERG Blockade by Iboga Alkaloids](../2016/Alper2016_hERG_Blockade.md)
**BREAKTHROUGH**: First precise IC50 values for hERG blockade:
- Ibogaine: **4.09 ± 0.69 µM**
- Noribogaine: **2.86 ± 0.68 µM** (more potent, longer-lasting = higher risk)
- 18-MC: **>50 µM** (12× safer—validates analogue development)

This paper quantifies the therapeutic window and explains why noribogaine persistence is the key risk factor.

### [Koenig & Hilber 2012: The Rosetta Stone — First hERG IC₅₀](../2012/Koenig2012_Ibogaine_hERG_Cardiac_Arrhythmia_Risk.md)
**LANDMARK**: The brief communication in *Addiction Biology* that cracked the code. First published IC₅₀ of **3.9 ± 0.3 μM** for ibogaine's hERG blockade, demonstrating that therapeutic plasma concentrations overlap hERG-blocking concentrations — placing ibogaine in the pharmacological company of drugs withdrawn from market for causing torsade de pointes (astemizole, cisapride, terfenadine). The sub-unity Hill coefficient (0.81) hinted at complex binding kinetics later elucidated by [Thurner 2014](../2014/Thurner2014_hERG_Channel_Block_Ibogaine.md). TSA-201 cells, 22°C, whole-cell patch clamp. This quantitative foundation underpins all subsequent cardiac risk assessment.

### [Koenig et al. 2013: Multi-Channel Cardiac Profile — Solving the Guinea Pig Paradox](../2013/Koenig2013_Ibogaine_Cardiac_Ion_Channel_Profile.md)
Expanded the Koenig 2012 finding into a comprehensive cardiac ion channel pharmacology. Multi-channel profile: **hERG IC₅₀ 4 μM, Nav1.5 IC₅₀ 142 μM, Cav1.2 IC₅₀ 53–163 μM**. 18-MC showed improved safety (hERG IC₅₀ 15 μM). The multi-channel data revealed why guinea pig cardiomyocytes were misleading models: at higher concentrations, Cav1.2 (L-type calcium channel) blockade shortened guinea pig action potential duration, masking the hERG-driven prolongation that dominates in human ventricle. Computer modelling of human ventricular tissue predicted net AP prolongation — a prediction experimentally confirmed four years later by [Rubi et al. 2017](../2017/Rubi2017_hERG_iPSC_Cardiomyocytes.md). Also demonstrated a −9.4→−18.6 mV shift in activation voltage and slowed deactivation kinetics.

### [Thurner et al. 2014: Molecular Mechanism — The Y652/F656 Binding Pocket](../2014/Thurner2014_hERG_Channel_Block_Ibogaine.md)
Resolved the molecular mechanism to atomic resolution. Ibogaine blocks hERG through the **canonical binding pocket** (Y652/F656) in the S6 pore-lining domain — the same site exploited by virtually all drugs withdrawn for QT prolongation. **Open/inactivated-state** block only (not resting-state), with **cytosolic access** via neutral membrane permeation (pKₐ 8.1). F656A mutation reduced potency 50-fold, confirming the binding site. Block is pulse-duration dependent rather than frequency dependent. Molecular docking confirmed central cavity binding. This mechanistic clarity placed ibogaine's cardiac risk on the same molecular footing as established pharmaceutical cardiotoxins — the drug isn't just correlated with QT prolongation, it blocks the exact same channel at the exact same site via the exact same mechanism.

### [Rubi et al. 2017: Human Proof — The Guinea Pig Paradox Resolved](../2017/Rubi2017_hERG_iPSC_Cardiomyocytes.md)
The experimental proof that [Koenig 2013](../2013/Koenig2013_Ibogaine_Cardiac_Ion_Channel_Profile.md)'s computational predictions were correct. Using **human iPSC-derived cardiomyocytes** (hiPS-CM), demonstrated that 3 μM ibogaine retards repolarisation in human ventricular-like cells — confirming that therapeutic concentrations prolong the human action potential. Crucially also demonstrated that **noribogaine prolongs the AP**, providing the mechanistic basis for understanding why cardiac events occur days after ibogaine has cleared. Guinea pig cardiomyocytes had shown paradoxical AP shortening at ≥10 μM (due to concurrent Cav1.2 blockade), misleading the field for years. This paper closed the translational gap between in vitro pharmacology and clinical cardiotoxicity.

### [Booze et al. 2012: Maryland Poison Center Alert](../2012/Booze2012_MPC_Ibogaine_Toxicity.md)
Maryland Poison Center bulletin documenting cardiac effects persisting up to **9 days** post-ibogaine exposure. An early clinical toxicology alert that, while lacking the experimental detail of subsequent electrophysiology publications, signalled the prolonged temporal risk window later mechanistically explained by noribogaine persistence. Contributed to growing awareness among poison centres and emergency departments.

---

## Controlled Clinical Safety Data

### [Glue et al. 2016: Noribogaine Phase I — Quantifying the Concentration-QTc Relationship](../2016/Glue2016_Noribogaine_Opioid_Patients_Safety.md)
**THE ONLY PLACEBO-CONTROLLED RCT** of noribogaine in patients. Three dose cohorts (60/120/180 mg) in opioid-dependent patients. Definitively quantified the **concentration-QTc relationship: 0.17 ms/ng/mL** (QTcI). ΔΔQTcI values of 16/28/42 ms across doses. The Data Safety Monitoring Board reduced the top dose from 240 to 180 mg after observing QTc prolongation at 120 mg — a safety signal within a formal RCT. Noribogaine t½ of 24–30 hours. hERG IC₅₀ of 5 μM for noribogaine confirmed. Critically, calculating that ~286 mg ibogaine would produce equivalent peak noribogaine exposure directly implicates noribogaine as the primary QTc driver during standard ibogaine treatment — where doses far exceed 286 mg. This is the only study providing formal pharmacokinetic-pharmacodynamic modelling of the QTc relationship.

### [Knuijver et al. 2021: Dutch Hospital Safety Study](../2021/Knuijver2021_Safety_Opioid_Detox.md)
**THE ONLY controlled hospital-based ibogaine study with continuous cardiac monitoring.** n=14 opioid-dependent patients, 10mg/kg dose in university medical centre. Key findings:
- **QTc prolongation average 95ms** (range 29-146ms)
- **50% reached QTc >500ms** during observation
- **Prolongation >450ms persisted >24h** in 6/14 patients
- **ZERO torsade de pointes** despite severe prolongation
- 11/14 did not return to morphine within 24h

This study proves that even with significant QTc prolongation, fatal arrhythmia can be prevented with proper hospital monitoring. The extended duration of QTc elevation (>24h) validates the need for prolonged cardiac observation post-treatment.

### [Rocha 2025: Dose-Escalation AUD Trial — Unprotected QTc Data](../2025/Rocha2025_PhD_Ibogaine_Alcohol_AUD.md)
**DOSE-RESPONSE WITHOUT MAGNESIUM**: First ibogaine trial for AUD (N=9, 20–400mg HCl). Provides controlled dose-response QTc data in the absence of magnesium cardioprotection — a critical contrast with [MISTIC](../2024/Cherian2024_Magnesium_Ibogaine_TBI.md):
- **Vol 3 (240mg):** Baseline 413ms → Peak 492ms at 12h (ΔQTc +79ms)
- **Vol 5 (400mg):** Baseline 413ms → Peak 496ms at 12h (ΔQTc +83ms)
- **Vol 9 (400mg):** Baseline 409ms → Peak 470ms at 6h (ΔQTc +61ms)
- **Novel finding — ischaemic mimic:** Vol 7 (400mg) developed transient ST-elevation and T-wave inversion in V2/V3 at 5–6h, spontaneously resolving by 12h. Follow-up angio-CT normal. This is the first controlled documentation of ibogaine-associated ST-changes beyond QTc prolongation.
- **Hypertensive crisis:** Vol 3 reached BP 180/110 mmHg at 240mg, requiring captopril + lorazepam. Planned 400mg session cancelled.
- **No electrolyte optimisation protocol** — reinforces the MISTIC finding that magnesium co-administration may be the critical differentiator.

**Clinical significance:** When read alongside Knuijver 2021 (also unprotected, QTc >500ms in 50%) and MISTIC (Mg-protected, ZERO events), this study strengthens the case that magnesium cardioprotection is not optional but essential.

---

## Fatality Case Reports

### [Marker & Stajic 2002: NYC Medical Examiner — The Earliest Forensic Ibogaine Fatality](../2002/Marker2002_Ibogaine_Related_Fatality.md)
The earliest ibogaine-associated death in the vault's forensic record — a conference abstract from the 40th TIAFT meeting, emerging not from ibogaine research but from routine toxicological screening at the NYC Office of Chief Medical Examiner. A 36-year-old male polydrug user, found unresponsive with drug paraphernalia and empty alcohol bottles at the scene. The tissue concentrations are staggering: **blood 9225 ng/mL, brain 18563 ng/kg, liver 18137 ng/kg** — approximately 2–9× the therapeutic plasma range later established in clinical studies. Co-intoxicants included morphine (22 ng/mL) and benzoylecgonine (633 ng/mL), with alcohol suspected from scene evidence. Ibogaine was initially detected as an "unknown substance" — in 2002, forensic laboratories did not yet have ibogaine in their screening panels, and Stajic (one of the most respected forensic toxicologists in the US) identified it only through further investigation. **No cardiac data were reported**, and this absence is itself a historical marker: the hERG/QTc framework that would explain ibogaine cardiotoxicity ([Koenig 2012](../2012/Koenig2012_Ibogaine_hERG_Cardiac_Arrhythmia_Risk.md)) was a decade away. Every risk factor that subsequent fatality reviews would identify — polydrug exposure, unsupervised use, unknown dosing, chronic substance abuse — is present in this single case. Compare the tissue concentrations with [Kontrimavičiūtė 2006](../2006/Kontrimaviciute2006_Tissue_Distribution_Ibogaine_Fatality.md) (comparable levels); the case is tabulated in [Corkery 2018](../2018/Corkery2018_Ibogaine_Benefits_Dangers_Fatalities.md)'s 33-death series and reviewed in [Litjens 2016](../2016/Litjens2016_How_Toxic_Is_Ibogaine.md).

### [Kontrimavičiūtė et al. 2006: First Human Tissue Distribution Post-Mortem](../2006/Kontrimaviciute2006_Tissue_Distribution_Ibogaine_Fatality.md)
First systematic measurement of ibogaine and noribogaine distribution across human tissues post-mortem. The highest concentrations were found in **lung and liver**, reflecting first-pass metabolism and extensive tissue binding. This forensic pharmacokinetic data — showing how the drug distributes after death — became essential reference for interpreting subsequent autopsy findings and understanding why post-mortem blood concentrations are unreliable predictors of perimortem exposure.

### [Chèze et al. 2008: Drowning Death — Hair Analysis Reveals Repeated Use](../2008/Cheze2008_Ibogaine_Noribogaine_LC-MSMS_Drowning_Death.md)
French case: death by drowning with ibogaine detected in post-mortem samples. The critical contribution was the **first detection of ibogaine in human hair** (1.2 and 2.5 ng/mg across segments), demonstrating repeated exposure prior to the fatal event. LC-MS/MS methodology. This paper expanded the forensic toolkit beyond blood and urine, enabling retrospective exposure assessment — relevant for cases where post-mortem degradation compromises conventional matrices.

### [Hoelen et al. 2009: First NEJM-Published Long-QT Case](../2009/Hoelen2009_Long_QT_Ibogaine.md)
The case that brought ibogaine cardiotoxicity to mainstream medical attention. Published in the *New England Journal of Medicine*, documenting a patient with **QTc 616 ms** following ibogaine ingestion. Hypokalemia and hypomagnesemia were documented — anticipating the electrolyte-cardiac connection that would become central to protocol development. The NEJM platform ensured this case reached cardiologists and emergency physicians who might otherwise never encounter ibogaine, broadening awareness beyond the addiction medicine community.

### [Paling et al. 2012: Three Dutch Cases — Life-Threatening Complications](../2012/Paling2012_Life_Threatening_Complications.md)
Three cases from the Netherlands with **QTc >700 ms** and confirmed **torsade de pointes** (TdP). Naranjo adverse drug reaction probability assessment confirmed causality. Part of the cluster of Dutch cases that eventually contributed to regulatory concern and the RIVM risk assessment ([Chen 2024](../2024/Chen2024_RIVM_Iboga_Risk_Assessment.md)). The extreme QTc values (>700 ms) placed these among the most severe QT prolongations documented in the ibogaine literature.

### [Pleškovič et al. 2012: Sustained Tachyarrhythmias — 5 VF + 3 VT Episodes](../2012/Pleskovic2012_Ibogaine_Ventricular_Tachyarrhythmias.md)
A remarkable case documenting **5 episodes of ventricular fibrillation and 3 of ventricular tachycardia** over 48 hours, with QTc 593 ms at 42 hours post-ingestion. Critically, **amiodarone administration worsened QTc** — a cautionary finding for emergency physicians who might reflexively reach for antiarrhythmics. The sustained and recurrent nature of the arrhythmias, extending nearly two days post-ingestion, powerfully illustrates the prolonged risk window driven by noribogaine persistence.

### [Shawn 2012: TdP Despite Normal Pre-Treatment Screening](../2012/Shawn2012_Ibogaine_TdP_VT.md)
**A critical lesson for protocols**: the first documented case of TdP in a patient whose pre-treatment screening was entirely normal. This case demonstrates that even comprehensive screening cannot eliminate cardiac risk — it can only reduce it. The implication is that continuous cardiac monitoring during and after ibogaine administration remains essential regardless of screening results. A humbling counterpoint to assumptions that screening alone is sufficient cardioprotection.

### [Warrick et al. 2012: Fatality with Pre-Existing AICD](../2012/Warrick2012_Ibogaine_Fatality.md)
25-year-old male with a **pre-existing automatic implantable cardioverter-defibrillator** (AICD) — a clear contraindication — who died following ibogaine use. Post-mortem ibogaine concentration **2.2 μg/mL** in heart blood. The presence of an AICD indicates known pre-existing cardiac disease, making this a preventable death with adequate screening. Published in *Clinical Toxicology*.

### [Asúa et al. 2013: First UK Case — Rescued by Overdrive Pacing](../2013/Asua2013_Ibogaine_Toxicity_UK_Case.md)
First documented UK case. A 7g dose produced **QTc 600 ms**. The patient was rescued by **transcutaneous overdrive pacing at 80 bpm** — a critical acute management technique that suppresses TdP by preventing the long pauses during which early afterdepolarisations trigger the arrhythmia. This case, alongside [Hildyard 2015](../2015/Hildyard2015_QT_Prolongation_TdP_Ibogaine.md), established overdrive pacing as a key intervention in ibogaine-associated cardiac emergencies.

### [Jalal et al. 2013: Death from Multi-Organ Failure](../2013/Jalal2013_Ibogaine_Death_Heroin_Case.md)
25-year-old male with SVT (supraventricular tachycardia) history who died from **multi-organ failure** two days after a 2.5g ibogaine dose. The multi-organ failure trajectory — rather than acute arrhythmia — represents a less commonly reported but important fatality mechanism, potentially involving hemodynamic compromise, hepatotoxicity, or rhabdomyolysis in addition to cardiac effects. The pre-existing SVT was an unscreened contraindication.

### [Papadodima et al. 2013: Greek Case — Multiple Comorbidities](../2013/Papadodima2013_Ibogaine_Sudden_Death_Case.md)
52-year-old male with alcohol dependence, **liver cirrhosis**, and **40–45% coronary artery occlusion** — three independent risk factors. This case illustrates the cumulative risk model: impaired hepatic metabolism (affecting both ibogaine clearance and CYP2D6-mediated conversion to noribogaine), pre-existing coronary disease reducing cardiac reserve, and the cardiac demands of ibogaine's autonomic effects. Multiple screenable comorbidities, any one of which should have been an exclusion criterion.

### [Vlaanderen et al. 2014: Healthy Young Male — Cardiac Arrest and Permanent Brain Injury](../2014/Vlaanderen2014_Cardiac_Arrest_Ibogaine.md)
A particularly sobering case: a **healthy 26-year-old male** with no apparent risk factors suffered cardiac arrest from ventricular fibrillation approximately 5 hours after ingesting 2,400 mg ibogaine. QTc max **663 ms**. The patient survived but sustained **permanent neurological deficits** — a devastating non-fatal outcome rarely emphasised in the literature, which tends to focus on mortality. Part of the Dutch case cluster that prompted regulatory scrutiny.

### [Hildyard & Bhatti 2015: Serial TdP — Rescued by Magnesium and Overdrive Pacing](../2015/Hildyard2015_QT_Prolongation_TdP_Ibogaine.md)
Dramatic case with QTc progression from **640 to 730 ms** (day 2) and **8 episodes of polymorphic VT/TdP**. Successfully terminated by **IV magnesium sulphate and overdrive pacing**. This case is directly relevant to the MISTIC rationale: the acute therapeutic response to IV magnesium during cardiac emergency foreshadowed the preventive strategy of magnesium co-administration. Together with [Grogan 2019](../2019/Grogan2019_Seizures_QT_Prolongation_Cardiac.md)'s QTc 788 ms case (also terminated by IV MgSO₄), it established the empirical basis for magnesium cardioprotection.

### [Aćimović et al. 2021: Serbian Forensic Case](../2021/Acimovic2021_Ibogaine_Death_Case_Report.md)
27-year-old heroin-dependent male, found dead. Post-mortem blood ibogaine concentration **3.26 mg/L** — within the range documented by Corkery 2018 (0.24–9.3 mg/L). Notably, **no cardiac pathology on histological examination** — consistent with a functional/electrophysiological mechanism (arrhythmia) rather than structural damage. Serbian case contributing to the geographical breadth of the fatality record.

### [Meisner et al. 2016: Ibogaine-Associated Cardiac Arrest and Death](../2016/Meisner2016_Cardiac_Arrest_Death_Case.md)
Boston case report: 40-year-old male used 4g ibogaine + 2g 'booster' for heroin detox. Found in asystole 8 hours later, brain death from cardiac arrest. Includes literature review on ibogaine cardiotoxicity. **Critical warning about unregulated internet sourcing.**

### [Mazoyer et al. 2013: Fatal Case of a 27-Year-Old Male](../2013/Mazoyer2013_Fatality_Case.md)
French forensic case report. 27-year-old male, cardiac arrest during ibogaine withdrawal treatment. QTc prolongation documented. Establishes European legal/forensic context.

### [Steinberg & Deyell 2018: Cardiac Arrest After Ibogaine Intoxication](../2018/Steinberg2018_Cardiac_Arrest_Case.md)
Recent cardiac arrest case with survival (ECMO/resuscitation). Documents massive QTc prolongation (>600ms). Demonstrates that even with extreme QTc, survival is possible with appropriate intervention.

### [Busby 2024: Rolling Stone Investigation - Beond Clinic Death](../Other/Busby2024_Beond_Death_Investigation.md)
Investigative journalism documenting a death at commercial Beond clinic in Cancún. Critical industry accountability document. Raises questions about safety protocols at commercial facilities.

### [Mestre et al. 2024: Portuguese Case — Multiple Cardiac Arrests After Test Dose](../2024/Mestre2024_Cardiac_Arrest_Case_Report.md)
A chilling recent case: multiple cardiac arrests after **only 200 mg ibogaine (2.6 mg/kg)** — a sub-therapeutic test dose. QTc 636 ms, torsade de pointes, **3 defibrillations** required. No structural heart disease identified. This case demolishes any assumption that low doses carry proportionally low risk. The 2.6 mg/kg dose is below many published "minimum therapeutic" thresholds, yet proved nearly lethal. Demonstrates that individual susceptibility — likely CYP2D6 phenotype, electrolyte status, or unknown factors — can override dose-response expectations. Published in *Cureus*.

### [Edwards et al. 2025: UK Poison Centre Case Series — A Decade of Toxicity](../2025/Edwards2025_UK_NPIS_Ibogaine_Toxicity_Case_Series.md)
Seven cases reported to the UK National Poisons Information Service (NPIS) between 2012 and 2022. **6/7 developed cardiotoxicity**; **2 suffered cardiac arrests with hypoxic brain injury** — devastating non-fatal outcomes. QTc values of **680–720 ms**. Doses ranged from 5–34g root bark. Notably, **no dose-response relationship** was observed — the severity of cardiotoxicity did not correlate with dose, reinforcing the role of individual metabolic variability. All cases were recorded as "recreational abuse," though two patients were actually attempting opioid withdrawal — a misclassification reflecting limited clinician familiarity with ibogaine's therapeutic context. Published in *Clinical Toxicology*.

---

## Clinical Toxicology & Pharmacokinetics

### [O'Connell et al. 2015: Internet-Purchased Ibogaine — Serial Pharmacokinetics](../2015/OConnell2015_Internet_Ibogaine_Toxicity.md)
Unusually detailed pharmacokinetic data from a clinical toxicity case. 33-year-old male, ~3.8g from internet capsules (479 mg/capsule). Peak serum **377 ng/mL**, QTc **527 ms** (transient). **Non-linear elimination** with multi-compartment kinetics: rapid α-phase (t½ 67 min) and slower β-phase (t½ 162 min). The serial serum sampling — rare in toxicity cases — provided a real-world pharmacokinetic profile complementing the controlled data from [Glue 2016](../2016/Glue2016_Noribogaine_Opioid_Patients_Safety.md). The internet-purchased product and self-dosing context typifies the uncontrolled exposure pattern seen in most serious adverse events.

### [Henstra et al. 2017: The Noribogaine Revelation — 2,540-Hour Half-Life](../2017/Henstra2017_Ibogaine_Noribogaine_Toxicokinetics_Cardiac.md)
The pharmacokinetically most important case report in the literature. QTc **647 ms** with documented TdP. Noribogaine elimination half-life of **2,540 hours** (106 days) — versus the 28–49 hours reported in healthy volunteers. The k₁₂/k₂₁ ratio of **21.5** demonstrated extreme deep-tissue sequestration of noribogaine in overdose. QTc prolongation persisted **12 days** post-ingestion, directly correlated with noribogaine plasma concentrations. Hypokalaemia and hypomagnesaemia present. Internet-purchased, 1,400 mg over 12 hours. This case fundamentally shifted understanding of the temporal risk window: when tissue reservoirs are saturated, noribogaine seeps back into plasma for weeks, maintaining cardiac risk long after the acute phase appears resolved.

### [Grogan et al. 2019: QTc 788 ms — The Most Extreme Prolongation on Record](../2019/Grogan2019_Seizures_QT_Prolongation_Cardiac.md)
Documents the **highest QTc value in the ibogaine literature: 788 ms** — with rare captured ECG tracings of TdP entry and exit. The dramatic response to **2g IV MgSO₄ terminated all dysrhythmias**, with QTc recovery trajectory: 788→615→464 ms. Hypokalaemia present. Product was mislabelled as "Devil's Claw" herbal supplement. Polysubstance context. Together with [Hildyard 2015](../2015/Hildyard2015_QT_Prolongation_TdP_Ibogaine.md), this case established the empirical basis for magnesium's acute antiarrhythmic efficacy in ibogaine-associated TdP — the clinical observation that was later formalised into the preventive MISTIC protocol.

### [Shi et al. 2021: Computational Modelling — New Approach Methodology](../2021/Shi2021_NAM_Ibogaine_Cardiotoxicity.md)
Computational tour de force applying **New Approach Methodology (NAM)** — PBK modelling combined with hiPSC-CM multi-electrode array data — to predict ibogaine cardiotoxicity without animal testing. The PBK-modelled BMDL₁₀ for QTc prolongation onset: **97 mg/70 kg (~1.4 mg/kg)** — clinical doses are 4–21× above this threshold. Crucially demonstrated that **noribogaine dominates in vivo cardiotoxicity** despite lower intrinsic per-molecule potency: its higher free fraction (fu 0.26 vs ibogaine's 0.04) and slow clearance overwhelm ibogaine's greater intrinsic potency. Ibogaine TEF = 1.0, noribogaine TEF = 0.65. Validated against Glue 2016 clinical PK data. The BMDL₁₀ of ~1.4 mg/kg aligns closely with [Schep 2016](../2016/Schep2016_Ibogaine_Safe_Dose.md)'s safety-factor calculation (0.87 mg/kg), providing orthogonal computational validation.

---

## Adverse Events Reviews

### [Oña et al. 2021: Adverse Events Updated Systematic Review](../2021/Ona2021_Adverse_Events_Ibogaine_Updated_Review_2015-2020.md)
Updates Alper 2012 with literature from 2015-2020. Documents evolution of safety protocols. Shows **declining fatality rates** in clinical settings—evidence that protocols work.

### [2015: Ibogaine and Mania Case Reports](../2015/Marta2015_Ibogaine_Mania_Case_Reports.md)
Three cases of manic episodes following ibogaine. Non-cardiac adverse event but important for psychiatric screening. Contraindication for bipolar disorder.

### [Breuer et al. 2015: "Herbal Seizures" Case Report](../2015/Breuer2015_Herbal_Seizures_Case_Report.md)
Seizure case with massive overdose (38g cumulative). Documents dose-dependent toxicity. Important for understanding threshold effects.

---

## Preclinical Safety Data

### [Uzelac et al. 2024: Cardiotoxic Necrosis in Rats—Role of Redox Processes](../2024/Uzelac2024_Cardiotoxic_Necrosis_Redox.md)
Animal study demonstrating ibogaine-induced cardiac necrosis via redox/oxidative mechanisms. Suggests antioxidant co-administration may be protective. Emerging research direction.

---

## The Solution: Magnesium Cardioprotection

**This is the paradigm shift.** The 2023-2024 MISTIC protocol studies demonstrate that magnesium co-administration may ELIMINATE cardiac risk:

### [Cherian et al. 2024: Magnesium-Ibogaine Therapy in Veterans with TBI](../2024/Cherian2024_Magnesium_Ibogaine_TBI.md)
**Nature Medicine landmark paper.** n=30 Special Operations Forces veterans with TBI. MASSIVE effect sizes (PTSD d=3.16, depression d=3.51). But the cardiac finding is revolutionary: **ZERO clinically significant QTc prolongation** with magnesium co-administration. This suggests the cardiac safety problem may be SOLVED.

### [Williams et al. 2025: Cortical Oscillations and Neural Complexity](../2025/Williams2025_Magnesium_Ibogaine_TBI.md)
Follow-up to 2023 paper. Confirms safety findings. Documents neuroplasticity effects via EEG. Validates the MISTIC protocol framework.

---

## Cross-References: Secondary RED Papers

These papers have a different primary category but contain clinically significant cardiac safety data. Grouped by primary category.

### ORANGE — Mechanisms & Pharmacology
- [Kontrimavičiūtė 2006 (LCMS Method)](../2006/Kontrimaviciute2006_LCMS_Method_Ibogaine_Noribogaine.md) — First validated LC-ESI-MS method for ibogaine/noribogaine quantification; applied to fatal poisoning case (blood levels 10–20× therapeutic)
- [Maciulaitis 2008](../2008/Maciulaitis2008_Ibogaine_Pharmacology_Narrative_Review.md) — Narrative review with PK data and safety concerns; early identification of cardiac risk mechanisms
- [Wasko et al. 2018](../2018/Wasko2018_Ibogaine_DARK_Classics_in_Chemical_Neuroscience.md) — DARK Classics series covering ibogaine pharmacology including cardiac channel interactions
- [Luz 2021](../2021/Luz2021_Toxicity_Therapeutic_Potential.md) — Toxicity review with cardiac safety discussion in pharmacological context
- [Martins 2022](../2022/Martins2022_Drug_Transporters_Ibogaine_PK.md) — Drug transporter interactions relevant to ibogaine/noribogaine distribution and cardiac exposure
- [Boukandou 2023](../2023/Boukandou2023_Mechanisms_Involved_Neuroprotection_Neurotoxicity_Iboga_Alkaloids.md) — Neurorestorative mechanisms review with cardiac safety considerations
- [Havel 2024 (Oxa-Iboga)](../2024/Havel2024_OxaIboga_Alkaloids_Lack_Cardiac_Risk_Disrupt_Opioid_Use.md) — Demonstrates oxa-iboga analogues LACK cardiac risk — validates safer-analogue development pathway
- [Knuijver 2024 (PK/PD)](../2024/Knuijver2024_Pharmacokinetics_Pharmacodynamics_Ibogaine_OUD_Patients.md) — Pharmacokinetic/pharmacodynamic modelling in OUD patients with cardiac monitoring data
- [Cameron 2021](../2021/Cameron2021_Tabernanthalog_Non_Hallucinogenic_Analog.md) — Tabernanthalog: non-hallucinogenic ibogaine analogue designed to avoid cardiac toxicity
- [Calvey 2026](../2026/Calvey2026_Neurorestorative_Properties_Ibogaine.md) — Neurorestorative review discussing cardiac safety in context of risk-benefit analysis

### BLUE — Outcomes & Efficacy
- [Noller 2017](../2017/Noller2017_Ibogaine_Opioid_12Month_Outcomes.md) — New Zealand 12-month outcomes study reporting cardiac monitoring data alongside efficacy
- [Brown 2018](../2018/Brown2018_OUD_Detoxification_Outcomes.md) — Observational OUD outcomes with safety reporting including cardiac adverse events
- [Davis 2020](../2020/Davis2020_SpecialOps_Veterans_Trauma.md) — Veterans study with cardiac monitoring documented
- [Davis 2023](../2023/Davis2023_Ibogaine_5MeO-DMT_for_SEALS.md) — Follow-up veterans study confirming cardiac safety profile under clinical conditions
- [Mosca 2023](../2023/Mosca2023_Ibogaine_Noribogaine_SUDs_Systematic_Review.md) — Systematic review of clinical outcomes incorporating cardiac safety evidence
- [Köck 2022](../2022/Kock2022_Systemic_Review_Clinical_Trials_Therapeutic_Applications_Ibogaine.md) — Systematic review including cardiac adverse event data
- [Canessa 2020](../2020/Canessa2020_Ibogaine_Noribogaine_in_Tx_Review_Safety_Efficacy.md) — Follow-up outcomes study with safety data

### GREEN — Protocols & Clinical Practice
- [GITA 2015 Guidelines](../Clinical_Guidelines/GITA2015_Clinical_Guidelines.md) — Industry gold standard for cardiac screening protocols
- [Rocha 2023: USP Safety Protocols](../2023/Rocha2023_USP_Safety_Protocols.md) — K+ 4.5-5.5, Mg 1.5-2.5 targets
- [Rocha 2023: Setting Factors](../2023/Rocha2023_Setting_Factors_Associated_With_Improved_Ibogaine_Safety.md) — Systematic review of what makes ibogaine safer
- [Bouso 2019](../2019/Bouso2019_Product_Quality.md) — Product quality analysis relevant to dose accuracy and cardiac risk
- [Cherian 2024 (Primer)](../2024/Cherian2024_Ibogaine_Primer_Clinicians.md) — Clinical primer including cardiac screening recommendations

### WHITE — History & Policy
- [Alper 2008](../2008/Alper2008_Ibogaine_Medical_Subculture.md) — Medical subculture history documenting early awareness of cardiac fatalities
- [Donnelly 2011](../2011/Donnelly2011_Ibogaine_Drug_Alcohol_Addiction_Legal.md) — Legal analysis referencing cardiac fatalities in regulatory context
- [Terasaki 2026](../2026/Terasaki2026_Ibogaine_OUD_Unrecognised_Risk.md) — Commentary documenting fatal fentanyl overdose in patient who rejected MOUD in favour of ibogaine; tolerance-loss-mediated death pathway distinct from cardiac toxicity but ibogaine-context fatality

---

## Clinical Implications Summary

| Risk Factor | Mitigation | Evidence |
|-------------|------------|----------|
| Hypokalemia | K+ supplementation to 4.5-5.5 mEq/L | Alper 2012, GITA 2015 |
| Hypomagnesemia | Mg supplementation to 1.5-2.5 mEq/L | MISTIC 2023-2024 |
| Baseline QTc >450ms | Exclusion criterion | GITA 2015 |
| Noribogaine persistence | 72h+ cardiac monitoring (up to 12 days in OD) | König-Hilber 2015, Henstra 2017 |
| Drug interactions (QT-prolonging) | Medication review/washout | GITA 2015, Pleškovič 2012 (amiodarone warning) |
| Co-intoxicants on board | Strict washout + urine drug screen | Corkery 2018 (≥12/33 deaths) |
| Pre-existing cardiac disease | ECG + cardiac history mandatory | Corkery 2018 (≥6/33 deaths), Warrick 2012 (AICD case) |
| CYP2D6 poor metaboliser status | Genotyping before treatment | Brunt 2026, Corkery 2018, Chen 2024 (3× AUC difference) |
| Pulmonary embolism risk | Mobility assessment, DVT history | Corkery 2018 (3/33 deaths) |
| Therapeutic dose (10 mg/kg) | Consider dose reduction or Mg co-admin | Knuijver 2021, Brunt 2026, Schep 2016 |
| Sub-therapeutic dose risk | Individual susceptibility overrides dose | Mestre 2024 (cardiac arrest at 2.6 mg/kg) |
| Normal screening ≠ zero risk | Continuous monitoring essential regardless | Shawn 2012, Vlaanderen 2014 |

---

## How We Got Here: The Cardiac Safety Story

**From mystery deaths to solved problem (1960s→2026)**

The most critical thread in ibogaine research. People died. We now know why—and how to prevent it.

### Act 1: Foundations (1960s–1999)
Before ibogaine entered human therapeutics, its toxicology was characterised in the laboratory. [Dhahir 1971](../1971/Dhahir1971_Ibogaine_Serotonin_Toxicity.md) established the LD₅₀ values (rat IP 145 mg/kg, mouse oral 263 mg/kg) and identified vagal cardiovascular mechanisms — data that would be cited for the next half-century. Deaths began occurring in underground treatment settings through the 1990s, but without systematic documentation or mechanistic understanding. The community knew something was wrong; the scientific framework to understand it did not yet exist.

### Act 2: First Documentation (2000–2008)
The first systematic case reports and forensic analyses emerged. [Marker 2002](../2002/Marker2002_Ibogaine_Related_Fatality.md) documented the earliest forensic ibogaine fatality — an NYC Medical Examiner case where ibogaine was initially identified as an "unknown substance," with extreme tissue concentrations (blood 9225 ng/mL) and the polydrug context that would become the field's recurring pattern. [Kontrimavičiūtė 2006](../2006/Kontrimaviciute2006_Tissue_Distribution_Ibogaine_Fatality.md) provided first human tissue distribution data. [Chèze 2008](../2008/Cheze2008_Ibogaine_Noribogaine_LC-MSMS_Drowning_Death.md) pioneered hair analysis for retrospective exposure detection. [Hoelen 2009](../2009/Hoelen2009_Long_QT_Ibogaine.md) brought ibogaine cardiotoxicity to mainstream medicine via the *NEJM* (QTc 616 ms).

[Maas & Strubelt 2006](../2006/Maas2006_Cardiac_Fatalities_Autonomic_Dysfunction.md) proposed the **first cardiac mechanism hypothesis**: autonomic nervous system dysregulation — sympathetic/parasympathetic imbalance triggering ventricular fibrillation via the cerebellar fastigial nucleus. Crucially, they identified Gabonese Bwiti ritual practices (sustained right-hemispheric trance, theta-inducing music, days-long isolation from startle stimuli) as a sophisticated cardioprotective protocol developed from 100,000+ initiations. The autonomic hypothesis would later be complemented — not replaced — by the direct hERG blockade mechanism (Act 4).

### Act 3: Epidemiology (2012–2018)
[Alper 2012](../2012/Alper2012_Ibogaine_Fatalities.md) delivered the first systematic review: **19 deaths documented**, mortality rate 1:427. Critical finding: 100% of cases with documented electrolytes showed **hypokalemia**. The electrolyte connection emerged. Case reports accumulated rapidly: [Paling 2012](../2012/Paling2012_Life_Threatening_Complications.md) (QTc >700 ms, TdP), [Pleškovič 2012](../2012/Pleskovic2012_Ibogaine_Ventricular_Tachyarrhythmias.md) (5 VF + 3 VT episodes over 48h), [Shawn 2012](../2012/Shawn2012_Ibogaine_TdP_VT.md) (TdP despite normal screening), [Warrick 2012](../2012/Warrick2012_Ibogaine_Fatality.md) (fatality with pre-existing AICD), [Asúa 2013](../2013/Asua2013_Ibogaine_Toxicity_UK_Case.md) (first UK case), [Jalal 2013](../2013/Jalal2013_Ibogaine_Death_Heroin_Case.md), [Papadodima 2013](../2013/Papadodima2013_Ibogaine_Sudden_Death_Case.md), [Vlaanderen 2014](../2014/Vlaanderen2014_Cardiac_Arrest_Ibogaine.md) (healthy 26M, permanent brain injury).

[Corkery 2018](../2018/Corkery2018_Ibogaine_Benefits_Dangers_Fatalities.md) extended the series to **33 deaths** (1990–2015), adding 14 cases including 5 previously unpublished UK coroner records. Established the risk triad (cardiac disease, co-intoxicants, CYP2D6 vulnerability) and the most comprehensive contraindication list in the literature.

**The death-to-treatment ratio — an epistemic arc.** The widely cited 1:427 ratio (Alper et al. 2008, via Corkery 2018) was calculated when the underground treatment population was still estimable — 3,414 treatment episodes between 1989–2006. Corkery 2018 formalised and cited it while noting it was already becoming obsolete as treatment moved beyond trackable settings. [Kock 2022](../2022/Kock2022_Systemic_Review_Clinical_Trials_Therapeutic_Applications_Ibogaine.md) abandoned ratio calculation entirely — the denominator is now untraceable. Modern literature ([Esperança 2026](../2026/Esperanca2026_Cardiac_Safety_Translational_Perspectives_Scoping_Review.md), [Chen 2024](../2024/Chen2024_RIVM_Iboga_Risk_Assessment.md)) focuses on mechanistic risk (hERG blockade, QTc prolongation) rather than statistical probability. The ratio is historical, not current — though given that many thousands of treatments have occurred at regulated clinics worldwide while the numerator has crept up by single digits, the true ratio has almost certainly improved. It simply can no longer be calculated. For the deduplicated mortality count that replaces ratio-based thinking, see [RED_Fatalities_Hub](RED_Fatalities_Hub.md).

### Act 4: The Mechanism (2012–2017)
The hERG convergence. [Koenig 2012](../2012/Koenig2012_Ibogaine_hERG_Cardiac_Arrhythmia_Risk.md) published the first IC₅₀ (3.9 μM), placing ibogaine alongside withdrawn drugs. [Koenig 2013](../2013/Koenig2013_Ibogaine_Cardiac_Ion_Channel_Profile.md) mapped the full cardiac ion channel profile and explained the guinea pig paradox. [Thurner 2014](../2014/Thurner2014_hERG_Channel_Block_Ibogaine.md) resolved the molecular mechanism to the Y652/F656 binding pocket. [König-Hilber 2015](../2015/Koenig2015_Cardiac_Mechanisms.md) synthesised the mechanistic picture. [Alper 2016](../2016/Alper2016_hERG_Blockade.md) provided the definitive IC₅₀ values (ibogaine 4.09 μM, noribogaine 2.86 μM, 18-MC >50 μM). [Rubi 2017](../2017/Rubi2017_hERG_iPSC_Cardiomyocytes.md) closed the loop with human iPSC-cardiomyocyte proof. Mechanism: understood.

### Act 5: Risk Quantification (2015–2021)
The clinical and computational data converged. [Schep 2016](../2016/Schep2016_Ibogaine_Safe_Dose.md) quantified the dose paradox (safe: 0.87 mg/kg; therapeutic: 6–30 mg/kg). [Litjens 2016](../2016/Litjens2016_How_Toxic_Is_Ibogaine.md) synthesised the toxicology. [Glue 2016](../2016/Glue2016_Noribogaine_Opioid_Patients_Safety.md) measured the concentration-QTc relationship (0.17 ms/ng/mL). [Henstra 2017](../2017/Henstra2017_Ibogaine_Noribogaine_Toxicokinetics_Cardiac.md) revealed noribogaine's extreme tissue sequestration (t½ 2,540h in overdose). [Hildyard 2015](../2015/Hildyard2015_QT_Prolongation_TdP_Ibogaine.md) and [Grogan 2019](../2019/Grogan2019_Seizures_QT_Prolongation_Cardiac.md) demonstrated acute magnesium rescue. [Shi 2021](../2021/Shi2021_NAM_Ibogaine_Cardiotoxicity.md) computationally validated the threshold (BMDL₁₀ ~1.4 mg/kg). [Knuijver 2021](../2021/Knuijver2021_Safety_Opioid_Detox.md) showed hospital monitoring prevents fatalities but NOT dangerous QTc prolongation (50% >500 ms).

### Act 6: Regulatory and Continuing Deaths (2024–2025)
[Chen 2024 (RIVM)](../2024/Chen2024_RIVM_Iboga_Risk_Assessment.md): **No safe dose derivable.** 34 deaths tabulated. Advises against consumer use. But deaths continued: [Mestre 2024](../2024/Mestre2024_Cardiac_Arrest_Case_Report.md) (cardiac arrests at merely 2.6 mg/kg test dose), [Edwards 2025](../2025/Edwards2025_UK_NPIS_Ibogaine_Toxicity_Case_Series.md) (UK series: 6/7 cardiotoxicity, 2 brain injuries). [Aćimović 2021](../2021/Acimovic2021_Ibogaine_Death_Case_Report.md) added to the forensic record.

### Act 7: The Solution and Synthesis (2023–2026)
[Cherian 2024 (MISTIC)](../2024/Cherian2024_Magnesium_Ibogaine_TBI.md) — **PARADIGM SHIFT**: Magnesium co-administration shows **ZERO clinically significant QTc prolongation**. From "managing risk" to potentially "eliminating risk." [Rocha 2025](../2025/Rocha2025_PhD_Ibogaine_Alcohol_AUD.md) provides the unprotected comparator data that makes MISTIC's results so compelling. [Brunt 2026](../2026/Brunt2026_Cardiovascular_Complications_Review.md) consolidates the evidence: therapeutic doses exceed cardiac safety thresholds by 10×, CYP2D6 genotyping recommended, safer analogues charted. [Esperança 2026](../2026/Esperanca2026_Cardiac_Safety_Translational_Perspectives_Scoping_Review.md) — the most current scoping review — positions ibogaine as a lead compound for next-generation therapeutics rather than a viable endpoint in its current form.

**The arc in one line**: *Toxicology (Dhahir 1971) → First deaths → Epidemiology (Alper/Corkery) → hERG mechanism (Koenig/Thurner/Rubi) → Dose paradox (Schep/Shi) → Noribogaine dominance (Glue/Henstra) → Regulatory verdict: no safe dose (RIVM) → Solution: Mg cardioprotection (MISTIC) → Synthesis: lead compound, not endpoint (Esperança)*

---

> [!warning] Never Forget
> Every death in this literature was preventable with proper screening and monitoring. The evidence shows controlled clinical settings achieve ZERO serious cardiac events. The deaths occur in uncontrolled settings without protocols. But even the best screening cannot eliminate all risk ([Shawn 2012](../2012/Shawn2012_Ibogaine_TdP_VT.md)); continuous cardiac monitoring and magnesium co-administration remain essential.

---

## Related Hubs

- **[RED_Fatalities_Hub](RED_Fatalities_Hub.md)** — Deduplicated mortality count, citation chain map, grey literature sources, and risk factor patterns
- **[GREEN_Clinical_Protocols_Hub](GREEN_Clinical_Protocols_Hub.md)** — The protocols that prevent what this hub documents: screening, contraindications, monitoring
- **[ORANGE_Mechanisms_Hub](ORANGE_Mechanisms_Hub.md)** — The receptor pharmacology underlying hERG blockade and cardiotoxicity
- **[BLUE_Outcomes_Hub](BLUE_Outcomes_Hub.md)** — The clinical outcomes that justify accepting cardiac risk under controlled conditions
- **[Hub_PK-PD_Synthesis](Hub_PK-PD_Synthesis.md)** — Pharmacokinetic/pharmacodynamic data: dosing, noribogaine persistence, CYP2D6 variability
- **[Kenneth_Alper_MOC](../MOCs/Kenneth_Alper_MOC.md)** — Alper's contributions spanning fatality documentation, hERG characterisation, and clinical overview

---

*Last updated: 2026-03-21*