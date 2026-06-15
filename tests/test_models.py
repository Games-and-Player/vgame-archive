from pathlib import Path
from web.models import load_issue, Page, Article


def test_load_issue_from_real_data():
    """Integration test: load 1994-vol1 from actual project files."""
    issues_dir = Path(__file__).parent.parent / "issues"
    issue = load_issue(issues_dir / "1994-vol1")

    assert issue.slug == "1994-vol1"
    assert len(issue.articles) >= 3  # dq5, dice-king, kick-king
    assert len(issue.pages) >= 2  # p003, p005

    dq5 = next(a for a in issue.articles if a.slug == "dq5")
    assert dq5.title == "勇者斗恶龙 V 快速攻略"
    assert dq5.section == "天堂任鸟飞"
    assert dq5.pdf_pages == [6, 7, 8, 9, 10, 11, 12, 13]

    p003 = next(p for p in issue.pages if p.slug == "p003")
    assert p003.title == "闯关族的舞台"
    assert p003.section == "卷首语"


def test_issue_sections():
    """Sections are extracted and ordered from articles + pages."""
    issues_dir = Path(__file__).parent.parent / "issues"
    issue = load_issue(issues_dir / "1994-vol1")
    sections = issue.sections()
    assert "天堂任鸟飞" in sections
    assert "卷首语" in sections


def test_issue_all_entries_sorted():
    """all_entries() returns articles + pages sorted by first pdf page."""
    issues_dir = Path(__file__).parent.parent / "issues"
    issue = load_issue(issues_dir / "1994-vol1")
    entries = issue.all_entries()
    pdf_starts = []
    for e in entries:
        if isinstance(e, Article):
            pdf_starts.append(e.pdf_pages[0])
        else:
            pdf_starts.append(e.pdf_page)
    assert pdf_starts == sorted(pdf_starts)
