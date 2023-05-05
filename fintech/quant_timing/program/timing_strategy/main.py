import sys

import pandas as pd
import Signals  # 同一级目录直接import
import Timing_Functions
from fintech.quant_timing.program import Functions  # 或者import program.Function
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行



# =====第一个模块：数据准备
# ===读入数据

code = "sz300001"
df = Functions.import_stock_data(code)
if df.shape[0] <250:
    print("股票上市未满一年，不运行策略")
    exit()


fuquan_type = "后复权"

