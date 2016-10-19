# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/14.
# 功能:
#  
import tool.log
import logging
from tool.jjson.basejson import *


# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)

CONFIG = None
CONFIGSUCCESS = False

def getconfig(filepath="config/config.json"):
    global CONFIG
    global CONFIGSUCCESS
    if CONFIGSUCCESS:
        return CONFIG
    with open(tool.log.BASE_DIR + "/" + filepath, "rb") as f:
        content = f.read().decode("utf-8", "ignore")
        error, right = isRightJson(content, True)
        if not right:
            exit()
        else:
            CONFIG = stringToObject(content)
            # TODO
            # 配置检查
            CONFIGSUCCESS = True
            return CONFIG


def copyright(info):
    us = getconfig()
    temp = {}
    temp["info"] = info
    temp["version"] = us["version"]
    temp["company"] = us["company"]
    temp["people"] = us["developer"]
    temp["time"] = us["time"]
    hehe = '''
    所属公司：{company}
    开发人员：{people}
    编译时间：{time}
    软件版本：{version}

    {info}
    '''.format_map(temp)
    return hehe


if __name__ == "__main__":
    print(getconfig())
    print(copyright("爬虫大霸王开始运行"))
