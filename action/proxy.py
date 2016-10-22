# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/10.
# 功能:
#   读取代理IP，可选择本地读取或者数据库读取

from tool.jmysql.mysql import *
import logging
import tool.log
from config.config import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger("proxy")
smartlogger = logging.getLogger("smart")

# 全局变量保证读取代理IP只有一次
IPPOOL = {}
IPPOOLSUCCESS = False
IPDEAD = []


# star 读取代理IP,格式为IP为键，地址为值，如104.143.159.232:808 美国加利福尼亚州洛杉矶
# {"125.1.1.1":"美国"}
# 代理可以选择从数据库读，但是要填数据库配置
def proxy(where="local", config={}, filepath="config/base/IP.txt", failtimes=0):
    filepath = tool.log.BASE_DIR + "/" + filepath
    global IPPOOL
    global IPPOOLSUCCESS
    global IPDEAD
    if IPPOOLSUCCESS:
        smartlogger.debug("IP已经加载过了")
        if len(IPPOOL) == 0:
            logger.error("IP池用完")
            exit()
        return IPPOOL
    ips = []
    if where == "local":
        logger.warning("加载本地代理IP文件")
        ipfile = open(filepath, 'rb')
        context = ipfile.read().decode("utf-8", "ignore")
        ipfile.close()
        ips = context.splitlines()
    else:
        logger.warning("加载数据库代理IP文件")
        mysql = Mysql(config)
        selectsql = "SELECT ip,zone,failtimes FROM smart_ip limit 1000;"
        result = mysql.ExecQuery(selectsql)
        for ip in result:
            if getconfig()["limitip"]:
                if ip[2] > failtimes:
                    pass
            else:
                ips.append(ip[0] + "-" + ip[1])
    IPPOOL = ipfilter(ips)
    # logger.error(IPPOOL)
    IPPOOLSUCCESS = True
    return IPPOOL


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
            logger.warning(ip + "-缺少端口")
            continue
        else:
            if (ipzone[1].isnumeric()):
                pass
            else:
                logger.warning(ip + "-端口有问题")
                continue
        ipdevide = ipzone[0].split(".")
        if len(ipdevide) != 4:
            logger.warning(ip + "-IP段不足")
            continue
        else:
            haserror = False
            for i in ipdevide:
                if i.isnumeric() and 0 <= int(i) <= 255:
                    pass
                else:
                    logger.warning(ip + "-IP段有问题")
                    haserror = True
                    break
            if haserror == False:
                # logger.warning(ip + "_正确！")
                returnips[ip] = [location]
    return returnips


def koipmysql(ip):
    try:
        mysql = Mysql(getconfig()["basedb"])
        sql = 'update smart_ip set failtimes=failtimes+1 where ip="' + ip + '"'
        mysql.ExecNonQuery(sql)
    except:
        logger.error("删除数据库IP" + ip + "失败！！")


# 只做测试！！！
if __name__ == "__main__":
    # 获取代理IP池
    config = {"host": "192.168.0.152", "user": "bai", "pwd": "123456", "db": "smart_base"}
    ips = proxy(where="mysql", config=config)
    print(ips)
    ips = proxy()
    print(ips)

    ips.pop('146.148.220.248:808')
    ips.pop('146.148.220.248:808')
