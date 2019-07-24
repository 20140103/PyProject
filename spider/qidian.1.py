# coding=utf-8
import urllib2
import sys
from bs4 import BeautifulSoup

# 设置编码
reload(sys)
sys.setdefaultencoding('utf-8')
# sys.setdefaultencoding('gb2312')
startIndex = 0  # 默认第0本
startPage = 0  # 默认第0页

# 获取一个章节的内容


def getChapterContent(file, url):
    try:
        bookContentRes = urllib2.urlopen(url)
        bookContentSoup = BeautifulSoup(bookContentRes.read(), "html.parser")
        file.write(bookContentSoup.select(
            "h3[class='j_chapterName']")[0].string + '\n')
        for p in bookContentSoup.select(".j_readContent p"):
            file.write(p.next + '\n')
    except BaseException:
        # 如果出错了，就重新运行一遍
        print(BaseException.message)
        getChapterContent(file, url)
    else:
        chapterNext = bookContentSoup.select("a#j_chapterNext")[0]
        if chapterNext.string != "书末页":
            nextUrl = "https:" + chapterNext["href"]
            getChapterContent(file, nextUrl)
# 获取一个章节的内容


def getChapterContent2(file, url):
    try:
        headers = {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        req = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(req)
        html = response.read().decode("gbk")
        # print(html.decode("gbk"))
        # headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        # req = urllib2.Request(url,headers=headers)
        # print(url)
        # bookContentRes = urllib2.urlopen(req)

        # print bookContentRes
        # print bookContentRes.read().edecode("gbk")
        html = html.replace('<td id="text"></div>', '<td id="text">')
        bookContentSoup = BeautifulSoup(html, "html.parser")

        # bookContentSoup2 = BeautifulSoup(bookContentRes,fromEncoding="gb2312")
        # print(bookContentSoup)
        print bookContentSoup.select('#text div')
        for p in bookContentSoup.select('#text div'):
            # print(p.next)
            file.write(p.next + '\n')
    except BaseException:
        # 如果出错了，就重新运行一遍
        print(BaseException.message)
        # getChapterContent2(file, url)
    else:
        print('dasfsa')
        # chapterNext = bookContentSoup.select("a#j_chapterNext")[0]
        # if chapterNext.string != "书末页":
        #     nextUrl = "https:" + chapterNext["href"]
        #     getChapterContent2(file,nextUrl)
# 获取当前页所有书的内容


def getCurrentUrlBooks(url):
    response = urllib2.urlopen(url)
    the_page = response.read()
    soup = BeautifulSoup(the_page, "html.parser")
    bookArr = soup.select("ul[class='all-img-list cf'] > li")
    global startIndex
    if startIndex > 0:
        bookArr = bookArr[startIndex:]
        startIndex = 0
    for book in bookArr:
        bookCover = book.select("div[class='book-mid-info'] h4 > a")[0]
        print "书名：" + bookCover.string
        # 先创建.txt文件，然后获取文本内容写入
        bookFile = open("crawler/books/" + bookCover.string + ".txt", "a+")
        # print "file path:"+bookFile.path
        bRes = urllib2.urlopen("https:" + bookCover['href'])
        bSoup = BeautifulSoup(bRes.read(), "html.parser")
        bookContentHref = bSoup.select(
            "a[class='red-btn J-getJumpUrl ']")[0]["href"]
        getChapterContent(bookFile, "https:" + bookContentHref)
        bookFile.close()
    nextPage = soup.select("a.lbf-pagination-next")[0]
    return nextPage["href"]


if len(sys.argv) == 1:
    pass
elif len(sys.argv) == 2:
    startPage = int(sys.argv[1])/20  # 从第几页开始下载
    startIndex = int(sys.argv[1]) % 20  # 从第几本开始下载
elif len(sys.argv) > 2:
    startPage = int(sys.argv[1])
    startIndex = int(sys.argv[2])

# 根据传入参数设置从哪里开始下载
# "//www.qidian.com/free/all?orderId=&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=1&page="+str(startPage+1)
url = "https://www.fushuwang.com/2018/71047.html"

# 死循环 直到没有下一页
# while True:
#     if url.startswith("//"):
#         print(url)
#         url = getCurrentUrlBooks("https:" + url)
#     else:
#         break;


bookFile = open("crawler/books/test.txt", "a+")
# url = "https://www.fushuwang.com/2018/71047_"+str(1)+".html"
# getChapterContent2(bookFile,url)
for num in range(1, 47):
    if num == 1:
        url = "https://www.fushuwang.com/2018/71047.html"
    else:
        url = "https://www.fushuwang.com/2018/71047_"+str(num)+".html"

    print url
    getChapterContent2(bookFile, url)
# url= "https://www.fushuwang.com/2018/71047_2.html?2"#"http://www.qq.com/"

# headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
# req = urllib2.Request(url,headers=headers)
# response= urllib2.urlopen(req)
# html = response.read().decode("gbk")
# html = html.replace('<td id="text"></div>','<td id="text">')
# bookFile.write(html)
# print html.decode("gbk")
