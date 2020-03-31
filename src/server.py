#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 20-3-30 下午3:22
# @Author  : Miaoyuan.Shi
# @Site    : 
# @File    : server.py
# @mail: jeff.shi@aispeech.com
from flask import Flask
from sina import sina
from datetime import datetime
import json

app = Flask(__name__)
sina_sample = sina()

@app.route('/update_today_stock')
def update_today_stock():
    sina_sample.insert_all_today_data()
    return 'Update Success'

@app.route('/create_all_stock')
def hello():
    sina_sample.new_all_table()
    return 'hello'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)