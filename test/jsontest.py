# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/8.
# 功能:
#

from tool.jjson.basejson import *
from tool.jjson.stringjson import *

if __name__ == "__main__":
    file = "jsontest/testjson.md"
    savefile = "jsontest/testjsonformat.md"
    temp = formatStrigToFile(file, True, savefile)
    print(temp)

    jstring = '''
    {
    "adid": "",
    "aid": "",
    "aiid": "",
    "an": "",
    "andid": ""
    }'''
    jobject = stringToObject(jstring)
    print(jobject)

    print(objectToString(jobject))

    print(objectToString(jobject, True, indent=4))

    errorstring = "{dddd:ddd}"
    ok = isRightJson(errorstring)
    print(ok)

    ok = isRightJson(errorstring, True)
    print(ok)
