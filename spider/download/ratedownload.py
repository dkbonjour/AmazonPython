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

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


# 用来解析网页的函数
# https://www.amazon.com/Best-Sellers-Home-Kitchen-Slumber-Bags/zgbs/home-garden/166452011/ref=zg_bs_nav_hg_3_1063268/159-5712866-5514666 类目页
# 翻页+?pg=2

def ratedownload(url, where="local", config={}, retrytime=5, timeout=60):
    if retrytime < 0:
        return None
    # 制作头部
    uas = useragent()
    ua = uas[random.randint(0, len(uas) - 1)]
    header = {
        'User-Agent': ua,
        'Referer': 'https://www.amazon.com/',
        'Host': 'www.amazon.com'
    }

    ips = proxy(where=where, config=config)
    ip = list(ips.keys())[random.randint(0, len(ips) - 1)]
    if ip in ips.keys():
        location = ips[ip]
    else:
        location = "unkonw"
    proxies = {"http": "http://" + ip}
    try:
        res = requests.get(url=url, headers=header, proxies=proxies, timeout=timeout)
        # print(res.status_code)
        res.raise_for_status()
        resdata = res.content
        res.close()
        robot(resdata)

        logger.warning(
                "抓取URL:{url},代理IP:{ip},IP位置:{location},UA:{ua},重试次数:{times}".format(url=url, ip=ip, location=location,
                                                                                    ua=ua,
                                                                                    times=5 - retrytime))
        return resdata
    except Exception as err:
        # IPPOOL.pop(ip)
        logger.error(
                "抓取URL错误:{url},代理IP:{ip},IP位置:{location},UA:{ua},重试次数:{times}".format(url=url, ip=ip, location=location,
                                                                                    ua=ua,
                                                                                    times=5 - retrytime))
        logging.error(err, exc_info=1)
        return ratedownload(url, retrytime - 1)


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
        with open(tool.log.BASE_DIR + "/data/rate" + url + ".html", "wb") as f:
            f.write(content)
