#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

phone = "2004-959-559 # This is Phone Number"

num = re.sub(r'#.*s',"",phone)

print "Phone Num :",num

# Remove anything other than digits
num = re.sub(r'\D', "", phone)
print "Phone Num : ", num

print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配
print(re.match('com', 'www.runoob.com'))         # 不在起始位置匹配

line = "Cats are smarter than dogs";

searchObj = re.search( r'(.*) are (.*?) .*', line, re.M|re.I)

if searchObj:
   print "searchObj.group() : ", searchObj.group()
   print "searchObj.group(1) : ", searchObj.group(1)
   print "searchObj.group(2) : ", searchObj.group(2)
   print "searchObj.group(1,2) : ", searchObj.group(0,2)
else:
   print "Nothing found!!"

url =  "https://www.baidu.com"

https = re.se