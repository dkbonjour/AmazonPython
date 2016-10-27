# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/11.
# 功能:
#   亚马逊排名爬虫处理逻辑器

from tool.jfile.file import *
import tool.log
from spider.download.ratedownload import *
from spider.parse.rateparse import *
from concurrent.futures import ThreadPoolExecutor
from config.config import *

# 日志
tool.log.setup_logging()
logger = logging.getLogger("smart")

# 文件位置
KEEPDIR = getconfig()["datadir"] + "/data/rateurl"

# 保存文件,减少代码
def savetofile(filepath, content=[]):
    global KEEPDIR
    dir = KEEPDIR
    if not content:
        # 保存恐慌
        filepath = filepath + "xx"
        logger.warning("空-保存到:" + filepath)
    else:
        logger.warning("保存到" + filepath)
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
        if onecontent == None or onecontent == 0:
            raise
        else:
            onecontent = onecontent.decode('utf-8', 'ignore')
        arr_oneurl, arr_onename = urlparse(onecontent)
        savetofile("oneurl.md", arr_oneurl)
        savetofile("onename.md", arr_onename)
        logger.warning("已经抓取了一级类目:" + firsturl + "的所有url...")
        logger.info(arr_oneurl)
    return arr_oneurl, arr_onename


# 二级类目
def level2(arr_oneurl, arr_onename):
    global KEEPDIR
    allfile = listfiles(KEEPDIR + "/2urls", ".md")
    emptyfile = listfiles(KEEPDIR + "/2urls", "-url.mdxx")
    for two in range(len(arr_oneurl)):
        # 已经抓过！
        prefix=str(two + 1)
        if prefix + '-url.mdxx' in emptyfile or (prefix + '-name.md' in allfile and prefix + "-url.md" in allfile):
            logger.info("已存在！第" + prefix + "个一级类目:" + arr_oneurl[two] + "的二级类目...")
            continue
        twocontent = ratedownload(arr_oneurl[two])
        if twocontent == None or twocontent==0:
            continue
        else:
            twocontent = twocontent.decode('utf-8', 'ignore')
        arr_twourl, arr_twoname = urlparse(twocontent, level=2)
        logger.warning("正抓取！第" + prefix + "个一级类目:" + arr_oneurl[two] + "的二级类目...")
        logger.warning("还剩下" + str(len(arr_oneurl) - two + 1) + "个一级类目")
        logger.info(arr_twourl)
        savetofile("2urls/" + prefix + "-url.md", arr_twourl)
        savetofile("2urls/" + prefix + "-name.md", arr_twoname)

    logger.warning("已经抓取了二级类目下的所有url...")


# 三级类目 从此处难度加大，出错，我干死自己
def level3(catchfiles=[]):
    global KEEPDIR
    # 1-url.md 2-url.md
    # 二级所有URL文件
    # 并发文件，如果传入文件，那么并发
    if not catchfiles:
        level2file = listfiles(KEEPDIR + "/2urls", "url.md")
    else:
        logger.warning("并发文件")
        level2file = catchfiles

    # 三级下所有文件
    level3file = listfiles(KEEPDIR + "/3urls", "md")
    emptyfile = listfiles(KEEPDIR + "/3urls", "-url.mdxx")

    # 遍历二级文件
    # position为文件序列
    for position in range(len(level2file)):
        # 文件名
        filename=level2file[position]
        # 文件名前缀位置
        weizhi=filename.split("-url")[0]
        urls = readfile("2urls/" + filename)
        # urlposition为链接序列
        for urlposition in range(len(urls)):
            # 已经抓过！1-2-url.md
            prefix = str(urlposition + 1)
            if weizhi + "-" + prefix + '-url.mdxx' in emptyfile or (weizhi + '-' + prefix + '-name.md' in level3file and weizhi + '-' + prefix + '-url.md' in level3file):
                logger.info("已存在！第" + weizhi + "个一级类目:" + filename + ",第" + prefix + "个二级类目：" + urls[urlposition] + "的三级类目...")
                continue
            threecontent = ratedownload(urls[urlposition])
            if threecontent == None or threecontent == 0:
                continue
            else:
                threecontent = threecontent.decode('utf-8', 'ignore')

            arr_threeurl, arr_threename = urlparse(threecontent, level=3)
            logger.warning("正抓取！第" + weizhi + "个一级类目:" + filename + ",第" + prefix + "个二级类目：" +urls[urlposition] + "的三级类目...")
            logger.warning("本目录还剩" + str(len(urls) - urlposition + 1) + "个二级类目,排队" + str(len(level2file) - position + 1) + "个一级类目")
            logger.info(arr_threeurl)
            savetofile("3urls/" + weizhi + '-' + prefix + '-url.md', arr_threeurl)
            savetofile("3urls/" + weizhi + '-' + prefix + '-name.md', arr_threename)
    logger.warning("已经抓取了三级类目下的所有url...")


# 四级类目 从此处难度加大,对！！！！
def level4(catchfiles=[]):
    global KEEPDIR
    # 1-1-url.md 1-2-url.md
    # 三级所有URL文件
    # 并发文件，如果传入文件，那么并发
    if not catchfiles:
        level3file = listfiles(KEEPDIR + "/3urls", "url.md")
    else:
        logger.warning("并发文件")
        level3file = catchfiles

    # 四级下所有文件
    level4file = listfiles(KEEPDIR + "/4urls", "md")
    emptyfile = listfiles(KEEPDIR + "/4urls", "-url.mdxx")

    # 遍历三级文件
    # position为文件序列
    for position in range(len(level3file)):
        # 文件名
        filename=level3file[position]
        # 文件名前缀位置
        weizhi=filename.split("-url")[0]

        urls = readfile("3urls/" + filename)
        # urlposition为链接序列
        for urlposition in range(len(urls)):
            # 已经抓过！1-1-1-url.md
            prefix = str(urlposition + 1)
            if weizhi + '-' + prefix + '-url.mdxx' in emptyfile or (weizhi + '-' + prefix + '-name.md' in level4file and weizhi + '-' + prefix + '-url.md' in level4file):
                logger.info("已存在！第" + str(position + 1) + "个二级类目:" + filename + ",第" + prefix + "个三级类目：" + urls[urlposition] + "的四级类目...")
                continue
            fourcontent = ratedownload(urls[urlposition])
            if fourcontent == None or fourcontent == 0:
                continue
            else:
                fourcontent = fourcontent.decode('utf-8', 'ignore')
            arr_foururl, arr_fourname = urlparse(fourcontent, level=4)
            logger.warning("正抓取！第" + str(position + 1) + "个二级类目:" + filename + ",第" + prefix + "个三级类目：" +urls[urlposition] + "的四级类目...")
            logger.warning("本目录还剩"+str(len(urls) - urlposition + 1) + "个三级类目,排队" + str(len(level3file) - position + 1) + "个二级类目")
            logger.info(arr_foururl)
            savetofile("4urls/" + weizhi + '-' + prefix + '-url.md', arr_foururl)
            savetofile("4urls/" + weizhi + '-' + prefix + '-name.md', arr_fourname)
    logger.warning("已经抓取了四级类目下的所有url...")


# 五级类目
def level5(catchfiles=[]):
    global KEEPDIR
    # 1-1-1-url.md 1-1-2-url.md
    # 四级所有URL文件
    # 并发文件，如果传入文件，那么并发
    if not catchfiles:
        level4file = listfiles(KEEPDIR + "/4urls", "url.md")
    else:
        logger.warning("并发文件")
        level4file = catchfiles

    # 五级下所有文件
    level5file = listfiles(KEEPDIR + "/5urls", "md")
    emptyfile = listfiles(KEEPDIR + "/5urls", "-url.mdxx")

    # 遍历四级文件
    # position为文件序列
    for position in range(len(level4file)):        # 文件名
        filename=level4file[position]
        # 文件名前缀位置
        weizhi=filename.split("-url")[0]

        urls = readfile("4urls/" + filename)
        # urlposition为链接序列
        for urlposition in range(len(urls)):
            # 已经抓过！1-1-1-1-url.md
            prefix = str(urlposition + 1)
            if weizhi + '-' + prefix + '-url.mdxx' in emptyfile  or (weizhi + '-' + prefix + '-name.md' in level5file and weizhi + '-' + prefix + '-url.md' in level5file):
                logger.info("已存在！第" + str(position + 1) + "个三级类目:" + filename + "，第" + prefix + "个四级类目：" + urls[urlposition] + "的五级类目...")
                continue
            fourcontent = ratedownload(urls[urlposition])
            if fourcontent == None or fourcontent == 0:
                continue
            else:
                fourcontent = fourcontent.decode('utf-8', 'ignore')
            arr_foururl, arr_fourname = urlparse(fourcontent, level=5)
            logger.warning("正抓取！第" + str(position + 1) + "个三级类目:" + filename + ",第" + prefix + "个四级类目：" +
                    urls[
                        urlposition] + "的五级类目...")
            logger.warning("本目录还剩"+str(len(urls) - urlposition + 1) + "个四级类目,排队" + str(len(level4file) - position + 1) + "个三级类目")
            logger.info(arr_foururl)
            savetofile("5urls/" + weizhi + '-' + prefix + '-url.md', arr_foururl)
            savetofile("5urls/" + weizhi + '-' + prefix + '-name.md', arr_fourname)
    logger.warning("已经抓取了五级类目下的所有url...")
    return "ok!!!----"


# 6级类目
def level6(catchfiles=[]):
    global KEEPDIR
    # 1-1-1-url.md 1-1-2-url.md
    # 四级所有URL文件
    # 并发文件，如果传入文件，那么并发
    if not catchfiles:
        level4file = listfiles(KEEPDIR + "/5urls", "url.md")
    else:
        logger.warning("并发文件")
        level4file = catchfiles

    # 五级下所有文件
    level5file = listfiles(KEEPDIR + "/6urls", "md")
    emptyfile = listfiles(KEEPDIR + "/6urls", "-url.mdxx")

    # 遍历四级文件
    # position为文件序列
    for position in range(len(level4file)):        # 文件名
        filename=level4file[position]
        # 文件名前缀位置
        weizhi=filename.split("-url")[0]

        urls = readfile("5urls/" + filename)
        # urlposition为链接序列
        for urlposition in range(len(urls)):
            # 已经抓过！1-1-1-1-url.md
            prefix = str(urlposition + 1)
            if weizhi + '-' + prefix + '-url.mdxx' in emptyfile  or (weizhi + '-' + prefix + '-name.md' in level5file and weizhi + '-' + prefix + '-url.md' in level5file):
                logger.info("已存在！第" + str(position + 1) + "个四级类目:" + filename + "，第" + prefix + "个五级类目：" + urls[urlposition] + "的六级类目...")
                continue
            fourcontent = ratedownload(urls[urlposition])
            if fourcontent == None or fourcontent == 0:
                continue
            else:
                fourcontent = fourcontent.decode('utf-8', 'ignore')
            arr_foururl, arr_fourname = urlparse(fourcontent, level=6)
            logger.warning("正抓取！第" + str(position + 1) + "个四级类目:" + filename + ",第" + prefix + "个五级类目：" +
                    urls[
                        urlposition] + "的六级类目...")
            logger.warning("本目录还剩"+str(len(urls) - urlposition + 1) + "个五级类目,排队" + str(len(level4file) - position + 1) + "个四级类目")
            logger.info(arr_foururl)
            savetofile("6urls/" + weizhi + '-' + prefix + '-url.md', arr_foururl)
            savetofile("6urls/" + weizhi + '-' + prefix + '-name.md', arr_fourname)
    logger.warning("已经抓取了六级类目下的所有url...")
    return "ok!!!----"


# 多线程
def fastlevel5(num=3):
    createjia(KEEPDIR + "/5urls")
    files = listfiles(KEEPDIR + "/4urls", "url.md")
    urls=devidelist(files,num)
    with ThreadPoolExecutor(max_workers=num) as e:
        for i in range(num):
            e.submit(level5,urls[i])


def fastlevel6(num=3):
    createjia(KEEPDIR + "/6urls")
    files = listfiles(KEEPDIR + "/5urls", "url.md")
    urls=devidelist(files,num)
    with ThreadPoolExecutor(max_workers=num) as e:
        for i in range(num):
            e.submit(level6,urls[i])


# 单线程
def ausalogic(level="all"):
    logger.warning("开跑："+level)
    global KEEPDIR
    # 创建文件夹
    createjia(KEEPDIR + "/2urls")
    createjia(KEEPDIR + "/3urls")
    createjia(KEEPDIR + "/4urls")
    createjia(KEEPDIR + "/5urls")
    createjia(KEEPDIR + "/6urls")

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
    # ausalogic("1-2")
    fastlevel5()