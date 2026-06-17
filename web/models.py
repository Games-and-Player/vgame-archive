from dataclasses import dataclass, field
from pathlib import Path
from typing import Union
from web.parser import parse_md_file


@dataclass
class Article:
    slug: str
    title: str
    section: str
    author: str | None
    pdf_pages: list[int]
    mag_pages: list[int]
    games: list[str]
    status: str
    body_html: str
    body_md: str

    @property
    def first_pdf_page(self) -> int:
        return self.pdf_pages[0]

    @property
    def page_count(self) -> int:
        return len(self.pdf_pages)


@dataclass
class Page:
    slug: str
    title: str
    section: str
    author: str | None
    pdf_pages: list[int]
    mag_pages: list[int]
    games: list[str]
    body_html: str
    body_md: str

    @property
    def pdf_page(self) -> int:
        return self.pdf_pages[0] if self.pdf_pages else 0

    @property
    def mag_page(self) -> int | None:
        return self.mag_pages[0] if self.mag_pages else None

    @property
    def first_pdf_page(self) -> int:
        return self.pdf_pages[0] if self.pdf_pages else 0


@dataclass
class Issue:
    slug: str
    title: str
    articles: list[Article] = field(default_factory=list)
    pages: list[Page] = field(default_factory=list)

    def sections(self) -> list[str]:
        seen = {}
        for entry in self.all_entries():
            s = entry.section
            if s not in seen:
                seen[s] = entry.first_pdf_page
        return sorted(seen, key=lambda s: seen[s])

    def all_entries(self) -> list[Union[Article, Page]]:
        entries: list[Union[Article, Page]] = [*self.articles, *self.pages]
        return sorted(entries, key=lambda e: e.first_pdf_page)

    def entries_by_section(self) -> dict[str, list[Union[Article, Page]]]:
        result: dict[str, list] = {}
        for entry in self.all_entries():
            result.setdefault(entry.section, []).append(entry)
        return result


def load_issue(issue_dir: Path) -> Issue:
    slug = issue_dir.name
    readme = issue_dir / "README.md"
    title = slug
    if readme.exists():
        for line in readme.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break

    articles = []
    articles_dir = issue_dir / "articles"
    if articles_dir.is_dir():
        for md in sorted(articles_dir.glob("*.md")):
            data = parse_md_file(md)
            m = data["meta"]
            articles.append(Article(
                slug=data["slug"],
                title=m.get("title", data["slug"]),
                section=m.get("section", ""),
                author=m.get("author"),
                pdf_pages=m.get("pdf_pages", []),
                mag_pages=m.get("mag_pages", []),
                games=m.get("games", []),
                status=m.get("status", ""),
                body_html=data["body_html"],
                body_md=data["body_md"],
            ))

    pages = []
    pages_dir = issue_dir / "pages"
    if pages_dir.is_dir():
        for md in sorted(pages_dir.glob("*.md")):
            data = parse_md_file(md)
            m = data["meta"]
            raw_pdf = m.get("pdf_pages") or ([m["pdf_page"]] if m.get("pdf_page") else [])
            raw_mag = m.get("mag_pages") or ([m["mag_page"]] if m.get("mag_page") else [])
            pages.append(Page(
                slug=data["slug"],
                title=m.get("title", data["slug"]),
                section=m.get("section", ""),
                author=m.get("author"),
                pdf_pages=raw_pdf,
                mag_pages=raw_mag,
                games=m.get("games", []),
                body_html=data["body_html"],
                body_md=data["body_md"],
            ))

    return Issue(slug=slug, title=title, articles=articles, pages=pages)
