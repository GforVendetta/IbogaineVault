# IbogaineVault-Tier1 Remediation Prompts

**Date:** 16 March 2026  
**Purpose:** Six prompts to paste sequentially into separate Claude Opus 4.6 + ET conversations within this project. Each prompt is self-contained with full context. Run them in order — later prompts depend on earlier ones having been completed.

**Critical context that applies to all prompts:**
- Working vault: `/Users/aretesofia/IbogaineVault/` (Tier 2, internal clinical instrument)
- Publishable vault: `/Users/aretesofia/IbogaineVault-Tier1/` (Tier 1, public research support tool)
- Tier 1 is populated by running `bash /Users/aretesofia/IbogaineVault/_meta/tools/sync_tier1.sh`
- The sync script rsyncs from working vault → Tier 1, then runs post-sync transforms
- Schema single source of truth: `/Users/aretesofia/IbogaineVault/_meta/schema_registry.yml`
- Index generator: `/Users/aretesofia/IbogaineVault/_meta/tools/generate_index.py`
- Use Desktop Commander MCP for all file operations. Always use absolute paths.

---
## PROMPT 1 — Schema Additions: `open_access`, `publisher`, `body_format`, `issn`

```
TASK: Add four new YAML fields to the IbogaineVault schema and update all downstream tooling.

CONTEXT:
The vault has a recurring copyright risk problem: there is no metadata-level way to determine whether a paper is open access, who published it, or whether its body is in the vault's own analytical format vs retained academic structure. This means copyright audits are manual grep-and-pray exercises that keep finding new problems. We need structured metadata to make copyright assessment queryable and automated.

Current state:
- 297 papers in Tier 1, 300 in working vault
- Zero papers have open_access, publisher, or body_format fields
- issn is already defined in schema_registry.yml but is not populated on any paper
- The schema single source of truth is: /Users/aretesofia/IbogaineVault/_meta/schema_registry.yml
- The index generator that produces papers.json + papers.csv is: /Users/aretesofia/IbogaineVault/_meta/tools/generate_index.py
- The validation script is: /Users/aretesofia/IbogaineVault/_meta/tools/validate_vault.py

WHAT TO DO:

1. READ the schema_registry.yml first. Understand the field definition format.

2. ADD these fields to the `paper` schema in schema_registry.yml, in the `# ── Optional ──` section, grouped together with a comment `# ── Optional — Copyright & format metadata (D17) ──`:

   open_access:    { type: enum, enum_ref: open_access_status, optional: true, omit_if_unavailable: true, note: "OA status — true (confirmed OA/CC licence), false (confirmed paywalled), unknown (not yet assessed)" }
   publisher:      { type: string, optional: true, omit_if_unavailable: true, note: "Publisher name — Elsevier, Wiley, Springer Nature, Frontiers, MDPI, etc." }
   body_format:    { type: enum, enum_ref: body_formats, optional: true, omit_if_unavailable: true, note: "Body structure — vault-analytical (Key Findings/Clinical Implications), academic-retained (Introduction/Methods/Results/Discussion), hybrid (both), or narrative (neither — grey literature, book chapters, primary sources)" }

3. ADD the corresponding enum blocks to the `enums:` section:

   open_access_status:
     - true
     - false
     - unknown

   body_formats:
     - vault-analytical
     - academic-retained
     - hybrid
     - narrative

4. UPDATE generate_index.py:
   - Read generate_index.py — find the INDEX_FIELDS list (around line 170)
   - Add these entries to INDEX_FIELDS (BEFORE the closing bracket, after the pmcid entry):
     ("open_access",          "open_access",          None),
     ("publisher",            "publisher",             None),
     ("body_format",          "body_format",           None),
     ("issn",                 "issn",                  None),

5. CHECK validate_vault.py:
   - Read validate_vault.py and search for where it validates field names or enum values
   - If it has a hardcoded list of valid fields, add the new fields
   - If it has hardcoded enum values for validation, add the new enums
   - The new fields are OPTIONAL so the validator must not fail on papers that lack them

VERIFICATION:
- Run: python3 /Users/aretesofia/IbogaineVault/_meta/tools/validate_vault.py /Users/aretesofia/IbogaineVault/
  It must pass with 0 errors (existing papers won't have the new fields, which is fine since they're optional)
- Run: python3 /Users/aretesofia/IbogaineVault/_meta/tools/generate_index.py --vault /Users/aretesofia/IbogaineVault --output /tmp/test_index/
  Verify the output papers.json includes the new fields (all null for now — that's expected)

DO NOT modify any paper files in this prompt. Schema + tooling only.

After completing, ask: "Shall I update the worklog?"
```

---
## PROMPT 2 — Automated Metadata Population Script

```
TASK: Write and run a Python script that auto-populates open_access, publisher, body_format, and issn across all ~300 papers in the IbogaineVault working vault. Also identify and fill missing DOIs where possible.

CONTEXT:
Prompt 1 has already added the open_access, publisher, body_format, and issn fields to the schema and index generator. No papers currently have these fields populated. This script will populate them using heuristics from existing metadata + body content detection.

Current field population rates (from papers.json):
- doi: 195/297 populated (102 missing — many of these exist but were never entered)
- pmid: 160/297 populated (137 missing)
- pmcid: 51/297 populated (246 missing)
- journal: 243/297 populated (54 missing)
- issn: 0/297 populated

WHAT TO DO:

1. READ the schema_registry.yml to understand field definitions:
   /Users/aretesofia/IbogaineVault/_meta/schema_registry.yml

2. WRITE a Python script at /Users/aretesofia/IbogaineVault/_meta/tools/populate_metadata.py that:

   a) DISCOVERS all paper markdown files (year folders + Clinical_Guidelines/ + Industry_Documents/ + Other/ + Primary_Sources/). Use the same discovery logic as generate_index.py.
   
   b) For EACH paper, reads the existing YAML frontmatter and determines:

      BODY FORMAT DETECTION (from the markdown body, NOT the YAML):
      - If body contains "## Key Findings" OR "## Clinical Implications" AND does NOT contain "## Introduction"/"## Methods"/"## Results"/"## Discussion" → body_format: vault-analytical
      - If body contains "## Introduction"/"## Methods"/"## Results"/"## Discussion" AND does NOT contain "## Key Findings" → body_format: academic-retained
      - If body contains BOTH patterns → body_format: hybrid
      - If body contains NEITHER → body_format: narrative
      
      PUBLISHER DETECTION (from DOI prefix):
      - 10.1016 → Elsevier
      - 10.1002 or 10.1111 → Wiley
      - 10.1007 or 10.1038 → Springer Nature
      - 10.3389 → Frontiers
      - 10.3390 → MDPI
      - 10.1371 → PLoS
      - 10.1080 → Taylor & Francis
      - 10.1177 → SAGE
      - 10.1101 → bioRxiv/Cold Spring Harbor
      - 10.1093 → Oxford University Press
      - 10.1155 → Hindawi/Wiley (OA)
      - 10.2174 → Bentham Science
      - 10.1556 → Akadémiai Kiadó
      - 10.21203 → Research Square (preprint)
      - 10.1186 → BioMed Central/Springer Nature (OA)
      - 10.1124 → ASPET
      - If no DOI, try to infer from journal name (e.g., "Frontiers in Pharmacology" → Frontiers)
      
      OPEN ACCESS DETECTION (multi-signal):
      - pmcid is populated → open_access: true (PMC = freely archived)
      - Publisher is Frontiers, MDPI, PLoS, BioMed Central, Hindawi → open_access: true (OA by definition)
      - journal contains "bioRxiv" or "preprint" or "Research Square" → open_access: true
      - journal contains "PhD Thesis" or "Thesis" → open_access: true
      - document_type is "journalism" or "primary-source" → open_access: true
      - Publisher is Elsevier, Wiley, Springer Nature (non-BMC), Taylor & Francis, SAGE, Bentham, Akadémiai Kiadó, Oxford UP → open_access: false (default paywalled; PMCID would override to true)
      - Cannot determine → open_access: unknown
      
      ISSN LOOKUP: Do NOT attempt network lookups. Leave issn unpopulated for now — it will be filled in Prompt 3 via API.

   c) WRITES the new fields into each paper's YAML frontmatter. Insert them AFTER the existing pmcid/issn block (or after pmid if pmcid is absent), grouped together:
      ```
      open_access: true
      publisher: "Frontiers"
      body_format: vault-analytical
      ```
      If a field value is "unknown" or cannot be determined, still write it (open_access: unknown). If publisher cannot be determined, omit the field entirely.

   d) DOES NOT modify any content outside the YAML frontmatter (between the --- delimiters). The body text must remain completely untouched.

   e) Has a --dry-run flag that prints what it would do without modifying files.

   f) Has a --report flag that outputs a CSV summary: filepath, open_access, publisher, body_format, line_count, doi, pmcid

3. RUN the script with --dry-run first and review the output.

4. RUN the script with --report to generate a CSV at /Users/aretesofia/IbogaineVault/_meta/tools/metadata_report.csv

5. REVIEW the report — look for:
   - Any paper marked open_access: false AND body_format: academic-retained AND line_count > 200 → these are the COPYRIGHT RISK papers
   - Any paper where publisher couldn't be determined despite having a DOI
   - Any paper marked body_format: narrative that you'd expect to have structure

6. RUN the script for real (without --dry-run) on the WORKING VAULT only.

7. VERIFY by running the validator:
   python3 /Users/aretesofia/IbogaineVault/_meta/tools/validate_vault.py /Users/aretesofia/IbogaineVault/
   Must pass with 0 errors.

IMPORTANT CONSTRAINTS:
- This script runs against the WORKING VAULT (/Users/aretesofia/IbogaineVault/), NOT Tier 1
- The script must preserve ALL existing YAML fields exactly as they are — only ADD new fields
- The script must handle edge cases: papers without DOI, papers without journal, papers in non-year folders (Clinical_Guidelines/, Industry_Documents/, Other/, Primary_Sources/)
- The SAFEST approach is: read the file, find the closing --- of frontmatter, insert the new fields just before it, write the file back. Do NOT parse and re-serialise the entire YAML.

After completing, output the copyright risk list (open_access: false/unknown AND body_format: academic-retained AND line_count > 200) and ask: "Shall I update the worklog?"
```

---
## PROMPT 3 — Missing Academic Identifier Lookup (DOI, PMID, PMCID, ISSN)

```
TASK: Write and run a script that looks up missing DOIs, PMIDs, PMCIDs, and ISSNs for IbogaineVault papers using the CrossRef and PubMed APIs, then populates them in the YAML frontmatter.

CONTEXT:
The vault has significant gaps in academic identifiers:
- 102 papers missing DOI (many of these DOIs exist — they were just never entered during conversion)
- 137 papers missing PMID
- 246 papers missing PMCID
- 0 papers have ISSN populated (field exists in schema but never filled)

APIs to use:
- CrossRef: https://api.crossref.org/works?query.title=TITLE&query.author=AUTHOR&rows=3
  Returns DOI, ISSN, publisher. Rate limit: be polite, add mailto param.
- PubMed ESearch: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=TITLE+AUTHOR&retmode=json
  Returns PMID.
- NCBI ID Converter: https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=DOI&format=json
  Converts DOI → PMID + PMCID (if available).
- CrossRef also returns ISSN in the response — capture it.

WHAT TO DO:

1. READ the current papers.json to get the list of papers and their existing identifiers:
   /Users/aretesofia/IbogaineVault/papers.json (regenerate if needed)

2. WRITE a Python script at /Users/aretesofia/IbogaineVault/_meta/tools/lookup_identifiers.py that:

   a) For papers MISSING DOI: query CrossRef by title + first author + year. Accept a match only if:
      - Title similarity > 85% (use difflib.SequenceMatcher)
      - Year matches exactly
      - Log all matches with confidence scores for human review
   
   b) For papers WITH DOI but MISSING PMID/PMCID: query NCBI ID Converter with the DOI.
   
   c) For papers MISSING DOI but WITH PMID: query PubMed efetch to get the DOI from the PubMed record.
   
   d) For ALL papers: if CrossRef returns ISSN and the paper doesn't have one, capture it.
   
   e) For ALL papers: if CrossRef returns publisher and the paper's publisher field is empty, capture it.
   
   f) Outputs a JSON report: /Users/aretesofia/IbogaineVault/_meta/tools/identifier_lookup_report.json
   
   g) Has a --apply flag that writes confirmed matches (confidence > 85%) to the YAML frontmatter.
   
   h) Has a --dry-run flag (default) that only generates the report.
   
   i) Rate limits: 1 request per second to CrossRef, 3 per second to NCBI. Add mailto header to CrossRef (use: mailto=philip@pangeabiomedics.com).

3. RUN with --dry-run first. Review the report.

4. RUN with --apply for high-confidence matches.

5. For low-confidence matches, present a list and ask me to confirm each one.

6. After population, regenerate the index:
   python3 /Users/aretesofia/IbogaineVault/_meta/tools/generate_index.py --vault /Users/aretesofia/IbogaineVault --output /Users/aretesofia/IbogaineVault

7. After applying, any paper that gained a PMCID should have its open_access field updated to true.

8. Report summary: how many DOIs added, PMIDs added, PMCIDs added, ISSNs added, papers still without DOI (list them — these are likely grey literature, theses, book chapters that genuinely lack DOIs).

IMPORTANT CONSTRAINTS:
- Only modify the WORKING VAULT, never Tier 1 directly
- Be conservative: only auto-apply matches with high confidence. False DOIs are worse than missing DOIs.
- Some papers genuinely don't have DOIs: theses, book chapters (DeRienzo1995), journalism (Evans2024, Wittier1998), primary sources. Don't force-match these.
- Respect rate limits. If 400+ API calls needed, it will take 7+ minutes. That's fine.

After completing, ask: "Shall I update the worklog?"
```

---
## PROMPT 4 — Sync Script v2: Override Mechanism + Post-Sync Transforms

```
TASK: Upgrade the sync_tier1.sh script to add a Tier 1 override mechanism and post-sync text transforms that prevent governance file regressions.

CONTEXT — THE ROOT CAUSE:
The sync script at /Users/aretesofia/IbogaineVault/_meta/tools/sync_tier1.sh uses rsync to mirror the working vault into Tier 1. Every governance file gets copied verbatim. This means ANY Tier-1-specific edit gets overwritten on the next sync run.

This has caused the same blockers to reappear across five consecutive audit sessions:
- _meta/README.md references WORKLOG.md, ROADMAP.md, Cowork_Outputs/, copilot/ — none exist in Tier 1
- README.md, CONTRIBUTING.md, CHANGELOG.md claim "~4,400 cross-references" but Tier 1 has ~3,400
- schema_registry.yml contains transcript_meeting block referencing Pangea_Ops/ and "pangea" in scopes
- validate_vault.py has "pangea" in VALID_SCOPES and TODO stubs
- Clare Wilkins MOC has "Internal Documents" section with Pangea Team Call
- Howard Lotsof MOC has "Pangea philosophy"
- Nardou2023 has parenthetical "(an entity associated with Pangea Biomedics)"
- PK-PD Hub has Aotearoa-specific clinical recommendation with imperative language
- GREEN Hub has prominent Pangea attribution framing

THE SOLUTION: _tier1_overrides/ directory + post-sync transforms in the script.

WHAT TO DO:

1. READ the current sync script: /Users/aretesofia/IbogaineVault/_meta/tools/sync_tier1.sh

2. READ the existing Tier 1 override README: /Users/aretesofia/IbogaineVault/_meta/_tier1_overrides/_meta_README.md

3. READ each file that needs transforms to understand the exact content:
   - /Users/aretesofia/IbogaineVault/README.md — find the "4,400+" count
   - /Users/aretesofia/IbogaineVault/CONTRIBUTING.md — find "~4,400 cross-references"
   - /Users/aretesofia/IbogaineVault/CHANGELOG.md — find "~4,400"
   - /Users/aretesofia/IbogaineVault/MOCs/Clare_Wilkins_MOC.md — find "Internal Documents" section
   - /Users/aretesofia/IbogaineVault/MOCs/Howard_Lotsof_MOC.md — find "Pangea philosophy"
   - /Users/aretesofia/IbogaineVault/2023/Nardou2023*.md — find Pangea Biomedics parenthetical
   - /Users/aretesofia/IbogaineVault/Hubs/Hub_PK-PD_Synthesis.md — find Aotearoa recommendation paragraph
   - /Users/aretesofia/IbogaineVault/Hubs/GREEN_Clinical_Protocols_Hub.md — find Pangea attribution

4. MODIFY the sync script:

   a) Add --exclude='_meta/_tier1_overrides/' to the rsync command

   b) After existing Pangea wikilink stripping, add new section "── Post-sync: Tier 1 overrides and transforms ──":
      
      OVERRIDE COPIES:
      - Copy _meta/_tier1_overrides/_meta_README.md → ${DEST}_meta/README.md
      
      SED TRANSFORMS (use sed -i '' on macOS):
      - README.md: replace "4,400+" with "3,400+" on the cross-references line
      - CONTRIBUTING.md: replace "~4,400 cross-references" with "~3,400 cross-references"
      - CHANGELOG.md: replace "~4,400" with "~3,400" in the cross-references row
      
      SCHEMA REGISTRY (${DEST}_meta/schema_registry.yml):
      - Remove entire transcript_meeting schema block
      - Remove "    - pangea     # Internal/operational" from scopes enum
      
      VALIDATE_VAULT.PY:
      - Replace VALID_SCOPES = {"pangea", "published"} with VALID_SCOPES = {"published"}
      - Remove TODO comment lines
      
      MOC TRANSFORMS:
      - Clare_Wilkins_MOC.md: remove "### Internal Documents" header + table header/separator + Pangea Team Call row
      - Howard_Lotsof_MOC.md: replace "ICEERS, GITA, Pangea philosophy" with "ICEERS, GITA"
      
      PAPER TRANSFORMS:
      - Nardou2023*.md: remove "(an entity associated with Pangea Biomedics)"
      
      HUB TRANSFORMS:
      - GREEN_Clinical_Protocols_Hub.md: replace "Clare Wilkins (Pangea Biomedics) developed" with "Clare Wilkins developed"
      - Hub_PK-PD_Synthesis.md: soften or remove Aotearoa clinical recommendation paragraph

   c) Update verification section with explicit checks that all transforms applied

5. TEST: bash /Users/aretesofia/IbogaineVault/_meta/tools/sync_tier1.sh

6. VERIFY all transforms via grep (each must return 0 hits for the removed content)

7. Run Tier 1 validator — must pass with 0 errors.

8. UPDATE CITATION.cff date-released to today's date in the Tier 1 copy.

IMPORTANT: Script must remain IDEMPOTENT. All transforms on DESTINATION only. Preserve existing functionality.

After completing, ask: "Shall I update the worklog?"
```

---
## PROMPT 5 — Copyright Risk Assessment + Reconversion Queue

```
TASK: Using the newly populated metadata (from Prompts 2-3), identify all copyright-risk papers and reconvert those that need it.

CONTEXT:
After Prompts 2 and 3, papers now have open_access, publisher, and body_format fields populated. We can now run the copyright risk query programmatically instead of manually grepping.

Risk criteria:
- HIGH RISK = open_access: false AND body_format: academic-retained AND line_count > 200
- MEDIUM RISK = open_access: unknown AND body_format: academic-retained AND line_count > 200
- REVIEW = open_access: false AND body_format: hybrid AND line_count > 400

Known highest-risk paper from manual audit: Mash2000_Ibogaine_Pharmacokinetics_Safety.md — 776 lines, Annals of NYAS (Wiley), no DOI, full numbered academic sections (1.1, 1.2, etc.). This paper MUST be reconverted regardless of what the automated assessment says.

The vault's copyright defence (in COPYRIGHT.md) claims all non-OA papers are "transformative scholarly works — structured critical analyses written in the vault curator's own voice." Any paper that uses Introduction/Methods/Results/Discussion structure contradicts this claim.

WHAT TO DO:

1. QUERY the working vault to generate the current risk list. You can either:
   - Run the metadata report script from Prompt 2: python3 /Users/aretesofia/IbogaineVault/_meta/tools/populate_metadata.py --report
   - Or query papers.json directly after regenerating the index

2. LIST all papers matching HIGH RISK and MEDIUM RISK. For each, report:
   - filepath, line count, journal, publisher, open_access, body_format, DOI
   - Whether source PDF exists at /Users/aretesofia/IbogaineVault/ + source_pdf path (check with ls)

3. For EACH HIGH RISK paper, RECONVERT to vault analytical format:
   
   THE RECONVERSION PROCESS:
   a) Read the paper ingestor skill: /mnt/skills/user/ibogavault-paper-ingestor/SKILL.md
   b) Read the source PDF if available (check source_pdf field in YAML → look for it at /Users/aretesofia/IbogaineVault/ + that path)
   c) If no source PDF available, work from the existing markdown body — you have the content, you just need to restructure it
   d) Rewrite the body to vault analytical format:

      ## Key Findings
      (Synthesised findings in the vault curator's own analytical voice. NOT paraphrased academic prose. Extract key data points as structured evidence statements. Use wikilinks to cross-reference other vault papers where relevant.)

      ## Clinical Implications
      (What this means for ibogaine treatment — safety signals, protocol considerations, cross-referenced to other vault papers)

      ## Methodology
      (2-4 sentence summary of study design, sample size, methods. NOT a reproduction of the Methods section.)

      ## Data Tables
      (Reconstruct KEY data as vault-created summary tables. Not every table from the paper — only the ones with clinical utility. Tables should be markdown format with a brief analytical caption.)

      ## Cross-References
      (Wikilinks to related vault papers organised by theme — e.g., "Cardiac safety context:", "Related clinical outcomes:", "Pharmacokinetic comparisons:")

   e) The reconverted paper should be SUBSTANTIALLY shorter than the original (target: under 50% of original line count)
   f) Preserve ALL existing YAML frontmatter exactly as-is EXCEPT: update body_format to vault-analytical
   g) The vault's analytical voice is: evidence-focused, clinical-utility-oriented, structured, cross-referencing. It is NOT academic prose reworded.

4. START WITH Mash2000. This is the #1 priority. After reconverting:
   - File should be under 300 lines (was 776)
   - Must NOT contain numbered sections (1.1, 1.2, etc.)
   - Must NOT contain "Introduction", "Methods", "Results", "Discussion" as section headers
   - Must contain "## Key Findings" and "## Clinical Implications"
   - Must preserve all existing wikilinks from the original where they point to valid vault papers
   - YAML unchanged except body_format: vault-analytical added/updated

5. For MEDIUM RISK papers (open_access: unknown): present the list and ask me which to reconvert. Some may turn out to be OA on investigation.

6. For papers where source PDF is NOT available: flag separately. These can still be reconverted by restructuring the existing markdown from academic to vault analytical. The content is there — it just needs a different structure and voice.

7. After all reconversions, verify each one:
   - Passes the validator
   - No new broken wikilinks introduced
   - body_format field updated in YAML
   - Line count reduced substantially

IMPORTANT CONSTRAINTS:
- Reconvert in the WORKING VAULT (/Users/aretesofia/IbogaineVault/), not Tier 1
- Preserve YAML frontmatter exactly — only change body_format field
- The reconverted text must be GENUINELY transformative — not cosmetic reordering of the same academic prose with synonyms swapped. It must read as an independent analytical work.
- Wikilinks should use exact filenames of papers that exist in the vault. Check before linking.
- If a paper has dense data tables worth preserving, the target may be higher than 300 lines — that's fine as long as the analytical voice and structure are genuinely different from the academic original.
- Do NOT strip useful information during reconversion. The goal is to change FORMAT and VOICE, not to lose content. Key data, statistics, findings, and clinical implications must all be preserved — just presented differently.

After completing, list all reconverted papers with before/after line counts and ask: "Shall I update the worklog?"
```

---
## PROMPT 6 — Final Validation, Sync, and Ship Readiness

```
TASK: Run the full sync → validate → verify pipeline and confirm the IbogaineVault-Tier1 is ready for public release.

CONTEXT:
Prompts 1-5 have completed:
- Schema additions (open_access, publisher, body_format, issn fields)
- Automated metadata population across all papers
- Missing identifier lookup (DOI, PMID, PMCID, ISSN via CrossRef + PubMed APIs)
- Sync script v2 with override mechanism + post-sync transforms
- Copyright risk papers identified and reconverted to vault analytical format

This prompt is the final quality gate before flipping the repo to public for the Martijn Arns collaboration.

WHAT TO DO:

1. RUN the sync script:
   bash /Users/aretesofia/IbogaineVault/_meta/tools/sync_tier1.sh
   
   Must complete with "Tier 1 sync PASSED — ready for git commit"

2. VERIFY all previous blockers are resolved (run each grep — every one must return 0 hits):

   BLOCKER 1 — _meta/README.md Tier 2 references:
   grep -c "WORKLOG\|ROADMAP\|conversion_manifest\|transcript_manifest\|NLQ_ARCHITECTURE\|Cowork_Outputs\|_builds\|copilot\|For Claude" /Users/aretesofia/IbogaineVault-Tier1/_meta/README.md

   BLOCKER 2 — Cross-reference count accuracy:
   grep "cross-references" /Users/aretesofia/IbogaineVault-Tier1/README.md
   (must say ~3,400 — verify actual count: grep -roh '\[\[' /Users/aretesofia/IbogaineVault-Tier1/ --include='*.md' | wc -l)

   BLOCKER 3 — schema_registry.yml Pangea/transcript:
   grep -c "pangea\|Pangea\|transcript_meeting" /Users/aretesofia/IbogaineVault-Tier1/_meta/schema_registry.yml

   BLOCKER 4 — validate_vault.py pangea/TODOs:
   grep -c "pangea\|TODO" /Users/aretesofia/IbogaineVault-Tier1/validate_vault.py

   BLOCKER 5 — Clare Wilkins MOC Internal Documents:
   grep -c "Internal Documents\|Pangea Team Call" /Users/aretesofia/IbogaineVault-Tier1/MOCs/Clare_Wilkins_MOC.md

   BLOCKER 6 — Mash2000 reconverted:
   wc -l /Users/aretesofia/IbogaineVault-Tier1/2000/Mash2000_Ibogaine_Pharmacokinetics_Safety.md
   (must be under 350 lines)
   grep -c "^## Introduction\|^## Methods\|^## Results\|^## Discussion\|^## 1\.\|^## 2\." /Users/aretesofia/IbogaineVault-Tier1/2000/Mash2000_Ibogaine_Pharmacokinetics_Safety.md
   (must be 0)

3. RUN the full validator:
   python3 /Users/aretesofia/IbogaineVault-Tier1/validate_vault.py /Users/aretesofia/IbogaineVault-Tier1/
   Must pass with 0 errors.

4. VERIFY papers.json has the new fields:
   python3 -c "
   import json
   d = json.load(open('/Users/aretesofia/IbogaineVault-Tier1/papers.json'))
   p = d['papers'][0]
   print('Fields:', [k for k in p.keys()])
   print('Paper count:', d['paper_count'])
   "
   Must include open_access, publisher, body_format, issn in the field list.

5. VERIFY no remaining unaccepted copyright risk:
   python3 -c "
   import json, os
   d = json.load(open('/Users/aretesofia/IbogaineVault-Tier1/papers.json'))
   risks = []
   for p in d['papers']:
       oa = p.get('open_access')
       bf = p.get('body_format')
       fp = p.get('filepath', '')
       full = os.path.join('/Users/aretesofia/IbogaineVault-Tier1', fp)
       if os.path.exists(full):
           lines = sum(1 for _ in open(full))
       else:
           lines = 0
       if oa in [False, 'false'] and bf == 'academic-retained' and lines > 200:
           risks.append((fp, lines, p.get('publisher'), p.get('journal')))
   print(f'HIGH RISK papers remaining: {len(risks)}')
   for r in risks:
       print(f'  {r[0]}  ({r[1]} lines, {r[2]}, {r[3]})')
   "
   Should be 0. If any remain, they must be either reconverted or consciously accepted with documented reasoning.

6. FULL Pangea contamination sweep:
   grep -ri "pangea" /Users/aretesofia/IbogaineVault-Tier1/ --include='*.md' --include='*.py' --include='*.yml' -l
   Only legitimate published mentions should remain (e.g., Wilkins2017 mentioning the facility as published fact, Nardou2023 disclosure without the parenthetical). No operational or internal references.

7. UPDATE CITATION.cff in Tier 1:
   - date-released: set to today's actual date (the day you're running this)
   - version: 1.0.0

8. VERIFY internal consistency of stats claims:
   - Paper count in README.md vs actual paper count in papers.json
   - Wikilink count in README.md vs actual (grep -roh '\[\[' --include='*.md' | wc -l)
   - Tag count claim vs actual
   These numbers must match within a reasonable margin (~5%). If README says "~300 documents" and there are 297, that's fine.

9. CHECK for any files that shouldn't be in Tier 1:
   - No .pdf files: find /Users/aretesofia/IbogaineVault-Tier1 -name '*.pdf' | wc -l → must be 0
   - No Pangea_Ops/: test -d /Users/aretesofia/IbogaineVault-Tier1/Pangea_Ops && echo "FAIL" || echo "PASS"
   - No CLAUDE.md: test -f /Users/aretesofia/IbogaineVault-Tier1/CLAUDE.md && echo "FAIL" || echo "PASS"
   - No Cowork_Outputs/: test -d /Users/aretesofia/IbogaineVault-Tier1/Cowork_Outputs && echo "FAIL" || echo "PASS"
   - No copilot/: test -d /Users/aretesofia/IbogaineVault-Tier1/copilot && echo "FAIL" || echo "PASS"

10. PRODUCE a final summary report:

    === IbogaineVault-Tier1 Ship Readiness Report ===
    Date: [today]
    
    CORPUS:
    - Total papers: [count from papers.json]
    - Total wikilinks: [grep count]
    - Broken wikilinks: [from validator]
    - Canonical tags: [count]
    
    IDENTIFIER COVERAGE:
    - Papers with DOI:    [count]/[total] ([pct]%)
    - Papers with PMID:   [count]/[total] ([pct]%)
    - Papers with PMCID:  [count]/[total] ([pct]%)
    - Papers with ISSN:   [count]/[total] ([pct]%)
    
    BODY FORMAT DISTRIBUTION:
    - vault-analytical:   [count]
    - academic-retained:  [count]
    - hybrid:            [count]
    - narrative:         [count]
    
    OPEN ACCESS STATUS:
    - true:    [count]
    - false:   [count]
    - unknown: [count]
    
    COPYRIGHT RISK:
    - HIGH RISK (non-OA + academic-retained + >200 lines): [count] — [list if >0]
    - Papers consciously accepted: [list with reasoning]
    
    BLOCKER STATUS:
    - BLOCKER 1 (_meta/README.md): [PASS/FAIL]
    - BLOCKER 2 (wikilink counts): [PASS/FAIL]
    - BLOCKER 3 (schema Pangea):   [PASS/FAIL]
    - BLOCKER 4 (validator Pangea): [PASS/FAIL]
    - BLOCKER 5 (Wilkins MOC):     [PASS/FAIL]
    - BLOCKER 6 (Mash2000):        [PASS/FAIL]
    
    VERDICT: [READY TO SHIP / NOT READY — reasons]

11. If everything passes: state clearly "IbogaineVault-Tier1 is ready for public release" and provide the git commands:
    cd /Users/aretesofia/IbogaineVault-Tier1
    git add .
    git commit -m "v1.0.0: IbogaineVault-Tier1 public release"
    git push

After completing, ask: "Shall I update the worklog?"
```

---
## Execution Notes

**Order matters:** Run prompts 1 → 2 → 3 → 4 → 5 → 6 sequentially. Each depends on the previous.

**Time estimates:**
- Prompt 1: 20-30 min (schema + tooling changes)
- Prompt 2: 30-45 min (script writing + population + review)
- Prompt 3: 45-60 min (API lookups are slow due to rate limiting — ~300+ requests at 1/sec)
- Prompt 4: 30-45 min (sync script upgrade + testing)
- Prompt 5: 30-60 min (reconversions depend on how many papers are flagged — Mash2000 alone is 20 min)
- Prompt 6: 15-20 min (verification pipeline)

**Total: ~3-4 hours of conversation time across 6 sessions.**

**If a prompt fails:** Fix the issue in the same conversation. Don't move to the next prompt until the current one's verification steps all pass.

**The sync script is the linchpin:** Prompt 4 is what prevents all future regressions. Until that's done, every fix in the working vault will be lost on the next sync. Prompts 1-3 can run before Prompt 4 because they modify the working vault (which persists). But Prompt 6 (final validation) absolutely requires Prompt 4 to be complete.

**Parallelism:** Prompts 1-3 (schema + metadata) and Prompt 4 (sync script) are independent tracks. If you want to run two conversations simultaneously, you can do 1→2→3 in parallel with 4. Just make sure both are complete before running 5 and 6.

**What these prompts DON'T cover (out of scope for Tier 1 release):**
- OA format consistency for all 97 GREEN papers (that's v1.1, per the 15 Mar decision)
- Email address stripping from paper bodies (low risk — these are published corresponding author emails)
- Wilkins2017 verbatim text assessment (published OA paper, lower copyright risk)
- Quartz web publishing layer (parallel track, not blocking Tier 1)
- Full ISSN population (Prompt 3 captures what CrossRef returns, but comprehensive ISSN lookup is a future task)
