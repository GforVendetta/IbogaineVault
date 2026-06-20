# Fidelity Status — read this before citing or relying on the vault

**Status as of 2026-06-01: NOT citation-ready. A fidelity audit is in progress.**

This page exists because accuracy here is not a formality. The vault's own stated standard is that *miscategorised cardiac-safety evidence can affect patient safety* — and the people who use this resource are often making real decisions about a drug with real cardiac risk. So when the audit found fabricated data, the right thing to do was to say so directly, in the open, rather than correct it quietly and hope no one had already relied on it.

## What happened

The vault converts research PDFs into structured markdown. For most of its history that pipeline was reliable. But an AI-assisted conversion step used on some **recently added clinical-trial entries** produced text that *read* like faithful summary while containing **fabricated data** — values, demographics, and safety claims with no basis in the source paper. These are not typos or misclassifications; they are invented facts presented with the same confidence as real ones.

The audit caught them. That is the system working as intended — but it also means we cannot yet vouch for the vault as a whole.

## What this means for you

- **Do not cite the vault or any entry** until this notice is lifted.
- **Verify every figure against the primary source** before relying on it — especially cardiac (QTc, ECG), dosing, electrolyte, and adverse-event data.
- If you have already cited or used an entry, **re-check it against the original** and [open an issue](https://github.com/GforVendetta/IbogaineVault/issues) — we will help you confirm what is and isn't sound.

## An important caveat about "passing" entries

The automated audit primarily compares each entry's **abstract** against the source. Most post-2010 entries pass that check. But the fabrications found so far were in the **body** — the tables, demographics, and safety sections that abstract-matching does not see. Body-level verification is **ongoing and incomplete**. Until it finishes, an entry passing the automated check is **not** a guarantee of citation-grade accuracy. That is why this notice applies to the whole vault, not only to the entries listed below.

## Confirmed fabrications and their current status

| Entry | Issue | Status |
|---|---|---|
| **Rocha2025** (Ibogaine for AUD, PhD thesis) | **Re-verified & corrected 2026-06-20** (13 corrections + 1 unverified ReBEC reg; full list on the card + ledger). Among the genuine errors: invented demographics ("all male, 29–58" vs source 3F/6M, ages 25–61); wrong efficacy instrument ("TLFB" — absent across 117 pp); inverted electrolyte summary ("no derangements" vs documented mild hyperkalemia). The earlier "14+ fabrications" was an over-count: the per-patient QTc table (Tabela 6), COVID-19 §3.1 protocol section, HRS instrument, 8/9 cocaine-comorbidity, AE percentages, and the cardiac AE narrative are **real and source-grounded** — the text-only audit over-flagged figure-grounded tables and untranslated Portuguese prose, while the text-only conversion fabricated identifiers, instruments, criteria, and one dose attribution (Vol 3 hypertensive crisis = 320 mg, not 240 mg). Both directions corrected. | **Corrected 2026-06-20** — re-verified directly against the primary source and restored for use, with a correction notice + verification ledger on the card. |
| **Carlucci2025** (Microdosing, bipolar II) | 5 fabrications, including invented demographics (reported as 45 F; source is 34 M), a fabricated "no adverse events" claim (source reports nausea + mild insomnia), invented concurrent medications, a fabricated mechanism passage, and an omitted systematic-review methodology. | **Corrected** (2026-06-01) directly against the source. |
| **Mash2000** (earlier entry) | The original case that revealed this failure mode: confabulated author names, a fabricated abstract, and an incorrect sample size. | **Corrected** (2026-03-17). |

## A known pattern, and what we're doing about it

The two clinical-trial fabrications found in this audit share a profile: recently added, non-English-origin (Brazilian/Portuguese) clinical-trial papers run through the AI-assisted conversion step. We are treating this as a **systemic conversion failure mode**, not three isolated mistakes. The current work:

1. ✅ Rocha2025 corrected & re-verified directly from source (2026-06-20) — 13 corrections applied; card restored with a verification ledger.
2. A body-level re-audit of the recently added (2024–2025) clinical-trial entries — beyond abstract matching.
3. Re-checking entries that previously cleared on abstract-only matching.

## When this notice will lift

This notice will be removed only when the body-level audit of the affected cohort is complete and any further fabrications are corrected or withdrawn.

**Target date:** approximately **August 2026**. Progress is tracked in commit history and [Issues](https://github.com/GforVendetta/IbogaineVault/issues).

_Last updated: 2026-06-01._
