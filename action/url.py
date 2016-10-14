# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/14.
# 功能:
#  获取大类下最小的类目

import tool.log
import logging
from tool.jmysql.mysql import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def usaurl(config={}, category=[]):
    mysql = Mysql(config)
    # ('1-1', 'https://www.amazon.com/Best-Sellers-Appliances-Cooktops/zgbs/appliances/3741261/ref=zg_bs_nav_la_1_la/161-2441050-2846244', 'Cooktops', 2, 5, '1', '1', 'Appliances')
    condition = ""
    length = len(category)
    for i in range(length):
        if i == length - 1:
            condition = condition + 'bigpname="' + category[i] + '"'
        else:
            condition = condition + 'bigpname="' + category[i] + '" or '
    selectsql = 'SELECT id,url,name,page,bigpname FROM smart_category where ismall=1 and isvalid=1 and (' + condition + ')'
    logger.warning(selectsql)
    result = mysql.ExecQuery(selectsql)
    return result


if __name__ == "__main__":
    config = {"host": "localhost", "user": "root", "pwd": "6833066", "db": "smart_base"}
    category = ["Industrial & Scientific", "Appliances"]
    print(usaurl(config, category=category))
