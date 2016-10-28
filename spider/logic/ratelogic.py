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
loggers = logging.getLogger("smart")

DATA_DIR = getconfig()["datadir"]


# 单类目抓取
def unitlogic(url, mysqlconfig):
    global DATA_DIR
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

    # 2016/Appl/20160606/
    todays = todaystring(3)
    year = todaystring(1)
    db = getconfig()["dbprefix"] + db
    if not dbexist(db, id, todays):
        return

    if getconfig()["ipinmysql"]:
        where = "mysql"
    else:
        where = "local"

    keepdir = createjia(DATA_DIR + "/data/items/" + year + "/" + bigpname.replace(" ", "") + "/" + todays + "/" + id)

    detaildir = createjia(DATA_DIR + "/data/detail/" + year + "/" + bigpname.replace(" ", "") + "/" + todays + "/" + id)

    detailall = {}

    # 列表頁抓完？
    finish = listfiles(keepdir, ".jinhan")
    pagefinish = False
    if len(finish) >= 1:
        pagefinish = True

    # 重試多次仍然抓不到頁面？
    retryhappen = False
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
            # 如果不存在文件且已經完成，證明頁數不足
            if pagefinish:
                break
            logger.warning("抓取:" + id + "(" + str(i + 1) + ")-" + bigpname + ":" + catchname + "(" + str(
                    level) + ") --" + catchurl)
            # 构造页数
            # ?_encoding=UTF8&pg=1&ajax=1   3个商品
            # ?_encoding=UTF8&pg=1&ajax=1&isAboveTheFold=0 17个商品
            # https://www.amazon.com/Best-Sellers-Clothing/zgbs/apparel/ref=zg_bs_apparel_pg_5?_encoding=UTF8&pg=5&ajax=1
            # Referer:https://www.amazon.com/gp/bestsellers/apparel/ref=pd_zg_hrsr_a_1_1
            # Referer:https://www.amazon.com/gp/bestsellers/apparel/ref=pd_zg_hrsr_a_1_1
            # X-Requested-With:XMLHttpRequest
            items3 = "/ref=zg_bs_apparel_pg_"+str(i + 1)+"?_encoding=UTF8&ajax=1&pg=" + str(i + 1)
            items17 = "/ref=zg_bs_apparel_pg_"+str(i + 1)+"?_encoding=UTF8&&isAboveTheFold=0&ajax=1&pg=" + str(i + 1)
            listheader = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                # "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Accept-Language": "en-US;q=0.8,en;q=0.5",
                "Upgrade-Insecure-Requests": "1",
                # 'Referer': 'https://www.amazon.com/',
                'Host': 'www.amazon.com'
            }
            content3 = ratedownload(url=catchurl + items3, where=where, config=mysqlconfig,header=listheader)
            content17 = ratedownload(url=catchurl + items17, where=where, config=mysqlconfig,header=listheader)
            if content3 == 0 or content17 == 0:
                break
            if content3 == None:
                retryhappen = True
                continue
            if content17 == None:
                retryhappen = True
                continue
            try:
                # {'91':['91', 'https://www.amazon.com/dp/B003Z968T0', 'WhisperKOOL® Platinum Split System 80...']}
                temp3 = rateparse(content3)
                temp17 = rateparse(content17)
                if temp3 == {} and temp17 == {}:
                    continue
                else:
                    with open(itempath, "wb") as f:
                        for i in sorted(temp3.keys()):
                            detailall[i] = temp3[i][1]
                            f.write((",".join(temp3[i]) + "\n").encode("utf-8"))
                        for j in sorted(temp17.keys()):
                            detailall[i] = temp17[j][1]
                            f.write((",".join(temp17[j]) + "\n").encode("utf-8"))
            except Exception as err:
                logger.error("解析列表頁錯誤：" + catchurl + ":" + str(i + 1))
                logger.error(err, exc_info=1)
                pass
    if retryhappen == False and pagefinish == False:
        with open(keepdir + "/ko.jinhan", "wt") as f:
            f.write("1")

    for rank in detailall:
        detailname = rank + "-" + detailall[rank]
        rankeep = detaildir + "/" + detailname
        if fileexsit(rankeep + ".md"):
            loggers.error("存在!" + rankeep)
            continue
        if fileexsit(rankeep + ".emd"):
            loggers.error("存在(页面找不到）)!" + rankeep)
            continue
        url = "https://www.amazon.com/dp/" + detailall[rank]

        # TODO
        # 本地文件不保存
        if fileexsit(rankeep + ".html"):
            with open(rankeep + ".html", "rb") as ff:
                detailpage = ff.read()
        else:
            detailheader = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                # "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Accept-Language": "en-US;q=0.8,en;q=0.5",
                "Upgrade-Insecure-Requests": "1",
                # "Cache-Control":"max-age=0",
                # 'Referer': 'https://www.amazon.com/',
                'Host': 'www.amazon.com'
            }
            detailpage = ratedownload(url=url, where=where, config=mysqlconfig,header=detailheader)
            if detailpage == None:
                continue
            if detailpage == 0:
                with open(rankeep + ".emd", "wt") as f:
                    f.write("1")
                continue
            else:
                if getconfig()["localkeep"]:
                    with open(rankeep + ".html", "wb") as f:
                        f.write(detailpage)
        try:
            pinfo = pinfoparse(detailpage.decode("utf-8", "ignore"))
        except:
            logger.error("解析詳情頁出錯:" + url)
            continue
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

    # 成功
    logger.error(todays + "|" + bigpname + "|" + db + ":" + id + " completed")


# 单进程抓取
def processlogic(processurls, mysqlconfig):
    logger.debug(processurls)
    for url in processurls:
        try:
            # url: ('1-1', 'https://www.amazon.com/Best-Sellers-Appliances-Cooktops/zgbs/appliances/3741261/ref=zg_bs_nav_la_1_la/161-2441050-2846244', 'Cooktops', 2, 5, '1', '1', 'Appliances')
            unitlogic(url, mysqlconfig)
            if getconfig("urlstop"):
                logger.error("大睡眠！" + str(getconfig()["urlstoptime"]) + "秒")
                time.sleep(getconfig()["urlstoptime"])
        except Exception as err:
            logger.error("單進程抓錯異常：")
            logger.error(url)
            logger.error(err, exc_info=1)


# 多进程抓取
def ratelogic(category=["Appliances"], processnum=1, limitnum=20000):
    allconfig = getconfig()
    try:
        mysqlconfig = allconfig["basedb"]
    except:
        raise Exception("基础数据库配置出错")
    urls = list(usaurl(config=mysqlconfig, category=category, limitnum=limitnum))
    tasklist = devidelist(urls, processnum)
    with ProcessPoolExecutor(max_workers=processnum) as e:
        for task in tasklist:
            # TODO
            # 任务不能同时进行
            time.sleep(random.randint(0, 3))

            ## TODO
            ## IP需要切分
            e.submit(processlogic, tasklist[task], mysqlconfig)


if __name__ == "__main__":
    a = time.clock()
    changeconfig("catchbywhich", "bigpname")
    category = ["Appliances", "Arts_ Crafts & Sewing"]
    processnum = 2
    ratelogic(category, processnum, 6)
    b = time.clock()
    print('运行时间：' + timetochina(b - a))
