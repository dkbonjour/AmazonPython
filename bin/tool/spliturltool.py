# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/22.
# 功能:
#   切割config/base中的URL文件
from  tool.jfile.file import *

if __name__ == "__main__":
    filename = input("你想切割config/base文件夹中哪个文件：")
    with open("../../config/base/" + filename, "rt") as f:
        j = f.readlines()
        shu = len(j)
        print("数量:" + str(shu))
        num = input("切割几份：")
        num = int(num)
        dd = int(shu / num)
        print(dd)
        for i in range(1, num + 1):
            with open("../../config/base/" + str(i) + "-" + filename, "wt") as ff:
                if i == num + 1:
                    ff.writelines(j[(i - 1) * dd:])
                else:
                    ff.writelines(j[(i - 1) * dd:(i * dd) + 1])
