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

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def ratelogic(category=["Appliances"], processnum=1):
    allconfig = getconfig()
    try:
        config = allconfig["basedb"]
    except:
        raise Exception("数据库配置出错")
    urls=list(usaurl(config,category))
    tasklist=devidelist(urls,processnum)
    for task in tasklist:
        print(tasklist[task])


if __name__ == "__main__":
    category = ["Appliances"]
    processnum = 5
    ratelogic(category, processnum)
