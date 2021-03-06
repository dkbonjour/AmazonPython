# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/11/5.
# 功能:
#  
import tool.log
import logging
import os

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def pingips():
    cmd = 'ping 146.148.123.199'
    # os.system(cmd)
    p = os.popen(cmd)
    data = p.read()
    if "请求超时" in data:
        print(cmd + "不通")
    else:
        print(cmd + "通!")


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
        ]
        # ,
        # "i": [
        #     "104.216.7.234-254",
        #     "104.216.18.233-254",
        #     "104.216.76.169-190",
        #     "104.216.77.41-62",
        #     "104.216.84.233-254",
        #     "104.216.91.105-126",
        #     "104.216.137.40-62",
        #     "104.216.157.168-190"
        # ],
        # "j": [
        #
        #     "104.216.135.232-254",
        #     "104.216.161.168-190",
        #     "104.216.167.104-126",
        #     "104.216.178.104-126",
        #     "104.128.112.168-190",
        #     "107.178.161.232-254",
        #     "104.143.128.232-254",
        #     "104.143.129.232-254"
        # ]

    }
    dudu = []
    for i in ips:
        for j in ips[i]:
            temp = j.split("-")
            ipend = int(temp[1])

            temptemp = temp[0].split(".")

            ipprefix = ".".join(temptemp[0:3])
            ipbegin = int(temptemp[3])
            for k in range(ipbegin, ipend + 1):
                dudu.append(ipprefix + "." + str(k) + ":808-美国加利福尼亚州洛杉矶" + i)
    with open(tool.log.BASE_DIR + "/config/base/IP.txt", "wb") as f:
        for o in dudu:
            print(o)
            f.write((o + "\n").encode("utf-8"))


if __name__ == "__main__":
    createips()
