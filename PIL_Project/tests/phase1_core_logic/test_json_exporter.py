# tests/test_json_exporter.py
"""
Unit test for pil_meta.exporters.json_exporter.export_entity_graph.
Checks file output and verifies that the returned path exists.
@tags: ["test", "json_exporter", "unit"]
@status: "stable"
"""

from pathlib import Path
from pil_meta.exporters.json_exporter import export_entity_graph

def test_export_entity_graph_writes_files(tmp_path):
    """
    Test that export_entity_graph writes output and returns a valid file path.
    """
    graph = {
        "foo.bar": {
            "fqname": "foo.bar",
            "type": "function",
            "module": "foo",
            "tags": [],
            "metadata": {}
        }
    }
    out_dir = tmp_path / "exports"
    out_dir.mkdir()
    result = export_entity_graph(graph, str(out_dir), project_name="TestProj", timestamp="20990101_120000")

    # Accepts either a string path or a dict of paths
    if isinstance(result, dict):
        # Accept any value in the dict as a valid file path
        assert any(Path(path).exists() for path in result.values())
    else:
        # If just a string, it must exist as a file
        assert Path(result).exists()
