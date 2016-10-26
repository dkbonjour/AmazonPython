# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/24.
# 功能:
#  
import tool.log
import logging
from action.redispool import *
# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    initippool()