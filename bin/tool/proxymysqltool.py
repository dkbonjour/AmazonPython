# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/14.
# 功能:
#  代理IP保存入数据库
#  IP.txt保存进数据库
from action.proxytool import *
from config.config import *

if __name__ == "__main__":
    allconfig = getconfig()
    try:
        config = allconfig["basedb"]
        # config = {"host": "localhost", "user": "root", "pwd": "6833066", "db": "smart_base"}
        savetomysql(filepath="config/base/IP.txt",config=config)
    except:
        raise Exception("数据库配置未填")