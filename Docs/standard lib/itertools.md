# Python `itertools` Module

<!--toc:start-->

- [Python `itertools` Module](#python-itertools-module)
  - [🧠 What is `itertools`?](#🧠-what-is-itertools)
  - [🔧 Infinite Iterators](#🔧-infinite-iterators)
    - [`count(start=0, step=1)`](#countstart0-step1)
    - [`cycle(iterable)`](#cycleiterable)
    - [`repeat(elem[, n])`](#repeatelem-n)
  - [🧱 Terminating Iterators](#🧱-terminating-iterators)
    - [`accumulate(iterable, func=operator.add)`](#accumulateiterable-funcoperatoradd)
    - [`chain(*iterables)`](#chainiterables)
    - [`chain.from_iterable(iterable)`](#chainfrom_iterableiterable)
    - [`compress(data, selectors)`](#compressdata-selectors)
    - [`dropwhile(pred, iterable)`](#dropwhilepred-iterable)
    - [`takewhile(pred, iterable)`](#takewhilepred-iterable)
    - [`filterfalse(pred, iterable)`](#filterfalsepred-iterable)
    - [`groupby(iterable, key=None)`](#groupbyiterable-keynone)
    - [`islice(iterable, start, stop[, step])`](#isliceiterable-start-stop-step)
    - [`starmap(func, iterable)`](#starmapfunc-iterable)
    - [`tee(iterable, n=2)`](#teeiterable-n2)
    - [`zip_longest(*iterables, fillvalue=None)`](#zip_longestiterables-fillvaluenone)
  - [🎲 Combinatoric Iterators](#🎲-combinatoric-iterators)
    - [`product(*iterables, repeat=1)`](#productiterables-repeat1)
    - [`permutations(iterable, r=None)`](#permutationsiterable-rnone)
    - [`combinations(iterable, r)`](#combinationsiterable-r)
    - [`combinations_with_replacement(iterable, r)`](#combinations_with_replacementiterable-r)
  - [🛠️ Common Patterns & Recipes](#️-common-patterns--recipes)
    - [`pairwise(iterable)`](#pairwiseiterable)
    - [`window(iterable, n)`](#windowiterable-n)
  - [⚡ Performance Notes](#-performance-notes)
  - [⚠️ Common Pitfalls](#️-common-pitfalls)
    - [1. Infinite loops without termination](#1-infinite-loops-without-termination)
    - [2. Forgetting `list()` for single use](#2-forgetting-list-for-single-use)
  - [🔗 Further Reading](#🔗-further-reading)

<!--toc:end-->

The `itertools` module provides high-performance, memory-efficient tools for working with iterators—sequences of data that are computed lazily.

---

## 🧠 What is `itertools`?

`itertools` is a **standard library module** that implements iterator building blocks inspired by functional programming languages like Haskell and LISP.

Key characteristics:

- **Lazy evaluation**: Values computed on-demand
- **Memory efficient**: No intermediate lists created
- **Composable**: Functions chain together naturally
- **C implementation**: Fast execution

```python
import itertools

# Example: Chain multiple iterables without creating intermediate lists
list(itertools.chain([1, 2], 'ABC', (3, 4)))
# ✅ [1, 2, 'A', 'B', 'C', 3, 4]
```

---

## 🔧 Infinite Iterators

These create iterators that can yield values indefinitely.

### `count(start=0, step=1)`

Returns an infinite arithmetic progression.

```python
# Count from 10, stepping by 2
for i in itertools.count(10, 2):
    if i > 20:
        break
    print(i)  # 10, 12, 14, 16, 18, 20

# Count with floats
list(itertools.islice(itertools.count(0.5, 0.25), 4))
# ✅ [0.5, 0.75, 1.0, 1.25]
```

### `cycle(iterable)`

Repeats the given iterable indefinitely.

```python
# Cycle through 'ABC' forever
c = itertools.cycle('ABC')
for _ in range(7):
    print(next(c), end=' ')  # A B C A B C A

# Practical use: alternate between two states
toggle = itertools.cycle(['ON', 'OFF'])
[next(toggle) for _ in range(5)]  # ['ON', 'OFF', 'ON', 'OFF', 'ON']
```

### `repeat(elem[, n])`

Repeats an element a specified number of times (or infinitely if `n=None`).

```python
# Repeat 'X' 3 times
list(itertools.repeat('X', 3))  # ['X', 'X', 'X']

# Infinite repeat (use with islice to limit)
list(itertools.islice(itertools.repeat('A'), 5))  # ['A', 'A', 'A', 'A', 'A']

# Combine with starmap for repeated arguments
list(itertools.starmap(pow, itertools.repeat((2, 5), 3)))
# ✅ [32, 32, 32] (pow(2, 5) three times)
```

---

## 🧱 Terminating Iterators

These process input iterables and produce finite output.

### `accumulate(iterable, func=operator.add)`

Returns cumulative sums or results of a binary function.

```python
import operator

# Default: cumulative sum
list(itertools.accumulate([1, 2, 3, 4]))
# ✅ [1, 3, 6, 10]  (1, 1+2, 1+2+3, 1+2+3+4)

# Custom function: cumulative product
list(itertools.accumulate([1, 2, 3, 4], operator.mul))
# ✅ [1, 2, 6, 24]

# Track maximum
list(itertools.accumulate([3, 1, 4, 2], max))
# ✅ [3, 3, 4, 4]
```

### `chain(*iterables)`

Flattens multiple iterables into one sequence.

```python
# Chain multiple iterables
list(itertools.chain('ABC', [1, 2], {3, 4}))
# ✅ ['A', 'B', 'C', 1, 2, 3, 4] (set order may vary)

# Chain with generators
def gen1(): yield 'a'; yield 'b'
def gen2(): yield 'c'; yield 'd'
list(itertools.chain(gen1(), gen2()))
# ✅ ['a', 'b', 'c', 'd']
```

### `chain.from_iterable(iterable)`

Like `chain()`, but takes a single iterable of iterables.

```python
# Better for chained iterables
list(itertools.chain.from_iterable(['ABC', 'DEF']))
# ✅ ['A', 'B', 'C', 'D', 'E', 'F']

# Useful with generator expressions
list(itertools.chain.from_iterable(
    [i, i*2] for i in range(3)))
# ✅ [0, 0, 1, 2, 2, 4]
```

### `compress(data, selectors)`

Filters elements from data using selector bits.

```python
list(itertools.compress('ABCDEF', [1, 0, 1, 0, 1, 1]))
# ✅ ['A', 'C', 'E', 'F']

# Practical: filter by condition
names = ['Alice', 'Bob', 'Charlie', 'Dave']
ages = [25, 30, 35, 40]
adults = [age >= 30 for age in ages]

list(itertools.compress(names, adults))
# ✅ ['Bob', 'Charlie', 'Dave']
```

### `dropwhile(pred, iterable)`

Drops items while predicate is true.

```python
list(itertools.dropwhile(lambda x: x < 5, [1, 4, 6, 7, 8]))
# ✅ [6, 7, 8]

# Practical: skip header lines
lines = ['---', 'Header', 'Data1', 'Data2']
list(itertools.dropwhile(lambda x: x.startswith('-'), lines))
# ✅ ['Data1', 'Data2']
```

### `takewhile(pred, iterable)`

Takes items while predicate is true.

```python
list(itertools.takewhile(lambda x: x < 5, [1, 4, 6, 7, 8]))
# ✅ [1, 4]

# Practical: collect until condition fails
values = [10, 20, 30, 5, 40]
list(itertools.takewhile(lambda x: x > 15, values))
# ✅ [20, 30]
```

### `filterfalse(pred, iterable)`

Filters items where predicate is false.

```python
list(itertools.filterfalse(lambda x: x % 2, range(10)))
# ✅ [0, 2, 4, 6, 8]

# Practical: filter out None values
data = [1, None, 2, None, 3]
list(itertools.filterfalse(lambda x: x is None, data))
# ✅ [1, 2, 3]
```

### `groupby(iterable, key=None)`

Groups consecutive items with the same key.

```python
# Basic grouping
for key, grp in itertools.groupby('AABBBCC'):
    print(key, list(grp))
# A ['A', 'A']
# B ['B', 'B']
# C ['C', 'C']

# With key function
data = [('apple', 1), ('avocado', 2), ('banana', 3)]
for key, grp in itertools.groupby(data, lambda x: x[0][0]):
    print(key, list(grp))
# a [('apple', 1), ('avocado', 2)]
# b [('banana', 3)]

⚠️ **Note**: `groupby` groups *consecutive* items only. Sort first if needed!
```

### `islice(iterable, start, stop[, step])`

Slices an iterator (like `list[start:stop:step]`).

```python
# Basic slicing
list(itertools.islice('ABCDEFG', 2, 7, 2))
# ✅ ['C', 'E', 'G']

# Equivalent to list slicing
lst = [0, 1, 2, 3, 4, 5]
list(itertools.islice(lst, 1, 5)) == lst[1:5]
# ✅ True

# With None for open-ended slices
list(itertools.islice(range(10), 3, None))
# ✅ [3, 4, 5, 6, 7, 8, 9]
```

### `starmap(func, iterable)`

Applies function to unpacked arguments.

```python
# Normal map: func receives tuple argument
list(map(lambda x: pow(*x), [(2, 5), (3, 2)]))
# ✅ [32, 9]

# starmap: unpacks tuple automatically
list(itertools.starmap(pow, [(2, 5), (3, 2)]))
# ✅ [32, 9]

# Practical: calculate distances
points = [(0, 0), (3, 4), (5, 12)]
import math
list(itertools.starmap(math.hypot, points))
# ✅ [0.0, 5.0, 13.0]
```

### `tee(iterable, n=2)`

Creates n independent iterators from one.

```python
# Create 2 independent copies
it1, it2 = itertools.tee('ABC', 2)
list(it1), list(it2)  # (['A','B','C'], ['A','B','C'])

⚠️ **Caution**: After tee, the original iterator should not be used!
```

### `zip_longest(*iterables, fillvalue=None)`

Zips iterators to longest length.

```python
list(itertools.zip_longest('ABC', 'XY', fillvalue='-'))
# ✅ [('A','X'), ('B','Y'), ('C','-')]

# Compare with normal zip
list(zip('ABC', 'XY'))  # Only goes to shortest: [('A','X'), ('B','Y')]
```

---

## 🎲 Combinatoric Iterators

These generate combinatorial combinations.

### `product(*iterables, repeat=1)`

Cartesian product of input iterables.

```python
list(itertools.product('AB', range(3)))
# ✅ [('A',0), ('A',1), ('A',2), ('B',0), ('B',1), ('B',2)]

# Repeat parameter
list(itertools.product('AB', repeat=2))
# ✅ [('A','A'), ('A','B'), ('B','A'), ('B','B')]

# Practical: generate all 3-digit binary numbers
list(itertools.product('01', repeat=3))
# ✅ [('0','0','0'), ('0','0','1'), ..., ('1','1','1')]
```

### `permutations(iterable, r=None)`

All possible orderings of length r.

```python
list(itertools.permutations('ABC', 2))
# ✅ [('A','B'), ('A','C'), ('B','A'), ('B','C'), ('C','A'), ('C','B')]

# Full permutations (r=None means len(iterable))
list(itertools.permutations('ABC'))
# ✅ [('A','B','C'), ('A','C','B'), ('B','A','C'), ...] (6 total)
```

### `combinations(iterable, r)`

All possible combinations of length r (no repeats).

```python
list(itertools.combinations('ABC', 2))
# ✅ [('A','B'), ('A','C'), ('B','C')]

# Number of combinations: nCr = n! / (r! * (n-r)!)
import math
n, r = 5, 2
print(math.comb(n, r))  # ✅ 10
```

### `combinations_with_replacement(iterable, r)`

Combinations where elements can repeat.

```python
list(itertools.combinations_with_replacement('ABC', 2))
# ✅ [('A','A'), ('A','B'), ('A','C'), ('B','B'), ('B','C'), ('C','C')]

# Compare with regular combinations
list(itertools.combinations('ABC', 2))  # No repeats: [('A','B'), ('A','C'), ('B','C')]
```

---

## 🛠️ Common Patterns & Recipes

### `pairwise(iterable)`

Iterate over overlapping pairs (Python 3.10+ has built-in).

```python
def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)  # Advance one iterator
    return zip(a, b)

list(pairwise('ABCD'))  # ✅ [('A','B'), ('B','C'), ('C','D')]

# Practical: calculate differences
data = [10, 15, 13, 18]
list(pairwise(data))          # [(10,15), (15,13), (13,18)]
[d2 - d1 for d1, d2 in pairwise(data)]  # [5, -2, 5]
```

### `window(iterable, n)`

Sliding window of size n.

```python
def window(iterable, n):
    iterators = itertools.tee(iterable, n)
    for i, it in enumerate(iterators):
        for _ in range(i):
            next(it, None)
    return zip(*iterators)

list(window(range(10), 3))
# ✅ [(0,1,2), (1,2,3), ..., (7,8,9)]

# With islice for fixed size
def sliding_window(iterable, n):
    return itertools.islice(
        (tuple(itertools.islice(it, n)) for it in itertools.tee(iterable)),
        len(list(iterable)) - n + 1
    )
```

---

## ⚡ Performance Notes

- **No intermediate lists**: `itertools` functions return iterators, computing values lazily
- **Memory efficient**: Great for large datasets
- **Composable**: Functions chain without creating temporary lists
- **C implementation**: Faster than pure Python equivalents

```python
# ✅ Memory efficient: no list created
total = sum(itertools.islice(range(1_000_000), 0, None, 2))

# ❌ Memory inefficient: creates huge list
total = sum(list(range(1_000_000))[::2])
```

---

## ⚠️ Common Pitfalls

### 1. Infinite loops without termination

Infinite iterators require explicit termination:

```python
# ❌ Infinite loop!
for i in itertools.count():
    print(i)  # Runs forever

# ✅ Add break condition
for i in itertools.count():
    if i > 10:
        break
    print(i)
```

### 2. Forgetting `list()` for single use

`tee()` creates independent iterators—using one exhausts the original:

```python
a, b = itertools.tee('ABC')

# ❌ Only works once!
list(a)  # ['A', 'B', 'C']
list(b)  # [] (already exhausted)

# ✅ Use list() to save results
a, b = itertools.tee('ABC')
a_list = list(a)  # Save first iterator
list(b)           # Now works: ['A', 'B', 'C']
```

---

## 🔗 Further Reading

- [Python docs: `itertools`](https://docs.python.org/3/library/itertools.html)
- [Python docs: Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Python docs: `islice`](https://docs.python.org/3/library/itertools.html#itertools.islice)
- [Python docs: `groupby`](https://docs.python.org/3/library/itertools.html#itertools.groupby)
- [Python docs: `zip_longest`](https://docs.python.org/3/library/itertools.html#itertools.zip_longest)
