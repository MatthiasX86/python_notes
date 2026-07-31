# Python’s Merge (`|`) and Update (`|=`) Operators

<!--toc:start-->

- [Python’s Merge (`|`) and Update (`|=`) Operators](#pythons-merge--and-update--operators)
  - [📘 Overview](#📘-overview)
  - [🔢 Dictionary Operators (`dict`)](#🔢-dictionary-operators-dict)
    - [Merge: `d1 | d2`](#merge-d1--d2)
    - [Update: `d1 |= d2`](#update-d1--=--d2)
    - [Key Collision Behavior](#key-collision-behavior)
  - [🧱 Set Operators (`set`, `frozenset`)](#🧱-set-operators-set-frozenset)
  - [🪞 Bitwise OR (`int`, `bool`)](#🪞-bitwise-or-int-bool)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Type mismatches](#1-type-mismatches)
    - [2. Mutability vs immutability](#2-mutability-vs-immutability)
  - [🧩 Custom Types: Supporting `|` and `|=`](#🧱-custom-types-supporting--and--)
  - [⚡ Performance Notes](#⚡-performance-notes)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

Python’s `|` and `|=` operators provide intuitive syntax for merging/updating dicts and sets, inherited from mathematics and bitwise logic.

---

## 📘 Overview

| Operator | Name | Mutates left operand? |
| -------- | ---- | --------------------- |
| `a       | b`   | **Merge** (union)     | ❌ No (returns new object) |
| `a       | = b` | **Update**            | ✅ Yes (in-place)          |

Introduced for dicts in Python 3.9 ([PEP 584]), and used historically for sets (since Python 2) and integers.

---

## 🔢 Dictionary Operators (`dict`)

### Merge: `d1 | d2`

Returns a **new dict** containing keys from both, with RHS overriding LHS on conflicts.

```python
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}

merged = d1 | d2
print(merged)   # → {'a': 1, 'b': 3, 'c': 4}
print(d1)       # → {'a': 1, 'b': 2} (unchanged!)
```

Can chain:

```python
d1 | d2 | d3    # left-associative: (d1 | d2) | d3
```

### Update: `d1 |= d2`

**Mutates `d1` in place**, adding/updating keys from `d2`.

```python
d1 = {'a': 1}
d2 = {'b': 2}

d1 |= d2
print(d1)       # → {'a': 1, 'b': 2}
# d2 unchanged
```

### Key Collision Behavior

- RHS keys **override** LHS keys on conflict:
  ```python
  {'a': 1} | {'a': 2}   # → {'a': 2}
  {'a': 1} |= {'a': 2}   # d1 becomes {'a': 2}
  ```

---

## 🧱 Set Operators (`set`, `frozenset`)

| Operator | Meaning | Example        |
| -------- | ------- | -------------- |
| `a       | b`      | Union          | `{1,2} | {2,3}`→`{1,2,3}` |
| `a       | = b`    | In-place union | `a     | = {2,3}`         |

Sets have long supported this; dicts added support in Python 3.9.

---

## 🪞 Bitwise OR (`int`, `bool`)

For integers, `|`/`|=` perform bitwise OR on binary representations.

```python
x = 5       # 0b101
y = 3       # 0b011

x | y       # → 7 (0b111)
x |= y      # x becomes 7
```

- Used for flag manipulation (e.g., permissions, mode bits)

```python
READ = 0b100   # 4
WRITE = 0b010  # 2
EXEC = 0b001   # 1

permissions = READ | EXEC      # 0b101 → read + execute
permissions |= WRITE           # now read + write + execute (0b111)
```

---

## ⚠️ Common Pitfalls

### 1. Type mismatches

```python
{'a': 1} | {2, 3}   # ❌ TypeError: unsupported operand type(s)
# (dict | set is invalid in Python 3.9+)
```

`|` works _only_ if both operands are of the same type (`dict`, `set`) or compatible numeric types.

### 2. Mutability vs immutability

```python
d1 = {'a': 1}
d2 = d1 | {'b': 2}   # d1 unchanged, new dict → d2

s1 = {1}
s1 |= {2}            # s1 mutated in place
```

⚠️ Remember: `|` is non-mutating; `|=` _always_ mutates the left operand (if it’s mutable).

---

## 🧩 Custom Types: Supporting `|` and `|=`

To support these operators, implement:

- `__or__(self, other)` → for `a | b`
- `__ior__(self, other)` → for `a |= b`

Example:

```python
class Config:
    def __init__(self, data):
        self.data = dict(data)

    def __or__(self, other):
        if not isinstance(other, Config):
            return NotImplemented
        return Config({**self.data, **other.data})

    def __ior__(self, other):
        if not isinstance(other, Config):
            return NotImplemented
        self.data.update(other.data)
        return self   # required for in-place ops!

c1 = Config({'a': 1})
c2 = Config({'b': 2})

c3 = c1 | c2     # non-mutating
print(c1.data)   # → {'a': 1} (unchanged)
c1 |= c2         # mutating
print(c1.data)   # → {'a': 1, 'b': 2}
```

> ✅ Always return `self` in `__ior__()` to enable chaining (e.g., `a |= b |= c`).

---

## ⚡ Performance Notes

- For **large dicts**: `d1 |= d2` is faster than `d1 = {**d1, **d2}` (avoids copying twice)
- `|` creates a shallow copy of the merged dict (O(_n + m_) time/space)

```python
# Timing for 10k keys:
timeit("d1 | d2", ... )      # ~0.8ms
timeit("{**d1, **d2}", ...)  # ~1.5ms
```

---

## 🔗 Further Reading

- [PEP 584 — Add Union Operators to `dict`](https://peps.python.org/pep-0584/)
- [Python docs: Mapping Types (`dict`)](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
- [Python docs: `__or__`](https://docs.python.org/3/reference/datamodel.html#object.__or__)
