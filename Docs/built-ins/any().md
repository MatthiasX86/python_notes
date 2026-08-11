# Python `any()`

<!--toc:start-->

- [Python `any()`](#python-any)
  - [🧠 What is `any()`?](#🧠-what-is-any)
  - [⚙️ Syntax & Parameters](#⚙️-syntax--parameters)
  - [✅ Behavior Table](#✅-behavior-table)
  - [🧱 Truthiness in Python](#🧱-truthiness-in-python)
  - [⚡ Short-Circuit Evaluation](#⚡-short-circuit-evaluation)
  - [🛠️ Common Use Cases](#️-common-use-cases)
    - [1. Check if any condition matches](#1-check-if-any-condition-matches)
    - [2. Validate data entries](#2-validate-data-entries)
    - [3. Filter with multiple conditions](#3-filter-with-multiple-conditions)
  - [⚠️ Pitfalls](#️-pitfalls)
    - [1. Using with empty iterables](#1-using-with-empty-iterables)
  - [🔗 Related Functions](#🔗-related-functions)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

`any()` is a built-in function that returns `True` if **any element** in an iterable is truthy.

---

## 🧠 What is `any()`?

A built-in function that evaluates the truthiness of elements in an iterable and returns `True` if **at least one** element is truthy, otherwise `False`.

```python
any([True, False])   # ✅ True (at least one truthy)
any([False, False])  # ❌ False (all falsy)
```

---

## ⚙️ Syntax & Parameters

```python
any(iterable) -> bool
```

| Parameter  | Type     | Description                                                         |
| ---------- | -------- | ------------------------------------------------------------------- |
| `iterable` | iterable | Any object that can be iterated over (list, tuple, generator, etc.) |

---

## ✅ Behavior Table

| Input                       | Result  | Explanation                            |
| --------------------------- | ------- | -------------------------------------- |
| `[True, anything...]`       | `True`  | First element is truthy                |
| `[False, True, ...]`        | `True`  | Later element is truthy                |
| `[False, False]`            | `False` | All elements are falsy                 |
| `[]`                        | `False` | Empty iterable (no truthy elements)    |
| `[0, None, ""]`             | `False` | All falsy values                       |
| `[0, 1, None]`              | `True`  | Contains truthy value (`1`)            |
| Generator with truthy value | `True`  | Works with generators (short-circuits) |

---

## 🧱 Truthiness in Python

Python's truthiness rules apply:

| Value             | Truthy?   |
| ----------------- | --------- |
| `0`, `0.0`        | ❌ Falsy  |
| `""` (empty str)  | ❌ Falsy  |
| `[]`, `{}`, `()`  | ❌ Falsy  |
| `None`            | ❌ Falsy  |
| `False`           | ❌ Falsy  |
| Non-zero numbers  | ✅ Truthy |
| Non-empty strings | ✅ Truthy |
| Non-empty lists   | ✅ Truthy |
| `True`            | ✅ Truthy |

```python
any([0, "", None])     # ❌ False
any([1, 2, 3])         # ✅ True
any(["hello"])         # ✅ True (non-empty string)
```

---

## ⚡ Short-Circuit Evaluation

`any()` **short-circuits**—it stops iterating as soon as it finds the first truthy value:

```python
# Generator with short-circuit (efficient!)
any(i > 5 for i in range(1000000))
# Returns True immediately when i=6, doesn't check remaining 999,994 values
```

This makes `any()` highly efficient for large datasets.

---

## 🛠️ Common Use Cases

### 1. Check if any condition matches

```python
words = ['apple', 'banana', 'cherry']
any(w.startswith('b') for w in words)  # ✅ True
```

### 2. Validate data entries

```python
# Check if any password in list is too short
passwords = ['pass123', 'short', 'valid']
any(len(p) < 6 for p in passwords)  # ✅ True ('short' is too short)
```

### 3. Filter with multiple conditions

```python
# Check if any user meets multiple criteria
users = [
    {'name': 'Alice', 'age': 25, 'active': True},
    {'name': 'Bob', 'age': 17, 'active': False}
]

any(u['age'] >= 18 and u['active'] for u in users)  # ✅ True (Alice)
```

---

## ⚠️ Pitfalls

### 1. Using with empty iterables

```python
any([])  # ❌ False (this is expected—no elements = no truthy values)
```

This is the correct behavior. To distinguish "empty" from "all falsy":

```python
def any_nonempty(iterable):
    return bool(iterable) and any(iterable)
```

---

## 🔗 Related Functions

| Function        | Purpose                                       |
| --------------- | --------------------------------------------- |
| `all()`         | Returns `True` if **all** elements are truthy |
| `sum()`         | Sum of elements                               |
| `min()`/`max()` | Find minimum/maximum value                    |

```python
all([True, True])   # ✅ True
any([True, False])  # ✅ True

all([True, False])  # ❌ False
any([False, False]) # ❌ False
```

---

## 🔗 Further Reading

- [Python docs: `any()`](https://docs.python.org/3/library/functions.html#any)
- [Python docs: Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)
- [`all()` documentation](https://docs.python.org/3/library/functions.html#all)
