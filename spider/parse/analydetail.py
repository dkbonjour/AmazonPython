# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
from lxml import etree
import re
from spider.logic.urllogic import *
import tool.log

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)

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


# 评论数 打分 评分
# id=productDetails_detailBullets_sections1
def pinfoparse(content):
    returnlist = {}
    soup = BeautifulSoup(content, 'html.parser')  # 开始解析

    temp = soup.find('table', attrs={"id": "productDetails_detailBullets_sections1"})
    # SalesRank
    try:
        try:
            text = temp.get_text()
        except:
            text = soup.find("li", attrs={"id": "SalesRank"}).get_text()
        returnlist["rank"] = getrank2reg(text)
    except Exception as err:
        logger.info(err, exc_info=1)
        returnlist["rank"] = -1

    header = soup.find("div", attrs={"id": "centerCol"})
    if header == None:
        header = soup.find("div", attrs={"id": "leftCol"})
    if header == None:
        header = soup.find("div", attrs={"id": "ppdBuyBox"})
    if header == None:
        logger.error("强制标记：" + content)
    title = header.find("span", attrs={"id": "productTitle"})
    dafen = header.find("span", attrs={"id": "acrPopover"})
    commentnum = header.find("span", attrs={"id": "acrCustomerReviewText"})
    price = header.find("span", attrs={"id": "priceblock_ourprice"})

    soldby = header.find("div", attrs={"id": "merchant-info"})
    commenttime = ""

    # 标题
    try:
        returnlist["title"] = title.get_text().strip().replace(",", "-")
    except Exception as err:
        logger.info(err, exc_info=1)
        returnlist["title"] = ""
    # 打分
    try:
        dafentemp = float(dafen["title"].replace(" out of 5 stars", ""))
        returnlist["score"] = dafentemp

    except Exception as err:
        logger.info(err, exc_info=1)
        returnlist["score"] = -1
    # 评论数
    try:
        # 1个人没有复数
        returnlist["commentnum"] = int(commentnum.get_text().replace(" customer review", "").replace("s", ""))
    except Exception as err:
        logger.info(err, exc_info=1)
        returnlist["commentnum"] = -1
        commenttime = "None"
    # 价格
    try:
        returnlist["price"] = float(price.get_text().replace("$", ""))
    except Exception as err:
        logger.info(err, exc_info=1)
        returnlist["price"] = -1

        # sold by who and FBA
        # Sold by Beadnova and Fulfilled by Amazon
        # Ships from and sold by CleverDelights
        # Ships from and sold by Amazon.com.
    s1 = ""
    s2 = ""
    try:
        soldtemp = soldby.get_text().strip()

        if "Fulfilled by Amazon" in soldtemp:
            s2 = "FBA"
        if "sold by Amazon.com" in soldtemp:
            s2 = "FBA"
            s1 = "Amazon.com"
        else:
            # https://www.amazon.com/sp?seller=A1RDLBSMJ0S327
            # /gp/help/seller/at-a-glance.html/ref=dp_merchant_link?ie=UTF8&seller=AJ11J3FSAZ6XV&isAmazonFulfilled=1
            try:
                s1 = geturlattr(soldby.find("a")["href"])["seller"]
            except:
                pass
    except Exception as err:
        logger.info(err, exc_info=1)
    returnlist["soldby"] = s1
    returnlist["shipby"] = s2

    if commenttime == "None":
        returnlist["commenttime"] = commenttime
    else:
        # revMH
        small = ""
        timetemp = soup.find("div", attrs={"id": "revMH"})
        if timetemp == None:
            pass
        else:
            element = timetemp.findAll("span", attrs={"class", "a-color-secondary"})
            smallyear = 3000
            for i in element:
                try:
                    j = i.get_text().strip()
                    if "on" in j:
                        tempyoukonw = int(j.split("on ")[1].split(",")[1])
                        # print(tempyoukonw)
                        if tempyoukonw < smallyear:
                            small = j.split("on ")[1]
                            smallyear = tempyoukonw
                except:
                    pass
        returnlist["commenttime"] = small.replace(",", "-")
    return returnlist


# 正则大类排名
def getrank2reg(string):
    # 这里正则只是选取1-5个字段，然后就匹配 in 。  (#######I live in)
    # 防止抓取到其他的东西，一定要用{1,5}
    reg = r'#(.{1,8}) in '
    all = re.compile(reg)
    alllist = re.findall(all, string)
    try:
        # 加强版
        rank = int(alllist[0].replace(",", ""))
        return rank
    except:
        pass
    return -1


if __name__ == '__main__':
    a = time.clock()
    filepath = tool.log.BASE_DIR + "/data/detail/2016/Arts_ Crafts & Sewing/20161017/3-1-10-1-1/"
    files = listfiles(filepath, ".html")
    for i in files:
        print(i)
        temp = filepath + i
        with open(temp, "rb") as f:
            content = f.read().decode("utf-8", "ignore")
            # print(content)
        print(pinfoparse(content))
    b = time.clock()
    print('运行时间：' + timetochina(b - a))
