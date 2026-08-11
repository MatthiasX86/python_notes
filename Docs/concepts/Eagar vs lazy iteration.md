# Eager vs. Lazy Iteration in Python

<!--toc:start-->

- [Eager vs. Lazy Iteration in Python](#eager-vs-lazy-iteration-in-python)
  - [🧠 Core Concepts](#🧠-core-concepts)
    - [What is Eager Evaluation?](#what-is-eager-evaluation)
    - [What is Lazy Evaluation?](#what-is-lazy-evaluation)
  - [📦 Built-ins: Eager vs. Lazy](#📦-built-ins-eager-vs-lazy)
  - [🔄 Conversion: Eager ↔ Lazy](#🔄-conversion-eager--lazy)
    - [Lazy → Eager: Materializing Iterators](#lazy--eager-materializing-iterators)
    - [Eager → Lazy: Creating Generators](#eager--lazy-creating-generators)
  - [⚙️ When to Choose Which](#️-when-to-choose-which)
    - [✅ Prefer Lazy When...](#✅-prefer-lazy-when)
    - [✅ Prefer Eager When...](#✅-prefer-eager-when)
  - [⚠️ Common Pitfalls & Fixes](#️-common-pitfalls--fixes)
    - [1. Exhausted iterators](#1-exhausted-iterators)
    - [2. Accidentally materializing too early](#2-accidentally-materializing-too-early)
    - [3. Length requires eager evaluation](#3-length-requires-eager-evaluation)
  - [🔍 Identity & Type Checks](#🔍-identity--type-checks)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

Understanding when Python evaluates iterators is essential for memory efficiency and performance — especially with large or unbounded data.

---

## 🧠 Core Concepts

### What is Eager Evaluation?

Data is **computed and stored all at once**, before use.

```python
# Eager: list comprehension — materializes immediately
squares = [x**2 for x in range(10)]
print(type(squares))  # ✅ <class 'list'>
print(len(squares))   # ✅ Instant (O(1))
```

- Pros: Random access, reusable, supports `len()`, indexing
- Cons: High memory usage; computes everything even if unused

---

### What is Lazy Evaluation?

Data is **computed on-demand**, one item at a time.

```python
# Lazy: generator expression — nothing computed yet
squares = (x**2 for x in range(10))
print(type(squares))  # ✅ <class 'generator'>
# print(len(squares))  # ❌ TypeError (no len on generator)

for s in squares:
    print(s)          # ✅ Only computes as needed
```

- Pros: Low memory; supports infinite streams; only computes what's used
- Cons: Single-use (exhausted after iteration), no `len()`, no indexing

---

## 📦 Built-ins: Eager vs. Lazy

| Construct                    | Type        | Eager? | Notes                       |
| ---------------------------- | ----------- | ------ | --------------------------- |
| `list(...)`, `[...]`         | `list`      | ✅ Yes | Materializes immediately    |
| `tuple(...)`, `(1,2)`        | `tuple`     | ✅ Yes | Immutable but eager         |
| `dict({...})`, `{...}`       | `dict`      | ✅ Yes | Eager key/value pairs       |
| `range(n)`                   | `range`     | ❌ No  | Lazy sequence (O(1) memory) |
| Generator expression `(...)` | `generator` | ❌ No  | One-time use                |
| `map()`, `filter()`, `zip()` | iterator    | ❌ No  | Lazy transformations        |

> 🔍 In Python 3, `range()` is lazy — a major difference from Python 2 (`xrange` was the lazy one).

---

## 🔄 Conversion: Eager ↔ Lazy

### Lazy → Eager: Materializing Iterators

Use these to _consume_ a lazy iterator and store results:

| Method                  | Result          |
| ----------------------- | --------------- |
| `list(iterator)`        | List of items   |
| `tuple(iterator)`       | Immutable tuple |
| `set(iterator)`         | Set             |
| `dict(zip(keys, vals))` | Dictionary      |

#### Examples

```python
# Generator → list (materialize)
g = (i * 2 for i in range(5))
lst = list(g)       # ✅ [0, 2, 4, 6, 8]
print(lst[2])       # ✅ Can now index

# zip() iterator → dict
keys = ['a', 'b']
vals = [1, 2]
pairs = zip(keys, vals)
d = dict(pairs)     # ✅ {'a': 1, 'b': 2}
print(d['a'])       # ✅ 1

# filter/map → list
nums = [1, 2, 3, 4]
evens = list(filter(lambda x: x % 2 == 0, nums))  # ✅ [2, 4]
squares = list(map(lambda x: x**2, nums))         # ✅ [1, 4, 9, 16]
```

#### ⚠️ Pitfall: Exhausted iterators

```python
g = (x**2 for x in range(3))
print(list(g))      # ✅ [0, 1, 4]
print(list(g))      # ❌ [] — generator exhausted!
```

✅ **Fix**: Materialize once, reuse:

```python
g = (x**2 for x in range(3))
squares = list(g)   # ✅ [0, 1, 4]
print(squares)
print(squares)      # ✅ Reusable now
```

---

### Eager → Lazy: Creating Generators

Use generator expressions or `yield`:

```python
# Generator expression (lazy)
squares_lazy = (x**2 for x in range(1_000_000))

# Generator function
def infinite_odds():
    n = 1
    while True:
        yield n
        n += 2

# Materialize only what you need:
odds = infinite_odds()
first_5 = [next(odds) for _ in range(5)]  # ✅ [1, 3, 5, 7, 9]
```

> 📌 Generators _cannot_ be reset — once exhausted, create a new one.

---

## ⚙️ When to Choose Which

### ✅ Prefer Lazy When

| Scenario                                   | Example                             |
| ------------------------------------------ | ----------------------------------- |
| Large datasets (e.g., file lines, DB rows) | `for line in open('big.txt'): ...`  |
| Infinite/unbounded streams                 | `def primes(): yield ...`           |
| Chained transformations                    | `filter(...) → map(...) → take(10)` |
| Early termination (break)                  | Find first match in large data      |

#### Example

```python
# Read 10GB file — without loading all at once!
with open("big_data.csv") as f:
    # Lazy iterator over lines — only reads what's needed
    for line in f:
        if "ERROR" in line:
            print(line)
            break  # ✅ Stops after first match
```

---

### ✅ Prefer Eager When

| Scenario                          | Example                               |
| --------------------------------- | ------------------------------------- |
| Need to reuse data multiple times | Sorting, repeated access              |
| Requires length/indexing          | `len(items)`, `items[5]`              |
| Small dataset                     | `<10k items` — memory cost negligible |

#### Example

```python
# Sorting requires all data upfront
words = ["apple", "pie", "a", "longer"]
# Can't sort a generator — need len() for merge sort
sorted_words = sorted(words)  # ✅ Materialized list

# Indexing
print(sorted_words[0])         # ✅ "apple"
```

---

## ⚠️ Common Pitfalls & Fixes

### 1. Exhausted iterators

```python
g = (i for i in range(3))
print(sum(g))       # ✅ 3
print(max(g))       # ❌ ValueError: max() arg is an empty iterable

# ✅ Fix: materialize once
g = (i for i in range(3))
nums = list(g)
print(sum(nums), max(nums))  # ✅ 3 2
```

---

### 2. Accidentally materializing too early

```python
# ❌ Wastes memory — list all items before slicing
data = [process(x) for x in range(1_000_000)]
first_10 = data[:10]

# ✅ Lazy: stop after 10 items
from itertools import islice
first_10 = list(islice((process(x) for x in range(1_000_000)), 10))
```

---

### 3. Length requires eager evaluation

```python
g = (x**2 for x in range(10))
# print(len(g))  # ❌ No len on generator

# ✅ Materialize if you *must* know length:
count = sum(1 for _ in g)    # One pass
# or:
items = list(g); count = len(items)
```

> 💡 Alternative: Use `collections.abc.Sized` subclass (e.g., `range`) if length is needed.

---

## 🔍 Identity & Type Checks

```python
from itertools import count, islice

g = (x for x in range(5))
print(isinstance(g, type([])))      # ❌ False — generator ≠ list
print(hasattr(g, "__next__"))       # ✅ True — it’s an iterator

# Check if *laziness* is needed:
def needs_lazy():
    return isinstance(data, (type(iter([])), range))

# Better: ask for permission
def safe_len(obj):
    try:
        return len(obj)
    except TypeError:
        # Must materialize to get length
        if hasattr(obj, "__iter__"):
            return sum(1 for _ in obj)
        raise
```

---
