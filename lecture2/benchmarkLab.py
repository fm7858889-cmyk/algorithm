import random
import time
import sys

sys.setrecursionlimit(10000)


# ---------- Algorithms ----------

def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    pivot = random.choice(arr)   # random pivot: avoids worst case on sorted input
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)


def builtin_sort(arr):
    return sorted(arr)


# ---------- Inputs ----------

def make_input(kind, n):
    if kind == "sorted":
        return list(range(n))
    elif kind == "reversed":
        return list(range(n, 0, -1))
    else:  # random
        data = list(range(n))
        random.shuffle(data)
        return data


# ---------- Benchmark ----------

ALGORITHMS = {
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "builtin": builtin_sort,
}

INSERTION_LIMIT = 5000    # insertion sort is slow above this size in Python
SIZES = [1000, 2000, 5000, 10000, 20000]
KINDS = ["sorted", "reversed", "random"]
REPEATS = 2               # best of 2 runs is enough for this experiment


def time_one(func, data):
    start = time.perf_counter()
    func(data)
    return time.perf_counter() - start


def benchmark():
    results = []  # list of (kind, n, algo, best_time)
    for kind in KINDS:
        for n in SIZES:
            data_list = [make_input(kind, n) for _ in range(REPEATS)]  # built before timing
            for name, func in ALGORITHMS.items():
                if name == "insertion" and n > INSERTION_LIMIT:
                    continue
                best = min(time_one(func, data) for data in data_list)
                results.append((kind, n, name, best))
                print(f"{kind:>9} n={n:>6} {name:>10}: {best:.6f} s", flush=True)
    return results


def print_table(results):
    for kind in KINDS:
        print(f"\n===== Input: {kind} =====")
        print(f"{'n':>8} {'insertion':>12} {'merge':>12} {'quick':>12} {'builtin':>12}")
        for n in SIZES:
            row = {}
            for k, sz, name, t in results:
                if k == kind and sz == n:
                    row[name] = t
            ins = f"{row['insertion']:.6f}" if "insertion" in row else "skipped"
            print(f"{n:>8} {ins:>12} {row['merge']:>12.6f} {row['quick']:>12.6f} {row['builtin']:>12.6f}")


if __name__ == "__main__":
    random.seed(42)
    results = benchmark()
    print_table(results)