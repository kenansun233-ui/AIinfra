import sys
import time
import random
from datetime import datetime

def generate_log(path, n):
    with open(path, "w") as f:
        for _ in range(n):
            status = random.choice([200, 200, 200, 404, 500])
            latency = random.uniform(10.0, 200.0)
            f.write(f"2026-09-21T20:00:00Z {status} {latency:.2f}\n")

def benchmark(path):
    start = time.perf_counter()

    result = analyze_log(path)

    end = time.perf_counter()
    elapsed = end - start
    total_number = result["total_number"]
    lines_per_second = result["total_number"] / elapsed

    return elapsed, lines_per_second, total_number

def analyze_log(log_address):

    sorted_latencies=[]
    latencies = []
    valid_requests = 0
    invalid_lines = 0
    total_number = 0
    error_requests = 0

    with open(log_address, "r") as f:

        for line_number, line in enumerate(f, start=1):

            parts = line.split()
            total_number += 1

            if len(parts) != 3:
                # 坏行
                print(f"invalid line {line_number}: {line.strip()}")
                invalid_lines += 1
                continue
            try:
                status = int(parts[1])
                latency = float(parts[2])
                timestamp = parts[0]
                dt = datetime.fromisoformat(timestamp.replace("Z","+00:00"))
            except (ValueError, OverflowError):
                # 坏行
                print(f"invalid line {line_number}: {line.strip()}")
                invalid_lines += 1
                continue
            if status >= 400:
                error_requests += 1

            valid_requests += 1
            latencies.append(latency)

        if valid_requests > 0:
            avgLatency = sum(latencies) / valid_requests
            error_rate = error_requests / valid_requests
            sorted_latencies = sorted(latencies)
            P95 = percentile(sorted_latencies , 0.95)
            P50 = percentile(sorted_latencies , 0.5)
        else:
            avgLatency = 0
            error_rate = 0
            P50 = 0
            P95 = 0

    result = {
    "sorted_latencies":sorted_latencies,
    "total_number":total_number, 
    "valid_requests": valid_requests,
    "invalid_lines": invalid_lines,
    "mean_ms": avgLatency,
    "p50_ms": P50,
    "p95_ms": P95,
    "error_rate": error_rate,}

    return result


def percentile(sorted_latencies, p):
    n = len(sorted_latencies)
    position = (n - 1) * p
    lower = int(position)
    upper = lower + 1
    fraction = position - lower
    if lower == n - 1:
       return sorted_latencies[n - 1]
    else:
       return sorted_latencies[lower] + fraction * (sorted_latencies[upper] - sorted_latencies[lower])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请在脚本后追加 log 地址")
        sys.exit(1)

    log_address = sys.argv[1]

    result = analyze_log(log_address)

    print(result)
    print(f"p95_ms: {result['p95_ms']:.2f}")
    
    #unordered_map<string, double> result;
    #result["p95_ms"]