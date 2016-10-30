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
import copy

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def phoneinsertpmysql(pmap, dbname, tablename):
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
    pmaps = copy.deepcopy(pmap)
    try:
        pmaps["tablename"] = tablename
        if len(pmaps["title"]) > 240:
            pmaps["title"] = pmaps["title"][0:220]
        pmaps["title"] = pymysql.escape_string(pmaps["title"])
        if len(pmaps["shipby"]) > 240:
            pmaps["shipby"] = pmaps["title"][0:220]
        pmaps["shipby"] = pymysql.escape_string(pmaps["shipby"])
        if "No sold" in pmaps["soldby"]:
            pass
        if "Amazon.com" in pmaps["soldby"]:
            pass
        else:
            pmaps["soldby"] = "https://www.amazon.com/sp?seller=" + pmaps["soldby"]
        config = getconfig()[getconfig()["dbprefix"] + dbname]
        db = Mysql(config)
        # escape_string
        sql = "INSERT IGNORE INTO `{tablename}`(`id`,`smallrank`,`name`,`bigname`,`title`,`asin`,`url`,`rank`,`soldby`," \
              "`shipby`,`col1`,`col2`,`score`,`commentnum`,`commenttime`,`createtime`)" \
              "VALUES('{id}',{smallrank},'{name}','{bigname}','{title}','{asin}','{url}',{rank},'{soldby}'," \
              "'{shipby}','{price}','{img}',{score},{commentnum},'{commenttime}',CURRENT_TIMESTAMP);".format_map(pmaps)
        db.ExecNonQuery(sql)
        logger.warning("插数据库成功,数据库:" + dbname + ",表:" + pmaps["tablename"] + ",Id:" + pmaps["id"])
        return True
    except Exception as err:
        logger.error("插数据库出错")
        logger.error(err, exc_info=1)
    return False


# 插列表页数据
def phoneinsertlist(parsecontent, url):
    try:
        # itemlist[asin] = [smallrank, url, img, title, price]
        # 抓取的类目URL
        catchurl = url[1]
        # 类目名
        catchname = url[2]
        # 类目ID
        tempid = url[0]
        # 大类名
        bigpname = url[4]
        # 数据库
        dbname = url[6]
        mysqlconfig = getconfig()["db"]
        db = Mysql(mysqlconfig)
        for item in parsecontent:
            try:
                try:
                    rank = int(parsecontent[item][0])
                except:
                    rank = -1
                asin = item
                url = parsecontent[item][1]
                img = parsecontent[item][2]
                if len(img) > 240:
                    img = ""
                title = parsecontent[item][3]
                title = pymysql.escape_string(title)
                price = parsecontent[item][4]

                # 标志
                id = tempid + "&" + str(rank) + "-" + asin
                selectsql = '''SELECT iscatch from `{tablename}` where id="{id}"'''.format(tablename=tool.log.TODAYTIME,
                                                                                           id=id)
                result = db.ExecQuery(selectsql)
                if result:
                    if result[0][0] == 1:
                        logger.warning("数据已存在:" + selectsql)
                        continue
                else:
                    insertsql = '''INSERT INTO `{tablename}`
                    (`id`,`purl`,`iscatch`,`smallrank`,`name`,`bigname`,`title`,`asin`,`url`,`dbname`,`price`,`img`) VALUES
                    ("{id}","{purl}",{iscatch},{smallrank},"{name}","{bigname}","{title}","{asin}","{url}","{dbname}","{price}","{img}")
                    '''.format(tablename=tool.log.TODAYTIME, id=id, purl=catchurl, iscatch=0, smallrank=rank,
                               name=catchname, title=title, url=url, asin=asin, dbname=dbname, price=price, img=img,
                               bigname=bigpname)
                    db.ExecNonQuery(insertsql)
                    logger.warning("预插数据库成功:" + insertsql)
            except Exception as e:
                logger.error("预插数据库出错" + insertsql)
                logger.error(e, exc_info=1)
    except Exception as e:
        logger.error("??mdzz")


# 插入已经存在的数据
def phoneinsertexsitlist(pmap, basedata):
    sql = ""
    pmaps = copy.deepcopy(pmap)
    try:
        pmaps["purl"] = basedata[1]
        pmaps["dbname"] = basedata[6]
        if len(pmaps["title"]) > 240:
            pmaps["title"] = pmaps["title"][0:220]
        pmaps["title"] = pymysql.escape_string(pmaps["title"])
        if len(pmaps["shipby"]) > 240:
            pmaps["shipby"] = pmaps["title"][0:220]
        pmaps["shipby"] = pymysql.escape_string(pmaps["shipby"])
        pmaps["tablename"] = tool.log.TODAYTIME
        pmaps["id"] = basedata[0] + "&" + str(pmaps["smallrank"]) + "-" + pmaps["asin"]
        if "No sold" in pmaps["soldby"]:
            pass
        if "Amazon.com" in pmaps["soldby"]:
            pass
        else:
            pmaps["soldby"] = "https://www.amazon.com/sp?seller=" + pmaps["soldby"]
        config = getconfig()["db"]
        db = Mysql(config)
        pmaps["iscatch"] = 1
        sql = "INSERT INTO `{tablename}`(`id`,`smallrank`,`name`,`bigname`,`title`,`asin`,`url`,`rank`,`soldby`," \
              "`shipby`,`price`,`score`,`commentnum`,`commenttime`,`createtime`,`iscatch`,`purl`,`dbname`)" \
              "VALUES('{id}',{smallrank},'{name}','{bigname}','{title}','{asin}','{url}',{rank},'{soldby}'," \
              "'{shipby}','{price}',{score},{commentnum},'{commenttime}',CURRENT_TIMESTAMP,{iscatch},'{purl}','{dbname}') " \
              "on duplicate key update `createtime` = CURRENT_TIMESTAMP,`rank`={rank}," \
              "`soldby`='{soldby}',`shipby`='{shipby}',`score`={score}," \
              "`commentnum`={commentnum},`commenttime`='{commenttime}',`iscatch`={iscatch};".format_map(
                pmaps)
        db.ExecNonQuery(sql)
        logger.warning("插日期数据库成功" + sql)
    except Exception as e:
        logger.error("插日期数据库失败" + sql)
        logger.error(e, exc_info=1)