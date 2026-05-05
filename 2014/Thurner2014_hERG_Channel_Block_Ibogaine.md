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
secondary_categories: [ORANGE]
tags:
  - topic/cardiac
  - mechanism/herg-blockade
  - mechanism/ion-channel
  - method/in-vitro
  - topic/toxicity
key_findings: "hERG IC₅₀ ~1.0 μM (Fig 5C tail) and ~1.2 μM (Fig 5B sustained at +10 mV); ~3–4 μM figures elsewhere cite Koenig 2012/2013. Y652A 5-fold + F656A 50-fold reductions. Best fit OIB; closed-state binding negligible (COIB null vs OIB, P>0.05)."
source_pdf: "2014/Thurner2014_hERG_Channel_Block_Ibogaine.pdf"
doi: "10.1124/jpet.113.209643"
pmid: "24307198"
journal: "Journal of Pharmacology and Experimental Therapeutics"
issn: "0022-3565"
publication_date: "2014-02-01"
document_type: in-vitro
clinical_significance: high
aliases:
  - "Thurner 2014"
  - "hERG channel block mechanism ibogaine"
evidence_level: in-vitro
qtc_data: false
electrolyte_data: false
herg_data: true
contraindications: []
dosing_range: "IC₅₀ ~1.0–1.2 μM (hERG wild-type, this paper's protocols); 3 μM standard test concentration — in vitro"
route: not-applicable
open_access: false
publisher: "ASPET"
body_format: vault-analytical
licence_type: all-rights-reserved
licence_verified: true
---

# Mechanism of hERG Channel Block by the Psychoactive Indole Alkaloid Ibogaine

**Citation:** Thurner, P., Stary-Weinzinger, A., Gafar, H., Gawali, V.S., Kudlacek, O., Zezula, J., Hilber, K., Boehm, S., Sandtner, W., & Koenig, X. (2014). Mechanism of hERG Channel Block by the Psychoactive Indole Alkaloid Ibogaine. *Journal of Pharmacology and Experimental Therapeutics*, 348(2), 346–358. <https://doi.org/10.1124/jpet.113.209643>

## Abstract

Ibogaine is a psychoactive indole alkaloid whose use as an antiaddictive agent has been accompanied by QT prolongation and cardiac arrhythmias, most likely caused by human ether-à-go-go-related gene (hERG) potassium channel inhibition. The authors studied the interaction of ibogaine with hERG channels heterologously expressed in mammalian tsA-201 cells. Key findings: currents were blocked regardless of extracellular or intracellular application; extent of inhibition was determined by relative pH values; block occurred during activation (not at rest); with increasing depolarisations, block grew and developed faster. Steady-state activation and inactivation shifted to more negative potentials. Deactivation was slowed, whereas inactivation was accelerated. Mutations in the canonical binding site (Y652A and F656A) reduced potency, whereas an inactivation-deficient double mutant (G628C/S631C) was equally sensitive. Molecular docking indicated binding within the inner cavity. A kinetic model revealed preferential binding to the open and inactivated state (OIB model).

## Key Findings

- **IC₅₀ values (this paper's own protocols):** ~1.0 μM (wild-type, tail current at −50 mV; Fig 5C) and ~1.2 μM (wild-type, sustained current at +10 mV; Fig 5B) — protocol-dependent within the same paper. Note: the ~3 μM (Results) and ~4 μM (Introduction) values referenced elsewhere in this paper are *citations* of prior work by the same group (Koenig et al., 2012, 2013), not measurements generated in this paper.
- **Binding site:** Y652 and F656 residues on S6 pore-lining domain — the canonical hERG blocker binding pocket
  - Y652A mutation: 5-fold reduction in potency (IC₅₀ \~5 μM)
  - F656A mutation: 50-fold reduction in potency (IC₅₀ \~50 μM)
- **State dependence:** Ibogaine binds to **open and inactivated** states (OIB model, best fit); does NOT block resting/closed channels. A closed-state-binding extension of the model (COIB) did not significantly improve fit over OIB (P > 0.05; Fig 8B), with the closed-state K_d ~690 μM ("data not shown") — confirming negligible closed-state binding
- **Inactivation-deficient mutant (G628C/S631C):** Equally sensitive to ibogaine as wild-type — inactivation is not a prerequisite for block, though it contributes to the blocking mechanism
- **Cytosolic action:** Ibogaine crosses the membrane in its neutral form (pKₐ \~8.1) and acts from the intracellular side
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
|---|---|---|---|---|
| IC₅₀ (tail current at −50 mV; Fig 5C) | ~1.0 μM | ~5 μM | ~50 μM | — |
| IC₅₀ (sustained current at +10 mV; Fig 5B) | ~1.2 μM | — | — | ~1 μM |
| Block at 3 μM (+10 mV) | >50% | Reduced | Greatly reduced | ~50% |

*Note: the ~3 μM (Results) and ~4 μM (Introduction) IC₅₀ values referenced elsewhere in this paper are cited from prior work by the same group (Koenig et al., 2012, 2013), not generated in this paper's own protocols.*

### Gating Modifications (3 μM ibogaine)

| Parameter | Control | Ibogaine | Change |
|---|---|---|---|
| V₀.₅ activation (mV) | −10 ± 1 | −19 ± 2 | −9 mV shift |
| V₀.₅ inactivation (mV) | −45 ± 3 | −63 ± 2 | −18 mV shift |
| Deactivation τ (−50 mV) | Baseline | Significantly prolonged | Slowed |
| Inactivation τ (+20 mV) | Baseline | Significantly decreased | Accelerated |

### Multi-Channel Selectivity

Thurner et al. (Discussion) cite the following multi-channel selectivity profile from their prior work (Koenig et al., 2013); these IC₅₀ values are *not* generated by this paper's own protocols:

| Channel | IC₅₀ | Source |
|---|---|---|
| hERG (Kv11.1) | ~1.0–1.2 μM | This paper (Fig 5B/5C) |
| Nav1.5 | 142 μM | Cited from Koenig et al., 2013 |
| Cav1.2 | 163 μM | Cited from Koenig et al., 2013 |
| Kv7.1 / I_Ks | >>100 μM | Discussion ("unpublished data") |

The authors note in the Discussion that on isolated guinea pig cardiomyocytes, the action-potential-prolonging effect of hERG block at clinically relevant ibogaine concentrations was *counteracted* by simultaneous calcium-channel block — raising the possibility of partial mechanistic compensation between hERG inhibition (pro-arrhythmic) and Cav1.2 inhibition (anti-arrhythmic) at higher concentrations. Note: this cardiomyocyte experiment is from the Koenig 2013 paper, not this one.

### Clinical Relevance of IC₅₀

Therapeutic ibogaine plasma concentrations reach low micromolar range after standard doses (0.5–1 g); plasma protein binding ~65% (Koenig et al., 2013). The IC₅₀ of ~1.0–1.2 μM (this paper's own protocols) falls within therapeutic free plasma concentrations — placing ibogaine in the high-risk category for QT prolongation per Redfern et al. (2003) classification.

## Clinical Implications

This paper provides the mechanistic foundation for understanding ibogaine's cardiac risk and has direct implications for ibogaine clinical practice:

1. **hERG block is the primary mechanism of QT prolongation.** An earlier hypothesis by Maas & Strubelt (2006) had proposed autonomic dysfunction as the cause of ibogaine-related sudden cardiac death; Thurner et al. cite Maas & Strubelt (2006) — alongside Hoelen (2009) and Alper (2012) — in support of the broader claim that these deaths are arrhythmic, then provide the direct mechanistic basis (hERG block) for that arrhythmia. The data shift the safety paradigm from monitoring autonomic function to monitoring repolarisation.

2. **pH dependence is clinically actionable** — intracellular acidosis (from vomiting, dehydration, metabolic stress) would enhance ibogaine's hERG block. This provides a mechanistic rationale for aggressive electrolyte and hydration management during treatment.

3. **Drug interaction risk** — concomitant use of any other hERG-blocking medication (antipsychotics, certain antibiotics, antiemetics like ondansetron) creates additive QT prolongation risk. The shared Y652/F656 binding site means competitive or additive interactions are expected.

4. **No frequency dependence** — unlike amiodarone, ibogaine's block does not increase with heart rate. This means tachycardia does not provide a protective "washout" effect.

5. **Analogue development context** — the detailed binding site characterisation (Y652/F656) provides a structural template for designing ibogaine analogues that avoid hERG block (cf. 18-MC, oxa-iboga compounds).

6. **Mechanistic placement on the torsadogenic spectrum** — the authors group ibogaine with cisapride, azimilide, and halofantrine on the basis of shared gating alterations (left-shifted activation/inactivation, slowed deactivation, accelerated inactivation), all of which are low-micromolar hERG blockers with established torsadogenic profiles. Cisapride was withdrawn from major markets specifically for torsade de pointes. By contrast, the authors note that chlorpromazine and ketoconazole — which bind hERG only in the closed conformation (Dumaine et al., 1998; Thomas et al., 2003) — display "little torsadogenic propensity" (Reilly et al., 2000; Redfern et al., 2003). The state-dependence of binding therefore tracks clinical risk, and the open/inactivated-state binding established here places ibogaine in the higher-risk grouping.

7. **Epidemiological context cited by the authors** — the Discussion frames the mechanistic findings against ~5000 ibogaine exposures between 1990 and 2006 (cited from Alper et al., 2008), 11 ibogaine-related deaths in that period (~0.2%, Alper et al., 2008), and eight case reports of ibogaine-triggered cardiac arrhythmias and sudden cardiac death "in the past 2 years" prior to publication (Paling et al., 2012; Pleskovic et al., 2012; Jalal et al., 2013; Mazoyer et al., 2013; Papadodima et al., 2013; Vlaanderen and Martial, 2013). These figures originate in the cited papers, not in Thurner et al.

## Limitations

- In vitro study in non-cardiac cells (tsA-201) — channel expression levels and cellular environment differ from native cardiomyocytes
- Room temperature recordings (\~22°C) — hERG channel kinetics are temperature-dependent; IC₅₀ values may differ at physiological temperature (37°C)
- Only ibogaine tested; noribogaine (the primary long-lived metabolite, t₁/₂ \~28–49 hours) was not studied — noribogaine may contribute significantly to sustained QT prolongation
- Homology model used for docking, not a crystal/cryo-EM structure
- Plasma protein binding effects on free drug concentration not directly measured in this study
- **Source-internal inconsistencies (vault-flagged):** (a) wild-type IC₅₀ varies between Fig 5B (1.2 μM, sustained current at +10 mV) and Fig 5C (1.0 μM, tail current at −50 mV) — likely protocol-dependent but not explained by the authors; (b) prior Koenig work is cited as 4 μM in the Introduction but "about 3 μM" in the Results; (c) Table 1's caption claims values were "rounded to four significant digits", but printed entries (e.g. 703.6111, 189.4601, 205.9105) actually carry seven significant digits and conform to four decimal places.

---

## See Also

- [Hoelen2009_Long_QT_Ibogaine](../2009/Hoelen2009_Long_QT_Ibogaine.md) — Clinical case confirming QT prolongation in humans
- [Alper2012_Ibogaine_Fatalities](../2012/Alper2012_Ibogaine_Fatalities.md) — Fatality analysis referencing cardiac mechanisms
- [Paling2012_Life_Threatening_Complications](../2012/Paling2012_Life_Threatening_Complications.md) — Cardiac complication case reports
- [Koenig2015_Cardiac_Mechanisms](../2015/Koenig2015_Cardiac_Mechanisms.md) — Follow-up from same group on cardiac mechanisms
- [Havel2024_OxaIboga_Alkaloids_Lack_Cardiac_Risk_Disrupt_Opioid_Use](../2024/Havel2024_OxaIboga_Alkaloids_Lack_Cardiac_Risk_Disrupt_Opioid_Use.md) — Analogue design avoiding hERG block
- [RED_Cardiac_Safety_Hub](../Hubs/RED_Cardiac_Safety_Hub.md) — Central hub for cardiac safety evidence
