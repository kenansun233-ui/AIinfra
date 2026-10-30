from vector_bench import  analyze_csv
import statistics
import matplotlib.pyplot as plt
from pathlib import Path
groups_csv_path = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "raw.csv"
)
groups = analyze_csv(groups_csv_path)
assert groups, "No benchmark data found"
sizes = sorted(set(n for n, _ in groups.keys()))
for n in sizes:
    for name in ["python", "numpy"]:
        key = (n, name)
        assert key in groups, f"Missing group: {key}"
        assert len(groups[key]) == 30, (
            f"{key}: expected 30 samples, "
            f"got {len(groups[key])}"
        )

python_ms = []
numpy_ms = []

for n in sizes:
    python_times = groups[(n, "python")]
    numpy_times = groups[(n, "numpy")]

    python_ms.append(
        statistics.median(python_times) / 1e6
    )

    numpy_ms.append(
        statistics.median(numpy_times) / 1e6
    )


fig, ax = plt.subplots()

ax.plot(
    sizes,
    python_ms,
    marker="o",
    label="Python"
)

ax.plot(
    sizes,
    numpy_ms,
    marker="s",
    label="NumPy"
)

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_xlabel("Vector Size N")
ax.set_ylabel("Median Time (ms)")
ax.set_title("Python vs NumPy Vector Addition")

ax.legend()
ax.grid(True, which="both", alpha=0.3)

output_path = groups_csv_path.parent / "median_time.png"

fig.savefig(
    output_path,
    dpi=200,
    bbox_inches="tight"
)

plt.show()