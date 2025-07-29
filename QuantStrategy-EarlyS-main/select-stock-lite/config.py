
from pathlib import Path

start_date = "2009-01-01"
# 回测数据的起始时间。如果因子使用滚动计算方法，在回测初期因子值可能为 NaN，实际的首次交易日期可能晚于这个起始时间。

end_date = None
# 回测数据的结束时间。可以设为 None，表示使用最新数据；也可以指定具体日期，例如 '2024-11-01'。


# 策略明细
strategy = {
    "name": "小市值策略",  # 策略名
    "hold_period": "W",  # 持仓周期，W 代表周，M 代表月
    "select_num": 1,  # 选股数量，可以是整数，也可以是小数，比如 0.1 表示选取 10% 的股票
    "factor_list": [  # 选股因子列表
        # ** 因子格式说明 **
        # 因子名称（与 '因子库' 文件中的名称一致），排序方式（True 为升序，False 为降序），因子参数，因子权重
        ("市值", True, None, 1),
        # 案例说明：使用'市值.py'因子，从小到大排序（越小越是我想要），None表示无额外参数，后面计算复合选股因子的时候权重为1
        # 可添加多个选股因子
    ],
    "filter_list": [],  # 过滤因子列表
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
