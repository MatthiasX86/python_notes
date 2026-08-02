# Python Core Concepts: Essential Overview

<!--toc:start-->

- [Python Core Concepts: Essential Overview](#python-core-concepts-essential-overview)
  - [🧠 Object Model Fundamentals](#🧠-object-model-fundamentals)
    - [Everything is an object](#everything-is-an-object)
    - [Identity, Type, Value](#identity-type-value)
  - [🪵 Data Types & Structures](#🪵-data-types-structures)
    - [Immutable types](#immutable-types)
    - [Mutable types](#mutable-types)
  - [🧱 Control Flow & Loops](#🧱-control-flow-loops)
    - [Conditional statements (`if`/`elif`/`else`)](#conditional-statements-ifelifelse)
    - [Loops (`for`/`while`)](#loops-forwhile)
    - [`break`, `continue`, `else` on loops](#break-continue-else-on-loops)
  - [🛠️ Functions & Lambdas](#🛠️-functions-lambdas)
    - [Defining functions (`def`)](#defining-functions-def)
    - [Lambda expressions](#lambda-expressions)
  - [⏳ Comprehensions & Generators](#comprehensions-generators)
    - [List/Dict/Set Comprehensions](#listdictset-comprehensions)
    - [Generator expressions](#generator-expressions)
  - [📦 Modules & Packages](#📦-modules-packages)
    - [Importing](#importing)
  - [🧱 Classes & OOP](#🧱-classes-oop)
    - [Basic class definition](#basic-class-definition)
    - [`__init__`, `__str__`, `__repr__`](#init-str-repr)
    - [Inheritance](#inheritance)
  - [🔍 Exception Handling](#🔍-exception-handling)
    - [`try`/`except`/`else`/`finally`](#tryexceptelsefinally)
  - [🔒 Decorators & Context Managers](#🔒-decorators-context-managers)
    - [Decorators (`@`)](#decorators)
    - [Context managers (`with`)](#context-managers-with)
  - [🧮 Built-in Functions](#🧮-built-in-functions)
  - [📝 Type Hints (Optional)](#📝-type-hints-optional)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

Python’s elegance stems from a small set of **unifying principles**. Master these, and advanced topics become natural extensions.

---

## 🧠 Object Model Fundamentals

### Everything is an object

Every value in Python is an object with a unique identity, type, and value.

```python
x = 42
print(type(x))      # ✅ <class 'int'>
print(id(x))        # Unique memory address (e.g., 140234567890)

y = 42
print(x is y)       # ✅ True (CPython caches small ints)
```

```python
def greet(): pass

print(callable(greet))      # ✅ True (functions are objects too)
print(type(greet))          # ✅ <class 'function'>
```

### Identity, Type, Value

| Attribute      | Purpose                            | Example                       |
| -------------- | ---------------------------------- | ----------------------------- |
| `id(obj)`      | Unique identity (memory address)   | `id(10)`                      |
| `type(obj)`    | Object’s class                     | `type([])` → `<class 'list'>` |
| `obj == other` | Value equality (may be overridden) | `[1] == [1]` → `True`         |

```python
a = [1, 2]
b = [1, 2]
c = a

print(a is b)     # ✅ False (different objects)
print(a == b)     # ✅ True (same value)
print(a is c)     # ✅ True (same object)
```

---

## 🪵 Data Types & Structures

### Immutable types

Cannot be changed after creation. Operations return _new_ objects.

| Type                      | Example                         |
| ------------------------- | ------------------------------- |
| `int`, `float`, `complex` | `42`, `3.14`                    |
| `str`                     | `"hello"`, `"a" + "b"` → `"ab"` |
| `tuple`                   | `(1, 2, 3)`                     |
| `frozenset`               | `frozenset([1, 2])`             |
| `bool`                    | `True`, `False`                 |

```python
s = "hello"
print(id(s))      # Original id
s += " world"     # Creates NEW string
print(id(s))      # ✅ Different id!
```

### Mutable types

Can be modified in-place.

| Type        | Example             |
| ----------- | ------------------- |
| `list`      | `[1, 2]` → append   |
| `dict`      | `{"a": 1}` → update |
| `set`       | `{1, 2}` → add      |
| `bytearray` | `bytearray(b"hi")`  |

```python
lst = [1, 2]
print(id(lst))    # Original id
lst.append(3)     # Modifies in-place
print(id(lst))    # ✅ Same id!
```

---

## 🧱 Control Flow & Loops

### Conditional statements (`if`/`elif`/`else`)

```python
x = 10

if x > 10:
    print("large")
elif x == 10:
    print("exact")   # ✅ This runs
else:
    print("small")
```

**Ternary operator:**

```python
result = "even" if x % 2 == 0 else "odd"
```

### Loops (`for`/`while`)

```python
# for: iterate over any iterable
for i in [1, 2, 3]:
    print(i)

# while: condition-based loop
count = 0
while count < 3:
    print(count)
    count += 1
```

### `break`, `continue`, `else` on loops

```python
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(f"{n} equals {x} * {n//x}")
            break
    else:
        # Runs only if loop completed WITHOUT break
        print(f"{n} is prime")
```

---

## 🛠️ Functions & Lambdas

### Defining functions (`def`)

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))          # ✅ "Hello, Alice!"
print(greet("Bob", "Hi"))      # ✅ "Hi, Bob!"
```

**Variadic arguments:**

```python
def log(*args, **kwargs):
    print("positional:", args)
    print("keyword:", kwargs)

log(1, 2, key="value")
# ✅ positional: (1, 2)
# ✅ keyword: {'key': 'value'}
```

### Lambda expressions

Anonymous functions for short operations.

```python
# Regular function
def square(x): return x * x

# Lambda equivalent
square = lambda x: x * x

# Common use case
numbers = [1, 2, 3]
print(list(map(lambda x: x * 2, numbers)))  # ✅ [2, 4, 6]
```

---

## ⏳ Comprehensions & Generators

### List/Dict/Set Comprehensions

| Type | Syntax                           |
| ---- | -------------------------------- |
| List | `[expr for item in iterable]`    |
| Dict | `{key: val for key in iterable}` |
| Set  | `{expr for item in iterable}`    |

```python
# List comprehension
squares = [x**2 for x in range(5)]      # ✅ [0, 1, 4, 9, 16]

# Dict comprehension
word_len = {w: len(w) for w in ["hi", "hello"]}  # ✅ {"hi": 2, "hello": 5}

# Set comprehension (unique values)
unique = {x % 3 for x in [1, 2, 3, 4, 5]}   # ✅ {0, 1, 2}
```

### Generator expressions

Parentheses instead of brackets—_lazy evaluation_.

```python
# Creates generator (no memory allocation yet)
gen = (x**2 for x in range(5))

print(next(gen))  # ✅ 0
print(list(gen))  # ✅ [1, 4, 9, 16]
```

Use generators for large datasets or streaming data.

---

## 📦 Modules & Packages

### Importing

```python
# Full module
import math
print(math.sqrt(16))  # ✅ 4.0

# Alias
import numpy as np

# Selective import
from math import pi, sqrt

# Wildcard (discouraged—pollutes namespace)
from os import *
```

**`__name__ == "__main__"` pattern:**

```python
def main():
    print("Running...")

if __name__ == "__main__":
    main()  # ✅ Runs only when executed directly
```

---

## 🧱 Classes & OOP

### Basic class definition

```python
class Dog:
    species = "canis"  # Class attribute (shared)

    def __init__(self, name, age):
        self.name = name  # Instance attribute
        self.age = age

    def bark(self):
        return f"{self.name} says woof!"

d = Dog("Fido", 3)
print(d.bark())  # ✅ "Fido says woof!"
```

### `__init__`, `__str__`, `__repr__`

| Method                | Purpose                               |
| --------------------- | ------------------------------------- |
| `__init__(self, ...)` | Constructor (initializer)             |
| `__str__(self)`       | String for `print()` / `str(obj)`     |
| `__repr__(self)`      | Unambiguous string for REPL/debugging |

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)
print(p)       # ✅ "(3, 4)" — uses __str__
repr(p)        # ✅ "Point(x=3, y=4)" — uses __repr__
```

### Inheritance

```python
class Animal:
    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return "woof!"

d = Dog()
print(d.speak())  # ✅ "woof!"
```

---

## 🔍 Exception Handling

### `try`/`except`/`else`/`finally`

```python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    else:
        # Runs only if no exception
        return f"Result: {result}"
    finally:
        # Always runs (cleanup/logging)
        print("Division attempt complete")

print(safe_divide(10, 2))  # ✅ "Result: 5.0"
print(safe_divide(10, 0))  # ✅ "Cannot divide by zero"
```

---

## 🔒 Decorators & Context Managers

### Decorators (`@`)

```python
def uppercase(func):
    def wrapper():
        return func().upper()
    return wrapper

@uppercase
def greet():
    return "hello"

print(greet())  # ✅ "HELLO"
```

**Common built-in decorators:**

- `@property` — turn method into attribute
- `@classmethod` — class-bound method
- `@staticmethod` — no-self method

### Context managers (`with`)

Automatically manage resources.

```python
# File handling (auto-closes)
with open("file.txt", "w") as f:
    f.write("hello")

# Custom context manager
from contextlib import contextmanager

@contextmanager
def open_db():
    print("Connecting...")
    try:
        yield "db_connection"
    finally:
        print("Closing...")

with open_db() as db:
    print(f"Using {db}")
```

---

## 🧮 Built-in Functions

| Function                                 | Purpose                         |
| ---------------------------------------- | ------------------------------- |
| `len(obj)`                               | Length of container             |
| `sum(iterable, start=0)`                 | Sum numbers                     |
| `min/max(iterable)`                      | Smallest/largest element        |
| `any(iterable)`                          | True if any truthy              |
| `all(iterable)`                          | True if all truthy              |
| `enumerate(iterable, start=0)`           | `(index, value)` pairs          |
| `zip(*iterables)`                        | Group elements by position      |
| `sorted(iterable, key=..., reverse=...)` | New sorted list                 |
| `map(func, iterable)`                    | Apply function to each item     |
| `filter(func, iterable)`                 | Keep items where func is truthy |

```python
nums = [1, 2, 3, 4]
print(list(enumerate(nums)))   # ✅ [(0, 1), (1, 2), (2, 3), (3, 4)]
print(list(zip(nums, "abcd"))) # ✅ [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
print(sum(nums))               # ✅ 10
```

---

## 📝 Type Hints (Optional)

Python is dynamically typed, but type hints improve tooling and documentation.

```python
from typing import List, Dict, Optional

def process(items: List[int], config: Dict[str, bool]) -> Optional[str]:
    if not items:
        return None
    return f"Processed {len(items)} items"

# IDEs and mypy/pyright use these hints for validation
```

---

## 🔗 Further Reading

- [Python Tutorial (Official)](https://docs.python.org/3/tutorial/)
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Standard Library](https://docs.python.org/3/library/)
