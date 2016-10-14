# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
import re
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


def getrank2reg(string):
    # 这里正则只是选取1-5个字段，然后就匹配 in 。
    # 防止抓取到其他的东西，一定要用{1,5}
    reg = r'(#)(.{1,8})( in )'
    all = re.compile(reg)
    alllist = re.findall(all, string)
    try:
        return alllist[0][1]
    except:
        return "No ranking"


def openpath():
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    # 读取到文件夹下所有的html文件
    htmlnames = listfiles(htmlpath, "html")
    # print(htmlnames)

    return htmlnames


# 定义一个数组
rank2 = []


def getrank2(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:
        # 建立一个临时数组来储存
        temprank2 = []
        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")
        # print(name)
        # 正则查找匹配的排名字段
        temprank2.append(getrank2reg(html))
        print(temprank2)
        rank2.append(temprank2)
        # print(rank2)
        # 这里返回的是rank2
        # 可以在这里写导入数据库
        # 或者另开一个函数写导入数据库
        return rank2


# 开启多线程
# 以5个线程跑解析函数getrank2
def threadingrank2():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getrank2, name)


if __name__ == '__main__':
    threadingrank2()
