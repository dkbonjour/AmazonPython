# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/10.
# 功能:
#   读取代理IP

from  tool.jmysql.mysql import *
from tool.jfile.file import *
import logging
from tool.log import *

# 日志
setup_logging()
logger = logging.getLogger("proxy")
smartlogger = logging.getLogger("smart")

# 全局变量保证读取代理IP只有一次
IPPOOL = {}
IPPOOLSUCCESS = False


# star 读取代理IP,格式为IP为键，地址为值，如104.143.159.232:808 美国加利福尼亚州洛杉矶
# {"125.1.1.1":"美国"}
def proxy(where="local", filepath="../config/IP.txt", failtimes=0):
    global IPPOOL
    global IPPOOLSUCCESS
    if IPPOOLSUCCESS:
        return IPPOOL, len(IPPOOL)
    ips = []
    if where == "local":
        logger.info("加载本地代理IP文件")
        ipfile = open(filepath, 'rb')
        context = ipfile.read().decode("utf-8", "ignore")
        ipfile.close()
        ips = context.splitlines()
    else:
        logger.info("加载数据库代理IP文件")
        config = {"host": "localhost", "user": "root", "pwd": "6833066", "db": "smart_base"}
        mysql = Mysql(config)
        selectsql = "SELECT ip,zone,failtimes FROM smart_ip limit 1000;"
        result = mysql.ExecQuery(selectsql)
        for ip in result:
            if ip[2] > failtimes:
                pass
            else:
                ips.append(ip[0] + "-" + ip[1])
    ipsright = ipfilter(ips)
    IPPOOL = ipsright
    IPPOOLSUCCESS = True
    return ipsright, len(ipsright)


# 过滤非法IP
def ipfilter(ips=[]):
    returnips = {}
    for ip in ips:
        location = "未知地址"
        ip = ip.strip().split("-")
        if len(ip) == 2:
            location = ip[1]
        ip = ip[0]
        ipzone = ip.split(":")
        if (len(ipzone) != 2):
            logger.info(ip + "-缺少端口")
            continue
        else:
            if (ipzone[1].isnumeric()):
                pass
            else:
                logger.info(ip + "-端口有问题")
                continue
        ipdevide = ipzone[0].split(".")
        if len(ipdevide) != 4:
            logger.info(ip + "-IP段不足")
            continue
        else:
            haserror = False
            for i in ipdevide:
                if i.isnumeric() and 0 <= int(i) <= 255:
                    pass
                else:
                    logger.info(ip + "-IP段有问题")
                    haserror = True
                    break
            if haserror == False:
                # logger.info(ip + "_正确！")
                returnips[ip] = location
    return returnips


if __name__ == "__main__":
    # 获取代理IP池
    ips, num = proxy("mysql")
    smartlogger.info(ips)
    smartlogger.info(str(num) + "条IP")
