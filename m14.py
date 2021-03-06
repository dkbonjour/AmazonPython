# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/17.
# 功能:   机器1
#  
import tool.log
from spider.logic.phonelogic import *
import shutil


# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print(copyright("亚马逊大霸王14开爬"))

    createjia(getconfig()["datadir"] + "/cookie")
    a = time.clock()
    # 大类名
    try:
        # changeconfig("catchbywhich","bigpname")
        # category = getconfig()["catchurl"]
        changeconfig("catchbywhich", "database")
        changeconfig("redispoolname","ippool14")
        changeconfig("redispoolfuckname","ippoolfuck14")
        category = ["14"]
        # category = ["9","10","11","12"]
        changeconfig("catchurl",category)
    except:
        category = ["Appliances", "Arts_ Crafts & Sewing"]

    # 并行数量
    try:
        processnum = getconfig()["processnum"]
    except:
        processnum = 10

    # 类目抓取数量
    try:
        limit = getconfig()["urlnum"]
    except:
        limit = 60
    # 开抓，ko
    ratelogic(category, processnum, limit)

    b = time.clock()

    logger.error('运行时间：' + timetochina(b - a))
