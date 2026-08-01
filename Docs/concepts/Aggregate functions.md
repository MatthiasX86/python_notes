# Aggregate Functions in Python

<!--toc:start-->

- [Aggregate Functions in Python](#aggregate-functions-in-python)
  - [📊 What Is an Aggregate Function?](#-what-is-an-aggregate-function)
  - [🛠️ Built-in Aggregate Functions](#-built-in-aggregate-functions)
    - [Numeric Aggregates](#numeric-aggregates)
    - [Logical Aggregates](#logical-aggregates)
    - [Structural Aggregates](#structural-aggregates)
  - [🧩 Custom Aggregation with `functools.reduce`](#-custom-aggregation-with-functoolsreduce)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Empty sequences](#1-empty-sequences)
    - [2. Generators vs lists](#2-generators-vs-lists)
  - [🧱 Aggregation with Data Structures](#-aggregation-with-data-structures)
    - [Dictionaries](#dictionaries)
    - [Nested Structures](#nested-structures)
  - [⚡ Performance Notes](#⚡-performance-notes)
  - [🔗 Further Reading](#-further-reading)

<!--toc:end-->

Aggregate functions reduce collections to _single summary values_ — a cornerstone of data processing, statistics, and list comprehension patterns.

---

## 📊 What Is an Aggregate Function?

An **aggregate function**:

1. Accepts a sequence (list, tuple, generator, etc.)
2. Returns **one reduced value**
3. Is deterministic for the same input

Example:

```python
sum([1, 2, 3])   # → 6  (aggregates multiple values into one)
```

Contrast with **transforming functions** like `map()` or slicing — those produce _new collections_ of the same size/shape.

---

## 🛠️ Built-in Aggregate Functions

### Numeric Aggregates

| Function | Description      | Example              |
| -------- | ---------------- | -------------------- |
| `sum()`  | Sum of all items | `sum([1,2,3])` → `6` |
| `min()`  | Smallest value   | `min([1,2,3])` → `1` |
| `max()`  | Largest value    | `max([1,2,3])` → `3` |
| `len()`  | Count of items   | `len([1,2,3])` → `3` |

> 💡 All accept generators: `sum(x*x for x in range(5))`

### Logical Aggregates

| Function | Description                              |
| -------- | ---------------------------------------- |
| `any()`  | `True` if _any_ element is truthy        |
| `all()`  | `True` only if _every_ element is truthy |

Examples:

```python
any([False, True])    # → True  (like logical OR over all items)
all([True, True])     # → True
all([True, False])    # → False

# Short-circuit behavior:
any(empty_list)   # → False (no iteration)
all([])           # → True  (vacuously true)
```

### Structural Aggregates

| Function   | Description                                 |
| ---------- | ------------------------------------------- |
| `sorted()` | Returns **new sorted list** (not in-place!) |

```python
sorted([3, 1, 2])      # → [1, 2, 3]
sorted(["b", "a"], key=str.lower)  # → ["a", "b"]
```

> ⚠️ `sorted()` is an aggregate (returns one list), even though it _contains_ multiple items — it's a _reordering_, not a reduction.

---

## 🧩 Custom Aggregation with `functools.reduce`

For custom logic, use `reduce()` (from Python 2.6+):

```python
from functools import reduce

numbers = [1, 2, 3, 4]
product = reduce(lambda x, y: x * y, numbers)
# → 24
```

But prefer built-ins when possible:

```python
import math
math.prod(numbers)  # → 24 (Python ≥3.8)
```

---

## ⚠️ Common Pitfalls

### 1. Empty sequences

```python
sum([])      # → 0  (empty sum is defined as 0)
min([])      # ❌ ValueError: min() arg is an empty sequence
max([])      # ❌ ValueError
any([])      # → False (logical OR over empty = False)
all([])      # → True  (logical AND over empty = True)
```

💡 Use `default` with `min()`/`max()` via conditional:

```python
values = []
result = min(values) if values else None
```

### 2. Generators vs lists

Generators are **consumed once**:

```python
nums = (x for x in range(3))  # generator

sum(nums)   # → 3
sum(nums)   # → 0 (generator exhausted!)
```

---

## 🧱 Aggregation with Data Structures

### Dictionaries

Aggregate _values_ only:

```python
scores = {"alice": 90, "bob": 85}
total_score = sum(scores.values())     # → 175
best_student = max(scores, key=scores.get)  # → "alice"
```

Aggregate _key-value pairs_:

```python
max(scores.items(), key=lambda x: x[1])  # → ("alice", 90)
```

### Nested Structures

Flatten + aggregate:

```python
nested = [[1, 2], [3, 4]]
total = sum(sum(inner) for inner in nested)  # → 10
```

---

## ⚡ Performance Notes

| Operation             | Time Complexity         |
| --------------------- | ----------------------- |
| `sum(list)`           | O(_n_)                  |
| `min/max(list)`       | O(_n_)                  |
| `any(all)(generator)` | O(_k_) (short-circuits) |

- Built-ins are implemented in C — faster than Python loops
- Generators avoid memory overhead for large data

---

## 🔗 Further Reading

- [Python docs: `built-in functions`](https://docs.python.org/3/library/functions.html)
- [PEP 479 — `StopIteration` handling in generators](https://peps.python.org/pep-0479/) (affects `any()`/`all()`)
- [`functools.reduce()`](https://docs.python.org/3/library/functools.html#functools.reduce)
