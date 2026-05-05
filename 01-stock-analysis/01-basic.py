# --- 1. 数据类型 ---
name = "茅台"
price = 1800.50
shares = 100
print(type(name), type(price), type(shares))

# --- 2. 列表操作 ---
stocks = ["茅台", "五粮液", "宁德时代"]
stocks.append("比亚迪")
for s in stocks:
    print(s)

# --- 3. 字典 ---
stock_data = {
    "茅台": {"price": 1800, "pe": 30},
    "宁德时代": {"price": 200, "pe": 50}
}
print(stock_data["茅台"]["pe"])

# --- 4. 函数 ---
def calculate_return(buy_price, sell_price):
    return (sell_price - buy_price) / buy_price * 100

print(f"收益率: {calculate_return(100, 120):.2f}%")

name="茅台"
price=1900.50
shares=100
print(type(name),type(price),type(shares))
