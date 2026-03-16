# Transcript Manifest
# Compact reference for converting call recordings, interviews, and talks into vault markdown.
# Same philosophy as conversion_manifest.md — read this + the recording/transcript. That's it.

---

## Purpose

Transcripts are operationally distinct from research papers. Papers report findings; transcripts capture decisions, reasoning, and institutional knowledge as they happen. Different provenance, different metadata needs, different query patterns.

The `scope` field (introduced here) is the first YAML property that distinguishes operational content from published research — enabling Copilot and NLQ queries like "what has Pangea discussed internally about dosing?" vs "what does the literature say about dosing?"

---

## YAML Schema — Meeting Transcripts

```yaml
---
title: "Descriptive Title of Meeting/Call"
document_type: meeting-transcript        # See valid types below
date: "YYYY-MM-DD"                       # When the call happened
participants:                            # All attendees, surname first
  - "Surname, Given Name"
duration: "~XX minutes"                  # Approximate call length
year: YYYY                               # Integer, for vault consistency
category: GREEN                          # Same 6-colour system as papers
scope: pangea                            # See scope values below
tags:                                    # From canonical 62-tag taxonomy
  - topic/protocol
  - method/qualitative                   # Always include for transcripts
key_findings: "≤250 chars"              # Key outcomes/decisions summary
clinical_significance: moderate          # high | moderate | low | landmark
aliases:                                 # For Obsidian search
  - "Short Reference Name"
contraindications: []                    # Usually [] for transcripts
key_decisions:                           # Strategic/operational decisions made
  - "Decision with enough context to be useful standalone"
action_items:                            # Follow-up tasks with assignees
  - "Person: specific action to take"
wikilinks:                               # Explicit cross-references
  - "[[path/to/Related_Document]]"
---
```

### Schema Notes
- `participants` (not `authors`) — transcripts have speakers, not academic authors
- `date` (not `publication_date`) — transcripts record when the conversation happened
- `key_decisions` and `action_items` — operational fields that don't apply to research papers
- `wikilinks` in YAML — transcripts reference vault content explicitly; papers use `## See Also` in the body
- `method/qualitative` — always include; transcripts are by definition qualitative primary sources
- `contraindications` — typically `[]` for transcripts, but populate if a call explicitly identifies new contraindications

---

## YAML Schema — Published Interviews & Conference Talks

Published content (podcasts, conference presentations, video interviews) uses a hybrid schema — research paper structure with transcript-specific additions where useful:

```yaml
---
title: "Talk/Interview Title"
authors:                                 # Use `authors` for published content
  - "Surname, Given Name"
year: YYYY
category: WHITE                          # Or appropriate category
scope: published                         # See scope values below
tags:
  - topic/relevant-topic
  - method/qualitative
document_type: interview-transcript      # Or conference-talk
key_findings: "≤250 chars"
clinical_significance: moderate
aliases:
  - "Short Reference"
contraindications: []
evidence_level: qualitative              # Or observational if data cited
---
```

Published content follows the research paper schema from `conversion_manifest.md` with the addition of `scope`. No `key_decisions`, `action_items`, or `wikilinks` in YAML — these are research artefacts, not operational documents.

---

## Scope Values

> Canonical source for all enums: `_meta/schema_registry.yml` | Verified: 2026-02-23

| Value | Meaning | Typical Location |
|-------|---------|-----------------|
| `pangea` | Internal/operational — Pangea team discussions, planning calls, strategy meetings. Includes external collaborators when meeting is Pangea-initiated. | `Pangea_Ops/Pangea_Internal_Calls/` |
| `published` | Publicly available — conference talks, podcast interviews, published video interviews. Content exists independently of the vault. | `Primary_Sources/` |

### When to use which
- **Pangea team call with Geoff Noller discussing clinic setup** → `scope: pangea` (operational, even though Geoff is external)
- **Clare Wilkins presenting at Horizons conference** → `scope: published` (public research dissemination)
- **Sam Oliver interviewing Clare for a documentary** → `scope: published` (published interview)

### Why not on research papers?
Research papers don't need `scope` — they're all inherently published research. The field exists specifically to distinguish the non-paper content that the vault increasingly contains. Adding `scope: research` to 189 papers would be noise with zero signal.

---

## Document Type Extensions

The following transcript-specific types are added to the canonical `document_type` enum (see `conversion_manifest.md` for the full list):

| Type | Use For |
|------|---------|
| `meeting-transcript` | Internal calls, planning meetings, strategy sessions |
| `interview-transcript` | Published interviews, podcast appearances (already in enum) |
| `conference-talk` | Conference presentations, panel discussions (already in enum) |
| `educational` | Lectures, online courses, webinars — pedagogical intent, not conference venue |

`meeting-transcript` is **new** — added to the conversion manifest enum alongside the existing types.

---

## File Placement

| Content Type | Location |
|-------------|----------|
| Pangea internal calls | `/Users/aretesofia/IbogaineVault/Pangea_Ops/Pangea_Internal_Calls/` |
| Published interviews | `/Users/aretesofia/IbogaineVault/Primary_Sources/` |
| Conference talks | `/Users/aretesofia/IbogaineVault/Primary_Sources/` |

### Filename Conventions

**Internal calls:** `YYYY-MM-DD_INITIALS_Topic.md`
- `2026-02-19_GN_PK_Vault_Demo_NZ_Regulatory_Fatalities.md`
- `2026-01-11_CW_SJW_PK_GN_ALH_DM_NZ_Clinic_Meeting.md`

**Published content:** `YYYY_Source_Speaker_Topic.md`
- `2018_Oliver_Wilkins_Pangea_Protocol.md`
- `2010_Horizons_Clare_Wilkins_400_Sessions.md`

---

## Body Template — Meeting Transcripts

```markdown
# Meeting Transcript: DD Month YYYY

**Platform:** Zoom / In-person / Phone
**Participants:** Name (Location), Name (Location)
**Context:** Brief situational context, links to prior meetings if relevant.

---

## Key Topics Discussed

[Optional summary sections before full transcript, especially for long calls]

---

## Full Transcript

**HH:MM:SS Speaker Name**
Dialogue text.

**HH:MM:SS Speaker Name**
Dialogue text.
```

### Body Notes
- Timestamps in `HH:MM:SS` format (from transcription tool)
- Speaker names in bold with timestamp
- Context block after the YAML header provides situational framing
- Key Topics section is optional but recommended for calls >30 minutes

---

## Retrofit Guide — Existing Transcripts

All transcripts have been retrofitted to this schema as of 2026-02-20.

### Retrofit Summary (Complete)

| File | What Was Done |
|------|--------------|
| `2026-01-07_CW_SJW_PK_Call.md` | `authors` → `participants`, `interview-transcript` → `meeting-transcript`, added `scope: pangea`, `date`, `key_decisions`, `action_items`, `method/qualitative` |
| `2026-01-09_CW_SJW_PK_Call.md` | Full YAML added from scratch |
| `2026-01-10_CW_SJW_PK_Call.md` | Full YAML added from scratch |
| `2026-01-11_CW_SJW_PK_GN_ALH_DM_NZ_Clinic_Meeting.md` | `authors` → `participants`, `primary-source` → `meeting-transcript`, added `scope: pangea`, `date`, `key_decisions`, `action_items`, `method/qualitative` |
| `2026-01-30_CW_SJW_PK_Call.md` | Full YAML added from scratch |

### Published Interview Retrofits (Complete)

All 12 files in `Primary_Sources/` received `scope: published`. Three also had `method/qualitative` added to tags.

---

## Pre-Completion Check

- [ ] YAML parses (no blank line after opening `---`)
- [ ] `document_type` is `meeting-transcript`, `interview-transcript`, or `conference-talk`
- [ ] `participants` (not `authors`) for meeting transcripts
- [ ] `scope` is `pangea` or `published`
- [ ] `date` field present (YYYY-MM-DD)
- [ ] `method/qualitative` in tags
- [ ] `key_decisions` populated (meeting transcripts)
- [ ] `action_items` populated with assignees (meeting transcripts)
- [ ] File in correct directory
