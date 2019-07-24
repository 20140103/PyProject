# -*- coding: utf-8 -*-
import scrapy
import re


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    # allowed_domains = ['quote.eastmoney.com']

    # ['http://quote.eastmoney.com/stocklist.html']
    start_urls = ['http://quote.eastmoney.com/center/gridlist.html#hs_a_board']

    def parse(self, response):
        # print("这里获取到html内容")
        print(response.body.decode())
        # print(response.css('a::attr(href)').extract())
        # for href in response.css('a::attr(href)').extract():
        #     try:
        #         stock = re.findall(r"[s][hz]\d(6)", href)[0]
        #         url = 'https://gupiao.baidu.com/stock/' + stock + '.html'
        #         print("test:url"+href)
        #     except:
        #         continue
        #     print("href:"+href)
        #     pass