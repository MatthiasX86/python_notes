# Python Packing and Unpacking

<!--toc:start-->

- [Python Packing and Unpacking](#python-packing-and-unpacking)
  - [🧱 What Are Packing and Unacking?](#🧱-what-are-packing-and-unacking)
    - [Packing](#packing)
    - [Unpacking](#unpacking)
  - [📦 Packing: Collecting Values into a Container](#📦-packing-collecting-values-into-a-container)
    - [Tuple packing](#tuple-packing)
    - [List packing](#list-packing)
  - [📦 Unpacking: Extracting Values from a Container](#📦-unpacking-extracting-values-from-a-container)
    - [Basic unpacking](#basic-unpacking)
    - [Unpacking in function calls (`*`)](#unpacking-in-function-calls)
    - [Unpacking in assignments](#unpacking-in-assignments)
  - [✨ The `*` Operator: Flexible Unpacking](#the-operator-flexible-unpacking)
    - [The "splat" operator (`*`) for variable-length unpacking](#the-splat-operator-for-variable-length-unpacking)
  - [✨ The `**` Operator: Dictionary Unpacking](#the-operator-dictionary-unpacking)
    - [Dictionary unpacking in function calls (`**`)](#dictionary-unpacking-in-function-calls)
    - [Dictionary unpacking in literals](#dictionary-unpacking-in-literals)
  - [🧱 Packing and Unpacking with Functions](#🧱-packing-and-unpacking-with-functions)
    - [Variadic parameters (`*args`, `**kwargs`)](#variadic-parameters-args-kwargs)
    - [Passing arguments with `*` and `**`](#passing-arguments-with-and)
  - [🔄 Unpacking in Loops](#🔄-unpacking-in-loops)
    - [Nested unpacking](#nested-unpacking)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Starred assignment must have at least one element](#1-starred-assignment-must-have-at-least-one-element)
    - [2. Unpacking mismatched lengths](#2-unpacking-mismatched-lengths)
    - [3. Unpacking sets/dicts](#3-unpacking-setsdicts)
  - [⚙️ Under the Hood: How Unpacking Works](#️-under-the-hood-how-unpacking-works)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

Packing and unpacking are fundamental operations that let you collect values into containers (**packing**) or extract values from them (**unpacking**).

---

## 🧱 What Are Packing and Unacking?

### Packing

**Packing** is creating a tuple/list by placing multiple values next to each other.

```python
# Tuple packing
t = 1, 2, 3
print(t)      # ✅ (1, 2, 3)

# List packing
l = [4, 5, 6]
print(l)      # ✅ [4, 5, 6]
```

### Unpacking

**Unpacking** is extracting individual values from a container into separate variables.

```python
t = (1, 2, 3)
a, b, c = t     # Unpacking
print(a, b, c)  # ✅ 1 2 3
```

---

## 📦 Packing: Collecting Values into a Container

### Tuple packing

```python
# Implicit tuple creation (packing)
coordinates = 10, 20, 30
print(coordinates)    # ✅ (10, 20, 30)

# With parentheses (more explicit)
point = (10, 20)
```

### List packing

```python
# List literal
numbers = [1, 2, 3, 4]
print(numbers)    # ✅ [1, 2, 3, 4]

# Using list()
numbers = list((1, 2, 3))  # Unpacking tuple into list
print(numbers)    # ✅ [1, 2, 3]
```

---

## 📦 Unpacking: Extracting Values from a Container

### Basic unpacking

```python
# Tuple unpacking
point = (3, 5)
x, y = point
print(x, y)   # ✅ 3 5

# List unpacking
rgb = [255, 128, 0]
red, green, blue = rgb
print(red)    # ✅ 255

# String unpacking (characters)
word = "hi"
a, b = word
print(a, b)   # ✅ h i
```

### Unpacking in function calls (`*`)

```python
def add(a, b):
    return a + b

args = (10, 20)
result = add(*args)   # ✅ Unpacks tuple into separate arguments
print(result)         # ✅ 30
```

### Unpacking in assignments

```python
# Swapping variables without temp
a, b = 1, 2
a, b = b, a    # ✅ Now a=2, b=1

# Multiple assignment
x = y = z = 0   # ✅ All set to 0
```

---

## ✨ The `*` Operator: Flexible Unpacking

The `*` operator provides variable-length unpacking.

### The "splat" operator (`*`) for variable-length unpacking

```python
# Get first element, rest in a list
head, *tail = [1, 2, 3, 4]
print(head)   # ✅ 1
print(tail)   # ✅ [2, 3, 4]

# Get last element
*head, tail = [1, 2, 3, 4]
print(head)   # ✅ [1, 2, 3]
print(tail)   # ✅ 4

# Get middle elements
first, *middle, last = [1, 2, 3, 4, 5]
print(first)    # ✅ 1
print(middle)   # ✅ [2, 3, 4]
print(last)     # ✅ 5
```

**Empty unpacking is allowed:**

```python
first, *middle = [1]
print(first)    # ✅ 1
print(middle)   # ✅ [] (empty list)
```

---

## ✨ The `**` Operator: Dictionary Unpacking

### Dictionary unpacking in function calls (`**`)

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

params = {"name": "Alice", "greeting": "Hi"}
msg = greet(**params)   # ✅ Unpacks dict into keyword arguments
print(msg)              # ✅ "Hi, Alice!"
```

### Dictionary unpacking in literals

```python
# Merge dictionaries (Python 3.5+)
defaults = {"host": "localhost", "port": 8080}
overrides = {"port": 3000}

# Method 1: unpacking
config = {**defaults, **overrides}
print(config)   # ✅ {'host': 'localhost', 'port': 3000}

# Method 2: dict update (pre-3.5)
config = defaults.copy()
config.update(overrides)

# Order matters: later dicts override earlier ones
a = {"x": 1}
b = {"y": 2}
c = {"x": 99}

merged = {**a, **b, **c}   # ✅ {'x': 99, 'y': 2}
```

---

## 🧱 Packing and Unpacking with Functions

### Variadic parameters (`*args`, `**kwargs`)

```python
# *args: pack positional arguments into a tuple
def sum_all(*numbers):
    return sum(numbers)

print(sum_all(1, 2, 3))   # ✅ 6
print(sum_all(10, 20))    # ✅ 30

# **kwargs: pack keyword arguments into a dict
def build_user(**info):
    return info

print(build_user(name="Alice", age=30))
# ✅ {'name': 'Alice', 'age': 30}
```

### Passing arguments with `*` and `**`

```python
def greet(name, greeting="Hello", punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

args = ("Alice",)
kwargs = {"greeting": "Hi"}

print(greet(*args))                     # ✅ "Hi, Alice!"
print(greet("Bob", **kwargs))           # ✅ "Hi, Bob!"
print(greet(*args, punctuation="!!!"))  # ✅ "Hi, Alice!!!"
```

---

## 🔄 Unpacking in Loops

```python
# Dictionary unpacking in loops
counts = {"a": 1, "b": 2, "c": 3}

# Unpack key-value pairs
for k, v in counts.items():
    print(k, "=", v)
# ✅ a = 1
# ✅ b = 2
# ✅ c = 3
```

### Nested unpacking

```python
points = [(1, 2), (3, 4), (5, 6)]

for x, y in points:
    print(f"Point at ({x}, {y})")

# Output:
# ✅ Point at (1, 2)
# ✅ Point at (3, 4)
# ✅ Point at (5, 6)

# Nested lists
matrix = [[1, 2], [3, 4]]
for row in matrix:
    a, b = row
    print(a + b)
# ✅ 3 (1+2)
# ✅ 7 (3+4)
```

---

## ⚠️ Common Pitfalls

### 1. Starred assignment must have at least one element

```python
# ❌ ValueError: not enough values to unpack
first, *rest = []    # rest can't be empty in this form

# ✅ Use multiple assignment
*rest, = []          # rest = []
```

### 2. Unpacking mismatched lengths

```python
# ❌ ValueError: too many values to unpack
a, b = [1, 2, 3]

# ❌ ValueError: not enough values to unpack
a, b, c = [1, 2]

# ✅ Use * for flexible unpacking
a, *b = [1, 2, 3]    # a=1, b=[2, 3]
```

### 3. Unpacking sets/dicts

```python
s = {1, 2, 3}
a, b, c = s     # ✅ Works (but order is arbitrary)

d = {"a": 1, "b": 2}
x, y = d        # ✅ Unpacks KEYS only: x="a", y="b"
x, y = d.values()  # ✅ Unpacks VALUES: x=1, y=2
x, y = d.items()   # ✅ Unpacks (key, value) tuples
```

---

## ⚙️ Under the Hood: How Unpacking Works

When you write `a, b = (1, 2)`:

1. Python evaluates the right side → creates tuple `(1, 2)`
2. It performs **sequence unpacking**:
   - Checks the length matches
   - Extracts each element by index
   - Assigns to left-side variables

**The `*` operator creates a list** from remaining elements.

```python
import dis

def unpack():
    a, *b = [1, 2, 3]
    return b

dis.dis(unpack)
# Shows: UNPACK_EX with count of items to unpack
```

**The `**` operator creates a new dict** from merged dictionaries.

```python
d1 = {"a": 1}
d2 = {"b": 2}

# d3 = {**d1, **d2} becomes:
d3 = dict()
d3.update(d1)
d3.update(d2)
```

---

## 🔗 Further Reading

- [Python docs: Tuples and Sequences](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)
- [PEP 448 — Additional Unpacking Generalizations](https://peps.python.org/pep-0448/)
- [Python docs: Unpacking Argument Lists](https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists)
- [Python docs: `*` expression](https://docs.python.org/3/reference/expressions.html#expression-lists)
