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
firstcommenttime = []


def getfirstcommenttime(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:

        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        # print(name)

        # 判断是否有评分
        # 没有评分就没有评论
        if "There are no customer reviews yet" in html:
            firstcommenttime.append("There are no customer reviews yet")
        elif 'class="a-section celwidget"' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品第一次评论时间
            commenttimes = content.xpath('//div[@class="a-section celwidget"][1]/div[1]/span/span/text()')
            print(commenttimes)

            # 剔除\n
            temp = commenttimes[3]
            firstcommenttime.append(temp.strip())

        print(firstcommenttime)
        print(len(firstcommenttime))
        # 这里返回的是firstcommenttime
        # 返回的顺序
        # 可以在这里写导入数据库
        # 或者另开一个函数写导入数据库
        return firstcommenttime


# 开启多线程
# 以5个线程跑解析函数getfirstcommenttime
def threadingfirstcommenttime():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getfirstcommenttime, name)


if __name__ == '__main__':
    threadingfirstcommenttime()
