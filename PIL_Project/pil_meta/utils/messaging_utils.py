# pil_meta/utils/messaging_utils.py
"""
Formatted reporting helpers for pipeline status, governance, and context.

@tags: ["utils", "messaging"]
@status: "stable"
"""

import os
import json
from pathlib import Path
from datetime import datetime

def set_debug(enabled: bool) -> None:
    os.environ["PIL_DEBUG"] = "1" if enabled else "0"

def debug(msg: str) -> None:
    if os.getenv("PIL_DEBUG") == "1":
        print(f"[DEBUG] {msg}")

def print_run_context(script: str, config: str, date: str) -> None:
    print("\n──────────────────────────────")
    print("🧠 PIL Pipeline Execution")
    print("──────────────────────────────")
    print(f"    [INFO] Script:            {script}")
    print(f"    [INFO] Config used:      {config}")
    print(f"    [INFO] Timestamp:        {date}")

def print_folder_tree_summary(lines: list) -> None:
    print("\n──────────────────────────────")
    print("📁 Folder Scan Summary")
    print("──────────────────────────────")
    for line in lines:
        print(f"    {line}")

def print_asset_scan_summary(exts: list, count: int) -> None:
    print("\n──────────────────────────────")
    print("🎨 Asset Scan Summary")
    print("──────────────────────────────")
    print(f"    [INFO] Asset extensions:  {', '.join(exts)}")
    print(f"    [INFO] Total assets:      {count}")

def print_symbol_extraction(code_count: int, asset_count: int, project: str) -> None:
    print("\n──────────────────────────────")
    print("🔍 Symbol Extraction")
    print("──────────────────────────────")
    print(f"    [INFO] Code symbols:      {code_count}")
    print(f"    [INFO] Asset symbols:     {asset_count}")
    print(f"    [INFO] Project name:      {project}")

def print_entity_graph(node_count: int, linkages_injected: bool = False) -> None:
    print("\n──────────────────────────────")
    print("📈 Entity Graph")
    print("──────────────────────────────")
    print(f"    [INFO] Nodes in graph:    {node_count}")
    print(f"    [INFO] Linkages applied:  {'Yes' if linkages_injected else 'No'}")

def print_exports(paths: dict) -> None:
    print("\n──────────────────────────────")
    print("📤 Exports Written")
    print("──────────────────────────────")
    if not paths:
        print("    [WARNING] No exports recorded.")
    else:
        for label, path in paths.items():
            label_fmt = label.replace("_", " ").capitalize()
            print(f"    [INFO] {label_fmt}:  {path}")

def print_governance_summary(missing: int, orphaned: int) -> None:
    print("\n[WARNING] Governance issues detected:")
    if missing:
        print(f"[WARNING]  - Missing docstrings: {missing}")
    if orphaned:
        print(f"[WARNING]  - Orphaned entities: {orphaned}")
    if missing or orphaned:
        print("[WARNING] Please ask the assistant to review governance exceptions if needed.")

def print_journal_entries_loaded(count: int) -> None:
    print("\n──────────────────────────────")
    print("📓 Journal/Design Documentation")
    print("──────────────────────────────")
    print(f"    [INFO] Journal entries loaded: {count}")

def print_pipeline_complete(file_count: int, snapshot_path: str) -> None:
    print("\n──────────────────────────────")
    print("✅ Pipeline complete")
    print("──────────────────────────────")
    print(f"    [INFO] Snapshot: {file_count} files → {snapshot_path}")
