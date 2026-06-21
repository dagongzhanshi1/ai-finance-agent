# Project 1: 股票收益率与风险分析

阶段 1 项目，目标是用 Python 跑通基础金融数据分析流程：获取数据、清洗数据、计算风险收益指标、生成可视化图表。

## What It Does

- 下载股票历史行情
- 计算日收益率和累计净值
- 计算年化收益率、年化波动率、最大回撤、夏普比率
- 对多只股票做相关性分析
- 输出净值曲线、热力图和行业对比图
- 用 SQLite 练习基础 SQL 查询

## Structure

```text
01-stock-analysis/
├── 01-basic.py                    # Python 基础
├── 02-pandas-intro.py             # Pandas 入门
├── 03-plot.py                     # Matplotlib 可视化
├── 05-preview-groupby-merge.py    # groupby / merge 预习
├── 06-groupby-merge.py            # 分组与合并练习
├── 07-exercises.py                # Pandas 练习
├── 08-download.py                 # yfinance 下载股票数据
├── 09-analyze.py                  # 风险收益指标计算
├── 10-visualize.py                # 净值曲线与相关性热力图
├── 11-semiconductor-analysis.py   # 半导体行业扩展分析
├── data/                          # 数据目录
├── output/                        # 图表输出目录
└── sql/                           # SQLite / SQL 练习
```

## Run

在仓库根目录安装依赖后运行：

```bash
python3 01-stock-analysis/08-download.py
python3 01-stock-analysis/09-analyze.py
python3 01-stock-analysis/10-visualize.py
```

## Key Learning Points

- `DataFrame` 存放二维表格数据，适合处理股票价格、收益率和指标表
- `pct_change()` 用来从价格序列计算收益率
- 最大回撤用于衡量从历史高点到低点的最大亏损幅度
- 相关性热力图可以快速观察多只股票收益率之间的联动关系

## Portfolio Value

这个项目展示的是金融数据分析底座：Python、Pandas、可视化和基本风险指标。它是后续 LLM 工具和 RAG 应用的基础阶段。
