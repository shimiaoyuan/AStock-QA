#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 20-3-30 下午3:22
# @Author  : Miaoyuan.Shi
# @Site    : 
# @File    : server.py
# @mail: jeff.shi@aispeech.com
from flask import Flask
from flask import request
from sina import sina
from datetime import datetime
import json

app = Flask(__name__)
sina_sample = sina()

@app.route('/update_today_stock')
def update_today_stock():
    day = request.args.get('day', default='', type=str)
    sina_sample.insert_all_today_data(day)
    return 'Update Success'

@app.route('/create_all_stock')
def hello():
    sina_sample.new_all_table()
    return 'Create Success'

@app.route('/delete_day_stock')
def delete_today_stock():
    day = request.args.get('day', default='', type=str)
    sina_sample.delete_oneday_all_data(day)
    return 'Delete Success'

@app.route('/stock_gain')
def search_stock_gain():
    day = request.args.get('day', default='', type=str)
    gain = request.args.get('gain', default='', type=str)
    st = request.args.get('st', default='', type=str)

    gain = float(gain)
    st = bool(st)
    data = sina_sample.stock_gain(day,gain,st)

    return data

@app.route('/stock_gain_time')
def search_stock_gain_time():
    day = request.args.get('day', default='', type=str)
    time = request.args.get('time', default='', type=str)
    gain = request.args.get('gain', default='', type=str)
    st = request.args.get('st', default='', type=str)
    open = request.args.get('open', default='', type=str)

    gain = float(gain)
    st = bool(st)
    open = bool(open)
    data = sina_sample.stock_gain_time(day,time, gain, st,open)
    return data

@app.route('/stock_gain_break')
def search_stock_gain_break():
    day = request.args.get('day', default='', type=str)
    gain = request.args.get('gain', default='', type=str)
    st = request.args.get('st', default='', type=str)

    gain = float(gain)
    st = bool(st)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,threaded=True)