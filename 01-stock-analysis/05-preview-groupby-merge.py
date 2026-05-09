"""Day 7 预习：groupby 和 merge"""
import pandas as pd

# ===== groupby =====
print("=== groupby 练习 ===")

data = {
    "股票": ["茅台", "茅台", "五粮液", "五粮液", "宁德", "宁德"],
    "年份": [2024, 2025, 2024, 2025, 2024, 2025],
    "营收_亿": [1500, 1700, 800, 850, 4000, 5000],
    "净利润_亿": [750, 850, 250, 270, 500, 600]
}
df = pd.DataFrame(data)
print(df)
print()

# 按股票分组，算平均净利润
print(df.groupby("股票")["净利润_亿"].mean())
print()

# 按股票分组，同时算营收总和和净利润均值
print(df.groupby("股票").agg({"营收_亿": "sum", "净利润_亿": "mean"}))

# ===== merge =====
print("\n=== merge 练习 ===")

# 两张表：一张股价、一张市盈率
price_df = pd.DataFrame({
    "股票代码": ["600519", "000858", "300750"],
    "收盘价": [1800, 150, 220]
})
pe_df = pd.DataFrame({
    "股票代码": ["600519", "000858", "300750"],
    "市盈率": [30, 25, 50]
})

print("股价表：")
print(price_df)
print("\n市盈率表：")
print(pe_df)

# 合并
merged = pd.merge(price_df, pe_df, on="股票代码")
print("\n合并结果：")
print(merged)
