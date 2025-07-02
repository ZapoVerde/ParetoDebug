# tests/phase2_export_utilities/test_export_cleanup_utils.py
"""
Unit tests for pil_meta.utils.export_cleanup_utils.

Covers:
- Only removes intended .json exports and variable_usage.md
- Leaves markdown and snapshot files untouched
- Handles missing directory gracefully

@tags: ["test", "export_cleanup_utils", "unit"]
@status: "stable"
"""

from pathlib import Path
from pil_meta.utils.export_cleanup_utils import clean_exports_dir

def test_cleanup_removes_json_and_variable_usage(tmp_path):
    """
    Removes entity_graph*.json, function_map_exceptions*.json, usage_map*.json, and variable_usage.md.
    """
    export_dir = tmp_path / "exports"
    export_dir.mkdir()
    # Files to be deleted
    eg = export_dir / "entity_graph_test.json"
    fm = export_dir / "function_map_exceptions.json"
    um = export_dir / "usage_map_proj.json"
    vu = export_dir / "variable_usage.md"
    for f in [eg, fm, um, vu]:
        f.write_text("dummy", encoding="utf-8")
    # Files to remain
    md = export_dir / "readme.md"
    snap = export_dir / "project_snapshot.zip"
    md.write_text("markdown", encoding="utf-8")
    snap.write_bytes(b"zip")

    clean_exports_dir(str(export_dir))
    files = set(p.name for p in export_dir.iterdir())
    # .json and variable_usage.md gone
    assert "entity_graph_test.json" not in files
    assert "function_map_exceptions.json" not in files
    assert "usage_map_proj.json" not in files
    assert "variable_usage.md" not in files
    # Others remain
    assert "readme.md" in files
    assert "project_snapshot.zip" in files

def test_cleanup_handles_missing_dir(tmp_path):
    """
    No error when export directory does not exist.
    """
    non_existent = tmp_path / "missing_exports"
    # Should not raise or error
    clean_exports_dir(str(non_existent))
