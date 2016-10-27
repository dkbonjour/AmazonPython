# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/10.
# 功能:
#  代理IP地址查询，保存文件,保存数据库辅助工具函数


import requests
from lxml import etree
from action.proxy import *
from tool.jmysql.mysql import *
import tool.log
from config.config import *

tool.log.setup_logging()
logger = logging.getLogger("proxy")


# 获取代理IP所在地址
def iplocation(ip):
    url = "http://www.ip138.com/ips138.asp?action=2&ip=" + ip
    header = {
        'User-Agent':
            'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Host': 'www.ip138.com',
    }
    res = requests.get(url, headers=header, timeout=60)
    content = res.content
    res.raise_for_status()
    html = content.decode("gbk", "ignore")
    contents = etree.HTML(html)
    location = contents.xpath('//ul[@class="ul1"]/li/text()')
    try:
        temp = str(location[1]).split("：")
        location = temp[len(temp) - 1]
    except Exception as e:
        logger.error("爬虫查找IP所在地址异常：" + ip + str(e))
        location = ""
    return location


# 获取所有代理IP地址，并存入文件
def ipalllocation(ips):
    returnips = {}
    for ip in ips:
        location = ""
        try:
            location = iplocation(ip.split(":")[0])
        except:
            pass
        if location == "":
            location = "unknown"
        logger.warning(ip + ":" + location + "处理完毕")
        returnips[ip] = location
    return returnips


# star 保存代理IP信息到本地文件
def savetofile(filepath="config/base/IPtemp.txt", savepath="config/base/IP.txt"):
    ips = []
    dir = tool.log.BASE_DIR
    with open(dir + "/" + filepath, "rt") as f:
        ips = f.readlines()
    ips = ipfilter(ips)
    temp = ipalllocation(ips)
    ipfile = open(dir + "/" + savepath, "wb")
    for i in temp:
        ipfile.write((i + "-" + temp[i] + "\n").encode("utf-8"))
    ipfile.close()


# star 保存代理IP信息到本地文件
def savetomysql(filepath="config/base/IP.txt", config={}):
    ips = proxy(filepath=filepath, config=config)
    mysql = Mysql(config)
    for ip in ips:
        sql = 'insert into smart_ip (ip,createtime,zone) values("{ip}",CURRENT_TIMESTAMP,"{zone}") on duplicate key update updatetime = CURRENT_TIMESTAMP,zone="{zone}"'
        insertsql = sql.format(ip=ip, zone=ips[ip])
        try:
            mysql.ExecNonQuery(insertsql)
            logger.warning("执行sql语句成功:" + insertsql)
        except Exception as err:
            logger.error(err, exc_info=1)


# 需手工修改，选择保存数据库或本地文件
if __name__ == "__main__":
    # 代理IP池寻找地址并保存
    # 首先往IPtemp.txt写IP，分条寻找地址所在地
    # 执行后生成IP.txt
    savetofile(filepath="config/base/IPtemp.txt", savepath="config/base/IP.txt")

