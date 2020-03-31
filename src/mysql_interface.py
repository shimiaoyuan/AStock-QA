#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 20-3-30 下午5:09
# @Author  : Miaoyuan.Shi
# @Site    : 
# @File    : mysql_interface.py
# @mail: jeff.shi@aispeech.com
import pymysql
class mysql_interface():
    def __init__(self):
        self.host = 'localhost'
        self.usr = 'root'
        self.password = 'miaoyuan.shi'
        self.database = 'stock'
        self.conn = pymysql.connect(self.host, self.usr,self.password,self.database)

    def get_conn(self,host,usr,password,databse):
        self.conn = pymysql.connect(host, usr, password,databse)
        return self.conn

