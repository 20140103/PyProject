#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import threading
import time
import requests
import json
import math

from jiexi import ExcelUtil

exitFlag = 0

vekey = 'V00002371Y65180478'
pid = 'mm_98723245_44422162_465706573'
baseUrl = 'http://api.vephp.com/super?vekey=%s&pid=%s'
# 1、page 参数：传递当前页码值。默认1.
# 2、pagesize 参数：传递每页最大显示数，默认15，最大值不要超过30.
# 3、coupon 参数：当不传递coupon参数或coupon=0时，默认搜索包含无券产品，当传coupon=1时则搜索有券产品。

# 4、start_price 和 end_price 参数：start_price 指折扣价范围下限，end_price 指折扣价范围上限，单位：元
# 5、start_tk_rate 和 end_tk_rate 参数：end_tk_rate，淘客佣金比率上限，如：1234表示12.34%，start_tk_rate淘客佣金比率下限
# 6、is_overseas 参数：是否海外商品，is_overseas=1 指定为海外产品。默认为否。
# 7、is_tmall 参数：是否商城商品，默认0（可选0或1），设为1表示商品是天猫商城商品，不设置或0表示不限制。
# 8、cat 参数： 淘宝分类类目ID，用,分割，最大10个，该ID可以通过taobao.itemcats.get接口获取到。当传递了cat参数时，可以不必使用para参数，比如：
#        http://apis.vephp.com/super?vekey=xxxxx&cat=50011129

# 9、sort 参数：排序，默认 total_sales_des（销量降序），可选值如下：
#         tk_rate_des（淘客佣金比率降序）,
#         tk_rate_asc（淘客佣金比率升序）,
#         total_sales_des（销量降序）,
#         total_sales_asc（销量升序）,
#         tk_total_sales_des（累计推广量降序）,
#         tk_total_sales_asc（累计推广量升序）,
#         tk_total_commi_des（总支出佣金降序）,
#         tk_total_commi_asc（总支出佣金升序）,
#         price_des（价格降序）,
#         price_asc（价格升序）;

# 10、onlysearch 参数（强制仅使用搜索）：可选，当指定 onlysearch=1 时，如果para参数是“淘口令、产品ID、二合一等各种淘宝链接”时，本接口默认是会直接把参数转入高佣API，得到该参数对应的产品推广详情和淘口令。但是指定“onlysearch=1”后，接口会把para参数中淘口令等解析后取得它对应的产品标题，并且它的标题去搜索，而不会进行高佣转链。
# 11、similar 参数：可选值0和1（默认值0），是指自动使用找相似功能。默认是不找相似。当搜索中指定该参数为1时，则自动在发现非联盟产品时使用找相似功能。这时，返回值中字段 is_similar 表示是否为相似搜索，is_similar值为1表示近似产品搜索。
# 12、searchid 参数：可选值0和1（默认值0），是指搜索产品ID，此时参数para必须是淘宝产品ID，使用本参数时，onlysearch和similar同时失效。这时返回的是该ID的产品搜索结果，而非定向转链接口。

# 13、ip 参数： 当需要限制包邮时，最好传递顾客的IP参数，比如：  ip=122.71.37.32 ，本参数最好和freeship一起使用。
# 14、freeship参数：是否只查包邮产品，默认值不限。如果只想要包邮产品，可以传递freeship=1
# 15、npx 参数： 默认不设置。此参数指定牛皮癣程度，此参数影响主图美观度，可用取值范围：1-不限，2-无，3-轻微

defaultQueryKeys = {'page': 0, 'pagesize': 30}


class myThread(threading.Thread):  # 继承父类threading.Thread
    # url = 'http://tooker.work:8080/webapi/classifications/'
    # url = 'http://api.vephp.com/super?vekey=%s&pid=%s&para=%s' % (vekey, pid,
    #                                                               para)
    url = baseUrl % (vekey, pid)

    headers = {'content-type': "application/json"}

    def __init__(self, keyWorks, queryKeys, app):
        threading.Thread.__init__(self)
        # self.threadID = threadID
        # self.name = name
        self.keyWorks = keyWorks  # 查询关键字
        self.queryKeys = queryKeys  # 查询参数
        self.queryKeys['pagesize'] = 30
        self.app = app
        self.Flag = True
        self.totalProducts = 0
        # print(app.var_config_sava_dir.get())
        self.excelUtil = ExcelUtil(app.var_config_sava_dir.get(),
                                   app.var_task_name.get())
        # self.state = threading.Condition()

        # self.excelUtil.readExcel('testJson.json')
        # self.excelUtil.writeM(self.excelUtil.readExcel('testJson.json'))

        # self.excelUtil.saveExcel()
        # self.url = #baseUrl % (vekey, pid)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数

        # print_time(self.name, self.counter, 5)
        # print(dict(self.queryKeys))
        self.app.showLogInfo('任务开始')
        self.app.showLogInfo('本次任务关键字共%d条' % len(self.keyWorks))
        self.app.showLogInfo(
            '本次任务查询参数 券后价:%d~%d  月销量：%d  佣金:%d~%d  天猫:%s  包邮:%s  优惠券:%s' %
            (self.queryKeys['start_price'], self.queryKeys['end_price'],
             self.queryKeys['volume'], self.queryKeys['start_tk_rate'],
             self.queryKeys['end_tk_rate'], self.isTmall(), self.isFreeship(),
             self.isCoupon()))

        # self.getProduce(self.url, self.keyWorks[0], 0)
        for keyWork in self.keyWorks:
            # for keyWork in range(2):
            if not self.Flag:
                break
            self.app.showLogInfo("开始搜索 %s 关键字" % keyWork)
            response = self.getProduce(self.url, keyWork, 0)
            # print(dict(response))
            error = int(response['error'])
            msg = response['msg']
            # print(error == 0)
            if error == 0:

                total_results = int(response['total_results'])
                result_list = response['result_list']
                self.totalProducts += total_results
                self.app.showLogInfo('%s 关键字查询成功 共%s条' %
                                     (keyWork, total_results))
                if (len(result_list) < total_results):
                    # print('page:%d 保存到excel' % 1)
                    self.filteProduct(result_list)
                    # 要分页下载
                    totalPage = math.ceil(total_results / len(result_list))
                    # print(totalPage)
                    for page in range(2, totalPage + 1):
                        tempResponse = self.getProduce(self.url,
                                                       keyWork, page)
                        error = int(tempResponse['error'])
                        result_list = tempResponse['result_list']
                        msg = tempResponse['msg']
                        if error == 0:
                            self.filteProduct(result_list)
                            # print('page:%d 保存到excel' % page)
                        else:
                            self.app.showLogInfo('%s 关键字查询失败 %s 第:%d页' %
                                                 (keyWork, msg, page))
                else:
                    # 直接处理了
                    # print('保存到excel')
                    self.filteProduct(result_list)
                    pass
            else:
                self.app.showLogInfo('%s 关键字查询失败 %s' % (keyWork, msg))

            # self.excelUtil.writeM(self.excelUtil.readExcel('testJson.json'))

            # self.app.showLogInfo("线程状态%s" % self.state)
            # time.sleep(2)
        self.excelUtil.saveExcel()
        self.app.showLogInfo('共保存%s条商品' %
                             (self.excelUtil.readExcelNrows() - 1))

        self.app.showLogInfo('数据保存在 %s' % self.excelUtil.path)
        self.app.showLogInfo('任务结束')
        self.app.tastStart = False
        self.Flag = False
        # print(keyWork)
        # self.getProduce(self.url,0,keyWork)

    def filteProduct(self, products):
        # print("filteProduct:11")
        # print(len(products))
        # print("filteProduct:22")
        # print(len(list(filter(self.func, products))))
        self.excelUtil.writeM(filter(self.func, products))
        # return filter(self.func, products)

    def func(self, product):
        # print(product)
        return int(product['volume']) > int(self.queryKeys['volume'])

    def isTmall(self):
        if self.queryKeys['is_tmall'] == 1:
            return '是'
        else:
            return '否'

    def isFreeship(self):
        if self.queryKeys['freeship'] == 1:
            return '是'
        else:
            return '否'

    def isCoupon(self):
        if self.queryKeys['coupon'] == 1:
            return '是'
        else:
            return '否'

    def isStarting(self):
        return self.Flag

    def stop(self):  # 外部停止线程的操作函数
        self.Flag = False  # boolean

    def getProduce(self, url, keyWork, page=0):
        self.queryKeys["para"] = keyWork
        self.queryKeys['page'] = page
        response = requests.get(url,
                                headers=myThread.headers,
                                params=self.queryKeys)

        # print((response.url))
        # print("%s:%s %s" % (response.text, url, keyWork))
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            jsonStr = '{"error": "1","msg": "", "search_type": "1", "is_similar": "0", "total_results": 50,  "result_list": []}'
            return json.loads(jsonStr)
        # return self.excelUtil.readExcel('testJson.json')



# http://api.vephp.com/super?vekey=V00002371Y65180478&pid=mm_98723245_44422162_465706573&coupon=0&volume=50000&is_tmall=0&freeship=0&pagesize=30&para=%E5%8F%A3%E7%BA%A2&page=0&start_tk_rate=0&end_tk_rate=5000&start_price=0&end_price=100000

# http://api.vephp.com/super?vekey=V00002371Y65180478&pid=mm_98723245_44422162_465706573&coupon=0&volume=50000&is_tmall=0&freeship=0&pagesize=30&para=%E5%8F%A3%E7%BA%A2&page=0&start_tk_rate=0&end_tk_rate=5000&start_price=10.0&end_price=100000.0