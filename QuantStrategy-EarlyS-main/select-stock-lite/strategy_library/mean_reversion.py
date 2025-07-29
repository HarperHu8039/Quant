# strategy_library/mean_reversion.py

class MeanReversionStrategy:
    def __init__(self):
        self.name = "均值回归策略"
        self.hold_period = "W"
        self.select_num = 20
        self.factor_name = "mean_reversion_score"

    def filter_before_select(self, df):
        # 过滤停牌、ST、上市小于250天
        df = df[(df['是否交易'] == 1) & (~df['是否ST']) & (df['上市至今交易日'] > 250)]
        return df

    def calc_select_factor(self, df):
        # 假设 zscore, macd_hist, momentum 三个因子已经在因子计算中准备好了
        score = (
            (df['zscore'].rank(pct=True) * -1) +
            (df['macd_hist'].rank(pct=True)) +
            (df['momentum'].rank(pct=True))
        )
        return score.to_frame(self.factor_name)
