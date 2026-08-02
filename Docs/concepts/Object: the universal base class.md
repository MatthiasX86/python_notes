# Python’s `object`: The Universal Base Class

<!--toc:start-->

- [Python’s `object`](#pythons-object)
  - [📘 What Is `object`?](#-what-is-object)
  - [🧠 Implicit Inheritance in Python 3](#-implicit-inheritance-in-python-3)
  - [🛠️ Built-ins Enabled by Inheriting `object`](#-built-ins-enabled-by-inheriting-object)
  - [⚠️ When You _Don’t_ Inherit `object`](#️-when-you-dont-inherit-object)
  - [🧱 The MRO Chain](#-the-mro-chain)
  - [⚡ Performance Notes](#⚡-performance-notes)
  - [🔗 Further Reading](#-further-reading)

<!--toc:end-->

In Python 3, **every class implicitly inherits from `object`** — making it the root of the entire object hierarchy.

---

## 📘 Why Everything Is an Object

### 🔑 Core design principle

> **In Python, _everything_ is an object — including classes, functions, modules, and even `object` itself.**

This means:

- Every value has a _type_ (`type(x)` returns its class)
- Every object has an _identity_ (`id(x)`, its memory address)
- Every object has _attributes_ (accessible via `.` or `getattr`)

### 🧪 Demonstrating universal objecthood

```python
# Integers are objects
print(type(42))         # → <class 'int'>
print(hasattr(42, "__add__"))  # → True (has methods!)

# Strings are objects
print("hello".upper())  # → "HELLO" (method call on object)

# Functions are objects
def f(): pass
print(callable(f))      # → True
f.desc = "my function"  # can attach attributes!

# Classes are objects (instances of `type`)
class C: pass
print(type(C))          # → <class 'type'>
print(issubclass(C, object))  # → True

# Even `object` is an object
print(type(object))     # → <class 'type'>
```

### ✅ Consequences of "everything is an object"

| Phenomenon                             | Explanation                          |
| -------------------------------------- | ------------------------------------ |
| `isinstance(42, object)` → `True`      | Integers inherit from `object`       |
| You can store functions in lists/dicts | Functions are first-class objects    |
| Decorators work                        | Taking/returning functions as values |
| `id(a) == id(b)` checks identity       | All objects have unique identity     |

---

## 📘 What Is `object`?

- **Type**: `<class 'type'>`
- **Instance**: All objects (including built-ins like `int`, `str`, `list`)
- **Role**: Provides default implementations for core dunder methods:
  - `__str__/__repr__`: Default string representations (`<ClassName object at 0x...>`)
  - `__eq__`: Identity-based equality (`a is b`)
  - `__hash__`: Identity-based hash (unless overridden)
  - `__setattr__/__getattr__/__delattr__`: Default attribute access
  - `__new__`: Object allocation

---

## 🧠 Implicit Inheritance in Python 3

### All classes inherit `object` — even without syntax

```python
# Explicit (Python 2 style — obsolete)
class OldStyle(object):
    pass

# Implicit (Python 3+)
class NewStyle:  # ← implicitly inherits object!
    pass

print(issubclass(NewStyle, object))   # → True
print(isinstance("hello", object))    # → True
```

### Why Python 3 made this implicit

| Scenario                  | Behavior                                   |
| ------------------------- | ------------------------------------------ |
| `class C:`                | → `class C(object):` internally            |
| Built-ins (`int`, `list`) | Also inherit `object` (unlike Python 2)    |
| Multiple inheritance      | `object` is the ultimate base of every MRO |

---

## 🛠️ Built-ins Enabled by Inheriting `object`

Inheriting from `object` enables:

| Feature                                 | Requires `object`?                          |
| --------------------------------------- | ------------------------------------------- |
| `super()` calls                         | ✅ Yes (fails without object)               |
| MRO calculation (`__mro__`)             | ✅ Yes                                      |
| `isinstance()` / `issubclass()`         | ✅ Yes (relies on object hierarchy)         |
| Descriptors (`__get__/__set__`)         | ✅ Yes (object defines descriptor protocol) |
| `type(obj)` → consistent representation | ✅ Yes                                      |

### Critical: `super()` fails without object

```python
# ❌ Fails — no object base class
class A:
    def __init__(self):
        super().__init__()  # AttributeError: 'super' object has no attribute '__init__'

A()
```

✅ Fix:

```python
class A(object):  # or just: class A:
    def __init__(self):
        super().__init__()  # works
```

---

## ⚠️ When You _Don’t_ Inherit `object`

### Only in Python 2 (obsolete)

- `class C:` → old-style class (no `__dict__`, limited features)
- Required explicit `class C(object):` for new features

### Modern Python (3.x+)

- **No way** to avoid inheriting `object`
- Even built-ins inherit it:

  ```python
  print(issubclass(int, object))    # → True
  print(issubclass(list, object))   # → True
  ```

---

## 🧱 The MRO Chain

Every class’s Method Resolution Order ends with `object`:

```python
class A: pass
print(A.__mro__)
# → (<class '__main__.A'>, <class 'object'>, <type>)

class B: pass
class C(A, B): pass
print(C.__mro__)
# → (<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>, <type>)
```

### Key properties

- `object` is _always_ the last base class in MRO
- Ensures consistent attribute lookup across inheritance trees
- Enables safe multiple inheritance (no ambiguous lookups)

---

## ⚡ Performance Notes

- `object` adds negligible overhead (one pointer per instance)
- Methods inherited from `object` are implemented in C and highly optimized
- No performance penalty vs. "bare" classes — inheritance is implicit

---

## 🔗 Further Reading

- [Python docs: `built-in object`](https://docs.python.org/3/library/functions.html#object)
- [Python docs: `type.__mro__`](https://docs.python.org/3/library/stdtypes.html#type.mro)
- [PEP 253 — Subtyping Built-in Types](https://peps.python.org/pep-0253/) (introduction of new-style classes)
