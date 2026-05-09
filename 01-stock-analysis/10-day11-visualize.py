"""
Day 11：可视化 — 净值曲线图 + 相关性热力图
输出：output/nav_curve.png、output/correlation_heatmap.png
"""
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# =============================================
# 设置中文字体（Mac）
# =============================================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC']
plt.rcParams['axes.unicode_minus'] = False

# =============================================
# 设置输出目录
# =============================================
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

# =============================================
# 1. 下载数据
# =============================================
symbols = ["600519.SS", "000858.SZ", "300750.SZ", "002594.SZ"]
names = ["茅台", "五粮液", "宁德时代", "比亚迪"]
colors = ["#E74C3C", "#3498DB", "#2ECC71", "#F39C12"]

all_data = {}  # 存每个股票的原始数据
daily_returns = pd.DataFrame()  # 存所有股票的日收益率，方便后面算相关性

for sym, name in zip(symbols, names):
    print(f"正在下载 {name}...")
    df = yf.download(sym, start="2024-01-01", end="2025-12-31")
    df["股票名称"] = name
    df["日收益率"] = df["Close"].pct_change()
    all_data[name] = df
    daily_returns[name] = df["日收益率"]

# 删除第一行的 NaN（第一天没有日收益率）
daily_returns = daily_returns.dropna()

# =============================================
# 2. 计算累计净值
# =============================================
nav = (1 + daily_returns).cumprod()
# nav 是一个 DataFrame，列是股票名，行是日期，值是累计净值
# 例：茅台那列，2024-01-03 是 1.0118，表示 1 块钱变成了 1.0118

# =============================================
# 3. 找最大回撤位置（用于在图上标注）
# =============================================
def find_max_drawdown_info(series):
    """找到最大回撤的起始日期和结束日期"""
    cum_return = (1 + series).cumprod()
    rolling_max = cum_return.cummax()
    drawdown = (cum_return - rolling_max) / rolling_max
    
    end_idx = drawdown.idxmin()          # 回撤最低点的日期
    peak_idx = rolling_max.loc[:end_idx].idxmax()  # 回撤开始前最高点的日期
    
    return peak_idx, end_idx, drawdown.min()

# =============================================
# 4. 画净值曲线图
# =============================================
print("正在画净值曲线图...")

fig, ax = plt.subplots(figsize=(14, 7))

# 画四条净值曲线
for i, name in enumerate(names):
    ax.plot(nav.index, nav[name], 
            label=name, 
            color=colors[i], 
            linewidth=1.8, 
            alpha=0.9)
    
    # 标注最大回撤位置
    peak_idx, end_idx, dd = find_max_drawdown_info(daily_returns[name])
    peak_val = nav.loc[peak_idx, name]
    end_val = nav.loc[end_idx, name]
    
    # 从最高点到最低点画一条虚线
    ax.plot([peak_idx, end_idx], [peak_val, end_val], 
            color=colors[i], linestyle="--", linewidth=1, alpha=0.5)
    # 在最低点画一个圆点
    ax.scatter(end_idx, end_val, color=colors[i], s=40, zorder=5)
    # 标注回撤百分比
    ax.annotate(f"{dd:.1%}", 
                xy=(end_idx, end_val),
                xytext=(10, -20),
                textcoords="offset points",
                fontsize=9,
                color=colors[i],
                arrowprops=dict(arrowstyle="->", color=colors[i], alpha=0.6))

# 画一条 y=1 的参考线
ax.axhline(y=1, color="gray", linestyle=":", alpha=0.3)

# 标签和标题
ax.set_title("四只股票累计净值走势对比（2024-2025）", fontsize=16, fontweight="bold")
ax.set_xlabel("日期", fontsize=12)
ax.set_ylabel("累计净值（初始 = 1）", fontsize=12)
ax.legend(loc="best", fontsize=11)
ax.grid(True, alpha=0.3)

# 设置 y 轴格式为百分比
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))

plt.tight_layout()
nav_curve_path = output_dir / "nav_curve.png"
plt.savefig(nav_curve_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  → 已保存: {nav_curve_path}")

# =============================================
# 5. 画相关性热力图
# =============================================
print("正在画相关性热力图...")

corr = daily_returns.corr()

fig, ax = plt.subplots(figsize=(8, 6))

sns.heatmap(corr, 
            annot=True,           # 在格子里显示数字
            fmt=".3f",            # 保留3位小数
            cmap="coolwarm",       # 颜色：蓝→白→红
            center=0,             # 0 为中心色
            square=True,           # 方块正方形
            linewidths=0.5,        # 格子间隔
            linecolor="white",
            xticklabels=names,
            yticklabels=names,
            ax=ax)

ax.set_title("股票日收益率相关性热力图", fontsize=14, fontweight="bold")
plt.tight_layout()
heatmap_path = output_dir / "correlation_heatmap.png"
plt.savefig(heatmap_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  → 已保存: {heatmap_path}")

# =============================================
# 6. 输出分析结论
# =============================================
print("\n" + "=" * 55)
print("分析结论")
print("=" * 55)

# 找出相关性最高的两只
corr_triu = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
max_pair = corr_triu.stack().idxmax()
print(f"相关性最高: {max_pair[0]} vs {max_pair[1]} = {corr.loc[max_pair]:.3f}")

# 找出相关性最低的两只
min_pair = corr_triu.stack().idxmin()
print(f"相关性最低: {min_pair[0]} vs {min_pair[1]} = {corr.loc[min_pair]:.3f}")

# 看谁累计收益最高
final_nav = nav.iloc[-1]
best = final_nav.idxmax()
print(f"累计收益最高: {best}（{final_nav[best]:.2%}）")
worst = final_nav.idxmin()
print(f"累计收益最低: {worst}（{final_nav[worst]:.2%}）")
