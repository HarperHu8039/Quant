
import time
import warnings

import pandas as pd

from core.model.backtest_config import create_factory
from program.step1_整理数据 import prepare_data
from program.step2_计算因子 import calculate_factors
from program.step3_选股 import select_stocks
from program.step4_实盘模拟 import simulate_performance

# ====================================================================================================
# ** 脚本运行前配置 **
# 主要是解决各种各样奇怪的问题
# ====================================================================================================
warnings.filterwarnings('ignore')  # 过滤一下warnings

# pandas相关的显示设置，基础课程都有介绍
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.unicode.ambiguous_as_wide', True)  # 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.east_asian_width', True)


def find_best_params(factory):
    """
    寻找最优参数
    :return:
    """
    # ====================================================================================================
    # 1. 准备工作
    # ====================================================================================================
    print('参数遍历开始', '*' * 72)

    conf_list = factory.config_list
    for index, conf in enumerate(conf_list):
        print(f'参数组合{index + 1}｜共{len(conf_list)}')
        print(f'{conf.get_fullname()}')
        print()
    print('✅ 一共需要回测的参数组合数：{}'.format(len(conf_list)))
    print('分割线', '-' * 96)
    print()

    # 生成一个conf，拥有所有策略的因子
    dummy_conf_with_all_factors = factory.generate_all_factor_config()

    # ====================================================================================================
    # 2. 读取回测所需数据，并做简单的预处理
    # ====================================================================================================
    # 读取数据
    prepare_data(dummy_conf_with_all_factors)

    # ====================================================================================================
    # 3. 计算因子
    # ====================================================================================================
    # 然后用这个配置计算的话，我们就能获得所有策略的因子的结果，存储在 `data/cache/all_factors_df.pkl`
    calculate_factors(dummy_conf_with_all_factors)

    # ====================================================================================================
    # 4. 选股
    # - 注意：选完之后，每一个策略的选股结果会被保存到硬盘
    # ====================================================================================================
    reports = []
    for config in factory.config_list:
        print(f'{config.iter_round}/{len(factory.config_list)}', '-' * 72)
        select_results = select_stocks(config)
        report = simulate_performance(config, select_results, show_plot=False)
        reports.append(report)

    return reports


if __name__ == '__main__':
    print(f'🌀 系统启动中，稍等...')
    r_time = time.time()
    # ====================================================================================================
    # 1. 配置需要遍历的参数
    # ====================================================================================================
    # 因子遍历的参数范围
    strategies = []
    for select_num in (1, 3, 5, 10, 30):
        strategy = {
            'name': '小市值策略',  # 策略名，对应策略库中的文件名，比如`小市值_基本面优化.py`
            'hold_period': 'W',  # 持仓周期，W 代表周，M 代表月
            'select_num': select_num,  # 选股数量，可以是整数，也可以是小数，比如 0.1 表示选取 10% 的股票
            "factor_list": [  # 选股因子列表
                # 因子名称（与 factors 文件中的名称一致），排序方式（True 为升序，False 为降序），因子参数，因子权重
                ('市值', True, None, 1),  # 案例：使用市值因子，参数从小到大排序，无额外参数，市值因子权重为1
                # 可添加多个选股因子
            ],
            "filter_list": []  # 过滤因子列表
        }
        strategies.append(strategy)

    # ====================================================================================================
    # 2. 生成策略配置
    # ====================================================================================================
    print(f'🌀 生成策略配置...')
    backtest_factory = create_factory(strategies)

    # ====================================================================================================
    # 3. 寻找最优参数
    # ====================================================================================================
    report_list = find_best_params(backtest_factory)

    # ====================================================================================================
    # 4. 根据回测参数列表，展示最优参数
    # ====================================================================================================
    s_time = time.time()
    print(f'🌀 展示最优参数...')
    all_params_map = pd.concat(report_list, ignore_index=True)
    report_columns = all_params_map.columns  # 缓存列名

    # 合并参数细节
    sheet = backtest_factory.get_name_params_sheet()
    all_params_map = all_params_map.merge(sheet, left_on='param', right_on='策略详情', how='left')

    # 按照累积净值排序，并整理结果
    all_params_map.sort_values(by='累积净值', ascending=False, inplace=True)
    all_params_map = all_params_map[[*sheet.columns, *report_columns]].drop(columns=['param'])
    all_params_map.to_excel(backtest_factory.result_folder / f'最优参数.xlsx', index=False)
    print(all_params_map)
    print(f'✅ 完成展示最优参数，花费时间：{time.time() - s_time:.2f}秒，累计时间：{(time.time() - r_time):.3f}秒')
    print()
