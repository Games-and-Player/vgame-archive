import re
from web.models import Issue, Article, Page

_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(html: str) -> str:
    return _TAG_RE.sub("", html)


def _snippet(body_md: str, max_len: int = 300) -> str:
    text = body_md.strip()
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith(">") or stripped == "---":
            continue
        if stripped:
            lines.append(stripped)
    joined = " ".join(lines)
    if len(joined) > max_len:
        return joined[:max_len].rsplit(" ", 1)[0] + "…"
    return joined


def build_search_index(issues: list[Issue]) -> list[dict]:
    entries = []
    for issue in issues:
        for article in issue.articles:
            entries.append({
                "title": article.title,
                "section": article.section,
                "author": article.author or "",
                "games": article.games,
                "issue": issue.slug,
                "slug": article.slug,
                "kind": "article",
                "url": f"/{issue.slug}/{article.slug}/",
                "snippet": _snippet(article.body_md),
            })
        for page in issue.pages:
            entries.append({
                "title": page.title,
                "section": page.section,
                "author": page.author or "",
                "games": page.games,
                "issue": issue.slug,
                "slug": page.slug,
                "kind": "page",
                "url": f"/{issue.slug}/{page.slug}/",
                "snippet": _snippet(page.body_md),
            })
    return entries
