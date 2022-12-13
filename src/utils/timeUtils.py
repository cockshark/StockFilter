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

# import datetime
from datetime import datetime


def get_today_date():
    today = datetime.today().date()
    return today.strftime("%Y_%m_%d")


if __name__ == '__main__':
    print(get_today_date())
