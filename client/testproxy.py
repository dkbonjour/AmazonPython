# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/11/7.
# 功能:
#  
import tool.log
import logging
import requests
import time

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def createips():
    ips = {
        "d": ["146.148.149.202-254", "146.148.150.194-254", "146.148.157.194-254"],
        "e": [
            "104.143.159.232-254",
            "107.190.231.232-254",
            "104.128.118.170-190",
            "104.128.119.169-190",
            "104.128.121.41-62",
            "104.128.122.41-62",
            "104.128.123.41-62",
            "104.128.124.105-126"],
        "f": [
            "146.148.178.233-254",
            "146.148.179.168-190",
            "104.149.46.234-254",
            "104.149.64.105-126",
            "104.149.66.41-62",
            "104.149.71.41-62",
            "146.148.133.41-62",
            "146.148.176.169-190"

        ],
        "h": [
            "146.148.217.104-126",
            "146.148.220.232-254",
            "146.148.238.232-254",
            "146.148.240.232-254",
            "146.148.246.41-62",
            "146.148.247.232-254",
            "146.148.215.169-190",
            "146.148.216.41-62"
        ],
        "i": [
            "104.216.7.234-254",
            "104.216.18.233-254",
            "104.216.76.169-190",
            "104.216.77.41-62",
            "104.216.84.233-254",
            "104.216.91.105-126",
            "104.216.137.40-62",
            "104.216.157.168-190"
        ],
        "j": [

            "104.216.135.232-254",
            "104.216.161.168-190",
            "104.216.167.104-126",
            "104.216.178.104-126",
            "104.128.112.168-190",
            "107.178.161.232-254",
            "104.143.128.232-254",
            "104.143.129.232-254"
        ]

    }
    dudu = {}
    for i in ips:
        dudu[i] = []
        for j in ips[i]:
            temp = j.split("-")
            ipend = int(temp[1])

            temptemp = temp[0].split(".")

            ipprefix = ".".join(temptemp[0:3])
            ipbegin = int(temptemp[3])
            for k in range(ipbegin, ipend + 1):
                dudu[i].append(ipprefix + "." + str(k) + ":808")
    return dudu


def proxyconfig():
    #     acl ip1 myip 192.168.1.2
    # acl ip2 myip 192.168.1.3
    # acl ip3 myip 192.168.1.4
    # tcp_outgoing_address 192.168.1.2 ip1
    # tcp_outgoing_address 192.168.1.3 ip2
    # tcp_outgoing_address 192.168.1.4 ip3
    ipmap = {}
    dudu = createips()
    for i in dudu:
        k = 0
        ipmap[i] = {}
        for j in dudu[i]:
            name = i + str(k)
            ipmap[i][name] = j
            k = k + 1
    o = input("哪个配置需要：")
    for i in ipmap[o]:
        print("acl " + i + " localip " + ipmap[o][i].split(":")[0])
    for i in ipmap[o]:
        print("tcp_outgoing_address " + ipmap[o][i].split(":")[0] + " " + i)


def testproxy(proxies, url):
    try:
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            'Host': 'www.amazon.com'
        }

        r = requests.get(url, headers=header, proxies=proxies, timeout=15)
        print("结果:" + r.text)
        r.raise_for_status()
    except Exception as e:
        print(e)


def mains():
    dudu = createips()
    url = "http://ip.42.pl/short"
    o = input("测试谁:")
    for i in dudu[o]:
        print("测试：" + i)
        proxies = {"http": "http://smart:smart2016@" + i}
        testproxy(proxies, url)
        time.sleep(1)


# defh

if __name__ == "__main__":
    # proxyconfig()
    mains()