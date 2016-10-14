# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/14.
# 功能:
#  
import tool.log
import logging
from  tool.jmysql import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)

def usaurl(config={}):
    mysql = Mysql(config)
    selectsql = "SELECT ip,zone,failtimes FROM smart_ip limit 1000;"
    result = mysql.ExecQuery(selectsql)


if __name__ == "__main__":