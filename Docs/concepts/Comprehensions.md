# 🧠 Under the Hood: Comprehensions in Python

Comprehensions are syntactic sugar — but they’re _intelligent_ sugar, often faster and more memory-efficient than equivalent `for` loops. Under the hood, they compile to optimized bytecode, avoid extra temporary list allocations in some cases, and even handle generator expressions natively.

---

## 📋 Syntax Overview

### List Comprehension

```python
squares = [x * x for x in range(5)]  # [0, 1, 4, 9, 16]
```

### Set Comprehension

```python
evens = {x for x in range(10) if x % 2 == 0}  # {0, 2, 4, 6, 8}
```

### Dict Comprehension

```python
indices = {v: i for i, v in enumerate(["a", "b", "c"])}  # {'a': 0, 'b': 1, 'c': 2}
```

### Generator Expression (not a comprehension — but related)

```python
squares_gen = (x * x for x in range(5))  # lazy generator object
```

> 💡 Note: Only `[]`, `{}`, and `{key: value}` forms are _comprehensions_. Parentheses create a **generator expression**, not a comprehension.

---

## 🔁 Under the Hood: How They Work

### 1. Compilation to Bytecode

Python compiles comprehensions into dedicated inner functions with `MAKE_FUNCTION`, then calls them once.

Example:

```python
squares = [x * x for x in range(5)]
```

Disassembly:

```python
import dis

code = "[x * x for x in range(5)]"
dis.dis(code)
```

Key opcodes:

- `LOAD_CONST` (the range iterator)
- `GET_ITER`
- `FOR_ITER` (looping)
- `LIST_APPEND` (building the list incrementally)

Unlike manual loops, comprehensions avoid repeated attribute lookups (`list.append`) and use optimized C-level calls.

---

### 2. Scope & Variable Isolation (Python 3+)

In Python 3, comprehension variables are _scoped to the comprehension itself_ — they don’t leak into the enclosing scope.

```python
x = "global"
squares = [x * 2 for x in range(3)]
print(x)  # "global" — NOT affected by loop variable
```

Under the hood, CPython creates a new local scope for each comprehension — preventing side effects.

Compare to generator expressions:

```python
x = "global"
g = (x := x + "!" for _ in range(3))  # uses walrus operator
print(x)  # "global!!!" — side effect persists (walrus mutates outer scope)
```

---

### 3. Memory Efficiency: Comprehensions vs Loops

#### List comprehension

- Allocates list _once_ (with sizing hint)
- Uses optimized `LIST_APPEND` C-level routine

#### Manual loop with `.append()`

- Multiple attribute lookups (`lst.append`)
- Potential memory over-allocation (dynamic resizing)

Benchmark:

```python
import timeit

timeit.timeit(
    "[x*2 for x in range(10_000)]",
    number=100
)
# → ~1.8ms

timeit.timeit(
    "lst=[]\nfor x in range(10_000):\n  lst.append(x*2)",
    number=100
)
# → ~2.6ms (44% slower)
```

---

### 4. Generator Expressions: Zero-Copy Lazy Evaluation

Generator expressions (`(...)`) are _not_ executed until iterated. They compile to a single function object — no intermediate list.

```python
# Builds generator → NO memory allocated for 1M items yet
gen = (i * i for i in range(1_000_000))

# Only when consumed:
first = next(gen)  # → 0
```

Disassembly shows no `BUILD_LIST` — just `LOAD_CONST`, `MAKE_FUNCTION`, `RETURN_VALUE`.

---

## 🧪 Performance Characteristics

| Type                       | Time (10k items)  | Space   | Evaluates |
| -------------------------- | ----------------- | ------- | --------- |
| List comprehension `[...]` | ~1.8ms            | O(_n_)  | Eager     |
| Loop + `.append()`         | ~2.6ms            | O(_n_)  | Eager     |
| Generator `(...)`          | ~0.1ms (creation) | O(1)    | Lazy      |
| `map()` / `filter()`       | ~2.0ms            | O(_n_)* | Eager     |

> *`map` returns iterator (lazy), but `list(map(...))` forces eager evaluation

---

## ⚠️ Common Pitfalls

### 1. Over-nesting makes comprehension unreadable

```python
# ❌ Hard to parse:
result = [a[i][j] for i in range(n) for j in range(m)]

# ✅ Prefer explicit loop or helper:
result = []
for i in range(n):
    for j in range(m):
        result.append(a[i][j])
```

### 2. Comprehensions can leak side effects in Python <3

In Python 2, loop variables leaked into the outer scope. In Python 3, they don’t — but generator expressions _do_ capture variables by reference:

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])  # [2, 2, 2] — all capture same `i`!

# Fix: bind early
funcs = [lambda i=i: i for i in range(3)]  # [0, 1, 2]
```

### 3. Dict/list comprehensions don’t support unpacking

```python
# ❌ Invalid:
{a, b: c for a, b, c in items}

# ✅ Use tuple unpacking:
{a: c for a, b, c in items}
```

### 4. Conditional expressions in comprehensions

```python
# This:
[x if x > 0 else -x for x in range(-3, 3)]

# Is different from:
[x for x in range(-3, 3) if x > 0 else -x]  # ❌ SyntaxError (else not allowed after `if` in filter position)

# Correct:
[x if x > 0 else -x for x in range(-3, 3)]  # filtering after transformation
# OR
[x for x in range(-3, 3) if x != 0]  # true filter — no else
```

---

## 🔍 Probing Under the Hood

### 1. Check bytecode

```python
import dis

dis.dis("[x*2 for x in range(5)]")
# → Shows `LIST_APPEND`, `FOR_ITER`, etc.

dis.dis("(x*2 for x in range(5))")
# → Shows `MAKE_FUNCTION`, no LIST_BUILD
```

### 2. Inspect compiled code object

```python
code = "[x*x for x in range(5)]"
result = eval(code)
print(result.__class__.__name__)  # list

# Check if it used special opcode
dis.dis(code)
```

### 3. Benchmark memory use

```python
import sys

# Eager list comprehension
lst = [i for i in range(10_000)]
print(sys.getsizeof(lst))  # ~87,616 bytes (holds 10k refs)

# Lazy generator
gen = (i for i in range(10_000))
print(sys.getsizeof(gen))  # ~128 bytes — constant size!
```

---

## 💡 Idiomatic Patterns & Best Practices

| Pattern               | Example                               | When to use                     |
| --------------------- | ------------------------------------- | ------------------------------- |
| Simple transformation | `[f(x) for x in items]`               | Readable, fast                  |
| Filtering only        | `[x for x in items if cond(x)]`       | Prefers filter before transform |
| Dual map/filter       | `[f(x) for x in items if cond(x)]`    | Combine transform + filter      |
| Nested loops          | `[(i,j) for i in a for j in b]`       | Cartesian product               |
| Building dicts        | `{k: v for k, v in enumerate(items)}` | Index mapping                   |
| Unique elements       | `{f(x) for x in items}`               | Set deduplication               |

### Avoid

- Long comprehensions (>1 line) — use loops instead for readability
- Deeply nested comprehensions (use helper functions or multiple steps)

---

### 🔗 Further Reading

- [Python docs: Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [PEP 202 — List Comprehensions](https://peps.python.org/pep-0202/)
- [CPython source: `compile_list_comprehension`](https://github.com/python/cpython/blob/main/Python/compile.c)
- [PEP 289 — Generator Expressions](https://peps.python.org/pep-0289/)
