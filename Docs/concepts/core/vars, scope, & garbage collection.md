# Python Variables, Scope, and Garbage Collection

<!--toc:start-->

- [Python Variables, Scope, and Garbage Collection](#python-variables-scope-and-garbage-collection)
  - [🧠 Variables in Python](#🧠-variables-in-python)
    - [What is a variable?](#what-is-a-variable)
    - [Assignment vs. Binding](#assignment-vs-binding)
  - [📐 Variable Scope](#📐-variable-scope)
    - [LEGB Rule](#legb-rule)
    - [`global` vs `nonlocal`](#global-vs-nonlocal)
  - [♻️ Garbage Collection](#️-garbage-collection)
    - [Reference Counting](#reference-counting)
    - [Cycle Detection](#cycle-detection)
  - [🔍 `id()`, `is`, and Identity](#🔍-id-is-and-identity)
  - [🧱 Objects, References, and Copies](#🧱-objects-references-and-copies)
    - [Mutable vs Immutable Assignment](#mutable-vs-immutable-assignment)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Mutable default arguments](#1-mutable-default-arguments)
    - [2. Capturing loop variables in closures](#2-capturing-loop-variables-in-closures)
    - [3. `==` vs `is`](#3-vs-is)
  - [⚙️ Memory Management Deep Dive](#️-memory-management-deep-dive)
    - [Heap vs Stack](#heap-vs-stack)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

Understanding how Python manages variables, scope, and memory reveals why certain patterns work—and others cause subtle bugs.

---

## 🧠 Variables in Python

### What is a variable?

A **variable** is just a _name_ (identifier) that refers to an _object_. Python variables are **references**, not containers.

```python
x = [1, 2, 3]
y = x          # y now references the *same* list object
z = [1, 2, 3]  # z references a *different* list with same value
```

```python
print(id(x), id(y))  # ✅ Same (both point to same object)
print(id(z))         # ✅ Different (new list)

y.append(4)
print(x)             # ✅ [1, 2, 3, 4] (x and y share the list)
print(z)             # ✅ [1, 2, 3]     (z is independent)
```

### Assignment vs. Binding

| Operation        | What Happens                                                                                                           | Type                |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------- |
| `x = obj`        | **Binds** name `x` to object `obj` (assignment)                                                                        | Assignment          |
| `x = y`          | Re-binds `x` to _whatever_ `y` references (assignment)                                                                 | Assignment          |
| `x += y`         | **Mutates** object in-place (if mutable), _not_ reassignment<br>→ But for immutables: `x = x + y` (re-**assignment**!) | Mixed / Conditional |
| `lst[0] = 5`     | Modifies _contents_ of list object; name `lst` unchanged                                                               | Mutation            |
| `x.append(y)`    | Mutates list in-place; no new object created                                                                           | Mutation            |
| `x[0].append(y)` | Mutates _nested_ mutable object (shallow copy still shares inner refs)                                                 | Mutation            |

#### Critical distinction

| Scenario                             | `id(x)` before | After operation                             | Type                                                 |
| ------------------------------------ | -------------- | ------------------------------------------- | ---------------------------------------------------- |
| `x = [1]`; then `x += [2]`           | ✅ Same        | ✅ Same                                     | Mutation (in-place)                                  |
| `x = 1`; then `x += 2`               | ❌ Changed     | ❌ Changed                                  | Assignment (`int` is immutable → creates new object) |
| `x = [1]`; then `x.append(2)`        | ✅ Same        | ✅ Same                                     | Mutation                                             |
| `x = [1]`; then `y = x; y.append(2)` | —              | `x` and `y` share same ID → both see change | Mutation (shared reference)                          |

#### Practical examples

```python
# ✅ In-place mutation: no assignment, same object ID
a = [1, 2]
id_a_before = id(a)
a += [3]        # extend (in-place for list)
print(id_a_before == id(a))   # ✅ True

# ❌ Assignment for immutable: new object created
b = 10
id_b_before = id(b)
b += 5          #相当于 b = b + 5 (creates new int)
print(id_b_before == id(b))   # ❌ False

# ⚠️ += behaves differently per type:
s = "hi"
id_s_before = id(s)
s += "!"        # string is immutable → re-assignment
print(id_s_before == id(s))   # ❌ False

# But for dict-like mappings with in-place ops:
d = {"a": 1}
id_d_before = id(d)
d.update({"b": 2})  # in-place → no reassignment
print(id_d_before == id(d))   # ✅ True
```

---

## 📐 Variable Scope

Python uses **lexical scoping**—inner functions can access outer scope variables, but assignment creates _new local variables_.

### LEGB Rule

Scopes are searched in this order:

| Letter        | Scope                                   |
| ------------- | --------------------------------------- |
| **L**ocal     | Inside current function                 |
| **E**nclosing | In any enclosing functions              |
| **G**lobal    | At module level                         |
| **B**uilt-in  | Predefined names (`len`, `range`, etc.) |

```python
x = "global"        # Global scope

def outer():
    y = "enclosing"  # Enclosing scope

    def inner():
        z = "local"  # Local scope
        print(x, y, z)  # ✅ Uses all three scopes

    inner()

outer()  # ✅ "global enclosing local"
```

### `global` vs `nonlocal`

```python
counter = 0  # Global

def increment_global():
    global counter   # ✅ Declare intent to modify global
    counter += 1

def outer():
    count = 0         # Enclosing

    def inner():
        nonlocal count   # ✅ Declare intent to modify enclosing
        count += 1

    inner()
    return count

increment_global()
print(counter)      # ✅ 1
print(outer())      # ✅ 1
```

⚠️ **Without `global`/`nonlocal`, assignment creates a new local variable:**

```python
x = 10

def test():
    print(x)   # ❌ UnboundLocalError
    x = 20     # Assignment makes 'x' local

test()
```

---

## ♻️ Garbage Collection

Python automatically reclaims memory using two strategies:

### Reference Counting

Each object tracks how many references point to it.

```python
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))   # ✅ 2 (one from 'a', one from getrefcount argument)

b = a
print(sys.getrefcount(a))   # ✅ 3 (now 'a' and 'b' both reference it)

del a                       # Decrements refcount
print(sys.getrefcount(b))   # ✅ 2 (now only 'b' references it)

del b                       # Refcount hits 0 → object destroyed
```

### Cycle Detection

Reference counting _can't_ handle circular references:

```python
a = []
b = []
a.append(b)
b.append(a)   # a and b reference each other → cycle

import sys
print(sys.getrefcount(a))  # ✅ 2 (even though unreachable!)
```

Python's cyclic garbage collector periodically detects and cleans up such cycles.

```python
import gc

gc.collect()  # Force cycle detection → returns number of freed objects
```

---

## 🔍 `id()`, `is`, and Identity

| Operator  | Purpose                                             |
| --------- | --------------------------------------------------- |
| `id(obj)` | Returns object's unique identifier (memory address) |
| `is`      | Checks _identity_ (same object in memory)           |
| `==`      | Checks _value equality_ (uses `__eq__`)             |

```python
a = [1, 2]
b = [1, 2]
c = a

print(a == b)   # ✅ True (same value)
print(a is b)   # ❌ False (different objects)

print(a == c)   # ✅ True
print(a is c)   # ✅ True (same object)

# Integer caching (CPython optimization)
x = 256
y = 256
print(x is y)   # ✅ True (cached small ints)

x = 257
y = 257
print(x is y)   # ❌ False (not cached)
```

---

## 🧱 Objects, References, and Copies

### Mutable vs Immutable Assignment

**Immutable objects** (int, str, tuple): Reassignment creates a new object.

```python
x = 42
id1 = id(x)
x += 1                  # Creates new int object
id2 = id(x)
print(id1 == id2)       # ❌ False
```

**Mutable objects**: Methods like `append` modify in-place (same id).

```python
lst = [1, 2]
id1 = id(lst)
lst.append(3)
id2 = id(lst)
print(id1 == id2)       # ✅ True
```

**Shadow copy**: `list.copy()` or slicing creates _shallow_ copies (new container, same elements).

```python
a = [[1], [2]]
b = a[:]      # Shallow copy

print(a is b)         # ❌ False (different lists)
print(a[0] is b[0])   # ✅ True (same inner list!)

b[0].append(99)
print(a)              # ✅ [[1, 99], [2]] — inner list mutated!
```

**Deep copy**: `copy.deepcopy()` recursively copies all nested objects.

```python
import copy

a = [[1], [2]]
c = copy.deepcopy(a)

c[0].append(99)
print(a)      # ✅ [[1], [2]] — unchanged!
```

---

## ⚠️ Common Pitfalls

### 1. Mutable default arguments

Default values are evaluated _once_ at function definition time:

```python
def add_item(item, lst=[]):   # ❌ Same list reused!
    lst.append(item)
    return lst

print(add_item(1))  # ✅ [1]
print(add_item(2))  # ❌ [1, 2] (same list!)
```

✅ **Safe pattern:**

```python
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(add_item(1))  # ✅ [1]
print(add_item(2))  # ✅ [2] (new list!)
```

### 2. Capturing loop variables in closures

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)   # ❌ All lambdas capture *same* 'i'

print([f() for f in funcs])   # ❌ [2, 2, 2] (final value of i)
```

✅ **Fix with default argument:**

```python
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)   # ✅ Captures current 'i'

print([f() for f in funcs])     # ✅ [0, 1, 2]
```

### 3. `==` vs `is`

```python
a = "hello"
b = "".join(["hel", "lo"])

print(a == b)   # ✅ True (same value)
print(a is b)   # ❌ False (different objects—interning doesn't always happen)

# For singletons, use 'is'
x = None
print(x is None)   # ✅ True (identity check—preferred over '== None')
```

---

## ⚙️ Memory Management Deep Dive

### Heap vs Stack

Python doesn't use a traditional "stack" for local variables. Instead:

| Area           | Purpose                                              |
| -------------- | ---------------------------------------------------- |
| **Heap**       | All Python objects live here (lists, dicts, etc.)    |
| **Call Frame** | Function call metadata (not actual variable storage) |

```python
def f():
    x = [1, 2, 3]   # 'x' is just a local *name* pointing to heap object
    return x

result = f()         # 'result' now points to same heap object
```

The variable `x` is just a reference stored in the function's local namespace—the actual list `[1, 2, 3]` lives on the heap.

---

## 🔗 Further Reading

- [Python docs: Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Python docs: `global` statement](https://docs.python.org/3/reference/simple_stmts.html#the-global-statement)
- [Python docs: `nonlocal` statement](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement)
- [Python docs: `gc` module](https://docs.python.org/3/library/gc.html)
- [CPython source: Reference counting](https://github.com/python/cpython/blob/main/Objects/object.c)
