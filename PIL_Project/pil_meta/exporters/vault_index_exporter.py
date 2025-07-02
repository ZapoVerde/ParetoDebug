# pil_meta/exporters/vault_index_exporter.py

from pathlib import Path
from typing import Union, Optional

def export_vault_index(graph: dict,
                       output_dir: Union[str, Path],
                       project_name: str = "project",
                       timestamp: Optional[str] = None) -> str:
    """
    Export a Markdown index listing all symbols in the vault, grouped by type.

    Args:
        graph (dict): Entity graph containing all symbols.
        output_dir (Union[str, Path]): Output directory.
        project_name (str): Optional project name prefix (unused).
        timestamp (str): Optional timestamp (unused).

    Returns:
        str: Full path to the created index.md file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    index_lines = ["# Symbol Index\n"]
    grouped = {}

    for node in graph.values():
        if node.get("visibility") == "internal":
            continue
        typ = node.get("type", "misc")
        grouped.setdefault(typ, []).append(node)

    for typ in sorted(grouped):
        index_lines.append(f"\n## {typ.capitalize()}s")
        for node in sorted(grouped[typ], key=lambda x: x.get("fqname", "")):
            name = node.get("name") or node.get("fqname")
            filename = name.replace("/", "_").replace(".", "_") + ".md"
            subdir = typ + "s"
            index_lines.append(f"- [{name}]({subdir}/{filename})")

    outfile = output_dir / "index.md"
    outfile.write_text("\n".join(index_lines), encoding="utf-8")
    return str(outfile)
