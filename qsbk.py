#!/usr/bin/env python
#coding=utf-8

#########################
# @function 糗事百科段子爬虫
# @author   libraco
# @date     2016-04-22
# @version  0.1.0
# @update   面向对象化设计+线程事件同步
#########################

import re
import time
import Queue
import requests
import threading
import traceback
from bs4 import BeautifulSoup

class QSBK(object):
    """
    糗百爬虫类
    1.爬取糗百的文本段子
    2.根据用户行为平滑地显示段子
    """
    def __init__(self):
        self.urlfmt = 'http://www.qiushibaike.com/hot/page/{page}'
        self.jokefmt = u'[序号]\t{no}\n[作者]\t{author}|{sex}|{age}\n[内容]\t{content}\n[好笑]\t{votes}\n[评论]\t{comments}\n'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
        self.jokes = Queue.Queue(200)       # 存放段子
        self.page = 1                       # 爬取的页码
        self.no = 0                         # 爬取段子数
        self.evt = threading.Event()        # 爬取页面同步锁

    def loadPage(self):
        # 加载一页糗百段子
        url = self.urlfmt.format(page=self.page)
        try:
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, 'lxml')
            jokes = soup.find_all('div',
                class_='article block untagged mb15',
                id=re.compile(r'qiushi_tag_(\d)+'))
            for joke in jokes:
                try:
                    if joke.find('div', class_='thumb'):
                        # 过滤图片段子
                        continue
                    self.no += 1
                    one = {}
                    author_tag = joke.find('div', class_='author clearfix')
                    one['author'] = author_tag.select('a')[1].select('h2')[0].string;
                    sex_age_tag = author_tag.select('div')[0]
                    if 'manIcon' in sex_age_tag['class']:
                        one['sex'] = u'男'
                    elif 'womenIcon' in sex_age_tag['class']:
                        one['sex'] = u'女'
                    else:
                        one['sex'] = u'不男不女'
                    one['age'] = sex_age_tag.string
                    one['content'] = joke.find('div', class_='content').text.strip()
                    one['votes'] = joke.find('span', class_='stats-vote').i.string.strip()
                    try:
                        one['comments'] = joke.find('span', class_='stats-comments').a.i.string.strip()
                    except:
                        one['comments'] = 0
                    one['no'] = self.no
                    self.jokes.put(one)
                except:
                    traceback.print_exc()
                    break
            self.page += 1
        except:
            traceback.print_exc()
            return False

    def loadPager(self):
        # 加载段子
        while 1:
            self.loadPage()
            self.evt.clear()
            self.evt.wait()

    def getJoke(self):
        # 获取段子
        while 1:
            try:
                if self.jokes.qsize() < 5:
                    self.evt.set()
                joke = self.jokes.get(timeout=1)
                self.showJoke(joke)
                self.jokes.task_done()
                time.sleep(1)
            except KeyboardInterrupt:
                break
            except:
                traceback.print_exc()

    def showJoke(self, joke):
        # 显示段子
        print self.jokefmt.format(**joke)
    
    def start(self):
        # 启动爬虫
        print u'开始爬取段子……\n'
        t = threading.Thread(target=self.loadPager, args=())
        t.setDaemon(True)
        t.start()
        self.getJoke()

if __name__ == '__main__':
    qsbk = QSBK()
    qsbk.start()
