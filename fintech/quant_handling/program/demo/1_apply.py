

import pandas as pd
from fintech.quant_handling.program import Functions

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行



code = 'sz300001'
df = Functions.import_stock_data(code)


def f1(x):
    return x +100


# print(df[["收盘价"]].apply(f1))

print(df["收盘价"].apply(lambda x :int(x *100)))
