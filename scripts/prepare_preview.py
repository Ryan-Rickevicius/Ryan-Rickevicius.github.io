#!/usr/bin/env python3
"""Make Hugo's relative-URL output navigable when opened directly from a ZIP.

Run after a build with HUGO_RELATIVEURLS=true. This updates generated HTML only,
replacing local directory links with explicit index.html files, and checks that
all local href/src targets exist. Source content and production output are not
modified. No third-party packages are required.
"""

from __future__ import annotations

import argparse
from html import escape
from html.parser import HTMLParser
import os
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit


class PreviewHTML(HTMLParser):
    def __init__(self, root: Path, page: Path) -> None:
        super().__init__(convert_charrefs=False)
        self.root = root
        self.page = page
        self.parts: list[str] = []
        self.errors: list[str] = []
        self.changed = 0

    def local_url(self, value: str) -> str:
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return value
        path = unquote(parsed.path)
        target = (self.root / path.lstrip("/")) if path.startswith("/") else self.page.parent / path
        target = target.resolve()
        if not target.is_relative_to(self.root):
            self.errors.append(f"{self.page.relative_to(self.root)}: URL escapes preview: {value}")
            return value
        new_path = parsed.path
        if path.startswith("/"):
            new_path = os.path.relpath(target, self.page.parent).replace(os.sep, "/")
        if target.is_dir() and (target / "index.html").is_file():
            new_path = f"{new_path.rstrip('/')}/index.html"
            target = target / "index.html"
        if not target.is_file():
            self.errors.append(f"{self.page.relative_to(self.root)}: Missing preview target: {value}")
        if new_path != parsed.path:
            self.changed += 1
            return urlunsplit(("", "", new_path, parsed.query, parsed.fragment))
        return value

    def tag(self, tag: str, attrs: list[tuple[str, str | None]], closing: str) -> None:
        result = [f"<{tag}"]
        for name, value in attrs:
            if value is None:
                result.append(f" {name}")
            else:
                if name.lower() in {"href", "src"}:
                    value = self.local_url(value)
                result.append(f' {name}="{escape(value, quote=True)}"')
        result.append(closing)
        self.parts.append("".join(result))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tag(tag, attrs, ">")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tag(tag, attrs, " />")

    def handle_endtag(self, tag: str) -> None:
        self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.parts.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self.parts.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self.parts.append(f"<!{decl}>")

    def handle_pi(self, data: str) -> None:
        self.parts.append(f"<?{data}>")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Generated draft-preview directory")
    args = parser.parse_args()
    root = args.directory.resolve()
    if not (root / "index.html").is_file():
        parser.error("The generated preview directory must contain index.html.")
    rendered: list[tuple[Path, str]] = []
    errors: list[str] = []
    changed = 0
    for page in sorted(root.rglob("*.html")):
        html = PreviewHTML(root, page)
        html.feed(page.read_text(encoding="utf-8"))
        html.close()
        rendered.append((page, "".join(html.parts)))
        errors.extend(html.errors)
        changed += html.changed
    if errors:
        for message in errors:
            print(message)
        return 1
    for page, markup in rendered:
        page.write_text(markup, encoding="utf-8")
    print(f"Prepared {len(rendered)} preview pages and updated {changed} local navigation links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
