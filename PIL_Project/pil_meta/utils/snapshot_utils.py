# pil_meta/utils/snapshot_utils.py
"""
Utility to create a zip snapshot of the full project for archival or traceability.

This should be called from within pipeline.py using:
    from pil_meta.utils.snapshot_utils import take_project_snapshot

@tags: ["utility", "snapshot", "archive"]
@status: "stable"
@visibility: "public"
"""

import zipfile
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

IGNORED_FOLDERS = {
    ".git", "__pycache__", "node_modules", "snapshots", "exports",
    ".mypy_cache", ".venv", "env", ".idea"
}

def take_project_snapshot(
    config: dict,
    entity_graph_path: Optional[str] = None
) -> Path:
    """Creates a compressed zip snapshot of the entire project_root.
    Optionally attaches entity_graph.json for traceability and audit.

    Args:
        config (dict): Loaded pilconfig for current run.
        entity_graph_path (str, optional): Path to entity graph export, if available.

    Returns:
        Path: Full path to the created snapshot zip.
    @tags: ["snapshot", "archive"]
    @status: "stable"
    """
    project_root = Path(config["project_root"]).resolve()
    snapshot_dir = Path(config["snapshot_dir"]).resolve()
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_file = snapshot_dir / f"project_snapshot_{timestamp}.zip"

    with zipfile.ZipFile(snapshot_file, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        for foldername, _, filenames in os.walk(project_root):
            rel_folder = Path(foldername).relative_to(project_root)
            if any(part in IGNORED_FOLDERS for part in rel_folder.parts):
                continue

            for filename in filenames:
                file_path = Path(foldername) / filename
                rel_path = file_path.relative_to(project_root)
                zipf.write(file_path, arcname=str(rel_path))

        if entity_graph_path:
            graph_file = Path(entity_graph_path)
            if graph_file.exists():
                arcname = f"entity_graph_{timestamp}.json"
                zipf.write(graph_file, arcname=arcname)

    return snapshot_file
