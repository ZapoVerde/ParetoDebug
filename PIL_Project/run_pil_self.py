# run_pil_self.py
"""
DO NOT RELOCATE OR REUSE THIS FILE OUTSIDE THE ADRIFT PROJECT.

Self-contained entry point for running the PIL pipeline locally.
Writes its own config and dynamically resolves the pipeline path.
Intended for internal testing and standalone runs only.

To run from root:
    python run_pil_self.py

@tags: ["entrypoint", "self-contained", "adrift-only"]
@status: "stable"
"""

import json
import traceback
import sys
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Callable

PIL_CONFIG = {
    # 📁 Root of the project to scan
    "project_root": ".",

    # 📂 Directories to scan for code and assets
    "scan_dirs": [
        "./pil_meta",
        "./tests",
        "./scripts"
    ],

    # 📤 Where exports (JSON, etc) are saved
    "output_dir": "./exports",

    # 🧳 Directory for full project snapshots
    "snapshot_dir": "./snapshots",

    # 📌 Where this config is written (by this file)
    "config_self_path": "./pilconfig.json",

    # 📦 Where the PIL module is located (for dynamic import)
    "pil_module_path": ".",

    # 🎨 Asset file extensions to include in scan
    "asset_extensions": [
        ".png", ".json", ".tmx", ".glb", ".shader", ".svg", ".csv"
    ],

    # 🚫 Folder names to ignore during scanning
    "ignored_folders": [
        ".git", "__pycache__", "snapshots", "exports",
        ".mypy_cache", ".venv", "env", ".idea", ".pytest_cache"
    ]
}

def import_pipeline_run_function(pil_module_path: str) -> Callable[[str], None]:
    """Dynamically imports run_pipeline() from pil_meta/pipeline.py inside pil_module_path."""
    pil_meta_path = Path(pil_module_path) / "pil_meta" / "pipeline.py"
    if not pil_meta_path.exists():
        raise FileNotFoundError(f"Pipeline file not found: {pil_meta_path}")

    spec = importlib.util.spec_from_file_location("pil_meta.pipeline", pil_meta_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create import spec for: {pil_meta_path}")

    module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_pipeline


def main():
    try:
        print("🔧 [BOOT] Starting PIL self-runner...\n")

        config_path = Path(PIL_CONFIG["config_self_path"])
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(PIL_CONFIG, f, indent=2)

        run_pipeline = import_pipeline_run_function(PIL_CONFIG["pil_module_path"])
        print(f"🚀 [RUNNING] Executing pipeline using: {config_path.resolve()}\n")
        run_pipeline(str(config_path))

        input("\n✅ Pipeline completed successfully. Press Enter to exit...")

    except Exception as e:
        print("\n❌ [RUN_PIL ERROR] Pipeline execution failed.")
        print(f"   Reason: {str(e)}")
        traceback.print_exc()
        input("\n🛑 Press Enter to close...")  # Prevent auto-close
        sys.exit(1)
    
    finally:
        input("\n✅ Pipeline complete. Press Enter to exit...")


if __name__ == "__main__":
    main()
