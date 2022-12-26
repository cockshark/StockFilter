#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   wush
@License :   (C) Copyright 2021-9999, {AKULAKU}
@Contact :   
@Software:   PyCharm
@File    :   server.py
@Time    :   2022/12/23 20:06
@Desc    :

'''

__author__ = "wush"

from fastapi import FastAPI

from handler.thunderHandler import filter_thunder_stocks

app = FastAPI()


@app.get("/today")
def get_thunder_stocks():
    result, todays = filter_thunder_stocks()

    return {"雷氏": result, "今日涨停": todays}


@app.get("/")
def hello_world():

    return "hello world"


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
