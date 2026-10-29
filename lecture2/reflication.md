# Reflection

**What surprised me:**
Python's built-in `sorted()` was much faster than my own implementations, even on large random inputs.
I expected Merge Sort and Quick Sort to be closer to it. The reason is that Timsort is written in C,
and it also detects runs of already-sorted data, which my code does not do.

Another surprise was how quickly Insertion Sort becomes impractical. Going from 1000 to 10000
elements made its running time grow much faster than the input size, which made the O(n²) behavior
very clear in the numbers.

**What I would do next:**
- Try a hybrid sort that switches to Insertion Sort below a small size k, and find the best k
  by measuring (this is the next project in the list).
- Improve Quick Sort to sort in place, so its memory use is O(log n) instead of O(n).
- Test on more realistic data, such as nearly sorted lists, lists with many duplicates, or real data from a file.
-