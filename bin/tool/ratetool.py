# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/12.
# 功能:
#   解析类目爬虫所有URL成整体,存入数据库

import tool.log
import logging
from tool.jfile.file import *
from tool.jmysql.mysql import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger("smart")


def dealurlfile():
    # 最小级目录
    lasturls = []

    # 根目录
    dir = tool.log.BASE_DIR + "/data/rateurl"

    # URL文件夹
    level1 = dir
    level2 = dir + "/2urls"
    level3 = dir + "/3urls"
    level4 = dir + "/4urls"
    level5 = dir + "/5urls"

    # 记录
    # id=filename+"-"+position name,url,parent,level
    # 1,mulu,http://dddd,0,1
    # 1_1,mulu,http://dddd,1,2
    # 1_1_1,mulu,http://dddd,1-1,3
    # 1_1_1_1,mulu,http://dddd,1-1-1,4
    # 1—1—1-1-1,mulu,http://dddd,1-1-1-1,5

    listtemp = {}
    t1 = readfilelist(dir + "/oneurl.md")
    t1name = readfilelist(dir + "/onename.md")
    for i in range(min(len(t1), len(t1name))):
        listtemp[str(i + 1)] = t1name[i].replace(",", "_") + "," + t1[i] + ",0,1"

    # 二级
    file2 = listfiles(level2, "-url.md")
    for urlfile in file2:
        position = urlfile.replace("-url.md", "")
        t2 = readfilelist(level2 + "/" + urlfile)
        t2name = readfilelist(level2 + "/" + position + "-name.md")

        # 如果为空,跳过
        if t2 == [] or t2name == []:
            lasturls.append(position)
            continue
        for i in range(min(len(t2), len(t2name))):
            listtemp[position + "-" + str(i + 1)] = t2name[i].replace(",", "_") + "," + t2[i] + "," + position + ",2"

    # 三级
    file3 = listfiles(level3, "-url.md", "")
    for urlfile in file3:
        position = urlfile.replace("-url.md", "")
        t3 = readfilelist(level3 + "/" + urlfile)
        t3name = readfilelist(level3 + "/" + position + "-name.md")

        # 如果为空,跳过
        if t3 == [] or t3name == []:
            lasturls.append(position)
            continue
        for i in range(min(len(t3), len(t3name))):
            listtemp[position + "-" + str(i + 1)] = t3name[i].replace(",", "_") + "," + t3[i] + "," + position + ",3"

    # 四级
    file4 = listfiles(level4, "-url.md")
    for urlfile in file4:
        position = urlfile.replace("-url.md", "")
        t4 = readfilelist(level4 + "/" + urlfile)
        t4name = readfilelist(level4 + "/" + position + "-name.md")

        # 如果为空,跳过
        if t4 == [] or t4name == []:
            lasturls.append(position)
            continue
        for i in range(min(len(t4), len(t4name))):
            listtemp[position + "-" + str(i + 1)] = t4name[i].replace(",", "_") + "," + t4[i] + "," + position + ",4"

    # 五级
    file5 = listfiles(level5, "-url.md")
    for urlfile in file5:
        position = urlfile.replace("-url.md", "")
        t5 = readfilelist(level5 + "/" + urlfile)
        t5name = readfilelist(level5 + "/" + position + "-name.md")

        # 如果为空,跳过
        if t5 == [] or t5name == []:
            lasturls.append(position)
            continue
        for i in range(min(len(t5), len(t5name))):
            listtemp[position + "-" + str(i + 1) + str(i + 1)] = t5name[i].replace(",", "_") + "," + t5[
                i] + "," + position + ",5"
    with open(tool.log.BASE_DIR + "/config/URL.txt", "wt") as hunterhug:
        for i in sorted(listtemp.keys()):
            hunterhug.write(i + "," + listtemp[i] + "\n")
    logger.warning("目录记录数：" + str(len(listtemp)))
    logging.warning("最小类目数" + str(len(lasturls)))
    with open(tool.log.BASE_DIR + "/config/CatchURL.txt", "wt") as hunterhug:
        for i in lasturls:
            try:
                hunterhug.write(i + ":"+listtemp[i]+"\n")
            except:
                logging.error(i)
                pass


# star 保存代理IP信息到本地文件
def keeptomysql(filepath="config/URL.txt", config={}):
    mysql = Mysql(config)
    urls = readfilelist(tool.log.BASE_DIR + "/" + filepath)
    for url in urls:
        sqlzone = url.split(",")
        sql = 'insert into smart_category (`id`,`url`,`name`,`level`,`pid`,`createtime`) values("{id}","{url}","{name}","{level}","{pid}",CURRENT_TIMESTAMP) on duplicate key update updatetime = CURRENT_TIMESTAMP'
        insertsql = sql.format(id=sqlzone[0], url=sqlzone[2], name=sqlzone[1], level=sqlzone[4], pid=sqlzone[3])
        try:
            mysql.ExecNonQuery(insertsql)
            logger.warning("执行sql语句成功:" + insertsql)
        except Exception as err:
            logging.error(err, exc_info=1)
            logger.error(insertsql)


if __name__ == "__main__":
    # 处理URL
    dealurlfile()

    # 保存入数据库
    # config = {"host": "localhost", "user": "root", "pwd": "6833066", "db": "smart_base"}
    # keeptomysql(config=config)
