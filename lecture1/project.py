import random
import time

# ===== 1. Implement =====
def insertion_sort(arr):
    a = arr[:]  # copy so the original list is not modified
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def insertion_sort_count(arr):
    # Same algorithm, but it also counts comparisons and shifts.
    # Used only for the report, not for timing.
    comparisons = 0
    shifts = 0
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comparisons, shifts


# ===== 2. Experiment =====
def make_input(kind, n):
    if kind == "sorted":
        return list(range(n))
    elif kind == "reverse":
        return list(range(n, 0, -1))
    else:  # random
        data = list(range(n))
        random.shuffle(data)
        return data


def measure(kind, sizes, repeats=3):
    times = []
    for n in sizes:
        best = float("inf")
        for _ in range(repeats):
            data = make_input(kind, n)       # created before the timer starts
            start = time.perf_counter()
            insertion_sort(data)
            best = min(best, time.perf_counter() - start)
        times.append(best)
    return times


# Sizes double each time, which makes the growth easy to read
sizes = [250, 500, 1000, 2000, 4000]

results = {
    "sorted": measure("sorted", sizes),
    "reverse": measure("reverse", sizes),
    "random": measure("random", sizes),
}


# ===== 3. Analyze =====
print("\n--- Results table (time in seconds) ---")
print(f"{'n':>6} {'sorted':>12} {'reverse':>12} {'random':>12}")
for i, n in enumerate(sizes):
    print(f"{n:>6} {results['sorted'][i]:>12.6f} {results['reverse'][i]:>12.6f} {results['random'][i]:>12.6f}")

print("\n--- Time ratio when n doubles ---")
print("Ratio near 2 means O(n), ratio near 4 means O(n^2).")
for kind in ["sorted", "reverse", "random"]:
    ratios = [results[kind][i] / results[kind][i - 1] for i in range(1, len(sizes))]
    print(f"{kind:>8}: " + ", ".join(f"{r:.2f}" for r in ratios))


# ===== 4. Report =====
def count_summary(n):
    print(f"\n--- Comparisons and shifts for n = {n} ---")
    for kind in ["sorted", "reverse", "random"]:
        _, comp, shifts = insertion_sort_count(make_input(kind, n))
        print(f"{kind:>8}: comparisons = {comp:>10}, shifts = {shifts:>10}")

count_summary(1000)