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

# 解析得到详情页的rank1
def detailrank1():
    # 打开下载到本地的文件
    htmlnames = listfiles(tool.log.BASE_DIR + "/data/","html")
    # 建立一个数组来储存解析得到的详情页rank1
    detailrank1s = []
    for htmlname in htmlnames:
        htmlpath = htmlname
        #print(htmlpath)
        file = open(tool.log.BASE_DIR + "/data/" + htmlpath,"rb")
        htmlcontent = file.read().decode("UTF-8","ignore")

        # xpath解析需要的东西
        content = etree.HTML(htmlcontent)
        # xpath解析得到当页商品的小类排名rank1
        rank1s = content.xpath('//div[@class="zg_rankDiv"]/span/text()')

        for item in rank1s:
            detailrank1s.append(item.strip().strip("."))

    return detailrank1s

if __name__ == "__main__":
    print(detailrank1())
