#!/usr/bin/env python3

"""
Generate a static JSON search index for the safesploitOrg/docs GitHub Pages site.

This script scans Markdown files in the repository and outputs:

    public/search-index.json

The generated index is consumed by:

    public/assets/js/search.js

Design goals:
- Works in GitHub Actions
- No external Python dependencies
- Skips hidden/system/vendor/build folders
- Avoids indexing ./public itself
- Produces browser-friendly JSON
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List


# =============================================================================
# GLOBAL VARS
# =============================================================================

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = REPO_ROOT / "public"
OUTPUT_FILE = PUBLIC_DIR / "search-index.json"

MARKDOWN_EXTENSIONS = {".md", ".markdown"}

EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".vscode",
    ".idea",
    "__pycache__",
    "node_modules",
    "vendor",
    "public",
    "dist",
    "build",
    ".venv",
    "venv",
}

EXCLUDED_FILES = {
    "LICENSE",
}

MAX_CONTENT_CHARS = 12000

DEFAULT_TAGS_BY_PATH = {
    "dns": ["DNS"],
    "bind": ["BIND", "DNS"],
    "dnsmasq": ["dnsmasq", "DNS"],
    "redcap": ["REDCap"],
    "linux": ["Linux"],
    "rhel": ["RHEL", "Linux"],
    "ansible": ["Ansible", "Automation"],
    "terraform": ["Terraform", "IaC"],
    "github": ["GitHub"],
    "gitops": ["GitOps"],
    "ci": ["CI/CD"],
    "cicd": ["CI/CD"],
    "security": ["Security"],
    "hardening": ["Hardening", "Security"],
    "netapp": ["NetApp", "ONTAP", "Storage"],
    "ontap": ["ONTAP", "NetApp"],
    "storage": ["Storage"],
    "proxmox": ["Proxmox", "Virtualisation"],
    "ceph": ["Ceph", "Storage"],
    "network": ["Networking"],
    "runbook": ["Runbook"],
    "architecture": ["Architecture"],
    "compliance": ["Compliance"],
}


# =============================================================================
# TEXT HELPERS
# =============================================================================

def normalise_whitespace(value: str) -> str:
    """Collapse repeated whitespace into single spaces."""
    return re.sub(r"\s+", " ", value).strip()


def strip_markdown(value: str) -> str:
    """Make Markdown content more search/snippet friendly."""
    text = value

    # Remove fenced code block markers but keep code contents searchable.
    text = re.sub(r"```[a-zA-Z0-9_-]*", " ", text)
    text = text.replace("```", " ")

    # Remove inline code backticks but keep content.
    text = text.replace("`", "")

    # Remove Markdown links while preserving readable text and URL signal.
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 \2", text)

    # Remove image syntax while preserving alt text.
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)

    # Remove common Markdown formatting characters.
    text = re.sub(r"[*_~>#|]", " ", text)

    # Remove HTML tags.
    text = re.sub(r"<[^>]+>", " ", text)

    return normalise_whitespace(text)


def extract_title(markdown_text: str, fallback: str) -> str:
    """Extract the first H1/H2-style heading, otherwise use filename stem."""
    for line in markdown_text.splitlines():
        clean_line = line.strip()

        if clean_line.startswith("#"):
            title = clean_line.lstrip("#").strip()
            if title:
                return title

    return fallback.replace("-", " ").replace("_", " ").title()


def extract_headings(markdown_text: str) -> List[str]:
    """Extract Markdown headings for extra searchable context."""
    headings: List[str] = []

    for line in markdown_text.splitlines():
        clean_line = line.strip()

        if clean_line.startswith("#"):
            heading = clean_line.lstrip("#").strip()
            if heading:
                headings.append(heading)

    return headings


def slugify(value: str) -> str:
    """Create a simple slug for fallback URLs."""
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "document"


# =============================================================================
# INDEX HELPERS
# =============================================================================

def should_exclude_path(path: Path) -> bool:
    """Return True if the file should not be indexed."""
    relative_parts = path.relative_to(REPO_ROOT).parts

    for part in relative_parts:
        if part in EXCLUDED_DIRS:
            return True

        if part.startswith(".") and part not in {".well-known"}:
            return True

    if path.name in EXCLUDED_FILES:
        return True

    if path.suffix.lower() not in MARKDOWN_EXTENSIONS:
        return True

    return False


def infer_tags(relative_path: Path, title: str, content: str) -> List[str]:
    """Infer lightweight tags from path, title and content."""
    discovered_tags: List[str] = []

    searchable = " ".join(
        [
            str(relative_path).lower(),
            title.lower(),
            content[:3000].lower(),
        ]
    )

    for keyword, tags in DEFAULT_TAGS_BY_PATH.items():
        if keyword in searchable:
            for tag in tags:
                if tag not in discovered_tags:
                    discovered_tags.append(tag)

    return discovered_tags[:8]


def build_github_url(relative_path: Path) -> str:
    """
    Link result cards back to the source file in GitHub.

    This avoids needing to convert every Markdown file into an HTML page.
    """
    path_posix = relative_path.as_posix()
    return f"https://github.com/safesploitOrg/docs/blob/main/{path_posix}"


def build_index_item(path: Path) -> Dict[str, object]:
    """Build a single search-index item from a Markdown file."""
    relative_path = path.relative_to(REPO_ROOT)

    markdown_text = path.read_text(encoding="utf-8", errors="replace")
    title = extract_title(markdown_text, path.stem)

    headings = extract_headings(markdown_text)
    stripped_content = strip_markdown(markdown_text)

    if len(stripped_content) > MAX_CONTENT_CHARS:
        stripped_content = stripped_content[:MAX_CONTENT_CHARS].rstrip() + "..."

    tags = infer_tags(relative_path, title, stripped_content)

    content_parts = [
        title,
        " ".join(headings),
        stripped_content,
    ]

    return {
        "title": title,
        "path": relative_path.as_posix(),
        "url": build_github_url(relative_path),
        "tags": tags,
        "content": normalise_whitespace(" ".join(content_parts)),
    }


def discover_markdown_files() -> List[Path]:
    """Find all indexable Markdown files under the repository root."""
    markdown_files: List[Path] = []

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue

        if should_exclude_path(path):
            continue

        markdown_files.append(path)

    return sorted(markdown_files, key=lambda item: item.relative_to(REPO_ROOT).as_posix())


def write_search_index(index_items: List[Dict[str, object]]) -> None:
    """Write the search index JSON to ./public/search-index.json."""
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(index_items, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    markdown_files = discover_markdown_files()

    index_items = []

    for markdown_file in markdown_files:
        try:
            index_items.append(build_index_item(markdown_file))
        except Exception as error:
            relative_path = markdown_file.relative_to(REPO_ROOT)
            print(f"WARNING: Failed to index {relative_path}: {error}")

    write_search_index(index_items)

    print(f"Indexed {len(index_items)} Markdown files")
    print(f"Wrote {OUTPUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
