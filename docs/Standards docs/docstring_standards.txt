# 📜 Docstring and Annotation Standards — Quick Instructions

**MANDATORY**
All code symbols (functions, classes, modules, variables, lists, constants) must follow these documentation standards.

---

## 🔹 Format Requirements

### 1. Docstring Structure

Each docstring must begin with a **one-sentence summary** of the symbol’s purpose.
This first line is extracted as the `description` in metadata exports.

You may include additional lines after the summary to explain behavior, usage, or rationale.
These extended lines are preserved in vault exports and docstring viewers but do not affect the primary `description` field.

#### Example

```python
def connect_to_server():
    """Establishes a connection to the primary service.
    This function handles retries, logging, and TLS negotiation.
    @tags: ["network", "core"]
    @status: "stable"
    """
```

---

### 2. Optional Annotation Lines (within docstrings or above variables)

* `@tags: ["tag1", "tag2"]` — Python list of strings (no spaces inside tags)
* `@journal: "Journal Entry Title"` — Link to internal documentation or design journal
* `@deprecated` — No value needed; marks the symbol as deprecated
* `@status: "draft"` — Acceptable values: `"draft"`, `"stable"`, `"experimental"`, etc.
* `@visibility: "internal"` — `"internal"` or `"public"`; used for vault filtering

---

### 3. Variables / Constants

Use `#` comments immediately above the assignment line. You may use any of the annotation fields above.

#### Example

```python
# Number of retries for the connection.
# @tags: ["network", "config"]
# @status: "draft"
MAX_RETRIES = 3
```

---

### 4. File Headers

Each Python file must begin with a **file header comment** that declares the relative path and filename. This ensures traceability in exports and navigation tools.

#### Example

```python
# pil_meta/utils/snapshot_utils.py
```

This header must be the first non-empty, non-shebang line in the file.

---

## 📟 Required Metadata Fields (for every symbol)

These fields are mandatory for all exported symbols and must be derivable from context or annotations:

| Field    | Required | Description                                                 |
| -------- | -------- | ----------------------------------------------------------- |
| `fqname` | ✅        | Fully qualified name (e.g. `mod.sub.func`)                  |
| `module` | ✅        | Module or file where symbol is defined                      |
| `type`   | ✅        | One of: `function`, `method`, `class`, `module`, `variable` |
| `name`   | ✅        | Local symbol name (e.g. `foo`)                              |

Missing or empty values are considered a **standards violation** and will be surfaced in validation or governance reports.

---

## 🚫 Enforcement Policy

No code or documentation will be accepted unless it fully complies with these standards. This includes:

* Assistant-generated output
* Pull requests and manual changes
* Vault-exported entities
* Entries in `entity_graph.json`

Violations will be flagged in `function_map_exceptions.json` and blocked from vault export.
When in doubt, write a clear summary and include tags or status markers.

---

## 🔍 Rationale

* Enables advanced search, filtering, and navigation in the vault and IDE.
* Links code to design docs and journals for live governance.
* Ensures assistant-generated code aligns with long-term project structure.
* Makes code discoverable, explainable, and self-validating.

Ask yourself:

> Would this symbol be understandable to a new team member or a future AI assistant?
> If not, document it better.

---

## 📦 Integration with PIL

These documentation standards are directly consumed by the **Project Intelligence Layer (PIL)**.

Specifically:

* The **first line** of each docstring is used as the `description` field in the entity graph.
* The following metadata is required for each symbol in `entity_graph.json`: `fqname`, `module`, `type`, `name`.
* Tags such as `@tags`, `@status`, and `@journal` are indexed and surfaced in:

  * Markdown vault exports
  * Symbol usage maps
  * Governance reports
* The `@visibility: "internal"` tag suppresses a symbol from being exported to documentation, but retains it in metadata.

📌 These annotations are not optional styling — they are **enforced** by PIL’s validators and required for metadata health.
