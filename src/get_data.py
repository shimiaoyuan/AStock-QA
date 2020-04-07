#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 20-3-30 下午3:22
# @Author  : Miaoyuan.Shi
# @Site    : 
# @File    : get_data.py
# @mail: jeff.shi@aispeech.com
import json
import requests
import codecs
from urllib.request import quote, unquote
from sina import sina
from datetime import datetime

import time
import re
sample = sina()
today = datetime.now().strftime("%Y-%m-%d")
# print(sample.request_all_day('2020-04-01'))
print(sample.change_data_type)
