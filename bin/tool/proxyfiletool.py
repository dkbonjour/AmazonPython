# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/10.
# 功能:
# 代理IP保存入文件
# 代理IP池寻找地址并保存
# 首先往IPtemp.txt读IP，分条寻找地址所在地
# 执行写入IP.txt
from action.proxytool import *

if __name__ == "__main__":
    savetofile(filepath="config/base/IPtemp.txt", savepath="config/base/IP.txt")
