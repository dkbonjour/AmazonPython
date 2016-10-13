# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/11.
# 功能: 解析类目URL
#  
from lxml import etree
import tool.log
import logging

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


# 解析类目URL，分级别
def rateparse(content, level=1):
    # xpath解析需要的东西
    contents = etree.HTML(content)
    # 找到类目下的url
    temp = ""
    for i in range(level):
        temp = temp + "ul/"
    # <title dir="ltr">Robot Check</title>
    robot = contents.xpath('//title[@dir="ltr"]/text()')
    if "Robot Check" in robot:
        logger.error("机器人")
        raise Exception("机器人")
    returnurl = []
    returnname = []
    urls = contents.xpath('//ul[@id="zg_browseRoot"]/' + temp + 'li/a/@href')
    # 将目录下的url储存到数组
    for url in urls:
        returnurl.append(url)

    names = contents.xpath('//ul[@id="zg_browseRoot"]/' + temp + 'li/a/text()')
    # 将目录下的url储存到数组
    for name in names:
        returnname.append(name)
    return returnurl, returnname


def robot(content):
    # xpath解析需要的东西
    contents = etree.HTML(content)
    # <title dir="ltr">Robot Check</title>
    robot = contents.xpath('//title[@dir="ltr"]/text()')
    if "Robot Check" in robot:
        logger.error("机器人")
        raise Exception("机器人")


if __name__ == "__main__":
    level = 4
    filepath = tool.log.BASE_DIR + "/data/rate" + str(level) + ".html"
    with open(filepath, "rb") as f:
        logging.warning(rateparse(f.read().decode("utf-8", "ignore"), level=level))
