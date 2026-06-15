import json
from pathlib import Path
from web.models import load_issue
from web.search import build_search_index


def test_search_index_structure():
    issues_dir = Path(__file__).parent.parent / "issues"
    issue = load_issue(issues_dir / "1994-vol1")
    index = build_search_index([issue])

    assert isinstance(index, list)
    assert len(index) >= 5  # 3 articles + 2 pages

    dq5 = next(e for e in index if e["slug"] == "dq5")
    assert dq5["title"] == "勇者斗恶龙 V 快速攻略"
    assert dq5["section"] == "天堂任鸟飞"
    assert dq5["issue"] == "1994-vol1"
    assert "url" in dq5
    assert "snippet" in dq5
    assert len(dq5["snippet"]) <= 300


def test_search_index_json_serializable():
    issues_dir = Path(__file__).parent.parent / "issues"
    issue = load_issue(issues_dir / "1994-vol1")
    index = build_search_index([issue])
    json_str = json.dumps(index, ensure_ascii=False)
    assert len(json_str) > 0
