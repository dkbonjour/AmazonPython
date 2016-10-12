# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/11.
# 功能:
#   亚马逊排名爬虫处理逻辑器

from tool.jfile.file import *
import tool.log
from spider.download.ratedownload import *
from spider.parse.rateparse import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)
KEEPDIR = tool.log.BASE_DIR + "/data/rateurl"


# 保存文件,减少代码
def savetofile(filepath, content=[]):
    # 空内容
    if not content:
        return
    global KEEPDIR
    dir = KEEPDIR
    with open(dir + "/" + filepath, "w") as f:
        for i in content:
            f.write(i + "\n")


# 读取URL文件内容
def readfile(filepath):
    global KEEPDIR
    dir = KEEPDIR
    return readfilelist(dir + "/" + filepath)


# 一级类目
def level1():
    global KEEPDIR
    allfile = listfiles(KEEPDIR, ".md")
    if 'onename.md' in allfile and "oneurl.md" in allfile:
        arr_oneurl = readfile("oneurl.md")
        arr_onename = readfile("onename.md")
        logger.warning("一级类目已经存在，直接抓取二级类目的url...")
    else:
        # 下面是一级类目的抓取
        # 一级目录下的网址
        firsturl = "https://www.amazon.com/Best-Sellers/zgbs"
        onecontent = ratedownload(firsturl)
        if onecontent == None:
            raise
        else:
            onecontent = onecontent.decode('utf-8', 'ignore')
        arr_oneurl, arr_onename = rateparse(onecontent)
        savetofile("oneurl.md", arr_oneurl)
        savetofile("onename.md", arr_onename)
        logger.warning("已经抓取了一级类目:" + firsturl + "的所有url...")
        logger.info(arr_oneurl)
    return arr_oneurl, arr_onename


# 二级类目
def level2(arr_oneurl, arr_onename):
    global KEEPDIR
    allfile = listfiles(KEEPDIR + "/2urls", ".md")
    for two in range(len(arr_oneurl)):
        # 已经抓过！
        if str(two + 1) + '-name.md' in allfile and str(two + 1) + "-url.md" in allfile:
            logger.warning("已存在！已经抓取了第" + str(two + 1) + "个一级类目:" + arr_oneurl[two] + "的二级类目...")
            continue

        twocontent = ratedownload(arr_oneurl[two])
        if twocontent == None:
            continue
        else:
            twocontent = twocontent.decode('utf-8', 'ignore')
        arr_twourl, arr_twoname = rateparse(twocontent, level=2)
        logger.warning("已经抓取了第" + str(two + 1) + "个一级类目:" + arr_oneurl[two] + "的二级类目...")
        logger.info(arr_twourl)
        savetofile("2urls/" + str(two + 1) + "-url.md", arr_twourl)
        savetofile("2urls/" + str(two + 1) + "-name.md", arr_twoname)

    logger.warning("已经抓取了二级类目下的所有url...")


# 三级类目 从此处难度加大
def level3():
    global KEEPDIR
    # 1-url.md 2-url.md
    # 二级所有URL文件
    level2file = listfiles(KEEPDIR + "/2urls", "url.md")

    # 三级下所有文件
    level3file = listfiles(KEEPDIR + "/3urls", "md")

    # 遍历二级文件
    # position为文件序列
    for position in range(len(level2file)):
        urls = readfile("2urls/" + level2file[position])
        # urlposition为链接序列
        for urlposition in range(len(urls)):
            # 已经抓过！1-2-url.md
            if str(position + 1) + '-' + str(urlposition + 1) + '-name.md' in level3file and str(
                            position + 1) + '-' + str(urlposition + 1) + '-url.md' in level3file:
                logger.warning("已存在！已经抓取了第" + str(position + 1) + "个一级类目，第" + str(urlposition + 1) + "个二级类目：" + urls[
                urlposition] + "的三级类目...")
                continue
            threecontent = ratedownload(urls[urlposition])
            if threecontent == None:
                continue
            else:
                threecontent = threecontent.decode('utf-8', 'ignore')

            arr_threeurl, arr_threename = rateparse(threecontent, level=3)
            logger.warning("已经抓取了第" + str(position + 1) + "个一级类目，第" + str(urlposition + 1) + "个二级类目：" + urls[
                urlposition] + "的三级类目...")
            logger.info(arr_threeurl)
            savetofile("3urls/" + str(position + 1) + '-' + str(urlposition + 1) + '-url.md', arr_threeurl)
            savetofile("3urls/" + str(position + 1) + '-' + str(urlposition + 1) + '-name.md', arr_threename)
    logger.warning("已经抓取了三级类目下的所有url...")


# 四级类目 从此处难度加大
def level4():
    global KEEPDIR
    # 1-1-url.md 1-2-url.md
    # 三级所有URL文件
    level3file = listfiles(KEEPDIR + "/3urls", "url.md")

    # 四级下所有文件
    level4file = listfiles(KEEPDIR + "/4urls", "md")

    # 遍历三级文件
    # position为文件序列
    for position in range(len(level3file)):
        urls = readfile("3urls/" + level3file[position])
        prefix = level3file[position].replace("-url.md", "")  # 1-1-url.md
        # urlposition为链接序列
        for urlposition in range(len(urls)):
            # 已经抓过！1-1-1-url.md
            if prefix + '-' + str(urlposition + 1) + '-name.md' in level4file and prefix + '-' + str(
                            urlposition + 1) + '-url.md' in level4file:
                logger.warning("已存在！已经抓取了第" + str(position + 1) + "个二级类目，第" + str(urlposition + 1) + "个三级类目：" + urls[
                urlposition] + "的四级类目...")
                continue
            fourcontent = ratedownload(urls[urlposition])
            if fourcontent == None:
                continue
            else:
                fourcontent = fourcontent.decode('utf-8', 'ignore')
            arr_foururl, arr_fourname = rateparse(fourcontent, level=4)
            logger.warning("已经抓取了第" + str(position + 1) + "个二级类目，第" + str(urlposition + 1) + "个三级类目：" + urls[
                urlposition] + "的四级类目...")
            logger.info(arr_foururl)
            savetofile("4urls/" + prefix + '-' + str(urlposition + 1) + '-url.md', arr_foururl)
            savetofile("4urls/" + prefix + '-' + str(urlposition + 1) + '-name.md', arr_fourname)
    logger.warning("已经抓取了四级类目下的所有url...")


# 五级类目
def level5():
    global KEEPDIR
    # 1-1-1-url.md 1-1-2-url.md
    # 四级所有URL文件
    level4file = listfiles(KEEPDIR + "/4urls", "url.md")

    # 五级下所有文件
    level5file = listfiles(KEEPDIR + "/5urls", "md")

    # 遍历四级文件
    # position为文件序列
    for position in range(len(level4file)):
        urls = readfile("4urls/" + level4file[position])
        prefix = level4file[position].replace("-url.md", "")  # 1-1-url.md
        # urlposition为链接序列
        for urlposition in range(len(urls)):
            # 已经抓过！1-1-1-1-url.md
            if prefix + '-' + str(urlposition + 1) + '-name.md' in level5file and prefix + '-' + str(
                            urlposition + 1) + '-url.md' in level5file:
                logger.warning("已存在！抓取了第" + str(position + 1) + "个三级类目，第" + str(urlposition + 1) + "个四级类目：" + urls[
                urlposition] + "的五级类目...")
                continue
            fourcontent = ratedownload(urls[urlposition])
            if fourcontent == None:
                continue
            else:
                fourcontent = fourcontent.decode('utf-8', 'ignore')
            arr_foururl, arr_fourname = rateparse(fourcontent, level=5)
            logger.warning("已经抓取了第" + str(position + 1) + "个三级类目，第" + str(urlposition + 1) + "个四级类目：" + urls[
                urlposition] + "的五级类目...")
            logger.info(arr_foururl)
            savetofile("5urls/" + prefix + '-' + str(urlposition + 1) + '-url.md', arr_foururl)
            savetofile("5urls/" + prefix + '-' + str(urlposition + 1) + '-name.md', arr_fourname)
    logger.warning("已经抓取了五级类目下的所有url...")


def ausalogic(level="all"):
    global KEEPDIR
    # 创建文件夹
    createjia(KEEPDIR + "/2urls")
    createjia(KEEPDIR + "/3urls")
    createjia(KEEPDIR + "/4urls")
    createjia(KEEPDIR + "/5urls")

    # 一级目录！
    if level == "1-2":
        arr_oneurl, arr_onename = level1()
        level2(arr_oneurl, arr_onename)
    elif level == "2-3":
        level3()
    elif level == "3-4":
        level4()
    elif level == "4-5":
        level5()
    else:
        arr_oneurl, arr_onename = level1()
        level2(arr_oneurl, arr_onename)
        level3()
        level4()
        level5()


if __name__ == "__main__":
    ausalogic("1-2")
