"""Day 3 复习：Pandas 入门"""
import pandas as pd

# 1. 从字典创建 DataFrame
data = {
    "股票": ["茅台", "五粮液", "宁德时代", "比亚迪"],
    "收盘价": [1800, 150, 220, 280],
    "市盈率": [30, 25, 50, 35],
    "涨跌幅%": [2.5, -1.2, 3.8, -0.5]
}
df = pd.DataFrame(data)
print("=== 原始数据 ===")
print(df)

# 2. 基本操作
print(f"\n平均收盘价: {df['收盘价'].mean()}")
print("\n=== 上涨的股票 ===")
print(df[df["涨跌幅%"] > 0])

print("\n=== 按市盈率排序 ===")
print(df.sort_values("市盈率"))

# 3. yfinance 下载真实数据
import yfinance as yf
maotai = yf.download("600519.SS", start="2025-01-01", end="2025-12-31")
print("\n=== 茅台 2025 数据前 5 行 ===")
print(maotai.head())
print("\n=== 统计描述 ===")
print(maotai.describe())

# 保存到 CSV
maotai.to_csv("maotai_2025.csv")
print("\n✅ 数据已保存到 maotai_2025.csv")
