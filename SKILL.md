---
name: history-notes-flashcards
description: Convert long history lecture recordings into 30-minute audio segments for manual Turbo AI transcription, then organize transcripts into concise syllabus-ordered PDF notes and create separate Anki import decks only when each history unit is complete.
---

# History Notes & Flashcards

## Purpose and approved style
Transform lecture recordings and manually supplied Turbo AI transcripts into study notes and (when appropriate) Anki flashcards. Follow the structural example in `examples/sample_notes.md` for layout and density, while honoring any user-provided approved reference PDF. This skill is *not* permission to assume missing information. Ask when unsure.

## Hard rules
1. **Source boundary:** History facts in notes and cards must come **only** from the user-provided lecture transcripts. The syllabus is for unit names and order, not for supplementing historical content. Do not browse or introduce textbook facts without explicit permission. Do not silently fix a date, name, claim, or apparent transcription error from background knowledge. If unclear and material, ask the user; otherwise flag it transparently.
2. **No assumptions:** If uncertain about whether a topic fits a unit, chronology of segment transcripts, unit completion, transcript gaps, or material historical terminology, ask a precise clarification. Don't stall for trivial details already provided.
3. **Units:** A unit is a *lecture topic named in the syllabus*, **not** a week, exam, file, or 30-minute segment. Titles must match syllabus titles and units must be displayed **in the order they occur in the syllabus**, even if audio discusses them out of order. Do not number units or subsection headings.
4. **Notes layout:** Each unit has (a) the **Unit name as its heading** (no "Unit 1" label), (b) **Main Ideas** with a short bulleted outline, (c) **Notes** with unnumbered bold topic labels and concise bulleted explanations. Bold important names, events, dates, groups, terms, and cause/effect statements where helpful. No colorful category pills or obligatory tags in PDFs.
5. **Detail:** Match the concise, exam-oriented density and styling of the approved sample notes. Capture professor-emphasized points, essential context, chronological connections, causes/effects, and significance. Cut verbal filler and duplicate tangents; do not flatten nuanced explanations into vague single sentences.
6. **Cross-lecture continuity:** Audio boundaries and lecture boundaries do not imply unit boundaries. If a lecture ends midway through a unit, publish the partial unit notes and mark its status **In progress** in a separate status report. When the next lecture resumes, integrate the new material into the **same** unit and regenerate its current notes without duplicating material. Update its Main Ideas. Keep an internal manifest of which transcript parts contribute to each unit. If completion is uncertain, ask, do not assume.
7. **Flashcards only upon completion:** **Never generate a deck or even provisional cards for an in-progress unit.** After a unit is confirmed completed (by clear transition to the next syllabus unit or user confirmation), generate **one separate Anki-compatible TSV import file per unit**. Never combine units within a deck/import file. If completed material later expands, revise that unit's deck rather than creating duplicates.
8. **Flashcard content:** Based on the completed notes, use the approved question style: major events, people, groups, causes, effects, significance. Strong, self-contained recall questions with concise accurate answers; avoid duplicates and low-value trivia. Use concise, exam-focused question-and-answer style. Have an explicit unique deck name matching the unit. Check a TSV import's columns and Anki mapping.
9. **Never claim a deliverable exists before verifying it.** Link only to paths created and checked in the current session. If the required rendering or audio tools are unavailable, state the limitation and ask for input or propose a supported path; do not invent attachments.

## Execution procedure

### A. Intake and audio splitting
- Accept the supplied audio file. If syllabus has not been provided, request it before assigning units; if already provided, reuse it.
- Get real audio duration with `ffprobe` (never infer from the filename).
- Split consecutively at **00:00, 30:00, 60:00, ...** until the final remainder; no intentional gaps or overlap. Use `scripts/split_audio.py` if Python and ffmpeg/ffprobe are available. The script uses audio re-encoding for reasonably accurate boundaries (codec timing can cause small deviations). Generate meaningful chronological filenames including part number and time interval; retain input format if possible, otherwise output playable `.m4a`.
- Verify expected count, approximate segment durations and nonempty files. Provide separate links or a zip and tell user to upload segments to Turbo AI in order.
- **Turbo AI is manual**: do not pretend to log in, transcribe, or upload for user. Pause the workflow until the user returns the corresponding transcripts.

### B. Transcript ingestion
- Accept multiple transcript messages/text files. Map each transcript to its audio segment and preserve order. Missing segment(s): ask rather than blend discontinuous text silently.
- Assemble content conceptually by historical subject, not by splitting every 30 minutes; remove duplications at boundaries.
- Use the user-supplied syllabus (see `references/syllabus-template.md` for the expected structure) to map transcript themes to unit titles, preserving order.
- Flag material uncertainty explicitly (e.g., malformed named entities). Do not rewrite transcript facts based on outside sources without permission.

### C. Notes generation
- For each covered syllabus unit, create or update one logical unit record (`title`, `status`, `main_ideas`, `notes`, `source_segments`, `questions_for_user`).
- Output PDF containing units in syllabus order, with visual separation between units. Follow reference PDF: restrained, readable typography, main ideas bullets, Notes with bold unnumbered topical subsections and bullet explanations. Avoid section numbers.
- An in-progress unit gets current partial notes, with completion tracked in a small summary outside the PDF or discretely if user wants. Do not imply it is completed or create flashcards.
- Compare new transcripts against prior notes to merge sections, eliminate redundant passages, and add new information. If a previous PDF is not available, request that previous file; don't assume a fresh conversation contains it.

### D. Anki deck generation
- Determine whether each unit is completed. Evidence may be a clear professor introduction of the next syllabus topic, or user confirmation. Ambiguous => in progress; ask.
- Generate one **UTF-8 TSV per completed unit**, not a consolidated file. Prefer `#separator:Tab`, `#html:false`, `#notetype:Basic`, `#deck:<unit title>` header directives supported by Anki imports, then Front, Back, Tags fields as actual tab-separated data. Consider version compatibility: if header parsing not supported in the user's Anki version, explain how to select the right deck and map columns manually.
- Keep questions independent, answers specific, no unsupported historical content. Test for duplicate fronts, missing fields, malformed tabs/newlines, mixed-unit tags. Put cards in the target unit deck only. If an old deck exists, update carefully: avoid creating duplicate Anki notes; explain import/update limitations where relevant.

### E. Delivery and check-in
- Give verified links to the current notes PDF, completed-unit TSVs, and audio segments (when requested). Explicitly state which units are complete vs in progress and which decks are withheld.
- Ask about substantive uncertainties. Do not silently change the approved level of detail or formatting.

## PDF structural example (illustrative only; not historical content to inject)

# The Example Republic

## Main Ideas
- Causes of the war
- Major campaigns
- Treaty and consequences

## Notes
**Causes of the war**
- Concise transcript-grounded explanation with bolded important people, events, dates, and consequences.

**Treaty and consequences**
- Concise transcript-grounded explanation.

## Project reference files
- `references/syllabus-template.md`: a generic syllabus template; replace with a user-supplied syllabus at runtime.
- `examples/sample_notes.md`: fictional sample notes illustrating the approved format.
- `examples/sample_unit_anki.tsv`: fictional completed-unit Anki import example; never use its content as historical source material.
