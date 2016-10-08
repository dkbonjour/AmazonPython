# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/8.
# 功能:
#
from tool.jhttp.spider import *

if __name__ == "__main__":
    print(getHtml("http://www.baidu.com").decode("utf-8", "ignore"))

    url = "http://dd.com?" + urlencode({"dd": "Ddd", "你好": 3})
    print(url)
