1. Foundational Fluency (Basics + Modern Nuances)

| Topic                        | Why It Matters     | Sample Question                                                              | ✅ Correct Response / Key Insight                                                      |
| ---------------------------- | ------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Data Structures & Mutability | Avoids subtle bugs | “Why does `a = [1]; b = a; b += [2]` mutate `a`, but `b = b + [3]` doesn’t?” | `+=` calls `__iadd__` (in-place mutate); `+` creates a new object.                     |
| Control Flow & Late Binding  | Logic clarity      | “What’s the output of `[lambda: i for i in range(3)]` when called?”          | All return 2 (late binding). Fix: `lambda i=i: i` (default arg capture).               |
| Function Mechanics           | Defensive coding   | “What’s wrong with `def f(x=[])`? How do you fix it?”                        | Defaults are evaluated once at definition. Fix: `def f(x=None): if x is None: x = [].` |
| Exception Groups (3.11+)     | Production safety  | “How do you handle multiple errors in `asyncio.gather()`?”                   | Use `except*` (PEP 654) to catch ExceptionGroups, not just single exceptions.          |
| Variable Scope (LEGB)        | Debugging          | “Why does `x += 1` fail inside a function if `x` is global?”                 | Assignment makes `x` local by default. Fix: `global x` or `nonlocal x.`                |

---

1. Modern Python Idioms (“Pythonic” ≠ “Older Style”)

| Technique                 | Expected Behavior   | Sample Question                                            | ✅ Correct Response / Key Insight                                          |
| ------------------------- | ------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------- |
| `pathlib` vs `os.path`    | Prefer Path objects | “How do you get the parent directory of a file?”           | `Path('file.txt').parent` (returns `Path`, not `str`).                     |
| f-strings & Debugging     | Readability         | “How do you print a variable name and value in one line?”  | `f"{var=}"` outputs `var=10` (Python 3.8+ feature).                        |
| Context Managers          | Resource safety     | “Write an async context manager.”                          | Must use `async with` and define `__aenter__`/`__aexit__`.                 |
| Pattern Matching (3.10+)  | Complex logic       | “Rewrite this if/elif chain using `match/case`.”           | Use structural matching: `case {"status": 200, "data": list(d)}:`          |
| `__slots__` & Dataclasses | Memory optimization | “How do you save memory in a dataclass with 1M instances?” | `@dataclass(slots=True)` (Python 3.10+) prevents `__dict__` creation.      |
| Walrus Operator (`:=`)    | Conciseness         | “When is `:=` actually useful?”                            | Inside comprehensions or `while (line := f.read()):` to avoid double read. |

---

1. OOP & Design Patterns (Not Just Syntax)

| Concept                            | Assessment Focus     | Sample Question                                                       | ✅ Correct Response / Key Insight                                                                              |
| ---------------------------------- | -------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Dunder Methods                     | Protocol adherence   | “If I override `__eq__`, what else must I override?”                  | `__hash__`. If `__eq__` changes, objects become unhashable (cannot be dict keys) unless `__hash__` is updated. |
| Composition > Inheritance          | Flexibility          | “How would you avoid deep inheritance here?”                          | Use Mixin classes, Protocols (structural typing), or Dependency Injection.                                     |
| Metaclasses vs `__init_subclass__` | Advanced control     | “When do you actually need a metaclass?”                              | Almost never. Use `__init_subclass__` (hook on class creation) or class decorators instead.                    |
| Singleton Pitfalls                 | Testability          | “Why is a global singleton risky in tests?”                           | State persists between tests. Fix: Use Dependency Injection or fixtures to reset state.                        |
| Method Resolution Order (MRO)      | Multiple Inheritance | “How does Python decide which method to call in diamond inheritance?” | C3 Linearization. Check with `Class.mro()`. `super()` follows this order, not just "parent".                   |

---

1. Standard Library + Tooling (2026 Expectations)

| Area                         | Must-Knows       | Sample Question                                              | ✅ Correct Response / Key Insight                                                       |
| ---------------------------- | ---------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| `pathlib`, `os`, `sys`       | File/Env ops     | “How do you safely read an env var that might be missing?”   | `os.getenv("KEY", "default")`. `os.environ["KEY"]` raises `KeyError`.                   |
| `datetime`, `zoneinfo`       | Timezones        | “Why is `datetime.utcnow()` deprecated?”                     | It returns a naive object. Use `datetime.now(timezone.utc)` (aware).                    |
| `itertools`, `functools`     | Efficiency       | “What’s the difference between `cache` and `lru_cache`?”     | `cache` is unbounded (memory leak risk); `lru_cache` limits size.                       |
| Testing (`pytest`)           | Robustness       | “How do you test an async function?”                         | Use `@pytest.mark.asyncio` and await the call.                                          |
| Packaging (`pyproject.toml`) | Modern Standards | “Where do you define dependencies in 2026?”                  | `pyproject.toml` (`[project.dependencies]`). `setup.py` is deprecated for new projects. |
| Linting/Formatting           | Consistency      | “What is the modern replacement for flake8 + isort + black?” | `ruff`. It does all three (and more) in a single, fast binary.                          |

---

1. Type Hints — From Basic to Expert

| Level        | Expectation      | Sample Question                                                      | ✅ Correct Response / Key Insight                                                |
| ------------ | ---------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Basic        | Signatures       | “How do you hint a list of integers in Python 3.9+?”                 | `list[int]` (built-in generics). `List[int]` (typing module) is legacy.          |
| Intermediate | Unions/Optionals | “How do you write `Union[str, None]` in modern syntax?”              | `` `str\|None` `` (PEP 604).                                                     |
| Advanced     | Protocols/Guards | “What is the difference between `TypeGuard` and `TypeIs`?”           | `TypeIs` (3.12+) narrows the type in the `else` block too; `TypeGuard` does not. |
| Key Insight  | Static Analysis  | “Do type hints affect runtime performance?”                          | No. They are ignored at runtime (unless using a library like pydantic).          |
| Generics     | Reusability      | “How do you hint a function that returns the same type it receives?” | Use `TypeVar`: `def identity(x: T) -> T:`                                        |

---

1. Concurrency & Performance (The 2026 Trap Zone)

| Concept             | Critical Question                                              | ✅ Correct Response / Key Insight                                               |
| ------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Async/await         | “What happens if you call `time.sleep(5)` inside `async def`?” | Blocks the entire event loop. Must use `await asyncio.sleep(5)`.                |
| GIL & Free-Threaded | “How does Python 3.13+ change the GIL conversation?”           | No-GIL builds (PEP 703) are available but experimental; C-extensions may break. |
| `multiprocessing`   | “When would you prefer this over `asyncio`?”                   | CPU-bound tasks. Note the overhead of pickling data between processes.          |
| Memory Optimization | “How would you reduce memory for 1M objects?”                  | `__slots__`, `array.array`, or NumPy structured arrays (contiguous memory).     |
| I/O vs CPU          | “When do threads actually help in Python?”                     | Only for I/O-bound tasks (network/disk) where the GIL is released during waits. |

---

## 7. Code Review & Debugging (Practical Judgment)

Give candidates real-world snippets like:

```python
# config.py (buggy)
DEFAULT_CONFIG = {"timeout": 10, "retries": []}  # 🚨 mutable default!

def load_config(path=None):
    config = DEFAULT_CONFIG
    if path:
        f = open(path)  # 🚨 no context manager!
        config.update(json.load(f))
    return config
```

Ask:

- Identify ≥3 bugs.
- Rewrite it with best practices

Scoring cues: ✅ Context manager (with), immutable default (or None check), deep copy (if sharing state is intended), pathlib usage. ❌ “Just copy the dict” (misses root cause of shared state), ignoring resource leaks.

---

## 8. Design Discussion (Senior-Level Thinking)

> _“How would you structure a CLI tool that reads secrets, validates config (Pydantic), and processes files? How do you handle circular imports or testability?”_

Strong signs:

- Modular design: cli.py → config.py → processor.py.
- Dependency Injection: Passing config objects rather than importing globals.
- Lazy Imports: Moving imports inside functions only if necessary to break cycles (otherwise, refactor).
- Typing: Uses Pydantic models for config validation, not just dicts.
- Testing: Mentions mocking file I/O and using pytest fixtures for config.

---

## 🚩 Red Flags Checklist

- [ ] Thinks `asyncio` = multithreading
- [ ] Uses `except Exception:` without re-raising/logging
- [ ] says “type hints improve runtime speed”
- [ ] Can’t explain `__slots__`, GIL, or mutable defaults

- Thinks asyncio = multithreading (it’s single-threaded concurrency).
- Uses except Exception: without logging or re-raising.
- Says “type hints improve runtime speed” (they don’t; they add startup overhead).
- Can’t explain why list is mutable but tuple is immutable (and the implications for hashing).
- Still uses setup.py for new projects instead of pyproject.toml.
- Uses datetime.utcnow() (deprecated in 3.12+).
- Believes TypeGuard narrows the else branch (it doesn’t; TypeIs does).

---

## 📝 Bonus: The “Production Readiness” Litmus

> _“Your team’s Python 3.10 app breaks when upgraded to 3.12 due to `distutils` removal. How do you fix it?”_

✅ Answers:

- Use `setuptools` (not `distutils`) + `packaging.version`
- Add CI tests across multiple Python versions
- Use feature flags if needed

❌ Answers:

- “Just patch distutils locally” (technical debt)
- “Tell users to stay on 3.10” (no upgrade path)

---
