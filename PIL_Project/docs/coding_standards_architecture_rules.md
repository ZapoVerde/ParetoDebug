# 🧑‍💻 Coding Standards and Architecture Rules

This document defines core coding standards and architectural rules enforced across the PIL codebase.
It complements the `docstring_standards_instructions.md` document by addressing broader structural, behavioral, and system-level best practices.

---

## ⚙️ Function Scoping and Export Rules

### 🔹 Local Function Visibility

Local (scoped) functions — i.e., those defined inside other functions — must never be exported to the `entity_graph.json`. These functions:

* Are exempt from docstring enforcement
* Cannot be linked in `calls_fqns`
* Must not contain architecture-critical logic

> ✅ Top-level functions and class methods are the only exportable symbols.

**Inline Rule:**

```python
# Local helper; not exported. Ignored in entity graph.
def helper():
    ...
```

---

## 🔁 MFV Dispatch and Top-Level Responsibility

### 🔹 Multi-Function Variable Usage Rule

> All calls to multi-function variables (MFVs) must occur in top-level functions or methods.

Inner/local functions **may receive** MFVs as parameters, but must not reference or call them directly. This ensures that MFV usage is:

* Registered in `calls_fqns`
* Testable and observable
* Separated from hidden logic paths

**✅ Correct:**

```python
def handle(mfv):
    def inner():
        return mfv()  # OK — passed in explicitly
    return inner()
```

**❌ Incorrect:**

```python
def outer():
    def inner():
        return global_mfv()  # BAD — untracked call
```

This constraint is enforceable via static AST scoping and manual validation.

---

## 📂 File and Module Boundaries

### 🔹 I/O Must Live in `loaders/`

Filesystem I/O — including reading config files, loading assets, and scanning source trees — must be implemented only in modules within the `loaders/` folder.

Utility modules in `utils/` must remain pure: no file I/O, subprocess calls, or mutable global state.

| Layer      | Permitted Actions                           |
| ---------- | ------------------------------------------- |
| `loaders/` | Load files, scan folders, parse documents   |
| `utils/`   | Pure transforms, path resolution, filtering |

---

## 🧠 Traceability vs Encapsulation

All architectural design must favor **traceability** when in conflict with **encapsulation**. This means:

* Prefer making critical dispatch points visible in exported functions
* Avoid deeply nested logic or anonymous inline behaviors that interfere with symbol extraction

---

## ⛔ What Not to Do

* Do **not** define business logic inside scoped helpers unless it’s also tested at the top level
* Do **not** perform file I/O inside `utils/` modules
* Do **not** reference MFVs inside local/closure functions
* Do **not** expect any inner function to appear in vault exports, governance reports, or metadata audits

---

## 📌 Enforcement Status

These standards are **mandatory** for all assistant-generated code, pull requests, and validator-integrated systems.

Violations will:

* Be flagged during entity graph construction
* Block vault exports
* Be listed in `function_map_exceptions.json` until resolved

For rationale, see `docstring_standards_instructions.md` → "📦 Integration with PIL"
