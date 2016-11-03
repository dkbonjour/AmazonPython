# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/11/3.
# 功能:
#  
import tool.log
import logging
from bs4 import BeautifulSoup
from tool.jfile.file import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)

def takeimg(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')  # 开始解析
        j=soup.find("input",attrs={"id":"cerberus-metrics"})["value"]
        print(j)
    except:
        print("ss")


if __name__ == "__main__":
    # dir=tool.log.BASE_DIR+"/robot"
    # allfile=listfiles(dir,".html")
    # print(allfile)
    s=''' <input type="hidden" name="" value="/gp/cerberus/log/gv/mid/ATVPDKIKX0DER/asin/B003Y22RDO/rc/19/subs/-/dev/WEB" id="cerberus-metrics">'''
    takeimg(s)
    if "sss" !=None:
        print("dd")