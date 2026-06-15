import pytest
from pathlib import Path
from web.parser import parse_md_file


@pytest.fixture
def fixtures(tmp_path):
    """Create test fixtures."""
    d = tmp_path / "fixtures"
    d.mkdir()

    (d / "article.md").write_text(
        "---\n"
        "issue: 1994-vol1\n"
        "title: 勇者斗恶龙 V 快速攻略\n"
        "section: 天堂任鸟飞\n"
        "pdf_pages: [6, 7, 8]\n"
        "mag_pages: [4, 5, 6]\n"
        "author: 韩友\n"
        "games:\n  - dq5\n"
        "status: 已完结（PDF 6-8 全文转录完成）\n"
        "---\n\n"
        "# 勇者斗恶龙 V\n\n"
        "> 栏目：天堂任鸟飞\n\n"
        "正文内容。\n\n"
        "| 列A | 列B |\n|---|---|\n| 1 | 2 |\n",
        encoding="utf-8",
    )

    (d / "page.md").write_text(
        "---\n"
        "issue: 1994-vol1\n"
        "pdf_page: 3\n"
        "mag_page: 1\n"
        "section: 卷首语\n"
        "title: 闯关族的舞台\n"
        "author: 重凡\n"
        "games: []\n"
        "---\n\n"
        "# 闯关族的舞台\n\n"
        "卷首语正文。\n",
        encoding="utf-8",
    )

    return d


def test_parse_article(fixtures):
    result = parse_md_file(fixtures / "article.md")
    assert result["meta"]["title"] == "勇者斗恶龙 V 快速攻略"
    assert result["meta"]["section"] == "天堂任鸟飞"
    assert result["meta"]["pdf_pages"] == [6, 7, 8]
    assert result["meta"]["games"] == ["dq5"]
    assert result["kind"] == "article"


def test_parse_page(fixtures):
    result = parse_md_file(fixtures / "page.md")
    assert result["meta"]["title"] == "闯关族的舞台"
    assert result["meta"]["pdf_page"] == 3
    assert result["kind"] == "page"


def test_body_html_has_table(fixtures):
    result = parse_md_file(fixtures / "article.md")
    assert "<table>" in result["body_html"]
    assert "列A" in result["body_html"]


def test_body_html_has_blockquote(fixtures):
    result = parse_md_file(fixtures / "article.md")
    assert "<blockquote>" in result["body_html"]
