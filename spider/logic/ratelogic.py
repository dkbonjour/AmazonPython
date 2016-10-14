# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/14.
# 功能:
#  
import tool.log
import logging
from action.url import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def ratelogic(category = ["Appliances"],processnum =1):
    usaurl(category)



if __name__ == "__main__":
    category = ["Appliances"]
    processnum = 4
    ratelogic(category,processnum)