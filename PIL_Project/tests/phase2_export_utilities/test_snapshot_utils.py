# tests/phase2_export_utilities/test_snapshot_utils.py
"""
Unit tests for pil_meta.utils.snapshot_utils.

Covers:
- Creation of project snapshot as a zip
- Ignores configured folders
- Optionally attaches entity graph file

@tags: ["test", "snapshot_utils", "unit"]
@status: "stable"
"""

import os
import zipfile
from pathlib import Path
from pil_meta.utils.snapshot_utils import take_project_snapshot

def test_snapshot_includes_project_files(tmp_path):
    """
    Snapshot includes all files from project_root except ignored folders.
    """
    # Setup fake project structure
    root = tmp_path / "proj"
    root.mkdir()
    (root / "main.py").write_text("print('hi')", encoding="utf-8")
    (root / "__pycache__").mkdir()
    (root / ".git").mkdir()
    (root / "data").mkdir()
    (root / "data" / "notes.txt").write_text("hello", encoding="utf-8")
    config = {
        "project_root": str(root),
        "snapshot_dir": str(tmp_path / "snapshots")
    }

    zip_path = take_project_snapshot(config)
    assert Path(zip_path).exists()
    # Open zip and check only main.py and data/notes.txt are present
    with zipfile.ZipFile(zip_path, "r") as z:
        files = set(z.namelist())
        assert "main.py" in files
        assert "data/notes.txt" in files
        # Ignored folders should not appear
        assert not any("pycache" in f or ".git" in f for f in files)

def test_snapshot_attaches_entity_graph(tmp_path):
    """
    Entity graph file is attached in the zip with correct naming.
    """
    root = tmp_path / "proj"
    root.mkdir()
    (root / "foo.py").write_text("x=1", encoding="utf-8")
    graph = tmp_path / "entity_graph.json"
    graph.write_text("{\"test\":true}", encoding="utf-8")
    config = {
        "project_root": str(root),
        "snapshot_dir": str(tmp_path / "snaps")
    }
    zip_path = take_project_snapshot(config, entity_graph_path=str(graph))
    with zipfile.ZipFile(zip_path, "r") as z:
        files = set(z.namelist())
        # At least one file in the zip should match entity_graph_*.json
        assert any(f.startswith("entity_graph_") and f.endswith(".json") for f in files)
