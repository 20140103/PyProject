# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanPipeline(object):
    def process_item(self, item, spider):
        if(spider.name == 'xiaoshuo'):
            # print("DoubanPipeline :"+item['title'])
            # print(item)
            # bookFile = open("/Users/twt/python/PyProject/spider/crawler/books/" + item['title'] + ".txt", "a+")
            bookFile = open("/home/python/pyProject/spider/twtspider/crawler/books/" + item['title'] + ".txt", "a+")
            bookFile.write(item['url']+'\n')
            bookFile.write(item['text'])
            bookFile.close()
        elif(spider.name == 'pic'):
            bookFile = open("/Users/twt/python/PyProject/spider/crawler/books/piclist.txt", "a+")
            bookFile.write(item['url']+'\n')
            bookFile.close()
        return item
