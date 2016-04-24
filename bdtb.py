#!/usr/bin/env python
#coding=utf-8

#########################
# @function 百度贴吧爬虫
# @author   libraco
# @date     2016-04-24
# @version  0.1.0
#########################

import re
import requests
import traceback
import time

class Tool:
    '''处理页面标签类'''
    removeImg = re.compile('<img.*?>| {7}|')
    #去除img标签,7位长空格
    removeAddr = re.compile('<a.*?>|</a>')
    #删除超链接标签
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #把换行的标签换为\n
    replaceTD= re.compile('<td>')
    #将表格制表<td>替换为\t
    replacePara = re.compile('<p.*?>')
    #把段落开头换为\n加空两格
    replaceBR = re.compile('<br><br>|<br>')
    #将换行符或双换行符替换为\n
    removeExtraTag = re.compile('<.*?>')
    #将其余标签剔除
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        return x.strip()

class BDTB(object):
    """百度贴吧帖子爬虫"""
    def __init__(self, base_url, see_lz):
        super(BDTB, self).__init__()
        self.base_url = base_url
        self.see_lz = see_lz
        self.defaultTitle = u"百度贴吧"
        self.file = None    # 存储文件句柄
        self.tool = Tool()
        self.floor = 1

    def getPage(self, pageno):
        '''爬取指定页面'''
        try:
            data = {'pn': pageno, 'see_lz': self.see_lz}
            r = requests.get(self.base_url, data)
            return r.text
        except Exception, e:
            traceback.print_exc()

    def getTitle(self):
        '''爬取标题'''
        try:
            pattern = re.compile(r'<h3 class=".*?core_title_txt.*?">(.*)</h3>')
            homepage = self.getPage(1)
            result = re.search(pattern, homepage)
            if result:
                return result.group(1).strip()
        except Exception, e:
            traceback.print_exc()

    def setFileTitle(self,title=None):
        '''如果标题不是为None，即成功获取到标题'''
        if title is None:
            title = self.defaultTitle
        self.file = open('{title}_{seelz}_{timestamp}.txt'.format(
            title=title.encode('utf-8'), 
            seelz=self.see_lz,
            timestamp=int(time.time())),"w")

    def _getNum(self):
        pattern = re.compile(r'<li class="l_reply_num".*?<span class="red".*>(\d+)</span>.*<span class="red">(\d+)</span>.*</li>')
        homepage = self.getPage(1)
        result = re.search(pattern, homepage)
        if result:
            return result.groups()

    def getPageNum(self):
        '''爬取总页数'''
        try:
            return self._getNum()[1]
        except Exception, e:
            traceback.print_exc()
            return 1

    def getPostNum(self):
        '''爬取帖子数'''
        try:
            return self._getNum()[0]
        except Exception, e:
            traceback.print_exc()
            return 1

    def getContent(self, page):
        '''爬取指定页面的帖子内容'''
        try:
            pattern = re.compile(r'<div id="post_content_\d+".*?>(.*?)</div>', re.S)
            result = re.findall(pattern, page)
            row = u'{floor}楼-----------------------------\n{item}\n\n'
            content = []
            for item in result:
                item = self.tool.replace(item)
                content.append(row.format(floor=self.floor, item=item).encode('utf-8'))
                self.floor += 1
            return content
        except Exception, e:
            traceback.print_exc()
            return {}

    def writeData(self, content):
        '''存储帖子内容'''
        try:
            if not self.file:
                title = self.getTitle()
                self.setFileTitle(title)
            self.file.writelines(content)
        except Exception, e:
            traceback.print_exc()

    def start(self):
        '''开始程序'''
        try:
            pagenum = int(self.getPageNum())
            print '一共{0}页'.format(pagenum)
            for i in range(1, pagenum+1):
                print '爬取第{0}页。。。'.format(i)
                page = self.getPage(i)
                content = self.getContent(page)
                self.writeData(content)
            self.file.close()
        except Exception, e:
            traceback.print_exc()


if __name__ == '__main__':
    try:
        print u"请输入帖子代号"
        baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
        seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
        bdtb = BDTB(baseURL,seeLZ)
        bdtb.start()
    except:
        traceback.print_exc()
