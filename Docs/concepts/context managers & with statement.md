# Context Managers and the `with` Statement in Python

<!--toc:start-->

- [Context Managers and the `with` Statement](#context-managers-and-the-with-statement)
  - [🧠 What is a Context Manager?](#🧠-what-is-a-context-manager)
    - [The Protocol: `__enter__` and `__exit__`](#the-protocol-__enter__-and-__exit__)
  - [📦 Built-in Context Managers](#📦-built-in-context-managers)
    - [File Handling](#file-handling)
    - [Threading Locks](#threading-locks)
    - [`contextlib`](#contextlib)
  - [🔄 The `with` Statement](#🔄-the-with-statement)
    - [Basic Syntax](#basic-syntax)
    - [Multiple Contexts](#multiple-contexts)
  - [🛠 Custom Context Managers](#️-custom-context-managers)
    - [Class-based Implementation](#class-based-implementation)
    - [`@contextmanager` Decorator](#contextmanager-decorator)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Exceptions in `__enter__` vs `__exit__`](#1-exceptions-in-__enter__-vs-__exit__)
    - [2. Re-raising vs swallowing exceptions](#2-re-raising-vs-swallowing-exceptions)
    - [3. `yield` vs `return` in generators](#3-yield-vs-return-in-generators)
  - [🔗 Related Patterns](#🔗-related-patterns)
    - [`async with`](#async-with)
    - [Decorator context managers](#decorator-context-managers)
  - [🔍 Identity and Type Checks](#🔍-identity-and-type-checks)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

Context managers ensure proper acquisition and release of resources — even in the presence of exceptions.

---

## 🧠 What is a Context Manager?

A **context manager** is an object that defines _runtime context_ for code executed within a `with` block.

It guarantees setup and teardown logic runs — especially cleanup (e.g., closing files, releasing locks).

### The Protocol: `__enter__` and `__exit__`

Any object implementing both methods is a context manager:

```python
class MyContextManager:
    def __enter__(self):
        # Setup: returns object assigned to `as` variable
        print("Entering")
        return "resource"

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Teardown: runs *always*, even if exception occurs
        print("Exiting")
        return False  # ← True would suppress the exception

# Usage:
with MyContextManager() as res:
    print(res)      # ✅ "resource"
# Output:
# Entering
# resource
# Exiting
```

### Parameters of `__exit__`

| Parameter  | Purpose                     |
| ---------- | --------------------------- |
| `exc_type` | Exception class (or `None`) |
| `exc_val`  | Exception instance          |
| `exc_tb`   | Traceback object            |

If an exception occurs inside the `with`, Python passes it to `__exit__`.

---

## 📦 Built-in Context Managers

### File Handling

```python
# Safe file reading — file closes automatically
with open("data.txt", "r") as f:
    content = f.read()
# ✅ File is closed even if read() raises UnicodeError

# Multiple files:
with open("in.txt", "r") as src, open("out.txt", "w") as dst:
    dst.write(src.read())
```

### Threading Locks

```python
import threading

lock = threading.Lock()
shared_counter = 0

def increment():
    global shared_counter
    with lock:          # 🔒 Acquires lock on entry, releases on exit
        shared_counter += 1

# Even if increment raises — lock is released!
```

### `contextlib`

A standard library of pre-built context managers:

```python
from contextlib import redirect_stdout, suppress

# Redirect stdout (great for tests)
with open("log.txt", "w") as f, redirect_stdout(f):
    print("This goes to the file!")

# Ignore specific exceptions
with suppress(FileNotFoundError):
    os.remove("optional_file.txt")   # ❌ FileNotFoundError → ignored
```

Other utilities: `closing()`, `nullcontext()`, `asynccontextmanager` (see below).

---

## 🔄 The `with` Statement

### Basic Syntax

```python
with context_expr [as var]:
    # body
```

- `context_expr` evaluated → result must have `__enter__/__exit__`
- Result passed to `__enter__` → return value assigned to `var` (if present)
- Body executed
- `__exit__(exc_type, exc_val, exc_tb)` called automatically

---

### Multiple Contexts

```python
# Python 3.10+ supports parentheses for multiline:
with (
    open("file1.txt") as f1,
    open("file2.txt") as f2,
):
    process(f1.read(), f2.read())

# Or chained commas:
with open("a.txt"), open("b.txt"):
    ...
```

> 🔍 All context managers are entered left-to-right, exited right-to-left (LIFO).

---

## 🛠 Custom Context Managers

### Class-based Implementation

```python
from time import perf_counter

class Timed:
    def __enter__(self):
        self.start = perf_counter()
        return self  # Often returned to access metrics later

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = perf_counter() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False  # Don't suppress exceptions

# Usage:
with Timed() as timer:
    sum(range(10_000_000))
# ✅ "Elapsed: 0.2345s"
```

---

### `@contextmanager` Decorator

Uses a generator to define context logic:

```python
from contextlib import contextmanager

@contextmanager
def open_file(path, mode):
    f = open(path, mode)
    try:
        yield f      # ✅ Value to bind to `as`
    finally:
        f.close()    # Teardown runs *always*

# Usage:
with open_file("data.txt", "w") as f:
    f.write("Hello!")
```

> ⚠️ Must use `try`/`finally`, not `with` — otherwise exceptions during `yield` break cleanup.

#### Real-world example: database connection

```python
@contextmanager
def db_session():
    conn = connect_to_db()
    try:
        yield conn
    finally:
        conn.close()

# Usage:
with db_session() as conn:
    conn.execute("SELECT * FROM users")
```

---

## ⚠️ Common Pitfalls

### 1. Exceptions in `__enter__` vs `__exit__`

```python
class BrokenCM:
    def __enter__(self):
        raise RuntimeError("Setup failed")
    def __exit__(self, *args):
        print("Cleaning up")  # ❌ Never runs!

with BrokenCM():
    pass
# Output: only RuntimeError — no "Cleaning up"
```

✅ Fix: Handle setup in `__enter__` and ensure teardown doesn’t depend on successful entry.

---

### 2. Re-raising vs swallowing exceptions

```python
class SilentError:
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Caught exception")
        return True   # ✅ Suppresses exception
# or:
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Caught exception")
        raise         # ✅ Re-raises (same as return False)
```

> 📌 `return True` → exception suppressed  
> 📌 `return False` or `None`/no return → re-raised  
> 📌 `raise` → forces re-raise (preserves original traceback)

---

### 3. `yield` vs `return` in generators

```python
@contextmanager
def bad_cm():
    yield "item"     # ❌ Exception after yield → cleanup skipped!
    print("Cleanup")  # Never runs on exception

@contextmanager
def good_cm():
    try:
        yield "item"  # ✅ Cleanup always runs
    finally:
        print("Cleanup")
```

---

## 🔗 Related Patterns

### `async with`

For async context managers:

```python
import asyncio
from aiofiles import open as aopen

async def main():
    async with aopen("data.txt", "w") as f:
        await f.write("Hello!")
# ✅ Resource cleaned up after async context
```

- Requires `__aenter__` and `__aexit__` methods

---

### Decorator Context Managers

Context managers can be _used as decorators_ (via `contextlib.ExitStack`):

```python
from contextlib import contextmanager, ExitStack

@contextmanager
def resource(name):
    print(f"Acquire {name}")
    try:
        yield name
    finally:
        print(f"Release {name}")

# Usage as context manager (with):
with resource("db"):
    print("Do work")

# Usage as decorator:
@resource("file")  # ❌ Actually *wraps* the function — use ExitStack for decorators
def work():
    print("Work done")
```

> 🔍 The `@contextmanager` decorator turns generators into context managers — but **decorator usage is rare**; prefer `with`.

---

## 🔍 Identity and Type Checks

```python
from contextlib import suppress

cm = suppress()
print(isinstance(cm, type))  # ❌ False
print(hasattr(cm, "__enter__"))  # ✅ True

# Common check:
from contextlib import AbstractContextManager
print(isinstance(cm, AbstractContextManager))  # ✅ True
```

---

## 🔗 Further Reading

- [Python docs: `with` statement](https://docs.python.org/3/reference/compound_stmts.html#with)
- [Python docs: `contextlib` module](https://docs.python.org/3/library/contextlib.html)
- [PEP 343 — The `with` Statement](https://peps.python.org/pep-0343/)
- [Python docs: `__exit__` protocol](https://docs.python.org/3/reference/datamodel.html#object.__exit__)
