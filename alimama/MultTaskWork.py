#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import math
import queue
import threading
import time
from concurrent.futures import (ThreadPoolExecutor, as_completed)
import multiprocessing as mp
import requests

from jiexi import ExcelUtil

exitFlag = 0

default_max_workers = 25

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

headers = {'content-type': "application/json"}


class MultTaskWork():  # 继承父类threading.Thread
    # url = 'http://tooker.work:8080/webapi/classifications/'
    # url = 'http://api.vephp.com/super?vekey=%s&pid=%s&para=%s' % (vekey, pid,
    #                                                               para)
    url = baseUrl % (vekey, pid)

    def __init__(self, keyWorks, queryKeys, app):
        self.keyWorks = keyWorks  # 查询关键字
        self.queryKeys = queryKeys  # 查询参数
        self.queryKeys['pagesize'] = 30
        self.app = app
        self.Flag = True
        self.totalProducts = 0
        self.stopTaskFlag = False
        self.keyWorkDoneCount = 0
        self.keyWorkCount = len(self.keyWorks)

        self.excelUtil = ExcelUtil(app.var_config_sava_dir.get(),
                                   app.var_task_name.get())
        self.douwnload_count = 0
        self.q = queue.Queue(1000)
        self.mutex = threading.Lock()
        # print(app.var_config_sava_dir.get())
        self.p1 = threading.Thread(target=self.testTask)
        self.p1.setDaemon(True)
        self.p1.start()

        self.c = threading.Thread(target=self.consumer, args=('c', ))
        self.c2 = threading.Thread(target=self.consumer, args=('c2', ))
        # self.c.setDaemon(True)
        self.c.start()
        self.c2.start()
        # self.p2 = mp.Process(target=self.consumerP, args=(self.q,))
        # self.p2.start()

    # 消费者
    def consumer(self, tag):
        while self.Flag:
            # print(list(self.q.get()))

            # print("consumer %s 1 qsize:%d row=%d" % (tag, self.q.qsize(), self.excelUtil.readExcelNrows()))
            try:
                items = self.q.get(timeout=10)
                self.excelUtil.writeM(items)
                # if self.q.qsize() > 800:
                #     self.excelUtil.saveExcel()
            except BaseException:
                # print('超时')
                return
                pass
            # print("consumer %s 2 qsize:%d" % (tag, self.q.qsize()))

            # print('[%s]取到了[%s]包子并且吃了它' %
            #       (name,   list(self.q.get())))  # get_nowait()不会阻塞等待
            # time.sleep(random.random() * 5)
        # print('consumer 完成')

    def testTask(self):
        # print('test %s' % self.queryKeys)

        time.perf_counter()

        # 创建线程池
        # self.keyWordThreadPool = ThreadPoolExecutor(max_workers=default_max_workers)
        # # 创建线程池
        self.executor = ThreadPoolExecutor(max_workers=default_max_workers)
        # self.executor.submit(self.testTask, (self.keyWorks[0]))
        self.Flag = True
        self.app.showLogInfo('任务开始')
        self.app.showLogInfo('本次任务关键字共%d条' % len(self.keyWorks))
        self.app.showLogInfo(
            '本次任务查询参数 券后价:%d~%d  月销量：%d  佣金:%d~%d  天猫:%s  包邮:%s  优惠券:%s' %
            (self.queryKeys['start_price'], self.queryKeys['end_price'],
             self.queryKeys['volume'], self.queryKeys['start_tk_rate'],
             self.queryKeys['end_tk_rate'], self.isTmall(), self.isFreeship(),
             self.isCoupon()))
        self.all_task = []
        for keyWork in self.keyWorks:
            # print(keyWork)
            self.all_task.append(self.executor.submit(self.doTask, (keyWork)))
        # wait(self.all_task, return_when=FIRST_COMPLETED)
        for future in as_completed(self.all_task):
            try:
                data = future.result()
                self.app.showLogInfo(f"{data} 关键字完成 ")
            except BaseException:
                # print("")
                pass
        t = time.perf_counter()
        self.app.showLogInfo('任务结束中 请稍后...1')
        self.c.join()
        self.c2.join()

        self.app.showLogInfo('任务结束中 请稍后...2')
        # self.p2.join()
        self.excelUtil.saveExcel()

        self.app.showLogInfo('任务结束中 请稍后...3')
        self.app.showLogInfo('共保存%s条商品' %
                             (self.excelUtil.readExcelNrows() - 1))
        self.app.showLogInfo('数据保存在 %s' % self.excelUtil.path)
        # t = time.perf_counter()
        self.app.showLogInfo(
            '共请求%d次 频率  %d次/分钟' %
            (self.douwnload_count, int(self.douwnload_count / (t / 60))))
        self.app.showLogInfo('任务结束 用时%d秒' % t)
        # self.p1.stop()
        # self.c.stop()
        self.app.tastStart = False
        self.Flag = False

    def doKeyWordTask(self, keyWork, page):

        self.app.showLogInfo('%s 关键字查询 第:%d页' % (keyWork, page))
        # self.app.showLogInfo("开始搜索 %s 关键字 " % keyWork)
        response = self.getProduce(self.url, keyWork, page)
        total_items = 0
        # print(dict(response))
        error = int(response['error'])
        msg = response['msg']
        # print(error == 0)
        if error == 0:
            # total_results = int(response['total_results'])
            result_list = response['result_list']
            # self.totalProducts += total_results
            # 直接处理了
            # print('保存到excel')
            total_items = self.filteProduct(result_list)
            # self.app.showLogInfo('%s 关键字查询成功 共%s条' % (keyWork, total_items))
        else:
            self.app.showLogInfo('%s 关键字查询失败 %s 第:%d页' % (keyWork, msg, page))
        return total_items

    def doTask(self, keyWork):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.app.showLogInfo("开始搜索 %s 关键字" % keyWork)
        response = self.getProduce(self.url, keyWork, 0)
        total_items = 0
        # print(dict(response))
        error = int(response['error'])
        msg = response['msg']
        # print(error == 0)
        if error == 0:
            total_results = int(response['total_results'])
            result_list = response['result_list']
            self.totalProducts += total_results

            if (len(result_list) < total_results):
                # print('page:%d 保存到excel' % 1)
                total_items += self.filteProduct(result_list)
                # 要分页下载
                totalPage = math.ceil(total_results / len(result_list))
                if totalPage > 1000:
                    volume = self.getPageVolume(keyWork, 1000)
                    print(volume)
                    if (volume >= self.queryKeys['volume']):
                        totalPage = 1000
                    else:
                        totalPage = self.binary_chop(keyWork, 1, 1000,
                                                     self.queryKeys['volume'])
                else:
                    totalPage = self.binary_chop(keyWork, 1, 1000,
                                                 self.queryKeys['volume'])

                print(totalPage)
                # return
                # 创建线程池
                self.keyWordThreadPool = ThreadPoolExecutor(
                    max_workers=default_max_workers)
                self.temp_all_task = []
                # wait(self.all_task, return_when=FIRST_COMPLETED)
                for page in range(2, totalPage + 1):
                    temp_all_task.append(
                        self.keyWordThreadPool.submit(self.doKeyWordTask,
                                                      keyWork, page))
                    self.app.showLogInfo('%s 关键字查询 第:%d页' % (keyWork, page))
                    tempResponse = self.getProduce(self.url, keyWork, page)
                    error = int(tempResponse['error'])
                    result_list = tempResponse['result_list']
                    msg = tempResponse['msg']
                    if self.stopTaskFlag:
                        break
                    if error == 0:
                        total_items += self.filteProduct(result_list)
                        volume = result_list[-1]['volume']
                        if (volume < self.queryKeys['volume']):
                            break
                        # print('page:%d 保存到excel' % page)
                    else:
                        self.app.showLogInfo('%s 关键字查询失败 %s 第:%d页' %
                                             (keyWork, msg, page))
                for future in as_completed(temp_all_task):
                    try:
                        data = future.result()
                        total_items += data
                        # self.app.showLogInfo(f"{data} 关键字完成 ")
                    except BaseException:
                        # print("")
                        pass
                self.app.showLogInfo('分页查询结束')
            else:
                # 直接处理了
                # print('保存到excel')
                total_items += self.filteProduct(result_list)
            self.app.showLogInfo('%s 关键字查询成功 共%s条' % (keyWork, total_items))
        else:
            self.app.showLogInfo('%s 关键字查询失败 %d %s' % (keyWork, error, msg))

        if self.mutex.acquire(1):
            self.keyWorkDoneCount += 1
            self.mutex.release()
        self.app.showLogInfo('任务进度 共 %d关键字 完成%d关键字 剩余%d关键字' %
                             (self.keyWorkCount, self.keyWorkDoneCount,
                              (self.keyWorkCount - self.keyWorkDoneCount)))
        # self.excelUtil.saveExcel()
        return keyWork

    def binary_chop(self, keyWork, first, last, data):
        """
        非递归解决二分查找
        :param alist:
        :return:
        """
        page = 0
        for page in range(first, last, 50):
            value = self.getPageVolume(keyWork, page)
            print('page %d volume %d' % (page, value))
            if value < data:
                break
        return page

    def getPageVolume(self, keyWork, page):
        tryCount = 0
        while tryCount < 3:
            tempResponse = self.getProduce(self.url, keyWork, page)
            error = int(tempResponse['error'])
            result_list = tempResponse['result_list']
            volume = 0
            tryCount += 1
            if error == 0:
                volume = result_list[-1]['volume']
                break
            else:
                pass
        # print('volume %d' % volume)
        return volume

    def filteProduct(self, products):
        fProducts = list(filter(self.func, products))
        count = len(fProducts)
        # print('count %d' % count)
        if (count > 0):
            self.q.put(fProducts)
            # print("filteProduct qsize:%d" % self.q.qsize())

        return count
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
        # self.Flag = False  # boolean
        for task in self.all_task:
            task.cancel()
        self.executor.shutdown(wait=False)
        try:
            for task in self.all_task:
            task.cancel()
            self.keyWordThreadPool.shutdown(wait=False)

        except BaseException:
            pass
        self.stopTaskFlag = True

    def getProduce(self, url, keyWork, page=0):
        if self.mutex.acquire(2):
            self.douwnload_count += 1
            t = time.perf_counter()
            p = int(self.douwnload_count / t)
            # print(p)
            if p > 23:
                time.sleep(0.1)
            self.mutex.release()
        self.queryKeys["para"] = keyWork
        self.queryKeys['page'] = page
        response = requests.get(url, headers=headers, params=self.queryKeys)

        # print((response.url))
        # print("%s %s %d" % (url, keyWork, page))
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            jsonStr = '{"error": "1","msg": "", "search_type": "1", "is_similar": "0", "total_results": 50,  "result_list": []}'
            return json.loads(jsonStr)
        # return self.excelUtil.readExcel('testJson.json')
        # http://api.vephp.com/super?vekey=V00002371Y65180478&pid=mm_98723245_44422162_465706573&coupon=0&start_price=0&end_price=10000&start_tk_rate=0&end_tk_rate=0&volume=50000&is_tmall=0&freeship=0&pagesize=30&para=ins&page=1000

        # http://api.vephp.com/super?vekey=V00002371Y65180478&pid=mm_98723245_44422162_465706573&coupon=1&start_price=0&end_price=10000&start_tk_rate=0&end_tk_rate=5000&volume=500&is_tmall=0&freeship=0&pagesize=30&para=ins&page=801

        # http://api.vephp.com/super?vekey=V00002371Y65180478&pid=mm_98723245_44422162_465706573&coupon=1&start_price=0&end_price=10000&start_tk_rate=0&end_tk_rate=5000&volume=500&is_tmall=0&freeship=0&pagesize=30&para=ins&page=801
