from pathlib import Path
from web.build import build_site


def test_build_produces_expected_files(tmp_path):
    issues_dir = Path(__file__).parent.parent / "issues"
    build_site(issues_dir=issues_dir, output_dir=tmp_path)

    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "1994-vol1" / "index.html").exists()
    assert (tmp_path / "1994-vol1" / "dq5" / "index.html").exists()
    assert (tmp_path / "1994-vol1" / "kick-king" / "index.html").exists()
    assert (tmp_path / "1994-vol1" / "p003" / "index.html").exists()
    assert (tmp_path / "search" / "index.html").exists()
    assert (tmp_path / "search-index.json").exists()
    assert (tmp_path / "static" / "style.css").exists()
    assert (tmp_path / "static" / "search.js").exists()


def test_build_article_html_contains_content(tmp_path):
    issues_dir = Path(__file__).parent.parent / "issues"
    build_site(issues_dir=issues_dir, output_dir=tmp_path)

    dq5_html = (tmp_path / "1994-vol1" / "dq5" / "index.html").read_text(encoding="utf-8")
    assert "勇者斗恶龙" in dq5_html
    assert "天堂任鸟飞" in dq5_html
    assert "韩友" in dq5_html


def test_build_index_links_to_issue(tmp_path):
    issues_dir = Path(__file__).parent.parent / "issues"
    build_site(issues_dir=issues_dir, output_dir=tmp_path)

    index_html = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert "1994-vol1" in index_html
