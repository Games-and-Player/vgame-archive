import re
from pathlib import Path
import frontmatter
import markdown


_md = markdown.Markdown(extensions=["tables", "fenced_code", "footnotes", "md_in_html"])

_HTML_BLOCK_RE = re.compile(r"<(aside|div|section)(\s[^>]*)?>", re.IGNORECASE)


def _inject_markdown_attr(text: str) -> str:
    """Add markdown="1" to HTML block tags so md_in_html processes their content."""
    def _add_attr(m):
        tag = m.group(1)
        attrs = m.group(2) or ""
        if "markdown" in attrs:
            return m.group(0)
        return f"<{tag}{attrs} markdown=\"1\">"
    return _HTML_BLOCK_RE.sub(_add_attr, text)


def parse_md_file(path: Path) -> dict:
    """Parse a markdown file with YAML frontmatter.

    Returns dict with keys: meta (dict), body_md (str), body_html (str), kind (str), slug (str).
    """
    post = frontmatter.load(path)
    meta = dict(post.metadata)

    _md.reset()
    body_html = _md.convert(_inject_markdown_attr(post.content))

    kind = "article" if "pdf_pages" in meta else "page"
    slug = path.stem

    return {
        "meta": meta,
        "body_md": post.content,
        "body_html": body_html,
        "kind": kind,
        "slug": slug,
    }
