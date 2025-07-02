# PIL_Project/scripts/rebuild_pil.py
"""
Entry point to run the PIL metadata pipeline.

Detects context (standalone vs embedded), adjusts sys.path, and invokes the main runner.
"""

import sys
from pathlib import Path

def main():
    # Resolve project structure
    this_file = Path(__file__).resolve()
    pil_project_root = this_file.parent.parent  # e.g., PIL_Project/
    pil_meta_path = pil_project_root / "pil_meta"

    if not pil_meta_path.exists():
        print(f"❌ Could not find pil_meta at expected location: {pil_meta_path}")
        sys.exit(1)

    # Register pil_meta for import resolution
    sys.path.insert(0, str(pil_project_root))

    from pil_meta.pipeline import run_pipeline

    config_path = sys.argv[1] if len(sys.argv) > 1 else "pilconfig.json"
    run_pipeline(config_path)

if __name__ == "__main__":
    main()
