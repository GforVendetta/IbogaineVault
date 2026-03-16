---
title: "Pre-Release Audit — Session 2 Continuation: Boolean Sweep Analysis"
created: 2026-03-14
type: session-prompt
phase: "pre-release"
model: "Claude Opus 4.6"
---

## Context — Read This First

You are continuing a Session 2 audit of the **IbogaineVault**, a structured
evidence map for ibogaine research about to go public as a citable academic
resource for Dr Martijn Arns (BrainClinics Foundation / Stanford).

### What happened in Session 2 (previous conversation)

**Decision: PASS** — 15-paper stratified sample, 0 SERIOUS, 1 MODERATE, 3 MINOR.

**5 fixes were applied:**
1. Schenberg2014 — `electrolyte_data: true` → `false` (screened but didn't report)
2. Brown2018 — added `dosing_range` and `route: oral` (were null)
3. Thurner2014 — added `secondary_categories: [ORANGE]` (consistency with Koenig2012)
4. Evans2026 — `clinical_significance: high` → `moderate` (journalism, not primary evidence)
5. Chen2024 — `key_findings` reworded to clarify deaths (not QTc) from 4.5 mg/kg

**1 fix was attempted then reverted:**
- Chen2024 tags `topic/drug-interaction` and `topic/neurotoxicity` — NOT in the 62-tag
  canonical taxonomy (`_meta/schema_registry.yml`). Reverted. Existing tags
  (`topic/toxicity`, `topic/pharmacokinetics`, `topic/cyp2d6`) cover the content.
  Adding new canonical tags is a governance decision for post-release.

### What this session does

The Schenberg2014 fix raised a question: is the "screened but didn't report"
confusion isolated, or systemic? Rather than manually sampling more papers,
a boolean sweep script was written to check programmatically.

The script (`_meta/tools/boolean_sweep.py`) scans `papers.json` for:
- All papers with `electrolyte_data: true` — any reviews/preclinical among them?
- All papers with `qtc_data: true` — sanity check
- All papers with `herg_data: true` — sanity check
- Both `herg_data` AND `qtc_data` true — should be rare (bench + clinical in one paper)
- RED papers with ALL three booleans false — are they missing data or legitimately empty?
- Non-RED papers with `mortality_count > 0` — should all have RED as secondary

**The user has run the script and pasted the output below.**

### Your task

1. **Interpret the sweep output.** Flag any papers that look suspicious.
2. **For each suspicious paper**, state the file path, the field, what's wrong,
   and the fix. Use severity ratings: CRITICAL / HIGH / MEDIUM / LOW / NOTE.
3. **Update the Session 2 verdict** if needed (it was PASS — does the sweep
   change that?).
4. **Produce a fix script** if there are fixes to make — a bash one-liner or
   Python script the user can run locally, so we don't waste context on
   round-trip file edits.
5. After fixes, ask: "Shall I update the worklog?"

### Key distinctions to remember

- `electrolyte_data: true` = paper **reports** electrolyte values or analysis.
  NOT merely screening electrolytes for eligibility.
- `qtc_data: true` = paper reports **clinical QTc interval measurements** from ECGs.
  NOT citing someone else's QTc data. NOT hERG channel IC₅₀ values.
- `herg_data: true` = paper reports **original hERG channel electrophysiology data**.
  NOT citing hERG studies. NOT clinical QTc.
- Reviews that **tabulate** others' data in a structured way (e.g., Chen2024's
  QTc table) can legitimately carry the boolean — they're presenting the data
  in usable form, not merely mentioning it.
- RED papers with all booleans false are legitimate if they're fatality case
  reports, adverse event narratives, or toxicity papers that don't include
  cardiac electrophysiology or electrolyte data.

### Reference paths

- Working vault: `/Users/aretesofia/IbogaineVault/`
- Tier 1: `/Users/aretesofia/IbogaineVault-Tier1/`
- Schema: `/Users/aretesofia/IbogaineVault/_meta/schema_registry.yml`
- papers.json: `/Users/aretesofia/IbogaineVault-Tier1/papers.json`

### Tools

Desktop Commander for file ops. Always absolute paths.
Use the `worklog-manager` skill for logging.

---

## Boolean Sweep Output

Paste the terminal output from `python3 /Users/aretesofia/IbogaineVault/_meta/tools/boolean_sweep.py` below this line:

