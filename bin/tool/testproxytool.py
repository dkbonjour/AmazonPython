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

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def testposta(url1, ip="146.148.240.241:808"):
    try:
        nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime())

        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            'Referer': 'https://www.amazon.com/',
            'Host': 'www.amazon.com'
        }

        proxies = {"http": "http://smart:smart2016@" + ip}
        # proxies = {"http": "socks5://smart:smart2016@146.148.157.225:1080"}
        r = requests.get(url1, headers=header, proxies=proxies)
        # print("right")
        # print(r.content)
    except Exception as e:
        print(e)
        print("error" + ip)
        raise


if __name__ == "__main__":
    local = input("本地还是远程(本地1，远程2):")
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
            testposta("https://www.amazon.com", i)
            ipss.append(i)
            print(i)
        except:
            iperr.append(i)
            pass
    fe=open("iperror.md","wt")
    f=open("ipright.md","wt")
    for ii in ipss:
        print(ii + "-" + ips[ii][0])
        fe.write(ii + "-" + ips[ii][0]+"\n")
    fe.close()
    print("*" * 10)
    for jj in iperr:
        print(jj + "-" + ips[jj][0])
        f.write(jj + "-" + ips[jj][0]+"\n")
    f.close()
