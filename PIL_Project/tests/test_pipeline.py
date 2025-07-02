# tests/test_pipeline.py
"""
Unit and edge tests for pil_meta.pipeline, in addition to the integration smoke test.
"""

import pytest
from pil_meta.pipeline import PipelineResult, print_full_report, run_pipeline

def test_pipelineresult_attributes():
    """PipelineResult attributes are set to expected default types/values."""
    result = PipelineResult()
    assert isinstance(result.context, dict)
    assert isinstance(result.folder_tree, dict)
    assert isinstance(result.scan_roots, list)
    assert isinstance(result.all_seen_folders, set)
    assert isinstance(result.asset_counts, dict)
    assert result.entity_graph is None

def test_print_full_report_mocked(monkeypatch):
    """print_full_report can run with a fully stubbed PipelineResult."""
    result = PipelineResult()
    # Set required fields to minimal valid values
    result.folder_tree = {"root": {"children": [], "num_py": 1, "assets": {}, "ignored": False, "skipped": False}}
    result.scan_roots = ["root"]
    result.asset_exts = [".py"]
    result.asset_files = ["file.py"]
    result.code_symbols = [{}]
    result.asset_symbols = [{}]
    result.project_name = "TestProj"
    result.entity_graph = {"foo": {}}
    result.combined_paths = {}

    # Mark vault export as disabled
    result.vault_files = []
    result.index_path = "[disabled]"

    result.journal_entries = []
    result.missing_docstrings = 0
    result.orphaned = 0
    result.snapshot_file_count = 1
    result.snapshot_path = "snap.zip"
    # Monkeypatch print functions
    monkeypatch.setattr("pil_meta.pipeline.print_run_context", lambda **kwargs: None)
    monkeypatch.setattr("pil_meta.pipeline.print_folder_tree_summary", lambda *args: None)
    monkeypatch.setattr("pil_meta.pipeline.print_asset_scan_summary", lambda *a, **k: None)
    monkeypatch.setattr("pil_meta.pipeline.print_symbol_extraction", lambda *a, **k: None)
    monkeypatch.setattr("pil_meta.pipeline.print_entity_graph", lambda *a, **k: None)
    monkeypatch.setattr("pil_meta.pipeline.print_exports", lambda *a, **k: None)
    monkeypatch.setattr("pil_meta.pipeline.print_governance_summary", lambda *a, **k: None)
    monkeypatch.setattr("pil_meta.pipeline.print_journal_entries_loaded", lambda *a, **k: None)
    monkeypatch.setattr("pil_meta.pipeline.print_pipeline_complete", lambda *a, **k: None)
    # Should run with no exceptions
    print_full_report(result)

def test_run_pipeline_missing_config(monkeypatch):
    """run_pipeline exits with code 1 on missing config."""
    monkeypatch.setattr(
        "pil_meta.loaders.config_loader.load_config",
        lambda path: (_ for _ in ()).throw(FileNotFoundError("not found"))
    )
    with pytest.raises(SystemExit) as excinfo:
        run_pipeline("fake_config.json")
    assert excinfo.value.code == 1
