# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/14.
# 功能:
#  获取大类下最小的类目

import tool.log
import logging
from tool.jmysql.mysql import *
from config.config import *
import pymysql

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def usaurl(config={}, category=[], limitnum=20000):
    mysql = Mysql(config)
    # ('1-1', 'https://www.amazon.com/Best-Sellers-Appliances-Cooktops/zgbs/appliances/3741261/ref=zg_bs_nav_la_1_la/161-2441050-2846244', 'Cooktops', 2, 5, '1', '1', 'Appliances')
    condition = ""
    length = len(category)
    catchbywhich = "`" + getconfig()["catchbywhich"] + "`"
    for i in range(length):
        if i == length - 1:
            condition = condition + catchbywhich + '="' + category[i] + '"'
        else:
            condition = condition + catchbywhich + '="' + category[i] + '" or '
    selectsql = 'SELECT id,url,name,page,bigpname,level,`database` FROM smart_category where isvalid=1 and (' + condition + ') group by url limit 0,' + str(
            limitnum)
    logger.warning("查詢：" + selectsql)
    result = mysql.ExecQuery(selectsql)
    return result


def dbexist(dbconfig, tablename, todays):
    try:
        temp = getconfig()[dbconfig]
        db = Mysql(temp)
        sql = 'SELECT count(*) from `' + tablename + '` where id like "' + todays + '%"'
        num = db.ExecQuery(sql)
        if num[0][0] >= getconfig()["itemnum"]:
            logger.warning(todays + "|" + dbconfig + ":" + tablename + " completed")
            return False
    except:
        logger.error(dbconfig + "数据库不存在，或者表" + tablename + "找不到" + sql)
        return False
    return True


def insertpmysql(pmap, dbname, tablename):
    # {
    #     "asin": "B004BPOPXS",
    #     "bigname": "Arts_ Crafts & Sewing",
    #     "commentime": "December 16- 2011",
    #     "commentnum": 15,
    #     "name": "Beading Cords & Threads",
    #     "price": 2.99,
    #     "rank": 10750,
    #     "score": 4.1,
    #     "shipby": "FBA",
    #     "smallrank": 63,
    #     "soldby": "Amazon.com",
    #     "title": "Pepperell Premium Quality Hippie Hemp Cord for Jewelry Making- 380-Feet- Natural",
    #     "url": "https://www.amazon.com/dp/B004BPOPXS"
    # }
    sql = ""
    try:
        pmap["tablename"] = tablename
        pmap["title"] = pymysql.escape_string(pmap["title"])
        if "No sold" in pmap["soldby"]:
            pass
        else:
            pmap["soldby"] = "https://www.amazon.com/sp?seller=" + pmap["soldby"]
        config = getconfig()[dbname]
        db = Mysql(config)
        # escape_string
        sql = "INSERT IGNORE INTO `{tablename}`(`id`,`smallrank`,`name`,`bigname`,`title`,`asin`,`url`,`rank`,`soldby`," \
              "`shipby`,`price`,`score`,`commentnum`,`commenttime`,`createtime`)" \
              "VALUES('{id}',{smallrank},'{name}','{bigname}','{title}','{asin}','{url}',{rank},'{soldby}'," \
              "'{shipby}',{price},{score},{commentnum},'{commenttime}',CURRENT_TIMESTAMP);".format_map(pmap)
        db.ExecNonQuery(sql)
        logger.warning("插数据库成功,数据库:" + dbname + ",表:" + pmap["tablename"] + ",Id" + pmap["id"])

        return True
    except Exception as err:
        logger.error("插数据库出错:" + sql)
    return False


# 插列表页数据
def insertlist(listdata, basedata):
    try:
        # 抓取的类目URL
        catchurl = basedata[1]
        # 类目名
        catchname = basedata[2]
        # 类目ID
        id = basedata[0]
        # 大类名
        bigpname = basedata[4]
        # 数据库
        dbname = basedata[6]
        # [rank, asin, title]
        try:
            rank = int(listdata[0])
        except:
            rank = -1
        asin = listdata[1]
        title = pymysql.escape_string(listdata[2])
        # 标志
        id = id + "&" + str(rank) + "-" + asin
        # SELECT count(*) from `20161028` where id="1-1-1-1&1-YJGSJSGJ" and iscatch=1
        mysqlconfig = getconfig()["db"]
        db = Mysql(mysqlconfig)
        selectsql = '''SELECT iscatch from `{tablename}` where id="{id}"'''.format(tablename=tool.log.TODAYTIME, id=id)
        result = db.ExecQuery(selectsql)
        if result:
            if result[0][0] == 1:
                # 记录存在
                logger.warning("数据已存在:" + selectsql)
                return False
            else:
                return True
        else:
            insertsql = '''INSERT INTO `{tablename}`
            (`id`,`purl`,`iscatch`,`smallrank`,`name`,`bigname`,`title`,`asin`,`url`,`dbname`) VALUES
            ("{id}","{purl}",{iscatch},{smallrank},"{name}","{bigname}","{title}","{asin}","{url}","{dbname}")
            '''.format(tablename=tool.log.TODAYTIME, id=id, purl=catchurl, iscatch=0, smallrank=rank,
                       name=catchname, title=title, url="https://www.amazon.com/dp/" + asin, asin=asin, dbname=dbname,
                       bigname=bigpname)
            db.ExecNonQuery(insertsql)
            logger.warning("预插数据库成功:" + insertsql)
            return True
    except Exception as e:
        logger.error("预插数据库出错" + insertsql)
        logger.error(e, exc_info=1)
        return False


# 插入已经存在的数据
def insertexsitlist(pmap, basedata):
    sql = ""
    try:
        # 类目ID
        id = basedata[0]
        pmap["title"] = pymysql.escape_string(pmap["title"])
        pmap["tablename"] = tool.log.TODAYTIME
        pmap["id"] = id = id + "&" + str(pmap["rank"]) + "-" + pmap["asin"]
        if "No sold" in pmap["soldby"]:
            pass
        else:
            pmap["soldby"] = "https://www.amazon.com/sp?seller=" + pmap["soldby"]
        config = getconfig()["db"]
        db = Mysql(config)
        sql = "INSERT INTO `{tablename}`(`id`,`smallrank`,`name`,`bigname`,`title`,`asin`,`url`,`rank`,`soldby`," \
              "`shipby`,`price`,`score`,`commentnum`,`commenttime`,`createtime`)" \
              "VALUES('{id}',{smallrank},'{name}','{bigname}','{title}','{asin}','{url}',{rank},'{soldby}'," \
              "'{shipby}',{price},{score},{commentnum},'{commenttime}',CURRENT_TIMESTAMP) " \
              "on duplicate key update `createtime` = CURRENT_TIMESTAMP,`title`='{title}',`rank`={rank}," \
              "`soldby`='{soldby}',`shipby`='{shipby}',`price`={price},`score`={score}," \
              "`commentnum`={commentnum},`commenttime`='{commenttime}';".format_map(pmap)
        db.ExecNonQuery(sql)
        logger.warning("插日期数据库成功" + sql)
    except Exception as e:
        logger.error("插日期数据库失败" + sql)
        logger.error(e, exc_info=1)


if __name__ == "__main__":
    config = {"host": "192.168.0.152", "user": "bai", "pwd": "123456", "db": "smart_base"}
    category = ["Industrial & Scientific", "Appliances"]
    print(usaurl(config, category=category))
    dbexist("basedb", "smart_ip", "20161018")
    dbexist("ratedb1", "3-1-1-1", "20161018")
