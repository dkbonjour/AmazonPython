# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import redis
import time
from config.config import *
from action.proxy import *

REDISSERVER = None
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def initredis():
    redisconfig = getconfig()["redispoolconfig"]
    global REDISSERVER
    REDISSERVER = redis.StrictRedis(host=redisconfig["host"], port=redisconfig["port"], db=0,
                                    password=redisconfig["pwd"])
    return REDISSERVER


def initippool(poolname="ippool"):
    global REDISSERVER
    if REDISSERVER == None:
        initredis()
    r = REDISSERVER
    ip = []
    # 删除旧的列队
    r.delete(poolname)
    try:
        config = getconfig()["basedb"]
        ips = proxy(where="mysql", config=config)
        # 将ip写入数组并加上时间戳
        for item in ips:
            # 标记时间戳
            markedtime = int(time.time())
            ipstr = item.strip() + "*" + str(markedtime) + "*0*0"
            ip.append(ipstr)

        # 将ip添加进消息列队
        for item in ip:
            r.lpush(poolname, item)
        logger.error("redis ip池好了")
    except Exception as err:
        logger.error(err, exc_info=1)
        exit()


def popip(secord=3, poolname="ippool"):
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
        logger.error(ip + "redis暂停:" + str(secord))
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
        r.lpush(poolname, ipstr)
    except Exception as err:
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
