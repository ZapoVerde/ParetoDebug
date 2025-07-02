# pil_meta/utils/export_cleanup_utils.py
"""
Cleans the exports directory before writing new output files.

Removes:
- entity graph JSONs
- function map exceptions
- usage maps
- variable usage reports

Leaves:
- Markdown vault content (assumed to be overwritten cleanly)
- Snapshots (handled separately)
"""

from pathlib import Path


def clean_exports_dir(export_dir: str) -> None:
    """
    Removes stale JSON exports before writing new ones.

    @tags: ["cleanup", "exports"]
    @status: "stable"
    @visibility: "internal"

    Args:
        export_dir (str): Path to the exports/ directory
    """
    export_path = Path(export_dir)
    if not export_path.exists():
        return

    for file in export_path.iterdir():
        if file.suffix != ".json" and file.name != "variable_usage.md":
            continue
        if file.name.startswith("entity_graph") or \
           file.name.startswith("function_map_exceptions") or \
           file.name.startswith("usage_map") or \
           file.name == "variable_usage.md":
            try:
                file.unlink()
            except Exception as e:
                print(f"⚠️ Could not delete {file}: {e}")
