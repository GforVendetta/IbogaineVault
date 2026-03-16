---
title: "Copyright N-gram Triage — 2026-03-15"
created: 2026-03-15
type: audit
---

# IbogaineVault Copyright N-gram Triage

**Date:** 2026-03-15
**Papers analysed:** 17
**Method:** 4/6/8-gram overlap (references stripped, tables stripped)

## Thresholds

| 4-gram overlap | Interpretation | Action |
|----------------|----------------|--------|
| < 0.20 | 🟢 Genuinely rewritten | Clear |
| 0.20 – 0.35 | 🟡 Moderate similarity | Likely OK |
| 0.35 – 0.50 | 🟠 Concerning | Manual review needed |
| > 0.50 | 🔴 Likely verbatim | Needs reconversion |

## Results (ranked by 4-gram overlap)

| Status | 4g | 6g | 8g | Words | ~Verbatim | Publisher | File |
|--------|-----|-----|-----|-------|-----------|-----------|------|
| 🔴 VERBATIM | 0.927 | 0.889 | 0.854 | 4,274 | ~3,753 | SAGE | Knuijver2024_Pharmacokinetics_Pharmacodynamics_Ibogaine_OUD_Patients |
| 🔴 VERBATIM | 0.914 | 0.874 | 0.843 | 4,495 | ~4,042 | T&F | Wilson2020_Novel_Tx_OUD_Ibogaine_Iboga_Case_Study |
| 🔴 VERBATIM | 0.897 | 0.846 | 0.794 | 4,143 | ~3,540 | Wiley | Glick1999_18MC_Review_CNS_Drugs |
| 🔴 VERBATIM | 0.798 | 0.747 | 0.702 | 3,630 | ~2,695 | Elsevier | Paskulin2010_Yeast_Enzymes_Ibogaine_Adaptation_ATP |
| 🔴 VERBATIM | 0.771 | 0.688 | 0.622 | 5,368 | ~3,867 | Oxford | Hearn1995_Noribogaine_Metabolite |
| 🔴 VERBATIM | 0.748 | 0.663 | 0.589 | 4,554 | ~2,896 | Wiley | Mundey2000_Ibogaine_18MC_Smooth_Muscle |
| 🔴 VERBATIM | 0.665 | 0.607 | 0.558 | 4,698 | ~2,968 | Springer Nature | Cherian2024_Magnesium_Ibogaine_TBI |
| 🔴 VERBATIM | 0.660 | 0.587 | 0.528 | 1,491 | ~961 | T&F | Davis2023_Ibogaine_5MeO-DMT_for_SEALS |
| 🟠 CONCERNING | 0.429 | 0.352 | 0.303 | 2,820 | ~1,126 | Elsevier | Arias2023_Catharanthine_18-MC |
| 🟠 CONCERNING | 0.404 | 0.304 | 0.244 | 1,856 | ~736 | ACS | Bhat2020_Tropane_Ibo_Analog_SERT_DAT |
| 🟠 CONCERNING | 0.373 | 0.303 | 0.262 | 1,632 | ~596 | Springer Nature | Iyer2025_Modular_Synthesis_Nature_Chemistry |
| 🟢 REWRITTEN | 0.196 | 0.168 | 0.149 | 1,763 | ~336 | Wiley | Carnicella2010_Noribogaine_18MC_GDNF |
| 🟢 REWRITTEN | 0.157 | 0.122 | 0.116 | 2,940 | ~449 | ACS | Hwu2025_Matrix_Pharmacology_VMAT2_SERT |
| 🟢 REWRITTEN | 0.155 | 0.132 | 0.121 | 2,003 | ~305 | Wiley | Knuijver2021_Safety_Opioid_Detox |
| 🟢 REWRITTEN | 0.153 | 0.115 | 0.095 | 1,848 | ~275 | Elsevier | Arias2010_Interactions_Ibogaine_NicotinicAChR_Human |
| 🟢 REWRITTEN | 0.114 | 0.083 | 0.073 | 2,288 | ~257 | RSC | Iyer2019_Iboga_Enigma_Chemistry_Neuropharmacology_Alkaloids_Analogs |
| 🟢 REWRITTEN | 0.012 | 0.003 | 0.001 | 2,597 | ~31 | Wiley | Mash2000_Ibogaine_Pharmacokinetics_Safety |

## Summary

- 🔴 **Likely verbatim (>0.50):** 8 papers — NEED RECONVERSION
- 🟠 **Concerning (0.35–0.50):** 3 papers — manual review
- 🟡 **Moderate (0.20–0.35):** 0 papers — likely OK
- 🟢 **Rewritten (<0.20):** 6 papers — clear
- **Total verbatim-equivalent words in 🔴+🟠:** ~27,180
