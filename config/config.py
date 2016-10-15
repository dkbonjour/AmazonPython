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

def copyright(info):
    us=getconfig()
    temp={}
    temp["info"]=info
    temp["version"] = us["version"]
    temp["company"]=us["company"]
    temp["people"]=us["developer"]
    temp["time"]=us["time"]
    hehe='''
    所属公司：{company}
    开发人员：{people}
    编译时间：{time}
    软件版本：{version}

    {info}
    '''.format_map(temp)
    print(hehe)


if __name__ == "__main__":
    print(getconfig())
    copyright("爬虫大霸王开始运行")
