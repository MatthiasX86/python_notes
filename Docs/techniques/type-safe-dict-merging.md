# TypedDict Merging: `|` vs Unpacking for Type Safety

<!--toc:start-->

- [TypedDict Merging: `|` vs Unpacking for Type Safety](#typeddict-merging-vs-unpacking-for-type-safety)
  - [🎯 The Problem: Runtime Merge ≠ Type Safety](#🎯-the-problem-runtime-merge-type-safety)
  - [🔧 Two Approaches Compared](#🔧-two-approaches-compared)
    - [❌ Approach 1: `|` Operator (Runtime Only)](#approach-1-operator-runtime-only)
    - [✅ Approach 2: Unpacking with TypedDict Inheritance (Type Safe)](#approach-2-unpacking-with-typeddict-inheritance-type-safe)
  - [🧠 Why Unpacking Works](#🧠-why-unpacking-works)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Missing required keys](#1-missing-required-keys)
    - [2. Extra fields in merge](#2-extra-fields-in-merge)
  - [🧱 When to Use Each Approach](#🧱-when-to-use-each-approach)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

When merging `TypedDict`s, the `|` operator works at runtime—but often breaks static type checking. Unpacking with inheritance is the **type-safe alternative**.

---

## 🎯 The Problem: Runtime Merge ≠ Type Safety

You might expect this to work:

```python
from typing import TypedDict

class First(TypedDict):
    first: int

class Second(TypedDict):
    second: int

class Third(TypedDict):
    first: int
    second: int

# Runtime-friendly but TYPE-UNSAFE:
first_obj: First = {"first": 1}
second_obj: Second = {"second": 2}

# ❌ Type checkers reject this!
other: Third = first_obj | second_obj
```

Error (mypy/pyright):

> `object of type 'First' is not assignable to 'Third'`

Because the type checker sees `first_obj | second_obj` as having inferred type `First`, not a combination of both.

---

## 🔧 Two Approaches Compared

### ❌ Approach 1: `|` Operator (Runtime Only)

```python
other: Third = first_obj | second_obj  # ❌ Type error
```

- ✅ Works at runtime (`{"first": 1, "second": 2}`)
- ❌ Fails static type checking (type doesn’t narrow to `Third`)
- ⚠️ Requires unsafe workarounds like `cast(Third, ...)`

### ✅ Approach 2: Unpacking with TypedDict Inheritance (Type Safe)

```python
class First(TypedDict):
    first: int

class Second(TypedDict):
    second: int

# Inherit fields from both
class Third(First, Second):  # ← key: inherits all fields
    pass

# ✅ Type-safe and works at runtime:
other: Third = {**first_obj, **second_obj}
# Dict unpacking preserves type info for type checkers!
```

- ✅ Passes static type checking
- ✅ Runtime behavior identical to `|`
- ✅ No `cast()` needed

---

## 🧠 Why Unpacking Works

Type checkers (`mypy` ≥1.1, `pyright`) understand:

- `{**d1: First, **d2: Second}` → creates a dict with all keys from both
- Since `Third` _inherits_ `First` and `Second`, the resulting dict is assignable to `Third`

The unpacking `{**d1, **d2}` is treated as a _typed merge_, not an opaque operation.

---

## ⚠️ Common Pitfalls

### 1. Missing required keys

```python
# ❌ type error: missing "second"
other: Third = {**first_obj}  # Missing required field
```

Solution: Ensure all fields are present _before_ assignment.

### 2. Extra fields in merge

```python
# ❌ Type error: extra key "extra"
other: Third = {**first_obj, **second_obj, "extra": 123}
```

TypedDicts are strict — unpacked dicts must match _exactly_ the defined keys.

---

## 🧱 When to Use Each Approach

| Scenario                                     | Recommendation                 |
| -------------------------------------------- | ------------------------------ |
| You control all `TypedDict` definitions      | ✅ Use inheritance + unpacking |
| Merging arbitrary dicts at runtime           | `                              | `, but add validation |
| Need strict type safety (e.g., in libraries) | ✅ Always prefer unpacking     |

---

## 🔗 Further Reading

- [PEP 681 — Data Class Transforms & TypedDict Merging](https://peps.python.org/pep-0681/)
- [`mypy` docs: TypedDict merging](https://mypy.readthedocs.io/en/stable/more_types.html#typeddict)
- [`pyright` issue #3892](https://github.com/microsoft/pyright/issues/3892) (on `|` operator limitations)
