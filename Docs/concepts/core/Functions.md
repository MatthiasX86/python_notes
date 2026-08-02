# Python Functions: A Comprehensive Guide

<!--toc:start-->

- [Python Functions: A Comprehensive Guide](#python-functions-a-comprehensive-guide)
  - [📋 Table of Contents](#📋-table-of-contents)
  - [🧱 Defining Functions](#🧱-defining-functions)
    - [✅ Basic Syntax](#basic-syntax)
    - [❌ Common Pitfalls](#common-pitfalls)
  - [🧪 Parameters & Arguments](#🧪-parameters--arguments)
    - [Positional-only parameters (`/`)](#positional-only-parameters--)
    - [Keyword-only parameters (`*`)](#keyword-only-parameters--)
  - [🧠 Default Parameter Behavior](#🧠-default-parameter-behavior)
    - [✅ Safe Default Pattern](#safe-default-pattern)
  - [🔄 Function Objects & First-Class Status](#🔄-function-objects--first-class-status)
  - [📎 Nested Functions & Closures](#📎-nested-functions--closures)
    - [✅ Closure Example](#closure-example)
  - [🛠️ Decorators](#🛠️-decorators)
    - [✅ Basic Decorator](#basic-decorator)
    - [🔍 `functools.wraps`](#functoolswraps)
  - [🧩 Callable Objects](#🧩-callable-objects)
    - [✅ callable vs Function](#callable-vs-function)
  - [⚡ Functional Programming Patterns](#⚡-functional-programming-patterns)
    - [📈 Higher-Order Functions](#higher-order-functions)
    - [🔗 `map`, `filter`, `reduce`](#map-filter-reduce)
  - [🔍 Introspection & Attributes](#🔍-introspection--attributes)
    - [🛠️ `dir()`, `vars()`, `inspect`](#dir-vars-inspect)
    - [🔍 Common Attributes](#common-attributes)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

Functions are foundational to Python—**everything is an object**, and functions are no exception. They enable code reuse, modularity, and functional programming patterns.

---

## 🧱 Defining Functions

### ✅ Basic Syntax

```python
def function_name(param1, param2=None):
    """Optional docstring."""
    return param1 + param2

# Call with positional or keyword arguments
result = function_name(5)          # pos-only
result = function_name(param1=5)   # keyword
```

### ❌ Common Pitfalls

```python
# ❌ SyntaxError: positional argument follows keyword argument
def f(a, b): return a + b
f(1, b=2)  # ✅ OK
f(a=1, 2)  # ❌ Invalid syntax

# ❌ IndentationError: expected an indented block
def empty():
    # Use 'pass' for stub functions
    pass

# ❌ NameError: name 'x' is not defined (scope issue)
def scope():
    x = 10
print(x)  # ❌ 'x' exists only inside function
```

---

## 🧪 Parameters & Arguments

Python supports five parameter kinds:

| Kind                  | Syntax    | Requirement           |
| --------------------- | --------- | --------------------- |
| Positional-only       | `a, b, /` | Must be passed by pos |
| Positional-or-keyword | `a, b`    | Either works          |
| Keyword-only          | `*, a, b` | Must be keyword arg   |

```python
def combined(pos_only, /, standard, *, kw_only):
    return pos_only + standard + kw_only

# ✅ Valid calls
combined(1, 2, kw_only=3)
combined(1, standard=2, kw_only=3)

# ❌ Invalid: positional_only as keyword
combined(pos_only=1, standard=2, kw_only=3)  # TypeError
```

### Positional-only parameters (`/`)

```python
def greet(name, /, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")          # ✅
greet(name="Bob")       # ❌ TypeError: name is positional-only
```

### Keyword-only parameters (`*`)

```python
def connect(*, host="localhost", port=8080):
    return f"{host}:{port}"

connect()                     # ✅ "localhost:8080"
connect(host="example.com")   # ✅
connect("example.com")        # ❌ TypeError: host is keyword-only
```

---

## 🧠 Default Parameter Behavior

**Defaults are evaluated _once_ at function definition time**, not each call.

```python
import datetime

def log(msg, timestamp=datetime.datetime.now()):
    print(f"{timestamp}: {msg}")

# ⚠️ All calls get the same timestamp (when function was defined)
log("First")
import time; time.sleep(1)
log("Second")  # ❌ Same timestamp!
```

### ✅ Safe Default Pattern

Use `None` and initialize inside the function:

```python
def log(msg, timestamp=None):
    if timestamp is None:
        timestamp = datetime.datetime.now()
    print(f"{timestamp}: {msg}")

# ✅ Different timestamps
log("First")
time.sleep(1)
log("Second")  # ✅ New timestamp
```

---

## 🔄 Function Objects & First-Class Status

Functions are objects of type `function`:

```python
def greet(): return "Hello"

# Assign to variable
hello = greet
print(hello())  # ✅ "Hello"

# Store in collection
funcs = [greet, print]
for f in funcs:
    f("Hi")  # Prints "Hi" twice

# Pass as argument
def apply(func, value):
    return func(value)

print(apply(lambda x: x * 2, 5))  # ✅ 10
```

---

## 📎 Nested Functions & Closures

A **closure** is a nested function that captures variables from its enclosing scope.

```python
def make_multiplier(factor):
    def multiply(x):          # Captures 'factor'
        return x * factor
    return multiply

times2 = make_multiplier(2)
times5 = make_multiplier(5)

print(times2(10))  # ✅ 20
print(times5(10))  # ✅ 50

# Inspect captured variables
print(times2.__closure__[0].cell_contents)  # ✅ 2
```

### ✅ Closure Example

```python
def counter():
    count = 0

    def increment():
        nonlocal count  # Required to modify enclosing variable
        count += 1
        return count

    return increment

c = counter()
print(c())  # ✅ 1
print(c())  # ✅ 2
```

---

## 🛠️ Decorators

Decorators modify function behavior without changing the function itself.

### ✅ Basic Decorator

```python
import functools

def logging_decorator(func):
    @functools.wraps(func)  # Preserves docstring/name
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@logging_decorator
def add(a, b):
    """Add two numbers."""
    return a + b

add(3, 5)
# Output:
# Calling add with args=(3, 5), kwargs={}
# add returned 8
```

### 🔍 `functools.wraps`

`@wraps` copies metadata (`__name__`, `__doc__`, etc.) from original to wrapper.

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper  # ❌ Loses docstring

@decorator
def documented():
    """This is documentation."""
    pass

print(documented.__doc__)  # ❌ None
```

```python
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper  # ✅ Preserves docstring

print(documented.__doc__)  # ✅ "This is documentation."
```

---

## 🧩 Callable Objects

Any object with a `__call__` method is callable—**functions are just one kind of callable**.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor

times3 = Multiplier(3)
print(times3(10))  # ✅ 30
```

### ✅ callable vs Function

```python
def regular_func():
    pass

class CallableClass:
    def __call__(self):
        return "called"

obj = CallableClass()

print(callable(regular_func))    # ✅ True
print(callable(obj))             # ✅ True (has __call__)
print(callable([1, 2, 3]))       # ❌ False

# Verify call
print(obj())                     # ✅ "called"
```

---

## ⚡ Functional Programming Patterns

Python supports functional programming through higher-order functions and composable operations.

### Higher-Order Functions

Functions that take or return other functions:

```python
def apply_transform(func, values):
    """Apply func to each element in values."""
    return [func(v) for v in values]

# Use with different transformations
print(apply_transform(lambda x: x * 2, [1, 2, 3]))     # ✅ [2, 4, 6]
print(apply_transform(lambda x: str(x), [1, 2, 3]))    # ✅ ["1", "2", "3"]
```

### 🔗 `map`, `filter`, `reduce`

| Function | Purpose                          | Example                                                               |
| -------- | -------------------------------- | --------------------------------------------------------------------- |
| `map`    | Apply function to each element   | `list(map(str, [1, 2]))`                                              |
| `filter` | Keep elements matching predicate | `list(filter(lambda x: x > 0, [-1, 2]))`                              |
| `reduce` | Accumulate to single value       | `from functools import reduce; reduce(lambda x, y: x + y, [1, 2, 3])` |

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Map: square each number
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # ✅ [1, 4, 9, 16, 25]

# Filter: keep even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)    # ✅ [2, 4]

# Reduce: compute product
product = reduce(lambda x, y: x * y, numbers)
print(product)  # ✅ 120
```

**Modern Python preference:** List comprehensions are often clearer than `map`/`filter`.

```python
# Equivalent to map/filter above
squared = [x ** 2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]

# For reduce, prefer explicit loops or sum/min/max
product = 1
for x in numbers:
    product *= x
```

---

## 🔍 Introspection & Attributes

### 🛠️ `dir()`, `vars()`, `inspect`

| Tool                       | Purpose                                  |
| -------------------------- | ---------------------------------------- |
| `dir(func)`                | List all attributes (including methods)  |
| `vars()` / `func.__dict__` | Instance or function attributes (if any) |
| `inspect.getsource(func)`  | Get source code                          |

```python
import inspect

def example(a: int, b: str = "hello") -> bool:
    """Example function."""
    return True

# Inspect parameters
sig = inspect.signature(example)
print(sig)  # ✅ (a: int, b: str = 'hello') -> bool

# Get parameters details
for name, param in sig.parameters.items():
    print(name, param.annotation, param.default)

# Get source
print(inspect.getsource(example))
```

### 🔍 Common Attributes

```python
def func(a, b=10):
    """Docstring."""
    pass

# Standard attributes
print(func.__name__)     # ✅ "func"
print(func.__doc__)      # ✅ "Docstring."
print(func.__module__)   # Module where defined
print(func.__defaults__) # ✅ (10,) — default values tuple
print(func.__annotations__)  # ✅ {'a': ..., 'b': ..., 'return': ...}
```

---

## 🔗 Further Reading

- [Python docs: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python docs: Decorators](https://docs.python.org/3/glossary.html#term-decorator)
- [PEP 3102 — Keyword-only arguments](https://peps.python.org/pep-3102/)
- [Python docs: `functools`](https://docs.python.org/3/library/functools.html)
- [Python docs: `inspect`](https://docs.python.org/3/library/inspect.html)
