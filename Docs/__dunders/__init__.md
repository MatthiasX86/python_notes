# Python’s `__new__` and `__init__`: Object Initialization

<!--toc:start-->

- [Python’s `__new__` and `__init__`](#pythons-__new__-and-__init__)
  - [📘 Core Concepts](#-core-concepts)
  - [🛠️ Built-ins & Operations Enabled by `__init__`](#-built-ins--operations-enabled-by-__init__)
  - [⚠️ When `__init__` Is _Not_ Called or Overridden](#️-when-__init__-is-not-called-or-overridden)
  - [🧠 `__new__` vs `__init__`: When to Use Which](#-__new__-vs-__init__-when-to-use-which)
  - [🧱 Inheritance & MRO Considerations](#-inheritance--mro-considerations)
  - [⚡ Performance Notes](#⚡-performance-notes)
  - [🔗 Further Reading](#-further-reading)

<!--toc:end-->

`__init__` is the initializer — called _after_ an instance is created to set up its state. It does **not** create the object (that’s `__new__`).

---

## 📘 Core Concepts

### Order of operations

```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        print("__new__ called")
        instance = super().__new__(cls)
        return instance

    def __init__(self, x):
        print("__init__ called")
        self.x = x

obj = MyClass(5)
# Output:
# __new__ called
# __init__ called
```

| Step | Method     | Returns      | Runs?                                              |
| ---- | ---------- | ------------ | -------------------------------------------------- |
| 1    | `__new__`  | New instance | Always                                             |
| 2    | `__init__` | `None`       | Only if `__new__` returns an instance of the class |

### Key rule

> ✅ If `__new__()` returns _another_ object (e.g., cached instance), `__init__` is **skipped**.

---

## 🛠️ Built-ins & Operations Enabled by `__init__`

Implementing or _not_ overriding `__init__` affects the following:

| Built-in / Operator       | Dependency on `__init__`                                      |
| ------------------------- | ------------------------------------------------------------- |
| `class(args...)`          | Calls `__new__()` then (if instance is of class) `__init__()` |
| `super().__init__(...)`   | Required for proper initialization in inheritance             |
| `dataclasses.dataclass()` | auto-generates `__init__` (unless `__init__=False`)           |
| `@cached_property`        | May rely on `self.attr = ...` in `__init__`                   |
| `pickle.loads(obj)`       | Calls `__setstate__(...)`, but `__init__` is skipped*         |
| `copy.copy(obj)`          | Does **not** call `__init__` (copies `__dict__` only)         |

> ⚠️ `pickle.loads()` skips `__init__` — uses `__setstate__` instead. Design for unpickling.

### 🔍 Critical behavior

```python
class A:
    def __init__(self):
        self.value = 1

obj = A()
print(obj.__dict__)  # → {'value': 1}
```

- Without `__init__`, instance attributes **cannot be set** during construction
- But they _can_ still be set later (`obj.value = 2`)

---

## ⚠️ When `__init__` Is _Not_ Called or Overridden

### 1. Subclassing built-ins without `__init__`

```python
class MyList(list):
    pass

l = MyList()  # → calls list.__init__() implicitly
```

✅ Built-ins like `list`, `dict`, `tuple` provide safe defaults — you don’t _have_ to override.

### 2. Overriding `__new__` and forgetting `super().__init__()`

```python
class A:
    def __init__(self):
        self.x = 1

class B(A):
    def __new__(cls):
        return super().__new__(cls)

b = B()  # ❌ AttributeError: 'B' object has no attribute 'x'
# → Forgot to call A.__init__(b) in B’s __new__
```

### 3. Returning non-instance from `__new__`

```python
class Lazy:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance  # → existing instance

    def __init__(self):
        # ❌ Called every time — even if instance already existed!
        print("initialized")
```

### 4. Using `__slots__` with no `__init__`

```python
class Point:
    __slots__ = ["x", "y"]

p = Point()
# p.x = 1  # ❌ TypeError (x not in __slots__)
# Must set via slots *during or after* construction:
p.__setattr__("x", 1)  # Works!
```

---

## 🧠 `__new__` vs `__init__`: When to Use Which

| Scenario                       | Use `__new__`                | Use `__init__`               |
| ------------------------------ | ---------------------------- | ---------------------------- |
| Immutable types (`int`, `str`) | ✅ Yes (create new instance) | ❌ Rarely                    |
| Singleton pattern              | ✅ Yes                       | ❌ No                        |
| Custom `__new__` caching       | ✅ Yes                       | ⚠️ Only if instance is _new_ |
| Setting default values         | ❌ No                        | ✅ Yes                       |
| Validation before construction | ✅ Yes                       | ❌ Too late                  |

### ⚠️ Common mistake: Using `__init__` for validation

```python
class Age:
    def __init__(self, value):
        if value < 0: raise ValueError("Age can’t be negative")
        self._value = value

# But this fails if __new__ returns cached instance:
class AgeCached:
    _cache = {}
    def __new__(cls, value):
        if value not in cls._cache:
            cls._cache[value] = super().__new__(cls)
        return cls._cache[value]

    def __init__(self, value):
        # ❌ Runs again on cached instance → validation skipped!
        if value < 0: raise ValueError("...")
```

✅ Fix: Move validation to `__new__` or check in both.

---

## 🧱 Inheritance & MRO Considerations

### Use `super().__init__()` to preserve method resolution

```python
class A:
    def __init__(self):
        self.a = 1

class B(A):
    def __init__(self):
        super().__init__()  # → calls A.__init__()
        self.b = 2

b = B()
print(b.__dict__)  # → {'a': 1, 'b': 2}
```

### Dataclasses auto-generate `__init__`

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(1, 2)  # → __init__ auto-generated
```

- Can be overridden, but call `super().__init__()` if needed
- Fields with `init=False` must be set manually (e.g., in `__post_init__`)

---

## ⚡ Performance Notes

- Default `object.__init__` is a no-op (O(1))
- Custom `__init__` adds linear cost to construction (`O(n)` for `n` attributes)
- For high-frequency objects, prefer slots + direct assignment over property setters

---

## 🔗 Further Reading

- [Python docs: `object.__init__`](https://docs.python.org/3/reference/datamodel.html#object.__init__)
- [`object.__new__`](https://docs.python.org/3/reference/datamodel.html#object.__new__)
- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [PEP 3115 — Metaclasses](https://peps.python.org/pep-3115/) (context for `__new__`)
