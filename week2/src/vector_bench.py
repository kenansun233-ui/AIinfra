import numpy as np
import time
from collections import defaultdict
import statistics
import csv
from pathlib import Path

def python_add(a, b):
    # 使用 for 循环进行逐元素加法
    # 不使用 NumPy
    result = [0.0] * len(a)
    for i in range(len(a)):
        result[i] = a[i] + b[i]
    return result

def numpy_add(a, b):
    # 使用 NumPy 进行向量化加法
    return a + b

def benchmark(func, a, b, warmup, repeat):
    times_ns = []
    # Step 1: 预热
    for _ in range(warmup):
        func(a, b)
    # Step 2: 独立计时
    for _ in range(repeat):
        start_ns = time.perf_counter_ns()
        func(a, b)
        end_ns = time.perf_counter_ns()
        elapsed_ns = end_ns - start_ns
        times_ns.append(elapsed_ns)
    return times_ns

def effective_bandwidth(n, median_ns):
    if median_ns <= 0:
        raise ValueError("median_ns must be positive")

    logical_bytes = 3 * n * 8
    median_seconds = median_ns / 1e9
    BW = logical_bytes / median_seconds
    return BW / 1e9  # 单位：GB/s

def analyze_csv(file_path):
    groups = defaultdict(list)

    # Step 1: 读取 CSV
    with open(
        file_path,
        "r",
        encoding="utf-8",
        newline=""
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:
            n = int(row["n"])
            name = row["implementation"]
            elapsed_ns = int(row["elapsed_ns"])

            key = (n, name)
            groups[key].append(elapsed_ns)

    # Step 2: 检查数据是否为空
    assert groups, "CSV contains no measurements"
    return groups

if __name__ == "__main__":
    rows = []
    for N in [1000, 10000, 100000, 10000000]:  # 重复三次测试
        a = [float(i) for i in range(N)]
        b = [float(i) for i in range(N)]
        a_np = np.asarray(a, dtype=np.float64)
        b_np = np.asarray(b, dtype=np.float64)
        python_result = python_add(a, b)
        numpy_result = numpy_add(a_np, b_np)
        assert np.allclose(python_result, numpy_result)
        assert len(a) == len(python_result)
        assert len(a_np) == len(numpy_result)
        python_times = benchmark(python_add, a, b, 5, 30)
        numpy_times = benchmark(numpy_add, a_np, b_np, 5, 30)

        for name, times in [("python", python_times),("numpy", numpy_times),]:
             for i, elapsed_ns in enumerate(times, start=1):
                 rows.append([ N, name, i, elapsed_ns, a_np.nbytes + b_np.nbytes,])

        python_median = statistics.median(python_times)/1e6
        numpy_median = statistics.median(numpy_times)/1e6
        p95_python = np.percentile(python_times, 95)/1e6
        p95_numpy = np.percentile(numpy_times, 95)/1e6
        speedup = python_median / numpy_median
        print(f"Vector addition benchmark for N={N}:")
        print("--------------------------------")
        print("Python measurements:", len(python_times))
        print("NumPy measurements:", len(numpy_times))
        print(f"Python median: {python_median:.6f} ms")
        print(f"Python p95: {p95_python:.6f} ms")
        print(f"NumPy median: {numpy_median:.6f} ms")
        print(f"NumPy p95: {p95_numpy:.6f} ms")
        print(f"Speedup: {speedup:.2f}x")
        print("All tests passed!")
        print("--------------------------------")
        
    output = Path("AIinfra/week2/results/raw.csv")
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="", encoding="utf-8") as f:
         writer = csv.writer(f)
         writer.writerow([
                "n", "implementation", "repeat",
             "elapsed_ns", "input_bytes"])
         writer.writerows(rows)