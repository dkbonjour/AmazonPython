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
from tool.jhttp.spider import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)
loggers = logging.getLogger("smart")

# 用来解析网页的函数
# https://www.amazon.com/Best-Sellers-Home-Kitchen-Slumber-Bags/zgbs/home-garden/166452011/ref=zg_bs_nav_hg_3_1063268/159-5712866-5514666 类目页
# 翻页+?pg=2
ROBBOTTIME = 0


def ratedownload(url, where="local", config={}, retrytime=5, timeout=60, header={}):
    cookiefile = ""
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
    # UA编号
    uano = 0
    if getconfig()["manyua"]:
        uas = useragent()
        ua = uas[random.randint(0, len(uas) - 1)]
        temp = ua.split("*")
        uano = temp[0]
        ua = temp[1]
    else:
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"
    if header == {}:
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'User-Agent': ua,
            # "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept-Language": "en-US;q=0.8,en;q=0.5",
            "Upgrade-Insecure-Requests": "1",
            # 'Referer': 'https://www.amazon.com/',
            'Host': 'www.amazon.com'
        }
    else:
        header['User-Agent'] = ua
    try:
        iperror = getconfig()["iperror"]
    except:
        logger.error("配置文件出错")
        exit()
    redisneed = getconfig()["redispool"]

    # 取IP
    ip = "127.0.0.1"
    location = "no"
    times = 0
    robottime = 0
    if getconfig()["proxy"]:
        if redisneed:
            ip, times, robottime = popip(getconfig()["redispoolsleeptimes"], getconfig()["redispoolname"])
        else:
            ips = proxy(where=where, config=config, failtimes=iperror)

            # TODO
            # 并行真随机数，需要！！
            randomnum = allrandom(len(ips))
            try:
                secord = getconfig()["sleeptimes"]
                secord = random.randint(secord, secord + 3)
                time.sleep(secord)
                logger.warning("暂停:" + str(secord) + "秒:" + url)
            except:
                logger.error("配置文件出错")
                exit()
            ip = list(ips.keys())[randomnum]
            if ip in ips.keys():
                location = ips[ip][0]
            else:
                location = "unkonw"
    proxies = {"http": "http://" + getconfig()["proxypwd"] + ip}
    # proxies = {
    #     'http': 'socks5://user:pass@host:port',
    #     'https': 'socks5://user:pass@host:port'
    # }
    try:
        # manycookie
        if getconfig()["manycookie"]:
            cookiefile = getconfig()["datadir"] + "/cookie" + "/" + ip + "-" + uano + '.txt'
            if getconfig()["proxy"]:
                if fileexsit(cookiefile)==False:
                    mulspider(url=url, proxies=proxies, headers=header, ua=uano,
                                 path=getconfig()["datadir"] + "/cookie",
                                 timeout=timeout)
                resdata = mulspider(url=url, proxies=proxies, headers=header, ua=uano,
                                 path=getconfig()["datadir"] + "/cookie",
                                 timeout=timeout)
            else:
                if fileexsit(cookiefile)==False:
                    mulspider(url=url, proxies=proxies, headers=header, ua=uano,
                                 path=getconfig()["datadir"] + "/cookie",
                                 timeout=timeout)
                resdata = mulspider(url=url, headers=header, ua=uano, path=getconfig()["datadir"] + "/cookie",
                                 timeout=timeout)
        else:
            if getconfig()["proxy"]:
                res = requests.get(url=url, headers=header, proxies=proxies, timeout=timeout)
            else:
                res = requests.get(url=url, headers=header, timeout=timeout)
            # print(res.status_code)
            res.raise_for_status()
            resdata = res.content
            res.close()
        if redisneed and getconfig()["proxy"]:
            logger.warning(
                    "抓取URL:{url},代理IP:{ip},IP位置:{location},UA:{ua},重试次数:{times}".format(url=url, ip=ip + "-" + str(
                            times) + "-err:" + str(robottime), location=location, ua=ua, times=5 - retrytime))

        else:
            logger.warning(
                    "抓取URL:{url},代理IP:{ip},IP位置:{location},UA:{ua},重试次数:{times}".format(url=url, ip=ip,
                                                                                        location=location,
                                                                                        ua=ua,
                                                                                        times=5 - retrytime))

        # 不需要去掉IP
        if redisneed:
            koipv1 = False
        else:
            koipv1 = koip
        if getconfig()["proxy"] and not robot(resdata, ip, koipv1, url):
            # 放IP
            if redisneed:
                puship(ip, times, robottime, getconfig()["redispoolname"])

            # 頁數不足
            # 或者找不到頁面
            return 0

        # 放IP
        if redisneed and getconfig()["proxy"]:
            puship(ip, times, robottime, getconfig()["redispoolname"])
        loggers.error(ip + "   |" + url)
        return resdata
    except Exception as err:
        if getconfig()["manycookie"]:
            if (str(err) == "机器人"):
                try:
                    pass
                    # os.remove(cookiefile)
                except:
                    pass
        if redisneed and getconfig()["proxy"]:
            if (str(err) == "机器人"):
                global ROBBOTTIME
                ROBBOTTIME = ROBBOTTIME + 1
                if koip and robottime + 1 > getconfig()["rediserrmaxtimes"]:
                    pushipfuck(ip, times, robottime + 1, getconfig()["redispoolfuckname"])
                else:
                    puship(ip, times, robottime + 1, getconfig()["redispoolname"])
                if getconfig()["urlrobotstop"]:
                    if ROBBOTTIME > getconfig()["processnum"]*5:
                        logger.error("超大睡眠！严重被防爬虫" + str(getconfig()["urlstoptime"] * 5) + "秒")
                        time.sleep(getconfig()["urlstoptime"] * 60)
            else:
                if getconfig()["notrobbotkoip"]:
                    logger.error("其他问题：干掉" + ip)
                    pass
                else:
                    puship(ip, times, robottime, getconfig()["redispoolname"])
        logger.error(err)
        if redisneed and getconfig()["proxy"]:
            logger.error(
                    "失敗抓取URL:{url},代理IP:{ip},IP位置:{location},UA:{ua},重试次数:{times}".format(url=url, ip=ip + "-" + str(
                            times) + "-err:" + str(robottime), location=location, ua=ua, times=5 - retrytime))

        else:
            logger.error(
                    "失敗抓取URL:{url},代理IP:{ip},IP位置:{location},UA:{ua},重试次数:{times}".format(url=url, ip=ip,
                                                                                          location=location,
                                                                                          ua=ua,
                                                                                          times=5 - retrytime))
        return ratedownload(url=url, where=where, config=config, retrytime=retrytime - 1, timeout=timeout,
                            header=header)


def downloaddetail():
    # ajaxurl = input("https://www.amazon.com/Best-Sellers-Home-Improvement-Fuse-Accessories/zgbs/hi/6355934011 ：")
    # ajaxurl="https://www.amazon.com/dp/B017KUENH8"
    tt = readfilelist(tool.log.BASE_DIR + "/data/test/url.html")
    print(tt)
    for i in range(len(tt)):
        try:
            content = ratedownload(tt[i].strip().replace("'", "").replace("\r", ""))
            dudu = tool.log.BASE_DIR + "/data/phonelist/detail" + str(i) + ".html"
            with open(dudu, "wb") as f:
                f.write(content)
            print(dudu)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    downloaddetail()
