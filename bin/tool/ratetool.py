# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/12.
# 功能:
#   解析类目爬虫所有URL成整体，存入数据库

import tool.log
import logging
from tool.jfile.file import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger("smart")


def dealurlfile():
    # 根目录
    dir = tool.log.BASE_DIR + "/data/rateurl"

    # URL文件夹
    level1 = dir
    level2 = dir + "/2urls"
    level3 = dir + "/3urls"
    level4 = dir + "/4urls"
    level5 = dir + "/5urls"

    # 记录
    # id=filename+"-"+position name,url,parent,level
    # 1,mulu,http://dddd,0,1
    # 11,mulu,http://dddd,1,2
    # 111,mulu,http://dddd,11,3
    # 1111,mulu,http://dddd,111,4
    # 11111,mulu,http://dddd,1111,5

    listtemp = {}
    t1 = readfilelist(dir + "/oneurl.md")
    t1name = readfilelist(dir + "/onename.md")
    for i in range(min(len(t1), len(t1name))):
        listtemp[str(i+1)]=t1name[i] + "," + t1[i] + ",0,1"

    # 二级
    file2=listfiles(level2,"-url.md")
    for urlfile in file2:
        position=urlfile.replace("-url.md","")
        t2=readfilelist(level2+"/"+urlfile)
        t2name=readfilelist(level2+"/"+position+"-name.md")

        # 如果为空，跳过
        if t2==[] or t2name==[]:
            continue
        for i in range(min(len(t2), len(t2name))):
            listtemp[position.replace("-","")+str(i+1)]=t2name[i] + "," + t2[i] + ","+position.replace("-","")+",2"

    # 三级
    file3=listfiles(level3,"-url.md","")
    for urlfile in file3:
        position=urlfile.replace("-url.md","")
        t3=readfilelist(level3+"/"+urlfile)
        t3name=readfilelist(level3+"/"+position+"-name.md")

        # 如果为空，跳过
        if t2==[] or t2name==[]:
            continue
        for i in range(min(len(t3), len(t3name))):
            listtemp[position.replace("-","")+str(i+1)]=t3name[i] + "," + t3[i] + ","+position.replace("-","")+",3"

    # 四级
    file4=listfiles(level4,"-url.md")
    for urlfile in file4:
        position=urlfile.replace("-url.md","")
        t4=readfilelist(level4+"/"+urlfile)
        t4name=readfilelist(level4+"/"+position+"-name.md")

        # 如果为空，跳过
        if t2==[] or t2name==[]:
            continue
        for i in range(min(len(t4), len(t4name))):
            listtemp[position.replace("-","")+str(i+1)]=t4name[i] + "," + t4[i] + ","+position.replace("-","")+",4"

    # 四=五级
    file5=listfiles(level5,"-url.md")
    for urlfile in file5:
        position=urlfile.replace("-url.md","")
        t5=readfilelist(level5+"/"+urlfile)
        t5name=readfilelist(level5+"/"+position+"-name.md")

        # 如果为空，跳过
        if t2==[] or t2name==[]:
            continue
        for i in range(min(len(t5), len(t5name))):
            listtemp[position.replace("-","")+str(i+1)]=t5name[i] + "," + t5[i] + ","+position.replace("-","")+",5"
    with open(tool.log.BASE_DIR+"/config/URL.txt","wt") as hunterhug:
        for i in sorted(listtemp.keys()):
            hunterhug.write(i+","+listtemp[i]+"\n")
    logger.warning("记录数："+str(len(listtemp)))


if __name__ == "__main__":
    dealurlfile()
