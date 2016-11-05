# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/14.
# 功能:
#  手机/PC端混合！！插数据库

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
        pmaps["title"] = pymysql.escape_string(pmaps["title"]).replace("'", "").replace('"', "").replace("\\", "")
        if len(pmaps["shipby"]) > 240:
            pmaps["shipby"] = pmaps["title"][0:220]
        pmaps["shipby"] = pymysql.escape_string(pmaps["shipby"]).replace("'", "").replace('"', "").replace("\\", "")
        pmaps["url"] = pmaps["url"].replace("'", "").replace('"', "").replace("\\", "")
        pmaps["bigname"] = pmaps["bigname"].replace("'", "").replace('"', "").replace("\\", "")
        pmaps["name"] = pmaps["name"].replace("'", "").replace('"', "").replace("\\", "")
        if "No sold" in pmaps["soldby"]:
            pass
        elif "Amazon.com" in pmaps["soldby"]:
            pass
        else:
            pmaps["soldby"] = pymysql.escape_string("https://www.amazon.com/sp?seller=" + pmaps["soldby"])
        config = getconfig()[getconfig()["dbprefix"] + dbname]
        db = Mysql(config)
        # escape_string
        # sql = "INSERT IGNORE INTO `{tablename}`(`id`,`smallrank`,`name`,`bigname`,`title`,`asin`,`url`,`rank`,`soldby`," \
        #       "`shipby`,`col1`,`col2`,`score`,`commentnum`,`commenttime`,`createtime`)" \
        #       "VALUES('{id}',{smallrank},'{name}','{bigname}','{title}','{asin}','{url}',{rank},'{soldby}'," \
        #       "'{shipby}','{price}','{img}',{score},{commentnum},'{commenttime}',CURRENT_TIMESTAMP);".format_map(pmaps)
        if pmaps["rank"] == -1:
            pmaps["rank"] = 20000000
        if pmaps["rank"] == 0:
            pmaps["rank"] = 10000000
        sql = '''INSERT IGNORE INTO `{tablename}`(`id`,`smallrank`,`name`,`bigname`,`title`,`asin`,`url`,`rank`,`soldby`,`shipby`,`score`,`commentnum`,`commenttime`,`createtime`) VALUES('{id}',{smallrank},'{name}','{bigname}','{title}','{asin}','{url}',{rank},'{soldby}','{shipby}',{score},{commentnum},'{commenttime}',CURRENT_TIMESTAMP);'''.format_map(
            pmaps)
        db.ExecNonQuery(sql)
        logger.warning("插详情分表数据库成功,数据库:" + dbname + ",表:" + pmaps["tablename"] + ",Id:" + pmaps["id"])
        return True
    except Exception as err:
        logger.error("插详情分表数据库出错：" + sql)
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
        insertsql = ""
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
                title = pymysql.escape_string(title).replace("'", "").replace('"', "").replace("\\", "")
                img = pymysql.escape_string(img).replace("'", "").replace('"', "").replace("\\", "")
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
                    insertsql = '''INSERT IGNORE INTO `{tablename}`
                    (`id`,`purl`,`iscatch`,`smallrank`,`name`,`bigname`,`title`,`asin`,`url`,`dbname`,`price`,`img`,`createtime`) VALUES
                    ("{id}","{purl}",{iscatch},{smallrank},"{name}","{bigname}","{title}","{asin}","{url}","{dbname}","{price}","{img}",CURRENT_TIMESTAMP)
                    '''.format(tablename=tool.log.TODAYTIME, id=id, purl=catchurl, iscatch=0, smallrank=rank,
                               name=catchname, title=title, url=url, asin=asin, dbname=dbname, price=price, img=img,
                               bigname=bigpname)
                    db.ExecNonQuery(insertsql)
                    logger.warning("预插列表数据库成功:" + insertsql)
            except Exception as e:
                logger.error("预插数据库出错，列表内层错误" + insertsql)
                logger.error(e, exc_info=1)
        return True
    except Exception as e:
        logger.error("??mdzz列表外层错误")
        return False


# 插入已经存在的数据
def phoneinsertexsitlist(pmap, basedata):
    sql = ""
    pmaps = copy.deepcopy(pmap)
    try:
        pmaps["purl"] = basedata[1].replace("'", "").replace('"', "").replace("\\", "")
        pmaps["dbname"] = basedata[6]
        if len(pmaps["title"]) > 240:
            pmaps["title"] = pmaps["title"][0:220]
        pmaps["title"] = pymysql.escape_string(pmaps["title"]).replace("'", "").replace('"', "").replace("\\", "")
        if len(pmaps["shipby"]) > 240:
            pmaps["shipby"] = pmaps["title"][0:220]
        pmaps["shipby"] = pymysql.escape_string(pmaps["shipby"]).replace("'", "").replace('"', "").replace("\\", "")
        pmaps["tablename"] = tool.log.TODAYTIME
        pmaps["id"] = basedata[0] + "&" + str(pmaps["smallrank"]) + "-" + pmaps["asin"]
        pmaps["url"] = pmaps["url"].replace("'", "").replace('"', "").replace("\\", "")
        pmaps["bigname"] = pmaps["bigname"].replace("'", "").replace('"', "").replace("\\", "")
        pmaps["name"] = pmaps["name"].replace("'", "").replace('"', "").replace("\\", "")
        if "No sold" in pmaps["soldby"]:
            pass
        elif "Amazon.com" in pmaps["soldby"]:
            pass
        else:
            pmaps["soldby"] = pymysql.escape_string("https://www.amazon.com/sp?seller=" + pmaps["soldby"])
        config = getconfig()["db"]
        db = Mysql(config)
        pmaps["iscatch"] = 1
        try:
            if pmaps["rdalei"] == "":
                raise Exception("真正大类没有")
        except:
            pmaps["rdalei"] = pmaps["bigname"]
        if pmaps["rank"] == -1:
            pmaps["rank"] = 20000000
        if pmaps["rank"] == 0:
            pmaps["rank"] = 10000000
        sql = '''INSERT INTO `{tablename}`(`id`,`smallrank`,`name`,`bigname`,`title`,`asin`,`url`,`rank`,`soldby`,`shipby`,`price`,`score`,`commentnum`,`commenttime`,`iscatch`,`purl`,`dbname`,`col1`)VALUES('{id}',{smallrank},'{name}','{bigname}','{title}','{asin}','{url}',{rank},'{soldby}','{shipby}','{price}',{score},{commentnum},'{commenttime}',{iscatch},'{purl}','{dbname}','{rdalei}') on duplicate key update `rank`={rank},`soldby`='{soldby}',`shipby`='{shipby}',`score`={score},`commentnum`={commentnum},`commenttime`='{commenttime}',`iscatch`={iscatch},`col1`='{rdalei}';'''.format_map(
            pmaps)
        db.ExecNonQuery(sql)
        logger.warning("插详情日期数据库成功" + sql)
        return True
    except Exception as e:
        logger.error("插详情日期数据库失败" + sql)
        logger.error(e, exc_info=1)
        return False
