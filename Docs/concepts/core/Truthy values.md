# Python Truthy Values

<!--toc:start-->

- [Python Truthy Values](#python-truthy-values)
  - [🧠 Falsity vs. Truthiness](#🧠-falsity-vs-truthiness)
    - [The Falsy Built-ins](#the-falsy-built-ins)
  - [🔍 Evaluation Contexts](#🔍-evaluation-contexts)
    - [`if`, `while`, `and`, `or`, `not`](#if-while-and-or-not)
    - [`bool()` and the `__bool__` Protocol](#bool-and-the-__bool__-protocol)
  - [🧱 Built-in Truthiness by Type](#🧱-built-in-truthiness-by-type)
    - [Collections](#collections)
    - [Numbers & Strings](#numbers--strings)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Empty collections ≠ `False`](#1-empty-collections--false)
    - [2. NumPy/`pandas` arrays behave unexpectedly](#2-numpypandas-arrays-behave-unexpectedly)
    - [3. String `"0"` is truthy](#3-string-0-is-truthy)
  - [⚙️ Custom Objects & Truthiness](#️-custom-objects--truthiness)
    - [`__bool__` vs `__len__`](#__bool__-vs-__len__)
  - [🔍 Identity Checks vs. Truthiness](#🔍-identity-checks-vs-truthiness)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

Python’s truthiness rules govern how _any_ value is interpreted in a boolean context — critical for writing correct conditionals and avoiding subtle bugs.

---

## 🧠 Falsity vs. Truthiness

Python is **not** C-style (where `0` and empty pointer = falsy). Instead, it defines:

- **Falsy**: Values explicitly defined as false in boolean context
- **Truthy**: _Everything else_ — including non-empty objects, custom instances

```python
# Explicitly falsy values (only these evaluate to False)
falsy_values = [
    None,           # The null object
    False,          # Boolean false
    0,              # Zero (int, float, complex)
    0.0,
    0j,
    "",             # Empty string
    [],             # Empty list
    {},             # Empty dict
    set(),          # Empty set
    range(0)        # Empty range
]

# All others are truthy — even many "empty"-looking objects!
truthy_values = [
    [0],            # Non-empty list (contains 0)
    "False",        # Non-empty string
    -1,             # Negative numbers (except 0)
    [None],         # List containing None
]
```

### The Falsy Built-ins

| Value               | Type       | Why it’s falsy              |
| ------------------- | ---------- | --------------------------- |
| `None`              | `NoneType` | Represents absence of value |
| `False`             | `bool`     | Boolean false               |
| `0`, `0.0`, `0j`    | Number     | Numeric zero                |
| `""`                | `str`      | Zero-length string          |
| `[]`, `{}`, `set()` | Collection | Zero-length container       |
| `range(0)`          | `range`    | Empty sequence              |

> ✅ **Key insight**: Falsiness is _binary_ and _explicitly defined_ — nothing else is falsy.

---

## 🔍 Evaluation Contexts

### `if`, `while`, `and`, `or`, `not`

These contexts implicitly call `bool()`:

```python
# All these trigger truthiness evaluation:
if value:         # bool(value) is called
    ...
while item:       # same as "while bool(item):"
    ...

# Logical operators also use truthiness:
a and b           # Returns a if falsy, else b
a or b            # Returns a if truthy, else b
not x             # Inverts truthiness of x
```

Example:

```python
items = []        # Empty list → falsy

if items:         # Equivalent to: if bool(items):
    print("Has items")
else:
    print("Empty")  # ✅ Runs this

# Logical operator behavior
print([] or "fallback")    # ✅ "fallback"
print({} and [1, 2])       # ❌ {} (falsy → returns first operand)
print(not [])              # ✅ True
```

---

### `bool()` and the `__bool__` Protocol

Python’s `bool(x)` does two things:

1. Calls `x.__bool__()` if defined
2. Falls back to `len(x) == 0` for containers (if `__bool__` missing)

```python
class Container:
    def __init__(self, items):
        self.items = list(items)

    def __len__(self):
        print("Called len()")
        return len(self.items)

c = Container([1, 2])
print(bool(c))   # ✅ "Called len()" → True (len = 2)
```

But:

```python
class Zeroish:
    def __bool__(self):
        return False

z = Zeroish()
print(bool(z))   # ✅ False (explicit __bool__ overrides len)
```

---

## 🧱 Built-in Truthiness by Type

### Collections

| Container       | Falsy? | Why                                |
| --------------- | ------ | ---------------------------------- |
| `[]`            | ✅ Yes | Empty list                         |
| `[0]`           | ❌ No  | Contains one element (`0`)         |
| `{}`            | ✅ Yes | Empty dict                         |
| `{"": 0}`       | ❌ No  | Has one key (even if empty string) |
| `set()`         | ✅ Yes | Empty set                          |
| `frozenset({})` | ✅ Yes | Same as above                      |

```python
print(bool([None]))   # ✅ True (non-empty list)
print(bool({"a": 0})) # ✅ True (key "a" exists, even if value=0)
print(bool({None}))   # ✅ True (set with one element: None)
```

### Numbers & Strings

| Type      | Falsy?     | Examples                         |
| --------- | ---------- | -------------------------------- |
| `int`     | Only `0`   | `-1`, `1`, `256` → truthy        |
| `float`   | Only `0.0` | `-0.1`, `0.0` → falsy            |
| `complex` | Only `0j`  | `1+2j`, `0+1j` → truthy          |
| `str`     | Only `""`  | `"0"`, `"False"`, `" "` → truthy |

> 📌 **Watch out**: String `"0"` is _truthy_ because it’s non-empty — not numeric!

```python
# Common gotcha:
password = "0"
if password:           # ✅ Runs (truthy!)
    print("Has password")
else:
    print("No password")  # Never runs

# For explicit numeric zero check:
if int(password) == 0:  # ✅ Better for validation
    print("Zero password")
```

---

## ⚠️ Common Pitfalls

### 1. Empty collections ≠ `False`

```python
def get_items():
    return []   # or None?

# ❌ Bad: can't distinguish "empty list" from "no result"
if get_items():
    process(items)
else:
    handle_error()  # Runs for [] — possibly wrong!
```

✅ **Safe pattern**:

```python
items = get_items()
if items is None:          # Explicit "no result"
    handle_error()
elif not items:            # Empty but valid
    print("No items found")
```

---

### 2. NumPy/`pandas` arrays behave unexpectedly

```python
import numpy as np

arr = np.array([])
# bool(arr) → ❌ ValueError: The truth value of an array is ambiguous

# ✅ Use explicit checks:
if arr.size == 0:     # → True
    ...
# Or: if len(arr) > 0:
```

Same for `pandas.DataFrame`: use `.empty`, `.any()`, or `.all()`.

---

### 3. String `"0"` is truthy

```python
user_input = input("Enter a number: ")  # User types "0"
if user_input:
    print("You entered something")     # ✅ Runs!
else:
    print("No input")
```

✅ **Fix**:

```python
if user_input and user_input != "0":  # Or use try/except + int()
    ...
```

---

## ⚙️ Custom Objects & Truthiness

### `__bool__` vs `__len__`

Python checks for truthiness in this order:

1. If object defines `__bool__()`, call it
2. Else, if it defines `__len__()`, return `False` if `__len__() == 0`
3. Else → always truthy (non-`None`, non-zero objects)

```python
class AlwaysFalse:
    def __bool__(self):
        return False

class EmptyContainer:
    def __len__(self):
        return 0

print(bool(AlwaysFalse()))       # ✅ False (via __bool__)
print(bool(EmptyContainer()))    # ✅ False (via __len__)

class NormalObj:
    pass

print(bool(NormalObj()))         # ✅ True (default: non-None objects are truthy)
```

---

## 🔍 Identity Checks vs. Truthiness

**Never** use `is True`/`is False` — those check _identity_, not truthiness!

```python
def is_empty(lst):
    return lst == []  # ✅ Safe comparison

print(is_empty([]))      # ✅ True
print([].__class__)      # <class 'list'> — not a singleton!

# ❌ Dangerous:
print([1] is True)       # ❌ False (always — lists aren't booleans)
print(bool([1]) is True) # ❌ Also False! (bool() returns *object* True)
```

✅ **Correct**:

```python
if value:               # Truthiness check — preferred
    ...
if value is True:       # Identity check — only when expecting *actual* True/False
    ...
```

> 📌 Only use `is` with `None`, `True`, `False` — and only to check _identity_, not truthiness.

---

## 🔗 Further Reading

- [Python docs: Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)
- [Python docs: Boolean Operations](https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not)
- [PEP 326 — Reason for `__bool__`](https://peps.python.org/pep-0326/)
- [CPython source: `PyObject_Bool()`](https://github.com/python/cpython/blob/main/Objects/boolobject.c)
