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
from datetime import datetime,timedelta
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
        print(self.data_url.format(stock_id,self.data_len))
        response = requests.request("GET", self.data_url.format(stock_id,self.data_len))
        res = response.text
        res = demjson.decode(res)
        items = []
        if res:
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
                if item:
                    cur.execute(sql, [item['day'],item['time'],item['open'],item['high'],item['low'],item['close'],item['volume'],item['ma_price5'],item['ma_volume5']])
            self.mysql.conn.commit()
            cur.close()

    def insert_all_today_data(self,day):
        fo = codecs.open('../data/date.txt','a','utf-8')
        fo.write(day+'\n')
        fo.close()

        fn = codecs.open('../data/stock.txt','r','utf-8')
        count = 0
        for line in fn:
            count+=1
            line = line.strip()
            line = line.split('\t')
            print(line,count)
            time.sleep(1)
            code = line[1]
            self.insert_today_data(code,day)

    def change_data_type(self):
        fn = codecs.open('../data/stock.txt','r','utf-8')
        cur = self.mysql.conn.cursor()

        count = 0
        for line in fn:
            count+=1
            print(count)
            line = line.strip()
            line = line.split('\t')
            code = line[1]
            sql = "ALTER TABLE {} MODIFY COLUMN ma_volume bigint;".format(code)
            cur.execute(sql)
        self.mysql.conn.commit()
        cur.close()

    #添加新股票
    def add_new_stock(self,name,stock_id):
        fn = codecs.open('../data/stock.txt','a','txt')
        fn.write(name+'\t'+stock_id+'\n')
        fn.close()
        self.new_table(stock_id)

    #删除数据
    def delete_oneday_stock_data(self,stock_id,day):
        cur = self.mysql.conn.cursor()
        sql = "DELETE FROM {} WHERE day = '{}'".format(stock_id,day)
        cur.execute(sql)
        self.mysql.conn.commit()
        cur.close()

    def delete_oneday_all_data(self,day):
        fn = codecs.open('../data/stock.txt','r','utf-8')
        count = 0
        for line in fn:
            count+=1
            line = line.strip()
            line = line.split('\t')
            code = line[1]
            print(line, count)
            self.delete_oneday_stock_data(code,day)

    #根据日期查询
    def search_oneday_stock(self,ziduan,stock_id,day):
        cur = self.mysql.conn.cursor()
        sql = "SELECT time,{} FROM {} WHERE day = '{}'".format(ziduan,stock_id,day)
        cur.execute(sql)
        data = cur.fetchall()
        self.mysql.conn.commit()
        cur.close()
        return data

    #获取前一天的日期
    def find_yesterday(self,day):
        day_line = []
        fn = codecs.open('../data/date.txt','r','utf-8')
        for line in fn:
            line = line.strip()
            if line not in day_line:
                day_line.append(line)

        today_index = day_line.index(day)
        return day_line[today_index-1]

    #找到收盘价
    def find_last_price(self,stock_id,day):
        data = self.search_oneday_stock('close',stock_id, day)
        time_price = {}

        for time,price in data:
            time_price[time] = price
        time_line = sorted(time_price.keys())
        last_price = 1e-5
        if time_line:
            last = time_line[-1]
            last_price = time_price[last]
        return last_price

    ##分析股票一天涨跌幅度
    def gain_one_stock(self,stock_id,day):
        #昨天收盘价
        yesterday = self.find_yesterday(day)
        yesterday_price = self.find_last_price(stock_id,yesterday)
        #当天收盘价
        today_price = self.find_last_price(stock_id,day)
        gain = (today_price/yesterday_price)-1
        gain*=100
        gain = round(gain, 3)
        return gain

    ##分析股票一天在某个时间点前的涨跌幅度
    def gain_one_time_stock(self,stock_id,day,query_time):
        #昨天收盘价
        yesterday = self.find_yesterday(day)
        yesterday_price = self.find_last_price(stock_id,yesterday)

        #当天time之前的收盘价
        data = self.search_oneday_stock('close',stock_id,day)
        query_time =  datetime.strptime(query_time,"%H:%M:%S")
        query_time = query_time-datetime(1900, 1, 1)
        time_price = {}
        for time,price in data:
            if time<query_time:
                time_price[time] = price

        time_line = sorted(time_price.keys())
        last_price = 1e-5
        if time_line:
            last = time_line[-1]
            last_price = time_price[last]

        gain = (last_price/yesterday_price)-1
        gain*=100
        gain = round(gain, 3)
        return gain

    ##分析股票一天是否打到过某个gain,最后又无法达到
    def gain_one_stock_break(self,stock_id,day):
        #昨天收盘价
        yesterday = self.find_yesterday(day)
        yesterday_price = self.find_last_price(stock_id,yesterday)
        data = self.search_oneday_stock('close',stock_id,day)

        time_price = {}
        for time,price in data:
            time_price[time] = price
        time_line = sorted(time_price.keys())
        first = time_line[0]

        gain_line = []
        for item in time_line:
            item_gain = (time_price[item] / yesterday_price) - 1
            item_gain *= 100
            item_gain = round(item_gain, 3)
            gain_line.append(item_gain)

        return gain_line

    def stock_gain(self,day,gain,st):
        fn = codecs.open('../data/stock.txt','r','utf-8')
        count = 0
        res = {}
        for line in fn:
            count+=1
            line = line.strip()

            if (not st )and 'ST' in line:
                continue

            line = line.split('\t')
            print(line,count)
            code = line[1]
            gain_res = self.gain_one_stock(code,day)
            if gain_res>= gain:
                res[code] = gain_res

        return json.dumps(res,ensure_ascii=False)

    #time之前达到gain的数,且收盘大于或小于达到gain的数
    def stock_gain_time(self,day,time,gain,st,open):
        fn = codecs.open('../data/stock.txt','r','utf-8')
        count = 0
        res = {}
        for line in fn:
            count+=1
            line = line.strip()
            print(st)
            if (not st )and 'ST' in line:
                continue

            line = line.split('\t')
            code = line[1]
            gain_time = self.gain_one_time_stock(code,day,time)
            gain_day = self.gain_one_stock(code, day)
            print(open)
            if not open:
                if (gain_time>= gain) and (gain_day>=gain):
                    res[code] = gain_day
            else:
                if (gain_time >= gain) and (gain_day < gain):
                    res[code] = gain_day

        return json.dumps(res,ensure_ascii=False)

    def stock_gain_break(self,day,gain,st):
        fn = codecs.open('../data/stock.txt','r','utf-8')
        count = 0
        res = {}
        for line in fn:
            count+=1
            line = line.strip()

            if (not st )and 'ST' in line:
                continue

            line = line.split('\t')
            print(line,count)
            code = line[1]
            gain_line = self.gain_one_stock_break(code,day)
            gain_break = False
            for i in range(0,len(gain_line)-1):
                if gain_line[i]>gain:
                    gain_break = True
                    break
            if (gain_break) and (gain_line[-1]<gain):
                res[code] = gain_line[-1]
        return json.dumps(res,ensure_ascii=False)
