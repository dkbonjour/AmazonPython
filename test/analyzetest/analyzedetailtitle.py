# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
import tool.log
import logging
from lxml import etree

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)

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


# 解析得到详情页的title
def gettitle():
    # 打开下载到本地的文件
    htmlnames = listfiles(tool.log.BASE_DIR + "/data/","html")
    # 建立一个数组来储存解析得到的详情页title
    gettitles = []
    for name in htmlnames:
        if "detail" in name:
            htmlpath = name
            #print(htmlpath)
            file = open(tool.log.BASE_DIR + "/data/" + htmlpath,"rb")
            htmlcontent = file.read().decode("UTF-8","ignore")

            # xpath解析需要的东西
            content = etree.HTML(htmlcontent)
            # xpath解析得到当页商品的标题title
            titles = content.xpath('//h1[@id="title"]/span/text()')

            for item in titles:
                gettitles.append(titles[0].strip())

    return gettitles

if __name__ == "__main__":
    print(gettitle())
    print(len(gettitle()))
