# 🧠 PIL User Guide — Project Intelligence Layer

This guide explains what the **Project Intelligence Layer (PIL)** is, why it exists, and how to use it effectively as a developer, team member, or AI assistant.

---

## 📖 Updated PIL Documentation

### 📖 Introduction to PIL

PIL is a code intelligence framework that builds and maintains a live metadata graph of all meaningful elements in your codebase: functions, classes, modules, variables, and assets. It supports governance, clarity, and assistant reasoning by extracting, validating, and exporting standardized metadata for every tracked symbol.

PIL is designed to:

* Eliminate redundant or abandoned code.
* Prevent misunderstandings about function roles or signatures.
* Maintain architectural clarity through metadata.
* Provide a persistent, factual map for AI to use during code reasoning.

### What Is the Entity Graph?

The **entity graph** is the central output of PIL — a JSON-based structure representing every tracked symbol and its metadata. It includes relationships (like function calls), annotations (e.g., `@tags`, `@status`), and linkage between code elements.

The graph is not a complete mirror of the code but rather a **structural intelligence layer**. It enables reliable decision-making, cross-referencing, and documentation generation.

> 📌 An **entity** is anything PIL tracks: a function, class, module, or asset. Each entity has a unique `fqname` and metadata such as description, tags, and links.

---

### 🗅 First-Time Setup

Before starting:

* Place the entire PIL folder (e.g. `PIL_Project/`) as a **sibling to your project root**.

  * For example, if your project is `AdriftProject`, then structure it as:

    ```
    AdriftProject/
    ├── Adrift/               ← your actual codebase
    ├── PIL_Project/          ← this contains pil_meta and scripts
    └── run_pil.py            ← placed in project root
    ```

1. Copy `run_pil.py` into your project root.

2. Edit the embedded configuration inside `run_pil.py` to set:

   * `project_root`, `output_dir`, `snapshot_dir`, and any other relevant paths.

3. Feed the AI assistant a copy of the **Docstring and Annotation Standards — Quick Instructions**, **Coding Standards and Architecture Rules**, and the **Assistant Behavior Profile: Structured Metadata Architect** documents.

   * These documents are included in the `PIL_Project/documents/` folder.

---

### 🔁 Normal Workflow

Once PIL is set up:

* Run `run_pil.py` for the first time and feed the resulting `entity_graph.json` back to the AI assistant.
* Run `run_pil.py` after each meaningful code change or refactor.
* Upload the latest `entity_graph.json` to the AI assistant at the start of each working session.
* If `scripts/snapshot_project.py` is present, a snapshot of the full project as well as a copy of the latest entity graph will be created automatically after each pipeline run.
* ⚠️ **The entire contents of the ************`exports/`************ folder are deleted and regenerated on each run.** Do not store anything here that you want to keep — this folder is volatile by design.
* ✅ **Only the most recent ************`entity_graph.json`************ is stored in ************`exports/`************.** Always use this file as the current source of truth. For older versions, consult the timestamped archives in the `snapshots/` directory.

---

### 📚 Embedded Configuration Example

Here is a basic working example of the embedded configuration inside `run_pil.py`, assuming your project is named `AdriftProject`:

```python
PIL_CONFIG = {
  "project_root": "./AdriftProject",
  "scan_dirs": [
    "./AdriftProject",
    "./tests",
    "./scripts"
  ],
  "journal_path": "./docs",
  "output_dir": "./exports",
  "docs_dir": "./documents",
  "snapshot_dir": "./snapshots",
  "vault_dir": "./exports/vault",
  "config_self_path": "./run_pil.py",
  "pil_module_path": "./AdriftProject",
  "asset_extensions": [".png", ".json", ".tmx", ".glb", ".shader", ".svg", ".csv"],
  "asset_dirs": ["./assets"]
}
```

Customize paths as needed, ensuring that:

* All paths are relative to the project root or absolute.
* `asset_extensions` lists the file types PIL should track.
* `config_self_path` points to the location of the `run_pil.py` file.

---

This update clearly explains the current single-file configuration approach.
