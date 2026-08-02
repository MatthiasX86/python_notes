# Python’s `__str__`: String Representation

<!--toc:start-->

- [Python’s `__str__`](#pythons-__str__)
  - [📘 Core Purpose](#-core-purpose)
  - [🛠️ Built-ins & Operations Enabled by `__str__`](#-built-ins--operations-enabled-by-__str__)
  - [🧠 How `print()` and `str()` Work](#-how-print-and-str-work)
  - [⚠️ When `__str__` Is _Not_ Called](#️-when-__str__-is-not-called)
  - [🧱 `__str__` vs `__repr__`](#-__str__-vs-__repr__)
  - [⚡ Performance Notes](#⚡-performance-notes)
  - [🔗 Further Reading](#-further-reading)

<!--toc:end-->

`__str__` defines the "human-readable" string representation of an object — what users see when they `print()` it or convert to `str`.

---

## 📘 Core Purpose

- **Audience**: End users / operators (not developers)
- **Goal**: Concise, readable summary — _not_ necessarily evaluable
- **Fallback**: If missing, uses `__repr__`

Example:

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age} years old"

u = User("Alice", 30)
print(u)          # → Alice, 30 years old
str(u)            # → Alice, 30 years old
```

---

## 🛠️ Built-ins & Operations Enabled by `__str__`

Implementing `__str__` directly affects these built-ins:

| Built-in / Operator | Behavior when `__str__` is defined           |
| ------------------- | -------------------------------------------- |
| `print(obj)`        | Calls `__str__(obj)` (if available)          |
| `str(obj)`          | Directly calls `__str__(obj)`                |
| `format(obj)`       | Uses `__str__` (no format spec like `{obj}`) |
| `f"{obj}"`          | Uses `__str__` (same as `str(obj)`)          |
| `logging.info(obj)` | Converts to string using `__str__`           |

### 🔍 Critical detail

- `print()` _always_ calls `str(obj)` — which delegates to `__str__()`
- If `__str__` is missing, it falls back to `obj.__repr__`

---

## 🧠 How `print()` and `str()` Work

The conversion chain is deterministic:

```python
# print() → str() → __str__() → fallback to __repr__()
print(obj)  # internally does: print(str(obj))
```

You can verify:

```python
class Demo:
    def __repr__(self):
        return "Demo.__repr__()"

d = Demo()
print(d)  # → Demo.__repr__() (because no __str__)
```

Add `__str__`:

```python
    def __str__(self):
        return "Demo.__str__()"

print(d)  # → Demo.__str__()
```

---

## ⚠️ When `__str__` Is _Not_ Called

| Scenario                    | Why?                                            |
| --------------------------- | ----------------------------------------------- |
| `repr(obj)`                 | Calls `__repr__()` directly — ignores `__str__` |
| `f"{obj!r}"`                | Uses explicit `repr()` format                   |
| `list.__str__([obj])`       | Calls each item’s `repr()`, not `str()`         |
| Container display (`[obj]`) | Uses `__repr__` for contents                    |

Example:

```python
class User:
    def __str__(self):
        return "User: Alice"

    def __repr__(self):
        return f"User(name='Alice')"

u = User()

print(u)      # → User: Alice          (__str__)
repr(u)       # → User(name='Alice')   (__repr__)
[str(u)]      # → ["User: Alice"]
[repr(u)]     # → ["User(name='Alice')"]
print([u])    # → [User(name='Alice')] (list uses __repr__ for contents)
```

---

## 🧱 `__str__` vs `__repr__`

| Aspect       | `__str__`                     | `__repr__`                                  |
| ------------ | ----------------------------- | ------------------------------------------- |
| **Audience** | End users                     | Developers (debugging)                      |
| **Goal**     | Readable, friendly            | Unambiguous, precise                        |
| **Fallback** | Falls back to `__repr__`      | Falls back to `<ClassName object>`          |
| **常用场景** | `print()`, user-facing output | `repr()`, debugging, logging at debug level |

### Best practices

- ✅ `__repr__` should be as precise as possible (ideally evaluable)
- ✅ `__str__` can be looser, more contextual
- ✅ If unsure, define only `__repr__` — it works everywhere

---

## ⚡ Performance Notes

- Both methods should be _fast_ and avoid I/O (no network/file calls)
- Caching in `__repr__`/`__str__` is acceptable for complex objects
- Format strings (`f"{self.attr}"`) are fastest; `str.format()` is slightly slower

---

## 🔗 Further Reading

- [Python docs: `object.__str__`](https://docs.python.org/3/reference/datamodel.html#object.__str__)
- [`object.__repr__`](https://docs.python.org/3/reference/datamodel.html#object.__repr__)
- [PEP 3101 — Advanced String Formatting](https://peps.python.org/pep-3101/)
