# Folder structure and versioning

```
Job Search/
├── CV/
│   ├── YYYY-MM-DD <Name>_Main_CV.docx / .pdf            # master CV (2 pages)
│   ├── YYYY-MM-DD <Name>_Main_CV_Background_Materials.docx   # content library
│   ├── <Story bank>.pdf                                  # STAR interview stories
│   └── Old versions/
├── Cover Letters/
│   ├── Cover_Letter_Template_and_Content_Library.docx
│   ├── README_for_Claude.md                              # letter rules for the agent
│   └── Old versions/
└── Job Applications/
    ├── Job Search Tracker                                # one row per application
    └── <Company>/
        └── <Requisition ID> <Role>/
            ├── <Role> - Job Description.pdf
            ├── Link to posting.docx
            ├── <Company>_<Role>_Fit.md
            ├── <Name>_CV_<Company>_<date>.docx / .pdf
            ├── <Name>_Cover_Letter_<Company>_<Role>.docx / .pdf   (if required)
            └── Not final/                                # v1_, v2_ ... earlier drafts
```

## Conventions
- A role folder keeps only the latest files; every replaced draft moves to `Not final/` with a `vN_` prefix, so the history is never lost.
- The master CV and content library are dated in the file name; the previous version moves to `Old versions/`.
- If the full posting cannot be saved, the job description PDF is labelled "(summary)".
- After submission: update the tracker, then copy any new wording into the content library and letter library.
