# Hashable Objects in Python

<!--toc:start-->

- [Hashable Objects in Python](#hashable-objects-in-python)
  - [✅ What Does “Hashable” Mean?](#✅-what-does-hashable-mean)
  - [🔢 How Hashing Works](#🔢-how-hashing-works)
  - [🛠️ Common Hashable vs Unhashable Types](#🛠️-common-hashable-vs-unhashable-types)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
  - [🧪 How to Check If an Object Is Hashable](#🧪-how-to-check-if-an-object-is-hashable)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

A value is **hashable** if it can be used as a dictionary key or set element — i.e., its hash never changes during its lifetime.

---

## ✅ What Does “Hashable” Mean?

An object is hashable if:

1. It has a hash value that remains constant (implements `__hash__()`)
2. It can be compared to other objects (`__eq__()`)
3. Equality implies equal hashes: if `a == b`, then `hash(a) == hash(b)`

Most **immutable** built-in types are hashable; most **mutable** ones aren’t.

---

## 🔢 How Hashing Works

Python’s `hash()` function:

```python
>>> hash("apple")
-1728643059

>>> hash((1, 2))    # tuple of hashables → hashable
-3550055125

>>> hash([1, 2])    # ❌ list is mutable → unhashable
TypeError: unhashable type: 'list'
```

- Hashes are typically integers used internally by `dict`/`set`
- Hash tables use the hash to assign buckets → O(1) average lookup

> 💡 Keys in `dict` and members of `set` must be hashable — otherwise, membership tests and lookups couldn’t be reliable.

---

## 🛠️ Common Hashable vs Unhashable Types

| Type        | Hashable? | Reason                                                 |
| ----------- | --------- | ------------------------------------------------------ |
| `int`       | ✅ Yes    | Immutable                                              |
| `float`     | ✅ Yes    | Immutable                                              |
| `str`       | ✅ Yes    | Immutable                                              |
| `tuple`     | ✅ Yes    | Only if all elements hashable                          |
| `bool`      | ✅ Yes    | Subclass of `int`                                      |
| `NoneType`  | ✅ Yes    | Single immutable instance                              |
| `list`      | ❌ No     | Mutable — contents can change → hash would be unstable |
| `dict`      | ❌ No     | Mutable                                                |
| `set`       | ❌ No     | Mutable                                                |
| `bytearray` | ❌ No     | Mutable buffer                                         |

Example with nested tuples:

```python
>>> hash((1, (2, 3)))   # ✅ OK — both elements hashable
-789123456

>>> hash((1, [2]))      # ❌ Fails — list is unhashable
TypeError: unhashable type: 'list'
```

---

## ⚠️ Common Pitfalls

### 1. Immutable _containers_ of unhashable items fail

```python
>>> t = (1, [2])   # tuple *contains* a list → unhashable
>>> hash(t)
TypeError: unhashable type: 'list'
```

### 2. Custom classes are hashable _by default_

```python
class Point:
    def __init__(self, x):
        self.x = x

p1 = Point(3)
p2 = Point(3)

hash(p1), hash(p2)  # Different — uses object identity
p1 == p2            # False — unless __eq__ is overridden
```

But if you define `__eq__()`, Python _disables_ `__hash__()` unless you also re-enable it:

```python
class Point:
    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x
    # Now: __hash__ is None (unhashable)!

# Fix: either re-enable default hash or define your own
    __hash__ = object.__hash__
```

---

## 🧪 How to Check If an Object Is Hashable

```python
def is_hashable(obj):
    try:
        hash(obj)
        return True
    except TypeError:
        return False

# Test:
assert is_hashable("hello")
assert not is_hashable([1, 2, 3])
```

---

## 🔗 Further Reading

- [Python docs: Data Model → Hashability](https://docs.python.org/3/reference/datamodel.html#object.__hash__)
- [PEP 20 — Hashability & Equality](https://peps.python.org/pep-0020/)
