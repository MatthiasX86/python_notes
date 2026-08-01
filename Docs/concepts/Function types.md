### 📊 Built-In Operations on Sequences/Collections

| Category      | Operation     | Native Syntax/Function                                           | Example                                                                     |
| ------------- | ------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Aggregate** | Sum           | `sum()`                                                          | `sum([1,2,3])` → `6`                                                        |
|               | Min/Max       | `min()`, `max()`                                                 | `min([1,2,3])` → `1`                                                        |
|               | Count         | `len()`                                                          | `len([1,2,3])` → `3`                                                        |
|               | Truthy Check  | `any()`, `all()`                                                 | `any([False, True])` → `True`                                               |
| **Transform** | Map           | `map()`                                                          | `list(map(str, [1,2]))` → `['1','2']`                                       |
|               | Comprehension | `[x*2 for x in ...]`                                             | `[x**2 for x in range(3)]` → `[0,1,4]`                                      |
|               | Generator Exp | `(x*2 for x in ...)`                                             | `tuple(x**2 for x in range(3))`                                             |
| **Filter**    | Filter        | `filter()`                                                       | `list(filter(bool, [0,1,2]))` → `[1,2]`                                     |
|               | Comprehension | `[x for x in ... if ...]`                                        | `[x for x in range(5) if x%2==0]`                                           |
| **Partition** | Comprehension | (two lists)                                                      | `evens = [x for x in nums if not x%2]`<br>`odds = [x for x in nums if x%2]` |
| **Zip/Join**  | Zip           | `zip()`                                                          | `list(zip([1,2], ['a','b']))` → `[(1,'a'),(2,'b')]`                         |
| **Unpack**    | Star `*`      | `a, *rest = [1,2,3]`                                             | → `a=1`, `rest=[2,3]`                                                       |
| **Scan**      | Accumulate    | `itertools.accumulate()`⚠️<br>_(not built-in)_ → use manual scan |                                                                             |

⚠️ **Note**: `itertools.accumulate()` is _not_ built-in — but you can mimic scan behavior with a simple comprehension:

```python
# Cumulative sum (scan) using only built-ins:
lst = [1, 2, 3]
cumsum = []
running_total = 0
for x in lst:
    running_total += x
    cumsum.append(running_total)
# → [1, 3, 6]

# Or with list comprehension (less efficient):
cumsum = [sum(lst[:i+1]) for i in range(len(lst))]
```

> ✅ All operations above use **only built-ins**: `sum()`, `map()`, `filter()`, list comprehensions, `zip()`, unpacking.

---

### 🧠 Relationship Summary

| Concept     | Built-In Tools                                           |
| ----------- | -------------------------------------------------------- |
| Aggregate   | `sum()`, `min()`, `max()`, `len()`, `any()`, `all()`     |
| Transform   | `map()`, list/dict comprehensions, generator expressions |
| Filter      | `filter()`, list/dict comprehensions                     |
| Partition   | Multiple comprehensions or conditionals                  |
| Zip/Join    | `zip()`, unpacking (`*`)                                 |
| Scan (scan) | Manual loop or nested `sum()` — no native built-in       |

You can build **all** other sequence transformations using only these primitives.
