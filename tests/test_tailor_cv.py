import json, sys, pathlib
import docx
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import tailor_cv


def make_cv(path):
    d = docx.Document()
    d.add_paragraph("EXPERIENCE")
    for t in ["Lead a team of four", "Own the annual plan", "Reversed a major cut", "Co-design incentives"]:
        p = d.add_paragraph()
        r = p.add_run(t)
        r.bold = t.startswith("Lead")
    d.save(path)


def texts(path):
    return [p.text for p in docx.Document(path).paragraphs]


def test_spec_is_applied_in_order(tmp_path):
    base, out, spec = tmp_path / "base.docx", tmp_path / "out.docx", tmp_path / "spec.json"
    make_cv(base)
    spec.write_text(json.dumps({
        "replace": [{"startswith": "Own the annual", "text": "Own the annual plan and reforecast"}],
        "insert_after": [{"startswith": "Reversed", "id": "new", "text": "Built a new model"}],
        "order": {"after": "Lead a team", "bullets": ["@new", "Reversed", "Own the annual"]},
        "remove": ["Co-design"],
    }))
    tailor_cv.main(base, spec, out)
    assert texts(out) == ["EXPERIENCE", "Lead a team of four", "Built a new model",
                          "Reversed a major cut", "Own the annual plan and reforecast"]


def test_replace_keeps_first_run_formatting(tmp_path):
    base, out, spec = tmp_path / "base.docx", tmp_path / "out.docx", tmp_path / "spec.json"
    make_cv(base)
    spec.write_text(json.dumps({"replace": [{"startswith": "Lead a team", "text": "Lead a team of six"}]}))
    tailor_cv.main(base, spec, out)
    p = [p for p in docx.Document(out).paragraphs if p.text.startswith("Lead")][0]
    assert p.runs[0].bold is True


def test_ambiguous_prefix_fails(tmp_path):
    base = tmp_path / "base.docx"
    make_cv(base)
    d = docx.Document(base)
    try:
        tailor_cv.find(d, "")
    except SystemExit as e:
        assert "Expected one paragraph" in str(e)
    else:
        raise AssertionError("expected SystemExit")
