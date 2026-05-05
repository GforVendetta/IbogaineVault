---

title: "🔴 Fatalities Hub" category: RED tags:

- meta/moc
- meta/hub
- topic/cardiac
- topic/toxicity
- topic/adverse-event aliases: \["Fatalities Hub", "Mortality Count", "Death Count"\] contraindications: \[\] qtc_data: false electrolyte_data: false herg_data: false

---

## Purpose

This hub is a **quantitative mortality counting instrument** within the IbogaineVault. It tracks every known ibogaine-associated death, maps the citation chains between cumulative reviews, and makes the deduplication methodology transparent and auditable.

It does not narrate cardiac mechanisms, discuss pharmacological pathways, or recommend clinical protocols. If you need the story of cardiac safety, see [RED_Cardiac_Safety_Hub](RED_Cardiac_Safety_Hub.md). If you need to validate a mortality count, you're in the right place.

The deduplicated count below synthesises 33 papers reporting mortality data (13 cumulative reviews, 12 discrete case reports, 8 incidental mentions) into a single auditable figure. Every inclusion, exclusion, and edge case is flagged with rationale.

## Methodology

The IbogaineVault tags every paper that reports deaths with a `mortality_scope` enum: **cumulative-review** (papers that tally deaths across the literature), **discrete-cases** (papers reporting unique incidents), and **incidental** (papers that mention deaths counted elsewhere). This enum prevents the single most dangerous analytical error in ibogaine mortality research: naively summing overlapping counts.

The deduplication algorithm proceeds in four steps:

1. **Group by scope.** 13 cumulative reviews, 12 discrete-case papers, 8 incidental papers.
2. **Establish baseline.** Identify the most comprehensive cumulative review as the anchor count. Kock2022 is the baseline: 38 ibogaine-associated deaths through 7 December 2020, derived via PRISMA-compliant search (PubMed + EMBASE), cross-referenced against Alper2012, Corkery2018, Koenig2015, and Litjens2016. The vault adds two further pre-2020 fatalities outside Köck's PRISMA catchment. The first is the cardiac-arrhythmia death within Noller, Frampton & Yazar-Klosinski's New Zealand 12-month observational cohort (Noller2017); Köck's literature search did not capture this paper despite its 2017 online publication, and Chen2024 subsequently captured the case in Annex III, providing the academic attestation. The second is the November 2017 death of Milos Martinovic at the Minds Alive Wellness Centre in Durban, South Africa, judicially established as culpable homicide in *S v Jeewa* (KZN High Court, Durban; Vahed J., 22 August 2024); the death falls within Köck's PRISMA catchment window but was not captured because no academic publication had documented it at the time of Köck's literature search (pre-conviction coverage was confined to South African press reports), and the conviction itself post-dates both Köck2022 and Chen2024 (see [2017_Minds_Alive_Martinovic_Death_Durban](../Primary_Sources/2017_Minds_Alive_Martinovic_Death_Durban.md)). These two additions bring the baseline-period total to 40.
3. **Add post-baseline discrete cases only.** For each discrete-case paper, verify the death occurred after Kock's cut-off date or was demonstrably absent from the review.
4. **Exclude incidental papers.** These mention deaths already counted in cumulative reviews.

**Why not Chen2024 as baseline?** Despite later publication (2024 vs 2022), Chen2024 counts fewer deaths (34 vs 38) — but this is a definitional divergence, not a coverage difference. Chen's "sudden death" framing categorically excludes three classes of fatality that Köck includes: deaths from haemorrhagic pancreatitis, deaths from mesenteric thrombosis, and deaths from duodenal ulcer complications. These are not edge cases or ambiguous attributions — they are deliberate, principled exclusions encoded in Chen's case-definition criteria. A later publication date does not guarantee a more comprehensive count, and a smaller count does not imply a less rigorous review; both papers are correct under their own definitions. The Hub adopts Köck's definition for the baseline because it is the more inclusive of the two and corresponds to the conventional pharmacovigilance question "how many deaths have been temporally associated with ibogaine ingestion?" rather than the narrower "how many sudden deaths have been temporally associated with ibogaine ingestion?"

**Why not Esperanca2026?** Esperanca2026 reports 19 deaths but did not conduct its own case enumeration — it cites Alper2012's figure directly. It is **non-independent** and cannot serve as a baseline or additive source.

## Deduplicated Mortality Count

> \[!summary\] **\~46 ibogaine-associated deaths**
>
> **Baseline:** 40 deaths (Köck 38 + Noller2017 +1 + [Martinovic2017](../Primary_Sources/2017_Minds_Alive_Martinovic_Death_Durban.md) +1, see Methodology §2; literature through 7 Dec 2020)
>
> **Post-baseline additions:** +6 deaths (2021–2026)
>
> **Excluded:** 1 death (Terasaki2026 — fentanyl OD, not ibogaine-associated)

**Breakdown of post-baseline additions:**

- Evans2026: 4 deaths across multiple clinics (2024–2026)
- Acimovic2021: 1 death, Serbia (flagged — see §6)
- Busby2024: 1 death, Cancún, spring 2022

**Confidence:** Moderate-to-high on the baseline (Kock2022 cross-referenced four prior systematic reviews). High on each post-baseline addition (individually verified against baseline coverage).

**Coverage gap:** This count almost certainly undercounts total ibogaine-associated deaths. Unreported fatalities in unregulated settings — particularly pre-2020 Africa, Central America, and underground treatment networks — represent a known gap. Community sources (MyEboga2018) note that reporting became unreliable from approximately 2006 as providers multiplied and treatment moved underground.

## Cumulative Reviews Timeline

All 13 papers with `mortality_scope: cumulative-review`, ordered chronologically. These counts **overlap** — they must not be summed.

PaperYearCountCoverage EndIndependence AssessmentMaas200620068\~2005Independent — earliest cumulative countAlper2008200811\~2006Independent — source of the 1:427 death-to-treatment ratioDonnelly201120119\~2010Independent — lower count reflects narrower scopeAlper2012201219\~2008Independent — foundational IRB-approved forensic case seriesKoenig2015201522\~2014Independent — extends prior literatureLitjens2016201627\~2015Independent — extends prior literatureSchep2016201619\~2015Independent — toxicological focusCorkery2018201833\~2017Independent — extends Alper2012 by +14 from coroners' records + literatureMyEboga2018201812\~2010Upstream community source (Lee Albert, [MyEboga.com](http://MyEboga.com)); all 12 subsumed in Kock2022Ona202120211—Single-case within update window — Meisner 2016 (already enumerated in Corkery2018); non-additiveKock2022**2022387 Dec 2020BASELINE — PRISMA-compliant, cross-refs 4 prior reviews, most comprehensive**Chen2024202434\~2021Independent enumeration but narrower "sudden death" criteria — undercountsEsperanca2026202619Refs Alper2012**NON-INDEPENDENT** — explicitly cites Alper2012's 19-death figure

## Citation Chain Map

Understanding which reviews subsume which earlier reports is essential for avoiding double-counting. The ibogaine mortality literature has a single dominant chain and several branches.

### Main chain

> Kock2022 (38) ← Corkery2018 (33) ← Alper2012 (19) ← Alper2008 (11) ← Maas2006 (8)

Each link represents explicit subsumption: Kock2022 deduplicated against Corkery2018 and three other reviews. Corkery2018 extended Alper2012 by adding 14 deaths from UK coroners' records and subsequent literature. Alper2012 built on the earlier Alper2008 consecutive case series. Alper2008 extended the Maas2006 count. Every death in a downstream review is already captured in Kock2022's 38.

### Branch: Alper1999 (case series with one fatality, non-additive)

Alper1999 reports a case series of 33 opioid-dependent patients treated with ibogaine in the Netherlands and USA between 1962 and 1993, including one fatality (24F, Netherlands 1993, 29 mg/kg, respiratory arrest at \~19 hours, charred tin foil among personal effects). This fatality is **identical** to Alper2012 Case #2 — same patient, same demographics, same dose, same mechanism. The 1999 paper served as the early documentation; the 2012 forensic case series captured this case (along with 18 others) within its systematic review. The case is counted exactly once via Alper2012 and is included in Kock2022's baseline of 38. Alper1999 must not be treated as an additive source.

This subsumption was confirmed by direct PDF arbitration of both papers (Gemini 3.1 Pro, 2026-04-25-c).

### Branch: MyEboga2018 (community source)

MyEboga2018 compiled 12 cases from community reporting (Lee Albert, [MyEboga.com](http://MyEboga.com)). This non-academic source fed into both Corkery2018 and Chen2024 as an upstream data source. All 12 cases are subsumed within Kock2022's baseline. MyEboga2018 Case 12 (Cameroon 2010, F/32, Bwiti initiation) corresponds to Black (2011) in Chen2024's grey literature table.

### Branch: Chen2024 (dual role)

Chen2024 functions both as a cumulative review (34 sudden deaths) and as the most systematic grey literature mapper in the corpus. Its case tables cross-reference journalistic reports, government risk assessments, and community sources. The lower count (34 vs 38) reflects narrower "sudden death" inclusion criteria, not missing data — Chen excluded non-sudden deaths (e.g. haemorrhagic pancreatitis) that Kock included.

### Branch: Esperanca2026 (non-independent)

Esperanca2026 reports 19 deaths but did not enumerate cases independently. The paper's Key Findings section explicitly references "19 fatalities in Alper 2012 forensic review." This is Alper2012's number, not an independent count. It must not be added to any total.

## Baseline Discrete Case Reports

The cumulative reviews above tally deaths across the literature, but the hub's purpose is tracing each death to its original source. The following 9 case reports each document a unique ibogaine-associated fatality within or contiguous to the Kock2022 baseline period (pre–7 December 2020). Seven of these deaths are counted within Köck's baseline 38; the remaining two (Noller2017 and [Martinovic2017](../Primary_Sources/2017_Minds_Alive_Martinovic_Death_Durban.md)) were outside Köck's PRISMA catchment and are added at vault level (Köck 38 + Noller +1 + Martinovic +1 = vault baseline 40, see Methodology §2). This section makes the primary evidence accessible.

PaperYearDemographicsMechanism / CauseKey Risk FactorsSubsumed ByMarker20022002M, 36, NYCIbogaine intoxication; blood 9225 ng/mL (5–9× therapeutic)Polydrug (morphine, cocaine metabolite, alcohol at scene); unsupervised; unknown doseAlper2012 (co-author Stajić is co-author on both — same NYC OCME forensic toxicologist)Kontrimaviciute20062006M, FranceIbogaine/noribogaine poisoning; lung 50.1/55.9 µg/g, liver 40.5/50.5 µg/g, blood 5–20× therapeuticRoot bark (\~18 spoonfuls over \~10h); unsupervised; concomitant drug abuse historyMosca2023, Esperanca2026Cheze20082008M, 37, Paris-based (died Gabon)Drowning; myocardial bridging at autopsy; femoral blood ibogaine 3.3 µg/mL, noribogaine 4.6 µg/mL (\~3.6× reference 4h concentration)Unsupervised Bwiti ceremony (Gabon); congenital myocardial bridging; physical exertion post-ingestion (swimming); unknown root bark dose; **iboga was sole xenobiotic — negative tox screen (blood and urine) for other licit/illicit drugs and alcohol**Esperanca2026Jalal2013 / Warrick20122013 (2012)M, 25, USA (Detroit)Cardiac arrest (Vtach/Vfib per AICD); QTc 521 ms, QRS 208 ms, EF 10%; multi-organ failure; brain death \~Day 2Pre-existing cardiac dysrhythmias with AICD (described as SVT in Jalal); 2–2.5g internet-sourced ibogaine; heroin user; unsupervised home settingCorkery2018 (via Jalal2013 + Bronstein2012), Mosca2023Mazoyer20132013M, 27, FranceDeath \~12h post-ingestion; femoral blood ibogaine 1.27 µg/mLRoot bark; co-ingestion methadone + diazepam (triple QT-prolongation risk); 15-year polysubstance history; unsupervisedMosca2023, Esperanca2026Papadodima20132013M, 52, GreeceCardiac death; blood ibogaine 2 mg/LLiver cirrhosis (&gt;90% fatty infiltration); 40–45% coronary occlusion; chronic alcoholism; internet-sourced productMosca2023, Esperanca2026Meisner20162016M, 40, BostonAsystole \~8h post-ingestion; brain death from cardiac arrest4g ibogaine + 2g uncharacterised "booster"; heroin detox; unsupervised; unregulated internet sourceCorkery2018, Ona2021, Mosca2023Noller20172017F, 45, NZ (Provider 1 clinic; observational cohort context)Cardiac arrhythmia (probable, per post-mortem); 2200 mg ibogaine HCl over \~24h, exceeding clinic protocol of 1600 mg/4hLong-term IV opioid use; abrupt venlafaxine cessation pre-treatment; pre-treatment Sevredol (morphine); prolonged fasting (post-mortem acetone 60 mg/L); de-facto unsupervised — treating physician left clinic for overseas travel mid-treatment, \~15h unmonitored before death**Köck-missed** (pre-2020 outside PRISMA catchment); attested in Chen2024 Annex III; primary clinical detail from HDC2016 Case 13HDC00966 (NZ Health and Disability Commissioner)[Martinovic2017](../Primary_Sources/2017_Minds_Alive_Martinovic_Death_Durban.md)2017M, 26, Canadian/French citizen (died Durban, South Africa)Drug-associated death consistent with alprazolam overdose (post-mortem); ibogaine in blood. Cardiac arrest at unknown interval after last of 3–4 sequential ibogaine doses on Day 1Active polysubstance use at admission (alprazolam 16 boxes + OxyContin); permitted by provider to keep and self-administer benzodiazepines and opioids throughout admission; no pre-treatment toxicology screening; multiple sequential ibogaine doses; unregistered facility operated by a dentist (not a medical practitioner); no continuous cardiac monitoring at time of arrest; no medical practitioner on site; CPR delayed ~7 min; no IV line; no antidotes; crash cart on different floor**Köck-missed** (within PRISMA catchment but no academic publication pre-conviction; *S v Jeewa* conviction August 2024 post-dates both Kock2022 and Chen2024); judicially-established protocol-failure stack documented in court record

**Note on Jalal2013 / Warrick2012:** These are the same fatality reported through two channels. Warrick & Baltarowich (Children's Hospital of Michigan Poison Center, Detroit) presented the case at NACCT 2012 (Abstract #184); Jalal, Daher & Hilu (St. John Hospital and Medical Center, Detroit) published the full case report in 2013. Confirmed identical by matching postmortem ibogaine concentrations across all four specimens (heart blood 2.2 µg/mL, iliac blood 1.8 µg/mL, vitreous 0.98 µg/mL, liver 4.2 µg/g). The conference abstract contains richer clinical data (AICD interrogation, QTc/QRS, EF, lab trajectories, postmortem levels) than the one-page journal publication. Both vault entries are retained for their complementary clinical value.

**Pattern:** All 9 cases involved unsupervised or de-facto unsupervised settings — including Noller2017 (where treatment occurred under a legal NZ regulatory framework but was functionally unsupervised at the time of death — treating physician had left the clinic for overseas travel; vital signs unrecorded for \~15 hours) and [Martinovic2017](../Primary_Sources/2017_Minds_Alive_Martinovic_Death_Durban.md) (provider was a dentist, not a medical practitioner; only one enrolled nurse on duty at the moment of cardiac arrest; no medical practitioner on site or on call). 7 of 9 involved active substance use or polysubstance co-exposure (Marker2002, Jalal2013, Mazoyer2013, Papadodima2013, Meisner2016, Noller2017, Martinovic2017). 8 of 9 had identifiable pre-existing risk factors (cardiac disease, liver cirrhosis, chronic substance abuse, congenital cardiac anomaly, long-term IV opioid use, or active uncontrolled benzodiazepine/opioid co-administration). These cases — spanning 2002 to 2017 across the USA, France, Greece, Gabon, New Zealand, and South Africa — illustrate the risk profile that drove development of comprehensive screening protocols (see [GREEN_Clinical_Protocols_Hub](GREEN_Clinical_Protocols_Hub.md)).

**Analytical note on Cheze2008 — the isolated-ibogaine case.** Most baseline discrete cases are polysubstance-confounded, which complicates causal attribution to ibogaine alone. Cheze2008 is an exception: a negative blood-and-urine toxicology screen leaves **iboga as the sole xenobiotic**, and the authors propose two ibogaine-specific mechanisms for the drowning — (a) ibogaine cardiotoxicity interacting with congenital myocardial bridging, and (b) amphetamine-like stimulation producing over-exertion while swimming. This case strengthens the evidence base that ibogaine can contribute to fatal outcomes through cardiac and exertional pathways in the **absence of polysubstance confound**, not only as an additive risk factor in multi-drug exposures.

**Analytical note on Noller2017 — the regulatory-framework-without-protocol-adherence case.** Mrs A (45F, NZ) died during ibogaine treatment within a legal regulatory framework (NZ Medsafe non-approved-medicine schedule; medically qualified physician at Provider 1's clinic) — but the HDC investigation (Case 13HDC00966) documented severe protocol-adherence and monitoring deficiencies at the moment of risk. The treating physician left the clinic for overseas travel at midday on Day 4, transferring sole monitoring responsibility to an assistant with no formal medical training. Vital signs were not recorded after 9:00 AM Day 4. Mrs A was found dead at 6:00 AM Day 5, lying in the same position observed at 3:00 PM the previous afternoon — approximately 15 hours unmonitored. Her total ibogaine HCl dose (2200 mg over \~24 hours) exceeded the clinic's own documented protocol limit (1600 mg over 4 hours). She had abruptly ceased venlafaxine before arrival, had received Sevredol (morphine) in the two days before treatment, and had post-mortem blood acetone of 60 mg/L consistent with prolonged fasting. Post-mortem assessment concluded death was strongly likely related to ibogaine ingestion, most probably a cardiac arrhythmia. This case is the inverse pole of the Dutch NVIC cohort data discussed below: regulation alone is necessary but not sufficient. The variable that discriminates safety outcomes is regulation conjoined with protocol adherence and continuous monitoring — and this conjunction is what the [GREEN_Clinical_Protocols_Hub](GREEN_Clinical_Protocols_Hub.md) operationalises.

**Analytical note on Martinovic2017 — the judicially-established protocol-failure case.** Milos Martinovic (26M, Canadian/French) died on 8 November 2017 at the Minds Alive Wellness Centre in Durban, South Africa — an unregistered private facility operated by Anwar Mohamed Jeewa, a registered dentist (not a medical practitioner) who had advertised himself online as an ibogaine specialist. The death occurred under conditions that combine, in a single case, every protocol-failure axis the corpus has documented separately elsewhere: benzodiazepine and opioid co-administration permitted throughout admission (16 boxes of Xanax + OxyContin, allowed and instructed); no pre-treatment toxicology screening of residual benzodiazepine concentrations; three to four sequential ibogaine doses on Day 1; no continuous cardiac monitoring at the moment of arrest (Jeewa later claimed Martinovic asked for the ECG leads to be removed — a claim Vahed J. rejected on grounds that Martinovic was already in an altered state from administered ibogaine and not capable of informed consent); no medical practitioner on site; only one enrolled nurse on duty; CPR initiated approximately seven minutes after cardiac arrest; no IV line; no antidotes; crash cart on a different floor and not retrieved during the emergency. Post-mortem cause of death was *"drug-associated death consistent with alprazolam overdose"* with ibogaine detected in the blood. The case is the **first judicially-established ibogaine-clinic negligence conviction** in the IbogaineVault corpus: in *S v Jeewa* (KZN High Court, Durban; Vahed J., 22 August 2024), Jeewa was convicted of culpable homicide alongside five statutory counts under the Medicines and Related Substances Act 101 of 1965 and one count of operating an unregistered treatment centre. Sentencing on 12 September 2024 imposed three years' correctional supervision, a R50,000 fine, and an order to provide 25 hours per month of dental services to inmates at Westville Prison. The case combines features individually present elsewhere in the corpus but rarely together: a fully documented protocol-failure stack and a definitive judicial finding of negligence as causally responsible for the death. Methodologically, this places Martinovic at the most evidentially complete pole of the post-Köck corpus — the standard of evidence is qualitatively different from the *"reportedly"* and *"allegedly"* registers that characterise grey-literature fatality entries. Full court record at [2017_Minds_Alive_Martinovic_Death_Durban](../Primary_Sources/2017_Minds_Alive_Martinovic_Death_Durban.md).

## Post-Baseline Additions

Deaths verified as occurring after Kock2022's 7 December 2020 literature cut-off, or demonstrably absent from its review.

PaperDeathsDate(s)RationaleStatusEvans202642024–2026, multiple clinicsAll post-baseline. Four discrete fatalities across regulated and unregulated settings**INCLUDED**Acimovic20211Pre-2021, SerbiaPublished 12 Jan 2021, after Kock's search cut-off. Death occurred pre-cut-off; later attested in Chen2024 Annex II but missed by Köck's 7 Dec 2020 search window (see note below)**INCLUDED (flagged)**Busby20241Spring 2022, CancúnPost-baseline. Discrete case in an unregulated Mexican setting**INCLUDED**Terasaki20261\~2025, "Mr S"Patient died of fentanyl overdose during buprenorphine taper. Previously used ibogaine but was not on ibogaine at time of death. Not ibogaine-associated per pharmacovigilance standards**EXCLUDED**

**Note on Acimovic2021:** This is a transparent edge case. The death occurred before Kock2022's cut-off date, but the publication appeared after it — meaning Kock's literature search could not have captured it. Chen2024 subsequently captured this case in Annex II, confirming its existence in the academic record but also confirming that Köck genuinely missed it (Köck's 7 December 2020 search cutoff predated Chen's coverage window). We include it in the post-baseline count but flag it explicitly: researchers conducting their own mortality analyses may apply their own assessment of whether this death should be classified as baseline or post-baseline.

## Grey Literature Sources

The following fatalities are documented only in journalistic reports, government databases, or community compilations — not in peer-reviewed case reports. Chen2024 is the authoritative academic source for these mappings.

SourceCitationCaseDemographicsContextCiting ReviewsBlack (2011)*Irish Independent*Cameroon 2010 Bwiti initiationF, 32Spiritual ceremony; cardiac arrest; no prior drug history. Previous mild iboga reaction in WalesChen2024; = MyEboga2018 Case 12Stewart (2015)Press reportUnknown locationF, 45Addiction treatment; sudden death \~32h; morphine user since teenagerChen2024; subsumed in Corkery2018 (within Kock2022's 38)Amundsen (2015)Norwegian Medicines Agency, *Verdens Gang* OsloNorwayF, 42Addiction treatment; four doses day 1 + dose day 2; found dead day 3Chen2024; subsumed in Corkery2018 (within Kock2022's 38)Cheer (2015)*Daily Mail Australia*Unknown locationM, 33Two-day treatment; dead 20 min after valium on day 2; polysubstance/heroinChen2024; subsumed in Corkery2018 (within Kock2022's 38)Gummin (2017)AAPCC NPDS 34th Annual Report Case 288USAM, 26Day 14; oxycodone detox; polysubstance abuse history; cardiac arrest with anoxic brain damage; QTc 536 msChen2024; subsumed in Corkery2018 §3.3.6 (within Kock2022's 38)Carr (2017)*Luton Today*Luton, UKM, 36Heroin addict. Providers criminally prosecutedChen2024; subsumed in Corkery2018 (within Kock2022's 38)

Chen2024 also references 3 cases cited only as "Corkery (2018)" from unpublished UK coroner records (M/36 opioid dependent; M/50s alcoholic/heroin/diazepam; M/53 heroin). All three fall within the Kock2022 baseline count.

## Risk Factor Patterns

### Demographic Profile

The most detailed demographic data comes from Corkery2018 (N=33): 25 male, 8 female, mean age 39.5 years (range 24–60). The overwhelming majority (26/33, 78%) were undergoing opioid detoxification. Across the broader case report literature (Chen2024, N=58), the pattern holds: 42 male, 16 female, aged 22–63, with 49 of 58 being substance users seeking addiction treatment.

### Geographic Distribution

CountryDeaths (Corkery2018, N=33)Mexico8USA7UK5France4Other (Netherlands, Norway, Canada, Cameroon, Serbia, Costa Rica, Greece)9+

The concentration in Mexico and the USA reflects the geography of unregulated ibogaine treatment during the 1990s–2010s, not differential pharmacological risk. Mexico's prominence is particularly notable — 3 of 3 pulmonary thromboembolism deaths occurred there (Alper2012), and the country remains a major destination for ibogaine treatment. Post-baseline deaths (Evans2026, Busby2024) continue to cluster in unregulated settings in Mexico and Costa Rica.

### Risk Factors

Across the three most detailed fatality analyses (Corkery2018 N=33, Alper2012 N=19, Chen2024 N=58 case reports including 34 sudden deaths), a consistent picture emerges. Pre-existing cardiac disease was present in at least 6 of 33 deaths as a proximate cause or contributing factor. Polysubstance co-exposure was documented in at least 12 of 33 deaths (Corkery2018) and 8 of 11 tested cases (Alper2012), with cocaine, opiates, methadone, and benzodiazepines the most common co-intoxicants. Broader medical comorbidities — liver disease, obesity, hypertensive cardiovascular disease — were present in at least 18 of 33 cases.

Three deaths involved pulmonary thromboembolism rather than cardiac arrhythmia, all in Mexico, with autopsies inadequate to determine proximate cause (Alper2012). This non-cardiac mechanism is easily overlooked in safety discussions focused on QTc prolongation.

CYP2D6 poor metaboliser status represents an under-recognised pharmacogenomic risk factor. Approximately 5–10% of Caucasians lack functional CYP2D6, resulting in approximately threefold higher ibogaine exposure (AUC 11,471 vs 3,936 ng·hr/mL in poor vs extensive metabolisers, Chen2024). Among fatalities where ethnicity was known, 10 of 11 were White/Caucasian (Alper2012), a population with higher CYP2D6 PM prevalence.

Deaths occurred between 1.5 and 76 hours post-ingestion (Alper2012). Fatalities at 24–76 hours implicate noribogaine (elimination half-life 28–49 hours) rather than ibogaine itself (half-life 4–7 hours), supporting clinical protocols requiring at least 72 hours of monitoring (Chen2024).

Every fatality with documented pre-treatment data had at least one identifiable, screenable risk factor. This is the central finding of Alper2012 (12 of 14 adequate autopsies showed cardiovascular disease plus polysubstance exposure explaining or contributing to death) and is corroborated across all subsequent reviews. It does not mean ibogaine is safe — it means the deaths were, in principle, preventable through adequate screening and monitoring.

The widely cited 1:427 death-to-treatment ratio (Alper et al. 2008, via Corkery2018) is now considered historical — the denominator is untraceable as treatment has moved into unregulated settings worldwide. For the epistemic arc of how this ratio was formulated, formalised, and ultimately abandoned, see [RED_Cardiac_Safety_Hub](RED_Cardiac_Safety_Hub.md#act-3-epidemiology-20122018).

### Regulated-Setting Cohort Data

Chen2024 Annex II reports a Dutch National Poisons Information Centre (NVIC) cohort of 14 ibogaine cases between 2010 and 2022 with **zero fatalities**. This is the only documented regulated-setting denominator in the corpus, and the cases are mutually exclusive with the 58 literature fatalities Chen catalogued elsewhere in the same report.

The methodological weight of this finding is asymmetric to its sample size. The ibogaine fatality literature catalogues deaths but rarely captures non-fatal exposures or treatments-without-incident, which means the headline mortality counts have no honest denominator. The Dutch cohort is small (N=14), but it is the only data point in the entire mortality corpus where both the numerator (0 deaths) and the denominator (14 exposures) are simultaneously known and the setting is medically supervised. Every case in the Köck2022 baseline of 38 occurred in unregulated, unsupervised, or community/Bwiti settings — and the Dutch cohort directly tests the counterfactual that the Hub's central pattern claim (deaths involve identifiable, screenable risk factors) implies: in a setting with adequate screening and monitoring, the death rate is zero in 14 exposures.

This evidence is consistent with, not equivalent to, a safety claim. Fourteen cases is too few to establish a confidence interval narrow enough to discriminate between "ibogaine is safe in regulated settings" and "ibogaine retains a low but non-zero baseline mortality rate even with screening." But it is the strongest evidence in the corpus that the deaths in the unregulated literature are not simply pharmacological inevitabilities — they are the predictable consequence of screening failures, which is the policy-relevant finding for clinical protocol development (see [GREEN_Clinical_Protocols_Hub](GREEN_Clinical_Protocols_Hub.md)).

## See Also

- [RED_Cardiac_Safety_Hub](RED_Cardiac_Safety_Hub.md) — Comprehensive cardiac safety narrative: mechanisms, screening, monitoring, protocol evolution
- [GREEN_Clinical_Protocols_Hub](GREEN_Clinical_Protocols_Hub.md) — Clinical screening and monitoring protocols that operationalise the safety evidence
- [ORANGE_Mechanisms_Hub](ORANGE_Mechanisms_Hub.md) — Pharmacological mechanisms of ibogaine and noribogaine including CYP2D6 metabolism
- [BLUE_Outcomes_Hub](BLUE_Outcomes_Hub.md) — Treatment outcome evidence across addiction, depression, and other indications
- [ORANGE_PK-PD_Hub](ORANGE_PK-PD_Hub.md) — Pharmacokinetic and pharmacodynamic synthesis including noribogaine's extended half-life
- [Kenneth_Alper_MOC](../MOCs/Kenneth_Alper_MOC.md) — Researcher map centred on the foundational contributor to ibogaine fatality research