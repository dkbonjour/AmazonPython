# -*-coding:utf-8-*-
# Created by 一只尼玛 on 16-8-26.
# 功能:
# 　抓取网页
#
import urllib.request, urllib.parse, http.cookiejar
import os, time, re
import http.cookies
import requests
from tool.jfile.file import *


# star 自己封装的抓取函数,单机应用,单进程，多进程可能全局变量多用
def spider(url, proxies={}, postdata={}, headers={}, ua="ua", path=".", timeout=60):
    try:
        """
        抓取网页：支持cookie
        第一个参数为网址，第二个为POST的数据
        """
        createjia(path)
        # 头部重包
        header = []
        for i in headers:
            header.append((i, headers[i]))
        # print(header)

        # COOKIE文件保存路径
        filename = path + "/" + ua + '-cookie.txt'
        try:
            # proxies = {
            #     'http': 'socks5://user:pass@host:port',
            #     'https': 'socks5://user:pass@host:port'
            # 'https': 'socks5://host:port'
            # }
            try:
                temp = proxies["http"]
            except:
                temp = proxies["https"]
            ip = validateTitle(temp)
            filename = path + "/" + ip + "-" + ua + '.txt'
        except Exception as e:
            print(e)

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
        # 开启代理支持
        if proxies:
            # 建造带有COOKIE处理器的打开专家
            opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies),
                                                 urllib.request.HTTPCookieProcessor(cj),
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
            html_bytes = urllib.request.urlopen(url=url, data=postdata.encode(), timeout=timeout).read()
        else:
            html_bytes = urllib.request.urlopen(url=url, timeout=timeout).read()

        # 保存COOKIE到文件中
        cj.save(ignore_discard=True, ignore_expires=True)
    except Exception as e:
        if hasattr(e, 'code'):
            e = Exception('页面不存在或时间太长.Error code:' + str(e.code))
            if e.code == 404:
                e = Exception('404错误，忽略')
        elif hasattr(e, 'reason'):
            e = Exception("无法到达主机.Reason:" + str(e.reason))
        raise e
    return html_bytes


# star 数据URL转义
def urlencode(postdata={}):
    return urllib.parse.urlencode(postdata)


# 多进程爬虫
def mulspider(url, proxies={}, postdata={}, headers={}, ua="ua", path=".", timeout=60):
    try:
        """
        抓取网页：支持cookie
        第一个参数为网址，第二个为POST的数据
        """
        createjia(path)
        # 头部重包
        header = []
        for i in headers:
            header.append((i, headers[i]))
        # print(header)

        # COOKIE文件保存路径
        filename = path + "/" + ua + '-cookie.txt'
        try:
            # proxies = {
            #     'http': 'socks5://user:pass@host:port',
            #     'https': 'socks5://user:pass@host:port'
            # 'https': 'socks5://host:port'
            # }
            try:
                temp = proxies["http"]
            except:
                temp = proxies["https"]
            ip = validateTitle(temp)
            filename = path + "/" + ip + "-" + ua + '.txt'
        except Exception as e:
            pass

        # 声明一个MozillaCookieJar对象实例保存在文件中
        cj = http.cookiejar.MozillaCookieJar(filename)
        # cj =http.cookiejar.LWPCookieJar(filename)

        # 从文件中读取cookie内容到变量
        # ignore_discard的意思是即使cookies将被丢弃也将它保存下来
        # ignore_expires的意思是如果在该文件中 cookies已经存在，则覆盖原文件写
        # 如果存在，则读取主要COOKIE
        if os.path.exists(filename):
            cj.load(filename, ignore_discard=True, ignore_expires=True)
        else:
            # TODO
            # 以手机形式访问
            # https://www.amazon.com/gp/anywhere/site-view.html/ref=footer_opt_in_mobile?ie=UTF8&opt=mobile&url=/gp/aw
            dudu = "https://www.amazon.com/gp/anywhere/site-view.html/ref=footer_opt_in_mobile?ie=UTF8&opt=mobile&url=%2Fgp%2Faw"
            dddmulspider(url="https://www.amazon.com", proxies=proxies, headers=headers, ua=ua, path=path,
                         timeout=timeout)
            time.sleep(8)
            dddmulspider(url=dudu, proxies=proxies, headers=headers, ua=ua, path=path, timeout=timeout)
            time.sleep(8)

        # 读取其他COOKIE
        if os.path.exists('../subcookie.txt'):
            cookie = open('../subcookie.txt', 'r').read()
        else:
            cookie = ''
        # 开启代理支持
        if proxies:
            # 建造带有COOKIE处理器的打开专家
            opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies),
                                                 urllib.request.HTTPCookieProcessor(cj),
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

        # 有数据需要POST
        if postdata:
            # 数据URL编码
            postdata = urllib.parse.urlencode(postdata)

            # 抓取网页
            html_bytes = opener.open(fullurl=url, data=postdata.encode(), timeout=timeout).read()
        else:
            html_bytes = opener.open(fullurl=url, timeout=timeout).read()

        # 保存COOKIE到文件中
        cj.save(ignore_discard=True, ignore_expires=True)
    except Exception as e:
        if hasattr(e, 'code'):
            e = Exception('页面不存在或时间太长.Error code:' + str(e.code))
            if e.code == 404:
                e = Exception('404错误，忽略')
        elif hasattr(e, 'reason'):
            e = Exception("无法到达主机.Reason:" + str(e.reason))
        if "timed out" in str(e):
            e = Exception("网络超时")
        raise e
    return html_bytes


# 多进程爬虫
def dddmulspider(url, proxies={}, postdata={}, headers={}, ua="ua", path=".", timeout=60):
    try:
        """
        抓取网页：支持cookie
        第一个参数为网址，第二个为POST的数据
        """
        createjia(path)
        # 头部重包
        header = []
        for i in headers:
            header.append((i, headers[i]))
        # print(header)

        # COOKIE文件保存路径
        filename = path + "/" + ua + '-cookie.txt'
        try:
            # proxies = {
            #     'http': 'socks5://user:pass@host:port',
            #     'https': 'socks5://user:pass@host:port'
            # 'https': 'socks5://host:port'
            # }
            try:
                temp = proxies["http"]
            except:
                temp = proxies["https"]
            ip = validateTitle(temp)
            filename = path + "/" + ip + "-" + ua + '.txt'
        except Exception as e:
            pass

        # 声明一个MozillaCookieJar对象实例保存在文件中
        cj = http.cookiejar.MozillaCookieJar(filename)
        # cj =http.cookiejar.LWPCookieJar(filename)

        # 从文件中读取cookie内容到变量
        # ignore_discard的意思是即使cookies将被丢弃也将它保存下来
        # ignore_expires的意思是如果在该文件中 cookies已经存在，则覆盖原文件写
        # 如果存在，则读取主要COOKIE
        if os.path.exists(filename):
            cj.load(filename, ignore_discard=True, ignore_expires=True)
        else:
            # TODO
            # 以手机形式访问
            # https://www.amazon.com/gp/anywhere/site-view.html/ref=footer_opt_in_mobile?ie=UTF8&opt=mobile&url=/gp/aw
            # spider(url=url, headers=header, ua=ua, path=path,timeout=timeout)
            pass
        # 读取其他COOKIE
        if os.path.exists('../subcookie.txt'):
            cookie = open('../subcookie.txt', 'r').read()
        else:
            cookie = ''
        # 开启代理支持
        if proxies:
            # 建造带有COOKIE处理器的打开专家
            opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies),
                                                 urllib.request.HTTPCookieProcessor(cj),
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

        # 有数据需要POST
        if postdata:
            # 数据URL编码
            postdata = urllib.parse.urlencode(postdata)

            # 抓取网页
            html_bytes = opener.open(fullurl=url, data=postdata.encode(), timeout=timeout).read()
        else:
            html_bytes = opener.open(fullurl=url, timeout=timeout).read()

        # 保存COOKIE到文件中
        cj.save(ignore_discard=True, ignore_expires=True)
    except Exception as e:
        if hasattr(e, 'code'):
            e = Exception('页面不存在或时间太长.Error code:' + str(e.code))
            if e.code == 404:
                e = Exception('404错误，忽略')
        elif hasattr(e, 'reason'):
            e = Exception("无法到达主机.Reason:" + str(e.reason))
        if "timed out" in str(e):
            e = Exception("网络超时")
        raise e
    return html_bytes


if __name__ == "__main__":
    ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'User-Agent': ua,
        # "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept-Language": "en-US;q=0.8,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        # 'Referer': 'https://www.amazon.com/',
        'Host': 'www.amazon.com'
    }
    # ip="http://smart:smart2016@146.148.149.209:808"
    # ip = "http://36.42.32.32:8080"
    # proxies = {"http": ip}
    url = "https://www.amazon.com/dp/B000TYSB8K"
    # data=requests.get(url=url, headers=header, proxies=proxies, timeout=60)
    # print(data.text)
    resdata = mulspider(url=url, headers=header, ua="1", timeout=5)
    print(resdata.decode("utf-8", "ignore"))
