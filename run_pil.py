# run_pil.py
"""
Self-contained entry point for running the PIL pipeline.
Handles path resolution and error reporting for the Adrift project.

@tags: ["entrypoint", "adrift", "self-contained"]
@status: "stable"
"""

import json
import sys
import traceback
from pathlib import Path
from types import ModuleType
from typing import Callable

# ================== PATH CONFIGURATION ==================
PROJECT_ROOT = Path(__file__).parent.absolute()
PIL_MODULE_PATH = PROJECT_ROOT / "PIL_Project"

PIL_CONFIG = {
    # 📁 Root of the project to scan
    "project_root": str(PROJECT_ROOT / "Testcode"),

    # 📂 Directories to scan for code and assets
    "scan_dirs": [str(PROJECT_ROOT / "Testcode")],

    # 📤 Where exports (JSON, etc) are saved
     "output_dir": str(PROJECT_ROOT / "exports"),

    # 🧳 Directory for full project snapshots
    "snapshot_dir": str(PROJECT_ROOT / "snapshots"),

    # 📌 Where this config is written (by this file)
    "config_self_path": str(PROJECT_ROOT / "pilconfig.json"),

    # 📦 Where the PIL module is located (for dynamic import)
    "pil_module_path": str(PIL_MODULE_PATH),

    # 🎨 Asset file extensions to include in scan
    "asset_extensions": [
        ".png", ".json", ".tmx", ".glb", ".shader", ".svg", ".csv"
        ],

    # 🚫 Folder names to ignore during scanning
    "ignored_folders": [
        ".git", "__pycache__", "snapshots", "exports",
        ".mypy_cache", ".venv", "env", ".idea", ".pytest_cache", 
        "node_modules", "documents", "PIL_Project"
    ]
}

def import_pipeline_run_function(pil_module_path: str) -> Callable[[str], None]:
    """Dynamically imports run_pipeline with full path validation.
    
    @tags: ["core", "import"]
    @status: "stable"
    """
    pil_meta_path = Path(pil_module_path) / "pil_meta" / "pipeline.py"
    
    print(f"🔍 Verifying pipeline at: {pil_meta_path}")
    if not pil_meta_path.exists():
        available = "\n  ".join(p.name for p in pil_meta_path.parent.iterdir())
        raise FileNotFoundError(
            f"Pipeline not found at {pil_meta_path}\n"
            f"Available files:\n  {available}"
        )

    spec = importlib.util.spec_from_file_location(
        "pil_meta.pipeline", 
        str(pil_meta_path)
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create import spec for: {pil_meta_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["pil_meta.pipeline"] = module  # Required for sub-imports
    spec.loader.exec_module(module)
    return module.run_pipeline

def main():
    """Main execution flow with error handling.
    
    @tags: ["core", "orchestration"]
    @status: "stable"
    """
    try:
        print(f"🏁 Starting PIL from: {PROJECT_ROOT}")
        print(f"📂 Scanning directory: {PIL_CONFIG['project_root']}")
        
        # Write config
        config_path = Path(PIL_CONFIG["config_self_path"])
        config_path.parent.mkdir(exist_ok=True)
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(PIL_CONFIG, f, indent=2)
        
        # Import and run
        run_pipeline = import_pipeline_run_function(PIL_CONFIG["pil_module_path"])
        run_pipeline(str(config_path))
        
    except Exception as e:
        print("\n❌ [RUN_PIL ERROR]", file=sys.stderr)
        print(f"   Reason: {type(e).__name__}: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        input("\n✅ Pipeline complete. Press Enter to exit...")

if __name__ == "__main__":
    import importlib.util  # Delayed import for cleaner error handling
    main()