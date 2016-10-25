# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/25.
# 功能:
#   人工打码

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tool.jhttp.spider import *


def getChmore(url, total=1):
    ip = "104.128.124.115:808"
    data = ""
    option=webdriver.ChromeOptions()
    option.add_argument(argument='--proxy-server=http://'+ip)#107.190.231.233
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(url)
    try:
        if total == 1:
            data = browser.page_source
        else:
            data = browser.find_element_by_xpath("html").text
    except NoSuchElementException:
        print("神马都没有")
    return browser, data


if __name__ == '__main__':
    url = "http://www.amazon.com"
    # # browers, data = getChmore(url=url, total=0)
    # print(data)
    # browers.close()
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.3; x64; rv:26.0) Gecko/20121011 Firefox/26",
        'Referer': 'https://www.amazon.com/',
        'Host': 'www.amazon.com'
    }
    data=spider(url=url,daili="107.190.231.233:808",headers=header)
    print(data.decode("utf-8","ignore"))