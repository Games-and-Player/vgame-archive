import json
import shutil
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from web.models import load_issue, Issue, Article, Page
from web.search import build_search_index

TEMPLATES_DIR = Path(__file__).parent / "templates"
STATIC_DIR = Path(__file__).parent / "static"
DEFAULT_ISSUES = Path(__file__).parent.parent / "issues"
DEFAULT_OUTPUT = Path(__file__).parent.parent / "dist"


def build_site(
    issues_dir: Path = DEFAULT_ISSUES,
    output_dir: Path = DEFAULT_OUTPUT,
):
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )

    # Load all issues
    issues: list[Issue] = []
    for d in sorted(issues_dir.iterdir()):
        if d.is_dir() and (d / "README.md").exists():
            issues.append(load_issue(d))

    # Clean and create output dir
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    # Copy static files
    static_out = output_dir / "static"
    shutil.copytree(STATIC_DIR, static_out)

    # Render home page
    tpl = env.get_template("index.html")
    (output_dir / "index.html").write_text(
        tpl.render(issues=issues), encoding="utf-8"
    )

    # Render each issue
    for issue in issues:
        issue_dir = output_dir / issue.slug
        issue_dir.mkdir(parents=True, exist_ok=True)

        # Copy assets if they exist
        src_assets = issues_dir / issue.slug / "assets"
        if src_assets.is_dir():
            shutil.copytree(src_assets, issue_dir / "assets")

        # Issue index page
        tpl = env.get_template("issue.html")
        (issue_dir / "index.html").write_text(
            tpl.render(issue=issue), encoding="utf-8"
        )

        # All entries (articles + pages) for prev/next nav
        all_entries = issue.all_entries()

        for i, entry in enumerate(all_entries):
            entry_dir = issue_dir / entry.slug
            entry_dir.mkdir(parents=True, exist_ok=True)

            prev_entry = all_entries[i - 1] if i > 0 else None
            next_entry = all_entries[i + 1] if i < len(all_entries) - 1 else None

            if isinstance(entry, Article):
                tpl = env.get_template("article.html")
            else:
                tpl = env.get_template("page.html")

            (entry_dir / "index.html").write_text(
                tpl.render(
                    issue=issue,
                    entry=entry,
                    prev_entry=prev_entry,
                    next_entry=next_entry,
                ),
                encoding="utf-8",
            )

    # Search page
    search_dir = output_dir / "search"
    search_dir.mkdir(parents=True, exist_ok=True)
    tpl = env.get_template("search.html")
    (search_dir / "index.html").write_text(
        tpl.render(issues=issues), encoding="utf-8"
    )

    # Search index JSON
    index = build_search_index(issues)
    (output_dir / "search-index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=None), encoding="utf-8"
    )

    print(f"Built {len(issues)} issue(s) → {output_dir}")


if __name__ == "__main__":
    issues = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ISSUES
    build_site(issues_dir=issues)
