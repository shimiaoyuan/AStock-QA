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

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)