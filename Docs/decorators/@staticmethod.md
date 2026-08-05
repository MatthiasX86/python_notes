# `@staticmethod` in Python

<!--toc:start-->

- [`@staticmethod` in Python](#staticmethod-in-python)
  - [✅ What Is `@staticmethod`?](#✅-what-is-staticmethod)
  - [🧱 Basic Syntax and Usage](#🧱-basic-syntax-and-usage)
  - [🔗 How It Differs From `@classmethod` and Regular Methods](#🔗-how-it-differs-from-classmethod-and-regular-methods)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Misusing `staticmethod` for stateful logic](#1-misusing-staticmethod-for-stateful-logic)
    - [2. Confusing `staticmethod` with `@classmethod`](#2-confusing-staticmethod-with-classmethod)
  - [🧪 How to Verify a Static Method](#🧪-how-to-verify-a-static-method)
  - [⚙️ Under the Hood: How `@staticmethod` Works](#⚙️-under-the-hood-how-staticmethod-works)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

A `@staticmethod` is a function defined inside a class that **does not receive an implicit first argument** (`self` or `cls`). It behaves like a regular function but lives in the class’s namespace.

---

## ✅ What Is `@staticmethod`?

A static method:

- Has **no automatic access** to the instance (`self`) or class (`cls`).
- Is defined using the `@staticmethod` decorator.
- Can be called on the class _or_ an instance (though conventionally called on the class).

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

# Usage:
MathUtils.add(2, 3)   # ✅ (preferred)
m = MathUtils()
m.add(2, 3)           # ✅ also works
```

---

## 🧱 Basic Syntax and Usage

```python
class Config:
    APP_NAME = "MyApp"

    @staticmethod
    def validate_env(env):
        return env in ("dev", "staging", "prod")

# Call via class:
Config.validate_env("prod")  # → True

# Or via instance (though not recommended):
cfg = Config()
cfg.validate_env("dev")      # → True
```

### When to Use `@staticmethod`

- Utility functions related to the class conceptually (e.g., validation, formatting).
- Functions that _could_ live outside the class but benefit from logical grouping.
- Helper functions that don’t need instance/class state.

> 💡 Use `@staticmethod` _only_ when the function **truly doesn’t need access** to `self` or `cls`.  
> If you later add dependencies on class state, refactor it to a `@classmethod`.

---

## 🔗 How It Differs From `@classmethod` and Regular Methods

| Type            | First Parameter | Access to State?    | Use Case                                    |
| --------------- | --------------- | ------------------- | ------------------------------------------- |
| Regular method  | `self`          | Instance attributes | Normal behavior (`obj.method()`)            |
| `@classmethod`  | `cls`           | Class attributes    | Alternate constructors, class-wide behavior |
| `@staticmethod` | _None_          | None                | Utility functions (no state needed)         |

Example contrast:

```python
class Person:
    species = "Homo sapiens"

    def greet(self):                    # ← regular method
        return f"Hello, I'm {self.name}"

    @classmethod
    def get_species(cls):               # ← class method
        return cls.species

    @staticmethod
    def is_adult(age):
        return age >= 18                # ← no access to self/cls
```

---

## ⚠️ Common Pitfalls

### 1. **Misusing `staticmethod` for stateful logic**

❌ Don’t do this:

```python
class Counter:
    count = 0

    @staticmethod
    def increment():
        # ❌ Can't access Counter.count without hardcoding the class!
        Counter.count += 1
```

✅ Better: Use a `@classmethod` instead:

```python
    @classmethod
    def increment(cls):
        cls.count += 1
```

### 2. **Confusing `staticmethod` with `@classmethod`**

A common mistake is using `@staticmethod` when you meant to access class-level data.

```python
class Database:
    connection_count = 0

    @staticmethod
    def open_connection():
        # ❌ Can't increment connection_count!
        Database.connection_count += 1

    @classmethod
    def open_connection(cls):
        cls.connection_count += 1   # ✅ Works for subclasses too
```

---

## 🧪 How to Verify a Static Method

You can check if an attribute is a static method using `inspect`:

```python
import inspect

class Example:
    @staticmethod
    def helper(): pass

assert isinstance(inspect.getattr_static(Example, "helper"), staticmethod)
# True
```

Or simply call it and confirm it works without arguments:

```python
Example.helper()  # Should run fine (no TypeError for missing self/cls)
```

---

## ⚙️ Under the Hood: How `@staticmethod` Works

The `@staticmethod` decorator wraps your function in a descriptor that:

1. Returns the underlying function (ignoring `obj` and `objtype`)
2. Disables method binding

```python
class staticmethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        return self.func   # ← no binding to obj/cls!
```

This is why static methods **behave like plain functions** — they’re just namespaced inside the class.

---

## 🔗 Further Reading

- [Python docs: `staticmethod`](https://docs.python.org/3/library/functions.html#staticmethod)
- [Python docs: Descriptors Guide](https://docs.python.org/3/howto/descriptor.html)
- [PEP 252 — Making Types Look More Like Classes](https://peps.python.org/pep-0252/) (introduced staticmethod)
