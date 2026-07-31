# Python Slicing: A Comprehensive Guide (Under the Hood)

<!--toc:start-->

- [Python Slicing: A Comprehensive Guide (Under the Hood)](#python-slicing-a-comprehensive-guide-under-the-hood)
  - [📋 Table of Contents](#📋-table-of-contents)
  - [📐 Basic Syntax](#📐-basic-syntax)
  - [🧠 How Slicing Works Internally](#🧠-how-slicing-works-internally)
  - [🔢 The `slice` Object](#🔢-the-slice-object)
  - [🧮 Negative Indices & Out-of-Range Handling](#🧮-negative-indices-out-of-range-handling)
    - [Negative indices wrap around](#negative-indices-wrap-around)
    - [Slicing is **forgiving**](#slicing-is-forgiving)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Empty vs None](#1-empty-vs-none)
    - [2. Negative steps need _inclusive_ stop](#2-negative-steps-need-inclusive-stop)
    - [3. Mutating while slicing](#3-mutating-while-slicing)
  - [🧱 Slicing in Custom Classes](#🧱-slicing-in-custom-classes)
    - [✅ Correct Implementation](#correct-implementation)
    - [❌ Anti-pattern: Don’t manually unpack or use raw slice attributes](#anti-pattern-dont-manually-unpack-or-use-raw-slice-attributes)
    - [✅ Use `slice.indices()` for all custom slicing](#use-sliceindices-for-all-custom-slicing)
  - [⚡ Performance Notes](#performance-notes)
  - [🔍 Under the Hood: How Python Handles Slicing](#🔍-under-the-hood-how-python-handles-slicing)
    - [📦 Memory & Copy Behavior](#📦-memory-copy-behavior)
    - [🏗️ CPython Internals (Lists)](#🏗️-cpython-internals-lists)
    - [⏱️ Performance Characteristics](#️-performance-characteristics)
    - [🧪 Probing Under the Hood](#🧪-probing-under-the-hood)
    - [🧩 Why `x[:]` is Faster Than `list(x)`](#🧩-why-x-is-faster-than-listx)
  - [🎯 Idiomatic Patterns & Best Practices](#🎯-idiomatic-patterns-best-practices)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

Slicing is one of Python’s most elegant and powerful features—but it can be subtle. This guide covers syntax, semantics, internals, and best practices.

---

## 📋 Table of Contents

1. [Basic Syntax](#basic-syntax)
2. [How Slicing Works Internally](#how-slicing-works-internally)
3. [The `slice` Object](#the-slice-object)
4. [Negative Indices & Out-of-Range Handling](#negative-indices--out-of-range-handling)
5. [Common Pitfalls](#common-pitfalls)
6. [Slicing in Custom Classes (`__getitem__`, `__setitem__`)](#slicing-in-custom-classes)
7. [Performance Notes](#performance-notes)
8. [Idiomatic Patterns & Best Practices](#idiomatic-patterns--best-practices)

---

## 📐 Basic Syntax

```python
sequence[start:stop:step]
```

- `start`: beginning index (inclusive) — defaults to 0
- `stop`: ending index (**exclusive**)
- `step`: increment — defaults to 1 (positive) or -1 for negative steps

```python
s = [0, 1, 2, 3, 4, 5]
print(s[1:4])    # [1, 2, 3]   ← stop=4 is exclusive
print(s[:3])     # [0, 1, 2]
print(s[2:])     # [2, 3, 4, 5]
print(s[::2])    # [0, 2, 4]
print(s[::-1])   # [5, 4, 3, 2, 1, 0] (reversed)
```

---

## 🧠 How Slicing Works Internally

When you write `obj[a:b]`, Python calls:

```python
obj.__getitem__(slice(a, b, None))
```

- Not `__getslice__()` (removed in Python 3)
- `slice` is a built-in type that stores `(start, stop, step)`

You can verify:

```python
import dis

def f(x):
    return x[1:3]

dis.dis(f)
# → ... LOAD_CONST, BINARY_SUBSCR (but uses slice internally)
```

For built-ins (`list`, `str`, `tuple`), CPython optimizes slicing using specialized routines.

---

## 🔢 The `slice` Object

A slice object encapsulates the three parameters:

```python
s = slice(1, 4, 2)   # equivalent to [1:4:2]
print(s.start, s.stop, s.step)  # (1, 4, 2)

# Use .indices() to compute real bounds for a given length
seq_len = 6
print(s.indices(seq_len))   # (1, 4, 2) — handles negative/overflow cleanly

# More examples:
print(slice(None, None, -1).indices(5))  # (4, -1, -1) → full reverse: [4,3,2,1,0]
print(slice(-3, None, None).indices(5))  # (2, 5, 1) → last 3 elements
```

`slice.indices(n)` is the _only safe way_ to convert a slice to concrete indices for length `n`.

---

## 🧮 Negative Indices & Out-of-Range Handling

### Negative indices wrap around

```python
s = [0,1,2,3,4]
print(s[-1])    # 4
print(s[-2:])   # [3, 4]
```

### Slicing is **forgiving**

- Overshoots `stop`? → clipped to sequence length
- Negative `start`? → converted using `len + start`
- Step=0? → raises `ValueError`

| Expression    | Result          | Why                         |
| ------------- | --------------- | --------------------------- |
| `s[100:200]`  | `[]`            | start beyond length → empty |
| `s[-100:-50]` | `[]`            | both negative → clamp to 0  |
| `s[2:100]`    | `[2,3,4]`       | stop clipped to `len(s)`    |
| `s[1:-1:0]`   | ❌ `ValueError` | step ≠ 0 required           |

```python
s[1:100] == s[1:]   # True (clipped stop behaves like end)
```

---

## ⚠️ Common Pitfalls

### 1. Empty vs None

```python
a = []
b = a[0:0]   # b is [] (empty slice) — NOT None!
b == []      # True
b is a       # False (always returns new object for lists)
```

### 2. Negative steps need _inclusive_ stop

```python
s = [0,1,2,3,4]
print(s[4:1:-1])  # [4, 3, 2] ← stop=1 is *exclusive*
print(s[4::-1])   # [4, 3, 2, 1, 0]
```

### 3. Mutating while slicing

```python
lst = [1,2,3]
lst[1:2] = [9,8,7]  # replaces index 1 only → [1,9,8,7]
# BUT:
lst = [1,2,3]
lst[1:3] = [9]       # replaces 2 & 3 → [1,9]
```

Assignment slices mutate **in-place** (for mutable sequences).

---

## 🧱 Slicing in Custom Classes

To support slicing, implement `__getitem__` (and optionally `__setitem__`):

```python
class Vector:
    def __init__(self, data):
        self._data = list(data)

    def __getitem__(self, index):
        if isinstance(index, slice):
            # Convert slice to concrete indices
            indices = index.indices(len(self._data))
            return Vector(self._data[slice(*indices)])
        else:
            return self._data[index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            indices = index.indices(len(self._data))
            self._data[slice(*indices)] = value
        else:
            self._data[index] = value

v = Vector([10,20,30,40])
print(v[1:3])      # Vector([20, 30])
v[1:3] = [99, 88]
print(v._data)     # [10, 99, 88, 40]
```

Note: You _must_ pass `slice(*indices)` to the underlying sequence—don’t manually unpack.

To support slicing, implement `__getitem__` (and optionally `__setitem__`) using the `slice.indices()` method for robust conversion of abstract slices to concrete indices.

### ✅ Correct Implementation

```python
class Vector:
    def __init__(self, data):
        self._data = list(data)

    def __getitem__(self, index):
        if isinstance(index, slice):
            # Convert abstract slice to concrete indices (handles negatives/None/out-of-range)
            indices = index.indices(len(self._data))
            return Vector(self._data[slice(*indices)])
        else:
            return self._data[index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            indices = index.indices(len(self._data))
            self._data[slice(*indices)] = value
        else:
            self._data[index] = value

v = Vector([10, 20, 30, 40])
print(v[1:3])      # Vector([20, 30])
v[1:3] = [99, 88]
print(v._data)     # [10, 99, 88, 40]
```

> ✅ **Key insight**: `slice.indices(n)` safely resolves `None`, negatives, and out-of-range values — _never_ use raw `start:stop:step` attributes.

---

### ❌ Anti-pattern: Don’t manually unpack or use raw slice attributes

```python
class BrokenVector:
    def __init__(self, data):
        self._data = list(data)

    def __getitem__(self, index):
        if isinstance(index, slice):
            # ❌ Fails when start/stop/step is None (e.g., s[:2], s[::2])
            start, stop, step = index.start, index.stop, index.step
            return BrokenVector([self._data[i] for i in range(start, stop, step)])
        else:
            return self._data[index]

# Breaks on common cases:
v = BrokenVector([1, 2, 3])
print(v[:2])      # ❌ TypeError: 'NoneType' object cannot be interpreted as an integer
print(v[::2])     # ❌ Same error (step=None)
```

`slice.start/stop/step` may be `None` or invalid — always normalize via `.indices(len())`.

```python
# Another failure case:
v2 = BrokenVector([0, 1, 2])
print(v2[3:0:-1])  # start=3 (out-of-range), stop=0, step=-1 → range(3, 0, -1) = (3,2,1)
# But slice semantics should clamp start to len-1 → (2,0,-1) = [2,1]
# Only .indices() handles this correctly:
print(slice(3, 0, -1).indices(3))  # (2, 0, -1)
```

---

### ✅ Use `slice.indices()` for all custom slicing

This is the _only_ reliable way to:

- Convert `None` → proper bounds
- Normalize negative indices
- Clamp out-of-range values
- Prevent subtle off-by-one errors

```python
start, stop, step = slice_obj.indices(len(sequence))
# → Safe, concrete indices guaranteed to be in [0, len(sequence)]
```

---

## ⚡ Performance Notes

- Slicing creates **shallow copies** for lists/strings (O(k) time, where k = slice length)
- For large slices, prefer generators:

  ```python
  # Instead of big_slice = data[1000:2000]
  for item in islice(data, 1000, 2000): ...
  ```

- `numpy` slices are _views_ (no copy), but Python lists/tuples/str always copy

---

## 🔍 Under the Hood: How Python Handles Slicing

### 📦 Memory & Copy Behavior

| Type        | `seq[a:b]` behavior                                                               | Memory implication                      |
| ----------- | --------------------------------------------------------------------------------- | --------------------------------------- |
| `list`      | **Shallow copy** — allocates new list, copies _references_ to elements            | O(_k_) space (where _k_ = slice length) |
| `tuple`     | **Shallow copy** — new tuple object, but same element references                  | Same as list                            |
| `str`       | **Shallow copy** — new string object (strings are immutable, so no aliasing risk) | O(_k_) space                            |
| `bytearray` | **Shallow copy** — new mutable buffer                                             | O(_k_) space                            |

```python
a = [1, 2, 3]
b = a[0:2]

print(b is a)        # False — different objects
print(id(a), id(b))  # Different memory addresses

b[0] = 99
print(a)             # [1, 2, 3] — unchanged (deep independence)
```

> 💡 Why shallow copy? Because Python copies the _container_, not the elements inside.

---

### 🏗️ CPython Internals (Lists)

When you slice a list, CPython calls [`list_getslice`](https://github.com/python/cpython/blob/main/Objects/listobject.c#L2879), which:

1. Normalizes `start`/`stop` using the same logic as `.indices()`
2. Computes new length (`max(0, (stop - start + step - sign(step)) // step)`)
3. Allocates a _new_ list of exact size
4. Copies elements in chunks (using `memcpy`-style loops for efficiency)

No per-element Python-level calls — purely C-level optimization.

---

### ⏱️ Performance Characteristics

For a list of length _n_ and slice length _k_:

| Operation                     | Time Complexity              | Space  |
| ----------------------------- | ---------------------------- | ------ |
| `lst[a:b]`                    | O(_k_)                       | O(_k_) |
| `lst[i:j:k]`                  | O(_k_)                       | O(_k_) |
| `lst[::-1]`                   | O(_n_) (reverse entire list) | O(_n_) |
| `lst[:10]` on 1M-element list | O(10) — cheap!               | O(10)  |

💡 Contrary to intuition: slicing **does not** involve iterating through skipped elements — only copies the selected items.

---

### 🧪 Probing Under the Hood

```python
import sys, gc

a = list(range(10_000))
b = a[5_000:6_000]  # slice of size 1000

print(sys.getsizeof(a))    # e.g., 8256 bytes (holds ~10k refs)
print(sys.getsizeof(b))    # e.g., 8256 bytes (holds exactly 1000 refs)

# Check reference counts:
import ctypes
def refcount(obj):
    return ctypes.c_long.from_address(id(obj)).value

print(refcount(a[10]))     # Original refcount
print(refcount(b[0]))      # Same object → same count +1 (from slice)
gc.collect()
print(refcount(a[10]))     # Still same — no new allocation of the *value*
```

---

### 🧩 Why `x[:]` is Faster Than `list(x)`

```python
import timeit

# For a list of 1M elements:
timeit.timeit("x[:]", setup="x=list(range(1_000_000))", number=100)
# → ~2.3ms per operation

timeit.timeit("list(x)", setup="x=list(range(1_000_000))", number=100)
# → ~4.8ms per operation
```

Why?

- `x[:]` → specialized C-level copy (`list_copy`)
- `list(x)` → generic constructor + iteration overhead

The same applies to `str` and `tuple`.

---

## 🎯 Idiomatic Patterns & Best Practices

| Pattern                | Example                 | Use Case                             |
| ---------------------- | ----------------------- | ------------------------------------ |
| Get last `n` items     | `seq[-n:]`              | “tail” of sequence                   |
| Remove last item       | `seq[:-1]`              | Immutable subset                     |
| Copy whole sequence    | `seq[:]`                | Shallow copy (faster than `.copy()`) |
| Reverse copy           | `seq[::-1]`             | Fast reversal (C-optimized)          |
| Skip every other item  | `seq[::2]`              | Interleaved data access              |
| Replace slice in-place | `lst[i:j:k] = iterable` | Batch assignment                     |

**Anti-pattern:**

```python
# ❌ Creating new lists just to drop elements
data[1:-1]  # If you only need iteration, use islice(data, 1, len(data)-1)
```

**Pro tip:**

```python
# Safe reverse — works even if len=0 or 1
if seq:
    reversed_seq = seq[::-1]
```

---

## 🔗 Further Reading

- [Python docs: `slice`](https://docs.python.org/3/library/functions.html#slice)
- [Python docs: `__getitem__`](https://docs.python.org/3/reference/datamodel.html#object.__getitem__)
- [PEP 472 — Support for slicing with steps](https://peps.python.org/pep-0472/) (for custom types)
- [CPython source: `list_subscript`](https://github.com/python/cpython/blob/main/Objects/listobject.c#L2879)
