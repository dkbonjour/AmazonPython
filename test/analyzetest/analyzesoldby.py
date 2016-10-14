# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import re


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

def getsoldbyreg(string):
    # 这里正则只是选取1-15个字段，然后就匹配.。
    # 防止抓取到其他的东西，一定要用{1,15}
    reg = r'(old by )(.*?)(\.)'
    all = re.compile(reg)
    alllist = re.findall(all, string)
    try:
        if alllist[0][1]:
            return alllist[0][1]
        else:
            return "No Sold by"
    except:
        return "No Sold by"

# 定义一个数组
soldby = []


def getsoldby(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:
        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")
        print(name)

        if 'id="shipsFromSoldBy_feature_div"' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品评论
            soldbys = content.xpath('//div[@id="shipsFromSoldBy_feature_div"]/div/a/text()')
            print(soldbys)
            if soldbys:
                temp = soldbys[0]
                #print(temp)
                # 写入数组
                soldby.append(temp)
            else:
                soldby.append("No Sold by")

        else:
            # 正则匹配
            temp = getsoldbyreg(html)
            soldby.append(temp)

        print(soldby)
        print(len(soldby))
        # 这里返回的是soldby
        # 返回的顺序
        # 可以在这里写导入数据库
        # 或者另开一个函数写导入数据库
        return soldby


# 开启多线程
# 以5个线程跑解析函数getsoldby
def threadingsoldby():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getsoldby, name)


if __name__ == '__main__':
    threadingsoldby()
