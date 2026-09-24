import sys
from pathlib import Path

# 让 pytest 能找到 src/log_stats.py
src_dir = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_dir))

from log_stats import analyze_log


def test_empty_log(tmp_path):
    log_file = tmp_path / "empty.log"
    log_file.write_text("")

    result = analyze_log(log_file)

    assert result["total_number"] == 0
    assert result["valid_requests"] == 0
    assert result["invalid_lines"] == 0
    assert result["sorted_latencies"] == []
    assert result["p50_ms"] == 0
    assert result["p95_ms"] == 0
    assert result["error_rate"] == 0


def test_single_log(tmp_path):
    log_file = tmp_path / "single.log"
    log_file.write_text(
        "2026-09-21T20:00:00Z 200 34.7\n"
    )

    result = analyze_log(log_file)

    assert result["total_number"] == 1
    assert result["valid_requests"] == 1
    assert result["invalid_lines"] == 0
    assert result["mean_ms"] == 34.7
    assert result["p50_ms"] == 34.7
    assert result["p95_ms"] == 34.7


def test_invalid_lines(tmp_path):
    log_file = tmp_path / "invalid.log"

    log_file.write_text(
        """2026-09-21T20:00:00Z 200 34.7
bad_timestamp 404 25.6
2026-09-21T20:00:02Z abc 45.2
2026-09-21T20:00:03Z 200 xyz
2026-09-21T20:00:04Z 404
"""
    )

    result = analyze_log(log_file)

    assert result["total_number"] == 5
    assert result["valid_requests"] == 1
    assert result["invalid_lines"] == 4
    assert result["error_rate"] == 0


def test_error_rate(tmp_path):
    log_file = tmp_path / "error.log"

    log_file.write_text(
        """2026-09-21T20:00:00Z 200 20.0
2026-09-21T20:00:01Z 404 30.0
2026-09-21T20:00:02Z 500 40.0
2026-09-21T20:00:03Z 302 50.0
"""
    )

    result = analyze_log(log_file)

    assert result["total_number"] == 4
    assert result["valid_requests"] == 4
    assert result["invalid_lines"] == 0
    assert result["error_rate"] == 0.5
    assert result["mean_ms"] == 35.0