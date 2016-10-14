# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
from lxml import etree
import tool.log
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
star = []


def getstars(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:
        # 建立一个临时数组储存
        tempstar = []

        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        # 判断是否有评分
        if "There are no customer reviews yet" in html:
            tempstar.append("There are no customer reviews yet")

        elif 'id="acrPopover"' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品等级
            stars = content.xpath('//span[@id="acrPopover"]/@title')

            # 原文4.2 out of 5 stars
            # 剔除 out of 5 stars
            temp = stars[0]
            tempstar.append(temp.replace(" out of 5 stars", ""))

        elif 'class="a-icon a-icon-star a-star-5' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品等级
            stars = content.xpath('//i[@class="a-icon a-icon-star a-star-5"]/span[@class="a-icon-alt"]/text()')

            # 原文4.2 out of 5 stars
            # 剔除 out of 5 stars
            temp = stars[0]
            tempstar.append(temp.replace(" out of 5 stars", ""))
        star.append(tempstar)
        # print(star)
        # 这里返回的是star
        # 可以在这里写导入数据库
        # 或者另开一个函数写导入数据库
        return star


# 开启多线程
# 以5个线程跑解析函数getstar
def threadingstar():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getstars, name)


if __name__ == '__main__':
    threadingstar()
