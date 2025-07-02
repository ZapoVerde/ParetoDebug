# tests/test_roundtrip.py

import os
import json
import shutil
from filecmp import dircmp
from pil_meta.exporters.markdown_vault_exporter import export_markdown_vault

INPUT_JSON = os.path.join(os.path.dirname(__file__), "sample_graph_edge_cases.json")

DIR1 = os.path.join(os.path.dirname(__file__), "export_roundtrip_1")
DIR2 = os.path.join(os.path.dirname(__file__), "export_roundtrip_2")

def setup_module():
    for d in (DIR1, DIR2):
        if os.path.exists(d):
            shutil.rmtree(d)

def test_exporter_is_idempotent():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        sample_graph = json.load(f)
    export_markdown_vault(sample_graph, DIR1)
    export_markdown_vault(sample_graph, DIR2)
    dcmp = dircmp(DIR1, DIR2)
    assert not dcmp.left_only and not dcmp.right_only, "Mismatch in output directories"
    # Optionally compare file contents for full fidelity
    for folder in dcmp.common_dirs:
        subcmp = dircmp(os.path.join(DIR1, folder), os.path.join(DIR2, folder))
        assert not subcmp.left_only and not subcmp.right_only, f"Mismatch in subfolder {folder}"
