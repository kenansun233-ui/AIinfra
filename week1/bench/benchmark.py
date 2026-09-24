from AIinfra.week1.src.log_stats import benchmark, generate_log
from pathlib import Path

output_path = Path("AIinfra/week1/results/raw.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

bench_dir = Path("AIinfra/week1/bench")
bench_dir.mkdir(parents=True, exist_ok=True)

print("--开始测试--")

with open(output_path, "w") as f:
    f.write("n\t run\t elapsed_s\t lines_per_second\n")

for i in [2,  4,  6]:
    n = 10 ** i
    path = bench_dir / f"bench_{n}.log"
    generate_log(path, n)
    benchmark(path)

    for run in range(3):
        elapsed, lines_per_second, total_number = benchmark(path)
        with open(output_path, "a") as f:
            f.write(
                f"{n}\t"
                f"{run + 1}\t"
                f"{elapsed:.6f}\t"
                f"{lines_per_second:.2f}\n"
            )
            if run == 2:
                f.write(f"\n")
print("--测试完成--")