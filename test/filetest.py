# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/8.
# 功能:
#
from tool.jfile.file import *

if __name__ == "__main__":
    path = "./filetest"
    createjia(path)
    content = [['第一列', '第二列'], ['１', '２']]
    writeexcel(path + "/" + todaystring(4) + ".xlsx", content)
    print(filetype('./filetest/22.gif'))
    print(filetype('./filetest/23.jpg'))

    print(filejoin(['.', "data", "test"]))

    print(todaystring(4))

    print(listfiles('../tool','.py',False))
    print(listfiles('../tool','.py',True))
