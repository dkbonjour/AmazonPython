# -*-coding:utf-8-*-
# Created by 一只尼玛 on 16-8-26.
# 功能:
# 　抓取网页
import urllib.request, urllib.parse, http.cookiejar
import os, time, re
import http.cookies


# 自己封装的抓取函数
def getHtml(url, daili='', postdata={}, header=[]):
    """
    抓取网页：支持cookie
    第一个参数为网址，第二个为POST的数据
    """
    # COOKIE文件保存路径
    filename = 'cookie.txt'

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
        print('代理:' + daili + '启动')
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


def urlencode(postdata={}):
    return urllib.parse.urlencode(postdata)


if __name__ == "__main__":
    # print(getHtml("http://www.baidu.com").decode("utf-8", "ignore"))

    url = "http://dd.com?" + urlencode({"dd": "Ddd", "你好": 3})
    print(url)
