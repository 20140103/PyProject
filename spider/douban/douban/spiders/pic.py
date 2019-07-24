# -*- coding: utf-8 -*-
import scrapy

from douban.items import Pic


class PicSpider(scrapy.Spider):
    name = 'pic'
    baseUrl = 'www.115je.com'
    allowed_domains = ['www.115je.com']
    start_urls = ['https://www.115je.com/pic/html28/']

    def parse(self, response):
        # print(response.body.decode())
        # movie_list = response.xpath("//div[@class='collapse navbar-collapse']/ul[@class='nav navbar-nav navbar-left']/li/a")#("//div[@class='collapse navbar-collapse']/ul/li")
        # print(movie_list)
        # title = response.xpath("//div[@class='box-title']/h3/text()").extract_first()
        # print(title)
        pic_list = response.xpath("//ul[@class='box-topic-list p-0 clearfix']/li/a")
        for i_item in pic_list:
            # print(i_item)

            # novel_item = XiaoshowNovel()

            # novel_item['title'] = i_item.xpath("@title").extract_first()
            # novel_item['url'] = i_item.xpath("@href").extract_first()

            # print(i_item.xpath("@title").extract_first())
            # print(i_item.xpath("@href").extract_first())
            # print(novel_item)
            # yield novel_item 
            url = i_item.xpath("@href").extract_first()
            # print(i_item.xpath("@title").extract_first())
            print("parse url:"+url)
            # print("\r\n")
            yield scrapy.Request("https://www.115je.com"+ url, callback=self.pic_des)

        next_link = response.xpath("//div[@class='box-page clearfix']//ul/li/a[text()='下一页']")
        
        if next_link:
            next_link = next_link.xpath("@href").extract_first()
            # print("https://www.122md.com"+next_link)
            yield scrapy.Request("https://www.115je.com"+next_link, callback=self.parse)
    

    # 抓取具体图片内容
    def pic_des(self, response):
        
        # print("novel_des")
        # print(response.body.decode())
        # print(response.xpath("//div[@class='details-content text-justify']/img/@src").extract_first())

        # pics = response.xpath("//div[@class='xs-details-content text-xs']//p/text()")
        # title = response.xpath("//h1[@class='text-overflow']/text()")
        # text = ""
        url = response.xpath("//div[@class='details-content text-justify']//img/@src").extract_first()
        pic_item = Pic()
        # # print(novel_text.extract_first())

        # pic_item['title'] = title.extract_first()
        pic_item['url'] = url
        # pic_item['text'] = text
        print("pic_des url:"+url)
        # print("title:"+title.extract_first())
        yield pic_item
