# The `@lru_cache` Decorator in Python

<!--toc:start-->

- [The `@lru_cache` Decorator in Python](#the-lrucache-decorator-in-python)
  - [🎯 What is `@lru_cache`?](#🎯-what-is-lrucache)
    - [How LRU stands for](#how-lru-stands-for)
  - [🧱 Basic Syntax and Usage](#🧱-basic-syntax-and-usage)
    - [✅ Simple caching example](#simple-caching-example)
  - [⚙️ Configuration and Methods](#️-configuration-and-methods)
    - [Cache size limit (`maxsize`)](#cache-size-limit-maxsize)
    - [Clearing the cache](#clearing-the-cache)
  - [🧠 How LRU Eviction Works](#🧠-how-lru-eviction-works)
    - [Example: LRU eviction in action](#example-lru-eviction-in-action)
  - [🧐 When to Use `@lru_cache`](#🧐-when-to-use-lrucache)
    - [✅ Good candidates for caching](#good-candidates-for-caching)
    - [❌ When NOT to use it](#when-not-to-use-it)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Mutable default arguments](#1-mutable-default-arguments)
    - [2. Non-hashable arguments](#2-non-hashable-arguments)
  - [⚙️ Under the Hood: How `@lru_cache` Works](#️-under-the-hood-how-lrucache-works)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

The `@lru_cache` decorator caches function results based on their arguments, dramatically improving performance for expensive or frequently-called functions.

---

## 🎯 What is `@lru_cache`?

**LRU** stands for **Least Recently Used**—a caching strategy that keeps recently accessed items and evicts the least recently used ones when capacity is full.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(x, y):
    # Simulate expensive computation
    import time
    time.sleep(1)
    return x + y

# First call: computes result (takes ~1 second)
print(expensive_function(1, 2))   # ✅ 3

# Second call with same args: returns cached result (instant!)
print(expensive_function(1, 2))   # ✅ 3
```

### How LRU stands for

| Term         | Meaning                                                  |
| ------------ | -------------------------------------------------------- |
| **L**east    | Discards items that haven't been accessed recently       |
| **R**ecently | Tracks access order (most recent last in eviction queue) |
| **U**sed     | Cache hits update "recently used" status                 |

---

## 🧱 Basic Syntax and Usage

### ✅ Simple caching example

```python
from functools import lru_cache

@lru_cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Without caching: O(2^n) time — painfully slow for n=35
# With caching: O(n) time

print(fibonacci(35))   # ✅ 9227465 (instant!)
```

**Key points:**

- Decorator wraps the function with a cache
- Cache is keyed by _argument tuple_ (positional + keyword args)
- Results are stored in a dictionary: `{(args, kwargs): result}`

---

## ⚙️ Configuration and Methods

### Cache size limit (`maxsize`)

```python
from functools import lru_cache

@lru_cache(maxsize=32)     # Maximum 32 cached entries
def compute(x):
    return x * 2

@lru_cache(maxsize=None)   # Unbounded cache (grows indefinitely)
def identity(x):
    return x

@lru_cache()               # Default: maxsize=128
def square(x):
    return x ** 2
```

| `maxsize`    | Behavior                                       |
| ------------ | ---------------------------------------------- |
| `None`       | Unbounded cache (memory risk!)                 |
| Positive int | Maximum entries; evicts LRU when full          |
| `0` or `1`   | Special case: caches single most recent result |

### Clearing the cache

```python
from functools import lru_cache

@lru_cache(maxsize=10)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

factorial(5)      # ✅ Cache populated
print(factorial.cache_info())
# ✅ CacheInfo(hits=0, misses=6, maxsize=10, currsize=6)

factorial.cache_clear()  # Clear all cached results

print(factorial.cache_info())
# ✅ CacheInfo(hits=0, misses=0, maxsize=10, currsize=0)
```

**Cache info attributes:**

- `hits` — Number of times cached result was used
- `misses` — Number of times function actually executed
- `maxsize` — Maximum cache size
- `currsize` — Current number of cached entries

---

## 🧠 How LRU Eviction Works

When cache is full, adding a new entry:

1. Checks if key exists → update existing entry
2. If cache is full → evict the _least recently used_ item
3. Add new entry and mark it as "most recently used"

### Example: LRU eviction in action

```python
from functools import lru_cache

@lru_cache(maxsize=2)
def compute(x):
    print(f"Computing {x}...")
    return x * 2

compute(1)  # ✅ "Computing 1..." → cache: {1: 2}
compute(2)  # ✅ "Computing 2..." → cache: {1: 2, 2: 4}
compute(1)  # ✅ (cached) → cache order: {2: 4, 1: 2} (1 is now MRU)
compute(3)  # ✅ "Computing 3..." → evicts 2 (LRU)
            #    cache: {1: 2, 3: 6}
```

```python
# Verify eviction behavior
@lru_cache(maxsize=3)
def f(x):
    print(f"miss: {x}")
    return x

f(1)  # miss: 1
f(2)  # miss: 2
f(3)  # miss: 3

# Cache is now full with entries in order: [1, 2, 3] (oldest to newest)

f(1)  # hit! — moves 1 to end: [2, 3, 1]

f(4)  # miss: 4 — evicts 2 (oldest/least recently used)
      #    new order: [3, 1, 4]
```

---

## 🧐 When to Use `@lru_cache`

### ✅ Good candidates for caching

| Candidate                 | Why                                   |
| ------------------------- | ------------------------------------- |
| Pure functions            | No side effects, deterministic output |
| Expensive computations    | Heavy math, file I/O, network calls   |
| Recursive algorithms      | Fibonacci, tree traversal             |
| Identical inputs repeated | Memoization pattern                   |

```python
from functools import lru_cache

# Pure, expensive, repetitive calls = perfect for caching
@lru_cache(maxsize=None)
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Multiple calls with same number are instant!
print(is_prime(97))   # First call: computes
print(is_prime(97))   # Second call: cached!
```

### ❌ When NOT to use it

| Situation               | Reason                                             |
| ----------------------- | -------------------------------------------------- |
| **Side effects**        | Cache won't re-execute (misses needed side effect) |
| **Mutable state**       | Cached result may become stale                     |
| **Non-hashable args**   | TypeError: unhashable type                         |
| **Huge argument space** | Memory exhaustion risk                             |

```python
from functools import lru_cache

@lru_cache
def get_timestamp():
    return datetime.datetime.now()  # ❌ Always same result!

print(get_timestamp())   # ✅ 2025-08-01 12:00:00
print(get_timestamp())   # ✅ Same timestamp! (cached)

# Non-hashable arguments fail:
@lru_cache
def process_list(lst):
    return sum(lst)

process_list([1, 2, 3])   # ❌ TypeError: unhashable type 'list'
```

---

## ⚠️ Common Pitfalls

### 1. Mutable default arguments

```python
from functools import lru_cache

# ❌ Dangerous: same list object reused across calls
@lru_cache
def append_to_list(item, lst=[]):
    lst.append(item)
    return lst

print(append_to_list(1))  # ✅ [1]
print(append_to_list(2))  # ❌ [1, 2] — same list reused!
```

✅ **Fix with sentinel:**

```python
@lru_cache
def append_to_list(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### 2. Non-hashable arguments

```python
@lru_cache
def func(d):
    return d["key"]

func({"key": "value"})  # ❌ TypeError: unhashable type 'dict'
```

**Workarounds:**

```python
# Convert to hashable type first
@lru_cache
def func_from_tuple(d_items):
    d = dict(d_items)
    return d["key"]

func_from_tuple(tuple({"key": "value"}.items()))  # ✅ Works
```

---

## ⚙️ Under the Hood: How `@lru_cache` Works

```python
# Simplified implementation of lru_cache
from functools import wraps
from collections import OrderedDict

def simple_lru_cache(maxsize=128):
    def decorator(func):
        cache = OrderedDict()  # Key → Value
        cache_stats = {"hits": 0, "misses": 0}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            key = (args, tuple(sorted(kwargs.items())))

            if key in cache:
                cache_stats["hits"] += 1
                # Move to end (most recently used)
                cache.move_to_end(key)
                return cache[key]

            # Cache miss
            cache_stats["misses"] += 1
            result = func(*args, **kwargs)

            # Evict oldest if full
            if len(cache) >= maxsize:
                cache.popitem(last=False)  # Remove LRU

            cache[key] = result
            return result

        def cache_info():
            return f"hits={cache_stats['hits']}, misses={cache_stats['misses']}"

        def cache_clear():
            cache.clear()
            cache_stats["hits"] = 0
            cache_stats["misses"] = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear

        return wrapper
    return decorator
```

**Key internal components:**

- `OrderedDict` — Maintains insertion/usage order for LRU tracking
- `move_to_end()` — Updates "recently used" status on cache hits
- Tuple key — Converts args/kwargs to hashable form

---

## 🔗 Further Reading

- [Python docs: `functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache)
- [PEP 498 — Literal String Interpolation](https://peps.python.org/pep-0498/) (for f-string examples)
- [Python docs: Descriptors](https://docs.python.org/3/howto/descriptor.html) (similar concept)
- [Wikipedia: Least Recently Used](https://en.wikipedia.org/wiki/Least_recently_used)
