#!/usr/bin/env python3
"""Render a DOCX CV to PDF and check the layout rules.

Checks:
  * page count is at most --max-pages (default 2)
  * no bullet runs longer than --max-lines (default 3)
  * no bullet ends with a single orphan word on its last line

Usage: python check_cv_layout.py cv.docx [--max-pages 2] [--max-lines 3] [--keep-pdf]
Requires LibreOffice (soffice) and Poppler (pdftotext, pdfinfo).
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

BULLET = "•"


def to_pdf(docx_path, out_dir):
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(docx_path)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return out_dir / (docx_path.stem + ".pdf")


def page_count(pdf):
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", info).group(1))


def parse_bullets(text):
    """Return (first_line, line_count, last_line) for every bullet in pdftotext -layout output."""
    found, current = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(BULLET):
            if current:
                found.append((current[0], len(current), current[-1]))
            current = [line]
        elif current and raw.startswith("  ") and line and not line.startswith("Page "):
            current.append(line)
        else:
            if current:
                found.append((current[0], len(current), current[-1]))
            current = None
    if current:
        found.append((current[0], len(current), current[-1]))
    return found


def bullets(pdf):
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                          capture_output=True, text=True, check=True).stdout
    return parse_bullets(text)


def find_problems(pages, bullet_list, max_pages=2, max_lines=3):
    """Return a list of human-readable layout problems."""
    problems = []
    if pages > max_pages:
        problems.append(f"{pages} pages (max {max_pages})")
    for first, n, last in bullet_list:
        label = first[:70]
        if n > max_lines:
            problems.append(f"{n} lines: {label}...")
        if n > 1 and len(last.split()) == 1:
            problems.append(f"orphan last word '{last}': {label}...")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx", type=pathlib.Path)
    ap.add_argument("--max-pages", type=int, default=2)
    ap.add_argument("--max-lines", type=int, default=3)
    ap.add_argument("--keep-pdf", action="store_true", help="save the PDF next to the DOCX")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        pdf = to_pdf(args.docx, pathlib.Path(tmp))
        pages = page_count(pdf)
        problems = find_problems(pages, bullets(pdf), args.max_pages, args.max_lines)
        if args.keep_pdf:
            shutil.copy(pdf, args.docx.with_suffix(".pdf"))

    print(f"Pages: {pages}")
    if problems:
        print("Layout problems:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("Layout OK")


if __name__ == "__main__":
    main()
