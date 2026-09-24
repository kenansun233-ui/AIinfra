1. 测试方法
   - 100 / 10,000 / 1,000,000 行
   - 每档 warm-up 一次
   - 正式运行 3 次
   - 使用 time.perf_counter()
   - 日志生成时间不计入 benchmark

2. 原始数据
   - 指向 raw.csv

3. 中位数结果
   - 上面这张表

4. 结论
   - 小输入受固定开销影响明显
   - 大输入吞吐约 38 万 lines/s
   - 百万行三次结果稳定
   - analyze_log 包含 O(n log n) 排序