import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# =====读入数据
df = pd.read_csv('./data/sz300001.csv', encoding='gbk')

df = df[['交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅']]
df.sort_values(by=['交易日期'], inplace=True)
df['交易日期'] = pd.to_datetime(df['交易日期'])
df.reset_index(inplace=True, drop=True)


df["复权因子"] = (df["涨跌幅"] +1).cumprod()
# =====计算复权价

initial_price = df.iloc[0]['收盘价'] / (1 + df.iloc[0]['涨跌幅'])  # 计算上市价格
df['收盘价_后复权'] = initial_price * df['复权因子']  # 相乘得到复权价
df['开盘价_后复权'] = df['开盘价'] / df['收盘价'] * df['收盘价_后复权']
df['最高价_后复权'] = df['最高价'] / df['收盘价'] * df['收盘价_后复权']
df['最低价_后复权'] = df['最低价'] / df['收盘价'] * df['收盘价_后复权']
# df[['开盘价', '最高价', '最低价', '收盘价']] = df[['开盘价_后复权', '最高价_后复权', '最低价_后复权', '收盘价_后复权']]
df = df[['交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅', '开盘价_后复权', '最高价_后复权', '最低价_后复权', '收盘价_后复权']]

ma_short = 5
ma_long =50

df['ma_short'] = df["收盘价_后复权"].rolling(ma_short,min_periods=1).mean()
df['ma_long'] = df["收盘价_后复权"].rolling(ma_long,min_periods=1).mean()

# 买入信号
condition1 =(df["ma_short"] >=df["ma_long"])
condition2 =(df["ma_short"].shift(1) < df["ma_long"].shift(1))

df.loc[condition2 & condition1,"signal"] =1

# ===找出卖出信号
# 当天的短期均线小于等于长期均线
condition1 = (df['ma_short'] <= df['ma_long'])
# 上个交易日的短期均线大于长期均线
condition2 = (df['ma_short'].shift(1) > df['ma_long'].shift(1))
# 将买入信号当天的signal设置为0
df.loc[condition1 & condition2, 'signal'] = 0

df.drop(['ma_short', 'ma_long'], axis=1, inplace=True)

df['pos'] = df['signal'].shift()
df["pos"].fillna(method="ffill",inplace=True)
df['pos'].fillna(value=0, inplace=True)  # 将初始行数的position补全为0


# ===跌停时不得买卖股票考虑进来
# 找出开盘涨停的日期
# 今天的开盘价相对于昨天的收盘价上涨了9.7%。为什么用9.7%？不用10%
cond_cannot_buy = df["开盘价_后复权"] >df["开盘价_后复权"].shift(1) *1.097
# 将开盘涨停日、并且当天position为1时的'pos'设置为空值
df.loc[ cond_cannot_buy & (df["pos"]==1),'pos'] =None

# 找出开盘跌停的日期
# 今天的开盘价相对于昨天的收盘价下跌了9.7%
cond_cannot_sell = df['开盘价_后复权'] < df['收盘价_后复权'].shift(1) * 0.903
# 将开盘跌停日、并且当天position为0时的'pos'设置为空值
df.loc[cond_cannot_sell & (df['pos'] == 0), 'pos'] = None

df["pos"].fillna(method="ffill",inplace=True)

df =df.iloc[250-1:]
df.iloc[0,-1]=0


# =====计算实际资金曲线(简单方法)
# 资金曲线是一个策略最终的结果。是评价一个策略最重要的标准。

# ==计算实际资金曲线
# 首先计算资金曲线每天的涨幅
# 当当天空仓时，pos为0，资产涨幅为0
# 当当天满仓时，pos为1，资产涨幅为股票本身的涨跌幅
df['equity_change'] = df['涨跌幅'] * df['pos']
# 根据每天的涨幅计算资金曲线
df['equity_curve'] = (df['equity_change'] + 1).cumprod()
# print df[['交易日期', '收盘价_后复权', 'pos', 'equity_change', 'equity_curve']]
# exit()

# 这样计算方式的缺点：
# 没有考虑交给券商的手续费,以及没有考虑交给国家的印花税
# 没有考虑交易的滑点
# 以及没有考虑...


df = df[['交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅', 'pos']]

df.reset_index(inplace=True,drop =True)


# ===设定参数
initial_money = 1000000  # 初始资金，默认为1000000元
slippage = 0.01  # 滑点，默认为0.01元
c_rate = 5.0 / 10000  # 手续费，commission fees，默认为万分之5
t_rate = 1.0 / 1000  # 印花税，tax，默认为千分之1


df.at[0,"hold_num"] =0
df.at[0,"stack_value"] =0
df.at[0,"actual_pos"] = 0

print(df )