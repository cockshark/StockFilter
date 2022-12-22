#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   wush
@License :   (C) Copyright 2021-9999, {AKULAKU}
@Contact :   
@Software:   PyCharm
@File    :   timeUtils.py
@Time    :   2022/12/13 19:14
@Desc    :

'''

__author__ = "wush"

from datetime import timedelta
from datetime import datetime


def get_today_date(format_date: str = "%Y_%m_%d"):
    today = datetime.today().date()
    return today.strftime(format_date)


def get_diff_x_date(date: str, diff: int, format_date: str = "%Y%m%d") -> str:
    """
    获取固定时间前后x天的日期
    如果获取过去，diff 为负数
    如果获取未来，diff 为正数
    >>> get_diff_x_date("20221222", -3) # 获取20221222 往前第三天的日期：20221219
    >>> get_diff_x_date("20221222", 4) # 获取20221222 未来第四天的日期： 20221226
    :param date: str
    :param diff: int
    :param format_date:str
    :return: str
    """
    get_date = datetime.strptime(date, format_date)
    target_date = get_date + timedelta(diff)
    return target_date.strftime(format_date)


if __name__ == '__main__':
    print(get_today_date())
    print(get_today_date("%Y%m%d"))
    print(get_diff_x_date("20221223", 18))
    print(get_diff_x_date("20221222", -39))
