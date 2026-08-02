# Python’s `@property`: Getters and Setters

<!--toc:start-->

- [Python’s `@property`](#pythons-property)
  - [📘 Why Use Properties?](#-why-use-properties)
  - [🛠️ Basic Syntax](#-basic-syntax)
    - [Getter Only (Read-Only)](#getter-only-read-only)
    - [With Setter (Validation)](#with-setter-validation)
    - [With Deleter](#with-deleter)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Using `__init__` for validation](#1-using-__init__-for-validation)
    - [2. Recursive property access](#2-recursive-property-access)
  - [⚡ Performance Notes](#⚡-performance-notes)

<!--toc:end-->

Properties let you define attributes with _computed_, _validated_, or _read-only_ behavior — while still using natural `obj.attr` syntax.

---

## 📘 Why Use Properties?

| Approach                     | Pros                                 | Cons                                           |
| ---------------------------- | ------------------------------------ | ---------------------------------------------- |
| Public attribute (`self.x`)  | Simple, fast                         | No validation or side effects                  |
| `@property` (`self.x`)       | Validation, caching, computed values | Slightly slower (function call)                |
| Explicit getters (`get_x()`) | Java-style control                   | Un-Pythonic (`obj.get_x()` instead of `obj.x`) |

---

## 🛠️ Basic Syntax

### Getter Only (Read-Only)

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):  # read-only: circle.area
        return 3.14 * self.radius ** 2

c = Circle(5)
print(c.area)   # → 78.5
c.area = 10     # ❌ AttributeError: property 'area' has no setter
```

### With Setter (Validation)

```python
class User:
    def __init__(self, name):
        self._name = name  # private backing field

    @property
    def name(self):       # getter
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value

u = User("Alice")
u.name = "Bob"      # ✅ Sets via setter
u.name = 123        # ❌ TypeError
```

### With Deleter

```python
class Config:
    def __init__(self):
        self._debug = False

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        if not isinstance(value, bool):
            raise TypeError("Debug must be boolean")
        self._debug = value

    @debug.deleter
    def debug(self):
        raise AttributeError("Cannot delete 'debug' attribute")
```

---

## ⚠️ Common Pitfalls

### 1. Using `__init__` for validation

```python
# ❌ No check on direct assignment later!
class Bad:
    def __init__(self, x):
        if x < 0: raise ValueError
        self._x = x

# ✅ Properties enforce validation always:
class Good:
    def __init__(self, x):
        self.x = x  # uses setter

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value < 0: raise ValueError
        self._x = value

g = Good(-1)   # ❌ ValueError during __init__
```

### 2. Recursive property access

```python
# ❌ Infinite recursion!
class Bad:
    @property
    def x(self):
        return self.x  # calls property again!

# ✅ Use underscore-prefixed backing field:
class Good:
    @property
    def x(self):
        return self._x  # ← attribute, not property

    @x.setter
    def x(self, value):
        self._x = value
```

---

## ⚡ Performance Notes

- Properties are **~10–20% slower** than direct attribute access (due to function call overhead)
- For hot paths, prefer raw attributes unless validation/computation is needed
- Caching inside properties (`functools.cached_property`) offsets cost for expensive computations

```python
from functools import cached_property

class Data:
    @cached_property
    def expensive_result(self):
        return self._compute()  # computed once, then cached

d = Data()
d.expensive_result   # computes
d.expensive_result   # uses cache (fast!)
```

---

Use `@property` when:

- You need validation or transformation
- Value is computed from other attributes
- You want read-only access
- Maintaining API stability (avoid breaking changes when adding logic later)
