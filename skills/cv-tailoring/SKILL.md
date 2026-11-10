---
name: cv-tailoring
description: Build a tailored 2-page CV (DOCX + PDF) for a posting from the closest previous tailored CV and approved content-library variants, then check the layout.
---

# CV tailoring

## Steps
1. Pick the base: the previous tailored CV closest to this role family (finance, product, operations, AI), or the master CV.
2. Summary: read the posting's signals (manager vs hands-on IC, years asked, startup or corporate, function) and pick the headline pattern from `docs/positioning-playbook.md`. Keep an honest label (never the posting's job title); sentence 2 carries the posting's two or three key themes using library wording.
3. Bullets: lead with the 2-3 bullets that answer the posting's first requirements; swap in library variants rather than writing new claims; drop the least relevant bullets to stay at 2 pages.
4. Skills line: only tools I use; add posting keywords only when true.
5. Write the changes as a JSON spec and apply it with `scripts/tailor_cv.py`, so formatting stays intact.
6. Run `scripts/check_cv_layout.py --keep-pdf`: max 2 pages, bullets max 3 lines, no orphan last word.
7. Save as `<Name>_CV_<Company>_<YYYY-MM-DD>.docx/.pdf`; move the previous version to `Not final/` with a `vN_` prefix.

## Rules
- Follow `docs/writing-rules.md` for bullets, numbers and credit ("my team" vs "I").
- Facts only. Every number must match the master CV. New facts I give in conversation go into the content library first.
- Separate wins stay separate: never write one project's result as the outcome of another.
- Present tense for current work.
