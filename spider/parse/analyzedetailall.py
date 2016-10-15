# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
from lxml import etree
import re
from spider.logic.urllogic import *

'''
# 抓取dp的正则表达式
def getdp(string):
    reg = r'(http.+?/dp/)(.+?)(/ref)'
    all = re.compile(reg)
    alllist = re.findall(all, string)
    try:
        return alllist[0][1]
    except:
        return "NO ASIN"
'''


# 正则大类排名
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


# 正则Sold by
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

    return htmlnames


# 定义一个数组
analyzecontent = []


def Analyzedetail():
    for name in openpath():
        # html保存的位置
        htmlpath = "H:/smartdo/data/"

        # 建立一个临时数组
        tempcontent = []

        if "detail" in name:
            # 读取html文件的内容
            filecontents = open(htmlpath + name, "rb")
            html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

            # xpath解析需要的东西
            content = etree.HTML(html)


           ## 得到大类排名
            # 正则查找匹配的排名字段
            try:
                tempcontent.append(getrank2reg(html))
            except Exception as err:
                print(err)
                tempcontent.append("Nothing")


             ## 得到商品名称
            # xpath解析得到当页商品的标题title
            titles = content.xpath('//h1[@id="title"]/span/text()')

            for item in titles:
                tempcontent.append(titles[0].strip())


            '''
            ## 得到ASIN
            ## 如果得到详情页的url，就可以在这里写下解析ASIN
            url = ""
            tempcontent.append(getdp(url.strip()))
            '''


            ## 得到评分等级
            # 判断是否有评分
            if "There are no customer reviews yet" in html:
                tempcontent.append("There are no customer reviews yet")

            elif 'id="acrPopover"' in html:

                # xpath解析得到当页商品等级
                stars = content.xpath('//span[@id="acrPopover"]/@title')

                # 原文4.2 out of 5 stars
                # 剔除 out of 5 stars
                temp = stars[0]
                tempcontent.append(temp.replace(" out of 5 stars", ""))

            elif 'class="a-icon a-icon-star a-star-5' in html:
                # xpath解析需要的东西
                content = etree.HTML(html)

                # xpath解析得到当页商品等级
                stars = content.xpath('//i[@class="a-icon a-icon-star a-star-5"]/span[@class="a-icon-alt"]/text()')

                # 原文4.2 out of 5 stars
                # 剔除 out of 5 stars
                temp = stars[0]
                tempcontent.append(temp.replace(" out of 5 stars", ""))
            else:
                tempcontent.append("Nothing")

            ## 得到评价数
            # 判断是否有评分
            # 没有评分就没有评论
            if "There are no customer reviews yet" in html:
                tempcontent.append("There are no customer reviews yet")
            elif 'id="acrCustomerReviewText"' in html:

                # xpath解析得到当页商品评论
                commentnums = content.xpath('//span[@id="acrCustomerReviewText"]/text()')

                # 原文117 customer reviews
                # 剔除 customer reviews
                temp = commentnums[0]
                tempcontent.append(temp.replace(" customer reviews", ""))
            elif 'class="a-size-small"' in html:
                # xpath解析需要的东西
                content = etree.HTML(html)

                # xpath解析得到当页商品评论数量
                commentnums = content.xpath(
                        '//span[@class="dpProductDetailB00WPRE0HA"]/span[@class="a-size-small"]/a[@class="a-link-normal"]/text()')

                # 原文117 customer reviews
                # 剔除 customer reviews
                temp = commentnums[0]
                tempcontent.append(temp.replace(" customer reviews", "").strip())
            else:
                tempcontent.append("Nothing")


            ## 得到价格
            if 'id="priceblock_saleprice"' in html:
                # xpath解析得到当页商品价格
                prices = content.xpath('//span[@id="priceblock_saleprice"]/text()')
                tempcontent.append(prices[0].strip())

            elif 'id="priceblock_ourprice"' in html:
                # xpath解析得到当页商品价格
                prices = content.xpath('//span[@id="priceblock_ourprice"]/text()')
                tempcontent.append(prices[0].strip())

            elif 'class="a-color-price"' in html:
                # xpath解析得到当页商品价格
                prices = content.xpath('//span[@class="a-color-price"]/text()')
                tempcontent.append(prices[0].strip())

            else:
                tempcontent.append("Price information is unavailable")


            ## 得到第一次评论时间
            # 判断是否有评分
            # 没有评分就没有评论
            if "There are no customer reviews yet" in html:
                tempcontent.append("There are no customer reviews yet")
            elif 'class="a-section celwidget"' in html:

                # xpath解析得到当页商品第一次评论时间
                commenttimes = content.xpath('//div[@class="a-section celwidget"][1]/div[1]/span/span/text()')

                # 剔除\n
                temp = commenttimes[3]
                if temp.strip():
                    tempcontent.append(temp.strip())
            else:
                tempcontent.append("Nothing")

            ## 得到Sold by
            if 'id="shipsFromSoldBy_feature_div"' in html:

                # xpath解析得到当页商品评论
                soldbys = content.xpath('//div[@id="shipsFromSoldBy_feature_div"]/div/a/text()')

                if soldbys:
                    temp = soldbys[0]

                    # 写入数组
                    tempcontent.append(temp)
                else:
                    tempcontent.append("No Sold by")

            else:
                # 正则匹配
                temp = getsoldbyreg(html)
                tempcontent.append(temp)

            ## 得到FBA
            if "Fulfilled by Amazon" in html:
                tempcontent.append("FBA")
            else:
                tempcontent.append("NO")


            '''
            ## 得到网址
            tempcontent.append("http://www.amazon.com/dp/" + getdp(url.strip()) + "/")
            '''

            analyzecontent.append(tempcontent)
    return analyzecontent


if __name__ == '__main__':
    a = time.clock()
    print(Analyzedetail())
    b = time.clock()
    print('运行时间：' + timetochina(b - a))
