import numpy as np

def calc_zscore_percentile(price_series):
    ma = price_series[-20:].mean()
    std = price_series[-20:].std()
    z = (price_series.iloc[-1] - ma) / std
    percentile = (price_series < price_series.iloc[-1]).sum() / len(price_series)
    return z, percentile

def mean_reversion_select(conf, current_data, price_data, indicator_data, positions):
    buy, sell = [], []
    df = current_data.copy()
    df = df[~df['paused'] & ~df['is_st']]
    df = df[(df['days_since_listed'] > 250) & (df['avg_turnover'] > 0.01)]
    stock_list = df['code'].tolist()

    for stock in stock_list:
        try:
            price_series = price_data[stock]
            if len(price_series) < 60:
                continue

            zscore, z_percentile = calc_zscore_percentile(price_series)
            macd_hist = indicator_data[stock]['macd_hist']
            ma5 = price_series[-5:].mean()
            ma20 = price_series[-20:].mean()
            momentum = (price_series.iloc[-1] / price_series.iloc[-20]) - 1
            hold = stock in positions

            criteria = 0
            if macd_hist > 0: criteria += 1
            if ma5 >= ma20 * 0.98: criteria += 1
            if momentum >= 0: criteria += 1

            if z_percentile <= 0.1 and not hold and criteria >= 2:
                buy.append(stock)

            if hold:
                cost_basis = positions[stock]['cost']
                price_now = price_series.iloc[-1]
                ret = price_now / cost_basis - 1
                if (z_percentile >= 0.9 or macd_hist < 0 or price_now < ma20 * 0.98 or
                    ret <= -0.08 or ret >= 0.15):
                    sell.append(stock)
        except:
            continue

    return buy, sell

