# Python’s `@classmethod`: Class-Level Methods

<!--toc:start-->

- [Python’s `@classmethod`](#pythons-classmethod)
  - [📘 Core Purpose](#-core-purpose)
  - [🛠️ Built-ins & Operations Enabled by `@classmethod`](#-built-ins--operations-enabled-by-classmethod)
  - [🧠 How It Works Internally](#-how-it-works-internally)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Confusing with `@staticmethod`](#1-confusing-with-staticmethod)
    - [2. Inheritance and MRO](#2-inheritance-and-mro)
  - [🧱 Common Use Cases](#-common-use-cases)
    - [Factory Methods](#factory-methods)
    - [Class State Management](#class-state-management)
  - [⚡ Performance Notes](#⚡-performance-notes)
  - [🔗 Further Reading](#-further-reading)

<!--toc:end-->

`@classmethod` defines methods that receive the _class_ (not instance) as their first argument — enabling class-wide operations and factory patterns.

---

## 📘 Core Purpose

- **First argument**: Conventionally named `cls` (not `self`)
- **Signature**: `@classmethod\ndef method(cls, *args):`
- **Accesses**: Class attributes, not instance-specific data
- **Inherits properly** through subclasses (unlike static methods)

Example:

```python
class User:
    count = 0

    def __init__(self):
        User.count += 1

    @classmethod
    def total(cls):
        return cls.count  # uses actual class (not User specifically)

u1 = User()
u2 = User()

print(User.total())  # → 2
print(u1.total())    # → 2 (inherited classmethod)
```

---

## 🛠️ Built-ins & Operations Enabled by `@classmethod`

`@classmethod` itself isn’t _called_ — it **enables these behaviors**:

| Feature                  | Enabled by `@classmethod`                   |
| ------------------------ | ------------------------------------------- |
| `cls.method()`           | Class can call method without instantiation |
| Subclass inheritance     | Overrides in subclasses, not parent class   |
| Factory methods          | `User.from_file(path)` pattern              |
| Alternative constructors | `dict.fromkeys(iterable, value)`            |

### 🔍 Critical details

- Class methods are stored in the class’s `__dict__` (not instance)
- When called on a subclass (`SubClass.method()`), `cls` resolves to _subclass_, not parent class

---

## 🧠 How It Works Internally

A `@classmethod` creates a **descriptor**:

```python
class ClassMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        # Returns a bound method where first arg is cls
        return functools.partial(self.func, objtype)
```

When you call `MyClass.method()`, Python:

1. Looks up `method` → finds descriptor
2. Calls `__get__(None, MyClass)` → returns bound method with `cls=MyClass`
3. Invokes the underlying function

---

## ⚠️ Common Pitfalls

### 1. Confusing with `@staticmethod`

```python
class A:
    @classmethod
    def cls_method(cls):
        return f"Class: {cls.__name__}"

    @staticmethod
    def static_method():
        return "Static method"

print(A.cls_method())    # → "Class: A"
print(A.static_method()) # → "Static method"

class B(A):
    pass

print(B.cls_method())    # → "Class: B" ✅ (uses subclass)
print(B.static_method()) # → "Static method" ❌ (hardcoded to A)
```

### 2. Inheritance and MRO

```python
class Base:
    count = 0

    @classmethod
    def increment(cls):
        cls.count += 1

class Child(Base):
    count = 0  # separate counter

Base.increment()
print(Child.count)  # → 1? ❌ No — Base and Child have separate 'count'
```

✅ Fix: Use class attribute access (`cls.count`) — not `Base.count`.

---

## 🧱 Common Use Cases

### Factory Methods

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"])

u = User.from_dict({"name": "Alice", "email": "a@b.com"})
```

### Class State Management

```python
class Cache:
    _instances = {}

    @classmethod
    def get_instance(cls, key):
        if key not in cls._instances:
            cls._instances[key] = cls()
        return cls._instances[key]

c1 = Cache.get_instance("a")
c2 = Cache.get_instance("a")
print(c1 is c2)  # → True (shared instance)
```

---

## ⚡ Performance Notes

- Class methods have **no performance penalty** vs regular instance methods
- Storage is one descriptor per class (vs. one bound method per instance call)
- Ideal for infrequently-called class operations

---

## 🔗 Further Reading

- [Python docs: `@classmethod`](https://docs.python.org/3/library/functions.html#classmethod)
- [`type.__mro__`](https://docs.python.org/3/library/stdtypes.html#type.mro)
- [PEP 253 — Subtyping Built-in Types](https://peps.python.org/pep-0253/) (context)
