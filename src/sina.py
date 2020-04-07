#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 20-3-30 下午3:32
# @Author  : Miaoyuan.Shi
# @Site    : 
# @File    : sina.py
# @mail: jeff.shi@aispeech.com
import json
import requests
import codecs
from urllib.request import quote, unquote
import demjson
from datetime import datetime
from mysql_interface import mysql_interface
import pymysql
import time


class sina():
    def __init__(self):
        self.data_url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={}&scale=5&ma=5&datalen={}'
        self.stock = ''
        self.data_len = 300
        self.mysql = mysql_interface()

    def get_day_url (self,stock_id):
        self.stock = stock_id
        self.data_url = self.data_url.format(stock_id,self.data_len)
        return self.data_url

    def new_table(self,stock_id):
        sql = """
                create table {}(
                day DATE,
                time TIME,
                open float,
                high float,
                low float,
                close float,
                volume int,
                ma_price float,
                ma_volume int
                )
            """.format(stock_id)
        cur = self.mysql.conn.cursor()
        cur.execute(sql)
        cur.close()

    def new_all_table(self):
        fn = codecs.open('../data/stock.txt','r','utf-8')
        for line in fn:
            line = line.strip()
            line = line.split('\t')
            code = line[1]
            self.new_table(code)

    def request_day_data(self,stock_id,day):
        self.stock = stock_id
        self.data_url = self.data_url.format(stock_id,self.data_len)
        response = requests.request("GET", self.data_url)
        res = response.text
        res = demjson.decode(res)
        items = []
        for item in res:
            if day in item['day']:
                real_tiem = item['day']
                item['day'] = real_tiem.split()[0]
                item['time'] = real_tiem.split()[1]
                items.append(item)
        return items

    def request_all_day(self,day):
        fn = codecs.open('../data/stock.txt','r','utf-8')
        for line in fn:
            line = line.strip()
            line = line.split('\t')
            print(line)
            code = line[1]
            time.sleep(1)
            self.request_day_data(code,day)

    def insert_today_data(self,stock_id,day):
        cur = self.mysql.conn.cursor()
        if not day:
            day = datetime.now().strftime("%Y-%m-%d")
        res = self.request_day_data(stock_id,day)
        if res:
            sql = "insert into {}(day,time,open,high,low,close,volume,ma_price,ma_volume) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(stock_id)
            for item in res:
                print(item)
                cur.execute(sql, [item['day'],item['time'],item['open'],item['high'],item['low'],item['close'],item['volume'],item['ma_price5'],item['ma_volume5']])
            self.mysql.conn.commit()
            cur.close()

    def insert_all_today_data(self,day):
        fn = codecs.open('../data/stock.txt','r','utf-8')
        count = 0
        for line in fn:
            count+=1
            line = line.strip()
            line = line.split('\t')
            print(line,count)
            time.sleep(2)
            code = line[1]
            self.insert_today_data(code,day)
