# Python’s `__dict__`: Instance Attribute Storage

<!--toc:start-->

- [Python’s `__dict__`](#pythons-__dict__)
  - [📘 What Is `__dict__`?](#-what-is-__dict__)
  - [📦 How It Works Internally](#-how-it-works-internally)
  - [🧱 Access and Mutability](#-access-and-mutability)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Built-in types lack `__dict__`](#1-built-in-types-lack-__dict__)
    - [2. Overriding `__dict__`](#2-overriding-__dict__)
  - [🧩 Classes with Custom Attribute Storage](#-classes-with-custom-attribute-storage)
    - [`__slots__`](#__slots__)
  - [🔍 `class.__dict__` vs `instance.__dict__`](#-classvs-instance)
  - [⚡ Performance Notes](#⚡-performance-notes)
  - [🔗 Further Reading](#-further-reading)

<!--toc:end-->

`__dict__` is the behind-the-scenes dictionary used to store an object's attributes — a fundamental part of Python’s dynamic attribute system.

---

## 📘 What Is `__dict__`?

- A special **dunder attribute** present on most user-defined class instances
- It’s a regular Python `dict` object containing the instance's attributes
- Provides dynamic attribute lookup and storage

Example:

```python
class Employee:
    pass

e = Employee()
print(e.__dict__)  # → {} (empty dict)

e.name = "Alice"
print(e.__dict__)  # → {'name': 'Alice'}
```

> ✅ Confirmed: `type(e.__dict__) is dict` → `True`

---

## 📦 How It Works Internally

When you assign an attribute:

```python
e.age = 30
```

Python translates it internally to:

```python
type(e).__dict__['age'].__set__(e, 30)  # simplified
# or more accurately:
object.__setattr__(e, 'age', 30) → updates e.__dict__
```

- Attribute access (`e.age`) first checks `__dict__`
- If not found, searches the class hierarchy (via `__mro__`)
- This enables dynamic attributes without pre-declaration

---

## 🧱 Access and Mutability

### Direct dictionary operations

```python
e.__dict__["city"] = "Paris"  # ✅ Add attribute
print(e.city)                  # → Paris

del e.__dict__["name"]        # ✅ Delete attribute
```

### Utility: Convert to dict (shallow copy)

```python
def to_dict(obj):
    return obj.__dict__.copy()
```

### ⚠️ Avoid modifying during iteration

```python
# ❌ Runtime error: dictionary changed size during iteration
for key in e.__dict__:
    if e.__dict__[key] is None:
        del e.__dict__[key]
```

---

## ⚠️ Common Pitfalls

### 1. Built-in types lack `__dict__`

```python
x = 42
hasattr(x, "__dict__")  # → False

s = "hello"
s.__dict__              # ❌ AttributeError
```

Built-in types (`int`, `str`, `list`, etc.) store data differently (in C structures), not in a user-mutable dict.

### 2. Overriding `__dict__`

You _can_ assign to `__dict__`, but it replaces the entire storage:

```python
e.__dict__ = {"new": "attrs"}  # ⚠️ Valid, but dangerous!
e.name  # ❌ AttributeError
```

---

## 🧩 Classes with Custom Attribute Storage

### `__slots__`

Defining `__slots__` **disables** the instance’s `__dict__` (and saves memory):

```python
class Person:
    __slots__ = ["name", "age"]

p = Person()
hasattr(p, "__dict__")  # → False
p.name = "Alice"        # ✅ Works (defined in slots)

# But no dynamic attributes:
p.email = "a@b.com"     # ❌ AttributeError: 'Person' has no attribute '__dict__'
```

Use cases:

- Large numbers of instances (memory savings)
- Enforcing fixed attribute sets
- Preventing accidental typo-based attribute creation

---

## 🔍 `class.__dict__` vs `instance.__dict__`

| Target              | What It Stores                                 |
| ------------------- | ---------------------------------------------- |
| `instance.__dict__` | Instance attributes (e.g., `self.name`)        |
| `class.__dict__`    | Class attributes & methods (e.g., `def foo()`) |

Example:

```python
class A:
    class_attr = 42

a = A()
a.instance_attr = 99

print(a.__dict__)      # → {'instance_attr': 99}
print(A.__dict__.keys())
# → dict_keys(['__module__', 'class_attr', '__init__', ...])
```

---

---

## 🛠️ Built-ins Enabled by `__dict__`

The following built-ins/functions **require or leverage** `obj.__dict__`:

| Built-in / Library            | Role of `__dict__`                                                         |
| ----------------------------- | -------------------------------------------------------------------------- |
| `setattr(obj, attr, val)`     | Writes directly to `obj.__dict__`                                          |
| `getattr(obj, attr, default)` | Reads from `obj.__dict__`, falls back to class hierarchy                   |
| `delattr(obj, attr)`          | Deletes from `obj.__dict__`                                                |
| `hasattr(obj, name)`          | Checks existence in `obj.__dict__` (and class)                             |
| `vars(obj)`                   | **Returns** `obj.__dict__`                                                 |
| `dir(obj)`                    | Includes keys from `obj.__dict__` (and inherited attributes)               |
| `pickle.dumps(obj)`           | Uses `obj.__dict__` for state serialization (unless custom `__getstate__`) |
| `copy.copy(obj)`              | Copies `obj.__dict__` (shallow copy of attributes)                         |
| `dataclasses.replace()`       | Replaces fields using `__dict__`                                           |
| `inspect.getmembers(obj)`     | Iterates through `obj.__dict__` for instance attributes                    |

### 🔍 Key relationships

```python
# vars() is literally an alias:
def vars(obj):
    return obj.__dict__
```

---

## ⚠️ When `__dict__` Is Missing or Overridden

### 1. Built-in types lack `__dict__`

```python
hasattr(42, "__dict__")   # → False
hasattr([1, 2], "__dict__")  # → False
```

- Designed for performance: immutable, fixed-layout C structs
- No dynamic attribute support

### 2. `__slots__` disables `__dict__`

```python
class Point:
    __slots__ = ["x", "y"]

p = Point()
hasattr(p, "__dict__")  # → False
p.z = 10                # ❌ AttributeError: 'Point' has no attribute '__dict__'
```

### 3. Overriding `__setattr__` _without_ `super()` breaks storage

```python
class Broken:
    def __setattr__(self, name, value):
        # ❌ Forgot super().__setattr__ → attribute not stored!
        print(f"Setting {name}")

b = Broken()
b.x = 1
print(b.__dict__)   # → {} (empty!)
```

### 4. `@property` doesn’t affect `__dict__`

```python
class Circle:
    def __init__(self, r):
        self._radius = r

    @property
    def area(self):
        return 3.14 * self._radius ** 2

c = Circle(5)
print(c.__dict__)   # → {'_radius': 5} (area is not stored)
```

---

## 🔍 `class.__dict__` vs `instance.__dict__`

| Target              | What It Stores                                 |
| ------------------- | ---------------------------------------------- |
| `instance.__dict__` | Instance attributes (e.g., `self.name`)        |
| `class.__dict__`    | Class attributes & methods (e.g., `def foo()`) |

Example:

```python
class A:
    class_attr = 42

a = A()
a.instance_attr = 99

print(a.__dict__)      # → {'instance_attr': 99}
print(A.__dict__.keys())
# → dict_keys(['__module__', 'class_attr', '__init__', ...])
```

---

✅ **Takeaway**: If you need dynamic attributes (`obj.x = y`), `__dict__` (or a custom equivalent) must exist — but other built-ins like `len()` or `hash()` rely on _different_ dunders entirely.

## ⚡ Performance Notes

- Access via `obj.attr` ≈ dictionary lookup — O(1) average
- Using `__slots__` reduces memory by ~35–50% per instance (no dict overhead)
- `obj.__dict__` is faster than manual attribute dicts for typical use cases

---

## 🔗 Further Reading

- [Python docs: Special Attributes → `__dict__`](https://docs.python.org/3/reference/datamodel.html#special-attributes)
- [`object.__setattr__`](https://docs.python.org/3/reference/datamodel.html#object.__setattr__)
- [PEP 276 — Previewing Python’s Attribute System](https://peps.python.org/pep-0276/) (historical context)
