"""
Day 9：下载多只股票数据
"""
import yfinance as yf
import pandas as pd

# 四只股票：茅台、五粮液、宁德时代、比亚迪
symbols = ["600519.SS", "000858.SZ", "300750.SZ", "002594.SZ"]
names = ["茅台", "五粮液", "宁德时代", "比亚迪"]

all_data = {}
for sym, name in zip(symbols, names):
    print(f"正在下载 {name} ({sym})...")
    df = yf.download(sym, start="2024-01-01", end="2025-12-31")
    df["股票名称"] = name
    all_data[name] = df
    print(f"  ✅ {name} 下载完成，{len(df)} 个交易日")

# 合并所有数据
combined = pd.concat(all_data.values())
combined.to_csv("multi_stocks.csv")
print(f"\n✅ 所有数据已保存到 multi_stocks.csv")
print(f"总行数：{len(combined)}")
print(combined.head())

