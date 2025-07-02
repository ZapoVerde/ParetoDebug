# pil_meta/loaders/markdown_loader.py
"""
Markdown Loader (loaders)

Parses Markdown files for structured metadata entries.
Used to populate the documentation and vault systems.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional


def load_markdown_entries(md_path: str, ignored_folders: Optional[List[str]] = None) -> List[Dict]:
    """
    Loads markdown entries from a .md file unless it resides in an ignored folder.

    @tags: ["loader", "markdown", "ignore"]
    @status: "stable"
    @visibility: "public"
    """
    path = Path(md_path).resolve()
    if ignored_folders and any(folder in path.parts for folder in ignored_folders):
        return []

    # Placeholder for actual markdown parsing logic
    return [{"path": str(path), "type": "markdown"}]
