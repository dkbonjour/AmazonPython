# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/10.
# 功能:
# http://docs.python-requests.org/zh_CN/latest/user/advanced.html#advanced

import requests
# 遇到网络问题（如：DNS 查询失败、拒绝连接等）时，Requests 会抛出一个 ConnectionError 异常。
#
# 如果 HTTP 请求返回了不成功的状态码， Response.raise_for_status() 会抛出一个 HTTPError 异常。
#
# 若请求超时，则抛出一个 Timeout 异常。
#
# 若请求超过了设定的最大重定向次数，则会抛出一个 TooManyRedirects 异常。
#
# 所有Requests显式抛出的异常都继承自 requests.exceptions.RequestException 。

def testget(url):
    header = {
        'User-Agent':
            'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        # 'Host': 'www.ip138.com',
    }
    res = requests.get(url, headers=header, timeout=10)

    # 二进制内容
    print(type(res.content), res.content)

    # 解码
    print(res.encoding)
    res.encoding = "utf-8"

    # 字符串内容
    print(type(res.text), res.text)

    # 原始套接字内容
    # res = requests.get(url, stream=True)
    # # raws=res.raw
    # # print(raws.read(10))
    # filename = "./request.txt"
    # chunk_size = 1000
    # with open(filename, 'wb') as fd:
    #     for chunk in res.iter_content(chunk_size):
    #         fd.write(chunk)


def testpost(url1):
    payload = {'key1': 'value1', 'key2': 'value2'}
    r = requests.post(url1, data=payload)
    print(r.text)
    # print(r.json())

    r = requests.post(url1, json=payload)
    print(r.text)
    # print(r.json())


    files = {'file': open('cookie.txt', 'rb')}  #推荐这种
    files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
    files = {'file': ('cookie.txt', open('cookie.txt', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
    r = requests.post(url1, files=files)
    print(r.text)

def testcode():
    bad_r = requests.get('http://httpbin.org/status/403')
    print(bad_r.status_code)
    print(requests.codes.ok)

    ## 非200抛出异常
    bad_r.raise_for_status()

def testheader():
    cookies = dict(cookies_are='working')
    bad_r = requests.get('http://httpbin.org/cookies',cookies=cookies,allow_redirects=False)
    print(type(bad_r.headers),bad_r.headers)
    print(type(bad_r.cookies),bad_r.cookies)
    print(bad_r.text)

    print(bad_r.history)

def testposta(url1):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
        'Referer': 'https://www.amazon.com/',
        'Host': 'www.amazon.com'
    }
    payload = {"asin": "B009ZJ2M7G","pageAction":"load"}
    r = requests.post(url1, data=payload,headers=header)
    print(r.text)
    with open("../test.html","wb") as f:
        f.write(r.content)

if __name__ == "__main__":
    url = "http://www.baidu.com"
    # testget(url)

    url1 = "http://httpbin.org/post"
    # testpost(url1)

    # testcode()

    testheader()

    # url="https://www.amazon.com/gp/product/ajax-handlers/enhanced-content-popover-metrics.html"
    # testposta(url)