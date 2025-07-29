import pandas as pd
import talib

def add_factor(df: pd.DataFrame, param=None, fin_data=None, col_name="macd_hist"):
    df = df.copy()
    close = df['收盘价'].astype(float)
    macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df[col_name] = hist
    return df, {col_name: 'last'}
