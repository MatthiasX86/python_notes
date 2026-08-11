# Modules vs Packages in Python

<!--toc:start-->

- [Modules vs Packages in Python](#modules-vs-packages-in-python)
  - [🧠 Core Concepts](#🧠-core-concepts)
    - [What is a Module?](#what-is-a-module)
    - [What is a Package?](#what-is-a-package)
  - [📁 Structure & Organization](#📁-structure--organization)
    - [Module Anatomy](#module-anatomy)
    - [Package Anatomy](#package-anatomy)
  - [📦 Import Mechanics](#📦-import-mechanics)
    - [`__name__`, `__file__`, and `__package__`](#__name____file__-and-__package__)
    - [Relative vs Absolute Imports](#relative-vs-absolute-imports)
  - [🔄 Dynamic Behavior](#🔄-dynamic-behavior)
    - [`__main__` and Execution Context](#__main__-and-execution-context)
    - [Namespace Packages (PEP 420)](#namespace-packages-pep-420)
  - [🔍 Identity & Equality: `is` vs `==`](#🔍-identity--equality-is-vs--)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Missing `__init__.py`](#1-missing-__init__.py)
    - [2. Circular imports](#2-circular-imports)
    - [3. Running packages vs modules directly](#3-running-packages-vs-modules-directly)
  - [⚙️ Implementation Details](#️-implementation-details)
    - [How import finds modules](#how-import-finds-modules)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

Understanding the distinction between modules and packages is essential for writing maintainable, scalable Python code.

---

## 🧠 Core Concepts

### What is a Module?

A **module** is a single Python file that contains definitions and statements.

- It’s the basic unit of code organization.
- Every `.py` file you write is a module by default.
- Imported modules become instances of `types.ModuleType`.

```python
# utils.py — a module
def greet(name):
    return f"Hello, {name}!"

PI = 3.14159
```

```python
import utils
print(utils.greet("Alice"))  # ✅ "Hello, Alice!"
print(utils.PI)              # ✅ 3.14159
```

> 📌 **Key insight**: A module is just a namespace — all top-level code runs once on import.

---

### What is a Package?

A **package** is a directory (namespace) that contains modules and/or other packages.

- Must include an `__init__.py` file (for regular packages).
- Enables hierarchical organization: `pkg.subpkg.mod`.

```
mypkg/
├── __init__.py     ← Makes it a package (can be empty)
├── utils.py        ← Module
└── io/
    ├── __init__.py
    └── fileops.py  ← Nested module & package
```

Import with dots:

```python
from mypkg.utils import greet
import mypkg.io.fileops as fileops

fileops.read("data.txt")
```

---

## 📁 Structure & Organization

### Module Anatomy

A typical module has three parts:

1. **Top-level code** — runs on import (e.g., `if __name__ == "__main__":`)
2. **Definitions** — functions, classes, constants
3. **Imports and exports** — `import`, `from X import Y`, `__all__`

```python
# logger.py
"""Simple logging module."""

import sys

VERSION = "1.0"
__all__ = ["log", "DEBUG"]

def log(msg, level="INFO"):
    print(f"[{level}] {msg}")

# Only run this if executed directly
if __name__ == "__main__":
    log("Module loaded!")
```

---

### Package Anatomy

A package organizes _multiple_ modules into a hierarchy.

| Component     | Purpose                                         |
| ------------- | ----------------------------------------------- |
| `__init__.py` | Marks directory as package; runs on import      |
| Modules       | `.py` files containing code                     |
| Subpackages   | Nested directories with their own `__init__.py` |

```python
# mypkg/__init__.py
"""My package initialization."""

from . import utils, io
__all__ = ["utils", "io"]
```

Now:

```python
import mypkg  # Runs __init__.py
print(mypkg.utils.greet("Bob"))
```

> 💡 tip: `__init__.py` can be empty — but often initializes shared state or exports a curated API.

---

## 📦 Import Mechanics

### `__name__`, `__file__`, and `__package__`

Every module object has these special attributes:

| Attribute     | Description                                        |
| ------------- | -------------------------------------------------- |
| `__name__`    | Module name (`"__main__"` for entry point)         |
| `__file__`    | Path to the `.py` file (or directory for packages) |
| `__package__` | Parent package name for relative imports           |

```python
# example.py (run as: python -m mypkg.example)
print(__name__)     # → "mypkg.example"
print(__file__)     # → "/path/to/mypkg/example.py"
print(__package__)  # → "mypkg" (for relative import resolution)
```

> ⚠️ If you run `python mypkg/example.py`, then `__name__ = "__main__"` and `__package__ = None` — relative imports will fail.

---

### Relative vs Absolute Imports

| Type         | Syntax                  | Pros & Cons                                 |
| ------------ | ----------------------- | ------------------------------------------- |
| **Absolute** | `import pkg.mod`        | Clear, explicit; works everywhere           |
| **Relative** | `from . import mod`     | Portable within package; avoids hard-coding |
|              | `from ..utils import x` |                                             |

✅ **Good** (absolute):

```python
# mypkg/network/http.py
import requests
from mypkg.utils import logger
```

✅ **Better** (relative):

```python
# mypkg/network/http.py
from ..utils import logger  # Works even if renamed to "web" or "api"
```

> 📌 Relative imports require `__package__` to be set — hence: use `python -m pkg.module`, not `python module.py`.

---

## 🔄 Dynamic Behavior

### `__main__` and Execution Context

When a module is run _directly_, Python creates a special `"__main__"` namespace:

```python
# app.py
def main():
    print("Running application...")

if __name__ == "__main__":
    main()
```

Run:

```bash
python app.py       # → "Running application..."
python -m app      # Same result (but sets __package__)
```

> 🔍 The difference: `-m` makes Python treat the module as part of a package — critical for relative imports.

---

### Namespace Packages (PEP 420)

Python 3.3+ allows **namespace packages**: directories _without_ `__init__.py`.

- Used for splitting a single package across multiple directories (e.g., `site-packages`).
- Each subdirectory can be in different locations.

```
lib1/
└── pkg/
    └── mod_a.py
lib2/
└── pkg/             ← Another "pkg" directory (no __init__.py)
    └── mod_b.py
```

Then:

```python
import sys
sys.path.extend(["lib1", "lib2"])

from pkg import mod_a, mod_b  # ✅ Works! Both parts merge into one namespace
```

> 📌 Namespace packages can’t define `__init__.py` — they’re automatically inferred.

---

## 🔍 Identity & Equality: `is` vs `==`

Modules have identity — two imports point to the _same object_.

```python
import mypkg.utils as u1
import mypkg.utils as u2

print(u1 is u2)     # ✅ True (cached after first import)
print(u1.__name__)  # → "mypkg.utils"
```

But packages are _not_ cached across separate import statements:

```python
import sys

# Two ways to get same module path — different names
sys.path.insert(0, "src")
import pkg.mod as m1

# But relative import inside same package reuses object
from . import mod as m2

print(m1 is m2)     # ❓ Depends on path resolution — avoid!
```

✅ Best practice: Use `import` once, then alias internally.

---

## ⚠️ Common Pitfalls

### 1. Missing `__init__.py`

```python
# project/
# └── data/      ← no __init__.py (in Python < 3.3)
#     └── io.py
```

```python
import project.data.io  # ❌ ImportError: No module named 'project.data'
```

✅ Fix: Add empty `__init__.py`, or use Python 3.3+ (namespace package).

---

### 2. Circular imports

```python
# a.py
import b
print("a loaded")

# b.py
import a
print("b loaded")
```

Run `python a.py` → infinite recursion and error.

✅ Fix strategies:

- Refactor shared code into `common.py`
- Delay imports inside functions
- Use `from X import Y` (imports only names, not full module)

---

### 3. Running packages vs modules directly

```bash
python pkg/main.py     # ❌ Breaks relative imports (main is "__main__", not "pkg.main")
python -m pkg.main     # ✅ Works — sets __package__ correctly
```

> 🧠 Rule: For packages, _always_ use `-m` for entry-point scripts.

---

## ⚙️ Implementation Details

### How import finds modules

Python’s `sys.meta_path` and import hooks resolve module locations:

1. **Built-in modules** (`sys`, `math`) — compiled C libraries
2. **Frozen modules** (e.g., in `.pyz` archives)
3. **`sys.path` directories**: current dir → site-packages → environment paths

```python
import sys
print(sys.path)
# ['/current/dir', '/usr/lib/python3.10', ...]
```

You can extend it:

```python
sys.path.insert(0, "/path/to/local/modules")
```

> 🔍 `importlib.import_module("pkg.mod")` is the programmatic way to import dynamically.

---

## 🔗 Further Reading

- [Python docs: Modules](https://docs.python.org/3/tutorial/modules.html)
- [Python docs: Packages](https://docs.python.org/3/tutorial/modules.html#packages)
- [PEP 420 — Implicit Namespace Packages](https://peps.python.org/pep-0420/)
- [Python docs: `importlib` module](https://docs.python.org/3/library/importlib.html)
- [Python docs: `__main__` special name](https://docs.python.org/3/library/__main__.html)
