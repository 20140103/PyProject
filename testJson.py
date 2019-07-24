#!/usr/bin/python
import json
import urllib2

#data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]

#json = json.dumps(data)
#print json
html = urllib2.urlopen(r'https://api.altama.pw/api/v1/Profile/GetRegionList')
hjson = json.loads(html.read())

#print hjson
regionList = hjson['data']
#provinceBeanArrayList
#districtBeanArrayList
#cityBeanArrayList

for region1 in regionList:
    provinceBean = { 'id': '','name':"" }
    if region1['layer']==1:
        provinceBean['id']=region1['regionid']
        provinceBean['name']=region1['name']
        #print provinceBean
    