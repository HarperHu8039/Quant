def rebalance(portfolio, buy_list, sell_list, price_data, cash, conf):
    max_hold = conf.get("max_hold", 10)
    min_cash = conf.get("min_cash_per_stock", 10000)

    for stock in sell_list:
        if stock in portfolio:
            del portfolio[stock]

    available_slots = max_hold - len(portfolio)
    selected_buys = buy_list[:available_slots]
    invest_per_stock = min(cash / max(1, len(selected_buys)), min_cash)

    for stock in selected_buys:
        entry_price = price_data[stock].iloc[-1]
        portfolio[stock] = {
            'cost': entry_price,
            'holding_days': 1,
            'weight': invest_per_stock
        }

    for stock in portfolio:
        portfolio[stock]['holding_days'] += 1

    return portfolio
