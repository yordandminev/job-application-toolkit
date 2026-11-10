#!/usr/bin/env python3
"""Tailor a DOCX CV from a JSON spec while keeping the original formatting.

The spec is a JSON object with any of these keys, applied in this order:

  "replace":       [{"startswith": "Lead a team", "text": "New bullet text"}]
  "insert_after":  [{"startswith": "Reversed a major", "text": "New bullet",
                     "id": "finance-models"}]
  "order":         {"after": "Lead a team",
                    "bullets": ["Own account", "Build the business", "@finance-models"]}
  "remove":        ["Run the team's product roadmap"]

Paragraphs are matched by the start of their text, so the spec stays readable.
New bullets copy the formatting of the paragraph they are inserted after.
In "order", "@id" refers to a bullet created by "insert_after".

Usage: python tailor_cv.py base.docx spec.json out.docx
"""
import copy
import json
import sys

import docx
from docx.text.paragraph import Paragraph


def find(doc, prefix):
    """Return the single paragraph whose text starts with prefix."""
    hits = [p for p in doc.paragraphs if p.text.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f"Expected one paragraph starting with {prefix!r}, found {len(hits)}")
    return hits[0]


def set_text(paragraph, text):
    """Replace paragraph text, keeping the formatting of the first run."""
    runs = paragraph.runs
    if not runs:
        paragraph.add_run(text)
        return
    runs[0].text = text
    for run in runs[1:]:
        run._r.getparent().remove(run._r)


def main(base, spec_path, out):
    doc = docx.Document(base)
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)

    for item in spec.get("replace", []):
        set_text(find(doc, item["startswith"]), item["text"])

    created = {}
    for item in spec.get("insert_after", []):
        anchor = find(doc, item["startswith"])
        new_p = copy.deepcopy(anchor._p)
        anchor._p.addnext(new_p)
        para = Paragraph(new_p, anchor._parent)
        set_text(para, item["text"])
        if "id" in item:
            created[item["id"]] = para

    order = spec.get("order")
    if order:
        anchor = find(doc, order["after"])._p
        for key in order["bullets"]:
            para = created[key[1:]] if key.startswith("@") else find(doc, key)
            anchor.addnext(para._p)
            anchor = para._p

    for prefix in spec.get("remove", []):
        p = find(doc, prefix)._p
        p.getparent().remove(p)

    doc.save(out)
    print(f"Saved {out}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
