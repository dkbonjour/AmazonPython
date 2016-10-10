# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/10.
# 功能:
#  代理IP地址查询，保存文件,保存数据库


from tool.jhttp.spider import *
from lxml import etree
from action.proxy import *
from tool.jmysql.mysql import *

setup_logging()
logger = logging.getLogger("proxy")
smartlogger = logging.getLogger("smart")


# 获取代理IP所在地址
def iplocation(ip):
    url = "http://www.ip138.com/ips138.asp?action=2&ip=" + ip
    header = {
        'User-Agent':
            'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Host': 'www.ip138.com',
    }
    content = spider(url, headers=header)
    html = content.decode("gbk", "ignore")
    contents = etree.HTML(html)
    location = contents.xpath('//ul[@class="ul1"]/li/text()')
    try:
        temp = str(location[1]).split("：")
        location = temp[len(temp) - 1]
    except Exception as e:
        logger.error("爬虫查找IP所在地址异常：" + ip + e)
        location = ""
    logger.info(ip + ":" + location + "处理完毕")
    return location


# 获取所有代理IP地址，并存入文件
def ipalllocation(ips):
    returnips = {}
    for ip in ips:
        location = iplocation(ip.split(":")[0])
        if location != "":
            returnips[ip] = location
        else:
            returnips[ip] = "未知IP"
    return returnips


# star 保存代理IP信息到本地文件
def savetofile(savepath="../config/IP.txt"):
    ips, _ = proxy(filepath="../config/IPtemp.txt")
    temp = ipalllocation(ips)
    ipfile = open(savepath, "wb")
    for i in temp:
        ipfile.write((i + "-" + temp[i] + "\n").encode("utf-8"))
    ipfile.close()


# star 保存代理IP信息到本地文件
def savetomysql(filepath="../config/IP.txt", config={}):
    ips, _ = proxy(filepath=filepath)
    mysql = Mysql(config)
    for ip in ips:
        sql = 'insert into smart_ip (ip,createtime,zone) values("{ip}",CURRENT_TIMESTAMP,"{zone}") on duplicate key update updatetime = CURRENT_TIMESTAMP,zone="{zone}"'
        insertsql = sql.format(ip=ip, zone=ips[ip])
        try:
            mysql.ExecNonQuery(insertsql)
            logger.info("执行sql语句成功:" + insertsql)
        except:
            logger.error("执行sql语句失败:" + insertsql)


# 需手工修改，选择保存数据库或本地文件
if __name__ == "__main__":
    # 代理IP池寻找地址并保存
    # 首先往IPtemp.txt写IP，分条寻找地址所在地
    # 执行后生成IP.txt
    # savetofile()

    # 保存代理IP数据库
    # IP.txt保存进数据库
    config = {"host": "localhost", "user": "root", "pwd": "6833066", "db": "smart_base"}
    savetomysql(config=config)