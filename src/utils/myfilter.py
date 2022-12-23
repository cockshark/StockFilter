#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   wush
@License :   (C) Copyright 2021-9999, {AKULAKU}
@Contact :   
@Software:   PyCharm
@File    :   myfilter.py
@Time    :   2022/12/13 17:20
@Desc    :

'''

__author__ = "wush"

from pathlib import Path

import efinance as ef
import pandas as pd
from pydantic import Json

from conf import dataFrame_path
from utils.timeUtils import get_today_date
from public.attributes import StockAttributes


def _filter_stock(item: dict) -> bool:
    """
    过滤 st *st
    股价超过50 小于2块
    :param item:
    :return:
    """
    try:
        if float(item[StockAttributes.now_price]) >= 50 or float(item[StockAttributes.now_price]) < 2:
            return False
        if float(item[StockAttributes.marketValue]) >= 50000000000:
            return False
        # if item[StockAttributes.turnoverRate] > 20:
        #     return False
        if item[StockAttributes.name].lower().startswith("ST") or \
                item[StockAttributes.name].lower().startswith("*ST") or \
                (len(str(item[StockAttributes.code])) == 6 and
                 (str(item[StockAttributes.code]).startswith("30") or
                  str(item[StockAttributes.code]).startswith("68"))):
            return False
        return True
    except Exception as e:
        return False


def get_today_filter_stock():
    """
    获取当天的股票信息
    :return:
    """
    today = get_today_date()
    path = dataFrame_path.joinpath(f"stock_{today}.json")  # type: Path
    if not path.exists():  # 不存在就读取
        print("当天数据不存在，重新读取")
        today_stocks = cache_sz_stock()
    else:
        today_stocks = pd.read_json(path)

    return list(filter(_filter_stock, today_stocks.to_dict(orient="records")))


def cache_sz_stock() -> Json:
    """
    获取当天主板的相关信息，主要是代码信息
    :return: 返回df 会比较好处理
    """
    today_stocks = ef.stock.get_realtime_quotes('沪深A股')  # type: pd.DataFrame
    is_saved = save_to_txt(today_stocks)
    if is_saved is False:
        raise ValueError("保存当天股票失败，查询接口出错")

    return today_stocks


def save_to_txt(data: pd.DataFrame) -> bool:
    """
    存储当天的数据到txt，避免反复读取
    :param data:
    :return:
    """
    today = get_today_date()
    path = dataFrame_path.joinpath(f"stock_{today}.json")  # type: Path
    try:
        data.to_json(path, orient="records", indent=4, force_ascii=False)
        return True
    except (ValueError, Exception) as e:
        from traceback import print_exc
        print_exc()
        return False


if __name__ == '__main__':
    data = get_today_filter_stock()
    print(len(data))
    # print(data)
