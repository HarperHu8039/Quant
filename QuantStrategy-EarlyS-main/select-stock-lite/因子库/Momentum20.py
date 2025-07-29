import pandas as pd

def add_factor(df: pd.DataFrame, param=None, fin_data=None, col_name="momentum"):
    df = df.copy()
    df[col_name] = df['收盘价'] / df['收盘价'].shift(20) - 1
    return df, {col_name: 'last'}
