# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/11.
# 功能:
#   美国亚马逊类目Url爬虫
from spider.logic.ratelogic import *
import tool.log
import logging

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    a = time.clock()
    isdead = False
    while not isdead:
        try:
            ausalogic("3-4")
            # isdead = True
        except Exception as err:
            logging.error(err, exc_info=1)
            pass
        time.sleep(3600)
        logger.error("一分钟后又跑一次")
    b = time.clock()
    logger.error('运行时间：' + timetochina(b - a))
