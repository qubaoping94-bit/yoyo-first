#!/usr/bin/env python3
"""Create a safe JSON inventory of a local AI skill folder."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit


TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".py", ".js", ".ts", ".tsx", ".ps1", ".sh"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}
SENSITIVE_PARTS = {".env", "secret", "token", "credential", "cookie", "private-key", "private_key", "id_rsa", "apikey", "api-key"}
URL_RE = re.compile(r"https?://[^\s<>()\]\[\"']+")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
MAX_FILE_BYTES = 2_000_000


def is_sensitive(path: Path) -> bool:
    lowered = "/".join(path.parts).lower()
    return any(part in lowered for part in SENSITIVE_PARTS)


def safe_url(raw: str) -> str:
    raw = raw.rstrip(".,;:!?")
    parts = urlsplit(raw)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def read_text(path: Path) -> str | None:
    if path.suffix.lower() not in TEXT_SUFFIXES or is_sensitive(path):
        return None
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        if key.strip() in {"name", "description"}:
            result[key.strip()] = value.strip().strip("\"'")
    return result


def inventory(root: Path) -> dict[str, Any]:
    root = root.resolve()
    skill_md = root / "SKILL.md"
    if not root.is_dir() or not skill_md.is_file():
        raise ValueError(f"Target must be a skill folder containing SKILL.md: {root}")

    files: list[dict[str, Any]] = []
    urls: set[str] = set()
    skill_text = skill_md.read_text(encoding="utf-8")

    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        relative = path.relative_to(root)
        if is_sensitive(relative):
            continue
        info: dict[str, Any] = {"path": relative.as_posix(), "bytes": path.stat().st_size}
        text = read_text(path)
        if text is not None:
            info["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
            headings = [match.group(2).strip() for match in HEADING_RE.finditer(text)]
            if headings:
                info["headings"] = headings[:40]
            for match in URL_RE.finditer(text):
                urls.add(safe_url(match.group(0)))
        files.append(info)

    return {
        "target": str(root),
        "frontmatter": parse_frontmatter(skill_text),
        "skill_md_bytes": skill_md.stat().st_size,
        "files": files,
        "public_url_candidates": sorted(urls),
        "notes": [
            "Query strings and fragments are removed from URLs to avoid leaking credentials.",
            "Sensitive-looking files and common generated directories are skipped.",
            "Inventory data must be verified by reading canonical source files.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Skill folder containing SKILL.md")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    try:
        result = inventory(args.target)
    except (ValueError, OSError, UnicodeDecodeError) as exc:
        parser.error(str(exc))

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
