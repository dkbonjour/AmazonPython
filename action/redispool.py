# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/10.
# 功能:
#   Redis IP池

import redis
import time
from config.config import *
from action.proxy import *
import random
from tool.jfile.file import *

REDISSERVER = None
tool.log.setup_logging()
logger = logging.getLogger(__name__)

def initredis():
    redisconfig = getconfig()["redispoolconfig"]
    global REDISSERVER
    REDISSERVER = redis.StrictRedis(host=redisconfig["host"], port=redisconfig["port"], db=0,
                                    password=redisconfig["pwd"])
    return REDISSERVER


def initippool(poolname="ippool", poolfuckname="ippoolfuck"):
    poolnum = getconfig()["redispoolnumber"]
    global REDISSERVER
    if REDISSERVER == None:
        initredis()
    r = REDISSERVER
    try:
        config = getconfig()["basedb"]
        renxin = input("根据原始配置来初始化，是选择1，否选择2：")
        if renxin == "1":
            if getconfig()["ipinmysql"]:
                where = "mysql"
            else:
                where = "local"
        else:
            renxin1 = input("从数据库加载选择1，从本地选择2：")
            if renxin1 == "1":
                where = "mysql"
            else:
                input("请往config/base/IP.txt按行放IP，准备好请按任意键：")
                where = "local"
        ips = proxyss(where=where, config=config)
        print(ips)
        ipss = ips.keys()
        temp = []
        for i in ipss:
            temp.append(i)
        # 切割IP
        ipss = temp
        ipss = devidelist(ipss, poolnum)
        logger.warning("IP切成：" + str(poolnum) + "份")
        for item in ipss:
            ip = []
            du = r.llen(poolname + str(item + 1))
            print(str(item + 1) + "还有IP：" + str(du))
            # 删除旧的列队
            ii = input("删除已经存在的" + str(item + 1) + "队列,是选择1:")
            if ii == "1":
                r.delete(poolname + str(item + 1))
            # r.delete(poolfuckname + str(item + 1))
            for i in ipss[item]:
                # 标记时间戳
                markedtime = int(time.time())
                ipstr = i.strip() + "*" + str(markedtime) + "*0*0"
                ip.append(ipstr)

            # 将ip添加进消息列队
            for j in ip:
                r.lpush(poolname + str(item + 1), j)
            logger.warning("redis ip池好了:" + poolname + str(item + 1))
    except Exception as err:
        logger.error(err, exc_info=1)
        # exit()


def popip(secord=5, poolname="ippool"):
    global REDISSERVER
    if REDISSERVER == None:
        initredis()
    r = REDISSERVER

    # 阻塞弹出
    try:
        temppop = r.brpop(poolname, timeout=0)
    except Exception as err:
        logger.error("redis没数据，阻塞失败")
        logger.error(err, exc_info=1)
    # print(temppop)
    splitstar = temppop[1].decode('utf-8', 'ignore').split("*")
    ip = splitstar[0]
    times = int(splitstar[2])
    robottime = int(splitstar[3])
    # 得到间隔大于3秒的ip
    # 当前时间
    nowtime = int(time.time())
    # 如果时间间隔大于3就取出来使用
    if nowtime - int(splitstar[1]) > secord:
        return ip, times, robottime
    else:
        # secord = random.randint(secord, secord + 1)
        if secord > 0:
            logger.warning(ip + ":" + str(times) + "-" + str(robottime) + ":redis暂停:" + str(secord))
            time.sleep(secord)
        return ip, times, robottime


def puship(ip, times, robottime, poolname="ippool"):
    global REDISSERVER
    if REDISSERVER == None:
        initredis()
    r = REDISSERVER
    nowtime = int(time.time())
    times = times + 1
    ipstr = ip + "*" + str(nowtime) + "*" + str(times) + "*" + str(robottime)
    try:
        r.rpush(poolname, ipstr)
    except Exception as err:
        logger.error("放IP失败")
        logger.error(err, exc_info=1)


def pushipfuck(ip, times, robottime, poolname="ippoolfuck"):
    global REDISSERVER
    if REDISSERVER == None:
        initredis()
    r = REDISSERVER
    nowtime = int(time.time())
    times = times + 1
    ipstr = ip + "*" + str(nowtime) + "*" + str(times) + "*" + str(robottime)
    try:
        r.lpush(poolname, ipstr)
    except Exception as err:
        logger.error("放IP失败")
        logger.error(err, exc_info=1)


if __name__ == '__main__':
    initredis()
    poolname = "ippool"
    initippool(poolname)
    # time.sleep(5)
    for i in range(1000):
        ip, times, robottime = popip(3, poolname)
        print(ip)
        print(times)
        print(robottime)
        puship(ip, times, robottime + 1, poolname)
