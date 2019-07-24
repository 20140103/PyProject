#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog
from tkinter import *
from tkinter import scrolledtext
import configparser
# from taskWork import myThread as taskWork
from MultTaskWork import MultTaskWork

from jiexi import ExcelUtil
import time
import os

DEFALUT = {
    'width': 1000,
    'height': 720,
    'showX': 100,
    'showY': 100,
    'is_tmall': 0,
    'freeship': 0,
    'coupon': 0,
    'var_task_name': '',
    'var_query_start_price': 0,
    'var_query_end_price': 0,
    'var_query_start_tk_rate': 0,
    'var_query_end_tk_rate': 0,
    'var_query_volume': 0,
    'var_config_sava_dir': '',
    'var_config_keywork_filename': ''
}


class App:
    window = 0
    width = 1000
    height = 720
    showX = 100
    showY = 100

    def __init__(self):
        self.keyWords = []
        self.queryKeys = {}
        App.window = tk.Tk()
        App.window.title('alimama')
        self.tastStart = False
        self.config = self.readConfig()
        # print(self.config)
        # print("%sx%s+%s+%s" % (self.config['width'], self.config['height'],
        #                        self.config['showX'], self.config['showY']))
        App.window.geometry("%sx%s+%s+%s" %
                            (self.config['width'], self.config['height'],
                             self.config['showX'], self.config['showY']))
        App.configLayout(self)
        App.window.bind("<Configure>", self.up)

        App.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        App.window.mainloop()

    def configLayout(self):
        tk.Label(App.window, text='任务名称: ').place(x=50, y=50)
        self.var_task_name = tk.StringVar()
        self.var_task_name.set(self.config['var_task_name'])
        entry_task_name = tk.Entry(App.window, textvariable=self.var_task_name)
        entry_task_name.place(x=160, y=50)

        tk.Label(App.window, text='筛选: ').place(x=50, y=140)

        y = 140 - 50
        x = 160
        dx = 200
        width = 5
        tk.Label(App.window, text='券后价: ').place(x=x, y=y)
        self.var_query_start_price = tk.IntVar()
        self.var_query_start_price.set(self.config['var_query_start_price'])
        entry_config_jiage_min = tk.Entry(
            App.window, textvariable=self.var_query_start_price, width=width)
        entry_config_jiage_min.place(x=x + 50, y=y)
        self.var_query_end_price = tk.IntVar()
        self.var_query_end_price.set(self.config['var_query_end_price'])
        entry_config_jiage_max = tk.Entry(
            App.window, textvariable=self.var_query_end_price, width=width)
        entry_config_jiage_max.place(x=x + 120, y=y)

        tk.Label(App.window, text='月销量>: ').place(x=x + dx * 1, y=y)
        self.var_query_volume = tk.IntVar()

        self.var_query_volume.set(self.config['var_query_volume'])
        entry_config_xiaoliang = tk.Entry(App.window,
                                          textvariable=self.var_query_volume,
                                          width=width)
        entry_config_xiaoliang.place(x=x + dx * 1 + 50, y=y)

        tk.Label(App.window, text='佣金: ').place(x=x + dx * 2, y=y)
        self.var_query_start_tk_rate = tk.IntVar()
        self.var_query_start_tk_rate.set(
            self.config['var_query_start_tk_rate'])
        entry_config_quanmiane = tk.Entry(
            App.window, textvariable=self.var_query_start_tk_rate, width=width)
        entry_config_quanmiane.place(x=x + dx * 2 + 50, y=y)

        self.var_query_end_tk_rate = tk.IntVar()
        self.var_query_end_tk_rate.set(self.config['var_query_end_tk_rate'])
        entry_config_quanmiane = tk.Entry(
            App.window, textvariable=self.var_query_end_tk_rate, width=width)
        entry_config_quanmiane.place(x=x + dx * 2 + 50 + 70, y=y)

        # tk.Label(App.window, text='收入比率>: ').place(x=x + dx * 3, y=y)

        # self.var_config_shourubi = tk.IntVar()

        # self.var_config_shourubi.set(self.config['var_config_shourubi'])
        # entry_config_shourubi = tk.Entry(App.window,
        #                                  textvariable=self.var_config_shourubi,
        #                                  width=width)
        # entry_config_shourubi.place(x=x + dx * 3 + 90, y=y)

        self.is_tmall = tk.IntVar()  # 定义var1和var2整型变量用来存放选择行为返回值
        self.is_tmall.set(self.config['is_tmall'])
        self.coupon = tk.IntVar()
        self.coupon.set(self.config['coupon'])
        self.freeship = tk.IntVar()
        self.freeship.set(self.config['freeship'])
        c1 = tk.Checkbutton(
            App.window,
            text='天猫',
            variable=self.is_tmall,
            onvalue=1,
            offvalue=0,
            command=self.print_selection)  # 传值原理类似于radiobutton部件
        c1.place(x=x, y=y + 50)
        c2 = tk.Checkbutton(
            App.window,
            text='优惠券',
            variable=self.coupon,
            onvalue=1,
            offvalue=0,
            command=self.print_selection)  # 传值原理类似于radiobutton部件
        c2.place(x=x + 60, y=y + 50)
        c3 = tk.Checkbutton(App.window,
                            text='包邮',
                            variable=self.freeship,
                            onvalue=1,
                            offvalue=0,
                            command=self.print_selection,
                            fg='blue')  # 传值原理类似于radiobutton部件
        c3.place(x=x + 140, y=y + 50)

        tk.Label(App.window, text='文件路径: ').place(x=50, y=y + 50 + 50)

        self.var_config_keywork_filename = tk.StringVar()

        self.var_config_keywork_filename.set(
            self.config['var_config_keywork_filename'])
        entry_config_filename = tk.Entry(
            App.window,
            textvariable=self.var_config_keywork_filename,
            width=60)
        entry_config_filename.place(x=x, y=y + 50 + 50)
        btn_open_file_up = tk.Button(App.window,
                                     text='...',
                                     bg="blue",
                                     command=self.xz)
        btn_open_file_up.place(x=x + 50 + 90 + 220 + 200, y=y + 50 + 50)

        tk.Label(App.window, text='保存位置: ').place(x=50, y=y + 50 + 50 + 50)

        self.var_config_sava_dir = tk.StringVar()

        self.var_config_sava_dir.set(self.config['var_config_sava_dir'])
        entry_config_save_dir = tk.Entry(App.window,
                                         textvariable=self.var_config_sava_dir,
                                         width=60)
        entry_config_save_dir.place(x=x, y=y + 50 + 50 + 50)
        btn_open_save_dir = tk.Button(App.window,
                                      text='...',
                                      bg="blue",
                                      command=self.saveDir)
        btn_open_save_dir.place(x=x + 50 + 90 + 220 + 200, y=y + 50 + 50 + 50)
        # btn_open_file_up.pack(fill=BOTH, expand=True)

        tk.Label(App.window, text='关键词预览: ').place(x=50, y=y + 50 + 50 + 150)

        self.t = scrolledtext.ScrolledText(App.window,
                                           width=90,
                                           height=9,
                                           font=('隶书', 12))
        # self.t = tk.Text(App.window, height=20)
        self.t.place(x=x, y=y + 50 + 50 + 100)

        tk.Label(App.window, text='日志: ').place(x=50,
                                                y=y + 50 + 50 + 100 + 160 + 30)
        self.tInfo = scrolledtext.ScrolledText(App.window,
                                               width=90,
                                               height=7,
                                               font=('隶书', 12))
        self.tInfo.place(x=x, y=y + 50 + 50 + 100 + 180)

        btn_create_task = tk.Button(App.window,
                                    text='开始创建',
                                    bg="blue",
                                    command=self.createTask,
                                    width=20)
        btn_create_task.place(x=500 - 150, y=720 - 70)
        if len(self.var_config_keywork_filename.get()) > 0:
            self.readKeyWordFile(self.var_config_keywork_filename.get())

    def showLogInfo(self, msg):
        detester = time.strftime("%m-%d %H:%M:%S", time.localtime())
        self.tInfo.insert(tkinter.INSERT, detester + ': ' + msg + '\n')
        self.tInfo.see(tkinter.END)

    def on_closing(self):
        if messagebox.askokcancel("退出", "你确认要退出吗?"):
            self.saveConfig()
            try:
                if self.multTaskWork:
                    self.multTaskWork.stop()
            except BaseException:
                pass
            App.window.destroy()

    ###
    def up(self, event):
        # pix = "坐标[%d,%d]" % (event.x, event.y)  # 获得窗口当前坐标
        # print(pix)
        # App.width = event.width
        # App.height = event.height
        App.showX = event.x
        App.showY = event.y
        self.saveConfig()

    def print_selection(self):
        # self.var_config_filename.set("print_selection")

        # print('print_selection')
        pass

    def saveConfig(self):
        config = configparser.ConfigParser()  # 类中一个方法 #实例化一个对象

        config["DEFAULT"] = {
            'width': App.width,
            'height': App.height,
            'showX': App.showX,
            'showY': App.showY,
            'is_tmall': self.is_tmall.get(),
            'freeship': self.freeship.get(),
            'coupon': self.coupon.get(),
            'var_task_name': self.var_task_name.get(),
            'var_query_start_price': self.var_query_start_price.get(),
            'var_query_end_price': self.var_query_end_price.get(),
            'var_query_start_tk_rate': self.var_query_start_tk_rate.get(),
            'var_query_end_tk_rate': self.var_query_end_tk_rate.get(),
            'var_query_volume': self.var_query_volume.get(),
            'var_config_sava_dir': self.var_config_sava_dir.get(),
            'var_config_keywork_filename':
            self.var_config_keywork_filename.get()
        }  # 类似于操作字典的形式
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def readConfig(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        if config.defaults():
            return config['DEFAULT']
        else:
            # print('空')
            return DEFALUT

    def createTask(self):
        if len(self.var_config_sava_dir.get()) <= 0:
            self.showLogInfo('请设置数据保存路径')
            return
        self.queryKeys['coupon'] = self.coupon.get()
        self.queryKeys['start_price'] = self.var_query_start_price.get()
        self.queryKeys['end_price'] = self.var_query_end_price.get()
        self.queryKeys['start_tk_rate'] = self.var_query_start_tk_rate.get()
        self.queryKeys['end_tk_rate'] = self.var_query_end_tk_rate.get()
        self.queryKeys['volume'] = self.var_query_volume.get()
        self.queryKeys['is_tmall'] = self.is_tmall.get()
        self.queryKeys['freeship'] = self.freeship.get()
        # 开始任务
        if (not self.tastStart):
            # self.work = taskWork(self.keyWords, self.queryKeys, self)

            self.multTaskWork = MultTaskWork(self.keyWords, self.queryKeys,
                                             self)
            # self.work.start()
            self.tastStart = self.multTaskWork.isStarting()
        else:
            self.showLogInfo('任务结束中 请稍后...0')
            self.multTaskWork.stop()
            self.tastStart = self.multTaskWork.isStarting()

    def xz(self):
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            # lb.config(text = "您选择的文件是："+filename)
            # print("您选择的文件是：%s" % filename)
            self.var_config_keywork_filename.set(filename)
            self.readKeyWordFile(filename)
        else:
            # lb.config(text = "您没有选择任何文件")
            messagebox.showinfo("您没有选择任何文件", filename)

    def saveDir(self):
        filename = tkinter.filedialog.askdirectory()
        if filename != '':
            # lb.config(text = "您选择的文件是："+filename)
            print("您选择的文件是：%s" % filename)
            self.var_config_sava_dir.set(filename)
        else:
            # lb.config(text = "您没有选择任何文件")
            messagebox.showinfo("您没有选择任何文件", filename)

    def readKeyWordFile(self, fileName):
        if not os.path.exists(fileName):
            self.showLogInfo('%s 不存在' % fileName)
            return

        fileObject = open(fileName, mode='r')
        keyWorkCount = 0
        self.keyWords = []  # 清空前一个数据
        self.showLogInfo('开始导入关键词')
        for line in fileObject:
            # print(line.strip())
            keyWorkCount += 1
            # print(keyWorkCount)
            kw = line.strip()
            self.keyWords.append(kw)
            self.t.insert(tkinter.INSERT, kw + '\n')
            self.t.see(tkinter.END)
        # 关闭打开的文件
        self.showLogInfo('本次共导入%d关键词' % keyWorkCount)
        fileObject.close()