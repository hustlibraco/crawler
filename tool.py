#!/usr/bin/env python
#coding=utf-8

#########################
# @function 爬虫工具类
# @author   libraco
# @date     2016-04-25
# @version  0.1.0
#########################

import re

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