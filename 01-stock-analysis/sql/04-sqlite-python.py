"""
Day 6 第二部分：Python + SQLite
用 Python 操作 stock_learning.db
"""

import sqlite3

# 1. 连接数据库（如果文件不存在，会自动创建）
conn = sqlite3.connect("../stock_learning.db")

# 2. 创建游标——相当于"遥控器"
cursor = conn.cursor()

# =============================================
# 查询：查所有股票
# =============================================
cursor.execute("SELECT * FROM stocks")
rows = cursor.fetchall()  # 获取所有结果

print("=== 所有股票 ===")
for row in rows:
    print(row)

# =============================================
# 条件查询：市盈率低于 20
# =============================================
cursor.execute("SELECT * FROM stocks WHERE pe_ratio < 20")
rows = cursor.fetchall()

print("\n=== 市盈率低于 20 ===")
for row in rows:
    print(row)

# =============================================
# 排序：按市值从高到低
# =============================================
cursor.execute("SELECT * FROM stocks ORDER BY market_cap DESC")
rows = cursor.fetchall()

print("\n=== 按市值排序 ===")
for row in rows:
    print(row)

# =============================================
# 分组统计
# =============================================
cursor.execute("""
    SELECT sector, COUNT(*), AVG(pe_ratio)
    FROM stocks
    GROUP BY sector
""")
rows = cursor.fetchall()

print("\n=== 行业统计 ===")
for row in rows:
    print(f"行业: {row[0]}, 股票数: {row[1]}, 平均市盈率: {row[2]:.1f}")

# 6. 关闭连接
conn.close()
print("\n✅ 完成")
