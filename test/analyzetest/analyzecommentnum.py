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
commentnum = []

def getcommentnum(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:

        # 建立一个临时数组储存
        tempcomment = []

        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        #print(name)

        # 判断是否有评分
        # 没有评分就没有评论
        if "There are no customer reviews yet" in html:
            tempcomment.append("There are no customer reviews yet")
        elif 'id="acrCustomerReviewText"' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品评论
            commentnums = content.xpath('//span[@id="acrCustomerReviewText"]/text()')
            # print(comments)

            # 原文117 customer reviews
            # 剔除 customer reviews
            temp = commentnums[0]
            tempcomment.append(temp.replace(" customer reviews", ""))
        elif 'class="a-size-small"' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品评论数量
            commentnums = content.xpath(
                    '//span[@class="dpProductDetailB00WPRE0HA"]/span[@class="a-size-small"]/a[@class="a-link-normal"]/text()')
            print(commentnums)

            # 原文117 customer reviews
            # 剔除 customer reviews
            temp = commentnums[0]
            tempcomment.append(temp.replace(" customer reviews", "").strip())

        commentnum.append(tempcomment)
    #print(commentnum)
    # 这里返回的是commentnum
    # 返回的顺序
    # 可以在这里写导入数据库
    # 或者另开一个函数写导入数据库
    return commentnum


# 开启多线程
# 以5个线程跑解析函数getcommentnum
def threadingcommentnum():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        results=pool.submit(getcommentnum, name)
    return results.result()

if __name__ == '__main__':
    a = []

    a.append(threadingcommentnum())
    print(a)
