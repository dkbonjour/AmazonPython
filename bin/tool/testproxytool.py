# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/26.
# 功能: 测试代理有效
#  
import tool.log
import logging
import time
import requests
from action.proxy import *
from tool.jhttp.spider import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def testposta(url1, ip="146.148.240.241:808", which="2"):
    try:
        nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime())

        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'User-Agent': ua,
            # "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept-Language": "en-US;q=0.8,en;q=0.5",
            "Upgrade-Insecure-Requests": "1",
            # 'Referer': 'https://www.amazon.com/',
            # 'Host': 'www.amazon.com'
        }

        proxies = {"http": "http://smart:smart2016@" + ip}
        # proxies = {"http": "socks5://smart:smart2016@146.148.157.225:1080"}
        if which == "1":
            t = requests.get(url1, headers=header, proxies=proxies, timeout=60)
            return t.content
        else:
            return spider(url=url1, proxies=proxies, path=tool.log.BASE_DIR + "/data/cookie", headers=header, ua="1",
                          timeout=60)
            # print("right")
            # print(r.content)
    except Exception as e:
        print(e)
        print("error" + ip)
        raise


if __name__ == "__main__":
    local = input("IP在本地还是远程(本地1，远程2):")
    which = input("request请按1，否则2：")
    if local == "1":
        config = {"host": "192.168.0.152", "user": "bai", "pwd": "123456", "db": "smart_base"}
    else:
        config = getconfig()["basedb"]
    ips = proxy(where="mysql", config=config)
    # for ii in ips:
    #     print(ii+"-"+ips[ii][0])
    ipss = []
    iperr = []
    for i in ips:
        try:
            data = testposta("http://ip.42.pl/short", i, which)
            j=data.decode("utf-8", "ignore")
            print(j)
            if "无效用户" in j:
                raise Exception("无效用户")
            ipss.append(i)
            print(i)
        except:
            iperr.append(i)
            pass
    ipfile = tool.log.BASE_DIR + "/config/ip"
    createjia(ipfile)
    fe = open(ipfile + "/iperror.md", "wt")
    f = open(ipfile + "/ipright.md", "wt")
    for ii in iperr:
        print(ii + "-" + ips[ii][0])
        fe.write(ii + "-" + ips[ii][0] + "\n")
    fe.close()
    print("*" * 10)
    for jj in ipss:
        print(jj + "-" + ips[jj][0])
        f.write(jj + "-" + ips[jj][0] + "\n")
    f.close()
