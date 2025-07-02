# tests/phase2/test_usage_map_exporter.py
"""
Unit tests for pil_meta.exporters.usage_map_exporter.export_usage_map.

Covers:
- File creation and structure
- Edge cases: empty usage map, missing output directory
- JSON content and metadata validation

@tags: ["test", "usage_map_exporter", "unit"]
@status: "stable"
"""

from pathlib import Path
import json
from pil_meta.exporters.usage_map_exporter import export_usage_map

def test_export_usage_map_writes_timestamped_file(tmp_path):
    """
    Test normal usage map export: file created, correct path and metadata.
    """
    usage_map = {
        "foo.bar": {"used_by": [], "uses": ["foo.baz"]},
        "foo.baz": {"used_by": ["foo.bar"], "uses": []}
    }
    out_dir = tmp_path / "exports"
    result = export_usage_map(usage_map, out_dir, project_name="TestProj", timestamp="20990101_120000")
    assert "timestamped" in result
    ts_path = Path(result["timestamped"])
    assert ts_path.exists()
    with open(ts_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    assert content["project_name"] == "TestProj"
    assert "usage_map" in content
    assert "foo.bar" in content["usage_map"]

def test_export_empty_usage_map_creates_valid_file(tmp_path):
    """
    Exporting an empty usage map creates a valid JSON file with metadata.
    """
    out_dir = tmp_path / "empty"
    result = export_usage_map({}, out_dir, project_name="EmptyTest", timestamp="20990101_120000")
    ts_path = Path(result["timestamped"])
    assert ts_path.exists()
    with open(ts_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["project_name"] == "EmptyTest"
    assert data["usage_map"] == {}

def test_export_usage_map_creates_parent_dirs(tmp_path):
    """
    Output directory should be created automatically if it does not exist.
    """
    deep_dir = tmp_path / "deep" / "structure"
    assert not deep_dir.exists()
    export_usage_map({}, deep_dir, project_name="TestProj", timestamp="20990101_120000")
    assert deep_dir.exists()
