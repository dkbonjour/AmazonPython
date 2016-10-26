# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/10.
# 功能:
#   亚马逊排名爬虫下载器

import requests
from action.proxy import *
import random
from action.useragent import *
import tool.log
from spider.parse.rateparse import *
from bs4 import BeautifulSoup
from config.config import *
from tool.jfile.file import *
from action.redispool import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


# 用来解析网页的函数
# https://www.amazon.com/Best-Sellers-Home-Kitchen-Slumber-Bags/zgbs/home-garden/166452011/ref=zg_bs_nav_hg_3_1063268/159-5712866-5514666 类目页
# 翻页+?pg=2

def ratedownload(url, where="local", config={}, retrytime=5, timeout=60):
    try:
        koip = getconfig()["koip"]
    except:
        logger.error("配置文件出错")
        exit()

    if where != "local" and not config:
        config = getconfig()["basedb"]
    if retrytime < 0:
        return None
    # 制作头部
    uas = useragent()
    if getconfig()["manyua"]:
        ua = uas[random.randint(0, len(uas) - 1)]
    else:
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'User-Agent': ua,
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept-Language": "en-US;q=0.8,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        # 'Referer': 'https://www.amazon.com/',
        'Host': 'www.amazon.com'
    }
    try:
        iperror = getconfig()["iperror"]
    except:
        logger.error("配置文件出错")
        exit()
    redisneed = getconfig()["redispool"]

    # 取IP
    if redisneed:
        ip, times, robottime = popip(getconfig()["redispoolsleeptimes"], getconfig()["redispoolname"])
        location = "no"
    else:
        ips = proxy(where=where, config=config, failtimes=iperror)

        # TODO
        # 并行真随机数，需要！！
        randomnum = allrandom(len(ips))
        try:
            if getconfig()["sleep"]:
                tt = random.randint(1, 3)
                time.sleep(tt)
                logger.error("暂停:" + str(tt) + "秒:" + url)
        except:
            logger.error("配置文件出错")
            exit()
        ip = list(ips.keys())[randomnum]
        if ip in ips.keys():
            location = ips[ip][0]
        else:
            location = "unkonw"
    proxies = {"http": "http://smart:smart2016@" + ip}
    # proxies = {
    #     'http': 'socks5://user:pass@host:port',
    #     'https': 'socks5://user:pass@host:port'
    # }
    try:
        res = requests.get(url=url, headers=header, proxies=proxies, timeout=timeout)
        if redisneed:
            logger.error(url + ":" + ip + "-" + str(times) + "-err:" + str(robottime))
        # print(res.status_code)
        res.raise_for_status()
        resdata = res.content
        res.close()

        # 不需要去掉IP
        if redisneed:
            koipv1 = False
        else:
            koipv1 = koip
        if not robot(resdata, ip, koipv1):
            return None

        logger.warning(
                "抓取URL:{url},代理IP:{ip},IP位置:{location},UA:{ua},重试次数:{times}".format(url=url, ip=ip, location=location,
                                                                                    ua=ua,
                                                                                    times=5 - retrytime))
        # 放IP
        if redisneed:
            puship(ip, times, robottime, getconfig()["redispoolname"])
        return resdata
    except Exception as err:
        # IPPOOL.pop(ip)
        # 放IP
        if redisneed:
            if (str(err) == "机器人"):
                if koip and robottime + 1 > getconfig()["rediserrmaxtimes"]:
                    pushipfuck(ip, times, robottime + 1, getconfig()["redispoolfuckname"])
                else:
                    puship(ip, times, robottime + 1, getconfig()["redispoolname"])
            else:
                puship(ip, times, robottime, getconfig()["redispoolname"])
        logger.error(err)
        logger.error("重试次数:{times}".format(times=5 - retrytime))
        logger.error(
                "抓取URL错误:{url},代理IP:{ip},IP位置:{location},UA:{ua},重试次数:{times}".format(url=url, ip=ip, location=location,
                                                                                      ua=ua,
                                                                                      times=5 - retrytime))
        return ratedownload(url=url, where=where, config=config, retrytime=retrytime - 1, timeout=timeout)


if __name__ == "__main__":
    # 一级
    level = 4
    urls = {"1": "https://www.amazon.com/Best-Sellers/zgbs",
            "2": "https://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/ref=zg_bs_nav_0/155-7707064-5178447",
            "3": "https://www.amazon.com/Best-Sellers-Appliances-Freezers/zgbs/appliances/3741331/ref=zg_bs_nav_la_2_3741261",
            "4": "https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Salad-Dressings/zgbs/grocery/16320901/ref=zg_bs_nav_gro_3_16319881"}
    for url in urls:
        if str(level) != url:
            continue
        content = ratedownload(urls[url])
        with open(tool.log.BASE_DIR + "/data/test/rate" + url + ".html", "wb") as f:
            f.write(content)

    ajaxurl = "https://www.amazon.com/Best-Sellers-Clothing-Mother-Bride-Dresses/zgbs/apparel/2969490011/161-2441050-2846244?_encoding=UTF8&pg=2&ajax=1&isAboveTheFold=0"
    content = ratedownload(ajaxurl)
    with open(tool.log.BASE_DIR + "/data/test/ajax" + ".html", "wb") as f:
        f.write(content)
