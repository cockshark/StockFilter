#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   wush
@License :   (C) Copyright 2021-9999, {AKULAKU}
@Contact :   
@Software:   PyCharm
@File    :   __init__.py.py
@Time    :   2022/12/13 18:55
@Desc    :

'''

__author__ = "wush"

from pathlib import Path

project_path = Path().absolute().parent.parent

dataFrame_path = project_path.joinpath("uplimits")

if __name__ == '__main__':
    print(project_path)
    print(dataFrame_path)
