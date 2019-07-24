# -*- coding: utf-8 -*-
import scrapy
from douban.items import XiaoshowNovel

class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuo'
    allowed_domains = ['www.122md.com'] #https://www.122md.com/novel/list2/
    start_urls = ['https://www.122md.com/novel/list2/'
    ,'https://www.122md.com/novel/list3/'
    ,'https://www.122md.com/novel/list4/'
    ,'https://www.122md.com/novel/list5/']

    def parse(self, response):
        # print(response.body.decode())
        # movie_list = response.xpath("//div[@class='collapse navbar-collapse']/ul[@class='nav navbar-nav navbar-left']/li/a")#("//div[@class='collapse navbar-collapse']/ul/li")
        # print(movie_list)
        title = response.xpath("//div[@class='box-title']/h3/text()").extract_first()
        # print(title)
        novel_list = response.xpath("//ul[@class='box-topic-list p-0 clearfix']/li/a")
        for i_item in novel_list:
            # print(i_item)

            novel_item = XiaoshowNovel()
            novel_item['title'] = i_item.xpath("@title").extract_first()
            novel_item['url'] = i_item.xpath("@href").extract_first()
            # print(i_item.xpath("@title").extract_first())
            # print(i_item.xpath("@href").extract_first())
            # print(novel_item)
            # yield novel_item
            yield scrapy.Request("https://www.122md.com"+novel_item['url'], callback=self.novel_des)

        next_link = response.xpath("//div[@class='box-page clearfix']//ul/li/a[text()='下一页']")
        
        if next_link:
            next_link = next_link.xpath("@href").extract_first()
            # print("https://www.122md.com"+next_link)
            yield scrapy.Request("https://www.122md.com"+next_link, callback=self.parse)
    

    # 抓取具体小说内容
    def novel_des(self, response):
        
        # print("novel_des")
        # print(response.body.decode())

        novel_texts = response.xpath("//div[@class='xs-details-content text-xs']//p/text()")
        title = response.xpath("//h1[@class='text-overflow']/text()")
        text = ""
        # print(novel_texts)
        for p in novel_texts:
            text += p.extract() + '\n'
            # print(text)
        # print(text)
        novel_item = XiaoshowNovel()
        # print(novel_text.extract_first())

        novel_item['title'] = title.extract_first()
        novel_item['url'] = response.url
        novel_item['text'] = text
        # print(novel_item)
        # print("title:"+title.extract_first())
        yield novel_item
