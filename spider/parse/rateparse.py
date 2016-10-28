# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/11.
# 功能: 解析类目URL
#  
from lxml import etree
import tool.log
import logging
from bs4 import BeautifulSoup
import action.proxy

# 日志
tool.log.setup_logging()
logger = logging.getLogger(__name__)


# 解析类目URL，分级别
def urlparse(content, level=1):
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


def robot(content, ip, koip=False, url=""):
    # xpath解析需要的东西
    contents = etree.HTML(content)
    # <title dir="ltr">Robot Check</title>
    try:
        robots = contents.xpath('//title/text()')
    except:
        logger.error("页数不足，机器人检测失败:" + url)
        return False
    if robots == []:
        if "Auth Result:" in content:
            raise Exception("没有标题，代理IP失效")
        logger.error("列表页无数据")
        return False
    if "Page Not Found" in robots:
        logger.error("找不到頁面:" + url)
        return False
    if "Robot Check" in robots:
        if koip:
            try:
                action.proxy.IPPOOL.pop(ip)
                logger.error("机器人，剔除IP：" + ip + ",IP池还剩：" + str(len(action.proxy.IPPOOL)))
                action.proxy.IPDEAD.append(ip)
                action.proxy.koipmysql(ip)
            except:
                pass
        raise Exception("机器人")
    return True


# 暂时用xpath，以后要使用BeautifulSoup
def rateparse(content):
    returncontent = {}
    soup = BeautifulSoup(content, 'html.parser')  # 开始解析

    items = soup.find_all('div', attrs={"class": "zg_itemImmersion"})
    for item in items:
        try:
            temp = BeautifulSoup(str(item), 'html.parser')
            rank = temp.find('span', attrs={"class": "zg_rankNumber"}).string
            rank = rank.replace(".", "")
            link = temp.find('div', attrs={"class": "zg_title"}).a["href"]
            asin = link.strip().split("/dp/")[1].split("/")[0]
            title = temp.find('div', attrs={"class": "zg_title"}).a.string
            title = title.replace(",", "")
            returncontent[rank] = [rank, asin, title]
        except:
            continue
    # contents = etree.HTML(content)
    # # rank span class="zg_rankNumber"
    # rank = contents.xpath('//span[@class="zg_rankNumber"]/text()')
    # # title link <div class="zg_title"><a  href="
    # link = contents.xpath('//div[@class="zg_title"]/a/@href')
    # title = contents.xpath('//div[@class="zg_title"]/a/text()')
    # try:
    #     for i in range(len(rank)):
    #         returncontent[rank[i].replace(".", "")] = [rank[i].replace(".", ""), link[i].replace("\n", ""), title[i].replace(",","")]
    # except:
    #     print(rank)
    #     print(link)
    #     print(title)
    #     raise
    return returncontent


if __name__ == "__main__":
    # level = 4
    dirpath = tool.log.BASE_DIR + "/data/test"
    # filepath = dirpath + "/rate" + str(level) + ".html"
    # with open(filepath, "rb") as f:
    #     print(urlparse(f.read().decode("utf-8", "ignore"), level=level))

    itemfile = dirpath + "/ajax.html"
    with open(itemfile, "rb") as f:
        items = rateparse(f.read().decode("utf-8", "ignore"))
        for item in items:
            print(item, items[item])
