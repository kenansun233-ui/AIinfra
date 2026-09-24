import pytest
from AIinfra.week1.src.log_stats import analyze_log

def test_error_lines(tmp_path):
    log_file = tmp_path / "error.log"

    log_file.write_text("""2026-09-21T20:00:00Z 200 18.5
2026-09-21T20:00:01Z 200 27.0
2026-09-21T20:00:02Z 404 33.5
2026-09-21T20:00:03Z 200 41.0
2026-09-21T20:00:04Z 500 52.5
2026-09-21T20:00:05Z 200 68.0
2026-09-21T20:00:06Z 200 79.5
2026-09-21T20:00:07Z 503 95.0
2026-09-21T20:00:08Z 200 140.0
2026-09-21T20:00:09Z 200 220.0""")

    result = analyze_log(log_file)

    assert result["sorted_latencies"] == [18.5, 27.0, 33.5, 41.0, 52.5, 68.0, 79.5, 95.0, 140.0, 220.0]
    assert result["total_number"] == 10
    assert result["valid_requests"] == 10
    assert result["invalid_lines"] == 0
    assert result["mean_ms"] == pytest.approx(77.5)
    assert result["p50_ms"] == pytest.approx(60.25)
    assert result["p95_ms"] == pytest.approx(184.0)
    assert result["error_rate"] == pytest.approx(0.3)