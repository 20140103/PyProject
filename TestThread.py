#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import threading
import time
import requests
import json
exitFlag = 0
 
class myThread (threading.Thread):   #继承父类threading.Thread
    url = 'http://tooker.work:10032/api/test_post'

    body = {"infos": [{"tag":"testInfo","time:":time.time()}]}
    
    headers = {'content-type': "application/json"}
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        print "Starting " + self.name
        # print_time(self.name, self.counter, 5)

        response = requests.post(self.url, data = json.dumps(self.body), headers = self.headers)
        print("%s:%s" % (self.name,response.status_code))
 
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            (threading.Thread).exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1
 
# 创建新线程
i = 0
while(i < 100000):
    thread1 = myThread(i, "Thread-%s" % i, i)
    thread1.start()
    i+=1

    # thread2 = myThread(2, "Thread-2", 2)
 
# 开启线程
# thread1.start()
# thread2.start()
 

# body = {"Infos": [{"tag":"testInfo","time:":time.time()}]}
# print json.dumps(body)
print "Exiting Main Thread"