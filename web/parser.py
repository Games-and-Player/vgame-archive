from pathlib import Path
import frontmatter
import markdown


_md = markdown.Markdown(extensions=["tables", "fenced_code", "footnotes"])


def parse_md_file(path: Path) -> dict:
    """Parse a markdown file with YAML frontmatter.

    Returns dict with keys: meta (dict), body_md (str), body_html (str), kind (str), slug (str).
    """
    post = frontmatter.load(path)
    meta = dict(post.metadata)

    _md.reset()
    body_html = _md.convert(post.content)

    kind = "article" if "pdf_pages" in meta else "page"
    slug = path.stem

    return {
        "meta": meta,
        "body_md": post.content,
        "body_html": body_html,
        "kind": kind,
        "slug": slug,
    }
