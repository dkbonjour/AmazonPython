# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/14.
# 功能:
#  
import tool.log
import logging
from action.url import *
from config.config import *
from tool.jfile.file import *
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from spider.download.ratedownload import *
from spider.parse.analydetail import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)

# 单类目抓取
def unitlogic(url, mysqlconfig):
    # url: ('1-1', 'https://www.amazon.com/Best-Sellers-Appliances-Cooktops/zgbs/appliances/3741261/ref=zg_bs_nav_la_1_la/161-2441050-2846244', 'Cooktops', 2, 5, '1', '1', 'Appliances')

    # 抓取的类目URL
    catchurl = url[1]
    # 类目名
    catchname = url[2]
    # 类目ID
    id = url[0]
    # 大类名
    bigpname = url[4]
    # 页数
    page = url[3]
    # 级别
    level = url[5]

    # 数据库
    db = url[6]

    if not dbexist(db, id):
        return

    # 2016/Appl/20160606/
    todays = todaystring(3)
    keepdir = createjia(
            tool.log.DATA_DIR + "/data/items/" + todaystring(1) + "/" + bigpname + "/" + todays + "/" + id)

    detaildir = createjia(
            tool.log.DATA_DIR + "/data/detail/" + todaystring(1) + "/" + bigpname + "/" + todays+ "/" + id)

    detailall = {}

    for i in range(min(page, 5)):
        itempath = keepdir + "/" + str(i + 1) + ".md"
        if fileexsit(itempath):
            logger.warning("已存在:" + id + "(" + str(i + 1) + ")-" + bigpname + ":" + catchname + "(" + str(
                    level) + ") --" + catchurl)
            temp = readfilelist(itempath)
            for i in temp:
                temptemp = i.split(",")
                detailall[temptemp[0]] = temptemp[1]
            continue
        else:
            logger.warning("抓取:" + id + "(" + str(i + 1) + ")-" + bigpname + ":" + catchname + "(" + str(
                    level) + ") --" + catchurl)
        # 构造页数
        # ?_encoding=UTF8&pg=1&ajax=1   3个商品
        # ?_encoding=UTF8&pg=1&ajax=1&isAboveTheFold=0 17个商品
        items3 = "?_encoding=UTF8&ajax=1&pg=" + str(i + 1)
        items17 = "?_encoding=UTF8&&isAboveTheFold=0&ajax=1&pg=" + str(i + 1)
        content3 = ratedownload(url=catchurl + items3, where="mysql", config=mysqlconfig)
        content17 = ratedownload(url=catchurl + items17, where="mysql", config=mysqlconfig)
        if content3 == None:
            continue
        if content17 == None:
            continue
        try:
            # {'91':['91', 'https://www.amazon.com/dp/B003Z968T0', 'WhisperKOOL® Platinum Split System 80...']}
            temp3 = rateparse(content3)
            temp17 = rateparse(content17)
            with open(itempath, "wb") as f:
                for i in sorted(temp3.keys()):
                    detailall[i] = temp3[i][1]
                    f.write((",".join(temp3[i]) + "\n").encode("utf-8"))
                for j in sorted(temp17.keys()):
                    detailall[i] = temp17[j][1]
                    f.write((",".join(temp17[j]) + "\n").encode("utf-8"))
        except Exception as err:
            logging.error(err, exc_info=1)
            pass
    for rank in detailall:
        detailname = rank + "-" + detailall[rank]
        rankeep = detaildir + "/" + detailname
        if fileexsit(rankeep + ".md"):
            continue
        url = "https://www.amazon.com/dp/" + detailall[rank]
        if fileexsit(rankeep + ".html"):
            with open(rankeep + ".html", "rb") as ff:
                detailpage = ff.read()
        else:
            detailpage = ratedownload(url=url, where="mysql", config=mysqlconfig)
            if detailpage == None:
                continue
            else:
                with open(rankeep + ".html", "wb") as f:
                    f.write(detailpage)
        pinfo = pinfoparse(detailpage.decode("utf-8", "ignore"))
        try:
            pinfo["smallrank"] = int(rank)
        except:
            pinfo["smallrank"] = -1
        pinfo["asin"] = detailall[rank]
        pinfo["url"] = url
        pinfo["name"] = catchname
        pinfo["bigname"] = bigpname
        pinfo["id"] = todays + "-" + detailname
        if insertpmysql(pinfo, db, id):
            with open(rankeep + ".md", "wb") as f:
                f.write(objectToString(pinfo).encode("utf-8"))


# 单进程抓取
def processlogic(processurls, mysqlconfig):
    logger.debug(processurls)
    for url in processurls:
        try:
            # url: ('1-1', 'https://www.amazon.com/Best-Sellers-Appliances-Cooktops/zgbs/appliances/3741261/ref=zg_bs_nav_la_1_la/161-2441050-2846244', 'Cooktops', 2, 5, '1', '1', 'Appliances')
            unitlogic(url, mysqlconfig)
        except Exception as err:
            logging.error(err, exc_info=1)


# 多进程抓取
def ratelogic(category=["Appliances"], processnum=1, limitnum="20000"):
    allconfig = getconfig()
    try:
        mysqlconfig = allconfig["basedb"]
    except:
        raise Exception("基础数据库配置出错")
    urls = list(usaurl(config=mysqlconfig, category=category, limitnum=limitnum))
    tasklist = devidelist(urls, processnum)
    with ProcessPoolExecutor(max_workers=processnum) as e:
        for task in tasklist:
            e.submit(processlogic, tasklist[task], mysqlconfig)


if __name__ == "__main__":
    a = time.clock()
    category = ["Appliances", "Arts_ Crafts & Sewing"]
    processnum = 5
    ratelogic(category, processnum, "6")
    b = time.clock()
    print('运行时间：' + timetochina(b - a))
