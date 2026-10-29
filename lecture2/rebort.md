# Sorting Benchmark Lab: Empirical Comparison of Four Sorting Methods

## 1. Problem

Sorting is one of the most common operations in computing. Several algorithms solve it with
different running times, and the best choice can depend on the shape of the input. This project
asks: how do Insertion Sort, Merge Sort, Quick Sort, and Python's built-in `sorted()` compare on
sorted, reversed, and random inputs as the input size n grows?

## 2. Method

Four algorithms were implemented in Python:

- **Insertion Sort**: repeatedly inserts the next element into the sorted part of the list.
- **Merge Sort**: splits the list in half, sorts each half recursively, and merges the results.
- **Quick Sort**: chooses a random pivot, partitions the list into less / equal / greater, and recurses.
- **Built-in `sorted()`**: Python's Timsort, used as a reference.

Three input types were used: sorted (`1, 2, ..., n`), reversed (`n, ..., 2, 1`), and random
permutations. Sizes were n = 1000, 2000, 5000, 10000, and 20000. Insertion Sort was only
measured up to n = 5000. Each timing is the best of 2 runs using `time.perf_counter()`.

Correctness was checked with unit tests that compare each algorithm's output to `sorted()` on
empty lists, single elements, duplicates, negative numbers, and random inputs.

## 3. Complexity Analysis

| Algorithm | Best case | Average case | Worst case | Extra memory |
|---|---|---|---|---|
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort (random pivot) | O(n log n) | O(n log n) | O(n²) | O(n) in this implementation |
| Built-in `sorted()` | O(n) | O(n log n) | O(n log n) | O(n) |

**Insertion Sort.** On a sorted input, each element is compared once with the element before it and
no shifts happen, so the work is O(n). On a reversed input, element i must be shifted past all i
previous elements, which gives about n(n−1)/2 comparisons and shifts, so the work is O(n²). On a random
input, each element moves about halfway back on average, which is still quadratic.

**Merge Sort.** The recursion has depth log n, and each level does O(n) work for merging, so the
total is O(n log n) for every input.

**Quick Sort.** A random pivot makes the expected depth of recursion O(log n), so the expected time
is O(n log n). The worst case O(n²) is very unlikely with random pivots. This implementation builds
new lists at every step, which is why its memory use is O(n).

**Built-in `sorted()`.** Timsort finds runs of already ordered data, so sorted and reversed inputs
take close to O(n). Random inputs take O(n log n).

## 4. Experiments

Fill in the table below with the numbers from your own run of `sorting_benchmark.py`.

### 4.1 Running time on random input (seconds)

| n | Insertion | Merge | Quick | Built-in |
|---|---|---|---|---|
| 1000 | [your value] | [your value] | [your value] | [your value] |
| 5000 | [your value] | [your value] | [your value] | [your value] |
| 10000 | skipped | [your value] | [your value] | [your value] |
| 20000 | skipped | [your value] | [your value] | [your value] |

### 4.2 Effect of input type on Insertion Sort

Compare the sorted and reversed rows for n = 5000. For each, write the time and the ratio
reversed / sorted. A large ratio shows how much the number of shifts matters.

### 4.3 Growth when n doubles

For Insertion Sort on reversed input, compute time(2000) / time(1000). Values close to 4 indicate O(n²). For Merge Sort, values close to 2 (a bit more)
indicate O(n log n).

## 5. Discussion

Describe what your numbers show. Expected observations:

- Insertion Sort is fastest on sorted input and slowest on reversed input, and the difference grows with n.
- Merge Sort and Quick Sort behave similarly on random data, and both are far faster than Insertion Sort for large n.
- Built-in `sorted()` is much faster than all three hand-written algorithms, because Timsort is
  written in C and it takes advantage of ordered runs in the data.

Also explain why the number of shifts, not just the number of elements, drives the cost of Insertion Sort.

## 6. Conclusion

Insertion Sort is simple and fast on small or nearly sorted data, but its quadratic growth makes it
impractical for large random inputs. Merge Sort and Quick Sort scale much better. In practice,
a library sort such as Python's `sorted()` is the best choice, but writing the algorithms by hand
is useful for understanding why these differences exist.