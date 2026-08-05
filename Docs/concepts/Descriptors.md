# Descriptors in Python

<!--toc:start-->

- [Descriptors in Python](#descriptors-in-python)
  - [✅ What Is a Descriptor?](#✅-what-is-a-descriptor)
  - [🔧 How Descriptors Work](#🔧-how-descriptors-work)
  - [🛠️ Common Descriptor Patterns](#🛠️-common-descriptor-patterns)
    - [1. Type-Enforcing Descriptor](#1-type-enforcing-descriptor)
    - [2. Lazy Property (Cached Computed Attribute)](#2-lazy-property-cached-computed-attribute)
    - [3. Validation Descriptor with Range Check](#3-validation-descriptor-with-range-check)
  - [🧠 Class Attributes vs. Instance Access](#🧠-class-attributes-vs-instance-access)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Data vs. Non-Data Descriptors](#1-data-vs-non-data-descriptors)
    - [2. Shadowing by Instance Attributes](#2-shadowing-by-instance-attributes)
  - [🧪 How to Check if an Object Is a Descriptor](#🧪-how-to-check-if-an-object-is-a-descriptor)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

A **descriptor** is a protocol that lets you customize how attribute access works — enabling validation, computed properties, lazy evaluation, and more—while still using clean dot notation (`obj.attr`).

---

## ✅ What Is a Descriptor?

An object is a **descriptor** if it defines one or more of the following methods:

| Method                  | Purpose              |
| ----------------------- | -------------------- |
| `__get__(obj, objtype)` | Read the attribute   |
| `__set__(obj, value)`   | Set the attribute    |
| `__delete__(obj)`       | Delete the attribute |

Key points:

- Descriptors are defined at the **class level**, not per-instance.
- They allow _behavior_ (e.g., validation, caching) to live on the class — but still be accessed like a plain attribute.
- `@property` is just a built-in descriptor in disguise!

```python
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):      # ← this is a descriptor!
        return self._name

p = Person("Alice")
print(p.name)  # → calls descriptor's __get__()
```

---

## 🔧 How Descriptors Work

When you access an attribute like `obj.attr`, Python follows this order:

1. If `attr` is a **data descriptor** (`__set__` or `__delete__` defined) in `type(obj).__dict__`, call its `__get__`.
2. Otherwise, check `obj.__dict__` for an instance attribute.
3. If not found, fall back to class attributes (including non-data descriptors).

> This means data descriptors always take precedence over instance attributes — critical for understanding why `@property` works the way it does.

---

## 🛠️ Common Descriptor Patterns

### 1. **Type-Enforcing Descriptor**

Ensures assigned values match a specific type.

```python
class TypedAttribute:
    def __init__(self, name, expected_type):
        self.name = f"_{name}"
        self.expected_type = expected_type

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name[1:]} must be {self.expected_type.__name__}")
        setattr(obj, self.name, value)

class Person:
    name = TypedAttribute("name", str)
    age = TypedAttribute("age", int)

p = Person()
p.name = "Alice"   # ✅
# p.age = 30.5     # ❌ TypeError: age must be int
```

---

### 2. **Lazy Property (Cached Computed Attribute)**

Computes a value once and caches it — ideal for expensive operations.

```python
class LazyProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.name, value)  # overrides descriptor with computed value
        return value

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @LazyProperty
    def area(self):
        import math
        return math.pi * self.radius ** 2

c = Circle(5)
print(c.area)  # "computes once"
print(c.area)  # uses cached value (no recomputation)
```

> 🔔 Note: After caching, the instance `__dict__` shadows the descriptor — this is why it only recomputes on _new instances_.

---

### 3. **Validation Descriptor with Range Check**

Ensures numeric values stay within bounds.

```python
class ValidatedRange:
    def __init__(self, name, min_val, max_val):
        self.name = f"_{name}"
        self.min = min_val
        self.max = max_val

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be numeric")
        if not self.min <= value <= self.max:
            raise ValueError(f"Value must be between {self.min} and {self.max}")
        setattr(obj, self.name, value)

class Student:
    score = ValidatedRange("score", 0, 100)

s = Student()
s.score = 85   # ✅
# s.score = 101 # ❌ ValueError
```

---

## 🧠 Class Attributes vs. Instance Access

You might wonder:

> _"If `score` is a class attribute, how does `obj.score` work?"_

- The descriptor lives on the **class**, not the instance.
- But Python automatically passes the _instance_ to `__get__(self, obj, objtype)`.
- Your descriptor uses that `obj` to store/read per-instance data (e.g., in `._score`).

```python
class Student:
    score = ValidatedRange("score", 0, 100)   # class-level descriptor

alice = Student()
alice.score = 95
# Under the hood: ValidatedRange.__set__(ValidatedRange, alice, 95)
```

So:

- ✅ Shared behavior across instances (one descriptor rules them all).
- ✅ Per-instance data stored in each instance’s `__dict__`.

---

## ⚠️ Common Pitfalls

### 1. **Data vs. Non-Data Descriptors**

| Type                    | Has `__set__`/`__delete__`? | Precedence               |
| ----------------------- | --------------------------- | ------------------------ |
| **Data descriptor**     | ✅ Yes                      | Highest                  |
| **Non-data descriptor** | ❌ No (only `__get__`)      | Lower than instance dict |

➡️ Example:

- `@property` is a _non-data descriptor_ (only has `__get__`).
- But if you define `@score.setter`, it becomes a _data descriptor_ (since the property now has `__set__`).

```python
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):           # non-data descriptor (read-only)
        return self._name

    @name.setter
    def name(self, value):    # now *data* descriptor (supports write)
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self._name = value
```

---

### 2. **Shadowing by Instance Attributes**

If your descriptor is _non-data_ (e.g., `@property` or our `LazyProperty`), assigning to the attribute on an instance will **override** it:

```python
c.area = 100   # replaces the descriptor in c.__dict__!
```

💡 To prevent accidental shadowing, prefer **data descriptors** (`__set__`) that raise errors on assignment, or use `@property` for strict read-only attributes.

---

## 🧪 How to Check If an Object Is a Descriptor

```python
def is_descriptor(obj):
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')

# Test:
from types import FunctionType

assert is_descriptor(property(lambda self: None))  # ✅
assert is_descriptor(TypedAttribute("x", int))   # ✅
assert not is_descriptor(42)                     # ❌
```

---

## 🔗 Further Reading

- [Python docs: Descriptors](https://docs.python.org/3/howto/descriptor.html)
- [Python docs: Data Model → Object model & special methods](https://docs.python.org/3/reference/datamodel.html)
- [PEP 252 — Making Types Look More Like Classes](https://peps.python.org/pep-0252/) (introduced descriptors)

---
