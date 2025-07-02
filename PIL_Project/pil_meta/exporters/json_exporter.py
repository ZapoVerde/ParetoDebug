# pil_meta/exporters/json_exporter.py

import json
from datetime import datetime
from pathlib import Path
from typing import Union, Optional

def export_entity_graph(
    graph: dict,
    output_dir: Union[str, Path],
    project_name: str = "project",
    timestamp: Optional[str] = None
) -> dict:
    """Exports the entity graph as a timestamped JSON file.
    The output filename includes both the project name and timestamp for traceability.
    The file content wraps the graph dict with `timestamp` and `project_name` fields.

    Args:
        graph (dict): Entity graph.
        output_dir (Union[str, Path]): Directory for output files.
        project_name (str): Project name for filename and metadata.
        timestamp (Optional[str]): Timestamp string (YYYYMMDD_HHMMSS). If not provided, uses current time.

    Returns:
        dict: {"timestamped": path to timestamped entity graph JSON file}
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"entity_graph_{project_name}_{ts}.json"
    ts_path = output_dir / filename

    wrapper = {
        "timestamp": ts,
        "project_name": project_name,
        "graph": graph
    }

    with open(ts_path, "w", encoding="utf-8") as f:
        json.dump(wrapper, f, indent=2, ensure_ascii=False)

    return {"timestamped": str(ts_path)}
