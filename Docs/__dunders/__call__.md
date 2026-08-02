# Python’s `__call__`: Making Objects Callable

<!--toc:start-->

- [Python’s `__call__`](#pythons-__call__)
  - [📘 Core Purpose](#-core-purpose)
  - [🛠️ Built-ins & Operations Enabled by `__call__`](#-built-ins--operations-enabled-by-__call__)
  - [🧠 How It Works Internally](#-how-it-works-internally)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Overriding `__call__` on built-ins](#1-overriding-__call__-on-built-ins)
    - [2. Inheritance and `super().__call__()`](#2-inheritance-and-supercall)
  - [🧱 Common Use Cases](#-common-use-cases)
    - [Functional Objects (Facades)](#functional-objects-facades)
    - [Caching Decorators](#caching-decorators)
    - [Stateful Callbacks](#stateful-callbacks)
  - [⚡ Performance Notes](#⚡-performance-notes)
  - [🔗 Further Reading](#-further-reading)

<!--toc:end-->

`__call__` allows instances to be called like functions — enabling objects that behave like functions with state.

---

## 📘 Core Purpose

- **Signature**: `def __call__(self, *args, **kwargs):`
- **Returns**: Any value (typically `None`, but can be anything)
- **Enables**: `obj(...)` syntax instead of `obj.method(...)`

Example:

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor

double = Multiplier(2)
print(double(5))  # → 10
```

---

## 🛠️ Built-ins & Operations Enabled by `__call__`

Implementing `__call__` unlocks these behaviors:

| Built-in / Operator | Behavior when `__call__` is defined                       |
| ------------------- | --------------------------------------------------------- |
| `obj(*args)`        | Calls `obj.__call__(*args)`                               |
| `type(obj)(...)`    | If `__new__/__init__` missing, may fallback to `__call__` |
| `callable(obj)`     | Returns `True` if `__call__` exists                       |

### 🔍 Critical details

- `callable(x)` → `True` if _any_ of these exist: `__call__`, built-in, function, method
- Only user-defined classes with `__call__` get `"is callable"` in introspection tools

```python
def f(): pass
class C:
    def __call__(self): pass

print(callable(f))      # → True
print(callable(C()))    # → True
print(callable([1,2]))  # → False (lists aren't callable)
```

---

## 🧠 How It Works Internally

When you write:

```python
obj(1, 2)
```

Python translates to:

```python
type(obj).__call__(obj, 1, 2)
```

Which invokes `obj.__call__(1, 2)` — _not_ the built-in `type(obj).__call__`.

---

## ⚠️ Common Pitfalls

### 1. Overriding `__call__` on built-ins

```python
class Int(int):
    def __call__(self):  # ❌ Fails — built-in types can't override __call__
        return "hello"

Int()()  # TypeError: 'int' object is not callable
```

Built-in types (`int`, `str`, etc.) use C-level callables — no Python `__call__` to override.

### 2. Inheritance and `super().__call__()`

```python
class Parent:
    def __call__(self):
        return "parent"

class Child(Parent):
    def __call__(self):
        # ❌ Infinite recursion!
        return self()  # calls Child.__call__ again

    def parent_call(self):
        return super().__call__()  # ✅ Calls Parent.__call__
```

---

## 🧱 Common Use Cases

### Functional Objects (Facades)

```python
class Endpoint:
    def __init__(self, host):
        self.host = host

    def __call__(self, path):
        return f"{self.host}/{path}"

api = Endpoint("https://api.example.com")
print(api("/users"))  # → https://api.example.com/users
```

### Caching Decorators

```python
class Cache:
    def __init__(self, func):
        self.func = func
        self._cache = {}

    def __call__(self, *args):
        if args in self._cache:
            return self._cache[args]
        result = self.func(*args)
        self._cache[args] = result
        return result

@Cache  # wraps function into callable object
def fib(n):
    if n < 2:
        return 1
    return fib(n-1) + fib(n-2)
```

### Stateful Callbacks

```python
class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count

tick = Counter()
print(tick())  # → 1
print(tick())  # → 2
```

---

## ⚡ Performance Notes

- `obj()` is **~15% slower** than a direct function call (due to method lookup)
- Ideal for stateful operations where you’d otherwise use globals/mutable defaults
- Use `functools.lru_cache` for caching instead of hand-written `__call__` when possible

---

## 🔗 Further Reading

- [Python docs: `object.__call__`](https://docs.python.org/3/reference/datamodel.html#object.__call__)
- [`callable()`](https://docs.python.org/3/library/functions.html#callable)
- [PEP 246 — Transforming Function Calls](https://peps.python.org/pep-0246/) (historical context)
