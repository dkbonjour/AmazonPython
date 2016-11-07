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


def savephoneerror(content):
    createjia(tool.log.BASE_DIR + "/data/merror")
    k = tool.log.BASE_DIR + "/data/merror/" + todaystring(6) + ".html"
    with open(k, "wb") as f:
        f.write(content.encode("utf-8"))
    logger.error("phone排名强制标记:" + k)


# 列表页
def phonelistparse(content):
    soup = BeautifulSoup(content, 'html.parser')  # 开始解析
    items = soup.find_all('div', attrs={"id": "pg"})
    itemlist = {}
    for i in items:
        if "Amazon.com Full Site" in soup.get_text():
            pass
        else:
            break
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
        if "Amazon.com Full Site" in soup.get_text():
            return itemlist, True
        items = soup.find_all('div', attrs={"class": "zg_itemImmersion"})
        for item in items:
            try:
                temp = BeautifulSoup(str(item), 'html.parser')
                rank = temp.find('span', attrs={"class": "zg_rankNumber"}).string
                rank = rank.replace(".", "").replace(",", "").strip()
                try:
                    ## p13n-asin
                    link = temp.find('div', attrs={"class": "zg_title"})
                    if not link or link==None:
                        link=temp.find('div', attrs={"class": "p13n-asin"})
                    link = link.find("a",attrs={"class":"a-link-normal"})["href"].strip()
                    asin = link.strip().split("/dp/")[1].split("/")[0]
                except Exception as e:
                    # logger.error(e, exc_info=1)
                    continue
                try:
                    img = temp.find("img")["src"].strip()
                except:
                    img = ""
                try:
                    price = temp.find("div", attrs={"class": "zg_price"}).get_text().strip()
                except:
                    try:
                        price=temp.find("span",attrs={"class":"a-color-price"}).get_text().strip()
                    except Exception as e:
                        # logger.error(e, exc_info=1)
                        price = ""
                try:
                    title = temp.find('div', attrs={"class": "zg_title"})
                    if not title or title==None:
                        title=temp.find('div', attrs={"class": "p13n-asin"})
                    # print(title)
                    title=title.find("a",attrs={"class":"a-link-normal"}).get_text()
                    title = title.replace(",", "").strip()
                except Exception as e:
                    # logger.error(e, exc_info=1)
                    title = ""
                itemlist[asin] = [rank, "https://www.amazon.com/dp/" + asin, img, title, price]
            except Exception as e:
                logger.error(e, exc_info=1)
        return itemlist, False
    return itemlist, True


## 额外补充的
def phonetopclistparse(content):
    soup = BeautifulSoup(content, 'html.parser')  # 开始解析
    itemlist = {}
    items = soup.find_all('div', attrs={"class": "zg_itemImmersion"})
    for item in items:
        try:
            temp = BeautifulSoup(str(item), 'html.parser')
            rank = temp.find('span', attrs={"class": "zg_rankNumber"}).string
            rank = rank.replace(".", "").replace(",", "").strip()
            try:
                ## p13n-asin
                link = temp.find('div', attrs={"class": "zg_title"})
                if not link or link==None:
                    link=temp.find('div', attrs={"class": "p13n-asin"})
                link = link.find("a",attrs={"class":"a-link-normal"})["href"].strip()
                asin = link.strip().split("/dp/")[1].split("/")[0]
            except Exception as e:
                # logger.error(e, exc_info=1)
                continue
            try:
                img = temp.find("img")["src"].strip()
            except:
                img = ""
            try:
                price = temp.find("div", attrs={"class": "zg_price"}).get_text().strip()
            except:
                try:
                    price=temp.find("span",attrs={"class":"a-color-price"}).get_text().strip()
                except Exception as e:
                    # logger.error(e, exc_info=1)
                    price = ""
            try:
                title = temp.find('div', attrs={"class": "zg_title"})
                if not title or title==None:
                    title=temp.find('div', attrs={"class": "p13n-asin"})
                # print(title)
                title=title.find("a",attrs={"class":"a-link-normal"}).get_text()
                title = title.replace(",", "").strip()
            except Exception as e:
                # logger.error(e, exc_info=1)
                title = ""
            itemlist[asin] = [rank, "https://www.amazon.com/dp/" + asin, img, title, price]
        except Exception as e:
            logger.error(e, exc_info=1)
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
    if "Amazon.com Full Site" in soup.get_text():
        pass
    else:
        raise Exception("不是手机端详情页")
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
        except Exception as e:
            logger.error(e, exc_info=1)
            pass
    # rubbish
    else:
        raise Exception("手机详情页故障")
    if returnmap["rank"] == -1:
        savephoneerror(content)
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
                return phonelistparse(content)
            except:
                print(i)
    b = time.clock()
    print('运行时间：' + timetochina(b - a))


if __name__ == '__main__':
    print(testlist())
    # testdetail()
