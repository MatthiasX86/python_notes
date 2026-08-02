# The `@property` Decorator in Python

<!--toc:start-->

- [The `@property` Decorator in Python](#the-property-decorator-in-python)
  - [📋 Table of Contents](#📋-table-of-contents)
  - [🎯 What is `@property`?](#-what-is-property)
    - [Property vs. Regular Attribute](#property-vs-regular-attribute)
  - [🧱 Basic Syntax and Usage](#🧱-basic-syntax-and-usage)
    - [✅ Simple Property Example](#simple-property-example)
  - [🔄 Property with Setters and Deleters](#🔄-property-with-setters-and-deleters)
    - [Adding a setter](#adding-a-setter)
    - [Adding a deleter](#adding-a-deleter)
  - [🧐 Why Use Properties?](#-why-use-properties)
    - [Encapsulation without breaking API](#encapsulation-without-breaking-api)
    - [Computed properties](#computed-properties)
  - [⚠️ Common Pitfalls](#⚠️-common-pitfalls)
    - [1. Infinite recursion in setters](#1-infinite-recursion-in-setters)
    - [2. Performance considerations](#2-performance-considerations)
  - [⚙️ Under the Hood: How `@property` Works](#⚙️-under-the-hood-how-property-works)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

The `@property` decorator lets you define methods that behave like attributes—enabling validation, computed values, and backward-compatible API evolution.

---

## 🎯 What is `@property`?

A **property** is a descriptor that lets you define methods accessible via attribute syntax (`obj.attr`) instead of method calls (`obj.method()`).

### Property vs. Regular Attribute

|                 | Regular Attribute | Property                     |
| --------------- | ----------------- | ---------------------------- |
| **Access**      | `obj.x`           | `obj.x` (same syntax!)       |
| **Computation** | Static value      | Computed on access           |
| **Validation**  | None possible     | Full control over assignment |

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

c = Circle(5)
print(c.radius)   # ✅ 5
c.radius = -10    # ❌ Allows invalid value!
```

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius   # "Private" by convention

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius must be non-negative")
        self._radius = value

c = Circle(5)
print(c.radius)   # ✅ 5
c.radius = -10    # ❌ ValueError!
```

---

## 🧱 Basic Syntax and Usage

### ✅ Simple Property Example

```python
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

p = Person("Alice", "Smith")
print(p.full_name)   # ✅ "Alice Smith"
# p.full_name = "Bob"  ❌ AttributeError: can't set attribute
```

**Key points:**

- Property is defined with `@property` decorator on a getter method
- Accessed like an attribute: `obj.property`
- Returns computed/dynamic values

---

## 🔄 Property with Setters and Deleters

### Adding a setter

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius  # Uses setter below!

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

t = Temperature(25)
print(t.celsius)    # ✅ 25
print(t.fahrenheit) # ✅ 77.0

t.celsius = -300    # ❌ ValueError!
```

### Adding a deleter

```python
class User:
    def __init__(self, username):
        self._username = username

    @property
    def username(self):
        return self._username

    @username.deleter
    def username(self):
        print("Deleting username...")
        self._username = None

u = User("alice")
del u.username      # ✅ "Deleting username..."
print(u.username)   # ✅ None
```

---

## 🧐 Why Use Properties?

### Encapsulation without breaking API

```python
# Phase 1: Simple attribute
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

# Phase 2: Add validation (breaking change without property!)
class BankAccount:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative!")
        self._balance = value

# Existing code continues to work: account.balance = 100
```

### Computed properties

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)

r = Rectangle(4, 5)
print(r.area)       # ✅ 20 (computed on access)
print(r.perimeter)  # ✅ 18
```

---

## ⚠️ Common Pitfalls

### 1. Infinite recursion in setters

```python
class Broken:
    def __init__(self, value):
        self.value = value  # ❌ Calls setter infinitely!

    @property
    def value(self):
        return self.value   # ❌ Calls getter infinitely!
```

✅ **Fix with private backing field:**

```python
class Fixed:
    def __init__(self, value):
        self._value = value  # ✅ Use underscore-prefixed field

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v < 0:
            raise ValueError("Must be non-negative")
        self._value = v
```

### 2. Performance considerations

Properties are called _every time_ they're accessed:

```python
import timeit

class Direct:
    def __init__(self, value):
        self.value = value * 1000

class Property:
    def __init__(self, value):
        self._value = value * 1000

    @property
    def value(self):
        return self._value

d = Direct(1)
p = Property(1)

print(timeit.timeit("d.value", globals={"d": d}, number=1_000_000))
print(timeit.timeit("p.value", globals={"p": p}, number=1_000_000))
# ✅ Property is ~3x slower due to method call overhead
```

Use properties only when you need validation, computed values, or encapsulation.

---

## ⚙️ Under the Hood: How `@property` Works

The `@property` decorator creates a **descriptor** object:

```python
class MyProperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)

# Simplified version of Python's property:
class Property:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def setter(self, fset):
        self.fset = fset
        return self

# Usage:
class Example:
    def __init__(self, value):
        self._value = value

    @Property
    def value(self):
        return self._value

# The decorator returns a Property descriptor instance
```

When you access `obj.attr`, Python calls the descriptor's `__get__` method.

---

## 🔗 Further Reading

- [Python docs: `property`](https://docs.python.org/3/library/functions.html#property)
- [Python docs: Descriptors](https://docs.python.org/3/howto/descriptor.html)
- [PEP 254 — Automatic return values](https://peps.python.org/pep-0254/) (for computed properties discussion)
