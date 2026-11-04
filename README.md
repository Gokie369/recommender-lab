# Recommender Lab

> 搜广推 9 周学习计划的主项目仓库。基于 MovieLens-1M 构建端到端推荐系统。

## 项目目标

从数据处理到在线服务，完整走一遍工业推荐系统的分层结构：

- **数据处理**：MovieLens 读取、清洗、时间切分
- **召回层**：热门基线、ItemCF、双塔向量召回
- **排序层**：LR、FM、DeepFM、DIN
- **重排层**：MMR 多样性、冷启动兜底
- **服务层**：FastAPI 接口、推理性能与延迟记录

## 技术栈

- Python 3.8+ / NumPy / Pandas
- scikit-learn（LR、GBDT 基线）
- PyTorch（深度模型）
- FAISS（向量检索）
- FastAPI（服务化）

## 数据集

**MovieLens-1M**（GroupLens）
- 1,000,209 条评分 · 6,040 用户 · 3,706 电影 · 2000–2003
- 下载：https://grouplens.org/datasets/movielens/1m/

> 注意：MovieLens 是显式评分数据。把它转成二分类时，只能说这是「偏好预测」，不等于真实广告系统的「曝光-点击」日志。所有结论都要带上这个边界。

## 目录结构

```
recommender-lab/
├── data/
│   ├── raw/              # 原始数据（ml-1m）
│   └── processed/        # 清洗后的数据
├── src/
│   ├── data_prep.py      # 数据读取与清洗
│   ├── recall/           # 召回模块
│   ├── ranking/          # 排序模块
│   ├── rerank/           # 重排模块
│   └── evaluation/       # 评估指标
├── algorithms/           # 手撕算法题（按周归档）
├── notebooks/            # Jupyter 实验笔记
├── tests/                # 测试
├── models/               # 模型权重
├── logs/                 # 训练与实验日志
├── requirements.txt
└── README.md
```

## 快速开始

```bash
pip install -r requirements.txt

# 下载 ml-1m.zip 并解压到 data/raw/ml-1m/
python src/data_prep.py

# 手撕题自测
python algorithms/leetcode_01_two_sum.py
```

## 实验记录

| 模型 | Recall@10 | NDCG@10 | AUC | LogLoss | 训练时间 |
|---|---|---|---|---|---|
| 热门基线 | TBD | TBD | TBD | TBD | - |
| ItemCF | TBD | TBD | TBD | TBD | TBD |
| 双塔 | TBD | TBD | TBD | TBD | TBD |

数据切分统一用**按时间切分**：用过去预测未来，避免用户未来行为泄漏进训练集。每次实验固定随机种子并记录在 `logs/`。

## 9 周进度

- [x] Week 1：环境搭建、Python 复健、Pandas、算法手感
- [ ] Week 2：数据结构、SQL、PyTorch 起步
- [ ] Week 3：LR / GBDT / 评估指标
- [ ] Week 4：SQL 进阶、特征工程、CTR 小练习
- [ ] Week 5：推荐全链路、FM、ItemCF、双塔
- [ ] Week 6：DeepFM、DIN、简历 v1
- [ ] Week 7：MMR、冷启动、A/B、搜索广告、Bandit
- [ ] Week 8：FastAPI、面经冲刺、集中投递
- [ ] Week 9：面试反馈补齐

## 数据使用声明

MovieLens 仅用于学术学习。评分经阈值转换为二分类标签后，属于「偏好预测」任务，不等同于真实曝光-点击日志。
