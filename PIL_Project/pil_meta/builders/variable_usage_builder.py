# variable_usage_builder.py
"""
Variable Usage Map Builder (builders)

Finds all variables (top-level assignments) used in more than one module,
and records which modules use them.
"""

from pathlib import Path
import re

def build_variable_usage_map(variables: list, all_source_files: list, root_path: Path) -> dict:
    """
    For each variable, scan all other modules for references by name.

    Parameters:
        variables (list): List of variable nodes (from loader, type=='variable')
        all_source_files (list): List of all source Path objects
        root_path (Path): Project root for relative paths

    Returns:
        dict: fqname -> list of modules (relative paths) where used
    """
    usage_map = {}
    for var in variables:
        name = var["function"]
        defining_file = var["source_file"]
        fqname = var["fqname"]
        used_in = set()

        pattern = re.compile(rf"\b{name}\b")

        for srcfile in all_source_files:
            relfile = str(srcfile.relative_to(root_path))
            if relfile == defining_file:
                continue
            try:
                code = srcfile.read_text(encoding="utf-8")
                if pattern.search(code):
                    used_in.add(relfile)
            except Exception:
                continue

        if used_in:
            usage_map[fqname] = sorted(used_in)
    return usage_map
