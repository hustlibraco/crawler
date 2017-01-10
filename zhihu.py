#!/usr/bin/env python
#coding=utf-8

#########################
# @function 知乎发现 https://www.zhihu.com/explore
# @author   libraco
# @date     2017-01-11
# @version  0.1.0
#########################

import re
import time
import Queue
import requests
import threading
import traceback
import json
from urllib import quote
from bs4 import BeautifulSoup

class Zhihu(object):
    """
    知乎发现
    """
    def __init__(self):
        self.source = {
        'explore':'https://www.zhihu.com/node/ExploreAnswerListV2?params={0}'
        }

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


    def explore(self):
        param = {"offset":1,"type":"day"}
        r = requests.get(self.source['explore'].format(quote(json.dumps(param))),
            headers=self.headers)
        print r.text, r.url


if __name__ == '__main__':
    zh = Zhihu()
    zh.explore()
