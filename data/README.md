# 数据目录说明

## raw/
原始数据，不做任何修改。

- `ml-1m/ratings.dat` — 用户评分：`UserID::MovieID::Rating::Timestamp`
- `ml-1m/movies.dat` — 电影信息：`MovieID::Title::Genres`
- `ml-1m/users.dat` — 用户信息：`UserID::Gender::Age::Occupation::Zip-code`

下载地址：https://files.grouplens.org/datasets/movielens/ml-1m.zip

## processed/
由 `src/data_prep.py` 生成的清洗结果。可随时重新生成，不提交版本库。

## 字段与口径

把评分转成二分类标签时，要明确写下阈值（例如 `rating >= 4` 记为正样本）和理由。这是「偏好预测」，不是真实曝光-点击任务。
