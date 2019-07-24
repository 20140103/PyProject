#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# 打开一个文件
fo = open("resources/language.txt","a+")
print "文件名: ", fo.name
print "是否已关闭 : ", fo.closed
print "访问模式 : ", fo.mode
print "末尾是否强制加空格 : ", fo.softspace

fo.write("\"ok\" = \"确认\"")
str = fo.read()
print str
fo.write("\ntest file write")
fo.flush()
str = fo.read()
print str
fo.close()

rootDir = 'C:\\zabbix\\'
def Test1(rootDir):
    for root,dirs,files in os.walk(rootDir):
        print "root",root
        for filespath in files:
            print os.path.join(root,filespath)

def Test2(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        print path
        if os.path.isdir(path):
            Test2(path)

Test1(".")
print "\n"
#Test2(".")