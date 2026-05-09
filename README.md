# 股票收益率与风险分析

基于 Python + Pandas + Matplotlib + Seaborn 的 A 股多只股票分析工具。

## 功能

- 下载多只股票历史数据（yfinance）
- 计算年化收益率、年化波动率、最大回撤、夏普比率
- 画累计净值曲线对比图（标注最大回撤位置）
- 画股票日收益率相关性热力图

## 项目结构

```
01-stock-analysis/
├── analyze.py                    # Day 10：计算风险收益指标
├── 10-day11-visualize.py         # Day 11：净值曲线 + 热力图
├── 11-semiconductor-analysis.py  # 半导体行业分析（你新建的）
├── output/                       # 输出图片
│   ├── nav_curve.png
│   └── correlation_heatmap.png
├── data/                         # 数据文件
├── sql/                          # SQL 学习文件
└── stock_learning.db             # SQLite 练习数据库
```

## 使用方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行分析（计算风险收益指标）
python 01-stock-analysis/analyze.py

# 运行可视化（画图）
python 01-stock-analysis/10-day11-visualize.py
```

## 分析结果示例

| 股票 | 年化收益率 | 年化波动率 | 最大回撤 | 夏普比率 |
|------|-----------|-----------|---------|---------|
| 茅台 | 15.2% | 22.1% | -18.5% | 0.68 |
| 宁德时代 | 248.12% | — | — | — |

（注：具体数值随下载时间段变化，每次运行可能不同。）

## 数据来源

Yahoo Finance（通过 yfinance 库获取）

## 环境要求

- Python 3.10+
- 依赖包见 requirements.txt
