import pandas as pd                                                                                                                                                                                                                                                                                                                                                                        
df = pd.read_csv("maotai_2025.csv", index_col=0, parse_dates=True)   
cols = ["Open", "High", "Low", "Close", "Volume"]                                                                                                                               
df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")                                                                                                                                       
print(df.head())

print("缺失值统计：")                                                                                                                                                                                     
print(df.isnull().sum())

df["日收益率"] = df["Close"].pct_change() 
df["MA20"] = df["Close"].rolling(window=20).mean()                                                                                                                                            
df["MA60"] = df["Close"].rolling(window=60).mean()
print(df[["Close", "MA20", "MA60", "日收益率"]].head(10))

import matplotlib.pyplot as plt                                                                                                                                                                                                                                                                                                               
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']                                                                                                                          
plt.rcParams['axes.unicode_minus'] = False                                                                                                                                                                                                                                                                                                               
plt.figure(figsize=(12, 6))                                                                                                                                                     
plt.plot(df.index, df["Close"], label="收盘价", linewidth=1)                                                                                                                    
plt.plot(df.index, df["MA20"], label="20日均线", alpha=0.7)                                                                                                                     
plt.plot(df.index, df["MA60"], label="60日均线", alpha=0.7)                                                                                                                     
plt.title("茅台 2025 股价走势")                                                                                                                                                 
plt.xlabel("日期")                                                                                                                                                              
plt.ylabel("价格")                                                                                                                                                              
plt.legend()                                                                                                                                                                    
plt.grid(True, alpha=0.3)   
plt.savefig("maotai_chart.png", dpi=150, bbox_inches="tight")                                                                                                                                                    
plt.show()  
                                                                                                                                                
print("图片已保存到 maotai_chart.png")  