# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

# 读取文件夹下面的文件
def listfiles(rootdir, prefix='.xml', iscur=False):
    file = []
    for parent, dirnames, filenames in os.walk(rootdir):
        if parent == rootdir:
            for filename in filenames:
                if filename.endswith(prefix):
                    file.append(filename)
            if not iscur:
                return file
        else:
            if iscur:
                for filename in filenames:
                    if filename.endswith(prefix):
                        file.append(filename)
            else:
                pass
    return file

def openpath():
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    # 读取到文件夹下所有的html文件
    htmlnames = listfiles(htmlpath, "html")
    # print(htmlnames)

    return htmlnames

# 定义一个数组
price = []
namelist = []
num = []

def getprice(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:
        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        # xpath解析需要的东西
        content = etree.HTML(html)

        if 'id="priceblock_saleprice"' in html:
            # xpath解析得到当页商品价格
            prices = content.xpath('//span[@id="priceblock_saleprice"]/text()')
            price.append(prices[0].strip())

        elif 'id="priceblock_ourprice"' in html:
            # xpath解析得到当页商品价格
            prices = content.xpath('//span[@id="priceblock_ourprice"]/text()')
            price.append(prices[0].strip())

        elif 'class="a-color-price"' in html:
            # xpath解析得到当页商品价格
            prices = content.xpath('//span[@class="a-color-price"]/text()')
            price.append(prices[0].strip())

        else:
            price.append("Price information is unavailable")


        num.append(len(namelist))
        namelist.append(name)
        print(num)
        print(namelist)
        print(price)
        # 这里返回的是price
        # 返回的顺序
        # 可以在这里写导入数据库
        # 或者另开一个函数写导入数据库
        return  price

# 开启多线程
# 以5个线程跑解析函数price
def threadingprice():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getprice, name)

if __name__ == '__main__':
    threadingprice()
