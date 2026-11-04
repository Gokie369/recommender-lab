"""MovieLens-1M 数据读取、清洗与统计。

对应第 1 周周三/周六的产出：读入原始 .dat 文件，完成清洗、分组统计、保存。

运行：
    python src/data_prep.py

数据放置：data/raw/ml-1m/{ratings.dat, movies.dat, users.dat}
下载：https://files.grouplens.org/datasets/movielens/ml-1m.zip

若数据不存在，脚本会用内置的少量样例数据跑通流程，方便先验证代码正确性。
"""

from pathlib import Path
import io
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "ml-1m"
PROCESSED_DIR = ROOT / "data" / "processed"

# 评分 >= 4 记为正样本（偏好预测口径）
POSITIVE_THRESHOLD = 4


def load_ratings() -> pd.DataFrame:
    path = RAW_DIR / "ratings.dat"
    if path.exists():
        df = pd.read_csv(
            path, sep="::", engine="python", header=None,
            names=["user_id", "movie_id", "rating", "timestamp"],
            encoding="latin-1",
        )
    else:
        print(f"[提示] 未找到 {path}，使用内置样例数据。")
        df = _sample_ratings()
    return df


def _sample_ratings() -> pd.DataFrame:
    return pd.DataFrame({
        "user_id": [1, 1, 2, 2, 3, 3, 4],
        "movie_id": [101, 102, 101, 103, 102, 103, 101],
        "rating": [5, 2, 4, 5, 3, 4, 1],
        "timestamp": [1000, 1010, 1005, 1020, 1030, 1040, 1050],
    })


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=["user_id", "movie_id", "timestamp"])
    df = df.dropna(subset=["user_id", "movie_id", "rating"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df["rating"] = df["rating"].astype("int8")
    df["is_positive"] = (df["rating"] >= POSITIVE_THRESHOLD).astype("int8")
    return df.reset_index(drop=True)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """每个物品的统计：评分次数、平均分、正样本率。"""
    summary = (
        df.groupby("movie_id")
        .agg(
            num_ratings=("rating", "size"),
            avg_rating=("rating", "mean"),
            positive_rate=("is_positive", "mean"),
        )
        .round(4)
        .sort_values("num_ratings", ascending=False)
        .reset_index()
    )
    return summary


def time_split(df: pd.DataFrame, ratio: float = 0.8) -> tuple[pd.DataFrame, pd.DataFrame]:
    """按时间切分，用过去预测未来，避免未来信息泄漏。"""
    df = df.sort_values("timestamp").reset_index(drop=True)
    cut = int(len(df) * ratio)
    return df.iloc[:cut].copy(), df.iloc[cut:].copy()


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_ratings()
    clean_df = clean(raw)
    summary = summarize(clean_df)
    train, test = time_split(clean_df)

    clean_df.to_csv(PROCESSED_DIR / "ratings_clean.csv", index=False)
    summary.to_csv(PROCESSED_DIR / "ratings_summary.csv", index=False)
    train.to_csv(PROCESSED_DIR / "train.csv", index=False)
    test.to_csv(PROCESSED_DIR / "test.csv", index=False)

    print(f"原始评分条数: {len(raw)}")
    print(f"清洗后条数:   {len(clean_df)}")
    print(f"用户数:       {clean_df['user_id'].nunique()}")
    print(f"物品数:       {clean_df['movie_id'].nunique()}")
    print(f"训练/测试:    {len(train)} / {len(test)}")
    print(f"\n评分分布:\n{clean_df['rating'].value_counts().sort_index().to_string()}")
    print(f"\n热门物品 Top5:\n{summary.head(5).to_string(index=False)}")
    print(f"\n结果已保存到: {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
