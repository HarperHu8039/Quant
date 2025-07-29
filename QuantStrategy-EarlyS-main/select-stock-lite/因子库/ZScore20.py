import pandas as pd

def add_factor(df: pd.DataFrame, param=None, fin_data=None, col_name="zscore"):
    df = df.copy()
    df[col_name] = (df['收盘价'] - df['收盘价'].rolling(20).mean()) / df['收盘价'].rolling(20).std()
    return df, {col_name: 'last'}  # 'last' 表示对周期转换采用“最后一个”值
