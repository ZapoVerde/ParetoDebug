# pil_meta/pipeline.py
"""
Orchestrates the full PIL metadata pipeline with structured reporting.
Focuses on core exports and clean governance summary.

@tags: ["pipeline", "orchestration", "reporting"]
@status: "stable"
"""

import sys
import traceback
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional
from collections import defaultdict
from zipfile import ZipFile

from pil_meta.loaders.config_loader import load_config
from pil_meta.loaders.asset_loader import load_asset_symbols
from pil_meta.loaders.code_loader import load_code_symbols
from pil_meta.loaders.markdown_loader import load_markdown_entries

from pil_meta.builders.entity_graph_builder import build_entity_graph
from pil_meta.builders.linkage_builder import inject_call_links
from pil_meta.builders.usage_map_builder import build_usage_map

from pil_meta.exporters.json_exporter import export_entity_graph
from pil_meta.exporters.usage_map_exporter import export_usage_map

from pil_meta.utils.snapshot_utils import take_project_snapshot
from pil_meta.utils.export_cleanup_utils import clean_exports_dir

from pil_meta.utils.messaging_utils import (
    set_debug,
    print_run_context,
    print_folder_tree_summary,
    print_asset_scan_summary,
    print_symbol_extraction,
    print_entity_graph,
    print_exports,
    print_governance_summary,
    print_journal_entries_loaded,
    print_pipeline_complete,
    debug,
)

class PipelineResult:
    """Container for all results and statistics from a full PIL pipeline run.

    @tags: ["container", "result"]
    @status: "stable"
    @visibility: "internal"
    """
    context: Dict
    folder_tree: Dict
    scan_roots: List[str]
    all_seen_folders: Set[str]
    py_files: List[str]
    asset_files: List[str]
    file_roots: List[str]
    asset_exts: List[str]
    asset_counts: Dict[str, int]
    entity_graph: Optional[Dict]
    graph_paths: Optional[Dict]
    usage_paths: Optional[Dict]
    combined_paths: Optional[Dict]
    project_name: str
    timestamp: str
    config: Dict
    asset_symbols: List
    code_symbols: List
    missing_docstrings: int
    orphaned: int
    snapshot_path: str
    snapshot_file_count: int

    def __init__(self):
        self.context = {}
        self.folder_tree = {}
        self.scan_roots = []
        self.all_seen_folders = set()
        self.py_files = []
        self.asset_files = []
        self.file_roots = []
        self.asset_exts = []
        self.asset_counts = defaultdict(int)
        self.entity_graph = None
        self.graph_paths = None
        self.usage_paths = None
        self.combined_paths = None
        self.project_name = ""
        self.timestamp = ""
        self.config = {}
        self.asset_symbols = []
        self.code_symbols = []
        self.missing_docstrings = 0
        self.orphaned = 0
        self.snapshot_path = ""
        self.snapshot_file_count = 0

def run_pipeline(config_path: str = "pilconfig.json") -> PipelineResult:
    """Orchestrates the PIL metadata pipeline (scan + process + reporting).

    Reads config, scans for symbols and assets, applies linkages, and exports structured outputs.

    @tags: ["entrypoint", "scan", "export"]
    @status: "stable"
    @visibility: "public"]

    Args:
        config_path (str): Path to the config JSON used to drive the pipeline.

    Returns:
        PipelineResult: Captures all exports, stats, paths, and entity graph output.
    """
    result = PipelineResult()
    try:
        set_debug(False)

        config = load_config(config_path)
        project_name = Path(config["project_root"]).resolve().name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        result.context = {
            "script": os.path.basename(sys.argv[0]),
            "config": config_path,
            "date": timestamp,
        }
        result.project_name = project_name
        result.timestamp = timestamp
        result.config = config

        scan_roots = [str(Path(d).resolve()) for d in config.get("scan_dirs", [config["project_root"]])]
        result.scan_roots = scan_roots
        asset_exts = config.get("asset_extensions", [])
        ignored_folders = set(config.get("ignored_folders", []))

        result.asset_exts = asset_exts
        all_seen_folders = set()
        py_files = []
        file_roots = []
        folder_tree = {}

        def get_parent_dir(path: str) -> str:
            return str(Path(path).parent)

        for scan_root in scan_roots:
            scan_path = Path(scan_root)
            if not scan_path.exists():
                folder_tree[scan_root] = {
                    "parent": None,
                    "children": [],
                    "num_py": 0,
                    "assets": defaultdict(int),
                    "ignored": False,
                    "skipped": True,
                }
                continue
            for folder, subdirs, files in os.walk(scan_path):
                folder_path = str(Path(folder).resolve())
                if folder_path in all_seen_folders:
                    continue
                all_seen_folders.add(folder_path)

                rel_parts = Path(folder).relative_to(scan_path).parts
                if any(part in ignored_folders for part in rel_parts):
                    folder_tree[folder_path] = {
                        "parent": get_parent_dir(folder_path),
                        "children": [],
                        "num_py": 0,
                        "assets": defaultdict(int),
                        "ignored": True,
                        "skipped": False,
                    }
                    subdirs[:] = []
                    continue

                parent = get_parent_dir(folder_path)
                if folder_path not in folder_tree:
                    folder_tree[folder_path] = {
                        "parent": parent if folder_path != scan_root else None,
                        "children": [],
                        "num_py": 0,
                        "assets": defaultdict(int),
                        "ignored": False,
                        "skipped": False,
                    }

                py_count = 0
                asset_count = defaultdict(int)
                for f in files:
                    ext = Path(f).suffix
                    full_path = str(Path(folder_path) / f)
                    if f.endswith(".py"):
                        py_count += 1
                        py_files.append(full_path)
                        file_roots.append(str(scan_path))
                    elif ext in asset_exts:
                        asset_count[ext] += 1
                        result.asset_counts[ext] += 1
                        result.asset_files.append(full_path)
                folder_tree[folder_path]["num_py"] += py_count
                for ext, ct in asset_count.items():
                    folder_tree[folder_path]["assets"][ext] += ct
                if parent and parent in folder_tree:
                    if folder_path not in folder_tree[parent]["children"]:
                        folder_tree[parent]["children"].append(folder_path)

        result.folder_tree = folder_tree
        result.all_seen_folders = all_seen_folders
        result.py_files = py_files
        result.file_roots = file_roots

        code_symbols = []
        for pyfile, file_root in zip(py_files, file_roots):
            code_symbols.extend(load_code_symbols(pyfile, file_root))
        result.code_symbols = code_symbols

        asset_symbols = load_asset_symbols(config)
        result.asset_symbols = asset_symbols

        entities = code_symbols + asset_symbols
        entity_graph = build_entity_graph(entities)
        entity_graph = inject_call_links(entity_graph, str(config["project_root"]))
        result.entity_graph = entity_graph

        clean_exports_dir(config["output_dir"])
        graph_paths = export_entity_graph(entity_graph, config["output_dir"], project_name, timestamp)
        usage_paths = export_usage_map(build_usage_map(entity_graph), config["output_dir"], project_name, timestamp)

        result.graph_paths = graph_paths
        result.usage_paths = usage_paths
        result.combined_paths = {**graph_paths, **usage_paths} if graph_paths and usage_paths else {}

        #result.journal_entries = load_markdown_entries(config["journal_path"])
        result.missing_docstrings = sum(1 for n in entity_graph.values() if not n.get("docstring_present"))
        result.orphaned = sum(1 for n in entity_graph.values() if n.get("is_orphaned"))

        entity_graph_path = result.graph_paths.get("timestamped") if result.graph_paths else None
        result.snapshot_path = str(take_project_snapshot(config, entity_graph_path=entity_graph_path))
        try:
            with ZipFile(result.snapshot_path, 'r') as zipf:
                result.snapshot_file_count = len(zipf.infolist())
        except Exception:
            result.snapshot_file_count = 0

        print_run_context(**result.context)
        print_folder_tree_summary(build_tree_lines(result.folder_tree, result.scan_roots))
        print_asset_scan_summary(result.asset_exts, len(result.asset_files))
        print_symbol_extraction(len(result.code_symbols), len(result.asset_symbols), result.project_name)
        print_entity_graph(len(result.entity_graph or {}), linkages_injected=True)
        print_exports(result.combined_paths or {})
        print_governance_summary(result.missing_docstrings, result.orphaned)
        #print_journal_entries_loaded(len(result.journal_entries))
        print_pipeline_complete(result.snapshot_file_count, result.snapshot_path)

        return result

    except Exception:
        traceback.print_exc()
        sys.exit(1)


def build_tree_lines(tree: dict, roots: list, depth: int = 0) -> list:
    """Builds indented string lines from a folder tree dictionary for printing.

    @tags: ["reporting", "tree"]
    @status: "stable"]
    @visibility: "internal"]

    Args:
        tree (dict): Nested folder structure.
        roots (list): Root-level folders to print.
        depth (int): Indentation level (used for recursion).

    Returns:
        list[str]: Formatted indented lines.
    """
    lines = []
    indent = "    " * depth
    for root in roots:
        if root not in tree:
            continue
        node = tree[root]
        line = indent + Path(root).name + "/"
        if node.get("skipped"):
            line += " [SKIPPED]"
        elif node.get("ignored"):
            line += " [IGNORED]"
        else:
            assets_summary = ", ".join(f"{ext}: {count}" for ext, count in sorted(node["assets"].items()))
            parts = []
            if node["num_py"]:
                parts.append(f"{node['num_py']} .py")
            if assets_summary:
                parts.append(assets_summary)
            if parts:
                line += " (" + ", ".join(parts) + ")"
        lines.append(line)
        child_lines = build_tree_lines(tree, sorted(node["children"], key=lambda c: Path(c).name), depth + 1)
        lines.extend(child_lines)
    return lines

if __name__ == "__main__":
    run_pipeline()
