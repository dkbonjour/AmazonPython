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


def getconfig(filepath="config/config.json"):
    with open(tool.log.BASE_DIR + "/" + filepath, "rb") as f:
        content = f.read().decode("utf-8","ignore")
        error, right = isRightJson(content, True)
        if not right:
            raise error
        else:
            return stringToObject(content)


if __name__ == "__main__":
    print(getconfig())
