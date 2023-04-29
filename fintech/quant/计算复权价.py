import pandas as pd

pd.set_option("expand_frame_repr",False)

df=pd.read_csv("./data/sz300001.csv",encoding="gbk")

# print(df["股票代码"])

df = df[['交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅']]

df.sort_values(by="交易日期",inplace=True)

# =====计算复权价，最重要的就是涨跌幅要复权。下面考察我们的数据中的涨跌幅
# df['涨跌幅2'] = df['收盘价'].pct_change()  # 通过pct_change计算基于未复权收盘价的涨跌幅
# print(df[abs(df['涨跌幅2'] - df['涨跌幅']) > 0.0001])  # 数据中的涨跌幅是复权后的涨跌幅
# del df['涨跌幅2']
# 有了复权涨跌幅，其他的复权价格都可以自己算。

df["复权因子"] = (df["涨跌幅"]+1).cumprod()

initial_price = df.iloc[0]['收盘价'] / (1 + df.iloc[0]['涨跌幅'])  # 计算上市价格
df['收盘价_后复权'] = initial_price * df['复权因子']  # 相乘得到复权价


# ===如果计算复权的开盘价、最高价、最低价？
# 通过如下公式计算：'开盘价_复权' / '收盘价_复权' = '开盘价' / '收盘价'
df['开盘价_后复权'] = df['开盘价'] / df['收盘价'] * df['收盘价_后复权']
df['最高价_后复权'] = df['最高价'] / df['收盘价'] * df['收盘价_后复权']
df['最低价_后复权'] = df['最低价'] / df['收盘价'] * df['收盘价_后复权']


