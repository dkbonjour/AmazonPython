# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/17.
# 功能:
#  
import tool.log
import logging
import time
from spider.logic.ratelogic import *
# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    a = time.clock()
    # 大类名
    category = ["Appliances", "Arts_ Crafts & Sewing"]

    # 并行数量
    processnum = 10

    # 类目抓取数量
    limit = "11"

    # 开抓，ko
    ratelogic(category, processnum, limit)

    b = time.clock()

    logger.error('运行时间：' + timetochina(b - a))