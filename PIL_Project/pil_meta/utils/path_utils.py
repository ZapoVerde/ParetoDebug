# pil_meta/utils/path_utils.py
"""
Path Utilities

Functions for resolving and normalizing paths across PIL modules.
"""

from pathlib import Path
from typing import Optional

def resolve_path(path: str, base: Optional[str] = None) -> str:
    """
    Resolve a given path (relative or absolute) to an absolute, normalized string.

    Args:
        path (str): File or directory path (can be relative)
        base (str, optional): Base directory to resolve from (if given)

    Returns:
        str: Absolute, normalized path
    """
    p = Path(path)
    if not p.is_absolute():
        if base is not None:
            p = Path(base) / p
        p = p.resolve()
    return str(p)
