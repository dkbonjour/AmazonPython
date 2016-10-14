# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import time
import random
import tool.log
import requests
from action.useragent import *
from action.proxy import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def downloadDetail(url):
    try:
        nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime())

        # 制作头部
        uas = useragent()
        ua = uas[random.randint(0, len(uas) - 1)]

        header = {
            'User-Agent': ua,
            'Referer': 'https://www.amazon.com/',
            'Host': 'www.amazon.com'
        }

        # 加载代理ip
        ips = proxy()
        ip = list(ips.keys())[random.randint(0, len(ips) - 1)]
        if ip in ips.keys():
            location = ips[ip]
        else:
            location = "unkonw"
        proxies = {"http": "http://" + ip}

        # 不加载代理ip
        # proxies = {"http": "http://107.190.231.236:808"}
        r = requests.get(url, headers=header, proxies=proxies)
        # 保存为详情页的网址html
        with open("../data/detail" + str(nowtime) + ".html", "wb") as f:
            f.write(r.content)
            f.close()
    except:
        # 抓不到就死抓
        downloadDetail(url)


def downloaddetail():
    # 打开详情页的url
    file = open(tool.log.BASE_DIR + "/data/detailurl.txt")
    urlsline = file.readlines()

    historyread = []

    # 读取历史抓过的url
    fileread = open(tool.log.BASE_DIR + "/data/history.txt")
    readsline = fileread.readlines()
    for item in readsline:
        historyread.append(item.strip())
    fileread.close()

    for line in urlsline:
        url = line.strip()
        # 判断是否抓过
        if url in historyread:
            print("已经抓过该url...")
        else:
            print(url)
            downloadDetail(url)
            time.sleep(5)

            # 记录已经抓过的url
            history = historyread
            history.append(url)
            filehistory = open(tool.log.BASE_DIR + "/data/history.txt", "w", encoding='utf-8')
            # 记录历史记录，防止重抓
            for item in history:
                filehistory.write(item + "\n")
            filehistory.close()

    file.close()


if __name__ == "__main__":
    downloaddetail()
