# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/14.
# 功能:
#  获取大类下最小的类目

import tool.log
import logging
from tool.jmysql.mysql import *
from config.config import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def usaurl(config={}, category=[], limitnum="20000"):
    mysql = Mysql(config)
    # ('1-1', 'https://www.amazon.com/Best-Sellers-Appliances-Cooktops/zgbs/appliances/3741261/ref=zg_bs_nav_la_1_la/161-2441050-2846244', 'Cooktops', 2, 5, '1', '1', 'Appliances')
    condition = ""
    length = len(category)
    for i in range(length):
        if i == length - 1:
            condition = condition + 'bigpname="' + category[i] + '"'
        else:
            condition = condition + 'bigpname="' + category[i] + '" or '
    selectsql = 'SELECT id,url,name,page,bigpname,level,`database` FROM smart_category where isvalid=1 and (' + condition + ') limit ' + limitnum
    logger.warning(selectsql)
    result = mysql.ExecQuery(selectsql)
    return result


def dbexist(dbconfig, tablename):
    try:
        temp = getconfig()[dbconfig]
        db = Mysql(temp)
        sql = "SELECT * from " + tablename + " limit 1"
        db.ExecQuery(sql)
    except:
        logger.error(dbconfig + "数据库不存在，或者表" + tablename + "找不到")
        return False
    return True


if __name__ == "__main__":
    config = {"host": "192.168.0.152", "user": "bai", "pwd": "123456", "db": "smart_base"}
    category = ["Industrial & Scientific", "Appliances"]
    print(usaurl(config, category=category))
    dbexist("basedb", "smart_ip")
    dbexist("basedb", "smart_")
