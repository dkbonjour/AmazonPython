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

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


# 单类目抓取
def unitlogic(url):
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

    # 2016/Appl/20160606/
    keepdir = createjia(tool.log.BASE_DIR + "/data/items/" + todaystring(1) + "/" + bigpname + "/" + todaystring(3) + "/" + id)
    for i in range(min(page, 5)):
        itempath = keepdir+"/"+str(i+1)+".md"
        if fileexsit(itempath):
            logger.warning("已存在:" + id + "(" + str(i+1) + ")-" + bigpname + ":" + catchname + "(" + str(level) + ") --" + catchurl)
            continue
        else:
            logger.warning("抓取:" + id + "(" + str(i+1) + ")-" + bigpname + ":" + catchname + "(" + str(level) + ") --" + catchurl)
        # 构造页数
        # ?_encoding=UTF8&pg=1&ajax=1   3个商品
        # ?_encoding=UTF8&pg=1&ajax=1&isAboveTheFold=0 17个商品
        items3 = "?_encoding=UTF8&ajax=1&pg=" + str(i + 1)
        items17 = "?_encoding=UTF8&&isAboveTheFold=0&ajax=1&pg=" + str(i + 1)
        content3 = ratedownload(catchurl + items3)
        content17 = ratedownload(catchurl + items17)
        if content3==None:
            continue
        if content17==None:
            continue
        try:
            temp3 = rateparse(content3)
            temp17 = rateparse(content17)
            with open(itempath,"wb") as f:
                for i in sorted(temp3.keys()):
                    f.write((",".join(temp3[i])+"\n").encode("utf-8"))
                for j in sorted(temp17.keys()):
                    f.write((",".join(temp17[j])+"\n").encode("utf-8"))
        except Exception as err:
            logging.error(err, exc_info=1)
            pass



# 单进程抓取
def processlogic(processurls):
    logger.debug(processurls)
    for url in processurls:
        try:
            unitlogic(url)
        except Exception as err:
            logging.error(err, exc_info=1)


# 多进程抓取
def ratelogic(category=["Appliances"], processnum=1):
    allconfig = getconfig()
    try:
        config = allconfig["basedb"]
    except:
        raise Exception("数据库配置出错")
    urls = list(usaurl(config, category))
    tasklist = devidelist(urls, processnum)
    with ProcessPoolExecutor(max_workers=processnum) as e:
        for task in tasklist:
            e.submit(processlogic, tasklist[task])


if __name__ == "__main__":
    category = ["Appliances"]
    processnum = 5
    ratelogic(category, processnum)
