# Python’s `__eq__`: Equality Comparison

<!--toc:start-->

- [Python’s `__eq__`](#pythons-__eq__)
  - [📘 Core Purpose](#-core-purpose)
  - [🛠️ Built-ins & Operations Enabled by `__eq__`](#-built-ins--operations-enabled-by-__eq__)
  - [🧠 How `==` Actually Works](#-how--actually-works)
  - [⚠️ Critical Requirement: Matching `__hash__`](#-critical-requirement-matching-__hash__)
  - [🧠 `__eq__` vs Identity (`is`)](#-__eq__-vs-identity-is)
  - [⚡ Performance Notes](#⚡-performance-notes)
  - [🔗 Further Reading](#-further-reading)

<!--toc:end-->

`__eq__` defines value-based equality — what it means for two objects to be "equal" (used by `==`).

---

## 📘 Core Purpose

- **Signature**: `def __eq__(self, other) -> bool:`
- **Return values**:
  - `True` if objects are equal
  - `False` if not equal
  - `NotImplemented` to defer comparison to the other object’s `__eq__`

Example:

```python
class Person:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.name == other.name

p1 = Person("Alice")
p2 = Person("Alice")
p3 = Person("Bob")

print(p1 == p2)  # → True
print(p1 == p3)  # → False
```

---

## 🛠️ Built-ins & Operations Enabled by `__eq__`

Implementing `__eq__` unlocks these built-ins:

| Built-in / Operator  | Behavior when `__eq__` is defined  |
| -------------------- | ---------------------------------- |
| `a == b`             | Calls `a.__eq__(b)`                |
| `a != b`             | Inverts result of `a.__eq__(b)`    |
| `x in container`     | Uses equality to find matches      |
| `container.count(x)` | Uses `__eq__` to count occurrences |
| `list.index(x)`      | Uses `__eq__` to find position     |

### 🔍 Critical details

- `a != b` is equivalent to `not (a == b)` — unless `__ne__` is explicitly defined
- Membership (`in`) uses linear search with `__eq__`:

  ```python
  [1, 2, 3].count(2)   # → 1 (uses == for comparisons)
  "a" in ["x", "y", "z"]  # → False (compares via ==)
  ```

---

## 🧠 How `==` Actually Works

Python’s comparison protocol:

1. `a == b`
2. Calls `a.__eq__(b)`
3. If that returns `NotImplemented`, tries `b.__eq__(a)`
4. If both return `NotImplemented`, falls back to identity comparison (`a is b`)

Example:

```python
class A:
    def __eq__(self, other):
        return NotImplemented  # defer to B

class B:
    def __eq__(self, other):
        return isinstance(other, A) and "same" == str(other)

a = A()
b = B()
print(a == b)  # → True (B.__eq__(a) is used)
```

---

## ⚠️ Critical Requirement: Matching `__hash__`

> 🚨 **Golden Rule**: If two objects compare equal (`a == b`), they **must** have the same hash.

Violating this breaks dictionaries and sets:

```python
class Broken:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Broken) and self.value == other.value

# ❌ No __hash__ defined! Python disables it automatically.
b1 = Broken(1)
b2 = Broken(1)

hash(b1)  # ❌ TypeError: unhashable type: 'Broken'
```

✅ Fix:

```python
class Fixed:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Fixed) and self.value == other.value

    def __hash__(self):
        return hash(self.value)

f1 = Fixed(1)
d = {f1: "value"}  # ✅ Works
```

> ⚠️ Warning: Defining `__eq__` without defining `__hash__` makes instances **unhashable** — even if the base class was hashable!

---

## 🧠 `__eq__` vs Identity (`is`)

| Operator | Checks                    | Use Case                               |
| -------- | ------------------------- | -------------------------------------- |
| `a == b` | Value equality (`__eq__`) | Do two objects represent same _value_? |
| `a is b` | Identity (same object)    | Are they the _exact same_ object?      |

```python
a = [1, 2]
b = [1, 2]
c = a

print(a == b)  # → True  (same contents)
print(a is b)  # → False (different objects)
print(a is c)  # → True  (same object)
```

- `list.sort()`, `set.add()` etc. use **identity** (`is`) internally for some operations
- But `in` uses **value equality** (`==`)

---

## ⚡ Performance Notes

- `==` is fast for built-ins (`int`, `str`, `tuple`) — optimized in C
- For custom classes:
  - Compare simplest/faster attributes first (early exit)
  - Avoid expensive computations in `__eq__`
- Do not call `self.__eq__(other)` manually — use `==`

---

## 🔗 Further Reading

- [Python docs: `object.__eq__`](https://docs.python.org/3/reference/datamodel.html#object.__eq__)
- [PEP 207 — Rich Comparisons](https://peps.python.org/pep-0207/)
- [Data classes & `__eq__`](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass) (auto-generates `__eq__`)
