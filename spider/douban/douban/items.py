# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 序号
    serial_number = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 介绍
    introduce = scrapy.Field()
    # 星级
    star = scrapy.Field()
    # 评价
    evaluate = scrapy.Field()
    # 描述
    describle = scrapy.Field()


class QidianBookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 书名称
    book_name = scrapy.Field()
    # 介绍
    introduce = scrapy.Field()
    # 星级
    star = scrapy.Field()
    # 评价
    evaluate = scrapy.Field()
    # 描述
    describle = scrapy.Field()
    # 字数
    textLength = scrapy.Field()
    #
    url = scrapy.Field()


class XiaoshowNovel(scrapy.Item):
    # 书名称
    title = scrapy.Field()
    #
    url = scrapy.Field()

    # 正文
    text = scrapy.Field()


class Pic(scrapy.Item):
    # 书名称
    title = scrapy.Field()
    #
    url = scrapy.Field()

    # 正文
    text = scrapy.Field()