import math
import random
import sys
import time
import unittest


# ---------- Heap operations ----------

class Recorder:
    """Records each swap so the steps can be shown or counted."""

    def __init__(self, snapshots=False):
        self.snapshots = snapshots   # store full array copies only when needed
        self.events = []             # list of (kind, i, j, array_copy, heap_size)

    def add(self, kind, i, j, a, heap_size):
        snap = a[:] if self.snapshots else None
        self.events.append((kind, i, j, snap, heap_size))


def max_heapify(a, i, heap_size, recorder=None):
    """Move a[i] down until the subtree rooted at i is a max-heap."""
    left = 2 * i + 1
    right = 2 * i + 2
    largest = i
    if left < heap_size and a[left] > a[largest]:
        largest = left
    if right < heap_size and a[right] > a[largest]:
        largest = right
    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        if recorder is not None:
            recorder.add("swap", i, largest, a, heap_size)
        max_heapify(a, largest, heap_size, recorder)


def build_max_heap(a, recorder=None):
    """Turn the whole array into a max-heap, starting from the last parent."""
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(a, i, n, recorder)


def heap_sort(arr, recorder=None):
    """Return a sorted copy of arr using heap sort."""
    if recorder is None:
        recorder = Recorder()
    a = arr[:]
    build_max_heap(a, recorder)
    for end in range(len(a) - 1, 0, -1):
        a[0], a[end] = a[end], a[0]          # move the max to its final place
        recorder.add("extract", 0, end, a, end)
        max_heapify(a, 0, end, recorder)     # restore the heap on the rest
    return a


def is_max_heap(a, heap_size):
    for i in range(heap_size):
        for child in (2 * i + 1, 2 * i + 2):
            if child < heap_size and a[child] > a[i]:
                return False
    return True


# ---------- Visualizer ----------

def print_tree(a, heap_size):
    """Print the heap level by level (level 0 is the root)."""
    if heap_size == 0:
        print("  (empty heap)")
        return
    level, start = 0, 0
    while start < heap_size:
        end = min(start + 2 ** level, heap_size)
        row = "   ".join(str(a[i]) for i in range(start, end))
        print(f"  level {level}: {row}")
        start = end
        level += 1


def visualize(arr):
    print(f"Input array: {arr}")
    print("Input as a tree (not a heap yet):")
    print_tree(arr, len(arr))
    print()

    recorder = Recorder(snapshots=True)
    result = heap_sort(arr, recorder)

    for number, (kind, i, j, snapshot, heap_size) in enumerate(recorder.events, 1):
        if kind == "extract":
            print(f"Step {number}: move the max ({snapshot[j]}) to position {j}, heap size is now {heap_size}")
        else:
            print(f"Step {number}: swap positions {i} and {j}")
        print_tree(snapshot, heap_size)
        print()

    print(f"Total steps: {len(recorder.events)}")
    print(f"Sorted output: {result}")


# ---------- Experiment ----------

def experiment():
    random.seed(1)
    print(f"{'n':>8} {'operations':>12} {'time (s)':>10} {'ops / (n log2 n)':>18}")
    for n in [1000, 5000, 10000, 50000, 100000]:
        data = list(range(n))
        random.shuffle(data)
        recorder = Recorder()          # no snapshots, so memory stays small
        start = time.perf_counter()
        heap_sort(data, recorder)
        elapsed = time.perf_counter() - start
        ops = len(recorder.events)
        ratio = ops / (n * math.log2(n))
        print(f"{n:>8} {ops:>12} {elapsed:>10.4f} {ratio:>18.3f}")


# ---------- Unit tests ----------

class TestHeapSort(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(heap_sort([]), [])

    def test_single(self):
        self.assertEqual(heap_sort([7]), [7])

    def test_sorted_input(self):
        self.assertEqual(heap_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reversed_input(self):
        self.assertEqual(heap_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_duplicates(self):
        self.assertEqual(heap_sort([3, 1, 3, 2, 1]), [1, 1, 2, 3, 3])

    def test_negative_numbers(self):
        self.assertEqual(heap_sort([-3, 0, -1, 5, -10]), [-10, -3, -1, 0, 5])

    def test_random_inputs_match_sorted(self):
        rng = random.Random(0)
        for _ in range(200):
            data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
            self.assertEqual(heap_sort(data), sorted(data))

    def test_original_not_modified(self):
        data = [3, 1, 2]
        heap_sort(data)
        self.assertEqual(data, [3, 1, 2])

    def test_max_heapify_fixes_root(self):
        a = [1, 9, 8, 2, 3]   # root violates the max-heap property
        max_heapify(a, 0, len(a))
        self.assertTrue(is_max_heap(a, len(a)))

    def test_build_max_heap(self):
        a = [4, 10, 3, 5, 1]
        build_max_heap(a)
        self.assertTrue(is_max_heap(a, len(a)))

    def test_recorder_counts_one_extract_per_element(self):
        recorder = Recorder()
        heap_sort([3, 1, 2, 5], recorder)
        extracts = [e for e in recorder.events if e[0] == "extract"]
        self.assertEqual(len(extracts), 3)


# ---------- Main ----------

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--test" in args:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    elif "--experiment" in args:
        experiment()
    else:
        numbers = [int(x) for x in args] or [4, 10, 3, 5, 1]
        visualize(numbers)