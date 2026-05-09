"""
Day 10：实现分析函数
输出：四只股票的 年化收益率 / 年化波动率 / 最大回撤 / 夏普比率
"""
import pandas as pd
import yfinance as yf
import numpy as np


def load_data(symbol, name, start="2024-01-01", end="2025-12-31"):
    """下载单只股票数据，返回带日收益率的 DataFrame"""
    df = yf.download(symbol, start=start, end=end)
    df["股票名称"] = name
    df["日收益率"] = df["Close"].pct_change()
    return df


def calc_volatility(series):
    """计算年化波动率：日标准差 × √252"""
    return series.std() * (252 ** 0.5)


def calc_annual_return(series):
    """计算年化收益率：(1 + 日均收益率) ** 252 - 1"""
    return (1 + series.mean()) ** 252 - 1


def calc_max_drawdown(series):
    """计算最大回撤"""
    # 累计收益率
    cum_return = (1 + series).cumprod()
    # 历史最高点
    rolling_max = cum_return.cummax()
    # 回撤 = (当前值 - 最高点) / 最高点
    drawdown = (cum_return - rolling_max) / rolling_max
    return drawdown.min()


def calc_sharpe_ratio(series, risk_free_rate=0.02):
    """计算夏普比率：(年化收益率 - 无风险利率) / 年化波动率"""
    annual_return = calc_annual_return(series)
    annual_vol = calc_volatility(series)
    return (annual_return - risk_free_rate) / annual_vol


# =============================================
# 主程序
# =============================================
symbols = ["600519.SS", "000858.SZ", "300750.SZ", "002594.SZ"]
names = ["茅台", "五粮液", "宁德时代", "比亚迪"]

results = []

for sym, name in zip(symbols, names):
    print(f"正在处理 {name}...")
    df = load_data(sym, name)
    daily_ret = df["日收益率"].dropna()

    results.append({
        "股票": name,
        "年化收益率": calc_annual_return(daily_ret),
        "年化波动率": calc_volatility(daily_ret),
        "最大回撤": calc_max_drawdown(daily_ret),
        "夏普比率": calc_sharpe_ratio(daily_ret),
    })

# 输出结果表格
result_df = pd.DataFrame(results)
result_df["年化收益率"] = result_df["年化收益率"].apply(lambda x: f"{x:.1%}")
result_df["年化波动率"] = result_df["年化波动率"].apply(lambda x: f"{x:.1%}")
result_df["最大回撤"] = result_df["最大回撤"].apply(lambda x: f"{x:.1%}")

print("四只股票风险收益分析结果")
print("=" * 55)
#print(result_df.to_string(index=False))
print(result_df)