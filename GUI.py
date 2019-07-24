#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from PIL import Image, ImageTk
import tkinter as tk
root = tk.Tk()

root.title('淘宝商品信息采集')        #窗口标题  
root.resizable(False, False)    #固定窗口大小  
windowWidth = 800               #获得当前窗口宽  
windowHeight = 500              #获得当前窗口高  
screenWidth, screenHeight = root.maxsize()     #获得屏幕宽和高  
geometryParam = '%dx%d+%d+%d'%(windowWidth, windowHeight, (screenWidth-windowWidth)/2, (screenHeight - windowHeight)/2)  
root.geometry(geometryParam)    #设置窗口大小及偏移坐标  
root.wm_attributes('-topmost',1)#窗口置顶  

# im=Image.open("IMG_4507.PNG")
# img=ImageTk.PhotoImage(im)

# label = tk.Label(root,image = img, fg = 'blue', bg = 'red',width = 300, height = 400, text = "color")

def show_image():
    imLabel=tk.Label(root,image=img).pack()

def change():
    # im=Image.open("IMG_4507.PNG")
    # img=ImageTk.PhotoImage(im)
    # label.configure(image=img)
    # # label.config(fg='blue')
    # label.config(bg='red')
    # label.config(width = 300)
    # label.config(height = 400)
    pass

def main():
    #不带图button  
    button = tk.Button(root, text = '不带图按钮',command=change) 
    button.pack()
    #显示图片
    # im=Image.open("IMG_4507.PNG")
    # img=ImageTk.PhotoImage(im)
    # imLabel=tk.Label(root,image=img).pack()
    # show_image()
    # label.pack()
     # 进入消息循环
    root.bind('<Escape>', lambda e: root.destroy())
    root.mainloop()

if __name__ == '__main__':
    main()