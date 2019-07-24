#!/usr/bin/python
# -*- coding: UTF-8 -*-

# from PIL import Image
# import numpy as np
# import cv2
# img2 = Image.open('./Amazing_COL_2Fix.bmp')
# img1 = Image.open('./Amazing_RGB_2L.bmp')
# # img1 = img1.convert('RGBA')
# img2 = img2.convert('RGBA')
# pixdata = img2.load()
# for y in range(img2.size[1]):
#     for x in range(img2.size[0]):
#         if pixdata[x,y][0]==0 and pixdata[x,y][1]==0 and pixdata[x,y][2]<256:
#            pixdata[x, y] = (255, 255, 255,0)

# img2.show()

from PIL import Image

from PIL import ImageFilter

i = 1
j = 1
img = Image.open('./ic_launcher.png')#读取系统的内照片
gray=img.convert('L')   #转换成灰度
gray.show()

threshold = 200
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
# 图片二值化
photo = gray.point(table, '1')
photo.save("./test2.jpg")
photo.show()
# r,g,b=img.split()   #分离三通道
# pic=Image.merge('RGB',(r,g,b)) #合并三通道
# pic.show()

print (img.size)#打印图片大小
print (img.getpixel((4,4)))
red = 100
glue = 140
blue = 180
width = img.size[0]#长度
height = img.size[1]#宽度

newIm= Image.new('RGBA', img.size)
newIm.save('./test003.png')
imgNew = Image.open('./test003.png')#读取系统的内照片
for i in range(1,width-1):#遍历所有长度的点
    for j in range(1,height-1):#遍历所有宽度的点

        data1 = (img.getpixel((i-1,j-1)))#打印该图片的所有点
        data2 = (img.getpixel((i-1,j)))#打印该图片的所有点
        data3 = (img.getpixel((i-1,j+1)))#打印该图片的所有点


        data4 = (img.getpixel((i,j-1)))#打印该图片的所有点
        data5 = (img.getpixel((i,j)))#打印该图片的所有点
        data6 = (img.getpixel((i,j+1)))#打印该图片的所有点


        data7 = (img.getpixel((i+1,j-1)))#打印该图片的所有点
        data8 = (img.getpixel((i+1,j)))#打印该图片的所有点
        data9 = (img.getpixel((i+1,j+1)))#打印该图片的所有点

        r = (data1[0] + data2[0] +data3[0] +data4[0] +data5[0] +data6[0] +data7[0] +data8[0] +data9[0] ) / 9
        g = (data1[1] + data2[1] +data3[1] +data4[1] +data5[1] +data6[1] +data7[1] +data8[1] +data9[1] ) / 9
        b = (data1[2] + data2[2] +data3[2] +data4[2] +data5[2] +data6[2] +data7[2] +data8[2] +data9[2] ) / 9

        # print("rgb: %d  %d %d" % (r,g,b))
        # print (data)#打印每个像素点的颜色RGBA的值(r,g,b,alpha)
        # print (data[0])#打印RGBA的r值!
        if (r>red  and g>glue  and b>blue ):#RGBA的r值大于170，并且g值大于170,并且b值大于170
            # img.putpixel((i,j),(234,53,57,255))#则这些像素点的颜色改成大红色
            imgNew.putpixel((i,j),(255,255,255,255))#则这些像素点的颜色改成大红色
# img = img.convert("RGBA")#把图片强制转成RGB
# img.save("./ic_launcher6.png")#保存修改像素点后的图片
imgNew.show()
imgNew = imgNew.filter(ImageFilter.SMOOTH) 
imgNew.show()
# from PIL import Image
# from PIL import ImageFilter
# import ImageFilter  
  
# im=Image.open('./ic_launcher.png')  
# im=im.filter(ImageFilter.SHARPEN)  
  
# im.show()

# 通常使用RGB模式就可以了
# newIm= Image.new('RGB', (100, 100), 'red')
# newIm.save('./test001.jpg')