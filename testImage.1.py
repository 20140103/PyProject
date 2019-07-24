#!/usr/bin/python
# -*- coding: UTF-8 -*-


from PIL import Image

from PIL import ImageFilter,ImageDraw

import math
def createCircleImage(size):
    width = size[0]
    height = size[1]
    
    r = width/2
    imgNew= Image.new('RGBA', size)

    
    draw = ImageDraw.Draw(imgNew) 
    x1 = 0
    y1 = 0
    x2 = 80
    y2 = 80   
    color = (255,255,255,200)               
    draw.line([(x1,y1),(x2,y2)], fill = color,width=1) 

    imgNew.save("./test0030.png", "PNG") 
    # newIm.save('./test0030.png')
    # imgNew = Image.open('./test0030.png')#读取系统的内照片
    # for i in range(width):#遍历所有长度的点
    #     for j in range(height):#遍历所有宽度的点
    #         dx = i - r
    #         dy = j - r
    #         dr = math.sqrt(dx*dx + dy*dy)
    #         if(dr >= r):
    #             imgNew.putpixel((i,j),(255,255,255,0))
    #         else:
    #             imgNew.putpixel((i,j),(45,92,227,255))
        
    # imgNew.show()
    # imgNew.filter(ImageFilter.SMOOTH).save("./test0030.png")
# imgNew = imgNew.filter(ImageFilter.SHARPEN)
# imgNew.show()
# # from PIL import Image
# # from PIL import ImageFilter
# # import ImageFilter  
  
# # im=Image.open('./ic_launcher.png')  
# # im=im.filter(ImageFilter.SHARPEN)  
  
# # im.show()

# # 通常使用RGB模式就可以了
# # newIm= Image.new('RGB', (100, 100), 'red')
# # newIm.save('./test001.jpg')

def createImage(saveImageName,imageColor,imageSize):

    width = imageSize[0]
    height = imageSize[1]
    imgNew= Image.new('RGBA', imageSize)
    for i in range(width):#遍历所有长度的点
        for j in range(height):#遍历所有宽度的点
            imgNew.putpixel((i,j),(255,255,255,255))
    imgNew.save(saveImageName)
def circle(imageFile):
    ima = Image.open(imageFile).convert("RGBA")
    # ima = ima.resize((600, 600), Image.ANTIALIAS)
    size = ima.size
    print(size)
 
    # 因为是要圆形，所以需要正方形的图片
    r2 = min(size[0], size[1])
    if size[0] != size[1]:
        ima = ima.resize((r2, r2), Image.ANTIALIAS)
 
    # 最后生成圆的半径
    r3 = 60
    imb = Image.new('RGBA', (r3*2, r3*2),(255,255,255,0))
    pima = ima.load()  # 像素的访问对象
    pimb = imb.load()
    r = float(r2/2) #圆心横坐标
 
    for i in range(r2):
        for j in range(r2):
            lx = abs(i-r) #到圆心距离的横坐标
            ly = abs(j-r)#到圆心距离的纵坐标
            l  = (pow(lx,2) + pow(ly,2))** 0.5  # 三角函数 半径
            if l < r3:
                pimb[i-(r-r3),j-(r-r3)] = pima[i,j]
    imb.save("test_circle.png")


# createImage("./test0030.png",(255,255,255,255),[80,80])
# circle("./test0030.png")
createCircleImage([160,160])