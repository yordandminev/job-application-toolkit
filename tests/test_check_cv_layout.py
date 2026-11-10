import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from check_cv_layout import parse_bullets, find_problems

SAMPLE = """EXPERIENCE
• Lead a team of 4-6 as analytics partner to the business unit
  leadership and the account managers
• Built a model that became the standard for planning and deal
  decisions
• One-line bullet
EDUCATION
"""


def test_parse_bullets_counts_lines():
    found = parse_bullets(SAMPLE)
    assert [n for _, n, _ in found] == [2, 2, 1]


def test_orphan_word_is_flagged():
    problems = find_problems(2, parse_bullets(SAMPLE))
    assert any("orphan last word 'decisions'" in p for p in problems)


def test_page_and_line_limits():
    long_bullet = [("• Long bullet", 4, "ends here fine")]
    problems = find_problems(3, long_bullet, max_pages=2, max_lines=3)
    assert "3 pages (max 2)" in problems
    assert any(p.startswith("4 lines") for p in problems)


def test_clean_layout_has_no_problems():
    assert find_problems(2, [("• Fine", 2, "a normal last line")]) == []
