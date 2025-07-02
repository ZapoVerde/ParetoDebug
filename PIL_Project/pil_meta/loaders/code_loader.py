# pil_meta/loaders/code_loader.py
"""
Code Loader (loaders)

Walks the source tree and extracts all top-level symbols (functions, classes, methods, variables, modules).
Enriches each symbol with structured docstring metadata in bulk for efficient processing.
"""

import ast
from pathlib import Path
from typing import List, Dict, Any

from pil_meta.utils.docstring_utils import extract_docstring_metadata

def extract_nodes_from_ast(tree: ast.AST, source_file: Path, root_path: Path) -> List[Dict[str, Any]]:
    """
    Extract all classes, functions, methods, variables, and modules from the AST of a source file.

    @tags: ["loader", "code", "ast"]
    @status: "stable"
    @visibility: "internal"

    Args:
        tree (ast.AST): The parsed AST of the source file.
        source_file (Path): The full path to the source file.
        root_path (Path): The project root path to calculate relative paths.

    Returns:
        List[Dict[str, Any]]: A list of enriched symbol dictionaries.
    """
    symbols = []

    def module_name(path: Path) -> str:
        rel = path.relative_to(root_path).with_suffix("")
        return ".".join(rel.parts)

    module = module_name(source_file)
    source = source_file.read_text(encoding="utf-8")

    class ParentNodeVisitor(ast.NodeVisitor):
        def visit(self, node):
            for child in ast.iter_child_nodes(node):
                setattr(child, 'parent', node)
                self.visit(child)

    ParentNodeVisitor().visit(tree)

    # Include module node
    tree_module = tree if isinstance(tree, ast.Module) else ast.Module()
    docstring = ast.get_docstring(tree_module) or ""

    doc_meta = extract_docstring_metadata(docstring)
    symbols.append({
        "fqname": module,
        "module": module,
        "name": module,
        "type": "module",
        "lineno": 1,
        "source_file": str(source_file.relative_to(root_path)),
        "description": doc_meta["description"],
        "docstring_full": doc_meta["docstring_full"],
        "tags": doc_meta["tags"],
        "linked_journal_entry": doc_meta["linked_journal_entry"],
        "deprecated": doc_meta["deprecated"],
        "status": doc_meta["status"],
        "visibility": doc_meta["visibility"],
        "docstring_present": bool(doc_meta["description"]),
        "metadata": {}
    })

    for node in ast.walk(tree):
        parent = getattr(node, 'parent', None)

        # ❌ Skip scoped/inner functions — only allow top-level + class-level
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not isinstance(parent, (ast.Module, ast.ClassDef)):
                continue
            node_type = "function" if isinstance(parent, ast.Module) else "method"
            docstring = ast.get_docstring(node) or ""
            doc_meta = extract_docstring_metadata(docstring)
            fqname = f"{module}.{node.name}"
            symbol = {
                "fqname": fqname,
                "module": module,
                "name": node.name,
                "type": node_type,
                "lineno": node.lineno,
                "source_file": str(source_file.relative_to(root_path)),
                "description": doc_meta["description"],
                "docstring_full": doc_meta["docstring_full"],
                "tags": doc_meta["tags"],
                "linked_journal_entry": doc_meta["linked_journal_entry"],
                "deprecated": doc_meta["deprecated"],
                "status": doc_meta["status"],
                "visibility": doc_meta["visibility"],
                "docstring_present": bool(doc_meta["description"]),
                "metadata": {
                    "args": [arg.arg for arg in node.args.args] if hasattr(node, 'args') else [],
                    "returns": None
                }
            }
            symbols.append(symbol)

        elif isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node) or ""
            doc_meta = extract_docstring_metadata(docstring)
            fqname = f"{module}.{node.name}"
            symbol = {
                "fqname": fqname,
                "module": module,
                "name": node.name,
                "type": "class",
                "lineno": node.lineno,
                "source_file": str(source_file.relative_to(root_path)),
                "description": doc_meta["description"],
                "docstring_full": doc_meta["docstring_full"],
                "tags": doc_meta["tags"],
                "linked_journal_entry": doc_meta["linked_journal_entry"],
                "deprecated": doc_meta["deprecated"],
                "status": doc_meta["status"],
                "visibility": doc_meta["visibility"],
                "docstring_present": bool(doc_meta["description"]),
                "metadata": {}
            }
            symbols.append(symbol)

        elif isinstance(node, ast.Assign):
            if isinstance(parent, ast.Module) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                lineno = getattr(node, 'lineno', 1)
                fqname = f"{module}.{var_name}"
                try:
                    source_lines = source.splitlines()
                    line_text = source_lines[lineno - 1]
                except Exception:
                    line_text = ""
                is_constant = var_name.isupper()
                is_public = not var_name.startswith('_')
                is_explicit = ('# @export' in line_text or '# doc:' in line_text)
                if is_constant or is_public or is_explicit:
                    doc_comment = ""
                    if '#' in line_text:
                        doc_comment = line_text.split('#', 1)[1].strip()
                    doc_meta = {
                        "description": doc_comment,
                        "docstring_full": doc_comment,
                        "tags": [],
                        "linked_journal_entry": "",
                        "deprecated": False,
                        "status": "",
                        "visibility": "",
                    }
                    symbol = {
                        "fqname": fqname,
                        "module": module,
                        "name": var_name,
                        "type": "variable",
                        "lineno": lineno,
                        "source_file": str(source_file.relative_to(root_path)),
                        "description": doc_meta["description"],
                        "docstring_full": doc_meta["docstring_full"],
                        "tags": doc_meta["tags"],
                        "linked_journal_entry": doc_meta["linked_journal_entry"],
                        "deprecated": doc_meta["deprecated"],
                        "status": doc_meta["status"],
                        "visibility": doc_meta["visibility"],
                        "docstring_present": bool(doc_comment),
                        "metadata": {}
                    }
                    symbols.append(symbol)

    return symbols

def load_code_symbols(pyfile_path: str, project_root: str) -> List[Dict[str, Any]]:
    """
    Parse a single Python file and return a list of symbols with metadata.

    @tags: ["loader", "code"]
    @status: "stable"
    @visibility: "internal"

    Args:
        pyfile_path (str): Path to .py file.
        project_root (str): Project root directory (absolute).

    Returns:
        list of dicts: Each with type, name, fqname, module, lineno, doc.
    """
    path = Path(pyfile_path).resolve()
    root_path = Path(project_root).resolve()
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source, filename=str(path))
    return extract_nodes_from_ast(tree, path, root_path)
