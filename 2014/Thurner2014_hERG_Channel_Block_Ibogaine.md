---
title: "Mechanism of hERG Channel Block by the Psychoactive Indole Alkaloid Ibogaine"
authors:
  - "Thurner, Patrick"
  - "Stary-Weinzinger, Anna"
  - "Gafar, Hend"
  - "Gawali, Vaibhavkumar S."
  - "Kudlacek, Oliver"
  - "Zezula, Juergen"
  - "Hilber, Karlheinz"
  - "Boehm, Stefan"
  - "Sandtner, Walter"
  - "Koenig, Xaver"
year: 2014
category: RED
tags:
  - topic/cardiac
  - mechanism/herg-blockade
  - mechanism/ion-channel
  - method/in-vitro
  - topic/toxicity
secondary_categories: [ORANGE]
key_findings: "Ibogaine blocks hERG channels from cytosolic side via open/inactivated-state binding at Y652/F656 residues; IC₅₀ ~1-4 μM; F656A mutation reduces potency 50-fold; inactivation-deficient mutant equally sensitive."
source_pdf: "2014/Thurner2014_hERG_Channel_Block_Ibogaine.pdf"
doi: "10.1124/jpet.113.209643"
pmid: "24307198"
journal: "Journal of Pharmacology and Experimental Therapeutics"
issn: "0022-3565"
publication_date: "2014-02-01"
document_type: in-vitro
clinical_significance: landmark
aliases:
  - "Thurner 2014"
  - "hERG channel block mechanism ibogaine"
evidence_level: in-vitro
qtc_data: false
electrolyte_data: false
herg_data: true
contraindications:
  - "Pre-existing hERG channel dysfunction"
  - "Concomitant use of other hERG-blocking drugs"
  - "Conditions favouring intracellular acidosis (increases ibogaine trapping and hERG block)"
dosing_range: "IC₅₀ ~1–4 μM (hERG wild-type); standard test concentration 3 μM — in vitro"
route: not-applicable
open_access: false
publisher: "ASPET"
body_format: vault-analytical
licence_type: all-rights-reserved
licence_verified: true
---

# Mechanism of hERG Channel Block by the Psychoactive Indole Alkaloid Ibogaine

**Citation:** Thurner, P., Stary-Weinzinger, A., Gafar, H., Gawali, V.S., Kudlacek, O., Zezula, J., Hilber, K., Boehm, S., Sandtner, W., & Koenig, X. (2014). Mechanism of hERG Channel Block by the Psychoactive Indole Alkaloid Ibogaine. *Journal of Pharmacology and Experimental Therapeutics*, 348(2), 346–358. https://doi.org/10.1124/jpet.113.209643

## Abstract

Ibogaine is a psychoactive indole alkaloid whose use as an antiaddictive agent has been accompanied by QT prolongation and cardiac arrhythmias, most likely caused by human ether-à-go-go-related gene (hERG) potassium channel inhibition. The authors studied the interaction of ibogaine with hERG channels heterologously expressed in mammalian tsA-201 cells. Key findings: currents were blocked regardless of extracellular or intracellular application; extent of inhibition was determined by relative pH values; block occurred during activation (not at rest); with increasing depolarisations, block grew and developed faster. Steady-state activation and inactivation shifted to more negative potentials. Deactivation was slowed, whereas inactivation was accelerated. Mutations in the canonical binding site (Y652A and F656A) reduced potency, whereas an inactivation-deficient double mutant (G628C/S631C) was equally sensitive. Molecular docking indicated binding within the inner cavity. A kinetic model revealed preferential binding to the open and inactivated state (OIB model).

## Key Findings

- **IC₅₀ values:** ~1 μM (wild-type, tail current) to ~4 μM (wild-type, sustained current at +10 mV); consistent with earlier reports (Koenig et al., 2012, 2013)
- **Binding site:** Y652 and F656 residues on S6 pore-lining domain — the canonical hERG blocker binding pocket
  - Y652A mutation: 5-fold reduction in potency (IC₅₀ ~5 μM)
  - F656A mutation: 50-fold reduction in potency (IC₅₀ ~50 μM)
- **State dependence:** Ibogaine binds to **open and inactivated** states (OIB model, best fit); does NOT block resting/closed channels
- **Inactivation-deficient mutant (G628C/S631C):** Equally sensitive to ibogaine as wild-type — inactivation is not a prerequisite for block, though it contributes to the blocking mechanism
- **Cytosolic action:** Ibogaine crosses the membrane in its neutral form (pKₐ ~8.1) and acts from the intracellular side
  - Extracellular alkalinisation (higher pH) enhances block (more neutral, membrane-permeable form)
  - Intracellular acidification enhances block (traps charged ibogaine in cytosol)
- **Gating effects:** Hyperpolarising shift in activation (V₀.₅ shifted from −10 to −19 mV at 3 μM) and inactivation (V₀.₅ shifted from −45 to −63 mV); deactivation slowed; inactivation accelerated
- **Frequency independence:** Block depends on pulse duration, not frequency — differs from amiodarone-type use-dependent block
- **Molecular docking:** Ibogaine binds central cavity of hERG; hydrophobic interactions with F656/Y652 aromatic rings; hydrogen bonds to selectivity filter S624

## Methodology

**Study design:** In vitro electrophysiology with molecular modelling

**Cell system:** tsA-201 cells transiently transfected with wild-type hERG (Kcnh2/Kv11.1) or mutant channels (Y652A, F656A, G628C/S631C)

**Techniques:**
- Whole-cell patch-clamp recordings at room temperature (22 ± 2°C)
- Multiple voltage protocols to assess activation, deactivation, inactivation, and frequency dependence
- pH manipulation experiments (pHₒ 6.8–8.2; pHᵢ 5.5–7.2)
- Intracellular ibogaine application via recording pipette (100 μM)
- Molecular drug docking using hERG homology model (Gold 4.0.1)
- Markov model kinetic fitting (Wang et al. 1997 base model, expanded with drug-bound states)
- Concentration-response curves fitted with Hill equation

**Drug:** Ibogaine hydrochloride; stock in 0.1% HCl; standard test concentration 3 μM

## Cardiac Safety Data

### hERG Block Parameters

| Parameter | Wild-type | Y652A | F656A | G628C/S631C |
|-----------|-----------|-------|-------|-------------|
| IC₅₀ (tail current) | ~1 μM | ~5 μM | ~50 μM | ~1 μM |
| IC₅₀ (sustained, +10 mV) | ~4 μM | — | — | — |
| Block at 3 μM (+10 mV) | >50% | Reduced | Greatly reduced | ~50% |

### Gating Modifications (3 μM ibogaine)

| Parameter | Control | Ibogaine | Change |
|-----------|---------|----------|--------|
| V₀.₅ activation (mV) | −10 ± 1 | −19 ± 2 | −9 mV shift |
| V₀.₅ inactivation (mV) | −45 ± 3 | −63 ± 2 | −18 mV shift |
| Deactivation τ (−50 mV) | Baseline | Significantly prolonged | Slowed |
| Inactivation τ (+20 mV) | Baseline | Significantly decreased | Accelerated |

### Clinical Relevance of IC₅₀

Therapeutic ibogaine plasma concentrations reach low micromolar range after standard doses (0.5–1 g); plasma protein binding ~65% (Koenig et al., 2013). The IC₅₀ of ~1–4 μM falls within or close to therapeutic free plasma concentrations — placing ibogaine in the high-risk category for QT prolongation per Redfern et al. (2003) classification.

## Clinical Implications

This paper provides the mechanistic foundation for understanding ibogaine's cardiac risk and has direct implications for ibogaine clinical practice:

1. **hERG block is the primary mechanism of QT prolongation** — not autonomic dysregulation as previously hypothesised (Maas & Strubelt, 2006). This shifts the safety paradigm from monitoring autonomic function to monitoring repolarisation.

2. **pH dependence is clinically actionable** — intracellular acidosis (from vomiting, dehydration, metabolic stress) would enhance ibogaine's hERG block. This provides a mechanistic rationale for aggressive electrolyte and hydration management during treatment.

3. **Drug interaction risk** — concomitant use of any other hERG-blocking medication (antipsychotics, certain antibiotics, antiemetics like ondansetron) creates additive QT prolongation risk. The shared Y652/F656 binding site means competitive or additive interactions are expected.

4. **No frequency dependence** — unlike amiodarone, ibogaine's block does not increase with heart rate. This means tachycardia does not provide a protective "washout" effect.

5. **Analogue development context** — the detailed binding site characterisation (Y652/F656) provides a structural template for designing ibogaine analogues that avoid hERG block (cf. 18-MC, oxa-iboga compounds).

## Limitations

- In vitro study in non-cardiac cells (tsA-201) — channel expression levels and cellular environment differ from native cardiomyocytes
- Room temperature recordings (~22°C) — hERG channel kinetics are temperature-dependent; IC₅₀ values may differ at physiological temperature (37°C)
- Only ibogaine tested; noribogaine (the primary long-lived metabolite, t₁/₂ ~28–49 hours) was not studied — noribogaine may contribute significantly to sustained QT prolongation
- Homology model used for docking, not a crystal/cryo-EM structure
- Plasma protein binding effects on free drug concentration not directly measured in this study

---

## See Also
- [Hoelen2009_Long_QT_Ibogaine](../2009/Hoelen2009_Long_QT_Ibogaine.md) — Clinical case confirming QT prolongation in humans
- [Alper2012_Ibogaine_Fatalities](../2012/Alper2012_Ibogaine_Fatalities.md) — Fatality analysis referencing cardiac mechanisms
- [Paling2012_Life_Threatening_Complications](../2012/Paling2012_Life_Threatening_Complications.md) — Cardiac complication case reports
- [Koenig2015_Cardiac_Mechanisms](../2015/Koenig2015_Cardiac_Mechanisms.md) — Follow-up from same group on cardiac mechanisms
- [Havel2024_OxaIboga_Alkaloids_Lack_Cardiac_Risk_Disrupt_Opioid_Use](../2024/Havel2024_OxaIboga_Alkaloids_Lack_Cardiac_Risk_Disrupt_Opioid_Use.md) — Analogue design avoiding hERG block
- [RED_Cardiac_Safety_Hub](../Hubs/RED_Cardiac_Safety_Hub.md) — Central hub for cardiac safety evidence
