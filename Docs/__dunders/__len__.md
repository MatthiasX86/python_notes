# Python’s `__len__`: Length Determination

<!--toc:start-->

- [Python’s `__len__`](#pythons-__len__)
  - [📘 Core Purpose](#-core-purpose)
  - [🛠️ Built-ins & Operations Enabled by `__len__`](#-built-ins--operations-enabled-by-__len__)
  - [⚠️ When `__len__` Is _Not_ Called](#️-when-__len__-is-not-called)
  - [🧠 Key Requirements & Pitfalls](#-key-requirements--pitfalls)
  - [⚡ Performance Notes](#⚡-performance-notes)
  - [🔗 Further Reading](#-further-reading)

<!--toc:end-->

`__len__` defines the _length_ or _size_ of an object — enabling Python’s built-in length operations.

---

## 📘 Core Purpose

- **Signature**: `def __len__(self) -> int:`
- **Return value**: Must be a non-negative integer
- **Audience**: Python’s `len()` and related operations

Example:

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def __len__(self):
        return len(self._items)  # or: return self._count

s = Stack()
s.push(1)
len(s)  # → 1
```

---

## 🛠️ Built-ins & Operations Enabled by `__len__`

Implementing `__len__` unlocks these built-ins:

| Built-in / Operator | Behavior when `__len__` is defined                                       |
| ------------------- | ------------------------------------------------------------------------ |
| `len(obj)`          | Directly calls `obj.__len__()`                                           |
| `bool(obj)`         | Falls back to `not (obj == 0)` or `__len__() > 0`                        |
| `if obj:`           | Uses truthiness based on length (empty = `False`)                        |
| `for item in obj:`  | No direct dependency — but `len(obj)` used internally by some algorithms |
| `obj[0]` (indexing) | No dependency — but sequence implementations often define both           |

### 🔍 Critical details

- `bool(obj)` uses `__len__()` if no `__bool__` is defined:

  ```python
  class Bag:
      def __init__(self, items):
          self.items = items

      def __len__(self):
          return len(self.items)

  b = Bag([])
  bool(b)     # → False (len=0)
  bool(Bag([1]))  # → True
  ```

- `if obj:` is shorthand for `bool(obj)`

---

## ⚠️ When `__len__` Is _Not_ Called

| Scenario                    | Why?                                                     |
| --------------------------- | -------------------------------------------------------- |
| `len(obj)` when missing     | ❌ Raises `TypeError: object of type '...' has no len()` |
| Direct access via attribute | `obj.length` — completely unrelated to `__len__()`       |
| `str(obj)` / `repr(obj)`    | Uses `__str__`/`__repr__`, not `__len__`                 |
| Iteration (`for x in obj`)  | Depends on `__iter__`, not length                        |
| Slicing (`obj[1:3]`)        | Uses `__getitem__`, not length                           |

---

## 🧠 Key Requirements & Pitfalls

### ✅ Required rules

| Rule                           | Example                             |
| ------------------------------ | ----------------------------------- |
| Must return `int`              | ❌ `"3"` → TypeError                |
| Must be non-negative           | ❌ `-1` → ValueError (if value < 0) |
| Must be stable during lifetime | Not enforced, but expected          |

### ❌ Common pitfalls

```python
class Broken:
    def __len__(self):
        return 3.14   # ❌ TypeError: 'float' object cannot be interpreted as an integer

class NegativeLen:
    def __len__(self):
        return -1   # ❌ ValueError: __len__() should return >= 0

class Flaky:
    def __init__(self):
        self.count = 1

    def __len__(self):
        self.count += 1
        return self.count   # ❌ Dangerous: side effects & non-stability

len(Flaky())  # raises ValueError!
```

---

## ⚡ Performance Notes

- `len()` is O(1) for built-ins (`list`, `tuple`, `str`, `dict`) — stored internally
- Custom classes should aim for O(1) (`__len__ = lambda self: self._size`)
- Avoid recalculating length in `__len__` — cache if expensive

```python
class Slow:
    def __init__(self):
        self._data = list(range(10_000))

    def __len__(self):
        return sum(1 for _ in self._data)  # ❌ O(n) on every call

len(slow_obj)  # extremely slow!
```

✅ Fix:

```python
class Fast:
    def __init__(self):
        self._data = list(range(10_000))
        self._size = len(self._data)

    def __len__(self):
        return self._size  # O(1)
```

---

## 🔗 Further Reading

- [Python docs: `object.__len__`](https://docs.python.org/3/reference/datamodel.html#object.__len__)
- [PEP 241 — Metadata for Python Packages](https://peps.python.org/pep-0241/) (early `len()` usage)
- [Built-in types: `len`](https://docs.python.org/3/library/functions.html#len)
