# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import re


## 合并到代码里面时
## 将name（文件名）替换数据库的唯一ID


# 大类排名的正则表达式
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


# Sold by的正则表达式
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


# 定义一个字典
star = {}
FBAs = {}
price = {}
rank2 = {}
soldby = {}
firstcommenttime = {}
commentnum = {}


## 得到评分等级
def getstars(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:

        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        # 判断是否有评分
        if "There are no customer reviews yet" in html:
            star[name] = "There are no customer reviews yet"

        elif 'id="acrPopover"' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品等级
            stars = content.xpath('//span[@id="acrPopover"]/@title')

            # 原文4.2 out of 5 stars
            # 剔除 out of 5 stars
            temp = stars[0]
            star[name] = temp.replace(" out of 5 stars", "")

        elif 'class="a-icon a-icon-star a-star-5' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品等级
            stars = content.xpath('//i[@class="a-icon a-icon-star a-star-5"]/span[@class="a-icon-alt"]/text()')

            # 原文4.2 out of 5 stars
            # 剔除 out of 5 stars
            temp = stars[0]
            star[name] = temp.replace(" out of 5 stars", "")

        return star


# 开启多线程
# 以5个线程跑解析函数getstar
def threadingstar():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getstars, name)
    return pool.submit(getstars, name).result()


## 得到价格
def getprice(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:
        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        # xpath解析需要的东西
        content = etree.HTML(html)

        if 'id="priceblock_saleprice"' in html:
            # xpath解析得到当页商品价格
            prices = content.xpath('//span[@id="priceblock_saleprice"]/text()')
            price[name] = prices[0].strip()

        elif 'id="priceblock_ourprice"' in html:
            # xpath解析得到当页商品价格
            prices = content.xpath('//span[@id="priceblock_ourprice"]/text()')
            price[name] = prices[0].strip()

        elif 'class="a-color-price"' in html:
            # xpath解析得到当页商品价格
            prices = content.xpath('//span[@class="a-color-price"]/text()')
            price[name] = prices[0].strip()

        else:
            price[name] = "Price information is unavailable"

        return price


# 开启多线程
# 以5个线程跑解析函数getprice
def threadingprice():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getprice, name)
    return pool.submit(getprice, name).result()


## 得到大类排名
def getrank2(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:
        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        # 正则查找匹配的排名字段
        rank2[name] = getrank2reg(html)

        return rank2


# 开启多线程
# 以5个线程跑解析函数getrank2
def threadingrank2():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getrank2, name)
    return pool.submit(getrank2, name).result()


## 得到Sold by
def getsoldby(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:
        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        if 'id="shipsFromSoldBy_feature_div"' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品评论
            soldbys = content.xpath('//div[@id="shipsFromSoldBy_feature_div"]/div/a/text()')

            if soldbys:
                temp = soldbys[0]

                # 写入数组
                soldby[name] = temp
            else:
                soldby[name] = "No Sold by"

        else:
            # 正则匹配
            temp = getsoldbyreg(html)
            soldby[name] = temp

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
    return pool.submit(getsoldby, name).result()


## 得到FBA
def getFBA(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:
        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        if "Fulfilled by Amazon" in html:
            FBAs[name] = "FBA"
        else:
            FBAs[name] = "NO"

        return FBAs


# 开启多线程
# 以5个线程跑解析函数getFBA
def threadingFBA():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getFBA, name)
    return pool.submit(getFBA, name).result()


##得到第一次评论时间
def getfirstcommenttime(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:

        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        # 判断是否有评分
        # 没有评分就没有评论
        if "There are no customer reviews yet" in html:
            firstcommenttime[name] = "There are no customer reviews yet"
        elif 'class="a-section celwidget"' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品第一次评论时间
            commenttimes = content.xpath('//div[@class="a-section celwidget"][1]/div[1]/span/span/text()')

            # 剔除\n
            temp = commenttimes[3]
            firstcommenttime[name] = temp.strip()

        return firstcommenttime


# 开启多线程
# 以5个线程跑解析函数getfirstcommenttime
def threadingfirstcommenttime():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getfirstcommenttime, name)
    return pool.submit(getfirstcommenttime, name).result()


## 得到评论数
def getcommentnum(name):
    # html保存的位置
    htmlpath = "H:/smartdo/data/"

    if "detail" in name:

        # 读取html文件的内容
        filecontents = open(htmlpath + name, "rb")
        html = filecontents.read().decode('UTF-8', 'ignore').replace("\r", "")

        # 判断是否有评分
        # 没有评分就没有评论
        if "There are no customer reviews yet" in html:
            commentnum[name] = "There are no customer reviews yet"
        elif 'id="acrCustomerReviewText"' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品评论
            commentnums = content.xpath('//span[@id="acrCustomerReviewText"]/text()')

            # 原文117 customer reviews
            # 剔除 customer reviews
            temp = commentnums[0]
            commentnum[name] = temp.replace(" customer reviews", "")
        elif 'class="a-size-small"' in html:
            # xpath解析需要的东西
            content = etree.HTML(html)

            # xpath解析得到当页商品评论数量
            commentnums = content.xpath(
                    '//span[@class="dpProductDetailB00WPRE0HA"]/span[@class="a-size-small"]/a[@class="a-link-normal"]/text()')

            # 原文117 customer reviews
            # 剔除 customer reviews
            temp = commentnums[0]
            commentnum[name] = temp.replace(" customer reviews", "").strip()

    return commentnum


# 开启多线程
# 以5个线程跑解析函数getcommentnum
def threadingcommentnum():
    pool = ThreadPoolExecutor(5)
    for name in openpath():
        pool.submit(getcommentnum, name)
    return pool.submit(getcommentnum, name).result()


## 合并字典输出
detailall = {}


def mergedetail():
    star = threadingstar()
    price = threadingprice()
    rank2 = threadingrank2()
    soldby = threadingsoldby()
    FBAs = threadingFBA()
    firstcommenttime = threadingfirstcommenttime()
    commentnum = threadingcommentnum()
    # 根据每个独立的键来合并
    for i in threadingstar():
        print(i)
        detailall[i] = [star[i], price[i], rank2[i], firstcommenttime[i], commentnum[i], soldby[i], FBAs[i]]
    return detailall


if __name__ == '__main__':
    print(mergedetail())
