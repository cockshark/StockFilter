#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   wush
@License :   (C) Copyright 2021-9999, {AKULAKU}
@Contact :   
@Software:   PyCharm
@File    :   thunderStrategy.py
@Time    :   2022/12/22 15:20
@Desc    :

'''

__author__ = "wush"

from typing import List

from strategy.base import BaseStrategy


class ThunderStrategy(BaseStrategy):
    """
        1，前期需要涨停板（不是一字板涨停）
        2，涨停板前一天收盘价涨幅不超过5%
        3，涨停后5天内现价在涨停板最低位以上5%以下预警，涨停板最低价5%以下不设限（天数可调）
        4，涨停板不是14：30分后涨停的个股。（比较弱势）
        5，换手率3%—20%以内优选
        6，如果连续涨停，视为一个涨停。
        7，回调到涨停底的时间越短越好
        8，涨停后第二天不是巨量。
        9，涨停后回调区间长上影线越小越好
        10，不是处在放量成交密集压力区位
    """

    def __init__(self, code_pool: List[dict]):
        super().__init__(code_pool)

    def filter_up10Percent_stock(self, stock: dict) -> bool:
        """
        判断近期是否有涨停，多个涨停视为一个涨停，不要是一字板
        :param stock: dict
        :return: bool
        """
        return self._filter_upStop_by_turnOver(stock)



if __name__ == '__main__':
    pass
