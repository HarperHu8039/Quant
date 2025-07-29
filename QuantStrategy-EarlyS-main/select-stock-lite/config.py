
from pathlib import Path

start_date = "2009-01-01"
# 回测数据的起始时间。如果因子使用滚动计算方法，在回测初期因子值可能为 NaN，实际的首次交易日期可能晚于这个起始时间。

end_date = None
# 回测数据的结束时间。可以设为 None，表示使用最新数据；也可以指定具体日期，例如 '2024-11-01'。


# 策略明细
strategy = {
    "name": "均值回归策略",
    "hold_period": "W",
    "select_num": 20,
    "factor_list": [
        ("ZScore20", False, None, 1),
        ("MACDHist", False, None, 1),
        ("Momentum20", False, None, 1)
    ],
    "filter_list": [],
}

# 💡运行提示：
# - 修改hold_period之后，需要执行step2因子计算，不需要再次准备数据
# - 修改select_num之后，只需要再执行step3选股即可，不需要准备数据和计算因子
# - 修改factor_list之后，需要执行step2因子计算，不需要再次准备数据
# - 修改filter_list之后，需要执行step2因子计算，不需要再次准备数据

# 资金曲线再择时
equity_timing = {"name": "移动平均线", "params": [20]}

# =====数据源的定义=====
# ** 股票日线数据 和 指数数据是必须的，其他的数据可以在 data_sources 中定义 **
# (必选) 股票日线数据
stock_data_path = r"C:\Users\asus\Desktop\量化分析\trading_database\stock-trading-data"
# (必选) 指数数据路径
index_data_path = r"C:\Users\asus\Desktop\量化分析\trading_database\stock-main-index-data"
# (可选) 财务数据
fin_data_path = r"C:\Users\asus\Desktop\量化分析\trading_database\stock-fin-data-xbx"

# =====以下参数几乎不需要改动=====
initial_cash = 10_0000  # 初始资金10w
# 手续费
c_rate = 1.2 / 10000
# 印花税
t_rate = 1 / 1000
# 上市至今交易天数
days_listed = 250

# =====参数预检查=====
if Path(stock_data_path).exists() is False:
    print(f"股票日线数据路径不存在：{stock_data_path}，请检查配置，程序退出")
    exit()
if Path(index_data_path).exists() is False:
    print(f"指数数据路径不存在：{index_data_path}，请检查配置，程序退出")
    exit()

# =====新增：策略控制参数=====
strategy_name = "mean_reversion"  # ← 这里控制主程序选择哪个策略模块执行

# 针对 mean_reversion 策略的参数（用于 rebalance）
max_hold = 10
min_cash_per_stock = 10000
