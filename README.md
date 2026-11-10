# AI Job Application Toolkit

A personal system for running a focused job search with an AI agent (Claude) as the analyst and drafter, and me as the editor and decision maker.

I built it because tailoring every application by hand does not scale, and generic AI output does not survive a close read. The toolkit turns one well-maintained source of truth (a master CV, a content library and a story bank) into tailored, fact-checked application packages, and it gets better with every application.

## What it does

```
Role search ──► Job posting ──► Fit analysis ──► Tailored CV ──► Form answers / cover letter ──► Saved package ──► Library update
                   (URL)        (score 0-10,      (DOCX + PDF,    (only facts from the            (versioned       (best new wording
                                 gaps, risks)      2-page check)    library or my own words)        folder)          flows back)
```

0. **Role discovery** (`skills/role-discovery`): screens job-alert emails, job boards and career pages against a search profile, drops hard no-gos and ranks a shortlist.
1. **Fit analysis** (`skills/fit-analysis`): reads the posting, maps each requirement to evidence, scores fit 0-10, names the gaps a recruiter will screen on and the risks the CV cannot fix (location, level, language).
2. **CV tailoring** (`skills/cv-tailoring`, `scripts/tailor_cv.py`): starts from the closest previous tailored CV, swaps in approved bullet variants from the content library, reorders bullets to match the posting's priorities, and keeps the original formatting.
3. **Layout check** (`scripts/check_cv_layout.py`): renders the DOCX to PDF and flags anything over 2 pages, bullets over 3 lines and bullets that end on a single orphan word.
4. **Answers and letters** (`skills/application-answers`, `skills/cover-letter`): drafts form answers and letters in a defined house style.
5. **Packaging** (`docs/folder-structure.md`): saves everything in one folder per company and role, with older drafts versioned in `Not final/`.
6. **Story bank** (`skills/story-bank`): every achievement lives once, in STAR form, with approved numbers and short variants for CV bullets, letter proof points and form answers.
7. **Feedback loop** (`skills/library-update`): after each submission, the final CV, letter and answers flow back into the content library and story bank, labelled by role type, so the next application starts stronger.

## Design principles

- **Facts only, enforced.** Every claim (number, tool, method, outcome) must trace to the master CV, the content library, the story bank or something I said. If a stronger point would help but isn't documented, the agent asks instead of filling the gap. This is the single most important rule: an invented detail can be probed in an interview.
- **Honest scoring.** The fit score is meant to inform the decision to apply, not to flatter. Gaps are named plainly, and "skip" is a valid recommendation.
- **One source of truth, many variants.** The content library holds alternative wordings for each achievement (finance, product, supply, AI framing). Tailoring means choosing and ordering, not rewriting from scratch.
- **Human in the loop.** The agent drafts and checks; I decide what is sent. Every edit request gets pros and cons, not just agreement.
- **Persistent memory.** Decisions, corrections and style feedback are saved as short memory notes, so a new session does not repeat old mistakes.

## Repository layout

| Path | What it is |
|---|---|
| `skills/` | Claude skills (SKILL.md files) for each step of the workflow |
| `scripts/tailor_cv.py` | Applies a JSON spec (text swaps, new bullets, reorder, removals) to a DOCX CV while keeping its formatting |
| `scripts/check_cv_layout.py` | Converts a DOCX to PDF with LibreOffice and checks page count and bullet length |
| `templates/` | Fit analysis template and a tailoring spec example |
| `docs/folder-structure.md` | The folder and versioning conventions |
| `examples/` | A fictional, fully anonymized example of a fit analysis |

## Requirements

- Python 3.10+ with `python-docx`
- LibreOffice (`soffice`) and Poppler (`pdftotext`, `pdfinfo`) for the layout check
- Claude (or another agent that can read skills and work with local files)

```bash
pip install python-docx
python scripts/tailor_cv.py base_cv.docx templates/tailoring_spec_example.json tailored_cv.docx
python scripts/check_cv_layout.py tailored_cv.docx --max-pages 2 --max-lines 3
```

## Privacy

This repository contains the system only. Personal documents (CVs, letters, the content library, the application tracker) stay in a private local folder and are never committed.
