# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
from lxml import etree


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


def getcommentnum():
    # html保存的位置
    htmlpath = "H:/smartdo/data/"
    # 读取到文件夹下所有的html文件
    htmlnames = listfiles(htmlpath, "html")

    comment = []

    for name in htmlnames:

        if "detail" in name:

            # 建立一个临时数组储存
            tempcomment = []

            # 读取html文件的内容
            filecontents = open(htmlpath + name, "rb")
            html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

            print(name)

            # 判断是否有评分
            # 没有评分就没有评论
            if "There are no customer reviews yet" in html:
                tempcomment.append("There are no customer reviews yet")
            elif 'id="acrCustomerReviewText"' in html:
                # xpath解析需要的东西
                content = etree.HTML(html)

                # xpath解析得到当页商品评论
                comments = content.xpath('//span[@id="acrCustomerReviewText"]/text()')
                # print(comments)

                # 原文117 customer reviews
                # 剔除 customer reviews
                temp = comments[0]
                tempcomment.append(temp.replace(" customer reviews", ""))
            elif 'class="a-size-small"' in html:
                # xpath解析需要的东西
                content = etree.HTML(html)

                # xpath解析得到当页商品评论
                comments = content.xpath(
                        '//span[@class="dpProductDetailB00WPRE0HA"]/span[@class="a-size-small"]/a[@class="a-link-normal"]/text()')
                print(comments)

                # 原文117 customer reviews
                # 剔除 customer reviews
                temp = comments[0]
                tempcomment.append(temp.replace(" customer reviews", "").strip())

            comment.append(tempcomment)
    print(comment)


if __name__ == '__main__':
    getcommentnum()
