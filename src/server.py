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
    sina_sample.insert_today_data('sz002412')
    return 'Update Success'

@app.route('/hello')
def hello():
    return 'hello'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)