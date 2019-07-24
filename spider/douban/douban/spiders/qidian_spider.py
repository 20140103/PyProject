# -*- coding: utf-8 -*-
import scrapy
from douban.items import QidianBookItem


class QidianSpiderSpider(scrapy.Spider):
    startIndex = 0  # 默认第0本
    startPage = 0  # 默认第0页
    # 爬虫的名称
    name = 'qidian_spider'
    # 爬虫允许抓取的域名
    allowed_domains = ['www.qidian.com']
    # 爬虫抓取数据地址,给调度器
    start_urls = [
        "https://www.qidian.com/free/all?orderId=&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=1&page="+str(startPage+1)]

    def parse(self, response):
        # bookArr = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        bookArr = response.xpath("//ul[@class='all-img-list cf']/li")

        # global startIndex
        # if startIndex > 0:
        #     bookArr = bookArr[startIndex:]
        #     startIndex = 0
        for book in bookArr:
            qidian_item = QidianBookItem()
            qidian_item['book_name'] = book.xpath(
                ".//div[@class='book-mid-info']/h4/a/text()")
            qidian_item['describle'] = book.xpath(
                ".//div[@class='book-mid-info']/p[2]/text()")
            # //ul[@class='all-img-list cf']/li//div[@class='book-mid-info']/p[3]/span/span/text()
            qidian_item['textLength'] = book.xpath(
                ".//div[@class='book-mid-info']/p[3]/span/span/text()")
            qidian_item['url'] = book.xpath(
                ".//div[@class='book-mid-info']/h4/a/@href")
            # print (qidian_item)
            yield qidian_item
            # 先创建.txt文件，然后获取文本内容写入
            # bookFile = open("crawler/books/" + bookCover.string + ".txt", "a+")
            # # print "file path:"+bookFile.path
            # bRes = urllib2.urlopen("https:" + bookCover['href'])
            # bSoup = BeautifulSoup(bRes.read(), "html.parser")
            # bookContentHref = bSoup.select("a[class='red-btn J-getJumpUrl ']")[0]["href"]
            # getChapterContent(bookFile, "https:" + bookContentHref)
            # bookFile.close()
        # nextPage = soup.select("a.lbf-pagination-next")[0]
        # return nextPage["href"]
        # print(bookArr)
