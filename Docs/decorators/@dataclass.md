# `@dataclass`

<!--toc:start-->

- [`@dataclass`](#dataclass)
  - [✅ What Is `@dataclass`?](#✅-what-is-dataclass)
  - [🧱 Basic Syntax and Usage](#🧱-basic-syntax-and-usage)
    - [Default Values](#default-values)
    - [Immutability with `frozen=True`](#immutability-with-frozentrue)
  - [🔗 How It Differs From Regular Classes](#🔗-how-it-differs-from-regular-classes)
  - [⚙️ Customizing Behavior](#⚙️-customizing-behavior)
    - [`__post_init__`](#__post_init__)
    - [Field metadata and defaults](#field-metadata-and-defaults)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Mutable default arguments](#1-mutable-default-arguments)
    - [2. Inheritance gotchas](#2-inheritance-gotchas)
  - [🧪 How to Inspect a Dataclass](#🧪-how-to-inspect-a-dataclass)
  - [⚙️ Under the Hood](#⚙️-under-the-hood)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

`@dataclass` is a decorator that automatically generates common boilerplate — like `__init__`, `__repr__`, and comparison methods — based on class field annotations.

---

## ✅ What Is `@dataclass`?

A dataclass is a regular class with added features:

- Automatic `__init__`, `__repr__`, `__eq__` (and more)
- Support for field defaults, type hints, and metadata
- Optional immutability (`frozen=True`)

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(1.5, 2.0)
print(p)           # → Point(x=1.5, y=2.0)
print(p.x)         # → 1.5
```

> 💡 A `@dataclass` is still a normal class — you can add custom methods, properties, and descriptors.

---

## 🧱 Basic Syntax and Usage

### Default Values

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    active: bool = True               # default value
    tags: list[str] = field(default_factory=list)  # mutable defaults

u1 = User("Alice")                   # → User(name='Alice', active=True, tags=[])
u2 = User("Bob", tags=["admin"])    # → User(name='Bob', active=True, tags=['admin'])
```

> 🔔 Important:
>
> - Use `default=` for immutable defaults (`int`, `str`, etc.)
> - **Always** use `default_factory=` for mutable defaults (`list`, `dict`, etc.)

---

### Immutability with `frozen=True`

```python
@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float

p = ImmutablePoint(1, 2)
# p.x = 3   # ❌ dataclasses.FrozenInstanceError
```

- Prevents modification of fields after creation.
- Makes the instance hashable (if all fields are hashable).

---

## 🔗 How It Differs From Regular Classes

| Operation                | Regular class            | `@dataclass`                         |
| ------------------------ | ------------------------ | ------------------------------------ |
| Constructor (`__init__`) | Must be written manually | Auto-generated from fields           |
| String repr (`__repr__`) | Must override            | Auto-generated                       |
| Equality (`__eq__`)      | Must define              | Auto-generated (field-based)         |
| Comparison ops           | Manual `__lt__`, etc.    | Auto-generated (if `order=True`)     |
| `asdict()`               | Manual                   | Built-in (`dataclasses.asdict(obj)`) |

Example of generated methods:

```python
from dataclasses import asdict, astuple

p = Point(1.5, 2.0)
print(asdict(p))   # → {'x': 1.5, 'y': 2.0}
print(astuple(p))  # → (1.5, 2.0)
```

---

## ⚙️ Customizing Behavior

### `__post_init__`

A hook that runs _after_ the auto-generated `__init__`.

```python
from dataclasses import dataclass

@dataclass
class Person:
    first_name: str
    last_name: str

    def __post_init__(self):
        # Validate or transform fields after init
        self.full_name = f"{self.first_name} {self.last_name}"

p = Person("Ada", "Lovelace")
print(p.full_name)  # → "Ada Lovelace"
```

> ⚠️ Don’t return a value from `__post_init__` — it’s only for side effects.

---

### Field metadata and defaults

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float = field(default=0.0, metadata={"unit": "USD"})
    tags: list[str] = field(default_factory=list)

# Access metadata:
from dataclasses import fields
print(fields(Product)[1].metadata)  # → {'unit': 'USD'}
```

---

## ⚠️ Common Pitfalls

### 1. **Mutable default arguments**

❌ Dangerous:

```python
@dataclass
class BadConfig:
    settings: dict = {}  # ← SAME DICT shared across ALL instances!
```

✅ Correct:

```python
settings: dict = field(default_factory=dict)
```

### 2. **Inheritance gotchas**

- Parent fields appear _before_ child fields in `__init__`.
- If parent has `__init__`, you must call it or override.

```python
@dataclass
class Base:
    x: int

@dataclass
class Derived(Base):
    y: int

d = Derived(x=1, y=2)  # ✅ works
```

But if you override `__init__`, dataclass _won’t_ generate one — treat as regular inheritance.

---

## 🧪 How to Inspect a Dataclass

```python
from dataclasses import fields, asdict

@dataclass
class Item:
    id: int
    name: str = "unnamed"

print(fields(Item))          # list of Field objects
# (Field(name='id',...), Field(name='name',...))

print(Item.__dataclass_fields__)  # dict view
```

---

## ⚙️ Under the Hood

The `@dataclass` decorator:

1. Scans class annotations for fields.
2. Generates `__init__`, `__repr__`, etc., based on:
   - Field order and defaults
   - `frozen` / `order` flags
3. Registers metadata in `__dataclass_fields__`.

> Behind the scenes, it uses Python’s introspection (PEP 526 annotations) to generate efficient C-like constructors.

---

## 🔗 Further Reading

- [Python docs: `dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [PEP 557 — Data Classes](https://peps.python.org/pep-0557/)
- [Real Python: Data Classes Guide](https://realpython.com/python-data-classes/)
