# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/12.
# 功能:
#   解析类目爬虫所有URL成整体,存入数据库

import tool.log
import logging
from tool.jfile.file import *
from tool.jmysql.mysql import *
from config.config import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger("smart")


def dealurlfile(rubbish="/161-2441050-2846244"):
    # 最小级目录
    lasturls = []

    # 根目录
    dir = getconfig()["datadir"] + "/data/rateurl"

    # URL文件夹
    level1 = dir
    level2 = dir + "/2urls"
    level3 = dir + "/3urls"
    level4 = dir + "/4urls"
    level5 = dir + "/5urls"
    level6 = dir + "/6urls"

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
        # /ref=zg_bs_nav_la_1_la/161-2441050-2846244
        listtemp[str(i + 1)] = t1name[i].replace(",", "_") + "," + t1[i].replace(rubbish,"") + ",0,1"

    # 二级
    file2 = listfiles(level2, "-url.md")
    for urlfile in file2:
        position = urlfile.replace("-url.md", "")
        t2 = readfilelist(level2 + "/" + urlfile)
        t2name = readfilelist(level2 + "/" + position + "-name.md")

        # 如果为空,跳过
        if t2 == [] or t2name == []:
            continue
        for i in range(min(len(t2), len(t2name))):
            listtemp[position + "-" + str(i + 1)] = t2name[i].replace(",", "_") + "," + t2[i].replace(rubbish,"") + "," + position + ",2"

    # 三级
    file3 = listfiles(level3, "-url.md", "")
    for urlfile in file3:
        position = urlfile.replace("-url.md", "")
        t3 = readfilelist(level3 + "/" + urlfile)
        t3name = readfilelist(level3 + "/" + position + "-name.md")

        # 如果为空,跳过
        if t3 == [] or t3name == []:
            continue
        for i in range(min(len(t3), len(t3name))):
            listtemp[position + "-" + str(i + 1)] = t3name[i].replace(",", "_") + "," + t3[i].replace(rubbish,"") + "," + position + ",3"

    # 四级
    file4 = listfiles(level4, "-url.md")
    for urlfile in file4:
        position = urlfile.replace("-url.md", "")
        t4 = readfilelist(level4 + "/" + urlfile)
        t4name = readfilelist(level4 + "/" + position + "-name.md")

        # 如果为空,跳过
        if t4 == [] or t4name == []:
            continue
        for i in range(min(len(t4), len(t4name))):
            listtemp[position + "-" + str(i + 1)] = t4name[i].replace(",", "_") + "," + t4[i].replace(rubbish,"") + "," + position + ",4"

    # 五级
    file5 = listfiles(level5, "-url.md")
    for urlfile in file5:
        position = urlfile.replace("-url.md", "")
        t5 = readfilelist(level5 + "/" + urlfile)
        t5name = readfilelist(level5 + "/" + position + "-name.md")

        # 如果为空,跳过
        if t5 == [] or t5name == []:
            continue
        for i in range(min(len(t5), len(t5name))):
            listtemp[position + "-" + str(i + 1)] = t5name[i].replace(",", "_") + "," + t5[i].replace(rubbish,"") + "," + position + ",5"
            # lasturls.append(position + "-" + str(i + 1))
    # 6级
    file6 = listfiles(level6, "-url.md")
    for urlfile in file6:
        position = urlfile.replace("-url.md", "")
        t6 = readfilelist(level6 + "/" + urlfile)
        t6name = readfilelist(level6 + "/" + position + "-name.md")

        # 如果为空,跳过
        if t6 == [] or t6name == []:
            continue
        for i in range(min(len(t6), len(t6name))):
            listtemp[position + "-" + str(i + 1)] = t6name[i].replace(",", "_") + "," + t6[i].replace(rubbish,"") + "," + position + ",6"
            lasturls.append(position + "-" + str(i + 1))

    temp = listfiles(rootdir=level1,iscur=True,prefix="-url.mdxx")
    for i in temp:
        lasturls.append(i.replace("-url.mdxx",""))

    logger.warning("可用类目记录数：" + str(len(listtemp)))
    logger.warning("最小类目数" + str(len(lasturls)))

    with open(tool.log.BASE_DIR + "/config/base/URL.txt", "wt") as hunterhug:
        for i in sorted(listtemp.keys()):
            bigpid = i.split("-")[0]
            bigpname = t1name[int(bigpid) - 1]
            if i in lasturls:
                hunterhug.write(i + "," + listtemp[i] + "," + bigpid + "," + bigpname.replace(",","_") + ",1" + "\n")
            else:
                hunterhug.write(i + "," + listtemp[i] + "," + bigpid + "," + bigpname.replace(",","_") + ",0" + "\n")


# star 保存代理IP信息到本地文件
def keeptomysql(filepath="config/base/URL.txt", config={}):
    mysql = Mysql(config)
    urls = readfilelist(tool.log.BASE_DIR + "/" + filepath)
    for url in urls:
        sqlzone = url.split(",")
        sql = 'insert into smart_category (`id`,`url`,`name`,`level`,`pid`,`createtime`,`bigpname`,`bigpid`,`ismall`) values("{id}","{url}","{name}",{level},"{pid}",CURRENT_TIMESTAMP,"{bigpname}","{bigpid}",{ismall}) on duplicate key update updatetime = CURRENT_TIMESTAMP'
        insertsql = sql.format(id=sqlzone[0], url=sqlzone[2].split("/ref")[0], name=sqlzone[1], level=sqlzone[4], pid=sqlzone[3],
                               bigpname=sqlzone[6], bigpid=sqlzone[5], ismall=sqlzone[7])
        try:
            mysql.ExecNonQuery(insertsql)
            logger.warning("执行sql语句成功:" + insertsql)
        except Exception as err:
            logger.error(err, exc_info=1)
            logger.error(insertsql)


if __name__ == "__main__":
    # 处理URL
    dealurlfile()

    # 保存入数据库
    # config = {"host": "localhost", "user": "root", "pwd": "6833066", "db": "smart_base"}
    allconfig = getconfig()
    try:
        config = allconfig["basedb"]
        keeptomysql(config=config)
    except:
        raise Exception("数据库配置出错")