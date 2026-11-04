# 第 1 周学习笔记（11/02–11/08）

## 周一 · 环境与 Python 复健

环境（2026-11-04 实测）：

- Python 3.11.7（Anaconda，`D:\jobs\anaconda\python.exe`）
- NumPy / Pandas / Jupyter / scikit-learn / matplotlib 均已安装
- Git 2.55.0；Node 24.13.0（用于跑学习工作台）

核心收获：

- **哈希表把 O(n²) 降到 O(n)**：两数之和用「查补数」代替「双重循环」。代价是 O(n) 额外空间。
- **字典记录的是「已见过的值」**：必须先查再存，否则 `[3, 3]` 这种重复值会返回同一个下标。

## 周二 · Python 数据结构与复杂度

- `list` 有序可重复，`tuple` 不可变，`dict` 键值对，`set` 只存键且去重。
- `Counter` 统计频次，`defaultdict(list)` 免去 `if key not in` 判断。
- `dict.fromkeys` 能在去重的同时保持原顺序（Python 3.7+ 字典有序）。
- 复杂度速查：数组遍历 O(n)、嵌套循环 O(n²)、二分 O(log n)、哈希查找 O(1)、堆插入 O(log n)。

## 周三 · NumPy + Pandas 入门

**NumPy**

- `shape` 就是每个维度的大小，`(2, 3)` 表示 2 行 3 列。
- 广播：形状不同的数组按规则自动扩展，`(2,3) + (2,1)` 合法，`(2,3) + (3,)` 也合法。
- `axis` 是「沿着哪个维度压缩」。`axis=0` 消失的是第 0 维（行），即**按列**聚合。

**Pandas**

- `DataFrame` 是一张表，`Series` 是其中一列。
- 读 MovieLens 的 `::` 分隔需要 `sep="::", engine="python"`。
- 布尔索引筛选：`df[df["rating"] >= 4]`。
- 缺失值：`df.isna().sum()` 统计，`fillna()` 填充，`dropna(subset=[...])` 定向删除。
- 类型转换：`pd.to_numeric(col, errors="coerce")` 能把脏字符串转成可空的 `Int64`。
- 时间字段：`pd.to_datetime(col, unit="s")` 把 Unix 秒转成时间戳。

**数据口径（重要）**

MovieLens 是**显式评分**数据。把 `rating >= 4` 记为正样本做二分类，只能叫「偏好预测」，不等于广告系统的「曝光→点击」日志。项目 README 和简历里都要写明这条边界。

## 周四 · Pandas 分组与合并

- `groupby("movie_id").agg(...)` 做分组统计，`size` 计数、`mean` 求均值。
- `merge` 默认 inner join，`how="left"` 保留左表全部行。
- Top-N：先 `sort_values(ascending=False)` 再 `head(n)`；数据量大时考虑 `nlargest`。
- 时间切分：先按 `timestamp` 排序，再取前 80% 做训练。**不能随机切分**，否则未来行为泄漏进训练集。

## 周五 · LeetCode 数组 / 哈希 / 双指针

- 双指针（对撞）：283 移动零、11 盛最多水的容器。
- 排序 + 双指针：15 三数之和，`O(n²)`，注意跳过重复元素。
- 哈希 + 滑动窗口：3 无重复字符最长子串，`O(n)`。

## 周六 · MovieLens 数据集与项目脚手架

- 三个文件：`ratings.dat`（评分）、`movies.dat`（电影）、`users.dat`（用户）。
- 编码问题：MovieLens-1M 的 `movies.dat` 含非 UTF-8 字符，读取用 `latin-1`。
- 目录结构固定：`data/` 存数据、`src/` 存代码、`notebooks/` 做探索、`tests/` 放测试。

## 周日 · 周复盘与关卡

关卡自检：

- [ ] 45 分钟独立写出读取、清洗、分组统计、保存的 Pandas 脚本
- [ ] 能解释 list/dict/set、Counter/defaultdict、复杂度与常见边界
- [ ] 随机抽 3 道 Easy 题闭卷通过
- [ ] Git 仓库有 README、requirements、首次 commit
