# Handoff Prompt — Ch12 Conversion

## Task

Convert Chapter 12 of De Rienzo & Beal's *The Ibogaine Story* (1997) to IbogaineVault markdown. This is part of a batch conversion of the book; Chapters 14–17 are already complete and can serve as exemplars.

## Source

**File:** `/Users/aretesofia/Library/Mobile Documents/com~apple~CloudDocs/IbogaineVault_PDFs/Other/The Ibogaine Story Report On The Staten Island Project by Dana Beal and Paul De Rienzo.txt`
**Ch12 lines:** 1601–1869 (approximately — the chapter begins "One day in late July 1990" and ends just before "CHAPTER 13: Bwiti" at the line beginning "The little guys in the secret early grey robes")

**Note:** The chapter boundary is fuzzy. Ch12 flows into Ch13 without a clean break. The Ch12 content proper ends around the Mark Lamontia treatment and follow-up section. The extended Bwiti cosmogony, VALIS holographic/Fibonacci material, and "Ibogaine Challenge" material from approximately line 1830 onward is Chapter 13 territory. Use your judgement — the conversion should capture everything thematically belonging to Ch12 and stop cleanly.

## Output

`/Users/aretesofia/IbogaineVault/Other/DeRienzo1995_Ibogaine_Story_Ch12.md`

## Workflow

1. Read the conversion manifest: `/Users/aretesofia/IbogaineVault/_meta/conversion_manifest.md`
2. Read the source text (lines 1601–1869)
3. Read one exemplar for format reference: `/Users/aretesofia/IbogaineVault/Other/DeRienzo1995_Ibogaine_Story_Ch17.md`
4. Write YAML frontmatter first (mode: rewrite)
5. Append body sections in chunks of ~20–25 lines each (mode: append)

## Category Assignment

**Primary: PURPLE** (phenomenology — the chapter's backbone is Philip K. Dick's VALIS theology as framework for understanding ibogaine's experiential dimension: Salvator Salvandas, hologramatic universe, Black Iron Prison, two-world superimposition)

**Secondary: WHITE, ORANGE**
- WHITE: Historical narrative (1990–1993 project timeline, Omnichem supply, DPF politics, INQUIRER breakthrough, Dhoruba on Donohue, Queens court proceedings, Clinton/Hillary meeting via Mash)
- ORANGE: Cerebellar mechanism (Heath brain pacemaker, Harlow monkey experiments, William Mason movable surrogates, cerebellum as addiction substrate — "addiction involves the same circuits as learning to walk")

## Key Content to Capture

### VALIS/Gnostic Framework (PURPLE)
- Philip K. Dick's VALIS as "roadmap to understanding gnostic substances, Ibogaine and Bwiti"
- Salvator Salvandas — the "saved savior" concept
- Black Iron Prison as supra-temporal constant
- Two-world superimposition parallel to ibogaine's phenomenology
- Entry 48 on anamnesis ("salvation through gnosis — more properly anamnesis, the loss of amnesia")
- Hologramatic memory coils / DNA carriers
- "Disinhibiting instructions" — core content intrinsic, not external (Plato: learning as remembering)
- Fibonacci's constant / Parmenides' perfect rectangle as chaos signature
- Grail/Blood/Burning Bush convergence in Bwiti

### Mark Lamontia Treatment (Clinically significant)
- January 1993, Rotterdam/Leiden international treatment seminar
- Came off 35mg methadone daily in 3 days
- First rigorous follow-up: weekly urines, complete physical by Dr Clark at 45 days
- Treatment team: Rommell Washington, Dr Clark (Harlem Hospital), Hans-Georg Behr, Boaz, Sergio Ramirez, Deborah Mash
- Jan Bastiaans supervising ("Only 10 treatments. But you're missing the important thing. It works.")
- Remote video tracking, dry-ice samples to University of Miami
- Another subject came off 125mg methadone
- "Informational shock wave sweeping through Harlem"

### Carol Baker Treatment
- First HIV-positive person treated with ibogaine
- Dual addiction: 80mg methadone (day) + $250 heroin (night)
- Uneventful 22-hour treatment
- "Her armor had been stripped away"
- "I kicked methadone once before and it was five months of Hell. This time I woke up, I hadn't had a fix in 24 hours, and I wasn't dopesick."
- Post-treatment evaluation at University of Miami with Mash/Ramirez
- Presented at ACT UP floor

### Cerebellar Mechanism (ORANGE)
- Molliver's cerebellum finding: toxicity at 100mg/kg i.p. in rats → possible ibogaine receptor site
- Cerebellum governs input from muscles, joints, tendons; regulates balance, spatial location, body position
- "True addiction involves the same kind of deep conditioning of the cerebellum as learning to walk"
- "No magic bullet for addiction without going into the cerebellum"
- No cerebellar action without tremor or visualisations (acetylcholine pathway requirement)

### REM/Dreaming Mechanism (ORANGE)
- Deportere paper: ibogaine tremor/behavioural immobility = stimulation of acetylcholine pathways (active during sleep/REM)
- EEG signature of true REM absent → Dana modified characterisation to "REM-like"
- Goutarel monograph passages: serotonin/catecholamine interplay, MAO inhibition, PGO waves
- Jouvet letter (Nov 7, 1990): hallucinations ≠ dreams, but reorganised wakefulness stages
- NDE as survival reflex: "stereoscopic" serotonergic + cholinergic entity scanning ancestral memory

### Political/Historical Thread (WHITE)
- July 1990: Dana re-reads VALIS, recognises ibogaine parallel
- Omnichem deal: Howard corners world supply of 99.7% pure ibogaine (vincristine by-product)
- "Hank the Skank" prank → Philadelphia Inquirer story (July 4, 1992 — "Declaration of Independence for Addicts")
- Deborah Mash / Hillary Clinton meeting (Dade County Democratic Committee connection)
- Herb Kleber blocking: torpedoed ACT UP/CASA meeting, activated cronies in NIDA peer review
- 1992 cocaine efficacy evidence: Dzoljic (90% reduction in self-administration), Sershen, Broderick
- Dhoruba on Phil Donohue via Flo Kennedy connection (post-LA riots)
- Queens court proceedings: Clayton motion, 60-day plea, medical marijuana defence

### Ibogaine Chemistry Notes
- Ibogaine = left half of vinblastine (dimeric ibogaine, Madagascar periwinkle) — KS drug
- Common component of vincristine — another KS drug
- Far less toxic than either
- Contoreggi submitted protocol to study as anti-viral; writing another for KS
- Rats pre-treated with ibogaine recovered from electro-shock twice as fast

## Clinical Fields

```yaml
evidence_level: qualitative
mortality_count: 0
qtc_data: false
electrolyte_data: false
herg_data: false
dosing_range: "35mg methadone detox (Lamontia); 125mg methadone detox (unnamed); 80mg methadone + heroin (Baker)"
route: oral
sample_size: ~10 (Bastiaans series referenced)
```

Note: dosing_range here refers to the addiction burden being treated, not ibogaine dose (which is not specified in the chapter). Frame accordingly in YAML.

## Wikilinks to Include

These should appear inline in body text and/or in a Cross-References section:

- [[Lotsof1985_Patent_Opioid]] / [[Lotsof1992_Patent_Polydrug]]
- [[Mash1998_Ibogaine_Human_Pharmacokinetics]] (Mash's later published work from this era)
- [[Molliver1994_Cerebellar_Toxicity]] or similar (Molliver finding referenced)
- [[Goutarel1993_Pharmacodynamics_Iboga]] (Goutarel monograph quoted extensively)
- [[Dzoljic1988_Ibogaine_Morphine]] / cocaine self-administration papers
- [[Broderick1992_Cocaine_Ibogaine_Interactions]]
- [[Sershen1992_Ibogaine_Dopamine]]
- [[DeRienzo1995_Ibogaine_Story_Ch14]] through [[DeRienzo1995_Ibogaine_Story_Ch17]] (sibling chapters)
- [[DeRienzo1995_Ibogaine_Story_Ch16]] (Gnostic sacrament lineage — direct thematic link)
- [[DeRienzo1995_Ibogaine_Story_Ch18]] (if exists — Nico interview referenced)
- [[Clinical_Outcomes_Hub]] / [[Phenomenology_Hub]] / [[Cerebellar_Mechanism_Hub]] (or whatever hub names exist)

**Check which of these actually exist in the vault before wikilinking.** Use Desktop Commander to search `/Users/aretesofia/IbogaineVault/` for filenames. Only wikilink to files that exist.

## Style Notes

- UK English throughout
- The source text is dense, discursive, and mixes political narrative with pharmacology with Gnostic theology. The conversion should impose clear thematic structure while preserving the chapter's intellectual range.
- The VALIS/Gnostic material is not clinical evidence but is essential to understanding the phenomenological framework the project operated within. Treat it with the same intellectual seriousness as mechanism sections — this is PURPLE category content, not decoration.
- Mark Lamontia's treatment is the most clinically significant content: first rigorous follow-up with weekly urines. Foreground this.
- The Goutarel quotes on serotonin/catecholamine/acetylcholine interplay and PGO waves are substantive pharmacology despite appearing in a chapter framed by VALIS. Extract and present clearly.

## Chunked-Append Strategy

Suggested section breakdown (adjust based on flow):

1. **YAML frontmatter** (rewrite)
2. **Overview** (~10 lines)
3. **VALIS Framework** (~20 lines — Dick's theology, Salvator Salvandas, Black Iron Prison, Entry 48 anamnesis)
4. **Political Context 1990–1992** (~20 lines — Omnichem, DPF, Inquirer, Kleber, Mash/Clinton)
5. **Carol Baker Treatment** (~12 lines)
6. **Mark Lamontia Treatment** (~15 lines — Rotterdam January 1993, first rigorous follow-up)
7. **Cerebellar Mechanism** (~15 lines — Molliver finding, addiction-as-walking, acetylcholine pathways)
8. **REM and the Near-Death Experience** (~15 lines — Deportere, Goutarel, Jouvet, NDE reflex)
9. **Gnostic Synthesis** (~12 lines — Grail/Blood/Burning Bush, Fibonacci doorway, hologramatic ancestors)
10. **Cross-References** (~15 lines)
