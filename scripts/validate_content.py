#!/usr/bin/env python3
"""Validate the small content contract before a Hugo build.

Uses Python's standard library and Ruby's bundled safe YAML reader, avoiding an
extra Python package installation. Run from any directory; content is located
relative to this script. It does not alter source files or publish anything.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime
from urllib.parse import unquote, urlsplit
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
EASTERN = ZoneInfo("America/New_York")
ERRORS: list[str] = []


def error(path: Path, message: str) -> None:
    ERRORS.append(f"{path.relative_to(ROOT)}: {message}")


def parse_yaml_batch(items: list[dict[str, str]]) -> list[dict]:
    ruby = shutil.which("ruby")
    if not ruby:
        raise RuntimeError("Ruby is required for safe YAML validation. Install Ruby or use a runner that includes it.")
    program = """
require 'json'
require 'yaml'
require 'date'
items = JSON.parse(STDIN.read)
puts JSON.generate(items.map do |item|
  begin
    value = YAML.safe_load(item['yaml'], permitted_classes: [Date, Time], aliases: false)
    { 'path' => item['path'], 'data' => value }
  rescue StandardError => e
    { 'path' => item['path'], 'error' => e.message }
  end
end)
"""
    result = subprocess.run(
        [ruby, "-e", program], input=json.dumps(items), text=True,
        capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Safe YAML validation failed.")
    return json.loads(result.stdout)


def valid_embed(url: str) -> bool:
    try:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.username or parsed.password or parsed.port:
            return False
        if parsed.hostname == "datawrapper.dwcdn.net":
            return bool(re.fullmatch(r"/[A-Za-z0-9]+/(?:\d+/?)?", parsed.path))
        if parsed.hostname == "flo.uri.sh":
            return bool(re.fullmatch(r"/(?:visualisation|story)/\d+/embed/?", parsed.path))
        if parsed.hostname == "public.tableau.com":
            return bool(re.fullmatch(r"/(?:views|shared)/[^<>\s]+", parsed.path))
    except ValueError:
        return False
    return False


def resource_exists(reference: str, page: Path) -> bool:
    parsed = urlsplit(reference)
    if parsed.scheme:
        return parsed.scheme == "https" and bool(parsed.hostname)
    pathname = unquote(parsed.path)
    if ".." in Path(pathname).parts:
        return False
    if pathname.startswith("/uploads/"):
        candidates = [ROOT / "assets" / pathname.lstrip("/")]
    elif pathname.startswith("/"):
        candidates = [ROOT / "static" / pathname.lstrip("/")]
    else:
        candidates = [page.parent / pathname, ROOT / "assets" / pathname, ROOT / "static" / pathname]
    return any(p.is_file() for p in candidates)


def validate_time(path: Path, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        error(path, f"{field} must be an ISO publication date/time.")
        return
    try:
        # Ruby renders explicit YAML times with spaces; ISO strings from CMS
        # retain T. Both represent the same parseable date/time.
        instant = datetime.fromisoformat(value.replace(" UTC", "+00:00").replace("Z", "+00:00"))
        if instant.tzinfo is None:
            instant = instant.replace(tzinfo=EASTERN)
        # Round-trip catches local times skipped by spring DST transitions.
        round_trip = instant.astimezone(ZoneInfo("UTC")).astimezone(EASTERN)
        if instant.tzinfo == EASTERN and round_trip.replace(tzinfo=None) != instant.replace(tzinfo=None):
            error(path, f"{field} is a skipped Eastern daylight-saving time. Choose a valid local time.")
    except (ValueError, TypeError):
        error(path, f"{field} must be an ISO date/time, such as 2026-11-02T09:00:00.")


def main() -> int:
    documents: list[dict[str, str]] = []
    bodies: dict[str, str] = {}
    for path in sorted((ROOT / "content").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", text, flags=re.S)
        if not match:
            error(path, "expected YAML metadata between --- delimiters.")
            continue
        relative = str(path.relative_to(ROOT))
        documents.append({"path": relative, "yaml": match.group(1)})
        bodies[relative] = match.group(2)
    config_path = ROOT / ".pages.yml"
    documents.append({"path": ".pages.yml", "yaml": config_path.read_text(encoding="utf-8")})
    try:
        parsed = parse_yaml_batch(documents)
    except RuntimeError as exc:
        print(f"Content validation failed: {exc}", file=sys.stderr)
        return 1
    slugs: dict[str, Path] = {}
    count = 0
    for item in parsed:
        path = ROOT / item["path"]
        if "error" in item:
            error(path, f"invalid YAML: {item['error']}")
            continue
        data = item["data"]
        if not isinstance(data, dict):
            error(path, "metadata must be a mapping.")
            continue
        if path == config_path:
            for key in ("media", "content"):
                if not isinstance(data.get(key), list) or not data[key]:
                    error(path, f"CMS {key} must be a nonempty list.")
            continue
        count += 1
        if not isinstance(data.get("title"), str) or not data["title"].strip():
            error(path, "title is required.")
        if "draft" in data and not isinstance(data["draft"], bool):
            error(path, "draft must be true or false, without quotes.")
        params = data.get("params") or {}
        if not isinstance(params, dict):
            error(path, "params must be a mapping.")
            continue
        is_article = path.is_relative_to(ROOT / "content" / "blog") and path.name != "_index.md"
        if is_article:
            if not isinstance(data.get("draft"), bool):
                error(path, "journal articles require an explicit draft true/false value.")
            validate_time(path, "publishDate", data.get("publishDate"))
            relative = path.relative_to(ROOT / "content" / "blog")
            slug = str(relative.parent if path.name == "index.md" else relative.with_suffix(""))
            if slug in slugs:
                error(path, f"duplicates the article address used by {slugs[slug].relative_to(ROOT)}.")
            slugs[slug] = path
        elif "publishDate" in data:
            validate_time(path, "publishDate", data["publishDate"])
        cover = params.get("cover")
        if cover:
            if not isinstance(cover, str) or not resource_exists(cover, path):
                error(path, "cover image does not exist or has an unsupported URL.")
            if not params.get("cover_alt"):
                error(path, "cover_alt is required when a cover image is supplied.")
        downloads = params.get("downloads") or []
        if not isinstance(downloads, list):
            error(path, "params.downloads must be a list.")
        else:
            for download in downloads:
                if not isinstance(download, dict) or not download.get("title") or not download.get("file"):
                    error(path, "each download needs a title and file.")
                elif not isinstance(download["file"], str) or not resource_exists(download["file"], path):
                    error(path, f"download does not exist: {download.get('file')}")
        embeds = params.get("embeds") or []
        if not isinstance(embeds, list):
            error(path, "params.embeds must be a list.")
        else:
            for embed in embeds:
                if not isinstance(embed, dict) or not embed.get("title"):
                    error(path, "each embed needs a title and supported URL.")
                elif not isinstance(embed.get("url"), str) or not valid_embed(embed["url"]):
                    error(path, f"unsupported embed URL: {embed.get('url')}")
        # Syntax demonstrations inside fenced or inline code are not rendered
        # images and must not be treated as missing article resources.
        rendered_body = re.sub(
            r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*\n?", "", bodies[item["path"]]
        )
        rendered_body = re.sub(r"`+[^`]*`+", "", rendered_body)
        for alt, reference in re.findall(r"!\[([^\]]*)\]\(([^\s)]+)(?:\s+[^)]*)?\)", rendered_body):
            if not alt.strip():
                error(path, "article images need descriptive alternative text.")
            if not resource_exists(reference, path):
                error(path, f"article image does not exist: {reference}")
    if ERRORS:
        print("Content validation failed:", file=sys.stderr)
        for message in ERRORS:
            print(f"- {message}", file=sys.stderr)
        return 1
    print(f"Validated {count} content pages and the browser editor configuration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
