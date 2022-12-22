#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   wush
@License :   (C) Copyright 2021-9999, {AKULAKU}
@Contact :   
@Software:   PyCharm
@File    :   stockUtils.py
@Time    :   2022/12/22 16:35
@Desc    :

'''

__author__ = "wush"

from typing import List, Optional

import efinance as ef
import pandas as pd

from utils.timeUtils import (
    get_today_date,
    get_diff_x_date
)
from public.attributes import StockAttributes


def get_item_most_six_days_data(code: str) -> Optional[List[dict]]:
    """
    获取一个股票最多六天内的数据,锚定10天，避开上下周六周日没有数据
    按照日期倒叙排列，最早日期放最前面
    :param code:
    :return:
    """
    diff = -9
    end = get_today_date("%Y%m%d")  # 结束日期
    begin = get_diff_x_date(end, diff)
    recent_data = ef.stock.get_quote_history(code, beg=begin, end=end)
    if len(recent_data) == 0:
        return None
    records = recent_data.to_dict(orient="records")

    records.sort(key=lambda x: x[StockAttributes.date], reverse=True)

    return records


"""
基本判斷策略
"""


def is_upStop(stock: dict) -> bool:
    """
    是否涨停
    :param stock:
    :return:
    """
    return 9.95 <= float(stock[StockAttributes.AmplitudeOfShock]) <= 10.05


def is_not_open_upStop(stock: dict):
    """
    开盘是否就涨停，是否一字涨停——振幅大于0
    :param stock:
    :return:
    """
    return float(stock[StockAttributes.AmplitudeOfShockOfToday]) > 0


def is_up10_percent_by_turnover_last_x_day(code: str) -> bool:
    """
    判断一只股票近期x天有涨停，且换手上去的，不是一字板(振幅大于0)
    :param code: str
    :return: bool
    """

    recent_records = get_item_most_six_days_data(code)  # 按照最新数据排列
    for idx, record in enumerate(recent_records):
        if idx > 5:
            return False
        if all([is_not_open_upStop(record), is_upStop(record)]):  # 涨停，且振幅>0（非一字）
            return True


if __name__ == '__main__':
    data = get_item_most_six_days_data("000610")
    print(data)
    print(len(data))
