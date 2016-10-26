# !/usr/bin/python3.4
# -*-coding:utf-8-*-
# Created by Smartdo Co.,Ltd. on 2016/10/25.
# 功能:
#   人工打码

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tool.jhttp.spider import *
import requests
from base64 import b64encode
from action.redispool import *
from lxml import etree


def getFirefox(url, ip, total=1):
    data = ""
    proxy = {
        "host": ip.split(":")[0],
        "port": ip.split(":")[1],
        "user": "smart",
        "pass": "smart2016"
    }
    profile = webdriver.FirefoxProfile()
    # add new header
    profile.add_extension("../modify_headers-0.7.1.1-fx.xpi")
    profile.set_preference("extensions.modify_headers.currentVersion", "0.7.1.1-fx")
    profile.set_preference("modifyheaders.config.active", True)
    profile.set_preference("modifyheaders.headers.count", 1)
    profile.set_preference("modifyheaders.headers.action0", "Add")
    profile.set_preference("modifyheaders.headers.name0", "Proxy-Switch-Ip")
    profile.set_preference("modifyheaders.headers.value0", "yes")
    profile.set_preference("modifyheaders.headers.enabled0", True)

    # add proxy
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', proxy['host'])
    profile.set_preference('network.proxy.http_port', int(proxy['port']))
    profile.set_preference('network.proxy.no_proxies_on', 'localhost, 127.0.0.1')

    # Proxy auto login
    profile.add_extension('../close_proxy_authentication-1.1-sm+tb+fx.xpi')
    credentials = '{user}:{pass}'.format(**proxy)
    credentials = b64encode(credentials.encode('ascii')).decode('utf-8')
    profile.set_preference('extensions.closeproxyauth.authtoken', credentials)
    browser = webdriver.Firefox(profile)
    browser.get(url)
    try:
        if total == 1:
            data = browser.page_source
        elif total == 0:
            data = browser.find_element_by_xpath("html").text
        else:
            pass
    except NoSuchElementException:
        print("神马都没有")
    return browser, data


def testposta(url1, ip="146.148.240.241:808"):
    try:

        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            'Referer': 'https://www.amazon.com/',
            'Host': 'www.amazon.com'
        }

        proxies = {"http": "http://smart:smart2016@" + ip}
        r = requests.get(url1, headers=header, proxies=proxies, timeout=100)
        r.raise_for_status()
        robot(r.content.decode("utf-8", "ignore"))

    except Exception as e:
        print(e)
        print("error:" + ip)
        raise


def robot(content):
    # xpath解析需要的东西
    contents = etree.HTML(content)
    # <title dir="ltr">Robot Check</title>
    try:
        robot = contents.xpath('//title/text()')
    except:
        print("页数不足，机器人检测失败")
    if "Robot Check" in robot:
        raise Exception("机器人")


if __name__ == '__main__':
    url = "https://www.amazon.com"
    print("准备解救IP们！！！时刻准备好人工打码")
    while True:
        try:
            ip, times, robbottime = popip(0, getconfig()["redispoolfuckname"])
            print(ip + "准备好了！！！")
            # ip=""
            # # ip="111.13.65.244:80"
            browers, data = getFirefox(url=url, ip=ip)
            time.sleep(20)
            try:
                testposta("https://www.amazon.com", ip)
            except:
                print("没能解救" + ip)
                puship(ip, times, robbottime, getconfig()["redispoolfuckname"])
                browers.close()
                continue
            browers.close()
            print("解救了" + ip)
            puship(ip, times, 0, getconfig()["redispoolname"])
        except Exception as e:
            print(e)
            if "Failed to decode" in str(e):
                print("解救了" + ip)
                puship(ip, times, 0, getconfig()["redispoolname"])
            else:
                print("没能解救" + ip)
                puship(ip, times, robbottime, getconfig()["redispoolfuckname"])
