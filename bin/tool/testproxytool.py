# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/26.
# 功能: 测试代理有效
#
import time
import requests
from action.proxy import *
from tool.jhttp.spider import *


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

        proxies = {"http": "http://"+ getconfig()["proxypwd"] + ip}
        # proxies = {"http": "socks5://smart:smart2016@146.148.157.225:1080"}
        if which == "1":
            t = requests.get(url1, headers=header, proxies=proxies, timeout=10)
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
    local = input("IP在本地还是远程(本地数据库1，远程数据库2，本地文件3):")
    which = input("request请按1，否则2：")
    ipfile = tool.log.BASE_DIR + "/config/ip"
    createjia(ipfile)
    if local == "1":
        config = {"host": "127.0.0.1", "user": "root", "pwd": "6833066", "db": "smart_base"}
        ips = proxy(where="mysql", config=config)
    elif local == "2":
        config = getconfig()["basedb"]
        ips = proxy(where="mysql", config=config)
    else:
        temp = {}
        print(ipfile + "/iptest.md")
        ips = readfilelist(ipfile + "/iptest.md")
        print(ips)
        for i in ips:
            i = i.split("-")[0]
            temp[i] = ["美国加利福尼亚州洛杉矶"]
        ips = temp
    ipss = []
    iperr = []
    for i in ips:
        try:
            data = testposta("http://ip.42.pl/short", i, which)
            j = data.decode("utf-8", "ignore")
            print("网站内容：" + j)
            if "无效用户" in j:
                print("无效用户: " + i)
                continue
            ipss.append(i)
        except:
            iperr.append(i)
            pass
    todays = todaystring(6)
    fe = open(ipfile + "/" + todays + "iperror.md", "wb")
    f = open(ipfile + "/" + todays + "ipright.md", "wb")
    for jj in ipss:
        print(jj + "-" + ips[jj][0])
        f.write((jj + "-" + ips[jj][0] + "\n").encode("utf-8"))
    f.close()
    print("err" + "*" * 10)
    for ii in iperr:
        print(ii + "-" + ips[ii][0])
        fe.write((ii + "-" + ips[ii][0] + "\n").encode("utf-8"))
    fe.close()
