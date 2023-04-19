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

from typing import List, Optional

from strategy.base import BaseStrategy
from utils.stockUtils import (
    get_item_most_six_days_data, is_not_open_upStop, is_upStop
)

from public.attributes import StockAttributes
from utils.timeUtils import get_diff_x_date, get_today_date


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

    def __init__(self):
        self.up10Percent_date: str = ""  # 涨停日期，多个涨停视为一个涨停，取最后一天的日期
        self.up10Percent_turnover: float = 0  # 记录涨停当日成交量

    def filter_turnOverRate_lessThan20(self, stock: dict) -> bool:
        """
        换手率3%—20%以内优选
        :param stock:
        :return:
        """
        return self._filter_turnoverRate(stock, max_turnoverRate=20, min_turnoverRate=3)

    def get_after_up10Percent_date(self, recent_records: List[dict]) -> str:
        before_target = None
        for idx, record in enumerate(recent_records):
            if record[StockAttributes.date].replace("-", "") == self.up10Percent_date:
                before_target = idx
                break

        return recent_records[before_target - 1][StockAttributes.date]

    def judge_release_hugeQuant_after_upStop(self, recent_records: List[dict]) -> bool:
        after_up10_percent_date = get_diff_x_date(self.up10Percent_date, 1)  # 有可能是非交易日
        after_up10_percent_date = self.get_after_up10Percent_date(recent_records)

        after_up10_percent_record = list(
            filter(lambda x: x[StockAttributes.date] == after_up10_percent_date, recent_records))[0]

        proportion = float(after_up10_percent_record[StockAttributes.turnover]) / self.up10Percent_turnover

        if proportion > 1.5:  # 当日的量超过了过去的1.5倍 暂定为巨量
            return True

        return False

    def judge_up10_percent_by_turnover_last_x_day(self, stock: dict) -> bool:
        """
        判断近期是否涨停
        涨停后  换手率3%—20%以内优选
        涨停后第二天不是巨量。
        :param stock:
        :return:
        """
        today = get_today_date("%Y%m%d")
        code = str(stock[StockAttributes.code]).zfill(6)
        stock = stock[StockAttributes.name]
        print(f"正在分析：{stock} ({code}).....")
        recent_records = get_item_most_six_days_data(code)  # 按照最新数据排列

        flag = False  # 有涨停 标记
        for idx, record in enumerate(recent_records):
            # 最新价不超过max price
            if idx > 5 and flag is False:  # 五天之内都没有过涨停，不符合规则
                return False

            if self._filter_upStop_by_turnOver(record):  # 涨停，且振幅>0（非一字）
                flag = True
                self.up10Percent_date = record[StockAttributes.date].replace("-", "")  # 记录这天涨停的日期
                if self.up10Percent_date == today:  # 当天涨停也算
                    return True
                self.up10Percent_turnover = float(record[StockAttributes.turnover])  # 记录涨停当日成交量
                break
            #     continue
            # if flag is True:  # 找到过了最新的涨停日期
            #     if self._filter_upStop_by_turnOver(record):
            #         continue  # 还是涨停就继续往前面找
            #     else: # 如果不是涨停，
            #         if self._filter_lessThan_AmplitudeOfShock(record, 5):
            #             # 涨停板前一天收盘价涨幅不超过5%（多个涨停视为一个涨停）

            if self.filter_turnOverRate_lessThan20(record):
                continue

        if flag is False:
            return False

        # 涨停后第二天不是巨量
        if not self.judge_release_hugeQuant_after_upStop(recent_records):
            return True


if __name__ == '__main__':
    thunder = ThunderStrategy()
    sample = {'股票名称': '翠微股份', '股票代码': '603123', '日期': '2022-12-23', '开盘': 13.42, '收盘': 14.13,
              '最高': 14.79, '最低': 13.42, '成交量': 776101, '成交额': 1102542341.0, '振幅': 10.16, '涨跌幅': 4.82,
              '涨跌额': 0.65, '换手率': 11.9}

    thunder.judge_up10_percent_by_turnover_last_x_day(sample)
