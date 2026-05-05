import pandas as pd
data = {                                                                                                                                                                                                  
         "股票": ["茅台", "五粮液", "宁德时代", "比亚迪"],                                                                                                                                                     
         "收盘价": [1800, 150, 220, 280],                                                                                                                                                                      
         "市盈率": [30, 25, 50, 35],                                                                                                                                                                           
         "涨跌幅%": [2.5, -1.2, 3.8, -0.5]                                                                                                                                                                     
     }
df = pd.DataFrame(data)                                                                                                                                                                                   
#print(df)

#print("=== 收盘价列 ===")                                                                                                                                                                                 
#print(df["收盘价"])

#print(f"\n平均收盘价: {df['收盘价'].mean()}")

#print("=== 上涨的股票 ===")                                                                                                                                                                             
#print(df[df["涨跌幅%"] > 0])

#print("=== 按市盈率排序 ===")                                                                                                                                                                           
#print(df.sort_values("市盈率"))


#print("第一行\n第二行")     # \n = 换行                                                                                                                                                                   
#print("Tab\t分隔")         # \t = Tab 制表符                                                                                                                                                              
#print("他说：\"你好\"")    # \" = 在字符串里输出双引号
import yfinance as yf
maotai = yf.download("600519.SS", start="2025-01-01", end="2025-12-31")                                                                                                                                   
print(maotai.head())                                                                                                                                                                                      
print(maotai.describe())
maotai.to_csv("maotai_2025.csv")


apple = yf.download("AAPL", start="2025-01-01", end="2025-12-31")                                                                                                                                   
print(apple.head())                                                                                                                                                                                      
print(apple.describe())
apple.to_csv("apple_2025.csv")