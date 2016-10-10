# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/10.
# 功能:
#
import requests
from action.proxy import *
import random

#cxdsfsdfdsffdsf

# 日志
setup_logging()
logger = logging.getLogger(__name__)


# 用来解析网页的函数
def download(url):
    # 制作头部
    header = {
        'User-Agent': 'ozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        'Referer': 'https://www.amazon.com/',
        'Host': 'www.amazon.com'
    }

    # 取IP池
    # 每一次生成一个随机数
    # 用来读取ip群的随机一个ip
    if not IPPOOLSUCCESS:
        proxy()

    ipsize=len(IPPOOL)
    if
    r = random.randint(0, ipsize- 1)
    try:
        proxies = {"http": ips[r]}
        res = requests.get(url=url, headers=header, proxies=proxies)
        resdata = res.content
        return resdata
    except Exception as err:
        # 如果排名r的ip失效，那么剔除这个ip
        # 但是这里没有考虑r为0或者len(ip)
        # 如果r出现了这个数就会出现数组报错，超过长度的报错
        del ips[r]

        logger.error(err)

        # 换一个ip来抓取
        r = random.randint(0, len(ips) - 1)
        proxies = {"http": ips[r - 1]}

        res = requests.get(url=url, headers=header, proxies=proxies)
        # ('UTF-8')('unicode_escape')('gbk','ignore')
        resdata = res.content
        return resdata
        print("暂停20秒")
        time.sleep(20)
        get(url)
