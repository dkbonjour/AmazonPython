# -*-coding:utf-8-*-
# Created by 一只尼玛 on 16-8-26.
# 功能:
# 　抓取网页

import urllib.request, urllib.parse, http.cookiejar
import os, time, re
import http.cookies


# 时间函数
def timetochina(longtime, formats='{}天{}小时{}分钟{}秒'):
    day = 0
    hour = 0
    minutue = 0
    second = 0
    try:
        if longtime > 60:
            second = longtime % 60
            minutue = longtime // 60
        else:
            second = longtime
        if minutue > 60:
            hour = minutue // 60
            minutue = minutue % 60
        if hour > 24:
            day = hour // 24
            hour = hour % 24
        return formats.format(day, hour, minutue, second)
    except:
        raise Exception('时间非法')


# star 自己封装的抓取函数,单机应用
def spider(url, daili='', postdata={}, headers={}):
    """
    抓取网页：支持cookie
    第一个参数为网址，第二个为POST的数据
    """

    # 头部重包
    header = []
    for i in headers:
        header.append((i, headers[i]))
    # print(header)

    # COOKIE文件保存路径
    filename = "./cookie/" + daili.split(":")[0] + '-cookie.txt'

    # 声明一个MozillaCookieJar对象实例保存在文件中
    cj = http.cookiejar.MozillaCookieJar(filename)
    # cj =http.cookiejar.LWPCookieJar(filename)

    # 从文件中读取cookie内容到变量
    # ignore_discard的意思是即使cookies将被丢弃也将它保存下来
    # ignore_expires的意思是如果在该文件中 cookies已经存在，则覆盖原文件写
    # 如果存在，则读取主要COOKIE
    if os.path.exists(filename):
        cj.load(filename, ignore_discard=True, ignore_expires=True)
    # 读取其他COOKIE
    if os.path.exists('../subcookie.txt'):
        cookie = open('../subcookie.txt', 'r').read()
    else:
        cookie = ''
    # 建造带有COOKIE处理器的打开专家
    proxy_support = urllib.request.ProxyHandler({'http': 'http://' + daili})
    # 开启代理支持
    if daili:
        # print('代理:' + daili + '启动')
        opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPCookieProcessor(cj),
                                             urllib.request.HTTPHandler)
    else:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    if header:
        pass
    else:
        header = [('User-Agent',
                   'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'),
                  ('Referer', 'http://s.m.taobao.com'),
                  ('Host', 'h5.m.taobao.com'),
                  ('Cookie', cookie)]
    # 打开专家加头部
    opener.addheaders = header

    # 分配专家
    urllib.request.install_opener(opener)
    # 有数据需要POST
    if postdata:
        # 数据URL编码
        postdata = urllib.parse.urlencode(postdata)

        # 抓取网页
        html_bytes = urllib.request.urlopen(url, postdata.encode()).read()
    else:
        html_bytes = urllib.request.urlopen(url).read()

    # 保存COOKIE到文件中
    cj.save(ignore_discard=True, ignore_expires=True)
    return html_bytes


def alone(url, daili):
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        # "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept-Language": "en-US;q=0.8,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        # 'Referer': 'https://www.amazon.com/',
        'Host': 'www.amazon.com'
    }
    return spider(url=url, headers=header, daili=daili)


def geturl(url):

if __name__ == "__main__":
    a = time.clock()
    url = "https://www.amazon.com/"
    daili = "146.148.179.174:808"
    err = 0
    success = 0
    robot = 0
    for i in range(100):
        try:
            data = alone(url, daili)
            # with open("./file/"+daili.split(":")[0]+".html","wb") as f:
            #     f.write(data)
            success = success + 1
            if "Robot Check" in data.decode("utf-8", "ignore"):
                robot = robot + 1
        except Exception as e:
            print(e)
            err = err + 1
        print(i,success,err,robot)
    b = time.clock()
    today = time.strftime('%Y%m%d', time.localtime())

    print('运行时间：' + timetochina(b - a))
