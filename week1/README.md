# Week 01 — Python Log Analyzer

## 1. Project Overview

本项目实现一个简单的 Python 日志分析工具，用于读取 HTTP 请求日志并统计基本指标。

主要功能包括：

* 统计日志总行数
* 统计有效请求数量
* 统计损坏日志数量
* 计算平均延迟
* 计算 P50 延迟
* 计算 P95 延迟
* 计算 HTTP 错误率
* 使用 pytest 进行单元测试
* 使用 benchmark 脚本测试日志解析性能

---

## 2. Log Format

每行日志包含三个字段：

```text
timestamp status_code latency_ms
```

示例：

```text
2026-09-21T20:00:00Z 200 34.7
2026-09-21T20:00:01Z 404 52.3
2026-09-21T20:00:02Z 500 91.7
```

字段说明：

* `timestamp`：ISO 格式时间戳
* `status_code`：HTTP 状态码
* `latency_ms`：请求延迟，单位为毫秒

以下情况会被视为损坏日志：

* 字段数量不是 3
* 时间戳无法解析
* HTTP 状态码无法转换为整数
* 延迟无法转换为浮点数

---

## 3. Project Structure

```text
week1/
├── README.md
├── src/
│   └── log_stats.py
├── tests/
│   └── test_log_stats.py
├── bench/
│   ├── benchmark.py
│   └── bench_*.log
└── results/
    ├── raw.csv
    └── summary.md
```

目录说明：

* `src/`：日志分析程序
* `tests/`：pytest 单元测试
* `bench/`：benchmark 脚本和生成的测试日志
* `results/`：性能测试原始数据和实验总结

---

## 4. Usage

运行日志分析器：

```bash
python src/log_stats.py <log_file>
```

例如：

```bash
python src/log_stats.py bench/bench_10000.log
```

程序会输出：

```text
total_number
valid_requests
invalid_lines
mean_ms
p50_ms
p95_ms
error_rate
```

CLI 显示时可以将延迟格式化为两位小数。

---

## 5. Statistics

### Mean Latency

平均延迟只统计有效请求：

```text
mean_latency = total_latency / valid_requests
```

### Error Rate

HTTP 状态码大于等于 `400` 的有效请求被视为错误请求：

```text
error_rate = error_requests / valid_requests
```

损坏日志不参与错误率计算。

### P50 / P95

首先将所有有效请求的延迟排序。

百分位位置采用：

```text
position = (n - 1) * p
```

其中：

* P50：`p = 0.50`
* P95：`p = 0.95`

如果计算得到的位置不是整数，则使用相邻两个延迟值进行线性插值。

---

## 6. Testing

运行单元测试：

```bash
python -m pytest tests/test_log_stats.py -v
```

测试覆盖的主要场景包括：

* 空日志文件
* 单条有效日志
* 多条有效日志
* 损坏日志
* 非法时间戳
* 非法状态码
* 非法延迟
* HTTP 404 / 500 错误
* P50 / P95 计算

浮点数结果使用 `pytest.approx()` 进行比较。

---

## 7. Benchmark

benchmark 用于测量日志解析耗时和处理吞吐量。

测试时：

* 日志文件提前生成
* 日志生成时间不计入解析耗时
* 使用 `time.perf_counter()` 计时
* 每个规模重复运行多次
* 原始数据保存到 `results/raw.csv`

吞吐量定义为：

```text
lines_per_second = total_number / elapsed_seconds
```

---

## 8. Environment

本次开发与测试环境：

```text
OS: Windows 10
Python: 3.11.7
pytest: 7.4.0
CPU: Intel Xeon Gold 5220R @ 2.20 GHz × 2
Memory: 127.65 GB
```

Python 解释器：

```text
D:/anaconda/python.exe
```

---

## 9. Notes

当前实现主要用于学习日志解析、异常处理、单元测试和基础性能测试。

当前版本会将所有有效延迟保存到内存中，并通过排序计算 P50 和 P95，因此不适用于直接处理无限流式日志。
