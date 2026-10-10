# History Notes & Flashcards

A reusable, transcript-grounded AI skill for turning lengthy **history lecture recordings** into concise **PDF study notes** and **separate Anki decks for completed units**.

The workflow is intentionally **human-in-the-loop**: you transcribe the audio yourself with Turbo AI, then provide the resulting transcripts. It does **not** automate Turbo AI, claim a Turbo AI API integration, or transcribe recordings on its own.

## How it works

1. Supply a lecture audio file and the course syllabus (or unit-topic list).
2. Split the recording into consecutive **30-minute audio segments** using the included helper script.
3. Upload the segments to **Turbo AI manually** and provide the resulting transcripts in chronological order.
4. Identify syllabus-defined units, even if a unit crosses recordings or starts midway through a lecture.
5. Create or update **concise, exam-focused PDF notes**, ordered by syllabus topic.
6. Keep unfinished units **in progress**. **Do not generate flashcards yet.**
7. Once a unit is completed, generate **one separate Anki TSV file per unit**. Never combine units into one deck.

### Notes format

For each unit:

```text
<Unit title exactly as shown on syllabus>

Main Ideas
- Key event, person, group, or theme
- Another main idea

Notes
Key topic
- Concise explanation supported by the transcript
- Important names, dates, events, and cause/effect relationships emphasized
```

No unit numbers or numbered notes subsections. See [`examples/sample_notes.md`](examples/sample_notes.md) for a **fictional formatting demonstration**.

## Use as a skill

The main instructions live in [`SKILL.md`](SKILL.md). In a compatible file-based AI skill environment, place this folder in the location prescribed by that environment. **Import/install is environment-dependent**; adding the repository does not automatically install a skill in ChatGPT.

Alternatively, provide `SKILL.md` and your syllabus to an assistant that supports file uploads and ask it to follow the instructions. An AI environment must have PDF-generation and file-handling capabilities to deliver the outputs.

## Split the audio

Requires Python 3.9+ and [`ffmpeg`](https://ffmpeg.org/) / `ffprobe` on your PATH.

```bash
python scripts/split_audio.py "lecture.m4a" --output-dir segments --minutes 30
```

The script writes chronologically named `.m4a` clips, using AAC encoding. It does not upload anything to Turbo AI. Actual segment length can vary slightly due to codec timing. Verify the resulting clips before transcription.

## Anki import

Each completed unit produces an independent UTF-8 tab-separated file (TSV), with Basic note fields: **Front**, **Back**, **Tags**. A deck header can request a unit-specific deck; if your Anki version ignores it, choose the target deck during import. See [`examples/sample_unit_anki.tsv`](examples/sample_unit_anki.tsv).

In Anki desktop, use **File → Import**, select the TSV file, inspect field mappings, and confirm the correct destination deck. For repeated imports, check for duplicate notes.

## Accuracy and privacy

- History facts come **only from user-supplied lecture transcripts**; the syllabus controls headings and ordering.
- Unclear names, dates, or unit transitions trigger clarification rather than guessing.
- Do not treat recording boundaries as unit boundaries.
- Do not publish user recordings, verbatim lecture transcripts, private syllabi, classroom notes, or lecture-derived flashcards to a public repository without permission.
- Examples here are fictional, not from a real course or professor.

## Project layout

```text
history-notes-flashcards/
├── SKILL.md
├── README.md
├── LICENSE
├── .gitignore
├── scripts/
│   └── split_audio.py
├── examples/
│   ├── sample_notes.md
│   └── sample_unit_anki.tsv
└── references/
    └── syllabus-template.md
```

## License

Licensed under the [MIT License](LICENSE). See the license file for the complete terms.
