#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   wush
@License :   (C) Copyright 2021-9999, {AKULAKU}
@Contact :   
@Software:   PyCharm
@File    :   thunderHandler.py
@Time    :   2022/12/23 17:13
@Desc    :

'''

__author__ = "wush"

from strategy.thunderStrategy import ThunderStrategy

from utils.myfilter import get_today_filter_stock
from public.attributes import StockAttributes


def filter_thunder_stocks(max_price: float = 15):
    """
    获取符合条件的所有代码
    :return:
    """
    thunderFilter = ThunderStrategy()
    samples = get_today_filter_stock()
    # 过滤创业板，科创板，st，以及*st
    sz_stocks = filter(thunderFilter.filter_remove_30x_68x_stx_stock, samples)
    # 过滤出符合涨停需求
    thunder_stocks = filter(thunderFilter.judge_up10_percent_by_turnover_last_x_day, sz_stocks)
    # 过滤出符合价格
    thunder_stocks = filter(lambda x: float(x[StockAttributes.now_price]) <= max_price, thunder_stocks)

    result = []
    for stock in thunder_stocks:
        code = str(stock[StockAttributes.code]).zfill(6)
        result.append(code)

    print(result)
    return result


if __name__ == '__main__':
    filter_thunder_stocks(max_price=15)
