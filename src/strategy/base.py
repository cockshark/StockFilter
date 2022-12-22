# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   wush
@License :   (C) Copyright 2021-9999, {AKULAKU}
@Contact :   
@Software:   PyCharm
@File    :   base.py
@Time    :   2022/12/22 15:20d
@Desc    :

'''

__author__ = "wush"

from typing import List

from public.attributes import StockAttributes

from utils.stockUtils import (
    is_upStop, is_not_open_upStop, is_up10_percent_by_turnover_last_x_day
)


class BaseStrategy(object):

    def __init__(self, code_pool: List[dict]):
        self.code_pool = code_pool  # 基础股票池，可通过util直接获取

    @staticmethod
    def _filter_price(stock: dict, maxPrice: float, minPrice: float = 1) -> bool:
        """
        过滤价格
        :param stock:
        :param maxPrice:
        :param minPrice:
        :return:
        """
        return minPrice <= float(stock[StockAttributes.now_price]) <= maxPrice

    @staticmethod
    def _filter_upStop_by_turnOver(stock: dict):
        """
        判斷股票是否通過換手漲停，非一字
        :param stock:
        :return:
        """
        return all([is_upStop(stock), is_not_open_upStop(stock)])

    @staticmethod
    def _filter_turnoverRate(stock: dict, max_turnoverRate: float = 20, min_turnoverRate: float = 2) -> bool:
        return min_turnoverRate <= float(stock[StockAttributes.turnoverRate]) <= max_turnoverRate

    @staticmethod
    def _filter_moreThan_AmplitudeOfShock(stock: dict, amplitude: float,):
        """
        漲跌圖大於等於 某個值
        :param stock:
        :param amplitude:
        :return:
        """
        return float(stock[StockAttributes.AmplitudeOfShock]) >= amplitude

    @staticmethod
    def _filter_lessThan_AmplitudeOfShock(stock: dict, amplitude: float,):
        """
        漲跌圖小於等於 某個值
        :param stock:
        :param amplitude:
        :return:
        """
        return float(stock[StockAttributes.AmplitudeOfShock]) <= amplitude


if __name__ == '__main__':
    pass
