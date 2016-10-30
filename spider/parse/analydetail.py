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


def saveerror(content):
    createjia(tool.log.BASE_DIR + "/data/errordetail")
    k = tool.log.BASE_DIR + "/data/errordetail/" + todaystring(6) + ".html"
    with open(k, "wb") as f:
        f.write(content.encode("utf-8"))
    logger.error("排名强制标记:" + k)


# 正则大类排名
def getrank2reg(string):
    # 这里正则只是选取1-5个字段，然后就匹配 in 。  (#######I live in)
    # 防止抓取到其他的东西，一定要用{1,5}
    reg = r'#(.{1,8}) in '
    all = re.compile(reg)
    alllist = re.findall(all, string)
    rank = int(alllist[0].replace(",", ""))
    return rank


# 评论数 打分 评分
# id=productDetails_detailBullets_sections1
def pinfoparse(content):
    # 返回的结果
    returnlist = {}
    soup = BeautifulSoup(content, 'html.parser')  # 开始解析
    temp = soup.find('table', attrs={"id": "productDetails_detailBullets_sections1"})
    if temp == None:
        temp = soup.find("li", attrs={"id": "SalesRank"})
    if temp == None:
        temp = soup.find("tr", attrs={"id": "SalesRank"})
    # 排名
    if temp:
        try:
            text = temp.get_text().strip()
            returnlist["rank"] = getrank2reg(text)
        except Exception as err:
            saveerror(content)
            logger.error(err, exc_info=1)
            returnlist["rank"] = -1
    else:
        saveerror(content)
        returnlist["rank"] = -1

    # 缩小范围
    header = soup.find("div", attrs={"id": "centerCol"})
    if header == None:
        header = soup.find("div", attrs={"id": "leftCol"})
    if header == None:
        header = soup.find("div", attrs={"id": "ppdBuyBox"})
    if header == None:
        header = soup.find("div", attrs={"id": "center-col"})
    if header == None:
        header = soup
        # return

    # 标题
    title = header.find("span", attrs={"id": "productTitle"})
    if title == None:
        title = header.find("span", attrs={"id": "btAsinTitle"})
    if title == None:
        title = soup.find("span", attrs={"id": "fineArtTitle"})
    if title == None:
        title = soup.find("span", attrs={"id": "productTitle"})
    try:
        returnlist["title"] = title.get_text().strip().replace(",", "-")
    except Exception as err:
        #logger.error(err, exc_info=1)
        returnlist["title"] = "No title"

    # 评论数
    hascomment = soup.find("span", attrs={"id": "dp-no-customer-review-yet"})
    if hascomment == None:
        hascomment = soup.find("span", attrs={"id": "noReviewYetText"})
    if hascomment != None:
        returnlist["commentnum"] = 0
        returnlist["commenttime"] = ""
    else:
        commentnum = header.find("span", attrs={"class": "a-size-small"})
        commenttime = ""
        if commentnum == None:
            commentnum = header.find("span", attrs={"id": "acrCustomerReviewText"})
        if commentnum == None:
            try:
                returnlist["commentnum"] = int(soup.find("div", attrs={"id": "summaryStars"}).get_text().split("stars")[1].replace('"',"").strip().replace(",", ""))
            except Exception as err:
                #logger.error(err, exc_info=1)
                returnlist["commentnum"] = -1
        else:
            if commentnum:
                try:
                    # 1个人没有复数
                    returnlist["commentnum"] = int(commentnum.get_text().strip().replace(" customer review", "").replace("s", "").replace(",", ""))
                except Exception as err:
                    try:
                        returnlist["commentnum"]=int(soup.find("span",attrs={"data-hook":"total-review-count"}).get_text().strip().replace(",", ""))
                    except Exception as err:
                        try:
                            returnlist["commentnum"] = int(soup.find("div", attrs={"id": "summaryStars"}).get_text().split("stars")[1].replace('"',"").replace(",", ""))
                        except Exception as err:
                            #logger.error(err, exc_info=1)
                            returnlist["commentnum"] = -1
                            commenttime = "None"

            else:
                try:
                    commentnum = soup.find("span", attrs={"id": "acrCustomerReviewText"})
                    returnlist["commentnum"] = int(commentnum.get_text().strip().replace(" customer review", "").replace("s", "").replace(",",""))
                except Exception as err:
                    #logger.error(err, exc_info=1)
                    returnlist["commentnum"] = -1
                    commenttime = "None"

        # 评论时间
        if commenttime == "None":
            returnlist["commenttime"] = commenttime
        else:
            # revMH
            small = ""
            timetemp = soup.find("div", attrs={"id": "revMHRL"})
            if timetemp == None:
                pass
            else:
                element = timetemp.findAll("span", attrs={"class", "a-color-secondary"})
                smallyear = 3000
                for i in element:
                    try:
                        j = i.get_text().strip()
                        if " on " in j:
                            tempyoukonw = int(j.split(" on ")[1].strip().split(",")[1].strip())
                            # print(tempyoukonw)
                            if tempyoukonw < smallyear:
                                small = j.split("on ")[1]
                                smallyear = tempyoukonw
                    except Exception as err:
                        pass#logger.error(err, exc_info=1)
                        #logger.error(err, exc_info=1)
            returnlist["commenttime"] = small.replace(",", "-").strip()
            if len(returnlist["commenttime"]) > 30:
                returnlist["commenttime"] = ""

    # 打分
    if hascomment != None:
        returnlist["score"] = -1
    else:
        dafen = header.find("span", attrs={"id": "acrPopover"})
        if dafen == None:
            dafen = header.find("i", attrs={"class": "a-icon-star"})

        if dafen:
            try:
                dafentemp = float(dafen["title"].replace(" out of 5 stars", ""))
                returnlist["score"] = dafentemp
            except Exception as err:
                try:
                    dafentemp = float(dafen.get_text().strip().replace(" out of 5 stars", ""))
                    returnlist["score"] = dafentemp
                except Exception as err:
                    #logger.error(err, exc_info=1)
                    returnlist["score"] = -1
        else:
            try:
                # <div id="averageCustomerReviewRating" class="txtnormal clearboth">4.0 out of 5 stars</div>
                dafen = soup.find("div", attrs={"id": "averageCustomerReviewRating"})
                dafentemp = float(dafen.get_text().strip().replace(" out of 5 stars", ""))
                returnlist["score"] = dafentemp
            except:
                try:
                    dafentemp = float(
                            soup.find("div", attrs={"id": "summaryStars"}).find("i").get_text().strip().replace(" out of 5 stars", ""))
                    returnlist["score"] = dafentemp
                except Exception as err:
                    #logger.error(err, exc_info=1)
                    returnlist["score"] = -1

    # 价格
    price = header.find("span", attrs={"id": "priceblock_ourprice"})
    if price == None:
        price = header.find("strong", attrs={"class": "priceLarge"})

    if price:
        try:
            returnlist["price"] = float(price.get_text().strip().replace("$", "").replace(",",""))
        except:
            try:
                returnlist["price"] = float(price.get_text().split("-")[1].strip().replace("$", "").replace(",",""))
            except Exception as err:
                try:
                    try:
                        e1=soup.find("span",attrs={"id":"priceblock_usedprice"}).find("span",attrs={"class","buyingPrice"}).get_text().strip()
                        returnlist["price"]=float(e1.replace("$", "").replace(",",""))
                    except Exception as err:
                        e1=soup.find("span",attrs={"id":"priceblock_ourprice"}).find("span",attrs={"class","buyingPrice"}).get_text().strip()
                        returnlist["price"]=float(e1.replace("$", "").replace(",",""))
                except Exception as err:
                    #logger.error(err, exc_info=1)
                    returnlist["price"] = -1

    else:
        try:
            price = soup.find("span", attrs={"id": "priceblock_saleprice"})
            returnlist["price"] = price.get_text().strip().replace("$", "").replace(",","")
        except:
            try:
                price = soup.find("span", attrs={"id": "priceblock_ourprice"})
                returnlist["price"] = float(price.get_text().strip().replace("$", "").replace(",",""))
            except Exception as err:
                pass
                # logger.error(err, exc_info=1)
                returnlist["price"] = -1

    # Sold by # 全局
    # print(header)
    # exit()
    soldby = soup.find("div", attrs={"id": "merchant-info"})
    if soldby == None:
        soldby = soup.find("span", attrs={"id": "merchant-info"})
    s1 = "No sold"
    s2 = "No ship"
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
            s1 = geturlattr(soldby.find("a")["href"])["seller"]
    except Exception as err:
        pass
        # logger.error(err, exc_info=1)
    returnlist["soldby"] = s1
    returnlist["shipby"] = s2

    return returnlist


if __name__ == '__main__':
    a = time.clock()
    filepath = tool.log.BASE_DIR + "/data/errortest/"

    # G:\smartdo\data\errordetail\20161018-135309.html
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
