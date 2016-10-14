# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
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
FBAs = []


def getFBA(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:
        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")
        print(name)

        if "Fulfilled by Amazon" in html:
            FBAs.append("FBA")
        else:
            FBAs.append("NO")

        print(FBAs)
        print(len(FBAs))


# 开启多线程
# 以5个线程跑解析函数getFBA
def threadingFBA():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getFBA, name)


if __name__ == '__main__':
    threadingFBA()
