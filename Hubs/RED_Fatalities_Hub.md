---
title: "🔴 Fatalities Hub"
category: RED
tags:
  - meta/moc
  - meta/hub
  - topic/cardiac
  - topic/toxicity
  - topic/adverse-event
aliases: ["Fatalities Hub", "Mortality Count", "Death Count"]
contraindications: []
qtc_data: false
electrolyte_data: false
herg_data: false
---

## Purpose

This hub is a **quantitative mortality counting instrument** within the IbogaineVault. It tracks every known ibogaine-associated death, maps the citation chains between cumulative reviews, and makes the deduplication methodology transparent and auditable.

It does not narrate cardiac mechanisms, discuss pharmacological pathways, or recommend clinical protocols. If you need the story of cardiac safety, see [RED_Cardiac_Safety_Hub](RED_Cardiac_Safety_Hub.md). If you need to validate a mortality count, you're in the right place.

The deduplicated count below synthesises 33 papers reporting mortality data (13 cumulative reviews, 12 discrete case reports, 8 incidental mentions) into a single auditable figure. Every inclusion, exclusion, and edge case is flagged with rationale.

## Methodology

The IbogaineVault tags every paper that reports deaths with a `mortality_scope` enum: **cumulative-review** (papers that tally deaths across the literature), **discrete-cases** (papers reporting unique incidents), and **incidental** (papers that mention deaths counted elsewhere). This enum prevents the single most dangerous analytical error in ibogaine mortality research: naively summing overlapping counts.

The deduplication algorithm proceeds in four steps:

1. **Group by scope.** 13 cumulative reviews, 12 discrete-case papers, 8 incidental papers.
2. **Establish baseline.** Identify the most comprehensive cumulative review as the anchor count. Kock2022 is the baseline: 38 ibogaine-associated deaths through 7 December 2020, derived via PRISMA-compliant search (PubMed + EMBASE), cross-referenced against Alper2012, Corkery2018, Koenig2015, and Litjens2016.
3. **Add post-baseline discrete cases only.** For each discrete-case paper, verify the death occurred after Kock's cut-off date or was demonstrably absent from the review.
4. **Exclude incidental papers.** These mention deaths already counted in cumulative reviews.

**Why not Chen2024 as baseline?** Despite later publication (2024 vs 2022), Chen2024 counts fewer deaths (34 vs 38) because its "sudden death" framing excludes deaths from haemorrhagic pancreatitis, mesenteric thrombosis, and duodenal ulcer complications that Kock included. A later publication date does not guarantee a more comprehensive count.

**Why not Esperanca2026?** Esperanca2026 reports 19 deaths but did not conduct its own case enumeration — it cites Alper2012's figure directly. It is **non-independent** and cannot serve as a baseline or additive source.

## Deduplicated Mortality Count

> [!SUMMARY] **~45 ibogaine-associated deaths**
> **Baseline:** 38 deaths (Kock2022, literature through 7 Dec 2020)
> **Post-baseline additions:** +7 deaths (2021–2026)
> **Excluded:** 1 death (Terasaki2026 — fentanyl OD, not ibogaine-associated)

**Breakdown of post-baseline additions:**

- Evans2026: 5 deaths across multiple clinics (2024–2026)
- Acimovic2021: 1 death, Serbia (flagged — see §6)
- Busby2024: 1 death, Cancún, spring 2022

**Confidence:** Moderate-to-high on the baseline (Kock2022 cross-referenced four prior systematic reviews). High on each post-baseline addition (individually verified against baseline coverage).

**Coverage gap:** This count almost certainly undercounts total ibogaine-associated deaths. Unreported fatalities in unregulated settings — particularly pre-2020 Africa, Central America, and underground treatment networks — represent a known gap. Community sources (MyEboga2018) note that reporting became unreliable from approximately 2006 as providers multiplied and treatment moved underground.

## Cumulative Reviews Timeline

All 13 papers with `mortality_scope: cumulative-review`, ordered chronologically. These counts **overlap** — they must not be summed.

| Paper | Year | Count | Coverage End | Independence Assessment |
|-------|------|-------|-------------|------------------------|
| Maas2006 | 2006 | 8 | ~2005 | Independent — earliest cumulative count |
| Alper2008 | 2008 | 11 | ~2006 | Independent — source of the 1:427 death-to-treatment ratio |
| Donnelly2011 | 2011 | 9 | ~2010 | Independent — lower count reflects narrower scope |
| Alper2012 | 2012 | 19 | ~2008 | Independent — foundational IRB-approved forensic case series |
| Koenig2015 | 2015 | 22 | ~2014 | Independent — extends prior literature |
| Litjens2016 | 2016 | 27 | ~2015 | Independent — extends prior literature |
| Schep2016 | 2016 | 19 | ~2015 | Independent — toxicological focus |
| Corkery2018 | 2018 | 33 | ~2017 | Independent — extends Alper2012 by +14 from coroners' records + literature |
| MyEboga2018 | 2018 | 12 | ~2010 | Upstream community source (Lee Albert, MyEboga.com); all 12 subsumed in Kock2022 |
| Ona2021 | 2021 | 1 | — | Single-case within a broader review |
| **Kock2022** | **2022** | **38** | **7 Dec 2020** | **BASELINE — PRISMA-compliant, cross-refs 4 prior reviews, most comprehensive** |
| Chen2024 | 2024 | 34 | ~2021 | Independent enumeration but narrower "sudden death" criteria — undercounts |
| Esperanca2026 | 2026 | 19 | Refs Alper2012 | **NON-INDEPENDENT** — explicitly cites Alper2012's 19-death figure |

## Citation Chain Map

Understanding which reviews subsume which earlier reports is essential for avoiding double-counting. The ibogaine mortality literature has a single dominant chain and several branches.

### Main chain

> **Kock2022** (38) ← **Corkery2018** (33) ← **Alper2012** (19) ← **Alper2008** (11) ← **Maas2006** (8)

Each link represents explicit subsumption: Kock2022 deduplicated against Corkery2018 and three other reviews. Corkery2018 extended Alper2012 by adding 14 deaths from UK coroners' records and subsequent literature. Alper2012 built on the earlier Alper2008 consecutive case series. Alper2008 extended the Maas2006 count. Every death in a downstream review is already captured in Kock2022's 38.

### Branch: MyEboga2018 (community source)

MyEboga2018 compiled 12 cases from community reporting (Lee Albert, MyEboga.com). This non-academic source fed into both Corkery2018 and Chen2024 as an upstream data source. All 12 cases are subsumed within Kock2022's baseline. MyEboga2018 Case 12 (Cameroon 2010, F/32, Bwiti initiation) corresponds to Black (2011) in Chen2024's grey literature table.

### Branch: Chen2024 (dual role)

Chen2024 functions both as a cumulative review (34 sudden deaths) and as the most systematic grey literature mapper in the corpus. Its case tables cross-reference journalistic reports, government risk assessments, and community sources. The lower count (34 vs 38) reflects narrower "sudden death" inclusion criteria, not missing data — Chen excluded non-sudden deaths (e.g. haemorrhagic pancreatitis) that Kock included.

### Branch: Esperanca2026 (non-independent)

Esperanca2026 reports 19 deaths but did not enumerate cases independently. The paper's Key Findings section explicitly references "19 fatalities in Alper 2012 forensic review." This is Alper2012's number, not an independent count. It must not be added to any total.

## Baseline Discrete Case Reports

The cumulative reviews above tally deaths across the literature, but the hub's purpose is tracing each death to its original source. The following 6 case reports each document a unique ibogaine-associated fatality within the Kock2022 baseline period (pre–7 December 2020). These deaths are counted within the baseline 38 — this section makes the primary evidence accessible.

| Paper | Year | Demographics | Mechanism / Cause | Key Risk Factors | Subsumed By |
|-------|------|-------------|-------------------|------------------|-------------|
| Marker2002 | 2002 | M, 36, NYC | Ibogaine intoxication; blood 9225 ng/mL (5–9× therapeutic) | Polydrug (morphine, cocaine metabolite, alcohol at scene); unsupervised; unknown dose | Alper2012 (co-author Stajić is co-author on both — same NYC OCME forensic toxicologist) |
| Kontrimaviciute2006 | 2006 | M, France | Ibogaine/noribogaine poisoning; lung 50.1/55.9 µg/g, liver 40.5/50.5 µg/g, blood 5–20× therapeutic | Root bark (~18 spoonfuls over ~10h); unsupervised; concomitant drug abuse history | Mosca2023, Esperanca2026 |
| Jalal2013 / Warrick2012 | 2013 (2012) | M, 25, USA (Detroit) | Cardiac arrest (Vtach/Vfib per AICD); QTc 521 ms, QRS 208 ms, EF 10%; multi-organ failure; brain death ~Day 2 | Pre-existing cardiac dysrhythmias with AICD (described as SVT in Jalal); 2–2.5g internet-sourced ibogaine; heroin user; unsupervised home setting | Corkery2018 (via Jalal2013 + Bronstein2012), Mosca2023 |
| Mazoyer2013 | 2013 | M, 27, France | Death ~12h post-ingestion; femoral blood ibogaine 1.27 µg/mL | Root bark; co-ingestion methadone + diazepam (triple QT-prolongation risk); 15-year polysubstance history; unsupervised | Mosca2023, Esperanca2026 |
| Papadodima2013 | 2013 | M, 52, Greece | Cardiac death; blood ibogaine 2 mg/L | Liver cirrhosis (>90% fatty infiltration); 40–45% coronary occlusion; chronic alcoholism; internet-sourced product | Mosca2023, Esperanca2026 |
| Meisner2016 | 2016 | M, 40, Boston | Asystole ~8h post-ingestion; brain death from cardiac arrest | 4g ibogaine + 2g uncharacterised "booster"; heroin detox; unsupervised; unregulated internet source | Ona2021, Mosca2023 |

**Note on Jalal2013 / Warrick2012:** These are the same fatality reported through two channels. Warrick & Baltarowich (Children's Hospital of Michigan Poison Center, Detroit) presented the case at NACCT 2012 (Abstract #184); Jalal, Daher & Hilu (St. John Hospital and Medical Center, Detroit) published the full case report in 2013. Confirmed identical by matching postmortem ibogaine concentrations across all four specimens (heart blood 2.2 µg/mL, iliac blood 1.8 µg/mL, vitreous 0.98 µg/mL, liver 4.2 µg/g). The conference abstract contains richer clinical data (AICD interrogation, QTc/QRS, EF, lab trajectories, postmortem levels) than the one-page journal publication. Both vault entries are retained for their complementary clinical value.

**Pattern:** All 6 cases share unsupervised or unregulated settings, and 5 of 6 involved active substance use or polysubstance co-exposure. Five had identifiable pre-existing risk factors (cardiac disease, liver cirrhosis, chronic substance abuse). These cases — spanning 2002 to 2016 across the USA, France, and Greece — illustrate the risk profile that drove development of comprehensive screening protocols (see [GREEN_Clinical_Protocols_Hub](GREEN_Clinical_Protocols_Hub.md)).

## Post-Baseline Additions

Deaths verified as occurring after Kock2022's 7 December 2020 literature cut-off, or demonstrably absent from its review.

| Paper | Deaths | Date(s) | Rationale | Status |
|-------|--------|---------|-----------|--------|
| Evans2026 | 5 | 2024–2026, multiple clinics | All post-baseline. Five discrete fatalities across regulated and unregulated settings | **INCLUDED** |
| Acimovic2021 | 1 | Pre-2021, Serbia | Published 12 Jan 2021, after Kock's search cut-off. Death occurred pre-cut-off but no alternative reporting pathway identified (see note below) | **INCLUDED (flagged)** |
| Busby2024 | 1 | Spring 2022, Cancún | Post-baseline. Discrete case in an unregulated Mexican setting | **INCLUDED** |
| Terasaki2026 | 1 | ~2025, "Mr S" | Patient died of fentanyl overdose during buprenorphine taper. Previously used ibogaine but was not on ibogaine at time of death. Not ibogaine-associated per pharmacovigilance standards | **EXCLUDED** |

**Note on Acimovic2021:** This is a transparent edge case. The death occurred before Kock2022's cut-off date, but the publication appeared after it — meaning Kock's literature search could not have captured it. The Serbian case report has no obvious alternative pathway into the English-language systematic review literature. We include it in the post-baseline count but flag it explicitly: researchers conducting their own mortality analyses may apply their own assessment of whether this death should be classified as baseline or post-baseline.

## Grey Literature Sources

The following fatalities are documented only in journalistic reports, government databases, or community compilations — not in peer-reviewed case reports. Chen2024 is the authoritative academic source for these mappings.

| Source | Citation | Case | Demographics | Context | Citing Reviews |
|--------|----------|------|-------------|---------|----------------|
| Black (2011) | *Irish Independent* | Cameroon 2010 Bwiti initiation | F, 32 | Spiritual ceremony; cardiac arrest; no prior drug history. Previous mild iboga reaction in Wales | Chen2024; = MyEboga2018 Case 12 |
| Stewart (2015) | Press report | Unknown location | F, 45 | Addiction treatment; sudden death ~32h; morphine user since teenager | Chen2024 |
| Amundsen (2015) | Norwegian Medicines Agency, *Verdens Gang* Oslo | Norway | F, 42 | Addiction treatment; four doses day 1 + dose day 2; found dead day 3 | Chen2024 |
| Cheer (2015) | *Daily Mail Australia* | Unknown location | M, 33 | Two-day treatment; dead 20 min after valium on day 2; polysubstance/heroin | Chen2024 |
| Gummin (2017) | AAPCC NPDS 34th Annual Report Case 288 | USA | M, 26 | Day 14; meth addiction; undiagnosed heart problem; MI | Chen2024 |
| Carr (2017) | *Luton Today* | Luton, UK | M, 36 | Heroin addict. Providers criminally prosecuted | Chen2024 |

Chen2024 also references 3 cases cited only as "Corkery (2018)" from unpublished UK coroner records (M/36 opioid dependent; M/50s alcoholic/heroin/diazepam; M/53 heroin). All three fall within the Kock2022 baseline count.

## Risk Factor Patterns

### Demographic Profile

The most detailed demographic data comes from Corkery2018 (N=33): 25 male, 8 female, mean age 39.5 years (range 24–60). The overwhelming majority (26/33, 78%) were undergoing opioid detoxification. Across the broader case report literature (Chen2024, N=58), the pattern holds: 42 male, 16 female, aged 22–63, with 49 of 58 being substance users seeking addiction treatment.

### Geographic Distribution

| Country | Deaths (Corkery2018, N=33) |
|---------|---------------------------|
| Mexico | 8 |
| USA | 7 |
| UK | 5 |
| France | 4 |
| Other (Netherlands, Norway, Canada, Cameroon, Serbia, Costa Rica, Greece) | 9+ |

The concentration in Mexico and the USA reflects the geography of unregulated ibogaine treatment during the 1990s–2010s, not differential pharmacological risk. Mexico's prominence is particularly notable — 3 of 3 pulmonary thromboembolism deaths occurred there (Alper2012), and the country remains a major destination for ibogaine treatment. Post-baseline deaths (Evans2026, Busby2024) continue to cluster in unregulated settings in Mexico and Costa Rica.

### Risk Factors

Across the three most detailed fatality analyses (Corkery2018 N=33, Alper2012 N=19, Chen2024 N=58 case reports including 34 sudden deaths), a consistent picture emerges. Pre-existing cardiac disease was present in at least 6 of 33 deaths as a proximate cause or contributing factor. Polysubstance co-exposure was documented in at least 12 of 33 deaths (Corkery2018) and 8 of 11 tested cases (Alper2012), with cocaine, opiates, methadone, and benzodiazepines the most common co-intoxicants. Broader medical comorbidities — liver disease, obesity, hypertensive cardiovascular disease — were present in at least 18 of 33 cases.

Three deaths involved pulmonary thromboembolism rather than cardiac arrhythmia, all in Mexico, with autopsies inadequate to determine proximate cause (Alper2012). This non-cardiac mechanism is easily overlooked in safety discussions focused on QTc prolongation.

CYP2D6 poor metaboliser status represents an under-recognised pharmacogenomic risk factor. Approximately 5–10% of Caucasians lack functional CYP2D6, resulting in approximately threefold higher ibogaine exposure (AUC 11,471 vs 3,936 ng·hr/mL in poor vs extensive metabolisers, Chen2024). Among fatalities where ethnicity was known, 10 of 11 were White/Caucasian (Alper2012), a population with higher CYP2D6 PM prevalence.

Deaths occurred between 1.5 and 76 hours post-ingestion (Alper2012). Fatalities at 24–76 hours implicate noribogaine (elimination half-life 28–49 hours) rather than ibogaine itself (half-life 4–7 hours), supporting clinical protocols requiring at least 72 hours of monitoring (Chen2024).

Every fatality with documented pre-treatment data had at least one identifiable, screenable risk factor. This is the central finding of Alper2012 (12 of 14 adequate autopsies showed cardiovascular disease plus polysubstance exposure explaining or contributing to death) and is corroborated across all subsequent reviews. It does not mean ibogaine is safe — it means the deaths were, in principle, preventable through adequate screening and monitoring.

The widely cited 1:427 death-to-treatment ratio (Alper et al. 2008, via Corkery2018) is now considered historical — the denominator is untraceable as treatment has moved into unregulated settings worldwide. For the epistemic arc of how this ratio was formulated, formalised, and ultimately abandoned, see [RED_Cardiac_Safety_Hub](RED_Cardiac_Safety_Hub.md#act-3-epidemiology-20122018).

## See Also

- [RED_Cardiac_Safety_Hub](RED_Cardiac_Safety_Hub.md) — Comprehensive cardiac safety narrative: mechanisms, screening, monitoring, protocol evolution
- [GREEN_Clinical_Protocols_Hub](GREEN_Clinical_Protocols_Hub.md) — Clinical screening and monitoring protocols that operationalise the safety evidence
- [ORANGE_Mechanisms_Hub](ORANGE_Mechanisms_Hub.md) — Pharmacological mechanisms of ibogaine and noribogaine including CYP2D6 metabolism
- [BLUE_Outcomes_Hub](BLUE_Outcomes_Hub.md) — Treatment outcome evidence across addiction, depression, and other indications
- [ORANGE_PK-PD_Hub](ORANGE_PK-PD_Hub.md) — Pharmacokinetic and pharmacodynamic synthesis including noribogaine's extended half-life
- [Kenneth_Alper_MOC](../MOCs/Kenneth_Alper_MOC.md) — Researcher map centred on the foundational contributor to ibogaine fatality research
