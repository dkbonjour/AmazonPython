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


# 列表页
def phonelistparse(content):
    soup = BeautifulSoup(content, 'html.parser')  # 开始解析
    items = soup.find_all('div', attrs={"id": "pg"})
    itemlist = {}
    for i in items:
        j = i.find_all("li")
        for jj in j:
            try:
                smallrank = int(jj["id"].replace("ranked-result-", "")) + 1
                asin = jj.find("a")["data-asin"]
                url = "https://www.amazon.com/dp/" + asin
                try:
                    img = jj.find("img")["data-src"]
                except:
                    # logger.error("图片解析出错")
                    img = ""
                try:
                    title = jj.find("h5").get_text()
                    if len(title) > 240:
                        title = title[0:220]
                except:
                    # logger.error("价格解析出错")
                    title = "no title"
                pricetemp = jj.find_all("div", attrs={"class": "a-row"})
                price = "no avaible"
                for i in pricetemp:
                    if "$" in i.get_text():
                        price = i.get_text().strip()
                        break

                itemlist[asin] = [smallrank, url, img, title, price]
            except Exception as e:
                logger.error(e, exc_info=1)
    if itemlist == {} or not itemlist:
        items = soup.find_all('div', attrs={"class": "zg_itemImmersion"})
        for item in items:
            try:
                temp = BeautifulSoup(str(item), 'html.parser')
                rank = temp.find('span', attrs={"class": "zg_rankNumber"}).string
                rank = rank.replace(".", "").replace(",", "")
                link = temp.find('div', attrs={"class": "zg_title"}).a["href"]
                try:
                    asin = link.strip().split("/dp/")[1].split("/")[0]
                except:
                    continue
                title = temp.find('div', attrs={"class": "zg_title"}).a.string
                title = title.replace(",", "")
                itemlist[asin] = [rank, "https://www.amazon.com/dp/" + asin, "", title, ""]
            except:
                pass
    return itemlist


# 详情页
def phonedetailparse(content):
    # {
    #     "commentime": "December 16- 2011",
    #     "commentnum": 15,
    #     "rank": 10750,
    #     "score": 4.1,
    #     "shipby": "FBA",
    #     "soldby": "Amazon.com",
    # }
    returnmap = {"rank": -1, "score": -1, "commentnum": -1, "commenttime": "", "shipby": "", "soldby": "No sold"}
    soup = BeautifulSoup(content, 'html.parser')  # 开始解析
    ul = soup.find("ul", attrs={"id": "productDetails_detailBullets_sections"})
    if ul == None or not ul:
        ul = soup.find("table", attrs={"id": "productDetails_techSpec_section_1"})
    if ul:
        infolist = []
        info = str(ul.get_text()).splitlines()
        for i in info:
            if i.strip():
                infolist.append(i)
        # print(infolist)
        for i in range(len(infolist)):
            if 'Customer Review'.lower() in infolist[i].lower():
                try:
                    returnmap["score"] = float(infolist[i + 1].split(" ")[0])
                except:
                    pass
                try:
                    returnmap["commentnum"] = int(infolist[i + 2].replace(",", "").replace(".", "").split("Review")[0])
                except:
                    pass
            if "Best Sellers Rank".lower() in infolist[i].lower():
                try:
                    returnmap["rank"] = int(infolist[i + 1].replace(",", "").replace(".", ""))
                except:
                    pass
            if "Date First Available".lower() in infolist[i].lower():
                try:
                    returnmap["commenttime"] = infolist[i + 1]
                except:
                    pass
        try:
            sold = soup.find("div", attrs={"id": "shipsFromSoldBy_feature_div"})
            soldtext = sold.get_text()
            if "Ships from and sold by Amazon.com".lower() in soldtext.lower():
                returnmap["shipby"] = "FBA"
                returnmap["soldby"] = "Amazon.com"
            elif "Fulfilled by Amazon".lower() in soldtext.lower():
                returnmap["shipby"] = "FBA"
            else:
                linka = sold.find("a")
                try:
                    returnmap["shipby"] = linka.get_text()
                    returnmap["soldby"] = linka["href"].split("seller=")[1].split("&")[0]
                except:
                    pass
        except:
            pass
    # rubbish
    else:
        raise Exception("详情页故障")
    return returnmap


def testdetail():
    a = time.clock()
    filepath = tool.log.BASE_DIR + "/data/phonedetail1/"
    filepath1 = tool.log.BASE_DIR + "/data/phonedetail1/"
    createjia(filepath)
    createjia(filepath1)
    # G:\smartdo\data\errordetail\20161018-135309.html
    files = listfiles(filepath, ".html")
    for i in files:
        temp = filepath + i
        with open(temp, "rb") as f:
            source = f.read()
            content = source.decode("utf-8", "ignore")
            try:
                phonedetailparse(content)
            except Exception as e:
                # raise
                # with open(filepath1 + i, "wb") as ff:
                #     ff.write(source)
                print(i)

    b = time.clock()
    print('运行时间：' + timetochina(b - a))


def testlist():
    a = time.clock()
    filepath = tool.log.BASE_DIR + "/data/phonelist/"
    # G:\smartdo\data\errordetail\20161018-135309.html
    files = listfiles(filepath, ".html")
    for i in files:
        temp = filepath + i
        with open(temp, "rb") as f:
            content = f.read().decode("utf-8", "ignore")
            try:
                phonelistparse(content)
            except:
                print(i)
    b = time.clock()
    print('运行时间：' + timetochina(b - a))


if __name__ == '__main__':
    # testlist()
    testdetail()
