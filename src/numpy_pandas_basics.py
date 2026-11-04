"""第 1 周 · 周三：NumPy + Pandas 入门。

目标（对应每日计划）：
  1. NumPy：ndarray 的 shape、广播、axis 三个概念
  2. Pandas：DataFrame / Series、read_csv、筛选、排序、缺失值、类型转换
  3. 产出：把操作写成 .py 脚本（就是本文件）

运行：
    python src/numpy_pandas_basics.py

设计说明：每个知识点都先给「可运行示例」，再留一个练习区。
练习区的答案折叠在文件末尾的 _answers()，建议先自己写再对照。
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"


# ============================================================
# Part 1  NumPy：shape / 广播 / axis
# ============================================================

def demo_shape() -> None:
    """shape 是数组每个维度的大小，是理解后续一切的前提。"""
    row = np.array([1, 2, 3])              # 一维
    table = np.arange(6).reshape(2, 3)     # 二维
    cube = np.arange(24).reshape(2, 3, 4)  # 三维

    print("一维 shape:", row.shape, "-> (元素个数,)")
    print("二维 shape:", table.shape, "-> (行, 列)")
    print("三维 shape:", cube.shape, "-> (层, 行, 列)")


def demo_broadcasting() -> None:
    """广播：形状不同也能运算，规则是把较小维度自动扩展。"""
    matrix = np.array([[1, 2, 3],
                       [4, 5, 6]])
    column = np.array([[10],
                       [20]])
    row = np.array([100, 200, 300])

    print("\n矩阵 + 列向量:\n", matrix + column)   # 列向量沿行方向复制
    print("矩阵 + 行向量:\n", matrix + row)        # 行向量沿列方向复制
    print("矩阵 * 标量:\n", matrix * 2)            # 标量广播到每个元素


def demo_axis() -> None:
    """axis 表示「沿着哪个维度压缩掉」。

    记忆法：axis=0 表示结果里消失的是第 0 维（行），即按列聚合。
    """
    table = np.array([[1, 2, 3],
                      [4, 5, 6]])
    print("\n原矩阵 shape:", table.shape)
    print("sum(axis=0) 按列求和 ->", table.sum(axis=0), "shape:", table.sum(axis=0).shape)
    print("sum(axis=1) 按行求和 ->", table.sum(axis=1), "shape:", table.sum(axis=1).shape)
    print("mean(axis=0) 每列均值 ->", table.mean(axis=0))


# ============================================================
# Part 2  Pandas：Series / DataFrame / read_csv
# ============================================================

def build_demo_dataframe() -> pd.DataFrame:
    """没有本地数据时，构造一份带缺失值和脏类型的表格用于练习。"""
    return pd.DataFrame({
        "user_id": [1, 2, 3, 4, 5, 6],
        "movie_id": [101, 101, 102, 103, 102, 104],
        "rating": [5, 4, None, 3, 4, 2],
        "genre": ["Action", "Action", "Comedy", "Drama", "Comedy", "Drama"],
        "year": ["1995", "1995", "2001", "1999", "2001", "2005"],
    })


def load_data() -> pd.DataFrame:
    """优先读真实清洗结果，没有就用演示数据。"""
    path = PROCESSED_DIR / "ratings_clean.csv"
    if path.exists():
        df = pd.read_csv(path)
        # 补上后续统计用得到的列
        if "genre" not in df.columns:
            df = df.assign(
                genre=np.where(df["movie_id"] % 2 == 0, "A", "B"),
                year="2000",
            )
        print(f"[数据] 读取 {path}")
        return df
    print("[数据] 未找到清洗结果，使用内置演示数据（先跑 src/data_prep.py 可生成真实数据）")
    return build_demo_dataframe()


def demo_inspect(df: pd.DataFrame) -> None:
    print("\n--- 基础查看 ---")
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    print("\n前 3 行:\n", df.head(3))
    print("\ndtypes:\n", df.dtypes.to_string())
    print("\n缺失值统计:\n", df.isna().sum().to_string())


def demo_select_filter_sort(df: pd.DataFrame) -> None:
    print("\n--- 筛选与排序 ---")
    # 布尔索引
    high = df[df["rating"] >= 4]
    print(f"评分 >= 4 的行数: {len(high)}")

    # isin 多值筛选
    action = df[df["genre"].isin(["Action", "Comedy"])] if "genre" in df else df
    print(f"genre 属于 Action/Comedy 的行数: {len(action)}")

    # 排序：按评分降序
    top = df.dropna(subset=["rating"]).sort_values("rating", ascending=False).head(3)
    print("评分最高的 3 行:\n", top.to_string(index=False))


def demo_clean(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- 清洗：缺失值 + 类型转换 ---")
    cleaned = df.copy()

    # 1. 数值列缺失值填 0（实际项目应结合业务决定填什么）
    if cleaned["rating"].isna().any():
        print(f"rating 缺失 {cleaned['rating'].isna().sum()} 个，填充为 0")
        cleaned["rating"] = cleaned["rating"].fillna(0)

    # 2. 类型转换：rating -> int，year -> int
    cleaned["rating"] = cleaned["rating"].astype(int)
    if "year" in cleaned.columns:
        cleaned["year"] = pd.to_numeric(cleaned["year"], errors="coerce").astype("Int64")

    # 3. 去重
    before = len(cleaned)
    cleaned = cleaned.drop_duplicates(subset=["user_id", "movie_id"])
    print(f"去重: {before} -> {len(cleaned)}")

    print("清洗后 dtypes:\n", cleaned.dtypes.to_string())
    return cleaned.reset_index(drop=True)


# ============================================================
# Part 3  五个统计任务
# ============================================================

def five_stats_tasks(df: pd.DataFrame) -> dict:
    """完成每日计划要求的「5 个统计任务」。"""
    results = {}

    # 任务 1：评分均值、中位数、标准差
    results["rating_mean"] = round(float(df["rating"].mean()), 4)
    results["rating_median"] = float(df["rating"].median())
    results["rating_std"] = round(float(df["rating"].std()), 4)

    # 任务 2：每个 genre 的评分数量与均值
    results["by_genre"] = (
        df.groupby("genre")["rating"].agg(["size", "mean"]).round(4).to_dict("index")
        if "genre" in df else {}
    )

    # 任务 3：评分最高的 Top5 电影
    results["top_movies"] = (
        df.groupby("movie_id")["rating"].mean()
        .sort_values(ascending=False).head(5).round(4).to_dict()
    )

    # 任务 4：最活跃用户 Top5（评分数最多）
    results["top_users"] = df["user_id"].value_counts().head(5).to_dict()

    # 任务 5：正样本率（rating >= 4）
    results["positive_rate"] = round(float((df["rating"] >= 4).mean()), 4)

    return results


def print_results(results: dict) -> None:
    print("\n--- 5 个统计任务结果 ---")
    print(f"1. 评分均值/中位数/标准差: {results['rating_mean']} / "
          f"{results['rating_median']} / {results['rating_std']}")
    print(f"2. 按 genre 分组:\n   {results['by_genre']}")
    print(f"3. 高评分电影 Top5: {results['top_movies']}")
    print(f"4. 活跃用户 Top5: {results['top_users']}")
    print(f"5. 正样本率(评分>=4): {results['positive_rate']}")


# ============================================================
# 练习区（先自己写）
# ============================================================

def exercise_1_normalize(df: pd.DataFrame) -> pd.Series:
    """练习 1：把 rating 做 min-max 归一化到 [0, 1]，返回 Series。"""
    raise NotImplementedError("自己实现，再对照 _answers.exercise_1")


def exercise_2_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """练习 2：用 pivot_table 求「每个 genre 的平均评分」，行是 genre，列是 avg_rating。"""
    raise NotImplementedError("自己实现，再对照 _answers.exercise_2")


def exercise_3_time_filter(df: pd.DataFrame) -> pd.DataFrame:
    """练习 3：如果存在 timestamp 列，返回时间前 80% 的数据（按时间排序后）。"""
    raise NotImplementedError("自己实现，再对照 _answers.exercise_3")


class _answers:
    """参考资料：写完之后再打开对照。"""

    @staticmethod
    def exercise_1(df: pd.DataFrame) -> pd.Series:
        r = df["rating"]
        return (r - r.min()) / (r.max() - r.min())

    @staticmethod
    def exercise_2(df: pd.DataFrame) -> pd.DataFrame:
        return df.pivot_table(index="genre", values="rating",
                              aggfunc="mean").rename(columns={"rating": "avg_rating"})

    @staticmethod
    def exercise_3(df: pd.DataFrame) -> pd.DataFrame:
        if "timestamp" not in df.columns:
            return df
        d = df.sort_values("timestamp").reset_index(drop=True)
        return d.iloc[: int(len(d) * 0.8)]


def main() -> None:
    print("=" * 56)
    print("Part 1  NumPy 三件套")
    print("=" * 56)
    demo_shape()
    demo_broadcasting()
    demo_axis()

    print("\n" + "=" * 56)
    print("Part 2  Pandas 基础")
    print("=" * 56)
    df = load_data()
    demo_inspect(df)
    demo_select_filter_sort(df)
    cleaned = demo_clean(df)

    print("\n" + "=" * 56)
    print("Part 3  五个统计任务")
    print("=" * 56)
    print_results(five_stats_tasks(cleaned))

    print("\n" + "=" * 56)
    print("练习区提示：打开本文件，实现 exercise_1/2/3，")
    print("完成后把 _answers 里的实现和自己的对比。")
    print("=" * 56)


if __name__ == "__main__":
    main()
