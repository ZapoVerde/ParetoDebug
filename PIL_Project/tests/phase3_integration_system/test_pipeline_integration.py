# tests/test_pipeline_integration.py
"""
End-to-end test for running the full PIL pipeline against a sample project.
"""

import os
from pathlib import Path
import shutil
from pil_meta.pipeline import run_pipeline

def test_full_pipeline_happy_path(tmp_path):
    """Run the entire pipeline with real config and validate basic outputs."""
    output_dir = tmp_path / "exports"
    vault_dir = output_dir / "vault"
    snapshot_dir = tmp_path / "snapshots"
    config_path = tmp_path / "pilconfig.json"

    config = {
        "project_root": "./pil_meta",
        "scan_dirs": ["./pil_meta"],
        "journal_path": "./documents",
        "output_dir": str(output_dir),
        "docs_dir": "./docs",
        "vault_dir": str(vault_dir),
        "snapshot_dir": str(snapshot_dir),
        "config_self_path": str(config_path),
        "pil_module_path": ".",
        "asset_extensions": [".json"],
        "ignored_folders": ["__pycache__"],
        "enable_md_export": False  # Simulate export-disabled mode
    }

    with config_path.open("w", encoding="utf-8") as f:
        import json
        json.dump(config, f, indent=2)

    result = run_pipeline(str(config_path))

    # Minimal core checks
    assert result.entity_graph is not None
    assert result.graph_paths
    assert result.usage_paths
    assert Path(result.snapshot_path).exists()

    # Vault export assertions guarded by config
    if result.config.get("enable_md_export", False):
        assert Path(result.index_path).exists()
        assert any(str(f).endswith(".md") for f in vault_dir.rglob("*.md"))
    else:
        assert result.index_path == "[disabled]"
